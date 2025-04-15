from setuptools import setup, find_packages

setup(
    name='random_allocation',  # Replace with your package name
    version='0.1',  # Initial version
    packages=find_packages(),  # Automatically find packages in the directory
    install_requires=[
        'numpy',  # List your package dependencies here
    ],
    description='A package for running random allocation experiments',  # Short description
    author='Your Name',  # Your name
    author_email='your.email@example.com',  # Your email
    url='https://github.com/yourusername/random_allocation',  # Link to your repository
)
