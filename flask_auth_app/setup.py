from setuptools import setup, find_packages

setup(
    name='flask_auth_app',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Flask',
    ],
)