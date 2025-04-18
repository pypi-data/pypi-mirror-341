from setuptools import setup, find_packages


EMAIL = '1281722462@qq.com'
AUTHOR = 'Samwe'
REQUIRES_PYTHON = '>=3.8.0'
DESCRIPTION = 'A high-performance Python library that relies on nodejs to execute JavaScript'


setup(
    name="pytwojs",
    version="1.0.0",
    packages=find_packages(),
    author=AUTHOR,
    author_email=EMAIL,
    python_requires=REQUIRES_PYTHON,
    description=DESCRIPTION
)

