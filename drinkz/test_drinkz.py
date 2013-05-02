"""
Test code to be run with 'nosetests'.

Any function starting with 'test_', or any class starting with 'Test', will
be automatically discovered and executed (although there are many more
rules ;).
"""

import sys
sys.path.insert(0, 'bin/') # allow _mypath to be loaded; @CTB hack hack hack

from cStringIO import StringIO
import imp

from . import db, load_bulk_data

from drinkz.recipes import Recipe

def test_foo():
    # this test always passes; it's just to show you how it's done!
    print 'Note that output from passing tests is hidden'

def test_add_bottle_type_1():
    print 'Note that output from failing tests is printed out!'
    
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')

def test_add_to_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

def test_add_to_inventory_2():
    db._reset_db()

    try:
        db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
        assert False, 'the above command should have failed!'
    except db.LiquorMissing:
        # this is the correct result: catch exception.
        pass

def test_get_liquor_amount_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount

def test_bulk_load_inventory_1():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 1, n

def test_get_liquor_amount_2():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1000 ml"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1000, amount

def test_bulk_load_bottle_types_1():
    db._reset_db()

    data = "Johnnie Walker,Black Label,blended scotch"
    fp = StringIO(data)                 # make this look like a file handle
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 1, n


def test_get_liquor_inventory():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

    x = []
    for mfg, liquor in db.get_liquor_inventory():
        x.append((mfg, liquor))

    assert x == [('Johnnie Walker', 'Black Label')], x

def test_ignore_commented_lines_booze():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_bottle_type('Captain', 'Morgan', 'Rum')

    data = open("test-data/data1.txt", "r")  

    stringdata = data.read()
    fp = StringIO(stringdata)
    n = load_bulk_data.load_inventory(fp)

    assert db.check_inventory('Johnnie Walker', 'Black Label')
    assert n == 2, n


def test_ignore_commented_lines_type():
    db._reset_db()

    data = open("test-data/data1.txt", "r")  

    stringdata = data.read()
    fp = StringIO(stringdata)
    n = load_bulk_data.load_bottle_types(fp)

    assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
    assert n == 2, n

def test_get_liquor_amount_3():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = open("test-data/data2.txt", "r")  

    stringdata = data.read()

    fp = StringIO(stringdata)                 # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 1088.7205, amount

def test_script_load_liquor_inventory_1():
    #db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    #db.add_bottle_type('Captain', 'Morgan', 'Rum')
    scriptpath = 'bin/load-liquor-inventory'
    module = imp.load_source('llt', scriptpath)
    exit_code = module.main([scriptpath, 'test-data/bottle-types-data-1.txt','test-data/inventory-data-1.txt', 'test-data/recipe-data-1.txt'])

    assert exit_code == 0, 'non zero exit code %s' % exit_code


def test_get_liquor_amount_gallon():
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    
    data = "Johnnie Walker,Black Label,1 gallon"
    fp = StringIO(data) # make this look like a file handle
    n = load_bulk_data.load_inventory(fp)

    amount = db.get_liquor_amount('Johnnie Walker', 'Black Label')
    assert amount == 3785.41, amount

def test_uniqify_inventory():
    """
Ensure that get_liquor_inventory doesn't return duplicates.
"""
    db._reset_db()

    db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '500 ml')
    db.add_to_inventory('Johnnie Walker', 'Black Label', '25 ml')

    uniq = set()
    for mfg, liquor in db.get_liquor_inventory():
        assert (mfg, liquor) not in uniq, "dup: %s, %s" % (mfg, liquor)
        uniq.add((mfg, liquor))

    assert len(uniq) == 1, "should only be one mfg/liquor in inventory"


def test_check_type_exists():
	db._reset_db()
	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
	db.add_bottle_type('Jameson', 'Delicious', 'blended scotch')

	typs = db.check_inventory_for_type('blended scotch')
	temp = set([('Johnnie Walker', 'Black Label'),('Jameson', 'Delicious')])

	assert typs.issubset(temp)
	

def test_save_load():
	db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
	db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')
	r = Recipe('scotch on the rocks', [('blended scotch','4 oz')], 5, 1)

	db.add_recipe(r)

	r = Recipe('gin and tonic', [('gin','4 oz')])

	db.add_recipe(r)


	db.save_db("testsave")
	db._reset_db()
	db.load_db("testsave")

	x = list(db.get_all_recipes())

	assert len(x) == 2
	assert db._check_bottle_type_exists('Johnnie Walker', 'Black Label')
	assert db.check_inventory('Johnnie Walker', 'Black Label')


def test_can_make():
	db._reset_db()

	db.add_bottle_type('Johnnie Walker', 'Black Label', 'blended scotch')
	db.add_to_inventory('Johnnie Walker', 'Black Label', '1000 ml')

	db.add_bottle_type('Coca-Cola', 'cola', 'cola')
	db.add_to_inventory('Coca-Cola', 'cola', '1000 ml')

	r = Recipe('whiskey coke', [('blended scotch','4 oz'),('cola','2 oz')])
	
	db.add_recipe(r)

	r = Recipe('gin and tonic', [('gin','4 oz')])

	db.add_recipe(r)

	assert len(db.can_make()) == 1
