"""
Startup example for senchar.

Usage examples:
  ipython --ipython-dir=/data/ipython --profile senchar -i -m senchar.startup_example
  python -i -m senchar.startup_example

With the -m option on python, the local variables here are imported into the CLI namespace.
"""

import os

import senchar
from senchar.tools import *
from senchar.parameters import Parameters
from senchar.web.fastapi_server import WebServer
from senchar import db

# default values (useful)
db.datafolder = "/data"
db.datafolder = "/data/DESI"
db.imageroi = [[500, 700, 500, 700], [2050, 2060, 500, 700]]

# parameters (useful)
params = Parameters()
parfile = os.path.join(db.datafolder, "parameters", "senchar.ini")
params.read_parfile(parfile)
params.update_pars()
del parfile
del Parameters

# web server (optional)
if 0:
    db.webserver = WebServer()
    db.webserver.start()
    del WebServer


# shortcuts (optional)
def sav():
    params.update_par_dict()
    params.save_pars()
    return
