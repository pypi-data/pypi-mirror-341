from setuptools import setup, find_packages
import os

moduleDirectory = os.path.dirname(os.path.realpath(__file__))
exec(open(moduleDirectory + "/gkdbutils/__version__.py").read())


def readme():
    with open(moduleDirectory + '/README.md') as f:
        return f.read()


setup(
    name="gkdbutils",
    description='A collection useful utilities - mostly related to astronomy',
    long_description=readme(),
    long_description_content_type="text/markdown",
    version=__version__,
    author='genghisken',
    author_email='ken.w.smith@gmail.com',
    license='MIT',
    url='https://github.com/genghisken/gkdbutils',
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
          'Development Status :: 4 - Beta',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities',
    ],
    install_requires=[
          'gkutils>=0.3.4',
          'gkhtm',
          'pandas',
      ],
    python_requires='>=3.6',
    entry_points = {
        'console_scripts': ['cassandraIngest=gkdbutils.ingesters.cassandra.ingestGenericDatabaseTable:main', 'mysqlIngest=gkdbutils.ingesters.mysql.ingestGenericDatabaseTable:main'],
    },
)
