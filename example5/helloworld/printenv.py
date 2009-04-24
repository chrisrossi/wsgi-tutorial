from webob import Request
from webob import Response

def wsgi_app(a):
    def wrapper(environ, start_response):
        request = Request(environ)
        response = a(request)
        return response(environ, start_response)
    return wrapper

def dict_to_string(d):
    keys = d.keys()
    keys.sort()
    return "\n".join(["%s=%s" % (key, d[key]) for key in keys])

def factory(global_config, favorite_color):
    @wsgi_app
    def app(request):
        body = html % (favorite_color,
                       dict_to_string(request.params), 
                       dict_to_string(request.environ))
        
        return Response(body=body, 
                        headerlist=[
                            ("Content-type", "text/html"),
                            ("Content-length", str(len(body))),
                        ])
    return app

html = """
<html>
  <head>
    <title>Hello World!</title>
  </head>
  <body>
    <img src="helloworld.jpg" align="right"/>
    <p>
      I see that your favorite color is <i>%s</i>.
    </p>
    <p>
      <b>Hey, here are some parameters!</b>
      <pre>%s</pre>
    </p>
    <p>
      <b>Check out my dynamic environment!</b>
      <pre>%s</pre>
    </p>
  </body>
</html>
"""