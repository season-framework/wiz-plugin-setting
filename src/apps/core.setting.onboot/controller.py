import sys

wiz = framework.model("wiz")
try: kwargs["SEASON_VERSION"] = season.version
except: kwargs["SEASON_VERSION"] = "<= 0.3.8"
kwargs["PYTHON_VERSION"] = sys.version
kwargs["themes"] = wiz.themes()
kwargs['IS_DEV'] = wiz.is_dev()
kwargs['BRANCH'] = wiz.workspace.branch()
kwargs['BRANCHES'] = wiz.workspace.branches()
