#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk
from interface.scrolable_frame import ScrollFrame
from interface.inventaire import inventaire
from interface.recherche import recherche
from interface.vente import vente
from interface.bibliotheque import bibli



class Core():
    """
    Classe gérant le noeud central de l'interface. 
    """
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Autodidacte')
        self.root.geometry('1200x800+0+0')
        self.root.resizable(True, True)
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.MainF = ScrollFrame(self.root)
        self.MainF.grid()
        self.onglet = ttk.Notebook(self.MainF)
        self.onglet.grid()
        
        self.vente = vente(self)
        self.bibli = bibli(self)
        self.recherche = recherche(self)
        self.inventaire = inventaire(self)
        
        

   
        self.root.mainloop()

if __name__ == '__main__':
    Core()
    
