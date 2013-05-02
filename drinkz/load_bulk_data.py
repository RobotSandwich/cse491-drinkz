"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db, recipes                        # import from local package

def load_bottle_types(fp):
    """
Loads in data of the form manufacturer/liquor name/type from a CSV file.

Takes a file pointer.

Adds data to database.

Returns number of bottle types loaded
"""
    reader = parse_csv(fp)

    x = []
    n = 0
    for line in reader:
        try:
            (mfg, name, typ) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
        
        n += 1
        db.add_bottle_type(mfg, name, typ)

    return n

def load_inventory(fp):
    """
Loads in data of the form manufacturer/liquor name/amount from a CSV file.

Takes a file pointer.

Adds data to database.

Returns number of records loaded.

Note that a LiquorMissing exception is raised if bottle_types_db does
not contain the manufacturer and liquor name already.
"""
    reader = parse_csv(fp)

    x = []
    n = 0

    for line in reader:
        try:
            (mfg, name, amount) = line
        except ValueError:
            print 'Badly formatted line: %s' % line
            continue
    
        n += 1
        db.add_to_inventory(mfg, name, amount)

    return n

def parse_csv(fp):
    reader = csv.reader(fp)

    for line in reader:
        if not line or not line[0].strip() or line[0].startswith('#'):
            continue

        yield line

def load_recipe(fp):
    """
Loads in data of the form "name/score/votesingredient/amnt/ingredient2/amnt2.... from a CSV file.

Takes a file pointer.

Adds data to database.

Returns number of records loaded.
"""
    reader = parse_csv(fp)

    
    n = 0
    ingr = []
    for line in reader:
         if ((len(line) % 2) != 1):
             raise ValueError
         name = line[0]
         score = line[1]
         votes = line[2]
         i = 3
         while i < len(line):
             ingr.append( (line[i], line[i + 1]) )
             i = i + 2
         r = recipes.Recipe(name, ingr,score, votes) 
         db.add_recipe(r)
         n = n + 1

    return n

