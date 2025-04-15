from setuptools import setup, find_packages

setup(
    name='quasi-sdk',
    version='0.1.1',  # Increment this for every update
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
    ],
    author='Rishwi Thimmaraju',
    description='GPU-based state vector quantum simulator',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/quasi-sdk',  # Optional but recommended
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)