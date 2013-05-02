from drinkz.app import SimpleApp
from drinkz import db
from drinkz import recipes
import simplejson
from cStringIO import StringIO

def make_rpc_call(fn_name, params):
    d = dict(method=fn_name, params=params, id="0")
    encoded = simplejson.dumps(d)
    
    environ = {}
    environ['PATH_INFO'] = '/rpc'
    environ['REQUEST_METHOD'] = 'POST'
    environ['wsgi.input'] = StringIO(encoded)
    environ['CONTENT_LENGTH'] = len(encoded)

    d = {}
    def my_start_response(s, h):
        d['status'] = s
        d['headers'] = h

    app_obj = SimpleApp()
    response = app_obj(environ, my_start_response)

    x = "".join(response)
    response = simplejson.loads(x)
    
    return response['result']

def test_json_convert():
    x = make_rpc_call('convert_units_to_ml', ['15 oz'])
    assert '443.6025 ml' == x, x

def test_json_recipes():
    db._reset_db()

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
    
    r = recipes.Recipe('whiskey bath', [('blended scotch', '2 liter')])
    db.add_recipe(r)

    x = make_rpc_call('get_recipe_names', [])
    assert 'whiskey bath' in x

def test_json_inventory():
    db._reset_db()

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
    
    r = recipes.Recipe('whiskey bath', [('blended scotch', '2 liter')])
    db.add_recipe(r)

    x = make_rpc_call('get_liquor_inventory', [])
    assert x == [[u"Uncle Herman's", u'moonshine']]

def test_add_bottle_type():
    db._reset_db()

    make_rpc_call('add_bottle_type',
                  ('Uncle Herman\'s', 'moonshine', 'blended scotchX'))

    # this will fail without the above working.
    x = make_rpc_call('add_to_inventory',
                      ('Uncle Herman\'s', 'moonshine', '5 liter'))
    
    x = make_rpc_call('get_liquor_inventory', [])
    assert x == [[u"Uncle Herman's", u'moonshine']]

def test_add_to_inventory():
    db._reset_db()

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')

    x = make_rpc_call('add_to_inventory',
                      ('Uncle Herman\'s', 'moonshine', '5 liter'))
    
    x = make_rpc_call('get_liquor_inventory', [])
    assert x == [[u"Uncle Herman's", u'moonshine']]

def test_json_add_recipe():
    db._reset_db()

    db.add_bottle_type('Uncle Herman\'s', 'moonshine', 'blended scotch')
    db.add_to_inventory('Uncle Herman\'s', 'moonshine', '5 liter')
    
    make_rpc_call('add_recipe',
                  (('whiskey bath', [('blended scotch', '2 liter')])))

    x = make_rpc_call('get_recipe_names', [])
    assert 'whiskey bath' in x

