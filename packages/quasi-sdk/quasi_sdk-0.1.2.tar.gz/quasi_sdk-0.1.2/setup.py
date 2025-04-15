from setuptools import setup, find_packages

setup(
    name="quasi-sdk",
    version="0.1.2",
    packages=find_packages(include=['quasi', 'quasi.*']),
    install_requires=[
        "numpy",
        "scipy",
    ],
    author="Rishwi Thimmaraju",
    description="GPU-powered statevector quantum simulator",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/quait/quasi",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.8",
)