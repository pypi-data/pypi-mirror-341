from setuptools import setup, find_packages

setup(
    name="zarf",
    version="0.0.1",
    description="A simple Dependency Container library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/hadi77ir/zarf",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
    ],
    python_requires=">=3.6",
)