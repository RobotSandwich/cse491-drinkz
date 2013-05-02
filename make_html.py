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
<script type="text/javascript" charset="utf-8" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
	</head>
	<body>
	"""

	print >>fp, "<h1>Welcome to The Lush.</h1>" 

	print >>fp, "<p><a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "
	print >>fp, "<a href='form'>Convert-to-ml</a> "

	print >>fp, "<p><p> This will one day be the ultimate tool for any hardy drinker. Sadly it is still a work in development. <p>Feel free to try out the available tools. <p>Remember you must be signed in to vote on recipes!"


	fp.close()

	###


	###

	fp = open('html/liquor_types.html', 'w')
	print >>fp, """<html>
	<head>
	<title>Liquor Types.</title>
	<style type='text/css'>
	h1 {color:black;}
	body {
	font-size: 14px;
	}
	</style>
	</script>
	</head>
	<body>
	"""
	print >>fp, "<h1>Types of Liquor </h1> "
	print >>fp, "<p><a href='/'>HomePage</a> "
	print >>fp, "<a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "
	print >>fp, "<p><a href='form_add_type'>Add a New Type</a> "
	print >>fp, '<script type="text/javascript"src="jquery-1.2.6.min.js"></script><script type="text/javascript" src="jquery.form.js"></script><script type="text/javascript" src="application.js"></script>'


	print >>fp, "<b><p>Liquor<p></b>"


	###

	###

	fp = open('html/inventory.html', 'w')

	print >>fp, """<html>
	<head>
	<title>Inventory Page.</title>
	<style type='text/css'>
	h1 {color:black;}
	body {
	font-size: 14px;
	}
	</style>
	</script>
	</head>
	<body>
	"""
	print >>fp, "<h1>Current Inventory </h1> "
	print >>fp, "<p><a href='/'>HomePage</a> "
	print >>fp, "<a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "
	print >>fp, "<p><a href='form_add_inv'>Add a New Inventory</a> "

	print >>fp, "<b><p>Name   :  Liquor    :   Amount in ml<p></b>"

	fp.close()

	###

	###

	fp = open('html/recipes.html', 'w')

	print >>fp, """<html>
	<head>
	<title>Recipe List.</title>
	<style type='text/css'>
	h1 {color:black;}
	body {
	font-size: 14px;
	}
	</style>
	</script>
	</head>
	<body>
	"""

	print >>fp, "<h1>Recipes </h1> "
	print >>fp, "<p><a href='/'>HomePage</a> "
	print >>fp, "<a href='liquortypes'>Types of Liquor</a> "
	print >>fp, "<a href='inventory'>Inventory of Booze</a> "
	print >>fp, "<a href='recipes'>Recipe List</a> "
	print >>fp, "<p><a href='form_add_recipe'>Add a New Recipe</a> "
	print >>fp, "<p>If you are logged in voting forms will appear next to each recipe. <p> Feel free to throw in your opinion and help decide what recipe is forever the best. <p> Scores are from 1-5 "
	print >>fp, "<b><p>Score  :  Name   :  Ingredients<p></b>"



	fp.close()

	###
	return 0

