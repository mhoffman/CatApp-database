[![Build Status](https://travis-ci.org/mhoffman/CatAppCLI.svg?branch=master)](https://travis-ci.org/mhoffman/CatAppCLI)

## Installation

Install with pip using

    pip install --user --upgrade git+https://github.com/kirstenwinther/CatalysisHubCLI.git


Run 

    eval "$(_CATAPP_COMPLETE=source catapp)"

for bash completion or better, yet, put in in your `~/.bashrc`.

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
