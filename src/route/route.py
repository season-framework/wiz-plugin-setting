import datetime

menus = []
menus.append({"url": "/wiz/admin/setting/status", "icon": "fas fa-heartbeat", "title": "System Status", 'pattern': r'^/wiz/admin/setting/status'})
menus.append({"url": "/wiz/admin/setting/configuration", "icon": "fas fa-cog", "title": "Configuration", 'pattern': r'^/wiz/admin/setting/configuration'})
menus.append({"url": "/wiz/admin/setting/plugin/list", "icon": "fas fa-plug", "title": "Plugin", 'pattern': r'^/wiz/admin/setting/plugin/list'})
menus.append({"url": "/wiz/admin/setting/acl", "icon": "fas fa-shield-alt", "title": "Access control", 'pattern': r'^/wiz/admin/setting/acl'})
menus.append({"url": "/wiz/admin/setting/onerror", "icon": "fas fa-exclamation-triangle", "title": "On error", 'pattern': r'^/wiz/admin/setting/onerror'})
menus.append({"url": "/wiz/admin/setting/onboot", "icon": "fas fa-power-off", "title": "On boot", 'pattern': r'^/wiz/admin/setting/onboot'})
menus.append({"url": "/wiz/admin/setting/build_resource", "icon": "fas fa-filter", "title": "Build resource", 'pattern': r'^/wiz/admin/setting/build_resource'})
menus.append({"url": "/wiz/admin/setting/after_request", "icon": "fas fa-filter", "title": "After Request", 'pattern': r'^/wiz/admin/setting/after_request'})

def setting_nav(menus):
    def itermenu(menu):
        pt = None
        if 'pattern' in menu: pt = menu['pattern']
        elif 'url' in menu: pt = menu['url']
        if pt is not None:
            if framework.request.match(pt): menu['class'] = 'active'
            else: menu['class'] = ''
        
    for menu in menus:
        itermenu(menu)
    return menus

menus = setting_nav(menus)

framework.layout('core.theme.layout', navbar=True, monaco=True)
framework.render("status", "core.setting.status", settingmenus=menus)
framework.render("configuration", "core.setting.configuration", settingmenus=menus)
framework.render("plugin/list", "core.setting.plugin.list", settingmenus=menus)
framework.render("acl", "core.setting.acl", settingmenus=menus)
framework.render("onerror", "core.setting.onerror", settingmenus=menus)
framework.render("onboot", "core.setting.onboot", settingmenus=menus)
framework.render("build_resource", "core.setting.build_resource", settingmenus=menus)
framework.render("after_request", "core.setting.after_request", settingmenus=menus)

framework.layout('core.theme.layout', navbar=False, monaco=True)
framework.render("plugin/editor/<plugin_id>", "core.setting.plugin.editor")
framework.render("plugin/browser/<plugin_id>/<target>", "core.setting.plugin.browser")

segment = framework.match("plugin/preview/<plugin_id>/<bundle_id>")
if segment is not None:
    plugin_id = segment.plugin_id
    bundle_id = segment.bundle_id
    framework.request.segment = season.stdClass()
    plugin = framework.model("plugin").instance(plugin_id)
    plugin.layout('core.theme.layout', navbar=False, monaco=True)
    plugin.render(bundle_id, settingmenus=menus)


segment = framework.match("api/config/clean")
if segment is not None:
    fs = framework.model("wizfs").use("wiz")
    fs.delete("public/templates")
    fs.delete("cache")
    fs.write("config/.cache", datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    framework.response.status(200, True)

framework.response.redirect("status")