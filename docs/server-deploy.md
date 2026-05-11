# Server Deployment Guide

Update và redeploy `mcp-atlassian` trên server khi có code mới.

## Setup trên server

| Path | Mục đích |
|------|----------|
| `~/mcp-src` | Source code (git repo) |
| `~/jira-mcp` | Docker Compose config + `.env.atlassian` |
| `mcp-atlassian-local:latest` | Docker image build từ `mcp-src` |

## Các bước deploy

### 1. Push code lên GitHub (từ local)

```bash
git push origin main
```

### 2. SSH vào server, pull source mới

```bash
cd ~/mcp-src
git pull origin main
```

### 3. Build lại Docker image từ source

```bash
docker build -t mcp-atlassian-local:latest ~/mcp-src
```

### 4. Restart container

```bash
cd ~/jira-mcp
docker compose down && docker compose up -d --force-recreate
```

### 5. Kiểm tra

```bash
docker logs mcp-atlassian -f
```
### 6. Bảo AI nó cập nhật cái file test_jira_rest_get.py và file jira_rest_get_guide.md để test ở trên server và gửi cho anh PO, 

### 7. sau đó chạy câu lệnh 
```bash
cd ~/jira-mcp
echo > test_jira_rest_get.py
vi test_jira_rest_get.py
```
sau đó copy cái file test_jira_rest_get.py từ ở git vào 
sau đó chạy câu lệnh
```bash
python3 test_jira_rest_get.py http://localhost:9200 
```
trên server để test
Container listen trên port `9200` (SSE transport).
