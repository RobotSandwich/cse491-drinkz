import app
import urllib
import drinkz.db

def test_index():
    environ = {}
    environ['PATH_INFO'] = '/'
    
    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)

    text = "".join(results)
    status, headers = d['status'], d['headers']
    
    assert text.find('Visit:') != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'

def test_form_recv():
    environ = {}
    environ['QUERY_STRING'] = urllib.urlencode(dict(firstname='FOO',
                                                    lastname='BAR'))
    environ['PATH_INFO'] = '/recv'

    d = {}
    def my_start_response(s, h, return_in=d):
        d['status'] = s
        d['headers'] = h

    app_obj = app.SimpleApp()
    results = app_obj(environ, my_start_response)
    
    text = "".join(results)
    status = d['status']
    headers = d['headers']

    assert text.find("First name: FOO; last name: BAR.") != -1, text
    assert ('Content-type', 'text/html') in headers
    assert status == '200 OK'


def test_recipes():
	db._reset_db()

	t = recipes.Recipe('Gin and Tonic', [('gin','4 oz')])
	db.add_recipe(t)
	r = recipes.Recipe('Pickle Back', [('whiskey','4 oz'),('pickle juice','2 oz')])
	db.add_recipe(r)
    
