
<!-- README.md is generated from README.Rmd. Please edit that file -->

# nchack - easy tools for manipulating netcdf data in Python

The goal of nchack is to provide a comprehensive tool in Python for manipulating individual netcdf files and ensembles of netcdf files. The philosophy is to provide sufficient methods to carry out 80-90% of netcdf manipulations.

This package should work with Python 2.7 upwards.

## Installation

You can install the development version of nchack using using pip as follows.
```sh
pip install git+https://github.com/r4ecology/nchack.git
```

This package relies on CDO and NCO under the hood.
Visit <https://code.mpimet.mpg.de/projects/cdo/files> for CDO download and
installation instructions. Note that the development version of is
currently being developed using CDO Version 1.9.7. Vist http://nco.sourceforge.net/ to download and install NCO.

If you use Anaconda, you can install these packages as follows:

```sh
conda install -c conda-forge cdo 
```
```sh
conda install -c conda-forge nco 
```
 
Currently, the package has been tested for Linux computers. It will not
work on Windows platforms, currently. But (buyer beware) it should work on Macs.

## Tutorials

In depth tutorials will be added over time to https://github.com/r4ecology/nchack/tree/master/examples. At present a Jupyter notebook outlining basic usage is provided.

## Development state

This package is currently in the early stages of development, and is relatively unstable. This will change by the end of 2019, when the package should be relatively stable.
