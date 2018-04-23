import setuptools

setuptools.setup(
    name='pipenvtest',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
)