""" headergenerator.py """

__author__ = "Etienne Faisant"
__date__ = "2013-07-16"
__version__ = "1.3"

import sublime
import sublime_plugin
from datetime import datetime
import os

C_CPP_EXT = [".c", ".cc", ".cpp", ".cxx", ".c++", ".h", ".hpp", ".hxx", ".h++", ".inl", ".ipp", ".inc"]
PY_EXT = [".py", ".py3", ".pyw"]
JAVA_EXT = [".java"]


class GenerateHeaderCommand(sublime_plugin.TextCommand):

    """Generate an header"""

    def run(self, edit):
        self.load_settings()
        self.view.sel().clear()
        pt = self.view.text_point(0, 0)
        self.view.sel().add(sublime.Region(pt))
        self.view.show(pt)
        filename = self.view.file_name()
        if filename:
            extension = os.path.splitext(filename)[1]
            if extension:
                if extension in C_CPP_EXT:
                    self.view.insert(edit, pt, self.generate_c_cpp(os.path.basename(filename)))
                    sublime.status_message("C/C++ header generated")
                elif extension in PY_EXT:
                    self.view.insert(edit, pt, self.generate_python(os.path.basename(filename)))
                    sublime.status_message("Python header generated")
                elif extension in JAVA_EXT:
                    self.view.insert(edit, pt, self.generate_java(os.path.basename(filename)))
                    sublime.status_message("Java header generated")
                else:
                    sublime.status_message("Extension not supported")
            else:
                sublime.status_message("Extension not found")
        else:
            sublime.status_message("Filename does not exist")

    def load_settings(self):
        settings_name = 'HeaderGenerator'
        settings = sublime.load_settings(settings_name + '.sublime-settings')
        self.author = settings.get("author")
        dateformat = settings.get("date_format")
        if not dateformat:
            dateformat = "%Y-%m-%d"
        self.date = datetime.now().strftime(dateformat)
        self.email = settings.get("email")
        self.print_email = settings.get("print_email")
        self.print_date = settings.get("print_date")
        self.print_filename = settings.get("print_filename")

    def generate_python(self, filename):
        retstr = ""
        if self.print_filename:
            retstr += "\"\"\" " + filename + " \"\"\"" + "\n\n"
        retstr += "__author__ = " + "\"" + self.author + "\"" + "\n"
        if self.print_email:
            retstr += "__email__ = " + "\"" + self.email + "\"" + "\n"
        if self.print_date:
            retstr += "__date__ = " + "\"" + self.date + "\"" + "\n"
        retstr += "\n"
        return retstr

    def generate_c_cpp(self, filename):
        retstr = "/**\n"
        if self.print_filename:
            retstr += " * " + filename + "\n"
            retstr += " * " + "\n"
        retstr += " * " + "Author : " + self.author + "\n"
        if self.print_email:
            retstr += " * " + " Email : " + self.email + "\n"
        if self.print_date:
            retstr += " * " + "  Date : " + self.date + "\n"
        retstr += " */\n\n"
        return retstr

    def generate_java(self, filename):
        retstr = "/**\n"
        if self.print_filename:
            retstr += " * " + filename + "\n"
            retstr += " * " + "\n"
        retstr += " * " + "Author : " + self.author + "\n"
        if self.print_email:
            retstr += " * " + " Email : " + self.email + "\n"
        if self.print_date:
            retstr += " * " + "  Date : " + self.date + "\n"
        retstr += " */\n\n"
        return retstr
