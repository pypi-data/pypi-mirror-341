from setuptools import setup, find_packages

setup(
    name="windroselab",
    version="0.1.5",
    author="Seyed Abdolvahab Taghavi",
    author_email="abdolvahab.taghavi@gmail.com",
    description="*WindRose Generator* is a Python library for creating customizable wind rose diagrams from Excel data. Visualize wind speed, direction, and frequency with options to adjust fonts, colors, styles, and export high-quality plots for reports or analysis."
,
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/AbdolvahabT/windroselab",
    packages=find_packages(),
    install_requires=[
        
        "matplotlib>=3.8.2",
        "numpy>=1.26.2",
        "pandas>=2.1.4",
        "Pillow>=10.1.0",
        "xlrd==1.2.0", 
        "tkvalidate==1.0.1",
        "PyPDF2==3.0.1"

    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
