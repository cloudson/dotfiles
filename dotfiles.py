#!/usr/bin/python

import sys
import cli.app 
import json
import shutil 
import os 

def parseJsonFile(filename): 
    fp = open(filename, 'r');
    json_raw = fp.read()
    
    return json.loads(json_raw)

def moveConfiguration(json, config_name):
    config_names = json["templates"]
    path = os.path.expanduser(config_names[config_name])  
    position = path.rfind('/') + 1
    if position == -1:
        position = 0
    template_file_name = path[position:]

    if os.path.isdir(path): 
        raise Error(path, "is a directory and should be a file")

    config = "./templates/" + template_file_name  

    print "copying", config, "to", path
    shutil.copy(config, path)

@cli.app.CommandLineApp
def dotfiles(app):
    try:
        json = parseJsonFile(app.params.file)
    except ValueError, e: 
        print e
        return 
 
    if app.params.configure is not None: 
        try:
            moveConfiguration(json, app.params.configure)
        except KeyError, e:
            print "Config ", e, " not found" 
            return 
        return 

dotfiles.add_param("-f", "--file", help="Json file that describes your configuration", default="dotfiles.json")
dotfiles.add_param("-c", "--configure", help="Move a configuration file locates on templates folder", default=None)

if __name__ == '__main__': 
    dotfiles.run() 
