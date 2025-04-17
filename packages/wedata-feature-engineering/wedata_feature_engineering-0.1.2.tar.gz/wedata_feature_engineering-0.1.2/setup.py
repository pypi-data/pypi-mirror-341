from setuptools import setup, find_packages

setup(
    name="wedata_feature_engineering",
    version="0.1.2",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        'pyspark>=3.0.0',
        'delta-spark>=1.0.0',
        'pandas>=1.0.0'
    ],
    python_requires='>=3.7',
    author="meahqian",
    author_email="",
    description="Wedata Feature Engineering Library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    license="Apache 2.0",
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
)
