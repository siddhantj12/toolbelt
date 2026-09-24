# toolbelt

Small, dependency-free Python utilities — the helpers that get rewritten from
scratch in every project. Python 3.9+, no runtime dependencies.

## Install

```bash
pip install -e ".[dev]"
```

## Usage

```python
from toolbelt import batched, dedupe, slugify, truncate

slugify("Crème Brûlée, please!")        # 'creme-brulee-please'
truncate("hello brave world", 12)        # 'hello brave…'
list(batched([1, 2, 3, 4, 5], 2))        # [[1, 2], [3, 4], [5]]
list(dedupe([3, 1, 3, 2, 1]))            # [3, 1, 2]
```

## Development

```bash
pytest
ruff check .
```

## Contributing

This repository is maintained partly by a scheduled agent that adds one small,
self-contained improvement per day via pull request. See [ROADMAP.md](ROADMAP.md)
for the queue of planned utilities, and [CONTRIBUTING.md](CONTRIBUTING.md) for
the bar every change is held to.

## License

MIT
