#!/usr/bin/python

try:
    from ipython_view import IPythonView
    USE_IPYTHON = True
except:
    USE_IPYTHON = False
from pyconsole import Console
    
import gtk
import pango
import platform
import os.path

from org.umlfri.api.mainLoops import GtkMainLoop

def deleteEvent(widget, event):
    widget.hide()
    return True

def pluginMain(interface):
    global USE_IPYTHON
    
    if platform.system()=="Windows":
        FONT = "Lucida Console 9"
    else:
        FONT = "Luxi Mono 10"
    
    W = gtk.Window()
    W.set_size_request(750,550)
    W.set_resizable(True)
    S = gtk.ScrolledWindow()
    S.set_policy(gtk.POLICY_AUTOMATIC,gtk.POLICY_AUTOMATIC)
    if USE_IPYTHON:
        try:
            V = IPythonView()
            V.updateNamespace({'i' : interface, 'exit': lambda: None})
        except:
            USE_IPYTHON = False
    
    if not USE_IPYTHON:
        V = Console(locals = {'i' : interface, 'exit': lambda: None})
    V.modify_base(gtk.STATE_NORMAL, gtk.gdk.color_parse('black'))
    V.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse('white'))
    V.modify_font(pango.FontDescription(FONT))
    V.set_wrap_mode(gtk.WRAP_CHAR)
    V.show()
    S.add(V)
    S.show()
    W.add(S)
    # W.show()
    W.connect('delete_event', deleteEvent)
    # W.connect('destroy', lambda x: (W.hide(), False)[-1])
    
    interface.gui_manager.button_bar.add_button(
        'OpenPythonConsole',
        lambda *a: W.show_all(),
        -1,
        'Python Console',
        imagefilename = os.path.join('icons', 'pythonTerminal-24.png')
    )
    
    interface.transaction.autocommit = True
    interface.set_main_loop(GtkMainLoop())
    
    # gtk.main()
