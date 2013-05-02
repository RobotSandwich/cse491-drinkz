"""
Database functionality for drinkz information.
"""
import recipes
from cPickle import dump, load
import sqlite3, os
from cStringIO import StringIO

# private singleton variables at module level
_bottle_types_db = set([])
_inventory_db = {}
#storing recipes in a set cus uniqueness is important and order is not
_recipes = set([])
#This is a list containing all user's voting information
_voted = set([])

def get_liquor_amount(mfg, liquor):
	"Retrieve the total amount of any given liquor currently in inventory. prints ml"
	amount = 0
	for key in _inventory_db:
		if key[0] == mfg and liquor == key[1]:
			temp = _inventory_db[key]
			for i in temp:
				amount += convert_to_ml(i)
        
	return amount

def _reset_db():
    "A method only to be used during testing -- toss the existing db info."
    global _bottle_types_db, _inventory_db, _recipes
    _bottle_types_db.clear()
    _inventory_db = {}
    _recipes.clear()
    _voted.clear()

def save_db(filename):
    fp = open(filename, 'wb')
    dbSQL = sqlite3.connect('data.db')
    c = dbSQL.cursor()

    c.execute('DELETE FROM Type')
    c.execute('DELETE FROM Inventory')
    c.execute('DELETE FROM Recipe')
    for i in _bottle_types_db:
        n = i[0]
        m = i[1]
        o = i[2]
        c.execute('INSERT INTO Type (mfg, lqr, typ) VALUES (?, ?, ?)', (n, m, o))
    for i in _inventory_db:
        n = i[0]
        m = i[1]
        o = str(get_liquor_amount(i[0], i[1])) + " ml"
        c.execute('INSERT INTO Inventory (mfg, lqr, amt) VALUES (?, ?, ?)', (n, m, o))
    for i in _recipes:
        n = i.get_name()
        m = int(i.get_score())
        o = int(i.get_votes())
        p = str(i.get_str_ingredients()) 
        c.execute('INSERT INTO Recipe (name, score, votes, ing) VALUES (?, ?, ?, ?)', (n, m, o, p))
    dbSQL.commit()
    tosave = (_recipes, _voted)
    dump(tosave, fp)

    fp.close()

def load_db(filename):
    global _bottle_types_db, _inventory_db, _recipes, _voted
    fp = open(filename, 'rb')

    dbSQL = sqlite3.connect('data.db')
    c = dbSQL.cursor()

    c.execute('SELECT * FROM Type')
    results = c.fetchall()
    for i in results:
        add_bottle_type(str(i[0]), str(i[1]), str(i[2]))

    c.execute('SELECT * FROM Inventory')
    results = c.fetchall()
    for i in results:
        add_to_inventory(str(i[0]), str(i[1]), str(i[2]))


    loaded = load(fp)
    (_recipes, _voted) = loaded
    c.close()
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
        yield (key[0], key[1])

def get_liquor_inventory_types():
    #"Retrieve all liquor types in inventory"
    for key in _bottle_types_db:
		yield key[2]

def get_all_liquor_inventory_types():
    for key in _bottle_types_db:
        yield key

def get_all_liquor_inventory():
    for key in _inventory_db:
        yield key


def add_recipe(r):
	for i in _recipes:
		if i.get_name() == r.get_name():
			raise DuplicateRecipeName(r.get_name())
	_recipes.add(r)
	
#given a name return the recipe of the same name
def get_recipe(name):
	for i in _recipes:
		if i.get_name() == name:
			return i
	else:
		return 0

#generator returning all the recipes
def get_all_recipes():
	for i in _recipes:
		yield i

#returns a list of all the recipes we can make with the current inventory
def can_make():
	makeable = list()
	for i in _recipes:
		if (len(i.need_ingredients()) == 0):
			makeable.append(i)
	return makeable


def user_voted(user, recName):
    _voted.add( str(user) + str(recName) )

def get_voted(user, recName):
    return ( str(user) + str(recName)) in _voted



