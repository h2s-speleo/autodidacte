#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 13:40:05 2020

@author: j
"""
import datetime
import uuid
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import req
from interface.formulaire import invForm
from interface.export import export




class inventaire():
    """
    Classe gérant la page inventaire
    """
    def __init__(self, core):
        """
        initialisation de la page des inventaires
        argument :
            core (obj) : objet Core 
        """
        self.activeInv = None
        self.combVal = list()
        self.core = core
        self.inventFrame = tk.Frame(core.MainF, width=1200, height=800)
        self.core.onglet.add(self.inventFrame, text='GESTION DU STOCK')
        self.activeInvWidjet()
        self.creatWidjet()
        self.completeWidjet()
        self.supWidjet()
        self.majWidjet()
        self.stockWidjet()
        self.expWidjet()
        self.refreshComboList()
        
        # export(self.core)
        
    def activeInvWidjet(self):
        self.activeInvFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.activeInvFrame.grid_propagate(0)
        self.strActiveInv = tk.StringVar()
        self.strActiveInv.set('')
        self.label1 = tk.Label( self.activeInvFrame ,
                      text="inventair actif    : ")
        self.label1.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.label2 = tk.Label( self.activeInvFrame ,
                      textvariable=self.strActiveInv)
        self.label2.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        self.activeInvFrame.grid()
        
    def creatWidjet(self):
        self.creatFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.creatFrame.grid_propagate(0)
        self.creatBut = tk.Button(
                self.creatFrame,
                text = "Créer un nouvel inventaire",
                command = self.creatButFonc)
        self.creatBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.newInventName = tk.StringVar()
        self.newInventName.set(self.builInventName())
        self.creatEntry = tk.Entry(self.creatFrame,
                                   textvariable=self.newInventName,
                                   width=50)
        self.creatEntry.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        self.creatFrame.grid()
        
    def builInventName(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        nom = "inventaire-"+today
        rows = req.select('listInvent', {'nom' : nom})
        if rows != list() :
            nom = nom + "_"
            count = 2
            while True :
                rows = req.select('listInvent', {'nom' : nom+str(count)})
                if rows == list():
                    nom = nom+str(count)
                    break
                else :
                    count += 1
        return nom

    def creatButFonc(self):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
        nom = self.newInventName.get()
        if nom != '':
            rows = req.select('listInvent', {'nom' : nom})
            if rows == list() :
                req.insert('listInvent', {'id' : str(uuid.uuid4()),
                                          'date' : today,
                                          'nom' : nom})
            else :
                nom = nom + "_"
                count = 2
                while True :
                    rows = req.select('listInvent', {'nom' : nom+str(count)})
                    if rows == list():
                        nom = nom+str(count)
                        req.insert('listInvent', {'id' : str(uuid.uuid4()),
                                                  'date' : today,
                                                  'nom' : nom})
                        self.newInventName.set(nom)
                        break
                    else :
                        count += 1
            self.refreshComboList()
            self.activeInv = nom
            # renvoyer vers un topLevel pour savoir si on veut commencer l'inventaire
            if self.activeInv not in ['', None]:
                print("commencer l'inventaire ?")
                question = messagebox.askquestion("Commencer inventaire", "ajouter des ouvrages a l'inventaire " + self.activeInv )
                if question == "yes":
                    self.startInv()
                

                    
    def refreshComboList(self):
        widjList = [self.compComb,
                    self.supComb,
                    self.majComb]
        self.combVal = list()
        rows = req.selectAll('listInvent')
        for row in rows :
            self.combVal.append(row['nom'])
        for widjet in widjList :
            widjet["values"] = self.combVal
                    
    def completeWidjet(self):
        self.completeFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.completeFrame.grid_propagate(0)
        self.compBut = tk.Button(
                self.completeFrame,
                text = "Poursuivre un inventaire",
                command = self.compButFonc)
        self.compBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.compComb = ttk.Combobox(self.completeFrame,
                                     values=self.combVal,
                                     state="readonly",
                                     width=50)
        self.compComb.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        self.completeFrame.grid()
    
    def compButFonc(self):
        name = self.compComb.get()
        if name != '':
            self.activeInv = name
            self.strActiveInv.set( name )
            self.startInv()
    
    def supWidjet(self):
        self.supFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.supFrame.grid_propagate(0)
        self.supBut = tk.Button(
                self.supFrame,
                text = "supprimer un inventaire",
                command = self.supFrameFonc)
        self.supBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.supComb = ttk.Combobox(self.supFrame,
                                     values=self.combVal,
                                     state="readonly",
                                     width=50)
        self.supComb.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        self.supFrame.grid()
    
    def supFrameFonc(self):
        name = self.supComb.get()
        if name != '':
            req.SQLdelet('listInvent', {'nom' : name})
            req.SQLdelet('inventaire', {'refInv' : name})
            self.refreshComboList()
            self.supComb.set('')
            if self.compComb.get() not in self.combVal :
                self.compComb.set('')
                self.strActiveInv.set( '' )
            if self.majComb.get() not in self.combVal :
                self.majComb.set('')
                self.strActiveInv.set( '' )
    
    def stockWidjet(self):
        self.stockFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.stockFrame.grid_propagate(0)
        self.skockBut = tk.Button(
                self.stockFrame,
                text = "ajouter exemplaire au stock",
                command = self.stockFrameFonc)
        self.skockBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.delskockBut = tk.Button(
                self.stockFrame,
                text = "suprimer exemplaire du stock",
                command = self.delstockFrameFonc)
        self.delskockBut.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        
        
        self.stockFrame.grid()
        
        
    def delstockFrameFonc(self):
        
        ret = 1
        while ret != None:
            try :
                info = invForm(self.core)
                ret = info.activInfo
                del(info)
            except :
                print('fail')
                ret = None
            if ret != None:
                print('do things')
                test = req.select("stock", {'refOuv' : ret['id']})
                if test == []:
                    req.insert('stock', {'refOuv' : ret['id'],
                                         'stock' : 0,
                                         'id' : str(uuid.uuid4())}
                               )
                else :
                    stock = int(test[0]['stock'])
                    ID = test[0]['id']
                    if stock < 0:
                        stock = 0
                    if stock > 0:
                        stock = stock - 1
                    req.SQLupdate('stock', {'stock' : stock}, {'id' : ID})
        
    def stockFrameFonc(self):
        
        ret = 1
        while ret != None:
            try :
                info = invForm(self.core)
                ret = info.activInfo
                del(info)
            except :
                print('fail')
                ret = None
            if ret != None:
                print('do things')
                test = req.select("stock", {'refOuv' : ret['id']})
                if test == []:
                    req.insert('stock', {'refOuv' : ret['id'],
                                         'stock' : 1,
                                         'id' : str(uuid.uuid4())}
                               )
                else :
                    stock = int(test[0]['stock'])
                    ID = test[0]['id']
                    stock += 1
                    req.SQLupdate('stock', {'stock' : stock}, {'id' : ID})
        
        
    def majWidjet(self):
        self.majFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.majFrame.grid_propagate(0)
        self.majBut = tk.Button(
                self.majFrame,
                text = "metre a jour le stocke a partir d'un inventaire",
                command = self.majFrameFonc)
        self.majBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.majComb = ttk.Combobox(self.majFrame,
                                     values=self.combVal,
                                     state="readonly",
                                     width=50)
        self.majComb.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        self.majFrame.grid()
        
    def majFrameFonc(self):
        name = self.majComb.get()
        if name != '':
            self.activeInv = name
            self.strActiveInv.set(name)
            exp = export(self.core, nom = 'stock')
            del exp
            req.SQLupdate('stock', {'stock' : '0'}, None)
            invent = req.select('inventaire', {'refInv' : name})
            for row in invent :
                if req.select('stock', {'refOuv' : row['refOuv']}) == []:
                    del row['refInv']
                    req.insert('stock', row)
                else :
                    req.SQLupdate('stock', {'stock': row['stock']}, {'refOuv' : row['refOuv']})
                    

            
    def startInv(self):
        ret = 1
        while ret != None:
            try :
                info = invForm(self.core)
                ret = info.activInfo
                del(info)
            except :
                print('fail')
                ret = None
            if ret != None:
                print('do things')
                test = req.select("inventaire", {'refOuv' : ret['id'],
                                                 'refInv' :  self.activeInv})
                if test == []:
                    req.insert('inventaire', {'refOuv' : ret['id'],
                                              'refInv' :  self.activeInv,
                                              'stock' : 1,
                                              'id' : str(uuid.uuid4())}
                               )
                else :
                    stock = int(test[0]['stock'])
                    ID = test[0]['id']
                    stock += 1
                    req.SQLupdate('inventaire', {'stock' : stock}, {'id' : ID})
                    
    def expWidjet(self):
        self.expFrame = tk.Frame(self.inventFrame, width=1200, height=50)
        self.expFrame.grid_propagate(0)
        self.expBut = tk.Button(
                self.expFrame,
                text = "IMPORT - EXPORT",
                command = self.expFrameFonc)
        self.expBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.expFrame.grid()
        
    def expFrameFonc(self):
        export(self.core)
        self.refreshComboList()
    
    