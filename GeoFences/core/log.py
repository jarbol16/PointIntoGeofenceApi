import logging
import json
import sys
import os

def init__():
    __path = os.getcwd()
    r = ""
    try:
        r = sys.argv[1]
    except:
        pass
    if len(r) > 0:
        __path = r

   # file = open("{0}/setting.json".format(__path),"r")
   # data = json.load(file)
    #logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', filename=sys.argv[3], level=logging.DEBUG)


def log_info(txt):
    print("INFO", txt)
    #init__()
    #logging.info(txt)

def log_debug(txt):
    print("DEBUG", txt)
   # init__()
    #logging.debug(txt)

def log_error(obj):
    print("ERROR", obj)
    #init__()
    #logging.error(obj)
