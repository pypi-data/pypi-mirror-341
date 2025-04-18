from setuptools import setup, find_packages

setup(
    name='canonical_loader',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'shining_pebbles>=0.5.3',
        'string_date_controller>=0.1.3',
        'tqdm',
    ],
    author='June Young Park',
    author_email='juneyoungpaak@gmail.com',
    description='A Python module for loading and managing canonical data files with standardized naming conventions',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/nailen1/canonical_loader.git',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    keywords='canonical data loader file management standardization',
)
