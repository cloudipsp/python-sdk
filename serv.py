from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import cgi
import urllib.parse


class S(BaseHTTPRequestHandler):
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        return

    def do_POST(self):
        content_type, pdict = cgi.parse_header(self.headers['content-type'])
        if content_type == 'multipart/form-data':
            postvars = cgi.parse_multipart(self.rfile, pdict)
        elif content_type == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            postvars = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            postvars = {}
        if len(postvars):
            i = 0
            for key in sorted(postvars):
                logging.debug('ARG[%d] %s=%s' % (i, key, postvars[key]))
                i += 1
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        str = ''
        str += '<html>'
        str += '  <head>'
        str += '    <title>Server POST Response</title>'
        str += '  </head>'
        str += '  <body>'
        str += '    <p>POST variables (%d).</p>' % (len(postvars))
        if len(postvars):
            str += '    <table>'
            str += '      <tbody>'
            i = 0
            for key in sorted(postvars):
                i += 1
                val = postvars[key]
                str += '        <tr>'
                str += '          <td align="right">%d</td>' % (i)
                str += '          <td align="right">%s</td>' % key
                str += '          <td align="left">%s</td>' % val
                str += '        </tr>'
            str += '      </tbody>'
            str += '    </table>'
        str += '  </body>'
        str += '</html>'
        self.wfile.write(str.format(self.path).encode('utf-8'))


def run(server_class=HTTPServer, handler_class=S, port=8080):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info('Starting httpd...\n')
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Stopping httpd...\n')


if __name__ == '__main__':
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
