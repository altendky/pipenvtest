import setuptools


setuptools.setup(
    name='gridtied',
    packages=setuptools.find_packages('python'),
    package_dir={'': 'python'},
    install_requires=[
        'ccstudiodss',
        'pytest',
        'pytest-twisted',
        'pytest-qt',
        'python-can',
        'pyqt5',
        'twisted',
        'pypiwin32;platform_system=="Windows"',
    ],
    entry_points={
        'pytest11': [
            'gridtied_cli = gridtied.tests.hil.pytest_plugin',
        ]
    },
)
