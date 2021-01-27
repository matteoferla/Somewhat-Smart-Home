import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'requests',
]

setup(
    name='homesensing_api_project',
    version='0.0',
    description='homesensing_api_project',
    long_description=open(os.path.join(here, 'README.md')).read(),
    classifiers=[
        'Programming Language :: Python',
    ],
    author='',
    author_email='',
    url='',
    keywords='api homesensing',
    packages=['homesensing_api'],
    include_package_data=True,
    install_requires=requires
)
