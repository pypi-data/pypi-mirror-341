from setuptools import setup, find_packages

setup(
    name="ded_sdk",
    version="0.1.0",
    description="Python SDK for Disposable Email Detection",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Akshat Kotpalliwar alias IntegerAlex",
    author_email="akshatkot@gmail.com",
    url="https://ded.gossorg.in",
    packages=find_packages(),
    install_requires=["requests>=2.25.1"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.6",
)

