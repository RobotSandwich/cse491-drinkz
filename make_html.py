import os
from drinkz import db, recipes

### first we do the dirty


db._reset_db()

db.add_bottle_type('Captain Morgan', 'Rum', 'spiced rum')
db.add_bottle_type('Seagrams', 'Fine Gin', 'gin')
db.add_bottle_type('Canada House', 'Canadian Whiskey', 'whiskey')
db.add_to_inventory('Captain Morgan', 'Rum', '2 liter')
db.add_to_inventory('Canada House', 'Canadian Whiskey', '5 oz')


t = recipes.Recipe('Gin and Tonic', [('gin','4 oz')])
db.add_recipe(t)
r = recipes.Recipe('Pickle Back', [('whiskey','4 oz'),('pickle juice','2 oz')])
db.add_recipe(r)





###
try:
	os.mkdir('html')
except OSError:
	# already exists
	pass


###

fp = open('index.html', 'w')
print >>fp, "Hello, world.<p>"
print >>fp, "<p><a href='html/liquor_types.html'>Types of Liquor</a> "
print >>fp, "<a href='html/inventory.html'>Inventory of Booze</a> "
print >>fp, "<a href='html/recipes.html'>Recipe List</a> "



fp.close()

###

###

fp = open('html/liquor_types.html', 'w')
print >>fp, "<p><a href='liquor_types.html'>Types of Liquor</a> "
print >>fp, "<a href='inventory.html'>Inventory of Booze</a> "
print >>fp, "<a href='recipes.html'>Recipe List</a> <p><p>"

print >>fp, "<b>Type<p></b>"
for mfg in db.get_liquor_inventory_types():
	print>>fp, mfg
	print >>fp, "<p>"
fp.close()

###

###

fp = open('html/inventory.html', 'w')
print >>fp, "<p><a href='liquor_types.html'>Types of Liquor</a> "
print >>fp, "<a href='inventory.html'>Inventory of Booze</a> "
print >>fp, "<a href='recipes.html'>Recipe List</a> <p><p>"

print >>fp, "<b>Name   :  Ingredients    :   Amount in ml<p></b>"
for mfg, liquor in db.get_liquor_inventory():
	print>>fp, mfg, " : ", liquor, " : ", db.get_liquor_amount(mfg, liquor )
	print >>fp, "<p>"

fp.close()

###

###

fp = open('html/recipes.html', 'w')
print >>fp, "<p><a href='liquor_types.html'>Types of Liquor</a> "
print >>fp, "<a href='inventory.html'>Inventory of Booze</a> "
print >>fp, "<a href='recipes.html'>Recipe List</a> <p><p>"

x = list(db.get_all_recipes())
print >>fp, "<b>Name   :  Ingredients<p></b>"
for i in x:
	print >>fp, i.get_name(),":"
	for z in i.get_ingredients():
		print >>fp, z, "+"
	print >>fp, "<p>"


fp.close()

###

