from setuptools import setup, find_packages

setup(
    name="ucwa-sdk",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "requests",  # Add other dependencies if necessary
    ],
    test_suite="tests",
    tests_require=["pytest"],
    author="Your Name",
    author_email="your.email@example.com",
    description="UCWA SDK for AI memory management and model integration",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/your-org/ucwa-sdk",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
