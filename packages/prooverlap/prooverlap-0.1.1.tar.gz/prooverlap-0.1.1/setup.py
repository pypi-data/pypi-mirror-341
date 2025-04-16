from setuptools import setup, find_packages

setup(
    name="prooverlap", 
    version="0.1.1", 
    description="Assessing feature proximity/overlap and testing statistical significance from genomic intervals",
    long_description=open('README.md').read(), 
    long_description_content_type="text/markdown",
    author="Nicolò Gualandi, Alessio Bertozzo, Claudio Brancolini", 
    author_email="nicolo.gualandi@uniud.it, bertozzo.alessio@spes.uniud.it, caludio.brancolini@uniud.it",
    license="GPL-3.0",  
    url="https://github.com/ngualand/ProOvErlap", 
    packages=find_packages(),  
    install_requires=[ 
        "biopython",
        "pandas",
        "scipy",
        "pybedtools",
        "numpy"
    ],
    classifiers=[ 
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL-3.0 License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)

