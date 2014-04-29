import sublime
import sublime_plugin
from urllib import request,parse
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
            print(apiRes)
            if apiRes:
                if 'out' in apiRes:
                    print("---------------------------------")
                    for r in apiRes['out']:
                        print(r)

        #sublime.set_timeout(self.callback, 1) ovc


def apiGet(api, **kwargs):
    if kwargs:
        data = parse.urlencode(kwargs)
        binary_data = data.encode("utf-8")
        #req = request.Request("http://192.168.2.2/api/%s/" % (api),binary_data)
        result = request.urlopen("http://192.168.2.2/api/%s/" % (api),binary_data)
    else:
        #req = request.Request("http://192.168.2.2/api/%s/" % (api),None)
        result = request.urlopen("http://192.168.2.2/api/%s/")
    try:
        return json.loads(result.readall().decode('utf-8'))
    except Exception as e:
        print(e)
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
