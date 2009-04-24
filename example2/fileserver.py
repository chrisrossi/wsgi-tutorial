from __future__ import with_statement

import os

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
    """ Serves static files from a directory.
    """
    
    def __init__(self, path):
        """ path is directory where static files are stored
        """
        self.path = path
        
    def __call__(self, environ, start_response):
        """ WSGI entry point
        """
        # Find path to file to server
        path_info = environ["PATH_INFO"]
        if not path_info:
            return self._not_found(start_response)
        
        file_path = os.path.join(self.path, path_info[1:])

        # If file does not exist, return 404
        if not os.path.exists(file_path):
            return self._not_found(start_response)
        
        # Guess mimetype of file based on file extension
        root, ext = os.path.splitext(path_info.lower())
        mimetype = ext_to_mimetype.get(ext, None)
        
        # If we can't guess mimetype, return a 403 Forbidden
        if mimetype is None:
            return self._forbidden(start_response)
        
        # Get size of file
        size = os.path.getsize(file_path)
        
        # Create headers and start response
        headers = [
            ("Content-type", mimetype),
            ("Content-length", str(size)),
        ]
        
        start_response("200 OK", headers)
        
        # Send file
        return self._send_file(file_path, size)
        
    def _send_file(self, file_path, size):
        """ A generator function which returns the blocks in a file, one at
        a time.
        
        """
        with open(file_path) as f:
            block = f.read(BLOCK_SIZE)
            while block:
                yield block
                block = f.read(BLOCK_SIZE)
                
    def _not_found(self, start_response):
        start_response("404 NOT FOUND", [("Content-type", "text/plain")])
        return ["Not found",]

    def _forbidden(self, start_response):
        start_response("403 FORBIDDEN", [("Content-type", "text/plain")])
        return ["Forbidden",]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    application = FileServer("/home/chris/proj/wsgi-tutorial/static-files")
    server = make_server('localhost', 8080, application)
    server.serve_forever()
