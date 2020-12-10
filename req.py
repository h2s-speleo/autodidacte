#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 30 21:44:39 2020

@author: j
"""
import sqlite3
import uuid
from isbnlib import meta

def getInfoFromNet(isbn):
    """
    recherche sur le net les information correspondant a un ISBN

    Parameters
    ----------
    isbn : str
        numero isbn rechercher

    Returns
    -------
    info : dict
        information sur l'ouvrage.

    """
    SERVICE = ['bnf',
               'wiki',
               'openl',
               'goob']
    info = {'ISBN' : isbn,
            'Title' : None,
            'Authors' : None,
            'Publisher' : None,
            'Year' : None,
            'Language' : None}
    champ = list(info.keys())
    # champ.remove('ISBN')
    for serv in SERVICE :
        try : 
            data = meta(isbn, service= serv)
            for key, value in data.items():
                if value != str() and value != ['']:
                    if key in champ :
                        info[key] = value
                        champ.remove(key)              
            if len(champ) == 0:
                break
        except  :
            pass
    convInfo = dict()
    for key, value in info.items():
        convInfo[key] = convert(value)

    convInfo['id']= str(uuid.uuid4())
    convInfo['prix']= ''
    return convInfo

def convert(data):
    """
    converti les valeurs pour enregistrement dans sqlite

    Parameters
    ----------
    data : ?
        valeur a convertir.


    Returns
    -------
    Ndata : str
        valeurs converti.

    """
    Ndata = data
    if isinstance(data, str):
        Ndata = netoyageStr(data)
    elif isinstance(data, float) or isinstance(data, float):
        Ndata = str(data)
    elif isinstance(data, list):
        liste = list()
        for elm in data:
            elm = elm.replace(',', ' ')
            elm = netoyageStr(elm)
            liste.append(elm)
        Ndata = ', '.join(liste)
    else :
        raise AttributeError('type de donné non pris en charge :' + str(type(data)))
    return Ndata

def netoyageStr(elm):
    while True:
        if elm.startswith(' '):
            elm = elm[1:]
        else :
            break
    while True:
        if elm.endswith(' '):
            elm = elm[:-1]
        else :
            break
    elm = elm.replace("\n", ' ')
    elm = elm.replace("'", ' ')
    elm = elm.replace('"""', ' ')
    elm = elm.replace('"', ' ')
    elm = elm.replace('\\', ' ')
    elm = elm.replace(',', '')
    while '  ' in elm :
        elm = elm.replace('  ', ' ')
    return elm

def SQLvaleur(table, data):
    """
    retourne une expression SQL de type "'valeur1', 'valeur2', ..."

    Parameters
    ----------
    table : str
        nom de la table.
    data : dict
        dictionaire de type {'champ' : 'valeur'}.

    Returns
    -------
    req2 : str
        portion de requette SQL.

    """
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    listeChamp = list()
    for row in c.execute("PRAGMA table_info(" + table + ");"):
        listeChamp.append(row[1])
    values = list()
    for elm in listeChamp:
        values.append("'" + str(data[elm]) + "'")
    req2 = "(" + ",".join(values) +")"
    conn.close()
    return req2
    
def SQLand(condition):
    """
    retourne une expression SQL de type "champ = 'valeur' AND ..."

    Parameters
    ----------
    condition : dict
        dictionaire de type {'champ' : 'valeur recherchée'}.

    Returns
    -------
    req2 : str
        portion de requette SQL.

    """
    listReq = list()
    for key, value in condition.items():
        listReq.append(key+"='" + str(value) +"'")
    req2=' AND '.join(listReq)
    return req2

def SQLnomValeur(data):
    """
    retourne une expression SQL de type "champ = 'valeur' , ..."

    Parameters
    ----------
    data : dict
        dictionaire de type {'champ' : 'valeur'}.

    Returns
    -------
    req2 : str
        portion de requette SQL.

    """
    listReq = list()
    for key, value in data.items():
        listReq.append(key+"='" + str(value) +"'")
    req2=' , '.join(listReq)
    return req2

def insert(table, data):
    """
    créée une entité dans une table SQLite

    Parameters
    ----------
    table : str
        nom de la table à modifier.
    data : dict
        dictionaire de type {'champ' : 'valeur'}.

    Returns
    -------
    None.

    """
    req1 = "INSERT INTO " + table +" VALUES "
    req = req1 + SQLvaleur(table, data)
    print(req)
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute(req)
    conn.commit() 
    conn.close()
    
def selectAll(table):
    """
    

    Parameters
    ----------
    table : str
        nom de la table a requeter.

    Returns
    -------
    output : list
        Liste de dictionnaire extrait par la requette

    """
    req = 'SELECT * FROM ' + table
    print(req)
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    rep = list()
    for row in c.execute(req):
        rep.append(row)
    listeChamp = list()
    for row in c.execute("PRAGMA table_info(" + table + ");"):
        listeChamp.append(row[1])
    conn.close()
    output = list()
    for row in rep:
        dico = dict()
        for i in range(len(listeChamp)):
            dico[listeChamp[i]] = row[i]
        output.append(dico)
    return output
    
def select(table, condition):
    """
    

    Parameters
    ----------
    table : str
        nom de la table a requeter.
    condition : dict
        dictionaire de type {'champ' : 'valeur recherchée'}.

    Returns
    -------
    output : list
        Liste de dictionnaire extrait par la requette

    """
    req2=SQLand(condition)
    req = 'SELECT * FROM ' + table + ' WHERE ' + req2
    print(req)
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    rep = list()
    for row in c.execute(req):
        rep.append(row)
    listeChamp = list()
    for row in c.execute("PRAGMA table_info(" + table + ");"):
        listeChamp.append(row[1])
    conn.close()
    output = list()
    for row in rep:
        dico = dict()
        for i in range(len(listeChamp)):
            dico[listeChamp[i]] = row[i]
        output.append(dico)
    return output

def SQLupdate(table, data, condition):
    """
    met a jour les données dans la base SQL

    Parameters
    ----------
    table : str
        table a modifier.
    data : dict
        dictionnaire des données a modifier de type {'champ' : 'valeur'}
    condition : dict
        condition : dict
        dictionaire de type {'champ' : 'valeur recherchée'}.

    Returns
    -------
    None.

    """
    req = "UPDATE " + table + " SET " + SQLnomValeur(data)
    if condition != None :
        req = req  + " WHERE "+ SQLand(condition)
    print(req)
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute(req)
    conn.commit() 
    conn.close()
    
def SQLdelet(table, condition):
    """
    supprime les entité en fonction de la requette

    Parameters
    ----------
    table : str
        table a modifier.
    condition : dict
        condition : dict
        dictionaire de type {'champ' : 'valeur recherchée'}.

    Returns
    -------
    None.

    """
    req = "DELETE FROM " + table + " WHERE "+ SQLand(condition)
    print(req)
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute(req)
    conn.commit() 
    conn.close()
    
def deletAll(table):
    req = "DELETE FROM " + table 
    print(req)
    conn = sqlite3.connect('base.db')
    c = conn.cursor()
    c.execute(req)
    conn.commit() 
    conn.close()
    
if __name__ == '__main__':
    
    # req = "UPDATE ouvrage SET ISBN='9782251450162' , Title='Cyropédi' , Authors='Xénophon' , Publisher='les Belles lettres (Paris)' , Year='2019' , Language='fre' , prix='23.5' WHERE id='163dce16-5c06-4557-a598-09cbfde3af6a'"
    # conn = sqlite3.connect('base.db')
    # c = conn.cursor()
    # c.execute(req)
    # conn.commit() 
    # conn.close()
    
    

    for row in selectAll('vente'):
        print(row)
        print()
        
        
        
        
        
        
    
    
    
    # deletAll('emprunteur')
    
    # isbn = ['9782412045145',
    #         '9782251450124',
    #         '9782251450162',
    #         '9782251450131',
    #         '9782070531103',
    #         '9782070533336',
    #         '9782070531837']
    # for elm in isbn:
    #     try :
    #         info = getInfoFromNet(elm)
    #         print(info)
    #     except :
    #         pass
    
            
    #     print()
    #     insert('ouvrage', info)
    
    
    # info = {
    #     'id' : 'dfwwwbwdbwd',
    #     'datePret' : '2020-01-01',
    #     'dateRet' : '2020-02-01',
    #     'quantite' : '1',
    #     'refEmprunteur' : '2d8fdb17-bb6b-4775-bb57-62c08ae98a1f',
    #     'refOuv' : 'bb8e9273-d872-40c4-9ce8-bb1075b3677d'}
    # insert('pret', info)
        
    
    # # info = {'ISBN': '9782412045145', 'Title': 'Programmer en Python', 'Authors': ['Ramalho, Luciano', 'bibi'], 'Publisher': 'First interactive (Paris)', 'Year': '2019', 'Language': 'fre'}
    # insert('reff', info)
    
    # print()
    
    # for row in select('reff', {'Year' : '2019'}) :
    #     print()
    #     print(row)
        
    # SQLupdate('reff', {'Year' : '2019'}, {'ISBN': '9782412045145', 'Title': 'Programmer en Python'})
    # SQLdelet('ouvrage', {'ISBN': ''})
    
    # for row in select('reff', {'Year' : '2019'}) :
    #     print()
    #     print(row)
