plugin = framework.model("plugin")

def info(framework):
    plugin_id = framework.request.segment.get(0, True)
    info = plugin.get(plugin_id)
    if info is None:
        framework.response.status(404)
    framework.response.status(200, info)
    
def update(framework):
    plugin_id = framework.request.segment.get(0, True)
    info = framework.request.query("info", True)
    apps = framework.request.query("apps", True)
    route = framework.request.query("route", True)

    status = plugin.update(plugin_id, info, apps, route)

    if status:
        framework.response.status(200)
    framework.response.status(500)

def delete(framework):
    plugin_id = framework.request.segment.get(0, True)
    plugin.delete(plugin_id)
    framework.response.status(200)
