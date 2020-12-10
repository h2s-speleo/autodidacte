#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 22:35:47 2020

@author: j
"""
import sqlite3

# q = input('en poursuivant vaous aller créer une nouvelle base et supprimer tous les enregistremant. poursuivre ? (o / n)\n')
# if q == 'o':
    
conn = sqlite3.connect('base.db')
c = conn.cursor()
c.execute('''CREATE TABLE reff
              (ISBN text, Title text, Authors text, Publisher text, Year text, Language text)''')
c.execute('''CREATE TABLE ouvrage
              (id text, ISBN text, Title text, Authors text, Publisher text, Year text, Language text, prix text)''')
c.execute('''CREATE TABLE inventaire
              (id text, stock text, refOuv text, refInv text)''')
c.execute('''CREATE TABLE listInvent
              (id text, date text, nom text)''')
c.execute('''CREATE TABLE stock
              (id text, stock text,  refOuv text)''')
c.execute('''CREATE TABLE vente
              (id text, date text, quantite text, refOuv text)''')
c.execute('''CREATE TABLE pret
              (id text, datePret text, dateRet text, quantite text, refEmprunteur text,  refOuv text)''')
c.execute('''CREATE TABLE emprunteur
              (id text, nom text, prenom text, code text, contact text, aJour text)''')





conn.commit()

conn.close()