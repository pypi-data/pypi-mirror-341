from setuptools import setup, find_packages

setup(
    name='CdBURY',
    version='0.1.0',
    packages=find_packages(include=['CdBURY', 'CdBURY.*']),
    install_requires=[
        'numpy',
        'matplotlib',
        'pandas'
    ],
    include_package_data=True,
    zip_safe=False,
)