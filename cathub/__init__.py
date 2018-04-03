import click
import six
import pprint


@click.group()
def cli():
    pass

@cli.command()
@click.argument('folder_name')
@click.option('--debug', default=False)
@click.option('--skip-folders', default='', help="""subfolders not to read, given as the name of a single folder, or a string with names of more folders seperated by ', '""")
@click.option('--goto-reaction', help="""name of reaction folder to skip to""")
def folder2db(folder_name, debug, skip_folders, goto_reaction):
    import os
    import folder2db

    skip = []
    for s in skip_folders.split(', '):
        for sk in s.split(','):
            skip.append(sk)
    folder2db.main(folder_name, debug, skip, goto_reaction)


@cli.command()
@click.argument('dbfile')
@click.option('--start_id', default=1, type=int)
@click.option('--write_reaction', default=True, type=bool)
@click.option('--write_reaction_system', default=True, type=bool)
@click.option('--write_ase', default=True, type=bool)
@click.option('--write_publication', default=True, type=bool)
@click.option('--block-size', default=1000, type=int)
@click.option('--start-block', default=0, type=int)
def db2server(dbfile, start_id, write_reaction, write_ase, write_publication,
              write_reaction_system, block_size, start_block):
    import os
    import db2server
    db2server.main(dbfile, start_id=start_id, write_reaction=write_reaction,
                   write_ase=write_ase,
                   write_publication=write_publication,
                   write_reaction_system=write_reaction_system,
                   block_size=block_size,
                   start_block=start_block)


reaction_columns = ['chemicalComposition', 'surfaceComposition',
                    'facet', 'sites', 'coverages', 'reactants', 'products', 'Equation',
                    'reactionEnergy', 'activationEnergy', 'dftCode', 'dftFunctional',
                    'username', 'pubId', 'reactionSystems', 'systems', 'publication']
publication_columns = ['pubId', 'title', 'authors', 'journal', 'year', 'doi', 'tags']

@cli.command()
@click.option('--columns', '-c',
              default=('chemicalComposition', 'Equation', 'reactionEnergy'),
              type=click.Choice(reaction_columns),
              multiple=True)
@click.option('--n_results', default=10)
@click.option('--queries', '-q',  default={}, multiple='True',
              help="Make a selection on one of the columns: {}\n Examples: \n -q chemicalComposition=~Pt for surfaces containing Pt \n -q reactants=CO for reactions with CO as a reactants".format(reaction_columns))
def reactions(columns, n_results, queries):
    import query
    if not isinstance(queries, dict):
        query_dict = {}
        for q in queries:
            key, value = q.split('=')
            if key == 'distinct':
                if value in ['True', 'true']:
                    query_dict.update({key: True})
                    continue
            try:
                value = int(value)
                query_dict.update({key: value})
            except:
                query_dict.update({key: '{}'.format(value)})
    #columns = [columns]
    query.main(table='reactions', columns=columns, n_results=n_results, queries=query_dict)


    
@cli.command()
@click.option('--columns', '-c',
              default = ('title', 'authors', 'journal', 'year'),
              type=click.Choice(publication_columns),
              multiple=True)
@click.option('--n_results', default=10)
@click.option('--queries', '-q', default={}, multiple=True,
              help="Make a selection on one of the columns: {}\n Examples: \n -q: \n title=~Evolution \n authors=~bajdich \n year=2017".format(publication_columns))
def publications(columns, n_results, queries):
    import query
    if not isinstance(queries, dict):
        query_dict = {}
        for q in queries:
            key, value = q.split('=')
            if key == 'distinct':
                if value in ['True', 'true']:
                    query_dict.update({key: True})
                    continue
            try:
                value = int(value)
                query_dict.update({key: value})
            except:
                query_dict.update({key: '{}'.format(value)})
    
    query.main(table='publications', columns=columns, n_results=n_results, queries=query_dict)


    
@cli.command()
@click.argument('template')
@click.option('--create-template', is_flag=True, help="Create an empty template file.")
@click.option('--custom-base', )
@click.option('--diagnose', )
def make_folders(create_template, template, custom_base, diagnose):
    """Create a basic folder tree to put in DFT calculcations.

    Dear all

    Use this command make the right structure for your folders
    for submitting data for Catalysis Hub.
    
    Start by creating a template file by calling:
    
    $ cathub make_folders --create-template <template_name>

    Then open the template and modify it to so that it contains the information
    for you data. You will need to enter publication/dataset information,
    and specify the types of surfaces, facets and reactions. 

    The 'reactions' key is a list of dictionaries. 
    A new dictionary is required for each reaction, and should include two 
    lists, 'reactants' and 'products'. Remember to balance the equation and 
    include a minus sign in the name when relevant.

    'reactions': [
        {
          'reactants': ['CCH3star@ontop'], 
          'products': ['Cstar@hollow', 'CH3star@ontop']
        },
        {
           'reactants': ['CH4gas', '-0.5H2gas', 'star'],
           'products':  ['CH3star']
        }
     ]

    Also, include the phase and of the species as an extension:
      'gas' for gas phase (i.e. CH4 -> CH4gas)
      'star' for empty site or adsorbed phase. (i.e. OH -> OHstar)

    The site of adsorbed species is also included as an extension:
      '@site' (i.e. OHstar in bridge-> OHstar@bridge)

    Then, save the template and call:
    
    $ cathub make_folders <template_name>

    And folders will be created automatically. 

    You can create several templates and call make_folders again
    if you, for example, are using different functionals or are 
    doing different reactions on different surfaces.
    """
    import make_folders_template
    import json
    import os

    if custom_base is None:
        custom_base = os.path.abspath(os.path.curdir)

    template_data = {
        'title': 'Fancy title',
        'authors': ['Doe, John', 'Einstein, Albert'],
        'journal': 'JACS',
        'volume': '1',
        'number': '1',
        'pages': '23-42',
        'year': '2017',
        'publisher': 'ACS',
        'doi': '10.NNNN/....',
        'DFT_code': 'Quantum Espresso',
        'DFT_functional': 'BEEF-vdW',
        'reactions': [
                {'reactants': ['2.0H2Ogas', '-1.5H2gas', 'star'], 
                 'products': [ 'OOHstar@top']},
                {'reactants': ['CCH3star@bridge'], 'products': ['Cstar@hollow', 'CH3star@ontop']},
                {'reactants': ['CH4gas', '-0.5H2gas', 'star'], 'products': ['CH3star@ontop']}
        ],
        'bulk_compositions': ['Pt'],
        'crystal_structures': ['fcc', 'hcp'],
        'facets': ['111']
    }
    if template is not None:
        if create_template:
            if os.path.exists(template):
                raise UserWarning(
                    "File {template} already exists. Refusing to overwrite".format(**locals()))
            with open(template, 'w') as outfile:
                outfile.write(json.dumps(template_data, indent=4,
                                         separators=(',', ': '), sort_keys=True) + '\n')
                return
        else:
            with open(template) as infile:
                template_data = json.load(infile)
                title = template_data['title']
                authors = template_data['authors']
                journal = template_data['journal']
                volume = template_data['volume']
                number = template_data['number']
                pages = template_data['pages']
                year = template_data['year']
                publisher = template_data['publisher']
                doi = template_data['doi']
                dft_code = template_data['DFT_code']
                dft_functional = template_data['DFT_functional']
                reactions = template_data['reactions']
                crystal_structures = template_data['crystal_structures']
                bulk_compositions = template_data['bulk_compositions']
                facets = template_data['facets']

    make_folders_template.main(
        title=title,
        authors=eval(authors) if isinstance(
            authors, six.string_types) else authors,
        journal=journal,
        volume=volume,
        number=number,
        pages=pages,
        year=year,
        publisher=publisher,
        doi=doi,
        DFT_code=dft_code,
        DFT_functional=dft_functional,
        reactions=eval(reactions) if isinstance(
            reactions, six.string_types) else reactions,
        custom_base=custom_base,
        bulk_compositions=bulk_compositions,
        crystal_structures=crystal_structures,
        facets=facets
    )


@cli.command()
def psql_server_connect():
    """Test connection to PostreSQL server."""
    import psql_server_connect


@cli.command()
@click.argument('user')
@click.argument('pub_level')
@click.argument('DFT_level')
@click.argument('XC_level')
@click.argument('reaction_level')
@click.argument('metal_level')
@click.argument('facet_level')
@click.argument('site_level')
@click.argument('final_level')
def write_user_spec():
    """Write JSON specfile for single DFT calculation."""
    import write_user_spec
