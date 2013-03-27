import os
from drinkz import db, recipes

### first we do the dirty

def main():

	db._reset_db()

	db.load_db("database")




	###
	try:
		os.mkdir('html')
	except OSError:
		# already exists
		pass


	###

	fp = open('index.html', 'w')

	print >>fp, """<html>
	<head>
	<title>The Lush - A Alcoholic Database.</title>
	<style type='text/css'>
	h1 {color:black;}
	body {
	font-size: 14px;
	}
	</style>
	<script>
	function myFunction()
	{
	alert("Hello! I am an alert box!");
	}
	</script>
	</script>
	</head>
	<body>
	"""

	print >>fp, "<h1>Welcome to The Lush.</h1>" 

	print >>fp, "<p><a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "
	print >>fp, "<a href='form'>Convert-to-ml</a> "

	print >>fp, "<p><p> This will one day be the ultimate tool for any hardy drinker. Sadly it is still a work in development. Feel free to try out the available tools. "
	print >> fp, '<p><button onclick="myFunction()">Try out our cool buttons!</button>'
	fp.close()

	###


	###

	fp = open('html/liquor_types.html', 'w')
	print >>fp, """<html>
	<head>
	<title>The Lush - Available Types of Liquor.</title>
	<style type='text/css'>
	h1 {color:red;}
	body {
	font-size: 14px;
	}
	</style>
	</script>
	</head>
	<body>
	"""
	print >>fp, "<p><h1>Types of Liquor </h1> "
	print >>fp, "<p><a href='/'>HomePage</a> "
	print >>fp, "<p><a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "


	print >>fp, "<b><p>Type<p></b>"
	for mfg in db.get_liquor_inventory_types():
		print>>fp, mfg
		print >>fp, "<p>"
	fp.close()

	###

	###

	fp = open('html/inventory.html', 'w')

	print >>fp, """<html>
	<head>
	<title>The Lush - Current Inventory.</title>
	<style type='text/css'>
	h1 {color:red;}
	body {
	font-size: 14px;
	}
	</style>
	</script>
	</head>
	<body>
	"""
	print >>fp, "<p><h1>Current Inventory </h1> "
	print >>fp, "<p><a href='/'>HomePage</a> "
	print >>fp, "<p><a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "

	print >>fp, "<b><p>Name   :  Ingredients    :   Amount in ml<p></b>"
	for mfg, liquor in db.get_liquor_inventory():
		print>>fp, mfg, " : ", liquor, " : ", db.get_liquor_amount(mfg, liquor )
		print >>fp, "<p>"

	fp.close()

	###

	###

	fp = open('html/recipes.html', 'w')

	print >>fp, """<html>
	<head>
	<title>The Lush - Recipe List.</title>
	<style type='text/css'>
	h1 {color:red;}
	body {
	font-size: 14px;
	}
	</style>
	</script>
	</head>
	<body>
	"""

	print >>fp, "<p><h1>Recipes </h1> "
	print >>fp, "<p><a href='/'>HomePage</a> "
	print >>fp, "<p><a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "

	x = list(db.get_all_recipes())
	print >>fp, "<b><p>Name   :  Ingredients<p></b>"
	for i in x:
		print >>fp, i.get_name(),":"
		for z in i.get_ingredients():
			print >>fp, z, "+"
		print >>fp, "<p>"


	fp.close()

	###
	return 0

