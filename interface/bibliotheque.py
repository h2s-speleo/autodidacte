#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Dec  7 23:13:44 2020

@author: j
"""
import tkinter as tk
# from tkinter import ttk
# from interface.formulaire import recForm, modForm
import req
from interface.formulaire import invForm
from interface.emprunteur import emprunteur
from interface.recap import recap
import uuid
import datetime
from dateutil.relativedelta import relativedelta





        


class bibli():
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
        self.core.onglet.add(self.Frame, text='BIBLIOTHEQUE')
        
        self.membreBut = tk.Button(
                self.Frame,
                text = "MEMBRE",
                command = self.membreButFonc)
        self.membreBut.grid(row = 0 ,column = 0,padx = 5, pady = 5)
        
        self.pretBut = tk.Button(
            self.Frame,
            text = "PRET",
            command = lambda sens = 'sortie' : self.pretButFonc(sens))
        self.pretBut.grid(row = 1 ,column = 0,padx = 5, pady = 5)
        
        self.retBut = tk.Button(
            self.Frame,
            text = "RETOUR",
            command = lambda sens = 'retour' : self.pretButFonc(sens))
        self.retBut.grid(row = 2 ,column = 0,padx = 5, pady = 5)
        
    
        
    def pretButFonc(self, sens ):
        print(sens)
        ouvrages = list()
        membre = self.membreButFonc()
        retards = self.retard(membre['id'])
        if retards != 0 or sens == 'retour' :
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
                    test = req.select("ouvrage", ret)
                    if test == []:
                        ret['id'] = str(uuid.uuid4())
                        req.insert("ouvrage", ret)
                    if ret['prix'] != 'B' :
                        newtext = "TITRE : {}\nAUTEUR  : {}\nEDITION : {}\nISBN : {}".format(
                            ret['Title'], ret['Authors'],ret['Publisher'],ret['ISBN'])
                        errtext = "Attention, cet ouvrage ne fait pas partie de la bibliotheque.\
                            \nil n'est pas pris en compte dans la pret\n\n" + newtext
                        tk.messagebox.showerror("PRET NON AUTORISE", errtext)
                    else :
                        ouvrages.append(ret)
                        
            if ouvrages != [] :
                if sens == 'sortie':
                    self.sortie(ouvrages, membre)
                    recap(self.core, membre, ouvrages)
                if sens == 'retour' :
                    self.retour(ouvrages, membre)
                    recap(self.core, membre)
                    
          
                
                
                
                
    def retour(self, ouvrages, membre):

        for ouv  in ouvrages:
            row = req.select('stock', {'refOuv' : ouv['id']} )
            if row == []:
                req.insert("stock", {'id' : str(uuid.uuid4()),
                                      'stock' : '1',
                                      'refOuv' : ouv['id']})
            else :
                nombre = int(row[0]['stock'])
                if nombre <= 0 :
                    nombre = 1
                elif nombre > 0:
                    nombre = nombre +1
                req.SQLupdate('stock', {'stock' : str(nombre)}, {'refOuv' : ouv['id']})
            newDico = {'refEmprunteur' : membre['id'],
                        'refOuv' : ouv['id']}
            test = req.select('pret', newDico)
            if test != []:
                req.SQLdelet('pret', test[0])
            
    def sortie(self, ouvrages, membre):
        today = datetime.datetime.today()
        dateRet = (today + relativedelta(months=+1)).strftime('%Y-%m-%d')
        today = today.strftime('%Y-%m-%d')
        for ouv  in ouvrages:
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
            newDico = {'id' : str(uuid.uuid4()),
                        'datePret' : today,
                        'dateRet' : dateRet,
                        'quantite' : '1',
                        'refEmprunteur' : membre['id'],
                        'refOuv' : ouv['id']
                        }
            req.insert('pret', newDico)
            

        
    def retard(self, ID):

        print(ID)
        
        valWidj = retard(self.core, ID)
        valid = valWidj.valid
        del valWidj
        print(valid)
        # si valid == 1 continuer le pret
        return valid
    
        
    def membreButFonc(self):
        self.emp = emprunteur(self.core)
        ret = self.emp.activeEmp
        del self.emp
        if ret != None:
            test = req.select('emprunteur', {'id' : ret['id']})
            if test == []:
                ret['id'] = str(uuid.uuid4())
                req.insert('emprunteur', ret)
            else :
                ID = ret['id']
                del ret['id']
                same = self.compDic(test[0], ret)
                if same == 1 :
                    req.SQLupdate('emprunteur', ret, {'id' : ID})
                    ret['id'] = ID
                else :
                    ask= question(self.core, test[0], ret)
                    rep = ask.rep
                    del ask
                    if rep == 'M':
                        req.SQLupdate('emprunteur', ret, {'id' : ID})
                        ret['id'] = ID
                    if rep == 'C':
                        ID = str(uuid.uuid4())
                        ret['id'] = ID
                        req.insert('emprunteur', ret)

        return ret
    
    def compDic(self, oldDico, newDico):
        err = 1
        Champs = ['nom', 'prenom', 'code']
        for champ in Champs:
            if oldDico[champ] != newDico[champ]:
                err = 0
        return err
            
class question():
    def __init__(self, core, oldDico, newDico):
        self.rep = 0
        self.core = core
        same = self.compDic(oldDico, newDico)
        if same == 1 :
            tk.messagebox.showerror(
                "INFO SIMILAIRES", 
                "impossible de créer deux utilisateurs avec les mêmes informations"
                )
        else :
            self.top = tk.Toplevel()
            self.top.bind('<Escape>', self.close)
            self.top.title("SMODIFIER OU CREER")
            self.topFrame = tk.Frame(self.top, width=800, height=400)
            self.top.geometry("800x500+0+0")
            text = " voulez vous modifier cet utilisateur :\n\n"
            text += self.makeText(oldDico)
            text += " \nen : \n\n\n"
            text += self.makeText(newDico)
            text += " \nou en créer un nouveau ?"
            
            tk.Label(
                self.topFrame ,
                text=text,
                wraplength = 700).grid(row = 0 ,column = 0,padx = 5, pady = 5)
            
            self.modBut = tk.Button(
                self.topFrame,
                text = 'MODIFIER LE MEMBRE',
                command = self.modButFonc)
            self.modBut.grid(row = 1 ,column = 0,padx = 5, pady = 5)
            
            self.creBut = tk.Button(
                self.topFrame,
                text = 'CREER UN NOUVEAU MEMBRE',
                command = self.creButFonc)
            self.creBut.grid(row = 2 ,column = 0,padx = 5, pady = 5)
            
            self.topFrame.grid()
            self.core.root.wait_window(self.top)
        
    def compDic(self, oldDico, newDico):
        err = 1
        Champs = ['nom', 'prenom', 'code']
        for champ in Champs:
            if oldDico[champ] != newDico[champ]:
                err = 0
        return err
        
    def modButFonc(self):
        self.rep = 'M'
        self.close()
        
    
    
    def creButFonc(self):
        self.rep = 'C'
        self.close()
        
        
    def makeText(self, dico):
        text = ''
        for key, value in dico.items():
            if key not in ['id', 'aJour']:
                text += '{} : {}\n'.format(key, value)
        text += '\n\n\n'
        return text
    
    def close(self, event = None):
        self.top.destroy()
        
    
        
        
class retard():
    def __init__(self, core, ID):
        self.valid = 1
        self.core = core
        # self.ID = ID
        
        
        self.liste = list()

        rows = req.select('pret', {'refEmprunteur' : ID})
        self.prets = rows
        if rows != []:
            for row in rows:
                # print(row['dateRet'])
                date = datetime.datetime.fromisoformat(row['dateRet'])
                today = datetime.datetime.today()
                if date < today :
                    self.valid = 0

                    ouvs = req.select('ouvrage', {'id' : row['id']})
                    
                    if ouvs == []:
                        dico = {'dateRet' : row['dateRet'],
                                'Title' : 'INCONNU',
                                'Authors' : '',
                                'Publisher' : '',
                                'ISBN' : ''}
                    else :
                        dico = {'dateRet' : row['dateRet']}
                        for ouv in ouvs:
                            for key, value in ouv.items():
                            
                                
                                dico[key] = value
                    self.liste.append(dico)
                    
        if self.valid == 0:
            
            self.top = tk.Toplevel()
            self.top.bind('<Escape>', self.close)
            self.top.title("RETARD")
            self.topFrame = tk.Frame(self.top, width=800, height=400)
            self.top.geometry("800x700+0+0")
            

            text = str()
            for row in self.liste:
                newtext = "TITRE : {}\nAUTEUR  : {}\nEDITION : {}\nISBN : {}".format(
                    row['Title'], row['Authors'],row['Publisher'],row['ISBN'])
                newtext = newtext + "\n\nDATE DE RETOUR : {}\n\n\n".format(row['dateRet'])
                text = text + newtext

            tk.Label(
                self.topFrame ,
                text="CE MEMBRE A DES PRETS EN RETARD").grid(
                    row = 0 ,column = 0,padx = 5, pady = 5
                    )
            
            self.OKdBut = tk.Button(
                self.topFrame,
                text = 'IGNORER',
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
        self.valid = 0
        self.close()
        
    def close(self, event = None):
        self.top.destroy()
        
    
    
        
        

        