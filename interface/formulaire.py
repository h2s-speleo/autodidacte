#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec  1 22:24:47 2020

@author: j
"""
from interface.autocomplet import AutocompleteCombobox as ACCombo
import tkinter as tk
import req
import uuid
import re
import req

class formulaire():
    """
    Classe gérant le toplevel formulaire
    """
    def __init__(self, core):
        """
        initialisation du formulaire
        argument :
            core (obj) : objet Core 
        """
        self.core = core
        self.activInfo = None
        self.top = tk.Toplevel()
        self.top.bind('<Escape>', self.close)
        self.top.title("formulaire")
        self.topFrame = tk.Frame(self.top, width=800, height=700)
        
        
        self.top.geometry("800x700+0+0")
        
        self.isbnWidj =champ(self,
                             self.topFrame,
                             'ISBN',
                             'ISBN')
        
        self.titreWidj = champ(self,
                               self.topFrame,
                               'Title',
                               'TITRE')
        
        self.autWidj = champ(self,
                             self.topFrame,
                             'Authors',
                             'AUTRICES / AUTEURS')
        
        self.ediWidj = champ(self,
                             self.topFrame,
                             'Publisher',
                             'EDITION')
        
        self.anneWidj = champ(self,
                              self.topFrame,
                              'Year',
                              'ANNEE')
        
        self.langWidj = champ(self,
                              self.topFrame,
                              'Language',
                              'LANGUE')
        
        self.priWidj = champ(self,
                             self.topFrame,
                             'prix',
                             'PRIX')
        
        self.champWidjet = [self.isbnWidj,
                            self.titreWidj,
                            self.autWidj,
                            self.ediWidj,
                            self.anneWidj,
                            self.langWidj,
                            self.priWidj]
                            
        self.endWidjet()
        self.listOuv = list()
        self.refreshList(self.listOuv)
        
        self.topFrame.grid()
        self.isbnWidj.combo.focus_set()
        self.core.root.wait_window(self.top)

    def endWidjet(self):
        self.endFrame = tk.Frame(self.topFrame, width=800, height=50)
        self.endFrame.grid_propagate(0)
        self.delBut = tk.Button(
            self.endFrame,
            text = 'EFFACER',
            command = self.delButFonc)
        self.delBut.grid(row = 0 ,column = 1,padx = 200, pady = 5)
        self.validBut = tk.Button(
            self.endFrame,
            text = 'VALIDER',
            command = self.ValidButFonc)
        self.validBut.bind('<Return>', self.ValidButFonc)
        self.validBut.grid(row = 0 ,column = 2,padx = 200, pady = 5)
        self.endFrame.grid()
        
    def getValues(self):
        newrow = dict()
        for widjet in self.champWidjet:
            if widjet.nomChamp == 'prix':
                val = self.corPrix(widjet.combo.get())
            else :
                val = widjet.combo.get()
            newrow[widjet.nomChamp ] = req.convert(val)
        self.refreshList(newrow)
        self.setColor()
        self.setFocus()
        
        
    def setColor(self):
        for widjet in self.champWidjet:
            if widjet.nomChamp in ['ISBN', 'Title', 'Authors', 'prix']:
                if widjet.combo.get() == '':
                    widjet.Frame.config(bg='orange')
                else :
                    widjet.Frame.config(bg='green1')
        
    def refreshList(self, row):
        condition = dict()
        if len(row) == 0 :
            self.listOuv = req.selectAll("ouvrage")
        else :
            for key, value in row.items():
                if value != '':
                    condition[key] = value
            if len(condition) == 0 :
                self.listOuv = req.selectAll("ouvrage")
            else :
                self.listOuv = req.select("ouvrage", condition)
        for widjet in self.champWidjet:
            widjet.setComboValues()
        self.getStock()

    def corPrix(self, value):
        if 'B' in value.upper():
            newVal = 'B'
        elif 'PL' in value.upper():
            newVal = 'PL'
        else :
            value = value.replace(' ', '')
            value = value.replace(',', '.')
            while True:
                if value == '0':
                    break
                if value.startswith(' ') or value.startswith('0'):
                    value = value[1:]
                else :
                    break
            while True:
                if value.endswith(' '):
                    value = value[:-1]
                else :
                    break
            if value.startswith('.'):
                value = "0" + value
            
            r = 0
            testList = value.split('.')
            
            if len(testList) > 0 :
                if not re.match("\d+", testList[0]):
                    r = 1
            if len(testList) == 2 :
                if not re.match("\d+", testList[1]):
                    r = 1
                if len(testList[1]) > 2:
                    testList[1] = testList[1][:2]
            if r == 0:
                newVal = str('.'.join(testList))
            else :
                newVal = ''
        self.priWidj.combo.set(newVal)
        return newVal

    def delButFonc(self):
        self.listOuv = list()
        for widjet in self.champWidjet:
            widjet.combo.delete(0, tk.END)
        self.refreshList(self.listOuv)
        self.setColor()
        
    def ValidButFonc(self, envent = None):
        self.getValues()
        newrow = dict()
        for widjet in self.champWidjet:
            if widjet.nomChamp == 'prix':
                val = self.corPrix(widjet.combo.get())

            else :
                val = widjet.combo.get()
            newrow[widjet.nomChamp ] = req.convert(val)
        reqRow = req.select("ouvrage", newrow)
        self.surcharge(newrow, reqRow)


    
    def setFocus(self):
        var = 0
        champs= [self.isbnWidj,
                self.titreWidj,
                self.autWidj,
                self.ediWidj,
                self.priWidj]
        for champ in champs :
            if champ.combo.get() == '':
                champ.combo.focus_set()
                var = 1
                break
        if var == 0:
            self.validBut.focus_set()
            
    
    def getFromChamp(self, value, champ):
        
        condition = None
        test = req.select("ouvrage", {champ : value})
        if len(test) == 0:
            print("recherche internet : ", end ='')
            if champ == 'ISBN':
                try :
                    info = req.getInfoFromNet(value)
                    for widj in self.champWidjet:
                        widj.combo.set(info[widj.nomChamp])
                    self.setFocus()
                    print('ok')
                    print(info)
                except :
                    print('fail')
                    for widjet in self.champWidjet :
                        if widjet.nomChamp != champ:
                            widjet.combo.delete(0, tk.END)
            else :
                condition = {champ: value}
        else :
            condition = {champ: value}
        if condition != None:
            for widjet in self.champWidjet :
                if widjet.nomChamp != champ:
                    widjet.combo.delete(0, tk.END)
            self.refreshList(condition)
        self.setColor()
            
    def check(self):
        var = 1
        champs= [self.isbnWidj,
                self.titreWidj,
                self.autWidj,
                self.ediWidj,
                self.priWidj]
        for champ in champs :
            if champ.combo.get() == '':
                var = 0
                break
        return var
    
    def getStock(self):
        pass
    
        
    def surcharge(self, newrow, reqRow):
        if self.check() == 1:
        
            if reqRow == []:
                self.activInfo = newrow
                self.activInfo['id'] = str(uuid.uuid4())
            else:
                self.activInfo = reqRow[0]
            self.top.destroy()  
        else :
            self.setFocus()
    
    def close(self, event = None):
        self.top.destroy()

     
class champ():
    
    def __init__(self, parentObj, parentFrame, nomChamp, label):
        self.parentObj = parentObj
        self.nomChamp = nomChamp
        self.Frame = tk.Frame(parentFrame, width=800, height=50)
        self.Frame.grid_propagate(0)
        self.But = tk.Button(
                self.Frame,
                text = label,
                command = self.ButFonc)
        self.But.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        self.combo = ACCombo(
                self.Frame,
                width=50)
        self.combo.bind('<Return>', self.enterBind)
        self.combo.bind("<<ComboboxSelected>>", self.enterBind)
        self.combo.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        self.Frame.grid()
    
    def enterBind(self, envent = None):
        self.parentObj.getValues()
        if self.nomChamp == 'ISBN' :
            code = self.combo.get()
            if len(code) > 13 :
                print(code)
                code = code[:13]
                print(code)

                self.combo.set(code)
            
            
            self.parentObj.getFromChamp(self.combo.get(), self.nomChamp )
        
    
            
    def ButFonc(self):
        self.parentObj.getFromChamp(self.combo.get(), self.nomChamp )
    
    def setComboValues(self):
        self.values = list()
        for row in self.parentObj.listOuv :
            self.values.append(row[self.nomChamp])
        # print(self.values)
        self.values = list(set(self.values))
        # print(self.values)
        # print()
        self.combo.set_completion_list(self.values)


class invForm(formulaire):
              
    def surcharge(self, newrow, reqRow):
        if self.check() == 1:
            if reqRow == []:
                testISBN = req.select("ouvrage", {'ISBN' : newrow['ISBN'] })
                if testISBN == []:
                    self.activInfo = newrow
                    self.activInfo['id'] = str(uuid.uuid4())
                    req.insert("ouvrage", self.activInfo)
                else :
                    req.SQLupdate("ouvrage", newrow , {'ISBN' : newrow['ISBN']})
                    self.activInfo = newrow
                    self.activInfo['id'] = testISBN[0]['id']
            else:
                self.activInfo = reqRow[0]
            self.top.destroy()  
        else :
            self.setFocus()
            
class recForm(formulaire):
    def endWidjet(self):
        self.stock = ''
        self.endFrame = tk.Frame(self.topFrame, width=800, height=100)
        self.endFrame.grid_propagate(0)
        
        tk.Label(
            self.endFrame ,
            text="STOCK").grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.stockVar = tk.StringVar()
        self.stockVar.set(self.stock)
        self.stockEntry = tk.Entry(self.endFrame,
                                   textvariable=self.stockVar,
                                   width=10)
        self.stockEntry.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        
        
        
        
        self.validBut = tk.Button(
            self.endFrame,
            text = 'EFFACER',
            command = self.delButFonc)
        self.validBut.bind('<Return>', self.ValidButFonc)
        self.validBut.grid(row = 1 ,column = 2,padx = 200, pady = 5)
        self.endFrame.grid()
        
    def getStock(self):
        # print('----------------------------')
        # print(self.listOuv)
        self. stock = ''
        if len(self.listOuv) == 1:
            ID = self.listOuv[0]['id']
            row = req.select('stock', {'refOuv' : ID})
            if row != []:
                self.stock = row[0]['stock']
        
        self.stockVar.set(self.stock)


    
class modForm(recForm):
    def endWidjet(self):
        self.stock = ''
        self.endFrame = tk.Frame(self.topFrame, width=800, height=100)
        self.endFrame.grid_propagate(0)
        
        tk.Label(
            self.endFrame ,
            text="STOCK").grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.stockVar = tk.StringVar()
        self.stockVar.set(self.stock)
        self.stockEntry = tk.Entry(self.endFrame,
                                   textvariable=self.stockVar,
                                   width=10)
        self.stockEntry.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        
        
        
        
        self.delBut = tk.Button(
            self.endFrame,
            text = 'EFFACER',
            command = self.delButFonc)
        self.delBut.grid(row = 1 ,column =2,padx = 150, pady = 5)
        
        
        
        self.validBut = tk.Button(
            self.endFrame,
            text = 'VALIDER',
            command = self.ValidButFonc)
        self.validBut.bind('<Return>', self.ValidButFonc)
        self.validBut.grid(row = 1 ,column = 3,padx = 150, pady = 5)
        
        self.endFrame.grid()
        

    def ValidButFonc(self, envent = None):
        nombre = int(self.stockVar.get())
        print(nombre)
        try :
            nombre = int(nombre)
            self.retStock  = str(nombre)
        except:
            self.retStock  = ''
        
        
        newrow = dict()
        for widjet in self.champWidjet:
            if widjet.nomChamp == 'prix':
                val = self.corPrix(widjet.combo.get())

            else :
                val = widjet.combo.get()
            newrow[widjet.nomChamp ] = req.convert(val)
        reqRow = req.select("ouvrage", {'ISBN' : newrow['ISBN']})
        self.surcharge(newrow, reqRow)
        
    
    
    def surcharge(self, newrow, reqRow):
        print('reqRow')
        print(reqRow)
        print()
        if self.check() == 1:
        
            if reqRow == []:
                self.activInfo = newrow
                self.activInfo['id'] = str(uuid.uuid4())
            else:
                self.activInfo = newrow
                self.activInfo['id'] =  reqRow[0]['id']


            self.activInfo['stock'] = self.retStock

        
            self.top.destroy()  
        else :
            self.setFocus()
    
    def close(self, event = None):
        self.top.destroy()