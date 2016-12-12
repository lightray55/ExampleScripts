from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir
from os.path import join as pjoin
import json
import subprocess

PORT_NUMBER = 8585

#This class will handles any incoming request from
#the browser
class myHandler(BaseHTTPRequestHandler):
        store_path = pjoin(curdir, 'store.json')

        #Handler for the GET requests
        def do_GET(self):
                self.send_response(200)
                self.send_header('Content-type','text/html')
                self.end_headers()
                # Send the html message
                self.wfile.write("Hello World !")
                return

        def parse_POST(self):
                ctype, pdict = parse_header(self.headers['content-type'])
                if ctype == 'multipart/form-data':
                    postvars = parse_multipart(self.rfile, pdict)
                elif ctype == 'application/x-www-form-urlencoded':
                    length = int(self.headers['content-length'])
                    postvars = parse_qs(
                            self.rfile.read(length),
                            keep_blank_values=1)
                else:
                    postvars = {}
                return postvars

        def do_POST(self):
                #postvars = self.parse_POST()
                if self.path == '/store.json':
                        length = self.headers['content-length']
                        data = self.rfile.read(int(length))

                        with open(self.store_path, 'w') as fh:
                                fh.write(data.decode())

                        data = json.loads(data.decode())
                        if data["repository"]["name"] == "EASWebsite":
                                print data["zen"]
                                subprocess.call([pjoin(curdir, 'testStuff.sh')])
                                #self.send_header('Returning-Hook-ID', data["hook_id"])
                self.send_response(200)
try:
        #Create a web server and define the handler to manage the
        #incoming request
        server = HTTPServer(('', PORT_NUMBER), myHandler)
        print 'Started httpserver on port ' , PORT_NUMBER

        #Wait forever for incoming http requests
        server.serve_forever()

except KeyboardInterrupt:
        print '^C received, shutting down the web server'
        server.socket.close()
