from setuptools import setup, find_packages
setup(
    name='neuroedge_model_transfer',
    version='1.0.0',
    packages=find_packages(),
    description='A package to read a file from a given location and upload it to an S3 bucket',
    author='Radhika Menon',
    author_email='Radhika.Menon@cognizant.com',
    install_requires=[
        "boto3>=1.18.0",  # AWS SDK for Python
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Choose your license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)