from setuptools import setup, find_packages

setup(
    name="ai-content-generator",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "google-generativeai"
    ],
    author="SRIRAM",
    description="A simple wrapper to generate content using RAM AI",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/sriram-65/gen_ai.git",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
)
