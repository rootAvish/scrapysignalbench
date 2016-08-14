import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="scrapysignalbench",
    version="0.1",
    description="A set of benchmarks for measuring Scrapy's signaling API performance.",
    long_description=read('README.rst'),
    url='https://github.com/rootavish/scrapysignalbench',
    license='BSD',
    author=' rootavish',
    author_email='rootavish@gmail.com',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Framework :: Scrapy',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Topic :: Software Development :: Testing',
        'Topic :: System :: Benchmark'
    ],
    install_requires=['simplejson==3.3.1'],
    entry_points={
        'console_scripts': ['scrapysignalbench=scrapysignalbench.main:main']
    }
)
