# recipe_line_parser
Simple but effective recipe line parser

There are a lot of python parsers out there, but a lot of them are either too simple and ineffective, or too complicated (like the NLP machine learning ones) that are too difficult to set up.
I basically created something that is based off of input from my own recipe collection.

To use, just import it:
from parse_ingredient_line import parse_ingredient_line

parse_ingredient_line('1 1/2 cup shredded monterray jack cheese, divided')

returns:

{'notes': ['divided'], 'ingredient': 'shredded monterray jack cheese', 'amount': '1 1/2', 'measurement': 'cup'}
