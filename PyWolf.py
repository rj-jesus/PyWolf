import cherrypy
import os
import sys
import urllib
import urllib2
import xml.etree.ElementTree as eT
from xml.sax.saxutils import unescape
reload(sys)
sys.setdefaultencoding('UTF8')


class PyWolf(object):
    def __init__(self):
        self.AppId = '' # Please define your own API Id. You can get one for free at Wolfram|Alpha.
        self.PodState = '*Step-by-step solution'
        self.Start = self.hunescape('&lt;!DOCTYPE html&gt;&lt;html lang=&quot;en&quot;&gt;&lt;head&gt; &lt;meta charset=&quot;utf-8&quot;&gt; &lt;meta http-equiv=&quot;X-UA-Compatible&quot; content=&quot;IE=edge&quot;&gt; &lt;meta name=&quot;viewport&quot; content=&quot;width=device-width, initial-scale=1&quot;&gt; &lt;meta name=&quot;description&quot; content=&quot;&quot;&gt; &lt;meta name=&quot;author&quot; content=&quot;&quot;&gt; &lt;title&gt;PyWolf - A Python Wolfram|Alpha Query Service&lt;/title&gt; &lt;link href=&quot;/static/img/favicon.ico&quot; rel=&quot;shortcut icon&quot; type=&quot;image/x-icon&quot; /&gt;&lt;/head&gt;&lt;body style=&quot;text-align: center;&quot;&gt;')
        self.End = self.hunescape('&lt;/body&gt;&lt;/html&gt;')

    @cherrypy.expose
    def index(self):
        return open('public_html/index.html', 'rb')
    
    @cherrypy.expose
    def query(self, input=None):
        xml = self.getXML(input)
        return self.Start + self.writeHTML(xml)

    def getXML(self, input):
        BaseURL = 'http://api.wolframalpha.com/v2/query?'
        URLParams = {'input': input, 'appid': self.AppId, 'podstate': self.PodState}
        Params = urllib.urlencode(URLParams)
        Headers = {'User-Agent': None}
        req = urllib2.Request(BaseURL, Params, Headers)
        return urllib2.urlopen(req).read()

    def writeHTML(self, xml):
        html = ''
        tree = eT.fromstring(xml)
        for pod in tree.iter('pod'):
            html += '<h2>' + pod.get('title') + '</h2>\n'
            for img in pod.iter('img'):
                html += '<img src=\"' + img.get('src') + '\" ' + 'alt=\"' + img.get('alt') + '\" />' + '\n'
        return html
    
    def hunescape(self, text):
        table = {
            "&quot;": '"',
            "&apos;": "'"
        }
        return unescape(text, table)


if __name__ == '__main__':
    conf = {
        'global': {
            'server.socket_host': '0.0.0.0',
            'server.socket_port': 8080
        },
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public_html'
        }
    }
    cherrypy.quickstart(PyWolf(), "/", conf)
