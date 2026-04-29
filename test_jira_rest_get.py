#!/usr/bin/env python3
"""Quick test script for jira_rest_get tool via MCP SSE."""

import json
import queue
import threading
import sys
import time
import requests

BASE_URL = "http://localhost:9200"


def open_sse_session() -> tuple[str, queue.Queue]:
    """Open SSE connection, return (session_id, event_queue). Keeps connection alive."""
    session_id = None
    ready = threading.Event()
    event_queue = queue.Queue()

    def stream():
        nonlocal session_id
        with requests.get(f"{BASE_URL}/sse", stream=True, timeout=120) as r:
            for line in r.iter_lines():
                if line:
                    decoded = line.decode()
                    if decoded.startswith("data:"):
                        data = decoded[5:].strip()
                        if session_id is None and "session_id=" in data:
                            session_id = data.split("session_id=")[1]
                            ready.set()
                        else:
                            event_queue.put(data)

    t = threading.Thread(target=stream, daemon=True)
    t.start()
    ready.wait(timeout=5)
    return session_id, event_queue


def send_initialize(session_id: str):
    payload = {
        "jsonrpc": "2.0",
        "id": 0,
        "method": "initialize",
        "params": {
            "protocolVersion": "2024-11-05",
            "capabilities": {},
            "clientInfo": {"name": "test-client", "version": "0.1"},
        },
    }
    requests.post(f"{BASE_URL}/messages/?session_id={session_id}", json=payload, timeout=10)

    notify = {
        "jsonrpc": "2.0",
        "method": "notifications/initialized",
        "params": {},
    }
    requests.post(f"{BASE_URL}/messages/?session_id={session_id}", json=notify, timeout=10)


def call_tool(session_id: str, call_id: int, path: str, query: dict = None) -> tuple[int, str]:
    payload = {
        "jsonrpc": "2.0",
        "id": call_id,
        "method": "tools/call",
        "params": {
            "name": "jira_rest_get",
            "arguments": {"path": path, **({"query": query} if query else {})},
        },
    }
    r = requests.post(
        f"{BASE_URL}/messages/?session_id={session_id}",
        json=payload,
        timeout=10,
    )
    return r.status_code, r.text


def wait_for_response(event_queue: queue.Queue, call_id: int, timeout: float = 10.0) -> dict | None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            raw = event_queue.get(timeout=0.5)
            try:
                data = json.loads(raw)
                if isinstance(data, dict) and data.get("id") == call_id:
                    return data
            except json.JSONDecodeError:
                pass
        except queue.Empty:
            continue
    return None


def run_upstream_error_test(label: str, session_id: str, event_queue: queue.Queue,
                            call_id: int, path: str, query: dict = None,
                            expect_status: int = None):
    """Test that Jira upstream errors (404, 401, etc.) surface correctly in body.status."""
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"PATH: {path}" + (f" | QUERY: {query}" if query else ""))
    print(f"Expecting: body.status == {expect_status}")

    http_status, _ = call_tool(session_id, call_id, path, query)
    print(f"HTTP status: {http_status} (202 = accepted by MCP)")

    response = wait_for_response(event_queue, call_id)
    if response is None:
        print("TIMEOUT: No response received via SSE")
        return

    result = response.get("result", {})
    content = result.get("content", [{}])
    text = content[0].get("text", "") if content else ""

    # MCP surfaces upstream errors as: "Error calling tool 'rest_get': {json}"
    # Extract the JSON part regardless of prefix
    json_text = text
    if text.startswith("Error calling tool"):
        idx = text.find("{")
        if idx != -1:
            json_text = text[idx:]

    try:
        data = json.loads(json_text)
        actual_status = data.get("status")
        if actual_status == expect_status:
            print(f"[UPSTREAM ERROR SURFACED] code={data.get('code')}, status={actual_status}")
            print(f"body: {json.dumps(data.get('body', {}))[:200]}")
            print("OK (upstream error propagated correctly)")
        else:
            print(f"UNEXPECTED: got status={actual_status}, expected {expect_status}")
            print(f"Full response: {text[:300]}")
            print("FAIL")
    except (json.JSONDecodeError, AttributeError):
        print(f"Could not parse response: {text[:300]}")
        print("FAIL")


def run_test(label: str, session_id: str, event_queue: queue.Queue, call_id: int,
             path: str, query: dict = None, expect_error: bool = False):
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"PATH: {path}" + (f" | QUERY: {query}" if query else ""))

    http_status, _ = call_tool(session_id, call_id, path, query)
    print(f"HTTP status: {http_status} (202 = accepted by MCP)")

    response = wait_for_response(event_queue, call_id)
    if response is None:
        print("TIMEOUT: No response received via SSE")
        return

    result = response.get("result", {})
    content = result.get("content", [{}])
    text = content[0].get("text", "") if content else ""

    is_error = "error" in response or "path_not_allowed" in text or text.startswith("Error calling tool")

    if expect_error:
        if is_error:
            print(f"[EXPECTED ERROR] {text}")
            print("OK (blocked as expected)")
        else:
            print(f"UNEXPECTED SUCCESS (should have been blocked): {text}")
            print("FAIL")
    else:
        if is_error:
            print(f"UNEXPECTED ERROR: {text}")
            print("FAIL")
        else:
            print(f"Result:\n{text}")
            print("OK")


def call_update_sprint(session_id: str, call_id: int, **kwargs) -> tuple[int, str]:
    """Call jira_update_sprint tool with given arguments."""
    payload = {
        "jsonrpc": "2.0",
        "id": call_id,
        "method": "tools/call",
        "params": {
            "name": "jira_update_sprint",
            "arguments": kwargs,
        },
    }
    r = requests.post(
        f"{BASE_URL}/messages/?session_id={session_id}",
        json=payload,
        timeout=10,
    )
    return r.status_code, r.text


def run_update_sprint_test(label: str, session_id: str, event_queue: queue.Queue,
                           call_id: int, expect_error: bool = False,
                           expect_error_code: str = None, **kwargs):
    """Test jira_update_sprint tool."""
    print(f"\n{'='*60}")
    print(f"TEST: {label}")
    print(f"ARGS: {kwargs}")

    http_status, _ = call_update_sprint(session_id, call_id, **kwargs)
    print(f"HTTP status: {http_status} (202 = accepted by MCP)")

    response = wait_for_response(event_queue, call_id)
    if response is None:
        print("TIMEOUT: No response received via SSE")
        return

    result = response.get("result", {})
    content = result.get("content", [{}])
    text = content[0].get("text", "") if content else ""

    is_error = "error" in response or text.startswith("Error calling tool")

    if expect_error:
        if is_error:
            # Extract JSON from error text
            json_text = text
            if text.startswith("Error calling tool"):
                idx = text.find("{")
                if idx != -1:
                    json_text = text[idx:]
            try:
                data = json.loads(json_text)
                actual_code = data.get("code")
                if expect_error_code and actual_code != expect_error_code:
                    print(f"UNEXPECTED ERROR CODE: got={actual_code}, expected={expect_error_code}")
                    print("FAIL")
                else:
                    print(f"[EXPECTED ERROR] code={actual_code}")
                    print("OK (error surfaced correctly)")
            except (json.JSONDecodeError, AttributeError):
                print(f"[EXPECTED ERROR] {text[:200]}")
                print("OK (error surfaced correctly)")
        else:
            print(f"UNEXPECTED SUCCESS (should have errored): {text[:200]}")
            print("FAIL")
    else:
        if is_error:
            print(f"UNEXPECTED ERROR: {text[:200]}")
            print("FAIL")
        else:
            try:
                data = json.loads(text)
                print(f"status={data.get('status')} body={json.dumps(data.get('body', {}))[:200]}")
                print("OK")
            except json.JSONDecodeError:
                print(f"Result: {text[:200]}")
                print("OK")


def main():
    global BASE_URL
    BASE_URL = sys.argv[1] if len(sys.argv) > 1 else BASE_URL

    print(f"Connecting to {BASE_URL} ...")
    session_id, event_queue = open_sse_session()
    if not session_id:
        print("ERROR: Could not get session_id from SSE endpoint")
        sys.exit(1)
    print(f"Session ID: {session_id}")

    send_initialize(session_id)
    time.sleep(0.5)  # let initialize response flush through

    call_id = 1
    run_test("List projects (v2)", session_id, event_queue, call_id,
             "/rest/api/2/project", {"startAt": 0, "maxResults": 3})
    call_id += 1
    run_test("Search user by email (v2)", session_id, event_queue, call_id,
             "/rest/api/2/user/search", {"username": "kiennv@savameta.com"})
    call_id += 1
    run_test("List boards", session_id, event_queue, call_id,
             "/rest/agile/1.0/board", {"startAt": 0, "maxResults": 3})
    call_id += 1
    run_test("Myself (v2)", session_id, event_queue, call_id,
             "/rest/api/2/myself")
    call_id += 1
    # Board 91 = LLA Board (LumiAI project), has active sprint "LLA Sprint 19"
    run_test("List sprints (board 91 - LLA Board)", session_id, event_queue, call_id,
             "/rest/agile/1.0/board/91/sprint", {"startAt": 0, "maxResults": 5})
    call_id += 1
    # Sprint 220 = LLA Sprint 19 (active), board 91 = LLA Board
    run_test("Get sprint issues (sprint 220 - LLA Sprint 19)", session_id, event_queue, call_id,
             "/rest/agile/1.0/sprint/220/issue", {"startAt": 0, "maxResults": 10})
    call_id += 1
    run_test("BLOCKED: admin endpoint", session_id, event_queue, call_id,
             "/rest/api/2/configuration", expect_error=True)
    call_id += 1
    run_test("BLOCKED: permissions endpoint", session_id, event_queue, call_id,
             "/rest/api/2/permissions", expect_error=True)
    call_id += 1
    # Upstream error propagation: Jira 404 should surface as body.status=404
    run_upstream_error_test("UPSTREAM 404: non-existent board", session_id, event_queue, call_id,
                            "/rest/agile/1.0/board/999999/sprint", expect_status=404)
    call_id += 1
    run_upstream_error_test("UPSTREAM 404: non-existent sprint", session_id, event_queue, call_id,
                            "/rest/agile/1.0/sprint/999999/issue", expect_status=404)
    call_id += 1
    # NOTE: 401 test not included — MCP credentials are fixed in server env and cannot be
    # overridden via tool arguments by design. To test 401, temporarily use wrong credentials
    # in the server's .env.atlassian and restart the container.

    # --- jira_update_sprint tests ---
    # Safe: update sprint 220 with same name (no actual change)
    run_update_sprint_test(
        "UPDATE SPRINT: happy path (safe — same name, no actual change)",
        session_id, event_queue, call_id,
        sprint_id=220, name="LLA Sprint 19",
    )
    call_id += 1
    # Error: non-existent sprint id → expect 404
    run_update_sprint_test(
        "UPDATE SPRINT: non-existent sprint id → expect 404",
        session_id, event_queue, call_id,
        expect_error=True, expect_error_code="jira_not_found",
        sprint_id=999999, name="ghost sprint",
    )
    call_id += 1
    # Error: no fields provided → expect no_fields validation error
    run_update_sprint_test(
        "UPDATE SPRINT: no fields provided → expect no_fields error",
        session_id, event_queue, call_id,
        expect_error=True, expect_error_code="no_fields",
        sprint_id=220,
    )

    print(f"\n{'='*60}")
    print("Done.")


if __name__ == "__main__":
    main()
