from setuptools import setup
setup(
    name = 'sport-update-cli',
    version = '1.0.0',
    packages = ['pycli'],
    entry_points = {
        'console_scripts': [
            'pycli = pycli.__main__:main'
        ]
    })