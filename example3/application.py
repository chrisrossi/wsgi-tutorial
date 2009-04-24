from helloworld import application as helloworld
from fileserver import FileServer

def factory(static_path):
    return FileServer(helloworld, static_path)

def test_server():
    from wsgiref.simple_server import make_server
    application = factory("/home/chris/proj/wsgi-tutorial/static-files")
    server = make_server('localhost', 8080, application)
    server.serve_forever()
    
if __name__ == '__main__':
    test_server()
    