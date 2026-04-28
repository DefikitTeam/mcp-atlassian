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

Container listen trên port `9200` (SSE transport).
