"""
Database functionality for drinkz information.
"""
import recipes
from cPickle import dump, load

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
#storing recipes in a set cus uniqueness is important and order is not
_recipes = set([])

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes
    _bottle_types_db.clear()
    _inventory_db = {}
    _recipes.clear()

def save_db(filename):
    fp = open(filename, 'wb')

    tosave = (_bottle_types_db, _inventory_db, _recipes)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes
    fp = open(filename, 'rb')

    loaded = load(fp)
    (_bottle_types_db, _inventory_db, _recipes) = loaded

    fp.close()

# exceptions in Python inherit from Exception and generally don't need to
# override any methods.
class DuplicateRecipeName(Exception):
    pass

class LiquorMissing(Exception):
    pass

def add_bottle_type(mfg, liquor, typ):
    "Add the given bottle type into the drinkz database."
    _bottle_types_db.add((mfg, liquor, typ))

def _check_bottle_type_exists(mfg, liquor):
    for (m, l, _) in _bottle_types_db:
        if mfg == m and liquor == l:
            return True

    return False

def add_to_inventory(mfg, liquor, amount):
	"Add the given liquor/amount to inventory."
	if not _check_bottle_type_exists(mfg, liquor):
		err = "Missing liquor: manufacturer '%s', name '%s'" % (mfg, liquor)
		raise LiquorMissing(err)

	if not (mfg,liquor) in _inventory_db:
		_inventory_db[mfg,liquor] = list([])
	
	_inventory_db[mfg,liquor].append(amount)

def check_inventory(mfg, liquor):
    for key in _inventory_db:
        if key[0] == mfg and liquor == key[1]:
            return True
        
    return False

#returns a set of mfg/liquor tuples.
def check_inventory_for_type(typ):
	Set = set([])
	for key in _bottle_types_db:
		if key[2] == typ:
			Set.add( (key[0], key[1]) )
	return Set


def get_liquor_amount(mfg, liquor):
	"Retrieve the total amount of any given liquor currently in inventory. prints ml"
	amount = 0
	for key in _inventory_db:
		if key[0] == mfg and liquor == key[1]:
			temp = _inventory_db[key]
			for i in temp:
				amount += convert_to_ml(i)
        
	return amount

def convert_to_ml(amount):
   # amount is going to be in format "number units"
   num, units = amount.split()
   num = float(num)
   units = units.lower()

   if units == 'ml':
      return num
   elif units == 'oz':
      return 29.5735 * num
   elif units == 'gallon':
      return 3785.41 * num
   elif units == 'liter':
      return 1000.00 * num
   else:
      raise Exception("unknown unit %s" % units)


def get_liquor_inventory():
    #"Retrieve all liquor types in inventory, in tuple form: (mfg, liquor)."
    for key in _inventory_db:
        yield key[0], key[1]

def get_liquor_inventory_types():
    #"Retrieve all liquor types in inventory"
    for key in _bottle_types_db:
		yield key[2]

def add_recipe(r):
	for i in _recipes:
		if i.get_name() == r.get_name():
			raise DuplicateRecipeName(r.get_name())
	_recipes.add(r)
	

def get_recipe(name):
	for i in _recipes:
		if i.get_name() == name:
			return i
	else:
		return 0

def get_all_recipes():
	for i in _recipes:
		yield i

