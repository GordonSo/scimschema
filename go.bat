python -m venv env
call .\env\Scripts\activate.bat
pip install -r requirements.txt --disable-pip-version-check
python setup.py develop
REM python setup.py sdist
REM twine upload dist/* -r testpypi