# jira_rest_get — Integration Guide for Point Poker

**Date:** 2026-04-28  
**Status:** Tested & Verified on production MCP server (jira.savameta.com)

---

## Overview

`jira_rest_get` là một MCP tool được thêm vào custom fork của `mcp-atlassian`.  
Tool này cho phép Point Poker gọi trực tiếp Jira REST API (read-only GET) thông qua MCP server — sử dụng lại credentials của service account đã cấu hình, không cần Point Poker tự quản lý Jira token.

**Chỉ cho phép GET. Không có quyền ghi/sửa/xóa.**

---

## Tool Signature

```
Tool name: jira_rest_get

Parameters:
  path   (string, required) — Jira REST path bắt đầu bằng /rest/
  query  (object, optional) — Query string parameters dạng key-value
```

---

## Allowlist (Các path được phép)

Chỉ các prefix sau mới được phép gọi:

| Prefix | Mô tả |
|--------|-------|
| `/rest/api/2/myself` | Thông tin service account |
| `/rest/api/2/project` | Danh sách / chi tiết project |
| `/rest/api/2/issue/{idOrKey}` | Chi tiết issue |
| `/rest/api/2/search` | JQL search |
| `/rest/api/2/user` | Lookup user theo username/email |
| `/rest/agile/1.0/board` | Danh sách boards |
| `/rest/agile/1.0/sprint/{id}` | Chi tiết sprint |

Các path ngoài danh sách trên sẽ bị block với lỗi `path_not_allowed`.

> **Note:** Đây là Jira Server (self-hosted) — dùng API v2, không phải v3 (Jira Cloud).

---

## Response Format

```json
{
  "status": 200,
  "body": { ... }
}
```

Khi lỗi (path bị block hoặc Jira trả lỗi):

```
Error calling tool 'rest_get': {"code": "path_not_allowed", "path": "/rest/api/2/configuration"}
```

---

## Tested Endpoints & Sample Responses

### 1. List Projects

**Request:**
```
path:  /rest/api/2/project
query: { "startAt": 0, "maxResults": 3 }
```

**Response (status 200):**
```json
[
  { "id": "10917", "key": "AIM", "name": "AI Metaverse", "projectTypeKey": "software", "archived": false },
  { "id": "10807", "key": "BG",  "name": "Breeding-Dino", "projectTypeKey": "software", "archived": false },
  { "id": "10808", "key": "BRH", "name": "Breeding-HotPot", "projectTypeKey": "software", "archived": false }
]
```

Tổng có 18 projects active. Dùng `startAt` + `maxResults` để phân trang.

<details>
<summary>Raw test output</summary>

```
TEST: List projects (v2)
PATH: /rest/api/2/project | QUERY: {'startAt': 0, 'maxResults': 3}
HTTP status: 202 (202 = accepted by MCP)
Result:
{"status": 200, "body": [{"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10917", "id": "10917", "key": "AIM", "name": "AI Metaverse", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10807", "id": "10807", "key": "BG", "name": "Breeding-Dino", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10808", "id": "10808", "key": "BRH", "name": "Breeding-HotPot", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10902", "id": "10902", "key": "GS", "name": "Game Studio", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10905", "id": "10905", "key": "GAME", "name": "Game3", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10906", "id": "10906", "key": "GAM4", "name": "Game4", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10907", "id": "10907", "key": "GAME05", "name": "HoleAway", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10913", "id": "10913", "key": "LOP", "name": "Lizard Out", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10908", "id": "10908", "key": "LLA", "name": "LumiAI", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10916", "id": "10916", "key": "LBA", "name": "LumiBrand AI", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10904", "id": "10904", "key": "GMKT", "name": "Marketing", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10911", "id": "10911", "key": "MIN", "name": "Mini-Games", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?pid=10911&avatarId=10011", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&pid=10911&avatarId=10011", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&pid=10911&avatarId=10011", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&pid=10911&avatarId=10011"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10900", "id": "10900", "key": "MWC", "name": "Music World Concept", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10910", "id": "10910", "key": "SBP", "name": "Sava Blockchain Project", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10918", "id": "10918", "key": "SSF", "name": "Sava Studio Framework", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10025", "id": "10025", "key": "POPM", "name": "Savrse POM", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10810", "id": "10810", "key": "SAV", "name": "SAVRSE-Architect", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}, {"expand": "description,lead,url,projectKeys", "self": "https://jira.savameta.com/rest/api/2/project/10915", "id": "10915", "key": "UAG", "name": "Unmaze Arrow", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/projectavatar?avatarId=10324", "24x24": "https://jira.savameta.com/secure/projectavatar?size=small&avatarId=10324", "16x16": "https://jira.savameta.com/secure/projectavatar?size=xsmall&avatarId=10324", "32x32": "https://jira.savameta.com/secure/projectavatar?size=medium&avatarId=10324"}, "projectTypeKey": "software", "archived": false}]}
OK
```

</details>

---

### 2. Lookup User by Email (accountId)

**Request:**
```
path:  /rest/api/2/user/search
query: { "username": "kiennv@savameta.com" }
```

> Note: Jira Server dùng param `username=`, không phải `query=` (đó là Jira Cloud).

**Response (status 200):**
```json
[
  {
    "key": "JIRAUSER11232",
    "name": "kiennv@savameta.com",
    "emailAddress": "kiennv@savameta.com",
    "displayName": "Kien Nguyen Van",
    "active": true,
    "timeZone": "Asia/Ho_Chi_Minh"
  }
]
```

Field `key` (`JIRAUSER11232`) là `accountId` dùng để assign issue trên Jira Server.

<details>
<summary>Raw test output</summary>

```
TEST: Search user by email (v2)
PATH: /rest/api/2/user/search | QUERY: {'username': 'kiennv@savameta.com'}
HTTP status: 202 (202 = accepted by MCP)
Result:
{"status": 200, "body": [{"self": "https://jira.savameta.com/rest/api/2/user?username=kiennv@savameta.com", "key": "JIRAUSER11232", "name": "kiennv@savameta.com", "emailAddress": "kiennv@savameta.com", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/useravatar?ownerId=JIRAUSER11232&avatarId=11428", "24x24": "https://jira.savameta.com/secure/useravatar?size=small&ownerId=JIRAUSER11232&avatarId=11428", "16x16": "https://jira.savameta.com/secure/useravatar?size=xsmall&ownerId=JIRAUSER11232&avatarId=11428", "32x32": "https://jira.savameta.com/secure/useravatar?size=medium&ownerId=JIRAUSER11232&avatarId=11428"}, "displayName": "Kien Nguyen Van", "active": true, "deleted": false, "timeZone": "Asia/Ho_Chi_Minh", "locale": "en_US"}]}
OK
```

</details>

---

### 3. List Boards

**Request:**
```
path:  /rest/agile/1.0/board
query: { "startAt": 0, "maxResults": 3 }
```

**Response (status 200):**
```json
{
  "maxResults": 3,
  "startAt": 0,
  "total": 26,
  "isLast": false,
  "values": [
    { "id": 69, "name": "1",        "type": "scrum" },
    { "id": 74, "name": "AAP board","type": "scrum" },
    { "id": 88, "name": "AIM board","type": "kanban" }
  ]
}
```

Tổng có 26 boards. Dùng `startAt` để phân trang.

<details>
<summary>Raw test output</summary>

```
TEST: List boards
PATH: /rest/agile/1.0/board | QUERY: {'startAt': 0, 'maxResults': 3}
HTTP status: 202 (202 = accepted by MCP)
Result:
{"status": 200, "body": {"maxResults": 3, "startAt": 0, "total": 26, "isLast": false, "values": [{"id": 69, "self": "https://jira.savameta.com/rest/agile/1.0/board/69", "name": "1", "type": "scrum"}, {"id": 74, "self": "https://jira.savameta.com/rest/agile/1.0/board/74", "name": "AAP board", "type": "scrum"}, {"id": 88, "self": "https://jira.savameta.com/rest/agile/1.0/board/88", "name": "AIM board", "type": "kanban"}]}}
OK
```

</details>

---

### 4. Myself (Service Account Info)

**Request:**
```
path: /rest/api/2/myself
```

**Response (status 200):**
```json
{
  "key": "JIRAUSER11232",
  "name": "kiennv@savameta.com",
  "emailAddress": "kiennv@savameta.com",
  "displayName": "Kien Nguyen Van",
  "active": true,
  "timeZone": "Asia/Ho_Chi_Minh",
  "locale": "en_US"
}
```

<details>
<summary>Raw test output</summary>

```
TEST: Myself (v2)
PATH: /rest/api/2/myself
HTTP status: 202 (202 = accepted by MCP)
Result:
{"status": 200, "body": {"self": "https://jira.savameta.com/rest/api/2/user?username=kiennv@savameta.com", "key": "JIRAUSER11232", "name": "kiennv@savameta.com", "emailAddress": "kiennv@savameta.com", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/useravatar?ownerId=JIRAUSER11232&avatarId=11428", "24x24": "https://jira.savameta.com/secure/useravatar?size=small&ownerId=JIRAUSER11232&avatarId=11428", "16x16": "https://jira.savameta.com/secure/useravatar?size=xsmall&ownerId=JIRAUSER11232&avatarId=11428", "32x32": "https://jira.savameta.com/secure/useravatar?size=medium&ownerId=JIRAUSER11232&avatarId=11428"}, "displayName": "Kien Nguyen Van", "active": true, "deleted": false, "timeZone": "Asia/Ho_Chi_Minh", "locale": "en_US", "groups": {"size": 1, "items": []}, "applicationRoles": {"size": 1, "items": []}, "expand": "groups,applicationRoles"}}
OK
```

</details>

---

### 6. List Sprints (by Board)

**Request:**
```
path:  /rest/agile/1.0/board/91/sprint
query: { "startAt": 0, "maxResults": 5 }
```

**Response (status 200, excerpt):**
```json
{
  "maxResults": 5,
  "startAt": 0,
  "isLast": false,
  "values": [
    {
      "id": 220,
      "name": "LLA Sprint 19",
      "state": "active",
      "startDate": "2025-04-14T02:00:00.000Z",
      "endDate": "2025-04-27T02:00:00.000Z",
      "originBoardId": 91
    },
    {
      "id": 216,
      "name": "LLA Sprint 18",
      "state": "closed",
      "originBoardId": 91
    }
  ]
}
```

Để lấy sprint đang active: lọc `"state": "active"` trong `values`. Sprint 220 = LLA Sprint 19 đang active tại thời điểm test.

> **Note:** Jira Server có thể trả về sprints từ board khác trong response (field `originBoardId` khác với board ID trong URL). Đây là behavior bình thường — lọc theo `originBoardId` hoặc `state` nếu cần chính xác.

<details>
<summary>Raw test output</summary>

```
TEST: List sprints (board 91 - LLA Board)
PATH: /rest/agile/1.0/board/91/sprint | QUERY: {'startAt': 0, 'maxResults': 5}
HTTP status: 202 (202 = accepted by MCP)
Result:
{"status": 200, "body": {"maxResults": 5, "startAt": 0, "isLast": false, "values": [{"id": 176, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/176", "state": "closed", "name": "AAP Sprint 2", "startDate": "2024-10-14T08:10:26.557Z", "endDate": "2024-10-27T08:10:00.000Z", "completeDate": "2024-10-28T02:48:42.614Z", "originBoardId": 74}, {"id": 177, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/177", "state": "closed", "name": "AAP Sprint 3", "startDate": "2024-10-28T03:10:46.574Z", "endDate": "2024-11-10T03:10:00.000Z", "completeDate": "2024-11-11T04:17:06.793Z", "originBoardId": 74}, {"id": 178, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/178", "state": "closed", "name": "AAP Sprint 4", "startDate": "2024-11-11T04:17:26.726Z", "endDate": "2024-11-24T04:17:00.000Z", "completeDate": "2024-11-25T09:52:02.014Z", "originBoardId": 74}, {"id": 209, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/209", "state": "closed", "name": "LLA Sprint 13", "startDate": "2025-01-20T09:00:00.000Z", "endDate": "2025-02-02T09:00:00.000Z", "completeDate": "2025-02-05T09:01:56.498Z", "originBoardId": 91}, {"id": 210, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/210", "state": "closed", "name": "LLA Sprint 14", "startDate": "2025-02-03T09:00:00.000Z", "endDate": "2025-02-16T09:00:00.000Z", "completeDate": "2025-02-18T04:32:39.019Z", "originBoardId": 91}]}}
OK
```

</details>

---

### 7. Get Sprint Issues

**Request:**
```
path:  /rest/agile/1.0/sprint/220/issue
query: { "startAt": 0, "maxResults": 10 }
```

**Response (status 200, excerpt — 1 issue):**
```json
{
  "startAt": 0,
  "maxResults": 10,
  "total": 42,
  "issues": [
    {
      "id": "23010",
      "key": "LLA-882",
      "fields": {
        "summary": "Onboarding for new user - đi từ web",
        "issuetype": { "name": "Task", "subtask": false },
        "status": { "name": "In Dev" },
        "assignee": { "key": "JIRAUSER11234", "displayName": "Khoi Tran Trong" },
        "customfield_10031": 8.0,
        "customfield_10016": null
      }
    }
  ]
}
```

Sprint 220 (LLA Sprint 19) có tổng 42 issues. Page đầu (10 issues) gồm Task + Story, không có Sub-task. Dùng `startAt` để phân trang.

**10 issues trong page đầu:**

| Key | Summary | Type | SP | Status |
|-----|---------|------|----|--------|
| LLA-882 | Onboarding for new user - đi từ web | Task | 8 | In Dev |
| LLA-892 | User Settings | Story | 0 | Planning |
| LLA-889 | [DC] Create Department | Story | 0 | Ready For Dev |
| LLA-891 | [DC] Collaboration Style for department | Story | 0 | Ready For Dev |
| LLA-895 | [DC] Invite User (tại Create department) | Story | 0 | Ready For Dev |
| LLA-897 | [DC] Onboarding for new user đi từ Internal Invitation | Story | 8 | Planning |
| LLA-878 | [DDM] Set-up Roles & Permissions | Story | 13 | Planning |
| LLA-900 | [DDM] Manage Roles & Permissions | Story | 8 | Planning |
| LLA-879 | [DDM] Department - Working Folder | Story | 13 | In Dev |
| LLA-881 | [DDM] Share Documents to Department | Story | 8 | Planning |

> **CRITICAL — Story Points field:**  
> Sava Meta Jira Server dùng **`customfield_10031`** cho Story Points (giá trị ví dụ: `8.0`, `13.0`).  
> **`customfield_10016` luôn là `null`** trên hệ thống này — không dùng field đó.  
> Point Poker phải đọc `customfield_10031`, không phải `customfield_10016`.

<details>
<summary>Raw test output</summary>

```
TEST: Get sprint issues (sprint 220 - LLA Sprint 19)
PATH: /rest/agile/1.0/sprint/220/issue | QUERY: {'startAt': 0, 'maxResults': 10}
HTTP status: 202 (202 = accepted by MCP)
Result:
{"status": 200, "body": {"expand": "schema,names", "startAt": 0, "maxResults": 10, "total": 42, "issues": [{"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23010", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23010", "key": "LLA-882", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10002", "id": "10002", "description": "A small, distinct piece of work.", "iconUrl": "https://jira.savameta.com/secure/viewavatar?size=xsmall&avatarId=10318&avatarType=issuetype", "name": "Task", "subtask": false, "avatarId": 10318}, "sprint": {"id": 220, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/220", "state": "active", "name": "LLA Sprint 19", "startDate": "2026-04-22T16:18:00.000+07:00", "endDate": "2026-05-06T16:18:00.000+07:00", "activatedDate": "2026-04-22T16:18:43.753+07:00", "originBoardId": 91, "goal": "", "synced": false, "autoStartStop": false}, "customfield_10031": 8.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=khoitt%40savameta.com", "name": "khoitt@savameta.com", "key": "JIRAUSER11234", "emailAddress": "khoitt@savameta.com", "avatarUrls": {"48x48": "https://jira.savameta.com/secure/useravatar?avatarId=10336", "24x24": "https://jira.savameta.com/secure/useravatar?size=small&avatarId=10336", "16x16": "https://jira.savameta.com/secure/useravatar?size=xsmall&avatarId=10336", "32x32": "https://jira.savameta.com/secure/useravatar?size=medium&avatarId=10336"}, "displayName": "Khoi Tran Trong", "active": true, "timeZone": "Asia/Ho_Chi_Minh"}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/10402", "description": "", "iconUrl": "https://jira.savameta.com/images/icons/statuses/generic.png", "name": "In Dev", "id": "10402", "statusCategory": {"self": "https://jira.savameta.com/rest/api/2/statuscategory/4", "id": 4, "key": "indeterminate", "colorName": "inprogress", "name": "In Progress"}}, "summary": "Onboarding for new user - đi từ web"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23025", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23025", "key": "LLA-892", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "description": "Created by Jira Software - do not edit or delete. Issue type for a user story.", "iconUrl": "https://jira.savameta.com/secure/viewavatar?size=xsmall&avatarId=10315&avatarType=issuetype", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "self": "https://jira.savameta.com/rest/agile/1.0/sprint/220", "state": "active", "name": "LLA Sprint 19", "startDate": "2026-04-22T16:18:00.000+07:00", "endDate": "2026-05-06T16:18:00.000+07:00", "activatedDate": "2026-04-22T16:18:43.753+07:00", "originBoardId": 91}, "customfield_10031": 0.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=khoitt%40savameta.com", "name": "khoitt@savameta.com", "key": "JIRAUSER11234", "displayName": "Khoi Tran Trong", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/1", "description": "Planning", "iconUrl": "https://jira.savameta.com/images/icons/statuses/open.png", "name": "Planning", "id": "1", "statusCategory": {"self": "https://jira.savameta.com/rest/api/2/statuscategory/2", "id": 2, "key": "new", "colorName": "default", "name": "To Do"}}, "summary": "User Settings"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23022", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23022", "key": "LLA-889", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 0.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=andt%40savameta.com", "name": "andt@savameta.com", "key": "JIRAUSER11229", "displayName": "An Dinh Tien", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/10401", "name": "Ready For Dev", "id": "10401", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DC] Create Department "}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23024", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23024", "key": "LLA-891", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 0.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=andt%40savameta.com", "name": "andt@savameta.com", "key": "JIRAUSER11229", "displayName": "An Dinh Tien", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/10401", "name": "Ready For Dev", "id": "10401", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DC] Collaboration Style for department (phong cách cộng tác)"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23029", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23029", "key": "LLA-895", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 0.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=andt%40savameta.com", "name": "andt@savameta.com", "key": "JIRAUSER11229", "displayName": "An Dinh Tien", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/10401", "name": "Ready For Dev", "id": "10401", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DC] Invite User (tại Create department)"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23036", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23036", "key": "LLA-897", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 8.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=khoitt%40savameta.com", "name": "khoitt@savameta.com", "key": "JIRAUSER11234", "displayName": "Khoi Tran Trong", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/1", "name": "Planning", "id": "1", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DC] Onboarding for new user đi từ Internal Invitation"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23006", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23006", "key": "LLA-878", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 13.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=trongtb%40savameta.com", "name": "trongtb@savameta.com", "key": "JIRAUSER11231", "displayName": "Trong Tran Binh", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/1", "name": "Planning", "id": "1", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DDM] Set-up Roles & Permissions"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23045", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23045", "key": "LLA-900", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 8.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=trongtb%40savameta.com", "name": "trongtb@savameta.com", "key": "JIRAUSER11231", "displayName": "Trong Tran Binh", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/1", "name": "Planning", "id": "1", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DDM] Manage Roles & Permissions"}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23007", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23007", "key": "LLA-879", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 13.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=namdh%40savameta.com", "name": "namdh@savameta.com", "key": "JIRAUSER11228", "displayName": "Nam Duong Hong", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/10402", "name": "In Dev", "id": "10402", "statusCategory": {"id": 4, "key": "indeterminate", "name": "In Progress"}}, "summary": "[DDM] Department - Working Folder "}}, {"expand": "operations,versionedRepresentations,editmeta,changelog,renderedFields", "id": "23009", "self": "https://jira.savameta.com/rest/agile/1.0/issue/23009", "key": "LLA-881", "fields": {"issuetype": {"self": "https://jira.savameta.com/rest/api/2/issuetype/10001", "id": "10001", "name": "Story", "subtask": false, "avatarId": 10315}, "sprint": {"id": 220, "state": "active", "name": "LLA Sprint 19", "originBoardId": 91}, "customfield_10031": 8.0, "customfield_10016": null, "assignee": {"self": "https://jira.savameta.com/rest/api/2/user?username=namdh%40savameta.com", "name": "namdh@savameta.com", "key": "JIRAUSER11228", "displayName": "Nam Duong Hong", "active": true}, "status": {"self": "https://jira.savameta.com/rest/api/2/status/1", "name": "Planning", "id": "1", "statusCategory": {"id": 2, "key": "new", "name": "To Do"}}, "summary": "[DDM] Share Documents to Department "}}]}}
OK
```

</details>

---

### 8. Blocked Path — Security Test

**Request:**
```
path: /rest/api/2/configuration
```

**Response:**
```
Error calling tool 'rest_get': {"code": "path_not_allowed", "path": "/rest/api/2/configuration"}
```

**Request:**
```
path: /rest/api/2/permissions
```

**Response:**
```
Error calling tool 'rest_get': {"code": "path_not_allowed", "path": "/rest/api/2/permissions"}
```

Các admin endpoint bị block đúng theo thiết kế.

<details>
<summary>Raw test output</summary>

```
TEST: BLOCKED: admin endpoint
PATH: /rest/api/2/configuration
HTTP status: 202 (202 = accepted by MCP)
[EXPECTED ERROR] Error calling tool 'rest_get': {"code": "path_not_allowed", "path": "/rest/api/2/configuration"}
OK (blocked as expected)

TEST: BLOCKED: permissions endpoint
PATH: /rest/api/2/permissions
HTTP status: 202 (202 = accepted by MCP)
[EXPECTED ERROR] Error calling tool 'rest_get': {"code": "path_not_allowed", "path": "/rest/api/2/permissions"}
OK (blocked as expected)
```

</details>

---

## Test Results Summary

| Test Case | Path | Status |
|-----------|------|--------|
| List projects | `/rest/api/2/project` | PASS |
| Search user by email | `/rest/api/2/user/search?username=` | PASS |
| List boards | `/rest/agile/1.0/board` | PASS |
| Service account info | `/rest/api/2/myself` | PASS |
| List sprints (board 91) | `/rest/agile/1.0/board/91/sprint` | PASS |
| Get sprint issues (sprint 220) | `/rest/agile/1.0/sprint/220/issue` | PASS |
| Block admin endpoint | `/rest/api/2/configuration` | PASS (blocked) |
| Block permissions endpoint | `/rest/api/2/permissions` | PASS (blocked) |

**8/8 test cases passed.**

---

## How Point Poker Should Call This Tool

Point Poker gọi tool `jira_rest_get` qua MCP client như bất kỳ tool nào khác:

```json
{
  "name": "jira_rest_get",
  "arguments": {
    "path": "/rest/api/2/user/search",
    "query": { "username": "user@savameta.com" }
  }
}
```

MCP server tự động đính kèm Jira credentials — Point Poker không cần biết token/password.

---

## Notes for Point Poker Dev

- Để lấy `accountId` của một user: gọi `/rest/api/2/user/search?username=<email>`, đọc field `key`
- Để list tất cả projects: gọi `/rest/api/2/project` (không có `/search` suffix — đó là Jira Cloud)
- Pagination: dùng `startAt` + `maxResults` cho tất cả list endpoints
- Mọi request đều là GET, không có quyền tạo/sửa/xóa
- Để lấy sprint đang active: gọi `/rest/agile/1.0/board/{boardId}/sprint`, lọc `state == "active"`
- **Story Points: dùng `customfield_10031`** — field `customfield_10016` luôn null trên Sava Meta Jira Server
