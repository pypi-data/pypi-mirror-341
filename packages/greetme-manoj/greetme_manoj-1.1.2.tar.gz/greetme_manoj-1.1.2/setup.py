from setuptools import setup, find_packages

setup(
    name='greetme-manoj',                        
    version='1.1.2',               
    packages=find_packages(),             
    install_requires=[],                  
    author='Manoj Prajapati',                  
    author_email='manojbittu161@gmail.com',        
    description='A simple greeting package for Python beginners',
    long_description=open('README.md').read(),  
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/greetme',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',              
)