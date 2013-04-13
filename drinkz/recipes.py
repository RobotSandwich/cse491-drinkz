import db

class Recipe:

	def __init__(self, name, ingredients):
		self._ingredients = set([])
		self._name = name
		for ing in ingredients:
			self._ingredients.add(ing)

	def get_name(self):
		return self._name

	def get_ingredients(self):
		for i in self._ingredients:
			yield i

	def need_ingredients(self):
		Available = []
		Needed = {}
		List = list()      
		for i in self._ingredients:
			items = db.check_inventory_for_type(i[0])
			#this is the amt we need in ml
			amt = db.convert_to_ml(i[1])
			Needed[i[0]] = amt
			for x in items:
				amt_avl = db.get_liquor_amount(x[0], x[1])
				#if the current amt_avl is the largest so far then remove it from the amount needed
				if (amt - amt_avl) < Needed[i[0]]:
					Needed[i[0]] = amt - amt_avl
			
			#The amount needed for the recipe will be less than 0 after this point if there is enough liquor available. So remove it from the Dictionary of needed ingredients
			if Needed[i[0]] <= 0.0:
				del Needed[i[0]]

		#put all the elements from the dictionary into a List 
		for i in Needed:
			List.append( (i, Needed[i]) )
		return List

		
