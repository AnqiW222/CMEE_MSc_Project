#!/bin/bash
# Author: Anqi Wang aw222@ic.ac.uk
# Script: CompileLaTeX.sh
# Description: Compiles latex with bibtex
#
# Outputs: pdf latex file
# Arguments: 1 (.tex latex code)
# Date: Oct 11th 2022

#set a variable so that it can be manipulated to remove the suffix
#remove the suffix and use it as a new input x
x=${1%.tex}

pdflatex $x.tex
bibtex $x
pdflatex $x.tex
pdflatex $x.tex
# evince $x.pdf &

## Cleanup
rm *.aux
rm *.log
rm *.bbl
rm *.blg
rm *.dvi
rm *.nav
rm *.out
rm *.toc