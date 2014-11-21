import json
import sys
from kazoo.exceptions import NoNodeError

from flask import Flask, render_template
import os
import kazoo.client

app = Flask(__name__)

class KazooWrapper(object):

    def __init__(self, hosts):
        self.hosts = hosts

    def __enter__(self):
        self.zk = kazoo.client.KazooClient(hosts=self.hosts)
        self.zk.start(timeout=5)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.zk.stop()


@app.route('/')
@app.route('/<path:path>')
def root(path=''):
    znodename = '/' + path
    with KazooWrapper(app.config['zookeeper_hosts']) as kw:
        try:
            data = kw.zk.get(znodename)
            children = kw.zk.get_children(znodename)

            return render_template('index.html',
                                   hosts=app.config['zookeeper_hosts'],
                                   path=znodename,
                                   content=data[0].__repr__(),  # avoids encoding issues.
                                   children=[dict(href=(znodename + '/' if znodename != '/' else znodename) + child,
                                                  label='/' + child) for child in children]
            )
        except NoNodeError:
            return render_template('index.html', path='No such node: ' + znodename)


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print "Required parameter:  zookeeper host(s)"
    else:
        app.config['zookeeper_hosts'] = sys.argv[1]
        app.run(port=3005, debug=True)
