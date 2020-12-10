#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  5 18:12:09 2020

@author: j
"""

import uuid
import datetime
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import req
import tkinter.filedialog as filedialog
from excel_lib import Tableur
import subprocess as sp

class export():
    def __init__(self, core, nom = None):
        self.tabSoft = "libreoffice"
        self.core = core
        self.top = tk.Toplevel()
        self.top.bind('<Escape>', self.close)
        self.top.title("IMPORT - EXPORT")
        self.topFrame = tk.Frame(self.top)
        self.top.geometry("800x100+0+0")
        
        self.combValues = ['stock','vente', 'pret','pret_en_retard', 'membre', 'refferences']
        rows = req.selectAll('listInvent')
        for row in rows :
            
            self.combValues.append(row['nom'])

        self.expBut = tk.Button(
                self.topFrame,
                text = "exporter",
                command = self.expButFonc)
        self.expBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.expComb = ttk.Combobox(self.topFrame,
                                      values=self.combValues,
                                      state="readonly",
                                      width=70)
        self.expComb.grid(row = 0 ,column = 1,padx = 5, pady = 5)
        
        # self.impBut = tk.Button(
        #         self.topFrame,
        #         text = "importer",
        #         command = self.impButFonc)
        # self.impBut.grid(row = 1 ,column = 0,padx = 5, pady = 5)
        
        
        self.topFrame.grid()
        

        
        if nom != None:
            print(nom)
            self.expComb.current(0)
            self.expButFonc(ouvrir = 0)
        else :

        
            self.core.root.wait_window(self.top) 
        
        
        
    def close(self, event = None):
        self.top.destroy()

    def creatInvDB(self, nom):
        today = datetime.datetime.today().strftime('%Y-%m-%d')
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

                    break
                else :
                    count += 1
        return nom
    
    def expStockInv(self, nom, ouvrir):
        
        if nom == 'stock':
            spec = nom
            today = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
            nom = 'export-'+nom+"-"+today

        else :
            spec = 0

        if ouvrir == 1:
            compPath = filedialog.asksaveasfilename(
                title="Enregistrer sous",
                initialdir='fichiers',
                initialfile=nom + ".xlsx",
                defaultextension=".xlsx",
                filetypes = [("xlsx", '*.xlsx')]
                )
        else :
            compPath = 'sauvegardes/{}.xlsx'.format(nom)
            
        if compPath != '':
            filename= nom + '.xlsx'
            print(filename)
            filePath = compPath.replace(filename, '')
            print(filePath)
            
            if spec == 'stock':
                extract =req.selectAll('stock')
            else : 
                extract = req.select('inventaire', {'refInv' : nom})
    
            if extract != []:
                rows = list()
                for elm in extract:
                    print(elm)
                    print()
                    
                    ouvs = req.select('ouvrage', {'id' : elm['refOuv']})
                    if ouvs == []:
                        ouvs = [{'id' : elm['refOuv'],
                               'ISBN' : '',
                               'Title' : '',
                               'Authors' : '',
                               'Publisher' : '',
                               'Years' : '',
                               'Language' : '',
                               'prix' : ''}]
                    for ouv in ouvs:
                        ouv['stock'] = elm['stock']
                        rows.append(ouv)
    
    
                    
                if rows != []:
                    keys = list(rows[0].keys())
                    TAB = Tableur(nom = filename,
                                  path = filePath,
                                  nouv = keys)
        
                    for row in rows:
                        print(row)
                        TAB.ajoutLigne(row)
                    
                    TAB.save()
    
            else :
                dico = {'id' : '',
                        'ISBN' : '',
                        'Title' : '',
                        'Authors' : '',
                        'Publisher' : '',
                        'Years' : '',
                        'Language' : '',
                        'prix' : '',
                        'stock' : ''}
                rows = [dico]
                keys = list(dico.keys())
                TAB = Tableur(nom = filename,
                              path = filePath,
                              nouv = keys)
    
                for row in rows:
                    print(row)
                    TAB.ajoutLigne(row)
                TAB.save()
    
    
            if ouvrir == 1:
                sp.Popen((self.tabSoft, filePath + filename))
        
    
    def expButFonc(self, ouvrir = 1):
        

        nom = self.expComb.get()
        

        

        if nom != "":
            if nom == 'pret':
                self.expPret(nom, ouvrir, retard = 0)
            elif nom == 'pret_en_retard':
                self.expPret(nom, ouvrir, retard = 1)
            elif nom == 'vente':
                self.expVente(nom, ouvrir)
            
            elif nom == 'membre':
                self.expTable(nom, ouvrir, 'emprunteur')
                
            elif nom == "refferences":
                self.expTable(nom, ouvrir, 'ouvrage')
            
            
            else :
                self.expStockInv(nom, ouvrir)
            
            
                
    
            self.close()
    def impButFonc(self):
        filename = filedialog.askopenfilename(
                title="ouvrir",
                initialdir='fichiers',
                initialfile="",
                defaultextension=".xlsx",
                filetypes = [("xlsx files", '*.xlsx')]
                )
        
        # filename = "/home/j/projet_python/autodidacte/fichiers/inventaire-2020-12-05.xlsx"
        print('import')
        
        if filename != '':
            champs = ['id',
                     'ISBN',
                     'Title',
                     'Authors',
                     'Publisher',
                     'Year',
                     'Language' ,
                     'prix',
                     'stock']
            TAB = Tableur(nom = filename)
            rows = list()
            for i in TAB.rechercheValeur():
                rows.append(i)
            if len(rows) != 0:
                err = 0
                # print(rows[0].keys())
                for champ in champs :
                    if champ not in rows[0].keys():
                        err = 1
                if err == 0:
                    newName = filename.split('/')[-1].replace('.xlsx', '')
                    newName = self.creatInvDB(newName)
                    
                    for row in rows:
                        
                        
                        print()
                        data = {'id' : str(uuid.uuid4()),
                                'stock' : str(row['stock']),
                                'refOuv' : str(row['id']),
                                'refInv' : newName }
                        print(data)
                        req.insert('inventaire', data)
                  
                else :
                    print('fail')
        
        
        self.close()
        
        
    def expVente(self, nom, ouvrir):
        

        today = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nom = 'export-'+nom+"-"+today



        if ouvrir == 1:
            compPath = filedialog.asksaveasfilename(
                title="Enregistrer sous",
                initialdir='fichiers',
                initialfile=nom + ".xlsx",
                defaultextension=".xlsx",
                filetypes = [("xlsx", '*.xlsx')]
                )
        else :
            compPath = 'sauvegardes/{}.xlsx'.format(nom)
            
        if compPath != '':
    
            filename= nom + '.xlsx'
            print(filename)
            filePath = compPath.replace(filename, '')
            print(filePath)
            
    
            extract =req.selectAll('vente')
    
    
            if extract != []:
                rows = list()
                for elm in extract:
                    print(elm)
                    print()
                    
                    ouvs = req.select('ouvrage', {'id' : elm['refOuv']})
                    if ouvs == []:
                        ouvs = [{'id' : elm['refOuv'],
                               'ISBN' : '',
                               'Title' : '',
                               'Authors' : '',
                               'Publisher' : '',
                               'Years' : '',
                               'Language' : '',
                               'prix' : ''}]
                    for ouv in ouvs:
                        ouv['quantite'] = elm['quantite']
                        ouv['date'] = elm['date']
                        rows.append(ouv)
    
    
                    
                if rows != []:
                    keys = list(rows[0].keys())
                    TAB = Tableur(nom = filename,
                                  path = filePath,
                                  nouv = keys)
        
                    for row in rows:
                        print(row)
                        TAB.ajoutLigne(row)
                    
                    TAB.save()
    
            else :
                dico = {'id' : '',
                        'ISBN' : '',
                        'Title' : '',
                        'Authors' : '',
                        'Publisher' : '',
                        'Years' : '',
                        'Language' : '',
                        'prix' : '',
                        'quantite' : '',
                        'date' : ''}
                rows = [dico]
                keys = list(dico.keys())
                TAB = Tableur(nom = filename,
                              path = filePath,
                              nouv = keys)
    
                for row in rows:
                    print(row)
                    TAB.ajoutLigne(row)
                TAB.save()
    
    
            if ouvrir == 1:
                sp.Popen((self.tabSoft , filePath + filename))
                    
            




    def expPret(self, nom, ouvrir, retard = 0):
        

        today = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nom = 'export-'+nom+"-"+today



        if ouvrir == 1:
            compPath = filedialog.asksaveasfilename(
                title="Enregistrer sous",
                initialdir='fichiers',
                initialfile=nom + ".xlsx",
                defaultextension=".xlsx",
                filetypes = [("xlsx", '*.xlsx')]
                )
        else :
            compPath = 'sauvegardes/{}.xlsx'.format(nom)
            
            
        if compPath != '':

            filename= nom + '.xlsx'
            print(filename)
            filePath = compPath.replace(filename, '')
            print(filePath)
            
    
            extract =req.selectAll('pret')
    
    
            if extract != []:
                rows = list()
                for elm in extract:
                    print(elm)
                    print()
                    
                    ouvs = req.select('ouvrage', {'id' : elm['refOuv']})
                    if ouvs == []:
                        ouvs = [{'id' : elm['refOuv'],
                               'ISBN' : '',
                               'Title' : '',
                               'Authors' : '',
                               'Publisher' : '',
                               'Years' : '',
                               'Language' : '',
                               'prix' : ''}]
                        
                    emps = req.select('emprunteur', {'id' : elm['refEmprunteur']})
                    if emps == []:
                        emps = [{
                            'nom' : '',
                            'prenom' : '',
                            'code' : '',
                            'contact' : '',
                            'aJour' : ''
                            }]
                    else :
                        del emps[0]['id']
    
    
                    
                    for ouv in ouvs:
                        ouv = {**ouv, **emps[0]}
                        ouv['quantite'] = elm['quantite']
                        del elm['id']
                        ouv = {**ouv, **elm}
                        

                        if retard == 1 :
                            date = datetime.datetime.fromisoformat(ouv['dateRet'])
                            today = datetime.datetime.today()
                            if date < today :
                                rows.append(ouv)
                        else :
                            rows.append(ouv)
    
    
                    
                if rows != []:
                    keys = list(rows[0].keys())
                    TAB = Tableur(nom = filename,
                                  path = filePath,
                                  nouv = keys)
        
                    for row in rows:
                        print(row)
                        TAB.ajoutLigne(row)
                    
                    TAB.save()
    
            else :
                dico = {'id' : '',
                        'ISBN' : '',
                        'Title' : '',
                        'Authors' : '',
                        'Publisher' : '',
                        'Years' : '',
                        'Language' : '',
                        'prix' : '',
                        'quantite' : '',
                        'date' : ''}
                rows = [dico]
                keys = list(dico.keys())
                TAB = Tableur(nom = filename,
                              path = filePath,
                              nouv = keys)
    
                for row in rows:
                    print(row)
                    TAB.ajoutLigne(row)
                TAB.save()
    
    
            if ouvrir == 1:
                sp.Popen((self.tabSoft , filePath + filename))




    def expTable(self, nom, ouvrir, nomTable):
        

        today = datetime.datetime.today().strftime('%Y-%m-%d_%H-%M-%S')
        nom = 'export-'+nom+"-"+today



        if ouvrir == 1:
            compPath = filedialog.asksaveasfilename(
                title="Enregistrer sous",
                initialdir='fichiers',
                initialfile=nom + ".xlsx",
                defaultextension=".xlsx",
                filetypes = [("xlsx", '*.xlsx')]
                )
        else :
            compPath = 'sauvegardes/{}.xlsx'.format(nom)
        
        if compPath != '':
        
            filename= nom + '.xlsx'
            print(filename)
            filePath = compPath.replace(filename, '')
            print(filePath)
            
    
            extract =req.selectAll(nomTable)
            if extract != []:
            
                keys = list(extract[0].keys())
                TAB = Tableur(nom = filename,
                              path = filePath,
                              nouv = keys)
        
        
                for row in extract:
                    print(row)
                    TAB.ajoutLigne(row)
                TAB.save()
        
        
                if ouvrir == 1:
                    sp.Popen((self.tabSoft , filePath + filename))
    

