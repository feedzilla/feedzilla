from setuptools import setup, find_packages

setup(
    name = 'feedzilla',
    version = '0.1.20',
    description = 'Django application for atom/rss feeds aggregation i.e. planet engine',
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
