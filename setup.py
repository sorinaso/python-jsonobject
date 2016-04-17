from setuptools import setup, find_packages
import codecs


PACKAGES = ['jsonobject']

REQUIREMENTS = []


def long_description():
    with codecs.open('README.rst', encoding='utf8') as f:
        return f.read()

version = __import__('jsonobject').__version__

setup(
      name='python-jsonobject',
      version=version,
      description="Json to object convertion with field type validations",
      long_description=long_description(),
      classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Python Modules'],
      author='Alejandro Souto',
      author_email='sorinaso@gmail.com',
      url='https://github.com/sorinaso/python-jsonobject',
      license='MIT',
      packages=PACKAGES,
      include_package_data=True,
      zip_safe=False,
      install_requires=REQUIREMENTS,
)
