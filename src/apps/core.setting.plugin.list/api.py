import json

plugin = framework.model("plugin")

def list(framework):
    rows = plugin.list()
    framework.response.status(200, rows)

def export(framework):
    plugin_id = framework.request.query("id", True)
    plugin_name = framework.request.query("name", True)
    app = plugin.get(plugin_id)
    app = json.dumps(app)
    framework.response.json({'code': 200, 'data': app})


def install(framework):
    plugin_id = framework.request.query("id", True)
    data = framework.request.query("data", True)
    data = json.loads(data)
    status = plugin.install(plugin_id, **data)
    framework.response.status(200)

def create(framework):
    plugin_id = framework.request.query("id", True)
    name = framework.request.query("name", True)
    status = plugin.create(plugin_id, name)
    framework.response.status(200)