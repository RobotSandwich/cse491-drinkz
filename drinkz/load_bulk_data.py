"""
Module to load in bulk data from text files.
"""

# ^^ the above is a module-level docstring.  Try:
#
#   import drinkz.load_bulk_data
#   help(drinkz.load_bulk_data)
#

import csv                              # Python csv package

from . import db                        # import from local package

def load_bottle_types(fp):
	"""
    Loads in data of the form manufacturer/liquor name/type from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of bottle types loaded
    """
	reader = csv.reader(fp)

	x = []
	n = 0
	while True:
		try:
			for (mfg, name, typ) in reader:
				print "mfg: ", mfg, ":", name, ":", typ
				if not mfg[0] == "#":
					db.add_bottle_type(mfg, name, typ)
					n += 1
			return n
		except ValueError:
			print "ValueError in load type"
		except db.LiquorMissing:
			print "liquor missing in load type"
		except IndexError:
			print "Chmon LEE!"

def load_inventory(fp):
	"""
    Loads in data of the form manufacturer/liquor name/amount from a CSV file.

    Takes a file pointer.

    Adds data to database.

    Returns number of records loaded.

    Note that a LiquorMissing exception is raised if bottle_types_db does
    not contain the manufacturer and liquor name already.
    """
	reader = csv.reader(fp)

	x = []
	n = 0
	while True:
		try:
			for (mfg, name, amount) in reader:
				if not mfg[0] == '#':
					db.add_to_inventory(mfg, name, amount)
					n += 1
			return n
		except ValueError:
			print "ValueError in Load inventory"
		except db.LiquorMissing:
			print "liquor missign in load inventory"
