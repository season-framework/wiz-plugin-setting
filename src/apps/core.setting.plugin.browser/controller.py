wiz = framework.model("wiz")

plugin_id = framework.request.segment.plugin_id
target = framework.request.segment.target

if plugin_id is None:
    framework.response.send("")
if target is None:
    framework.response.send("")

fs = framework.model("wizfs").use(f"wiz/plugin/{plugin_id}")
if fs.isdir(target) == False:
    fs.makedirs(target)

TARGET_PATH = fs.abspath()
kwargs["TARGET_PATH"] = f"wiz/plugin/{plugin_id}"
kwargs["TARGET"] = target
