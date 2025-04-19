from setuptools import setup, find_packages

setup(
    name="sn_restapi_wrapper",
    version="1.1.3",
    description="A wrapper for ServiceNow RestAPI to pull large data volumes from different tables based on a time period",
    long_description=open("README.md").read() + "\n\n" + open("changelog.txt").read(),
    long_description_content_type="text/markdown",
    author="Mihindu Perera",
    author_email="mihinduperera35@gmail.com",
    license="MIT",
    packages=find_packages(),
    install_requires=[
        "requests",
        "pandas",
        "tqdm"
    ],
    keywords=["wrapper", "servicenow-restapi"],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
