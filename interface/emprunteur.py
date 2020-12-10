#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  6 12:56:53 2020

@author: j
"""

import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
from interface.autocomplet import AutocompleteCombobox as ACCombo
from interface.recap import recap
import req



class emprunteur():
    def __init__(self, core):
        self.activeEmp = None
        self.aJour = ''
        self.contact = ''
        self.id = None
        self.core = core
        self.activInfo = None
        self.top = tk.Toplevel()
        self.top.bind('<Escape>', self.close)
        self.top.title("MEMBRE BIBLIOTHEQUE")
        self.topFrame = tk.Frame(self.top, width=800, height=700)
        self.top.geometry("800x700+0+0")
        
        self.codeWidj =champ(self,
                             self.topFrame,
                             'code',
                             'CODE')
        
        self.nomWidj =champ(self,
                            self.topFrame,
                             'nom',
                             'NOM')
        
        self.prenomWidj =champ(self,
                               self.topFrame,
                               'prenom',
                               'PRENOM')

        
        self.champWidjet = [self.codeWidj,
                            self.nomWidj,
                            self.prenomWidj]
        
        self.endWidjet()
        
        self.listEmp = list()
        self.refreshList(self.listEmp)
        
    

        
        self.topFrame.grid()
        self.core.root.wait_window(self.top)
        
    def close(self, event = None):
        self.top.destroy()
        
    def endWidjet(self):
        self.endFrame = tk.Frame(self.topFrame, width=800, height=250)
        self.endFrame.grid_propagate(0)
        
        
        tk.Label(
            self.endFrame ,
            text="CONTACT").grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.contScrolT = scrolledtext.ScrolledText(
            self.endFrame,
            wrap = tk.WORD,
            width = 80,
            height = 8)
        self.contScrolT.delete('1.0',tk.END)
        self.contScrolT.insert('1.0','-contact-')
        self.contScrolT.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        
        tk.Label(
            self.endFrame ,
            text="A JOUR").grid(row = 1 ,column = 0,padx = 5, pady = 5)
        
        self.AJdBut = tk.Button(
            self.endFrame,
            text = '',
            command = self.AJButFonc)
        self.AJdBut.grid(row = 1 ,column = 1,padx = 5, pady = 5)
        
        
        
        self.delBut = tk.Button(
            self.endFrame,
            text = 'EFFACER',
            command = self.delButFonc)
        self.delBut.grid(row = 2 ,column = 1,padx = 5, pady = 5)
        
        self.validBut = tk.Button(
            self.endFrame,
            text = 'VALIDER',
            command = self.ValidButFonc)
        self.validBut.bind('<Return>', self.ValidButFonc)
        self.validBut.grid(row = 2 ,column = 2,padx = 5, pady = 5)


        self.endFrame.grid()
        
    def delButFonc(self):
        self.id = None
        self.listEmp = list()
        for widjet in self.champWidjet:
            widjet.combo.delete(0, tk.END)
        self.refreshList(self.listEmp)
        self.contScrolT.delete('1.0',tk.END)
        self.AJdBut['text'] = ''
        
        

    def refreshAJ(self, ID = None):
        print('refresh a jour')
        if ID == None:
            if self.activeEmp != None :
                ID = self.activeEmp ['id']
        if ID != None:
            rows = req.select('pret', {'refEmprunteur' : ID})
            self.prets = rows
            if rows == []:
                self.aJour = 'oui'
            else :
                aJour = 'oui'
                for row in rows:
                    print(row['dateRet'])
                    date = datetime.datetime.fromisoformat(row['dateRet'])
                    today = datetime.datetime.today()
                    if date < today :
                        aJour = 'non'
                self.aJour = aJour
                req.SQLupdate('emprunteur', {'aJour' : aJour}, {'id' : ID})
        else :
            self.aJour = ''
            self.prets = list()
        self.AJdBut['text'] = self.aJour
        print(self.aJour)
        
    def getFromChamp(self, value, champ):
        test = req.select("emprunteur", {champ : value})
        for widjet in self.champWidjet :
                if widjet.nomChamp != champ:
                    widjet.combo.delete(0, tk.END)
        if len(test) == 0:
            self.refreshList([])
        else :
            condition = {champ: value}
            self.refreshList(condition)

    
    def refreshList(self, row):
        # self.contactInput = req.convert(self.contScrolT.get("1.0", tk.END))
        condition = dict()
        
        if len(row) == 0 :
            self.listEmp = req.selectAll("emprunteur")
        else :
            for key, value in row.items():
                if value != '':
                    condition[key] = value
            if len(condition) == 0 :
                self.listEmp= req.selectAll("emprunteur")
            else :
                self.listEmp = req.select("emprunteur", condition)
                
                
                
        for widjet in self.champWidjet:
            widjet.setComboValues()
            
            
            
        if len(self.listEmp) == 1:
            
            self.validBut.configure(bg = 'green2')
            
            
            self.activeEmp = self.listEmp[0]
            print('rrrrrrrrrrrrrrrrrrrrrrr')
            print(self.activeEmp)
            self.refreshAJ(ID = self.activeEmp['id'])
            self.id = self.activeEmp['id']
            contact = req.select("emprunteur", {'id' : self.activeEmp['id']})
            print(contact)
            contact = contact[0]['contact']
            print(contact)
            print(type(contact))
            
            
            self.contact = req.convert(contact) 
            print(self.contact)
            
        else :
            self.validBut.configure(bg = 'red')
            
            self.activeEmp = None
            self.refreshAJ()
            self.contact = ''
        print(self.contact)
        self.AJdBut['text'] = self.aJour
        self.contScrolT.delete('1.0',tk.END)
        self.contScrolT.insert('1.0',self.contact)
        
        
        
    def AJButFonc(self):
        if self.activeEmp != None:
            recap(self.core,self.activeEmp)
    
    def getValues(self):
        
        newrow = dict()
        for widjet in self.champWidjet:
            val = widjet.combo.get()
            newrow[widjet.nomChamp ] = req.convert(val)
        self.contactInput = req.convert(self.contScrolT.get("1.0", tk.END))
        return newrow
            
        
    def ValidButFonc(self):
        newrow = self.getValues()
        print(newrow)
        err = 1
        for value in newrow.values():
            if value != '':
               err = 0
        print()
        print('CONTACT INPUT')
        print("'" + self.contactInput+"'")
        print(type(self.contactInput))
        # print(contact)
        if req.netoyageStr(self.contactInput) == '':
            print('contact vide')
            err = 1
            self.activeEmp = None
        
        
        if err == 0:
            cond = dict()
            for key, value in newrow.items():
                if value != '':
                    cond[key] = value
            test = req.select('emprunteur', cond)
            if self.aJour == '':
                self.Ajour = 'oui'
            print('ajour')
            print(self.aJour)
            
            
            newrow['aJour'] = self.aJour
            newrow['contact'] = self.contactInput
            print('""""""""""""""""""""')
            print(newrow)

            newrow['id'] = self.id


            print()
            self.activeEmp = newrow
            self.top.destroy()
            
            
        print(err)
        # if err = o : ajouter une ligne ou modifier une ligne
        
        
        
    
        
        
        
        
        
        
        
        
        
        
        
        
        
    
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
        row = self.parentObj.getValues()
        self.parentObj.refreshList(row)
        



    def ButFonc(self):
        self.parentObj.getFromChamp(self.combo.get(), self.nomChamp )
    
    def setComboValues(self):
        self.values = list()
        for row in self.parentObj.listEmp :
            self.values.append(row[self.nomChamp])

        self.values = list(set(self.values))

        self.combo.set_completion_list(self.values)

        