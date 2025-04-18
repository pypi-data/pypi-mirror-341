from setuptools import setup, find_packages

setup(
    name='MSpypi',
    version='1.0',
    description='Un package python pour les opérations mathématiques courantes',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown", 
    url="https://stagee.readthedocs.io/en/latest/",
   

    project_urls={
        'Documentation': 'https://stagee.readthedocs.io/en/latest/',  # Ajoutez ici la documentation si applicable
        'Source': 'https://app.readthedocs.org/projects/stagee/',
    },
    author='ngouhouo nabil',
    author_email='nabilf045@gmail.com',
    packages=find_packages(),
    
    install_requires=[],

)
