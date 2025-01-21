pip install mypy[mypyc] setuptools
python3 setup.py bdist_wheel
pip install dist/*.whl