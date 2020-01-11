python3 -m venv env
env/bin/pip3 install -r requirements.txt --disable-pip-version-check
pushd src
../env/bin/python3 setup.py develop
popd
REM python setup.py sdist
REM twine upload dist/* -r testpypi