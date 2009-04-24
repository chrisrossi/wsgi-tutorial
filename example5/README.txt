# To run this example:

virtualenv --no-site-packages venv

venv/bin/python setup.py develop

venv/bin/paster serve helloworld.ini

Hit this url with your browser:

http://localhost:8080/

For extra kicks, play with the "path" and "favorite_color" configuration
parameters in helloworld.ini, rerun paster serve, and see how that affects
the application.
