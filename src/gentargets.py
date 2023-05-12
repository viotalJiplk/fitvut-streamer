#!/usr/bin/python

import pathlib
import json
import os
from sys import argv

config={}

configFile = str(pathlib.Path(__file__).parent.resolve())+ "/config.json"

print("Setting targets up")

if os.path.exists(configFile):
    f = open(configFile)
    config = json.loads(f.read())
    f.close()
    os.remove(configFile)
else:    
    config["path"] = "/video/www/"
config["targets"] = argv[1:]
#config["targets"][0] = config["targets"][0][1:]
#config["targets"][-1] = config["targets"][-1][:-1]

f = open(configFile, 'w+')
json.dump(config, f)
f.close()