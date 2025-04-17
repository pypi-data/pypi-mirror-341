from setuptools import setup, find_packages

long_description = """
XNAT is a flexible imaging informatics software platform for organizing and managing 
imaging data. DAX is a Python project that provides a uniform interface to run 
pipelines on a cluster by pulling data from an XNAT database via REST API calls. 
The dax client further enhances DAX by offering powerful command-line tools that 
streamline extracting information from XNAT, creating pipelines (spiders/processors), 
building projects on XNAT with pipeline assessors, managing pipeline execution on a cluster, 
and automatically uploading results back to XNAT. By leveraging XnatUtils commands, 
the dax client also enables a programmatic workflow for interacting directly with XNAT in Python.  
"""

setup(
    name='dax-client',
    version='1.1.6',
    packages=find_packages(),
    description='dax-client',
    long_description_content_type='text/plain',
    long_description=long_description,
    url='https://github.com/VUIIS/dax_bids',
    download_url='https://github.com/VUIIS/dax_bids',
    project_urls={
        'Documentation': 'https://github.com/VUIIS/dax_bids'},
    author='Baxter Rogers',
    author_email='baxpr@vu1.org',
    python_requires='>=3.6',
    platforms=['MacOS', 'Linux'],
    license='MIT',
    install_requires=[
        'pyyaml',
        'pydantic',
        'cpjson'
    ],

)
