""" headergenerator.py """

__author__ = "Etienne Faisant"
__date__ = "2013-07-16"
__version__ = "2.0"

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
                    header_str = self.c_cpp_generate(os.path.basename(filename))
                elif extension in PY_EXT:
                    header_str = self.py_generate(os.path.basename(filename))
                elif extension in JAVA_EXT:
                    header_str = self.java_generate(os.path.basename(filename))
                else:
                    sublime.status_message("Extension not supported")
            else:
                sublime.status_message("Extension not found")
        else:
            sublime.status_message("Filename does not exist")
        if header_str:
            self.view.insert(edit, pt, header_str)

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
        self.allow_rev = settings.get("allow_rev")

    def set_comment(self, text):
        self.comment = text

    def py_generate(self, filename):
        if not self.py_detect(filename):
            ret = self.py_first_time(filename)
            sublime.status_message("Python header generated")
        else:
            if self.allow_rev:
                ret = self.py_write_rev(filename)
                sublime.status_message("Python header revision generated")
        return ret

    def py_first_time(self, filename):
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

    def py_write_rev(self, filename):
        self.comment = ""
        self.window.show_input_panel("Comment:", "", self.set_comment, None, None)
        retstr = "##########\n"
        retstr += "# " + self.date + "\n"
        retstr += "#\n"
        if self.comment:
            retstr += "# " + self.comment + "\n"
            retstr += "#\n"
        retstr += "\n"
        return retstr

    def c_cpp_generate(self, filename):
        if not self.c_cpp_detect(filename):
            ret = self.c_cpp_first_time(filename)
            sublime.status_message("C/C++ header generated")
        else:
            if self.allow_rev:
                ret = self.c_cpp_write_rev(filename)
                sublime.status_message("C/C++ header revision generated")
        return ret

    def c_cpp_first_time(self, filename):
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

    def c_cpp_write_rev(self, filename):
        self.comment = ""
        self.window.show_input_panel("Comment:", "", self.set_comment, None, None)
        retstr = "/*********\n"
        retstr += " * " + self.date + "\n"
        retstr += " *\n"
        if self.comment:
            retstr += " * " + self.comment + "\n"
            retstr += " *\n"
        retstr += " */\n"
        retstr += "\n"
        return retstr

    def java_generate(self, filename):
        if not self.java_detect(filename):
            ret = self.java_first_time(filename)
            sublime.status_message("Java header generated")
        else:
            if self.allow_rev:
                ret = self.java_write_rev(filename)
                sublime.status_message("Java header revision generated")
        return ret

    def java_first_time(self, filename):
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

    def java_write_rev(self, filename):
        self.comment = ""
        self.window.show_input_panel("Comment:", "", self.set_comment, None, None)
        retstr = "/*********\n"
        retstr += " * " + self.date + "\n"
        retstr += " *\n"
        if self.comment:
            retstr += " * " + self.comment + "\n"
            retstr += " *\n"
        retstr += " */\n"
        retstr += "\n"
        return retstr

    def py_detect(self, filename):
        return False

    def c_cpp_detect(self, filename):
        return False

    def java_detect(self, filename):
        return False
