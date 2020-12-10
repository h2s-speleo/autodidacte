#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec  9 11:39:28 2020

@author: j
"""
import tkinter as tk
import req

class recap():
    def __init__(self, core, membre, liste = []):
        dicoPret = dict()
        prets = req.select('pret', {'refEmprunteur' : membre ['id']})
        for pret in prets :
            dicoPret[pret['refOuv']] = pret
        
        if liste == []:
            label = "ensemble des prets"
            
            for key in dicoPret.keys():
                test = req.select('ouvrage', {'id' : key})
                if test != []:
                    liste.append(test[0])
        else :
            label = "résumé de l'emprunt"
            
        textList = list()
        for row in liste:
            newtext = "TITRE : {}\nAUTEUR  : {}\nEDITION : {}\nISBN : {}".format(
                row['Title'], row['Authors'],row['Publisher'],row['ISBN'])
            
            dateRet = dicoPret[row['id']]['dateRet']
            newtext = newtext + "\n\nDATE RETOUR : {}\n\n\n".format(dateRet)
            textList.append((newtext, dateRet))
            
            test = req.select('pret', {'refEmprunteur' : membre ['id'],
                                       'refOuv' : row['id']})
            

            for i in range(len(test)-1):
                textList.append((newtext, dateRet))
            
            
        textList = sorted(textList, key=lambda textList: textList[1])
        text = ''
        for row in textList :
            text = text + row[0]

    
        self.core = core
        self.liste = liste
        self.top = tk.Toplevel()
        self.top.bind('<Escape>', self.close)
        self.top.title("SYNTHESE")
        self.topFrame = tk.Frame(self.top, width=800, height=400)
        self.top.geometry("800x700+0+0")
        


        
        tk.Label(
            self.topFrame ,
            text=label).grid(
                row = 0 ,column = 0,padx = 5, pady = 5
                )
        
        self.OKdBut = tk.Button(
            self.topFrame,
            text = 'OK',
            command = self.close)
        self.OKdBut.grid(row = 1 ,column = 0,padx = 5, pady = 5)
        

        
        self.contScrolT = tk.scrolledtext.ScrolledText(
            self.topFrame,
            wrap = tk.WORD,
            width = 80,
            height = 8)

        self.contScrolT.insert('1.0',text)
        self.contScrolT.grid(row = 2 ,column = 0,padx = 5, pady = 5)
        
        self.topFrame.grid()
        
        self.OKdBut.focus_set()
        self.core.root.wait_window(self.top)
        
        

        
    def close(self, event = None):
        self.top.destroy()
        
         