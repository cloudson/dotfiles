#!/usr/bin/python

import sys
import cli.app 
import json
import shutil 
import os 
import subprocess

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

def install(json, package):
    install_cmd = json["install-cmd"] 
    packages = json["packages"]

    if not package in packages:
        raise ValueError("%s isn't declared in json file" % (package)) 

    full_cmd = install_cmd % (package) 
    print "Running `%s`" % (full_cmd)   
    full_cmd_splited = full_cmd.split(' '); 
    p = subprocess.Popen(full_cmd_splited, stdout=sys.stdout, 
            stderr=subprocess.PIPE, 
            stdin=sys.stdin)
    out, err = p.communicate()
    if err:
        raise ValueError(err) 
    print out 


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
    
    if app.params.install is not None: 
        try:
            install(json, app.params.install)
        except KeyError, e: 
            print "Config ", e, " not found" 
            return 
        return 
    
    if app.params.install_all is not None: 
        try:
            for package in json["packages"]:
                install(json, package)
        except KeyError, e: 
            print "Config ", e, " not found" 
            return 
        return 


dotfiles.add_param("-f", "--file", help="Json file that describes your configuration", default="dotfiles.json")
dotfiles.add_param("-i", "--install", help="Install a package declared on json file", default=None)
dotfiles.add_param("-c", "--configure", help="Move a configuration file locates on templates folder", default=None)
dotfiles.add_param("-ia", "--install-all", help="Install all dependencies", default=False)



if __name__ == '__main__': 
    dotfiles.run() 
