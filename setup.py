import os
from setuptools import setup

# Compile the list of packages available, because distutils doesn't have
# an easy way to do this.

packages, data_files = [], []
root_dir = os.path.dirname(__file__)
if root_dir:
    os.chdir(root_dir)

PACKAGE = 'feedzilla'

for dirpath, dirnames, filenames in os.walk(PACKAGE):
    for i, dirname in enumerate(dirnames):
        if dirname in ['.', '..']:
            del dirnames[i]
    if '__init__.py' in filenames:
        pkg = dirpath.replace(os.path.sep, '.')
        if os.path.altsep:
            pkg = pkg.replace(os.path.altsep, '.')
        packages.append(pkg)
    elif filenames:
        prefix = dirpath[len(PACKAGE) + 1:] # Strip package directory + path separator
        for f in filenames:
            data_files.append(os.path.join(prefix, f))

setup(
    version = '0.1.10',
    description = 'Django application for atom/rss feeds aggregation i.e. planet engine',
    author = 'Grigoriy Petukhov',
    author_email = 'lorien@lorien.name',
    url = 'http://bitbucket.org/lorien/feedzilla',
    name = 'feedzilla',

    packages = packages,
    package_data = {'feedzilla': data_files},

    license = "BSD",
    keywords = "django application feeds syndication aggregation atom rss planet",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Utilities'
    ],
)
