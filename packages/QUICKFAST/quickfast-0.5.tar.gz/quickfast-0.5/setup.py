from setuptools import setup, find_packages

setup(
    name="QUICKFAST",
    version="0.5",
    packages=find_packages(),
    include_package_data=True,
    package_data={
        'QUICKFAST': [
            'CSV/*.csv',
            'DBCOMMANDS/*.txt',
            'DOC/*.docx',
            'EXCEL/*.xlsx',
            'MANUAL/*.pdf',
            'PYTHON/*.py',
            'R/*.R',
            'TEXT/*.txt',
        ],
    },
    description="A module with documents, data files, and scripts",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://example.com/mymodule",
)



