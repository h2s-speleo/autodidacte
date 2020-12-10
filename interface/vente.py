#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 02:22:05 2020

@author: j
"""
import tkinter as tk
# from tkinter import ttk
# from interface.formulaire import recForm, modForm
import req
from interface.formulaire import invForm
import uuid
import datetime

class vente():
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
        self.core.onglet.add(self.Frame, text='VENTE')
        
        self.sorBut = tk.Button(
                self.Frame,
                text = "DEBUTER LA VENTE",
                command = self.sorButFonc)
        self.sorBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        

        
    def sorButFonc(self):
        ret = 1
        ouvrages = list()
        while ret != None:
            try :
                info = invForm(self.core)
                ret = info.activInfo
                del(info)
            except :
                print('fail')
                ret = None
            if ret != None:
                print(ret)
                
                test = req.select("ouvrage", ret)
                if test == []:
                    ret['id'] = str(uuid.uuid4())
                    req.insert("ouvrage", ret)
                
                if ret['prix'] == 'B' :
                    
                    newtext = "TITRE : {}\nAUTEUR  : {}\nEDITION : {}\nISBN : {}".format(
                        ret['Title'], ret['Authors'],ret['Publisher'],ret['ISBN'])
                    
                    errtext = "Attention, cet ouvrage fait partie de la bibliotheque.\
                        \nil n'est pas pris en compte dans la vente\n\n" + newtext
                    tk.messagebox.showerror("Livre de la bibliotheque", errtext)
                else :
                    ouvrages.append(ret)
        if ouvrages != [] :

            if self.synth(ouvrages) == 1:
                for ouv  in ouvrages:
                    print(ouv)
                    print()
                    
                    dicoVente = {
                        'id' : str(uuid.uuid4()),
                        'date' : datetime.datetime.today().strftime('%Y-%m-%d'),
                        'quantite' : 1,
                        'refOuv': ouv['id']
                        }
                    
                    req.insert('vente', dicoVente)
                    
                    test = req.select("ouvrage", ouv)
                    if test == []:
                        ouv['id'] = str(uuid.uuid4())
                        req.insert("ouvrage", ouv)
                        req.insert("stock", {'id' : str(uuid.uuid4()),
                                             'stock' : '0',
                                             'refOuv' : ouv['id']})
                    else :
                        row = req.select('stock', {'refOuv' : ouv['id']} )
                        if row == []:
                            req.insert("stock", {'id' : str(uuid.uuid4()),
                                                 'stock' : '0',
                                                 'refOuv' : ouv['id']})
                        else :
                            nombre = int(row[0]['stock'])
                            if nombre < 0 :
                                nombre = 0
                            elif nombre > 0:
                                nombre = nombre -1
                            req.SQLupdate('stock', {'stock' : str(nombre)}, {'refOuv' : ouv['id']})
                        

    def synth(self, liste):
        
        
        valWidj = recap(self.core, liste)
        valid = valWidj.valid
        del valWidj

        return valid


class recap():
    def __init__(self, core, liste):
        self.valid = 0
        self.core = core
        self.liste = liste
        self.top = tk.Toplevel()
        self.top.bind('<Escape>', self.close)
        self.top.title("SYNTHESE VENTE")
        self.topFrame = tk.Frame(self.top, width=800, height=400)
        self.top.geometry("800x700+0+0")
        
        
        somme = 0
        text = str()
        for row in self.liste:
            newtext = "TITRE : {}\nAUTEUR  : {}\nEDITION : {}\nISBN : {}".format(
                row['Title'], row['Authors'],row['Publisher'],row['ISBN'])
            prix = row['prix']
            if prix == 'B' :
                errtext = "Attention, cet ouvrage fait partie de la bibliotheque.\
                    \nil n'est pas pris en compte dans la vente\n\n" + newtext
                tk.messagebox.showerror("Livre de la bibliotheque", errtext)
            else :
                if prix == 'PL' :
                    floatprix = 0
                else :
                    try :
                        floatprix = float(row['prix'])
                    except :
                        errtext = "Attention, impossible de lire le prix de cet ouvrage.\
                            \nson prix n'a pas été ajouté a l'adition\n\n" + newtext
                        tk.messagebox.showerror("Livre de la bibliotheque", errtext)
                        floatprix = 0
                somme = somme + floatprix
                newtext = newtext + "\n\n{} €\n\n\n".format(row['prix'])
                text = text + newtext
            

        somme = str(somme)
        if somme[-2] == '.':
            somme = somme + '0'
        print(text)
        print(somme)
        

        
        tk.Label(
            self.topFrame ,
            text="TOTAL : " + somme + "€\nVALIDER LA VENTE").grid(
                row = 0 ,column = 0,padx = 5, pady = 5
                )
        
        self.OKdBut = tk.Button(
            self.topFrame,
            text = 'OK',
            command = self.OKButFonc)
        self.OKdBut.grid(row = 1 ,column = 0,padx = 5, pady = 5)
        
        self.CancelBut = tk.Button(
            self.topFrame,
            text = 'ANNULER',
            command = self.CancelButFonc)
        self.CancelBut.grid(row = 2 ,column = 0,padx = 5, pady = 5)
        
        self.contScrolT = tk.scrolledtext.ScrolledText(
            self.topFrame,
            wrap = tk.WORD,
            width = 80,
            height = 8)

        self.contScrolT.insert('1.0',text)
        self.contScrolT.grid(row = 3 ,column = 0,padx = 5, pady = 5)
        
        self.topFrame.grid()
        self.core.root.wait_window(self.top)
        
        
    def OKButFonc(self):
        self.valid = 1
        self.close()

    
    def CancelButFonc(self):
        self.close()
    

        
    def close(self, event = None):
        self.top.destroy()
        
    
        
    
    
