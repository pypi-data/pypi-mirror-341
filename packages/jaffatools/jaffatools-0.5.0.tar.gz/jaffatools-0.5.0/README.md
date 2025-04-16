
# JaffaTools

A Python toolkit for JAFFA fusion gene detection

### Instructions

1. **Filter FASTQ files**: Filter FASTQ files based on the reads in the BAM file and keep only matching reads.
2. **Run JAFFA**: Encapsulates the running function of the JAFFA fusion gene detection process.
3. **Add NB:Z tags**: Extract NB:Z tags from the BAM file and add them to the JAFFA result CSV file.
4. **jaffa-viz**: Visualize JAFFA results
	1. **jaffa-viz circos**: Creates Circos plots to visualize fusion genes
	2. **jaffa-viz cell-stats:** Generates statistics about fusion genes per cell
	3. **jaffa-viz class-stats:** Creates plots showing the classification of fusion genes


## Install

```bash
pip install jaffatools
```

## Dependencies
### System Requirements
* **Python**: 3.6 or later
* **R**: 4.0.0 or later (Required for visualization functions)
### Python Dependencies

* **NumPy**: For numerical operations
* **pandas**: For data manipulation
* **pysam**: For parsing and manipulating SAM/BAM file
* **subprocess**: For executing R scripts (built-in)
* **argparse**: For command-line interface (built-in)
* **os**: For file path operations (built-in)
### R Package Dependencies
The visualization functions require the following R packages:
* **data.table**: Fast data manipulation
* **ggplot2**: Statistical data visualization
* **RCircos**: Circular visualization of genomic data
* **gtools**: Various R programming tools
* **dplyr**: Data manipulation grammar
#### Installation of R Dependencies
You can install all required R packages with the following R command:

```R
install.packages(c("data.table", "ggplot2", "RCircos", "gtools", "dplyr"))  
if (!requireNamespace("BiocManager", quietly = TRUE))  
    install.packages("BiocManager")  
BiocManager::install("RCircos")  
```

