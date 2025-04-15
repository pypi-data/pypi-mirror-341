from setuptools import setup, find_packages

long_description = ''
try:
    with open('readme.md', encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    pass

setup(
    packages = find_packages(),
    name = 'pyreinst',
    version = '0.0.1',
    author = "Stanislav Doronin",
    author_email = "mugisbrows@gmail.com",
    url = 'https://github.com/mugiseyebrows/pyreinst',
    description = 'Script to reinstall pip package',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    install_requires = ['colorama'],
    entry_points = {
        'console_scripts': [
            'pyreinst = pyreinst:main'
        ]
    }
)