from setuptools import setup, find_packages

setup(
    name = 'feedzilla',
    version = '0.2.1',
    description = 'Django application for ATOM/RSS feeds aggregation i.e. planet engine',
    long_description = open('README.rst').read(),
    url = 'http://bitbucket.org/lorien/feedzilla',
    author = 'Grigoriy Petukhov',
    author_email = 'lorien@lorien.name',

    packages = find_packages(),
    include_package_data = True,

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
