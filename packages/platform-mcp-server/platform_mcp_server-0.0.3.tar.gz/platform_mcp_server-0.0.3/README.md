# platform-mcp-server

## Development

Create a virtual environment:

```bash
uv venv
uv sync -U
```

Build the distribution:

```bash
uv build
```

Upload to PyPI:

```bash
twine upload dist/*
```
