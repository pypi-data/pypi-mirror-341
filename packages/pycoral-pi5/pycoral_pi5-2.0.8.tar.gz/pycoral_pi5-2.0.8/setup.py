from setuptools import setup, find_packages
from pathlib import Path

# Läs README om den finns, annars fallback till en kort beskrivning
readme_path = Path(__file__).parent / "README.md"
long_description = readme_path.read_text(encoding="utf-8") if readme_path.exists() else "PyCoral for Raspberry Pi 5"

setup(
    name='pycoral-pi5',
    version='2.0.8',
    packages=find_packages(),
    install_requires=[
        'numpy>=1.26.0',
        'Pillow',
    ],
    python_requires='>=3.11',
    description='PyCoral built for Raspberry Pi 5 with Python 3.11',
    long_description=long_description,
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
        'pycoral': ['*.so'],  # säkerställ att .so-filen inkluderas
    },
    include_package_data=True,
    data_files=[('pycoral', ['pycoral/_pywrap_coral.so'])],  # tvinga in .so-filen
)
