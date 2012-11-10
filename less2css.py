# -*- coding: utf-8 -*-
import sublime, sublime_plugin
import os
import compiler

#message window
class MessageWindow:
  def __init__(self, message = ''):
    self.show(message)

  def show(self, message):
    if message == '':
      return

    settings = sublime.load_settings('less2css.sublime-settings')
    show_alert = settings.get("showErrorWithWindow", True)

    if show_alert == False:
      return

    sublime.error_message(message)


############################
##### SUBLIME COMMANDS #####
############################

#single less file
class LessToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    l2c = compiler.Compiler(self.view)
    resp = l2c.convertOne()
    MessageWindow(resp)

class AutoLessToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    print os.path.abspath('.')
    l2c = compiler.Compiler(self.view)
    resp = l2c.convertOne(is_auto_save = True)
    MessageWindow(resp)

#all less files
class AllLessToCssCommand(sublime_plugin.TextCommand):
  def run(self, text):
    l2c = compiler.Compiler(self.view)
    sublime.status_message("Compiling .less files...")
    resp = l2c.convertAll()

    if resp != "":
      MessageWindow(resp)
    else:
      sublime.message_dialog("All .less files compiled successfully")

#listener to current less file
class LessToCssSave(sublime_plugin.EventListener):
  def on_post_save(self, view):
    view.run_command("auto_less_to_css")

#change css base setting
class SetLessBaseCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Enter Your Less Base Directory: ", '', lambda s: self.set_less_setting(s), None, None)

  def set_less_setting(self, text):
    settings_base = 'less2css.sublime-settings'

    settings = sublime.load_settings(settings_base)
    
    settings.set("lessBaseDir", text)
    sublime.save_settings(settings_base)

    message = 'Less base directory updated to: ' + text
    sublime.status_message(message)
    sublime.message_dialog(message)

class SetOutputDirCommand(sublime_plugin.WindowCommand):
  def run(self):
    self.window.show_input_panel("Enter CSS Output Directory: ", "", lambda s: self.set_output_dir(s), None, None)

  def set_output_dir(self, text):
    settings_base = 'less2css.sublime-settings'

    settings = sublime.load_settings(settings_base)

    settings.set('outputDir', text)
    sublime.save_settings(settings_base)

    message = 'Output directory updated to: ' + text
    sublime.status_message(message)
    sublime.message_dialog(message)

#toggle minification
class toggleCssMinificationCommand(sublime_plugin.WindowCommand):
  def run(self):
    #show yes/no input
    self.window.show_quick_panel(["Minify css", "Don't minify css"], lambda s: self.set_minify_flag(s))

  def set_minify_flag(self, minify):
    minify_flag = False

    if minify == 0:
      minify_flag = True

    settings_base = 'less2css.sublime-settings'
    settings = sublime.load_settings(settings_base)

    if minify == -1:
      #input was cancelled, don't change
      minify_flag = settings.get('minify', True) #existing or default

    settings.set('minify', minify_flag)
    sublime.save_settings(settings_base)

    message = 'Minify flag updated to: ' + str(minify_flag)
    sublime.status_message(message)
    sublime.message_dialog(message)
