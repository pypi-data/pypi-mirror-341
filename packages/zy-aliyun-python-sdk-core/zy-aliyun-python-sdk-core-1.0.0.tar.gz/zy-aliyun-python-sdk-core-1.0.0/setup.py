import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="zy-aliyun-python-sdk-core",
    version="1.0.0",
    author="munan921",
    license='MIT',
    author_email="immndev@hotmail.com",
    description="sample sdk for aliyun",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/munan921/zy-aliyun-python-sdk",
    install_requires=[
        'certifi>=2019.6.16',
        'chardet>=3.0.4',
        'decorator>=4.4.0',
        'idna>=2.8',
        'requests>=2.22.0',
        'retry>=0.9.2',
        'urllib3>=1.25.3',
        'xmltodict>=0.12.0'
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
