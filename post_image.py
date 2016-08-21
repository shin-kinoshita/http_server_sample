from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
from PIL import Image

class PostHandler(BaseHTTPRequestHandler):
    
    image_dir_path = 'images'

    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(
            fp=self.rfile, 
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                     'CONTENT_TYPE':self.headers['Content-Type'],
                     })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        self.wfile.write('Client: %s\n' % str(self.client_address))
        self.wfile.write('User-agent: %s\n' % str(self.headers['user-agent']))
        self.wfile.write('Path: %s\n' % self.path)
        self.wfile.write('Form data:\n')

        # Echo back information about what was posted in the form
        for field in form.keys():
            if field == 'image':
                name = form[field].filename
                print str(form[field])
                img = self._get_image(form[field])
                img.save(image_dir_path + "/" + name)
        return

    def _get_image(self, image_item):

        raw_data = image_item.file.read()
        raw_len = len(raw_data)
        img = Image.frombytes('RGB', raw_len, raw_data)
        return img


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('localhost', 8080), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
    
