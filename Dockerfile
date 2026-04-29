# Use a Python image with uv pre-installed
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS uv

# Install the project into `/app`
WORKDIR /app

# Enable bytecode compilation
ENV UV_COMPILE_BYTECODE=1

# Copy from the cache instead of linking since it's a mounted volume
ENV UV_LINK_MODE=copy

# Copy source code first
COPY . /app

# Force version to local so uv doesn't pull from PyPI
ENV SETUPTOOLS_SCM_PRETEND_VERSION=99.0.0
ENV UV_DYNAMIC_VERSIONING_BYPASS=99.0.0

# Install dependencies first (without project)
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --no-dev --no-install-project

# Build and install local package, bypassing PyPI
RUN --mount=type=cache,target=/root/.cache/uv \
    uv build --wheel --out-dir /tmp/dist && \
    uv pip install --no-index /tmp/dist/*.whl

# Verify
RUN grep -c "jira_rest_get\|jira_update_sprint" /app/.venv/lib/python3.13/site-packages/mcp_atlassian/servers/jira.py

# Remove unnecessary files from the virtual environment before copying
RUN find /app/.venv -name '__pycache__' -type d -exec rm -rf {} + && \
    find /app/.venv -name '*.pyc' -delete && \
    find /app/.venv -name '*.pyo' -delete && \
    echo "Cleaned up .venv"

# Final stage
FROM python:3.13-alpine

# Create a non-root user 'app'
RUN adduser -D -h /home/app -s /bin/sh app
WORKDIR /app
USER app

COPY --from=uv --chown=app:app /app/.venv /app/.venv

# Place executables in the environment at the front of the path
ENV PATH="/app/.venv/bin:$PATH"

# Disable Python output buffering for proper stdio communication
ENV PYTHONUNBUFFERED=1

ENTRYPOINT ["mcp-atlassian"]
