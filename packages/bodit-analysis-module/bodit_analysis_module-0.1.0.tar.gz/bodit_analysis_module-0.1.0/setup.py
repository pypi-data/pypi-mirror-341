from setuptools import setup, find_packages

setup(
    name="bodit-analysis-module",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "boto3>1.34.154",
        "pandas>2.2.3",
        "numpy>1.26.4",
        "mysql-connector>2.2.9",
    ],
    python_requires=">=3.8",
    author="BODIT Inc.",
    keywords="bodit, analysis, module",
    description="BODIT Data Analysis Package",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
) 