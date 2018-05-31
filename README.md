[![Build Status](https://travis-ci.org/mhoffman/CatalysisHubCLI.svg?branch=master)](https://travis-ci.org/mhoffman/CatalysisHubCLI)

## Disclaimer

This project is no longer maintained since it has merged into CatKit: https://github.com/SUNCAT-Center/CatKit

## Installation

Install with pip using

    pip install --user --upgrade git+https://github.com/kirstenwinther/CatalysisHubCLI.git
    pip install --user python-Levenshtein

and when using Python 2.7

    pip install --user pathlib


## Usage

Run `cathub`, like so

    cathub --help

or with any of its sub-commands, like so

    cathub make_folders_template --help

## Examples


To create an .json input file

    cathub make_folders_template project1.json --create-template

To create a folder structures from a .json input file

    cathub make_folders_template project1.json

Querying the Catalysis Hub database:

    cathub reactions -q reactants=CO -q chemicalComposition=~Pt

    cathub publications -q title=~Evolution -q year=2017

Reading folders into sqlite3 db file:

    cathub folder2db <foldername>

Sending the data to the Catalysis Hub server:

    cathub db2server <dbfile>
