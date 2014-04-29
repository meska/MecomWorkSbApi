import sublime
import sublime_plugin
import urllib
from urllib import request
from urllib import parse
import json
import threading


class ApiThread(threading.Thread):
    def __init__(self, cmd,text, edit):
        threading.Thread.__init__(self)
        self.cmd = cmd
        self.text = text
        self.edit = edit

    def run(self):
        for chunk in self.text.splitlines():
            apiRes = apiGet('bot', cmd=chunk.strip())
            if apiRes:
                if 'out' in apiRes:
                    print("---------------------------------")
                    for r in apiRes['out']:
                        print(r)

        #sublime.set_timeout(self.callback, 1)


def apiGet(api, **kwargs):
    req = request.Request("http://192.168.2.2/api/%s/" % (api))

    if kwargs:
            req.add_data(parse.urlencode(kwargs))
    result = urllib.request.urlopen(req, timeout=120)
    try:
        return json.load(result)
    except:
        return None


class MecomWorkSendToBotThreadedCommand(sublime_plugin.TextCommand):

    def run(self, edit):
        sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

        for selection in self.view.sel():
            # if the user didn't select anything, search the currently highlighted word
            if selection.empty():
                text = self.view.word(selection)

            text = self.view.substr(selection)
            print("invio comandi al bot...")
            apiT = ApiThread(self, text, edit)
            apiT.start()
