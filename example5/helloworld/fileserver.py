from __future__ import with_statement

import os

from webob.exc import HTTPForbidden

from webob import Request
from webob import Response

ext_to_mimetype = {
    '.txt': 'text/plain',
    '.html': 'text/html',
    '.pdf': 'application/pdf',
    '.jpeg': 'image/jpeg',
    '.jpg': 'image/jpeg',
}

# Number of bytes to send in each block
BLOCK_SIZE = 4096

class FileServer(object):
    """ Checks request to see if it corresponds to a static file in a 
    directory.  If file is found serves it, otherwise passes request on to
    dynamic application.

    """
    
    def __init__(self, application, global_conf, path):
        """ path is directory where static files are stored
        """
        self.path = path
        self.application = application
        assert application
        
    def __call__(self, environ, start_response):
        """ WSGI entry point
        """
        request = Request(environ)
        response = self._service(request)
        return response(environ, start_response)
    
    def _service(self, request):
        assert isinstance(request, Request)
        
        # Find path to file to server
        path_info = request.path_info
        if not path_info:
            return request.get_response(self.application)
        
        file_path = os.path.join(self.path, path_info[1:])

        # If file not found, delegate to dynamic application
        if not os.path.isfile(file_path):
            return request.get_response(self.application)
        
        # Guess mimetype of file based on file extension
        root, ext = os.path.splitext(path_info.lower())
        mimetype = ext_to_mimetype.get(ext, None)
        
        # If we can't guess mimetype, return a 403 Forbidden
        if mimetype is None:
            return HTTPForbidden()
        
        # Get size of file
        size = os.path.getsize(file_path)
        
        # Create headers and response
        headers = [
            ("Content-type", mimetype),
            ("Content-length", str(size)),
        ]
        
        # Send file
        return Response(
            headerlist=headers,
            app_iter=self._send_file(file_path, size),
        )
    
    def _send_file(self, file_path, size):
        """ A generator function which returns the blocks in a file, one at
        a time.
        
        """
        with open(file_path) as f:
            block = f.read(BLOCK_SIZE)
            while block:
                yield block
                block = f.read(BLOCK_SIZE)
                

