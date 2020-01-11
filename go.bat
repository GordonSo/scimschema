python3 -m venv env
call .\env\Scripts\activate.bat
pip3 install -r requirements.txt --disable-pip-version-check
pushd src
pip3 setup.py develop
popd
REM python setup.py sdist
REM twine upload dist/* -r testpypi