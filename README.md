# TRPO-project

## Running

To run the program:

```bash
python program/main.py
```

## Tests

To run tests:

- Run pytest with a coverage report
```bash
python -m pytest -v --cov=program/
```

## Profiling

When executed the program outputs the results of profiling the Program.analyze function.

## Dependencies

- `requirements.txt` - runtime dependencies.
- `docs/requirements-docs.txt` - dependencies for building docs.
- `tests/requirements-tests.txt` - dependencies for testing.

To install the dependencies using `pip` (replace `requirements.txt` with any of the above):

- (optional) Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

- Install the required dependencies
```bash
pip install -r requirements.txt
```
