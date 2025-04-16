setup:
    uv venv
    uv sync

test:
    uv run pytest tests

lint:
    uv run ruff check .
    uv run ruff format --check .
    uv run pyright

lint-fix:
    uv run ruff check . --fix
    uv run ruff format .

run:
    uv run python -m mcp_multilspy

dev:
    uv run mcp dev -m mcp_multilspy

install:
    uv run mcp install -m mcp_multilspy

clean:
    rm -rf .venv target dist *.egg-info
    find . -type d -name "__pycache__" -exec rm -rf {} +
    rm -rf .mcp_server
