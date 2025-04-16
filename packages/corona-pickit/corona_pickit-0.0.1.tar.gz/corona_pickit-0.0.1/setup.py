import os
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(here, 'README.rst')).read()

setup(
    name='corona-pickit',
    version='0.0.1',
    packages=['pickit'],
    description='Django Pickit Integration',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Corona Development Team',
    author_email='rolguin@corona.cl',
    url='https://gitlab.com/linets-projects/python-libraries/django-pickit/',
    license='MIT',
    python_requires=">=3.7",
    install_requires=[
        'Django>=3',
        'requests>=2.25.1'
    ]
)
