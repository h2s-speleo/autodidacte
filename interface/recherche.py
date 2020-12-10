#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 23:49:01 2020

@author: j
"""
import tkinter as tk
from tkinter import ttk
from interface.formulaire import recForm, modForm
import req

class recherche():
    """
    Classe gérant la page inventaire
    """
    def __init__(self, core):
        """
        initialisation de la page des inventaires
        argument :
            core (obj) : objet Core 
        """

        self.core = core
        self.Frame = tk.Frame(core.MainF, width=1200, height=800)
        self.core.onglet.add(self.Frame, text='RECHERCHE')
        self.recBut = tk.Button(
                self.Frame,
                text = "recherche simple",
                command = self.recButFonc)
        self.recBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.modBut = tk.Button(
                self.Frame,
                text = "rechercher et modifier",
                command = self.modButFonc)
        self.modBut.grid(row = 1 ,column = 0,padx = 5, pady = 5)
        

    def recButFonc(self):
        ret = 1
        while ret != None:
            # try :
            info = recForm(self.core)
            ret = info.activInfo
            del(info)
            # except :
            #     print('fail')
            #     ret = None

    def modButFonc(self):
        ret = 1
        while ret != None:
            # try :
            info = modForm(self.core)
            ret = info.activInfo
            del(info)
            if ret != None:
                ID = ret['id']
                stock = ret['stock']
                del ret['stock']
                test = req.select('ouvrage', {'id' : ID})
                if test == []:
                    req.insert('ouvrage', ret)
                else :
                    del ret['id']
                    req.SQLupdate('ouvrage', ret, {'id' : ID})
                req.SQLupdate('stock', {'stock' : stock}, {'refOuv' : ID})
                
       
            # except :
            #     print('fail')
            #     ret = None
