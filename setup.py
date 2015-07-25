import os
from setuptools import setup, find_packages
from monarch import __version__

DESCRIPTION = 'Database system migration for django.'

CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Framework :: Django',
    'Framework :: Django :: 1.7',
    'Framework :: Django :: 1.8',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2.7',
    'Topic :: Utilities',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

def read(fname):
    readme_file = os.path.join(os.path.dirname(__file__), fname)
    return os.popen('[ -x "$(which pandoc 2>/dev/null)" ] && pandoc -t rst {0} || cat {0}'.format(readme_file)).read()


setup(
    name='django-monarch',
    version=__version__,
    author='Kevin Clark',
    author_email='ticalcster@gmail.com',
    description=DESCRIPTION,
    long_description=read('README.md'),
    url='https://github.com/jrief/django-websocket-redis',
    license='MIT',
    keywords=['django', 'migration'],
    platforms=['OS Independent'],
    classifiers=CLASSIFIERS,
    packages=find_packages(exclude=['example', 'docs']),
    include_package_data=True,
    install_requires=[
        'setuptools',
        'six',
    ],
    zip_safe=False,
)