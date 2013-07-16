import sublime
import sublime_plugin
from datetime import datetime

class GenerateCommand(sublime_plugin.TextCommand):
    """Generate an header"""

    def run(self, edit):
        date = datetime.now().strftime("%Y-%m-%d")
        header = date + "\n"
        self.view.sel().clear()
        pt = self.view.text_point(0, 0)
        self.view.sel().add(sublime.Region(pt))
        self.view.show(pt)
        self.view.insert(edit, pt, header)
