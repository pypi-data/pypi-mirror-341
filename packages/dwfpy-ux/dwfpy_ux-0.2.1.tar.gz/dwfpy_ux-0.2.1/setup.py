from setuptools import setup, find_packages

setup(
    name="dwfpy-ux",
    version="0.2.1",
    author="Your Name",
    author_email="your.email@example.com",
    description="Digilent Waveforms API facade with optional UIX",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/dwfpy-ux",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "numpy",
        "pandas",
        "PyQt5",
        "pyqtgraph",
        "pglive",
        "ipython",  # For display and clear_output functions
    ],
    # Include the package data
    package_data={
        "DwfInterface": ["*.py"],
    },
) 