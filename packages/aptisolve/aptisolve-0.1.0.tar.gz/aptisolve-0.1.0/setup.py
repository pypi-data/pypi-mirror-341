from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="aptisolve",  
    version="0.1.0",
    packages=find_packages(include=[
        'aptisolve',
        'aptisolve.*',  
        'numerical_aptitude',
        'numerical_aptitude.*',  
        'verbalapt',
        'verbalapt.*',  
        'logical_reasoning',
        'logical_reasoning.*',  
        'data_interpretation',
        'data_interpretation.*'  
    ]),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'aptisolve=aptisolve.cli:main',
        ],
    },
    author="Abishek, Nithish, Vishal, Praveen",  
    author_email="p26055114@gmail.com",
    description="A package for solving numerical and verbal aptitude problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aptisolve",  # Added URL field
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        'data_interpretation': ['data/*'],
        'logical_reasoning': ['data/*'],
        'numerical_aptitude': ['data/*'],
        'verbalapt': ['data/*']
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",  # Added development status
        "Intended Audience :: Education",  # Added intended audience
        "Topic :: Education :: Computer Aided Instruction (CAI)",  # Added topic
    ],
)