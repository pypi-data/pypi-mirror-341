from setuptools import setup, find_packages

setup(
    name="infinityvoid",
    version="0.6",
    packages=find_packages(),
    include_package_data=True,  # Ensures non-code files (like PDFs) are included
    package_data={
        'infinityvoid': ['ALL_PRACT_PROPER/*.docx'],
        'infinityvoid': ['ALL_PRACT_Easy/*.pkt'],

  # Specify that we want to include the PDF
    },
    description="A module with a PDF and Python file",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://example.com/mymodule",
)
