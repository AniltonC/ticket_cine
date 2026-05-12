FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

# Install uv (pinned version for reproducibility)
COPY --from=ghcr.io/astral-sh/uv:0.9.26 /uv /uvx /bin/

# Compile bytecode for faster container startup
ENV UV_COMPILE_BYTECODE=1

# Use copy link mode to support Docker layer caching
ENV UV_LINK_MODE=copy

WORKDIR /app/

# Place .venv executables in PATH
ENV PATH="/app/.venv/bin:$PATH"

# Install dependencies before copying app code so this layer is only
# invalidated when pyproject.toml or uv.lock change, not on every code change.
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen --no-install-project

# Copy application code
COPY ./app /app/app

# Sync the project itself (installs the local package)
RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=uv.lock,target=uv.lock \
    --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    uv sync --frozen

# Run with multiple workers for production
CMD ["fastapi", "run", "--workers", "4", "app/main.py"]
