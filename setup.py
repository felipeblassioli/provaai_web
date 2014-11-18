"""
Provaai
-------

Links
`````
* `development version
  <https://github.com/provaai/provaai_web>`_


"""
from setuptools import setup, find_packages


setup(
    name='Provaai',
    version='0.0.1',
    url='https://github.com/provaai/provaai_web',
    author='Felipe Blassioli',
    author_email='felipeblassioli@gmail.com',
    description='Discover cool clothes from cool stores.',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask>=0.7',
        'flask-peewee>=0.6.4',
        'flask-classy>=0.6.8',
        'PyMySQL',
        'flask-uploads>=0.1.3',
        'flask-login>=0.2.9',
        'flask-wtf>=0.10.0',
        'Flask-Admin>=1.0.8'
    ],
    dependency_links=[
        "https://github.com/felipeblassioli/flask_rest/tarball/master#egg=Flask-SimpleRest-0.1.5"
    ]
)
