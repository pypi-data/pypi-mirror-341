from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = fh.read().splitlines()

setup(
    name="aptisolve",  
    version="0.2.0",
    packages=find_packages(),  # Simplified package finding
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'aptisolve=aptisolve.main:cli',  # Changed from cli:main to main:cli
        ],
    },
    author="Abishek, Nithish, Vishal, Praveen",  
    author_email="p26055114@gmail.com",
    description="A package for solving numerical and verbal aptitude problems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/aptisolve",  
    python_requires=">=3.6",
    include_package_data=True,
    package_data={
        'aptisolve': [
            'numerical_aptitude/*',
            'verbalapt/*',
            'logical_reasoning/*',
            'data_interpretation/*'
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 3 - Alpha",  
        "Intended Audience :: Education",  
        "Topic :: Education :: Computer Aided Instruction (CAI)",  
    ],
)