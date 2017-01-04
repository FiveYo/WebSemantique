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
    return listresult
        
def percentage(part, whole):
    if whole ==0:
        return 0
    else :
        return 100 * float(part)/float(whole)
    
    
def routineMatrice(dictGraphe,parametreQueryList):
    listeGraphe=list(dictGraphe.values())
    listeUrl = list(dictGraphe.keys())
    dictMatrice = {}
    for itemQuery in parametreQueryList :
        
        listeTemp=grouperGraphes(itemQuery.upper(),listeGraphe)
        dictMatrice[itemQuery]=listeTemp
        
    return dictMatrice



        

# graphe1=graphRDF("http://www.azlyrics.com/lyrics/joeybada/waves.html")
# graphe2=graphRDF("http://www.lyricsmania.com/waves_lyrics_joey_badass.html")
# SVO1=getSVO(graphe1[0])
# SVO2=getSVO(graphe2[0])
# InitItem,InitMatrice=initMatriceSim(graphe1,SVO1)
# result=createMatriceSimPredicat(InitMatrice,InitItem,SVO2)



        
        
    
            
    
    
    
    
