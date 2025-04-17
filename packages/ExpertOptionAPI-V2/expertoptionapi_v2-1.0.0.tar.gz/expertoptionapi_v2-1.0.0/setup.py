from setuptools import setup, find_packages

setup(
    name='ExpertOptionAPI-V2',  # Replace with your package name
    version='1.0.0',  # Initial version
    author='Vigo Walker',
    author_email='vigopaul05@gmail.com',
    description='Expert Option API V2 is a API for the ExpertOption broker',
    long_description=open('README.md').read(),  # Assumes you have a README.md
    long_description_content_type='text/markdown',
    url='https://github.com/ChipaDevTeam/ExpertOptionAPI-V2',
    packages=find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',  # Change if needed
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',  # Adjust as needed
    install_requires=[
        'pause==0.3',
        'simplejson==3.20.1',
        'websocket-client==1.8.0'
    ],
    include_package_data=True,
)
