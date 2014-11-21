### zoospider

A simple python server for viewing zookeeper data.

Usage:

    python zoospider.py <zookeeper host:port pairs>

Example, if your have a zookeeper running on 10.141.141.10:2181:

    python zoospider.py 10.141.141.10:2181

Visit  http://localhost:3005/ to explore the znodes.



Requires flask, kazoo.

    pip install flask, kazoo
    
Uses the html5 mobile boilerplate. http://html5boilerplate.com/mobile/
