from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="jaffatools",
    version="0.5.0",
    author="Waidong Huang",
    author_email="wdhuang927@gmail.com",
    description="Tools for working with JAFFA fusion gene detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/WhaleGe/jaffatools",
    packages=[  
        'jaffatools',
        'jaffatools.cli',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pysam>=0.16.0",
        "pandas>=1.0.0",
        "numpy>=1.18.0",
    ],
    entry_points={
        "console_scripts": [
            "jaffa-filter=jaffatools.cli.fastq_filter_cli:main",
            "jaffa-annotate=jaffatools.cli.bam_annotator_cli:main",
            "jaffa-run=jaffatools.cli.jaffa_runner_cli:main",
            "jaffa-viz=jaffatools.cli.jaffa_viz_cli:main", 
        ],
    },
    package_data={
        'jaffatools': [
            'data/*.txt',
            'data/*.R',
        ],  
    },  
    include_package_data=True,
)
