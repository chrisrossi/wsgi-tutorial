def application(environ, start_response):
    env_names = environ.keys()
    env_names.sort()
    view_env = "\n".join(
        ["%s=%s" % (name, environ[name]) for name in env_names]
    )
    body = html % view_env
    start_response("200 OK", 
                   [("Content-type", "text/html"),
                    ("Content-length", str(len(body))),
                    ])
    
    return [body,]

html = """
<html>
  <head>
    <title>Hello World!</title>
  </head>
  <body>
    <img src="helloworld.jpg" align="right"/>
    <b>Check out my dynamic environment!</b>
    <pre>%s</pre>
  </body>
</html>
"""