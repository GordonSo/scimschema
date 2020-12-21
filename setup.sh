curl -fsS -o get-poetry.py https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py
python3 get-poetry.py -y
source $HOME/.poetry/env
poetry install
poetry run black . --check
poetry run isort . --check
poetry run mypy ./scimschema ./tests
poetry run pytest
