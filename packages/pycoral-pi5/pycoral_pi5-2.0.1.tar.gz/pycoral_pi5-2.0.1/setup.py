from setuptools import setup, find_packages

setup(
    name='pycoral-pi5',
    version='2.0.1',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.26.0',
        'Pillow',
    ],
    python_requires='>=3.11',
    description='PyCoral built for Raspberry Pi 5 with Python 3.11',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pierre Gode',
    author_email='pierre@gode.one',
    url='https://github.com/PierreGode/pycoral-pi5',
    license='Apache-2.0',
    classifiers=[
        'Programming Language :: Python :: 3.11',
        'Operating System :: POSIX :: Linux',
        'License :: OSI Approved :: Apache Software License',
    ],
    package_data={
        'pycoral': ['*.so'],  # Inkluderar native shared object-filen
    },
    include_package_data=True,
)
