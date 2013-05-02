#! /usr/bin/env python
from wsgiref.simple_server import make_server
import urlparse
import simplejson
import drinkz.db
import drinkz.load_bulk_data
from cStringIO import StringIO
from Cookie import SimpleCookie
import jinja2
import uuid
dispatch = {
    '/' : 'index',
    '/content' : 'somefile',
    '/error' : 'error',
    '/helmet' : 'helmet',
    '/form' : 'form',
    '/recv' : 'recv',
    '/login_1' : 'login1',
    '/login1_process' : 'login1_process',
    '/logout' : 'logout',
    '/form_add_type' : 'form_add_type',
    '/recv_type' : 'recv_type',
    '/form_add_inv' : 'form_add_inv',
    '/recv_inv' : 'recv_inv',
    '/form_add_recipe' : 'form_add_recipe',
	'/recv_vote' : 'recv_vote',
    '/recv_recipe' : 'recv_recipe',
    '/rpc'  : 'dispatch_rpc',
	'/liquortypes'  : 'liquortypes',
	'/inventory'  : 'inventory',
	'/recipes'  : 'recipes'
}

html_headers = [('Content-type', 'text/html')]

usernames = {}

class SimpleApp(object):
    def __call__(self, environ, start_response):

        path = environ['PATH_INFO']
        fn_name = dispatch.get(path, 'error')

        # retrieve 'self.fn_name' where 'fn_name' is the
        # value in the 'dispatch' dictionary corresponding to
        # the 'path'.
        fn = getattr(self, fn_name, None)

        

        if fn is None:
            start_response("404 Not Found", html_headers)
            return ["No path %s found" % path]

        return fn(environ, start_response)
            
    def index(self, environ, start_response):
        data = open('index.html').read()
        start_response('200 OK', list(html_headers))
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                data += "<br><br> Logged in as: " + str(usernames.get(c.get('name1').value, "")) + "<br><br>"
                data += "<a href='logout'>Logout</a> "
        else:
	        data +="<p><form action='login1_process'> Username: <input type='text' name='name' size='15'> <input type='submit' value='log in'> </form>"
        return [data]

    def login1(self, environ, start_response):
        start_response('200 OK', list(html_headers))

        title = 'login'
        template = env.get_template('login1.html')
        return str(template.render(locals()))

    def login1_process(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        content_type = 'text/html'

        # authentication would go here -- is this a valid username/password,
        # for example?

        k = str(uuid.uuid4())
        usernames[k] = name

        headers = list(html_headers)
        headers.append(('Location', '/'))
        headers.append(('Set-Cookie', 'name1=%s' % k))

        start_response('302 Found', headers)
        return ["Redirect to liquor types..."]

    def logout(self, environ, start_response):
        if 'HTTP_COOKIE' in environ:
            c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
            if 'name1' in c:
                key = c.get('name1').value
                name1_key = key

                if key in usernames:
                    del usernames[key]
                    print 'DELETING'

        pair = ('Set-Cookie',
                'name1=deleted; Expires=Thu, 01-Jan-1970 00:00:01 GMT;')
        headers = list(html_headers)
        headers.append(('Location', '/'))
        headers.append(pair)

        start_response('302 Found', headers)
        return ["Redirect to /status..."]

    def liquortypes(self, environ, start_response):
        content_type = 'text/html'
        data = open('html/liquor_types.html').read()
        for mfg in drinkz.db.get_liquor_inventory_types():
           data += mfg + "<p>"

        start_response('200 OK', list(html_headers))
        return [data]

    def recipes(self, environ, start_response):
        content_type = 'text/html'
        data = open('html/recipes.html').read()
        for i in list(drinkz.db.get_all_recipes()):
            data += i.get_average() + " : "
            data += i.get_name() +" :"
            for z in i.get_ingredients():
                data += " " + z[0] + " " + z[1] + " "
                data = data[:-1]

            if 'HTTP_COOKIE' in environ:
                c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
                if 'name1' in c:
                    if not drinkz.db.get_voted( usernames.get(c.get('name1').value, ""), i.get_name()):
                        data += form_vote(i.get_name())
            data += "<p>"
        data += "<br><b>Recipes Available to Make</b><p>"
        for i in drinkz.db.can_make():
            data += i.get_name() + "<p>"

        start_response('200 OK', list(html_headers))
        return [data]

    def inventory(self, environ, start_response):
        content_type = 'text/html'
        data = open('html/inventory.html').read()
        for mfg, liq in drinkz.db.get_liquor_inventory():
            data += mfg + " : " + liq + " : "
            data += str(drinkz.db.get_liquor_amount(mfg, liq)) + "<p>"

        start_response('200 OK', list(html_headers))
        return [data]

    def error(self, environ, start_response):
        status = "404 Not Found"
        content_type = 'image/png'
        data = open('notfound.png', 'rb').read()
       
        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def helmet(self, environ, start_response):
        content_type = 'image/gif'
        data = open('Spartan-helmet-Black-150-pxls.gif', 'rb').read()

        start_response('200 OK', [('Content-type', content_type)])
        return [data]

    def form(self, environ, start_response):
        data = form()

        start_response('200 OK', list(html_headers))
        return [data]
   
    def recv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        firstname = results['ozamount'][0]
        content_type = 'text/html'

        try:
            firstname += " oz"
            firstname = drinkz.db.convert_to_ml(firstname)
            data = "Amount in ml: %s.  <a href='./'>return to index</a>" % (firstname)
        except:
            data = "unexpected input. <a href='./'>return to index</a>"


        start_response('200 OK', list(html_headers))
        return [data]

########################################
#Forms for Type
    def form_add_type(self, environ, start_response):
        data = form_add_type()

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_type(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        typ = results['type'][0]
        content_type = 'text/html'


        try:
            data = "Added: <p> %s : %s : %s.  <p><a href='liquortypes'>return to types</a>" % (mfg, liquor, typ)
            drinkz.db.add_bottle_type(mfg,liquor,typ)
        except:
            data = "unexpected input. <a href='./'>return to index</a>"

        
        drinkz.db.save_db("database")
        start_response('200 OK', list(html_headers))
        return [data]

########################################
#Forms for Inventory
    def form_add_inv(self, environ, start_response):
        data = form_add_inv()

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_inv(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        mfg = results['mfg'][0]
        liquor = results['liquor'][0]
        amt = results['amt'][0]
        measure = results['measure'][0]
        content_type = 'text/html'
        amt += " " + measure

        try:
            data = "Added: <p> %s : %s : %s.  <p><a href='inventory'>return to inventory</a>" % (mfg, liquor, amt)
        except:
            data = "unexpected input. <a href='./'>return to index</a>"

        try:
            drinkz.db.add_to_inventory(mfg,liquor,amt)
        except drinkz.db.LiquorMissing:
            data = "That brand does not exist in the database. Add the Type before adding it to the inventory. <p><a href='./'>return to index</a>"

        drinkz.db.save_db("database")
        start_response('200 OK', list(html_headers))
        return [data]

########################################
#Forms for Recipes
    def form_add_recipe(self, environ, start_response):
        data = form_add_recipe()

        start_response('200 OK', list(html_headers))
        return [data]

    def recv_recipe(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        name = results['name'][0]
        ingr = results['ingr'][0]
        content_type = 'text/html'
        recipe_temp = name + ",0"+ ",0" +"," + ingr

        try:
            fp = StringIO(recipe_temp)
            drinkz.load_bulk_data.load_recipe(fp)
            data = "Added: <p> %s.  <p><a href='recipes'>return to recipes</a>" % (name)
        except:
            data = "unexpected input. <a href='./'>return to index</a>"

        drinkz.db.save_db("database")
        start_response('200 OK', list(html_headers))
        return [data]

    def recv_vote(self, environ, start_response):
        formdata = environ['QUERY_STRING']
        results = urlparse.parse_qs(formdata)

        try:
            voteScore = results['voteScore'][0]
            currentVote = results['currentVote'][0]
            for i in list(drinkz.db.get_all_recipes()):
                if i.get_name() == currentVote:
                    data = "Vote Succesful. <a href='recipes'>return to recipes</a>"
                    i.add_vote(voteScore)
            if 'HTTP_COOKIE' in environ:
                c = SimpleCookie(environ.get('HTTP_COOKIE', ''))
                if 'name1' in c:
                    drinkz.db.user_voted( usernames.get(c.get('name1').value, ""), currentVote)
            

        except:
            data = "unexpected input. <a href='./'>return to index</a>"


        drinkz.db.save_db("database")
        start_response('200 OK', list(html_headers))
        return [data]
########################################

    def dispatch_rpc(self, environ, start_response):
        # POST requests deliver input data via a file-like handle,
        # with the size of the data specified by CONTENT_LENGTH;
        # see the WSGI PEP.
        
        if environ['REQUEST_METHOD'].endswith('POST'):
            body = None
            if environ.get('CONTENT_LENGTH'):
                length = int(environ['CONTENT_LENGTH'])
                body = environ['wsgi.input'].read(length)
                response = self._dispatch(body) + '\n'
                start_response('200 OK', [('Content-Type', 'application/json')])

                return [response]

        # default to a non JSON-RPC error.
        status = "404 Not Found"
        content_type = 'text/html'
        data = "Couldn't find your stuff."
       
        start_response('200 OK', list(html_headers))
        return [data]

    def _decode(self, json):
        return simplejson.loads(json)

    def _dispatch(self, json):
        rpc_request = self._decode(json)

        method = rpc_request['method']
        params = rpc_request['params']
        
        rpc_fn_name = 'rpc_' + method
        fn = getattr(self, rpc_fn_name)
        result = fn(*params)

        response = { 'result' : result, 'error' : None, 'id' : 1 }
        response = simplejson.dumps(response)
        return str(response)

    def rpc_hello(self):
        return 'world!'

    def rpc_add(self, a, b):
        return int(a) + int(b)

    def rpc_convert(self, amount):
        return "%s ml" % (drinkz.db.convert_to_ml(str(amount)))



def form():
    return """
<head>
<script type="text/javascript" charset="utf-8" src="http://code.jquery.com/jquery-1.7.2.min.js"></script>
</head>
Convert:  <input type='text' class='a' value='' size='4' />

<p class='toupdate' />

<script type="text/javascript">

function update_result(a, c) {
   text = '<font color="red"><b>' + a + ' equals ' + c + '</font></b>';
   $('p.toupdate').html(text);
}

function do_add() {
 a = $('input.a').val();

 
 $.ajax({
     url: '/rpc',
     data: JSON.stringify ({method:'convert', params:[a], id:"0"} ),
     type: "POST",
     dataType: "json",
     success: function (data) { update_result(a,data.result) },
     error: function (err) { alert ("Error");}
  });
}

$('input.a').change(do_add);
</script>
"""


def form_add_type():
    return """
<form action='recv_type'>
Manufacturer: <input type='text' name='mfg' size'20'>
Liquor: <input type='text' name='liquor' size'20'>
Type: <input type='text' name='type' size'20'>
<input type='submit'>
</form>
"""

def form_vote(name):
    return """

<form action='recv_vote'>
<input type="radio" name="voteScore" value="1">1
<input type="radio" name="voteScore" value="2">2
<input type="radio" name="voteScore" value="3">3
<input type="radio" name="voteScore" value="4">4
<input type="radio" name="voteScore" value="5">5
<input type='submit' value = "Submit Vote" >
<input type='hidden' name='currentVote' value='"""+name+"""' />
</form>
"""



def form_add_inv():
    return """
<form action='recv_inv'>
Manufacturer: <input type='text' name='mfg' size'20'>
Liquor: <input type='text' name='liquor' size'20'>
Amount: <input type='text' name='amt' size'20'><br>
<input type="radio" name="measure" value="oz">oz<br>
<input type="radio" name="measure" value="liter">liter<br>
<input type="radio" name="measure" value="gallon">gallon<br>
<input type="radio" name="measure" value="ml">ml<br>
<input type='submit'>
</form>
"""

def form_add_recipe():
    return """
<form action='recv_recipe'>
Name: <input type='text' name='name' size'20'><p>
Ingredients: <input type='text' name='ingr' size'50'><p>
<input type='submit'>
<p><small><b>Correct Format for Ingredients is 'name1,#amt unit,name2,#amt unit,...'
</form>
"""

if __name__ == '__main__':
    import random, socket
    port = random.randint(8000, 9999)
    
    app = SimpleApp()
    
    httpd = make_server('', port, app)
    print "Serving on port %d..." % port
    print "Try using a Web browser to go to http://%s:%d/" % \
          (socket.getfqdn(), port)
    httpd.serve_forever()
