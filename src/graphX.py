from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
import numpy as np
from difflib import SequenceMatcher
from alchemyapi import AlchemyAPI
from lxml import html
import requests
import json
import re
import time
import urllib.request






#TODO POST TRAITEMENT SUJET VERBE OBJET OK BOF
#TODO POST TRAITEMENT SVO OK BOF
#TODO DICTIONNAIRE [album, artiste,...] OK BOF 

        
        
        
########################################################MATRICE SIMILARITE #########################################################

        
def initMatriceSim(graphe1,listItem1):
    longueurPred = len(listItem1)
    matrice=np.ones((1,longueurPred))
    return (listItem1,matrice)
        
    
    
def getItems(Graphe):
    listeVerbe=[]
    listeObjet=[]
    listeSujet=[]
    for s,p,o in Graphe:
        listeSujet.append(s)
        listeVerbe.append(p)
        listeObjet.append(o)
    return listeSujet,listeVerbe,listeObjet
        
def parsageItemUrl(Item):
    ItemTemp=Item
    uselessChars=['.htm','.html','?php','.com','www.','.net','.fr','.xhtml']
    keyChars=['album','lyrics','cover','single','tube']
    if isinstance(ItemTemp,URIRef) or isinstance(ItemTemp,Literal):
        #on vire les /, les . et les autres trucs (html, htm, php, www, com,net)
        # if '/' in Item :
            # for chars in keyChars:
            #     if chars in ItemTemp:
            #         ItemTemp= ItemTemp.split('/')[-2]+" "+ ItemTemp.split('/')[-1]
        if "." in ItemTemp:
            ItemTemp2=ItemTemp
            for chars in uselessChars:
                ItemTemp2 = ItemTemp2.replace(chars,"")
            ItemTemp = ItemTemp2 
        ItemTemp=ItemTemp.split('/')[-1]
    return ItemTemp
    
def getSVO(Graphe):
    listeSVO=[]
    for s,p,o in Graphe:
        sTemp=parsageItemUrl(s)
        pTemp=parsageItemUrl(p)
        oTemp=parsageItemUrl(o)
        strtemp = sTemp+" "+pTemp+" "+oTemp
        listeSVO.append(strtemp.upper())
        
    return listeSVO
        


    
def grouperGraphes(itemQuery,listeGraphe):
    NbGraph = len(listeGraphe)
    listresult=[]
    varTemp=0
    for indexgraph in range(NbGraph):
        SVOtemp = getSVO(listeGraphe[indexgraph])
        for items in SVOtemp:
            if itemQuery in items:
                listresult.append(indexgraph)
                break
            else : 
                temp=re.split(" |_|:|#", items)
                for item in temp:
                    result = jaccard(item,itemQuery)
                    if result < 2 :
                        listresult.append(indexgraph)
                        break

    return listresult
        
    
    
def routineMatrice(dictGraphe,parametreQueryList):
    listeGraphe=list(dictGraphe.values())
    listeUrl = list(dictGraphe.keys())
    dictMatrice = {}
    for itemQuery in parametreQueryList :
        
        listeTemp=grouperGraphes(itemQuery.upper(),listeGraphe)
        dictMatrice[itemQuery]=listeTemp
        
    return dictMatrice


def compte_lettre(mot):
    d = {}
    for c in mot:
        d[c] = d.get(c,0) + 1
    return d

def jaccard(mot1, mot2):
    d1 = compte_lettre(mot1)
    d2 = compte_lettre(mot2)
    suppression = {}
    for l in d1:
        c1 = d1[l]
        c2 = d2.get(l, 0)  # la lettre l n'appartient pas forcément au second mot
        if c2 != c1:
            suppression[l] = c2 - c1
    ajout = {}
    for l in d2:
        if l not in d1:
            c1 = 0
            c2 = d2[l]
            if c2 != c1:
                ajout[l] = c2 - c1
        else:
            # on a déjà compté les lettres présentes dans les deux mots
            # lors de la première boucle
            pass
    dist = sum(abs(x) for x in suppression.values()) + sum(abs(x) for x in ajout.values())
    return dist
        

# graphe1=graphRDF("http://www.azlyrics.com/lyrics/joeybada/waves.html")
# graphe2=graphRDF("http://www.lyricsmania.com/waves_lyrics_joey_badass.html")
# SVO1=getSVO(graphe1[0])
# SVO2=getSVO(graphe2[0])
# InitItem,InitMatrice=initMatriceSim(graphe1,SVO1)
# result=createMatriceSimPredicat(InitMatrice,InitItem,SVO2)



        
        
    
            
    
    
    
    
