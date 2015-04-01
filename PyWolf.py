import cherrypy
import os
import sys
import urllib
import urllib2
import xml.etree.ElementTree as eT
reload(sys)
sys.setdefaultencoding('UTF8')


class PyWolf(object):
    def __init__(self):
        self.AppId = 'H2YK4X-A73JKEPU6P'
        self.PodState = '*Step-by-step solution'
        self.Start = open('WolfBegin.txt', 'rb').read()
        self.End = open('WolfEnd.txt', 'rb').read()

    @cherrypy.expose
    def index(self):
        return open('public_html/index.html', 'rb')
    
    @cherrypy.expose
    def query(self, input=None):
        f = open('public_html/WolfOut.html', 'wb')
        f.write(self.Start)
        xml = self.getXML(input)
        self.writeHTML(xml, f)
        f.write(self.End)
        f.close()
        return open('public_html/WolfOut.html', 'rb')

    def getXML(self, input):
        BaseURL = 'http://api.wolframalpha.com/v2/query?'
        URLParams = {'input': input, 'appid': self.AppId, 'podstate': self.PodState}
        Params = urllib.urlencode(URLParams)
        Headers = {'User-Agent': None}
        req = urllib2.Request(BaseURL, Params, Headers)
        return urllib2.urlopen(req).read()

    def writeHTML(self, xml, f):
        tree = eT.fromstring(xml)
        for pod in tree.iter('pod'):
            f.write('<h2>' + pod.get('title') + '</h2>\n')
            for img in pod.iter('img'):
                f.write('<img src=\"' + img.get('src') + '\" ' + 'alt=\"' + img.get('alt') + '\" />' + '\n')
                f.write('<br>\n')


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
