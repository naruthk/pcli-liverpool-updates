from setuptools import setup

setup(
    name="cli-soccer",
    version='0.1',
    py_modules=['starter'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        cli-soccer=starter:start
    ''',
)