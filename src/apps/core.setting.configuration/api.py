import season
import json
import datetime
from werkzeug.exceptions import HTTPException

def packageinfo(framework):
    package = framework.model("config").get()        
    framework.response.status(200, package)

def update(framework):
    data = framework.request.query("data", True)
    fs = framework.model("wizfs").use("wiz")
    fs.write("wiz.json", data)
    framework.response.status(200, True)

def apply(framework):
    config = framework.model("config")

    # create config code
    configpy = config.build_config()
    wizconfigpy = config.build_wiz()

    # save config files
    fs = framework.model("wizfs").use("wiz")
    fs.write("config/config.py", configpy)
    fs.write("config/wiz.py", wizconfigpy)
    
    framework.response.status(200, True)

def clean(framework):
    fs = framework.model("wizfs").use("wiz")
    fs.delete("public/templates")
    fs.delete("cache")
    fs.write("config/.cache", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    framework.response.status(200, True)