from setuptools import setup, find_packages

setup(
    name="dfcleaner",  
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "pandas",
        "numpy",  
    ],
    author="Brandyn Hamilton",
    author_email="brandynham1120@gmail.com",
    description="Automating DF and CSV Data Cleaning",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url=" ",  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
