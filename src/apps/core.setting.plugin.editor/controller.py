model = framework.model("plugin")

plugin_id = framework.request.segment.plugin_id

if plugin_id is None:
    framework.response.redirect("plugin/list")

plugin = model.get(plugin_id)

if plugin is None:
    framework.response.redirect("plugin/list")

kwargs["PLUGIN_ID"] = plugin_id
