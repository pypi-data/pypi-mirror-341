from setuptools import setup, find_packages

setup(
    name="financial-backtesting",
    version="0.2.2",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",
        "scikit-learn",
        "joblib",
    ],
    author="Shashwat Chaturvedi",
    author_email="chaturvedishashwat5@gmail.com",
    description="A backtesting framework for machine learning and financial trading strategies.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/shashwatop3/backtesting_package",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    license="MIT",  
)