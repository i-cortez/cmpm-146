import pyhop
import json

def check_enough (state, ID, item, num):
	if getattr(state,item)[ID] >= num: return []
	return False

def produce_enough (state, ID, item, num):
	return [('produce', ID, item), ('have_enough', ID, item, num)]

pyhop.declare_methods ('have_enough', check_enough, produce_enough)

def produce (state, ID, item):
	return [('produce_{}'.format(item), ID)]

pyhop.declare_methods ('produce', produce)

def make_method (name, rule):
	def method (state, ID):
		methods = []

		if 'Requires' in rule:
		  for item, num in rule['Requires'].items():
			  methods.append(('have_enough', ID, item, num))

		if 'Consumes' in rule:	
		  for item, num in rule['Consumes'].items():
			  methods.append(('have_enough', ID, item, num))

		methods.append((('op_' + name), ID))
		
		return methods
	method.__name__ = name.replace(" ", "_")
	# print("New Method: " + method.__name__)
	return method


def declare_methods(data):
    # some recipes are faster than others for the same product even though they might require extra tools
    # sort the recipes so that faster recipes go first

    # your code here
    # hint: call make_method, then declare the method to pyhop using pyhop.declare_methods('foo', m1, m2, ..., mk)
	methods = {}

	# sort by time
	for name, recipe in sorted(data['Recipes'].items(), key=lambda item: item[1]['Time'], reverse=False):
		name = name.replace(' ', '_')
		for product in recipe["Produces"].items():
			new_method = {product: make_method(name,recipe)}
			methods.update(new_method)

	for product, method in methods.items():
		pyhop.declare_methods('produce_' + product[0], method)	

def make_operator(rule):
	def operator (state, ID):
		# your code here
		if 'Requires' in rule:
			for item, quantity in rule['Requires'].items():
				if not getattr(state, item)[ID] >= quantity:
					return False
		if 'Consumes' in rule:
			for item, quantity in rule['Consumes'].items():
				if getattr(state, item)[ID] >= quantity:
					setattr(state, item, {ID: quantity - getattr(state, item)[ID]})
				else:
					return False
		if 'Produces' in rule:
				for item, quantity in rule['Produces'].items():
					setattr(state, item, {ID: quantity - getattr(state, item)[ID]})
		state.time[ID] -= rule['Time']
		return state
	return operator


def declare_operators(data):
    # your code here
    # hint: call make_operator, then declare the operator to pyhop using pyhop.declare_operators(o1, o2, ..., ok)
    operators = []

    for name, rule in sorted(data['Recipes'].items(), key=lambda item: item[1]['Time'], reverse=False):
        name = name.replace(' ', '_')
        operator = make_operator(rule)
        operator.__name__ = 'op_' + name
        operators.append(operator)

    for operator in operators:
        pyhop.declare_operators(operator)

    return

def add_heuristic (data, ID):
	# prune search branch if heuristic() returns True
	# do not change parameters to heuristic(), but can add more heuristic functions with the same parameters: 
	# e.g. def heuristic2(...); pyhop.add_check(heuristic2)
	def heuristic (state, curr_task, tasks, plan, depth, calling_stack):
		# your code here
		return False # if True, prune this branch

	pyhop.add_check(heuristic)


def set_up_state (data, ID, time=0):
	state = pyhop.State('state')
	state.time = {ID: time}

	for item in data['Items']:
		setattr(state, item, {ID: 0})

	for item in data['Tools']:
		setattr(state, item, {ID: 0})

	for item, num in data['Initial'].items():
		setattr(state, item, {ID: num})

	return state

def set_up_goals (data, ID):
	goals = []
	for item, num in data['Goal'].items():
		goals.append(('have_enough', ID, item, num))

	return goals

if __name__ == '__main__':
	rules_filename = 'crafting.json'

	with open(rules_filename) as f:
		data = json.load(f)

	state = set_up_state(data, 'agent', time=300) # allot time here
	goals = set_up_goals(data, 'agent')

	declare_operators(data)
	declare_methods(data)
	add_heuristic(data, 'agent')

	# pyhop.print_operators()
	# pyhop.print_methods()

	# Hint: verbose output can take a long time even if the solution is correct; 
	# try verbose=1 if it is taking too long

	# pyhop.pyhop(state, goals, verbose=3)

	#a test
	#pyhop.pyhop(state, [('have_enough', 'agent', 'plank', 1)], verbose=3)

	#b test
	pyhop.pyhop(state, [('have_enough', 'agent', 'wooden_pickaxe', 1)], verbose=1)

	# pyhop.pyhop(state, [('have_enough', 'agent', 'cart', 1),('have_enough', 'agent', 'rail', 20)], verbose=3)