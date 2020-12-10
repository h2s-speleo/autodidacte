# -*- coding: utf-8 -*-
"""
Éditeur de Spyder

Ceci est un script temporaire.
"""

import tkinter as tk
 
class AutoScrollbar(tk.Scrollbar):
    # a scrollbar that hides itself if it's not needed.  only
    # works if you use the grid geometry manager.
    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            # grid_remove is currently missing from Tkinter!
            self.tk.call("grid", "remove", self)
        else:
            self.grid()
        tk.Scrollbar.set(self, lo, hi)
 
class ScrollFrame(tk.Frame) :
    def __init__(self, parent) :
        self._vscrollbar = AutoScrollbar(parent)
        self._vscrollbar.grid(row=0, column=1, sticky=tk.NS)
        self._hscrollbar = AutoScrollbar(parent, orient=tk.HORIZONTAL)
        self._hscrollbar.grid(row=1, column=0, sticky=tk.EW)
        self._can = tk.Canvas(parent, bg='white',
                              yscrollcommand=self._vscrollbar.set,
                              xscrollcommand=self._hscrollbar.set)
 
        self._can.grid(row=0, column=0, sticky=tk.NSEW)
        self._vscrollbar.config(command=self._can.yview)
        self._hscrollbar.config(command=self._can.xview)
 
        super().__init__(self._can)
        self._can.create_window(0, 0, anchor=tk.NW, window=self, state=tk.NORMAL)
        self.bind('<Configure>', self._actualiserDimension)
 
    def _actualiserDimension(self, evt) :
        self._can.config(scrollregion=self._can.bbox("all"))
 
    def grid(self, **dargs) :
        ''' Ne pas grid la Frame '''
        pass