from setuptools import setup, find_packages

setup(
    name="infinityvoid",
    
    version="0.1.4",
    author="Your Name",
    author_email="your.email@example.com",
    description="A package to list docx and pkt files",
    url="https://github.com/yourusername/infosec",  # optional if you host on GitHub
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'python-docx',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # or whatever license you pick
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
   

)
