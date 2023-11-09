# TRPO-project

## Tests

To run tests:

- (optional) Create a virtual environment
```bash
python -m venv .venv-tests
source .venv-tests/bin/activate
```

- Install the required dependencies
```bash
pip install -r requirements-tests.txt
```

- Run pytest with a coverage report
```
python -m pytest --cov=.
```
