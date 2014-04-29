import sublime
import sublime_plugin
import urllib
import simplejson


def apiGet(api, **kwargs):
    request = urllib.request.Request("http://192.168.2.52/api/%s/" % (api))

    if kwargs:
            request.add_data(urllib.urlencode(kwargs))
    result = urllib.request.urlopen(request, timeout=120)
    try:
        return simplejson.load(result)
    except:
        return None


class MecomWorkSendToBotCommand(sublime_plugin.TextCommand):

    def run(self, edit):
		#sublime.log_commands(True)
    	sublime.active_window().run_command("show_panel", {"panel": "console", "toggle": True})

        for selection in self.view.sel():
            # if the user didn't select anything, search the currently highlighted word
            if selection.empty():
                text = self.view.word(selection)

            text = self.view.substr(selection)
            for chunk in text.splitlines():
                apiRes = apiGet('bot', cmd=chunk.strip())
                if apiRes:
                    if 'out' in apiRes:
                        print("---------------------------------")
                        for r in apiRes['out']:
                        	print(r)
