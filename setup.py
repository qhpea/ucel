import setuptools

extras_require = {
    'docker': ['docker~=5.0'],
    'azureml': ['azureml-core~=1.34']
}

setuptools.setup(
    extras_require = extras_require
)
