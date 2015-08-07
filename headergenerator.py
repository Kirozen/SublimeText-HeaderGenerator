""" headergenerator.py """

__author__ = "Etienne Faisant"
__date__ = "2013-07-16"
__version__ = "2.1"

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
        self.edit = edit
        self.window = sublime.active_window()
        self.view.sel().clear()
        self.point = self.view.text_point(0, 0)
        self.region = sublime.Region(self.point)
        self.view.sel().add(self.region)
        self.view.show(self.point)
        filename = self.view.file_name()
        if filename:
            extension = os.path.splitext(filename)[1]
            if extension:
                if extension in C_CPP_EXT:
                    self.c_cpp_generate(os.path.basename(filename))
                elif extension in PY_EXT:
                    self.py_generate(os.path.basename(filename))
                elif extension in JAVA_EXT:
                    self.java_generate(os.path.basename(filename))
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
        self.allow_rev = settings.get("allow_rev")

    def py_generate(self, filename):
        index = self.py_detect(filename)
        if index < 0:
            self.py_first_time(filename)
            sublime.status_message("Python header generated")
        else:
            if self.allow_rev:
                self.py_write_rev(filename, index)
                sublime.status_message("Python header revision generated")

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
        self.view.insert(self.edit, self.point, retstr)

    def py_write_rev(self, filename, line):
        def with_comment(comment, filename=filename, line=line):
            retstr = "##########\n"
            retstr += "# " + self.date + "\n"
            retstr += "#\n"
            if comment:
                retstr += "# " + comment + "\n"
                retstr += "#\n"
            self.view.run_command("goto_line", {"line": line})
            self.view.run_command("insert", {"characters": retstr})

        self.window.show_input_panel("Comment:", "", with_comment, None, None)

    def c_cpp_generate(self, filename):
        index = self.c_cpp_detect(filename)
        if index < 0:
            self.c_cpp_first_time(filename)
            sublime.status_message("C/C++ header generated")
        else:
            if self.allow_rev:
                self.c_cpp_write_rev(filename, index)
                sublime.status_message("C/C++ header revision generated")

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
        self.view.insert(self.edit, self.point, retstr)

    def c_cpp_write_rev(self, filename, line):
        def with_comment(comment, filename=filename, line=line):
            retstr = "/*********\n"
            retstr += " * " + self.date + "\n*\n"
            if comment:
                retstr += "* " + comment + "\n"
                retstr += "*\n"
            retstr += "*/\n"
            self.view.run_command("goto_line", {"line": line})
            self.view.run_command("insert", {"characters": retstr})

        self.window.show_input_panel("Comment:", "", with_comment, None, None)

    def java_generate(self, filename):
        index = self.java_detect(filename)
        if index < 0:
            self.java_first_time(filename)
            sublime.status_message("Java header generated")
        else:
            if self.allow_rev:
                self.java_write_rev(filename, index)
                sublime.status_message("Java header revision generated")

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
        retstr += " */\n"
        self.view.insert(self.edit, self.point, retstr)

    def java_write_rev(self, filename, line):
        def with_comment(comment, filename=filename, line=line):
            retstr = "/*********\n"
            retstr += " * " + self.date + "\n"
            retstr += "*\n"
            if comment:
                retstr += "* " + comment + "\n"
                retstr += "*\n"
            retstr += "*/\n"
            self.view.run_command("goto_line", {"line": line})
            self.view.run_command("insert", {"characters": retstr})

        self.window.show_input_panel("Comment:", "", with_comment, None, None)

    def py_detect(self, filename):
        region = sublime.Region(0, self.view.size())
        lines = self.view.substr(region).split('\n')
        header = "\"\"\" %s \"\"\"" % filename

        index = 0
        while lines[index] and lines[index].isspace():
            index += 1

        if index >= len(lines):
            return -1

        if lines[index] == header or lines[index].startswith('__author__') or lines[index].startswith('date'):
            while index < len(lines):
                if lines[index].startswith('import'):
                    break
                index += 1

            index -= 1
            while index >= 0:
                if lines[index] and not lines[index].isspace():
                    index += 1
                    break
                index -= 1
        else:
            return -1
        return index + 1

    def c_cpp_detect(self, filename):
        region = sublime.Region(0, self.view.size())
        lines = self.view.substr(region).split('\n')
        index = 0
        while lines[index] and not lines[index].startswith("#include"):
            if lines[index].startswith(" */"):
                return index + 2
            index += 1

        return -1

    def java_detect(self, filename):
        return -1
