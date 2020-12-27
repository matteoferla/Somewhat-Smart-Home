import os

from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))

requires = [
    'requests',
    'picamera',
    'PIL',
    'apscheduler',
    'flask'
]

tests_require = [
    'WebTest >= 1.3.1',  # py3 compat
    'pytest >= 3.7.4',
    'pytest-cov',
]

setup(
    name='photologger',
    version='0.0',
    description='photologger',
    long_description='photologger',
    classifiers=[
        'Programming Language :: Python',
        'Framework :: Pyramid',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: WSGI :: Application',
    ],
    author='Matteo Ferla',
    author_email='',
    url='',
    keywords='web pyramid pylons',
    packages=['photologger'],
    include_package_data=True,
    zip_safe=False,
    extras_require={
        'testing': tests_require,
    },
    install_requires=requires,
    entry_points={
        'paste.app_factory': [
            'main = photologger:main',
        ]
    },
)
