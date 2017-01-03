

from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF
from difflib import SequenceMatcher

from lxml import html

import numpy as np

########################################################MATRICE SIMILARITE #########################################################
def includeMatrice(M1,M2):
    if M1.shape[0]>M2.shape[0] and M1.shape[1]>M2.shape[1]:
        raise Exception ("tu t'es planté de matrice ")
    elif M1.shape == M2.shape:
        return M2
    else :
        for M1ligne in range(M1.shape[0]):
            for M1colonne in range (M1.shape[1]):
                M2[M1ligne][M1colonne]=M1[M1ligne][M1colonne]
        return M2
        
def createMatriceSimPredicat(PrevMatrice,PrevListItem,itemNewGraph):
    #On initialise la matrice pour la 1ère fois avec les 2 premiers graphes à merger
    matrice=[]
    #on merge les deux listes
    listeItem = list(set(PrevListItem) | set(itemNewGraph))
    lenItem=len(listeItem)
    Temp=np.zeros(PrevMatrice.shape[0]+1,lenItem)
    matrice = includeMatrice(PrevMatrice,Temp)
    #Update la nouvelle ligne 
    for indexListeItem in range(lenItem):
        matrice[lenItem-1][indexListeItem]=1
    return(listeItem,matrice)
        
        
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
        listeSVO.append(sTemp+" "+pTemp+" "+oTemp)
    return listeSVO
        

def merge2liste(liste1,liste2):
    #C'est des liste de string hein cassez pas les couilles
    #liste 2 >= liste 1 
    lenl1=len(liste1)
    lenl2=len(liste2)
    listeCoeff=np.zeros(lenl2)
    if lenl1>lenl2:
        raise Exception("card(liste2) < card(liste1)")
    for indexl2 in range(lenl2):
        iteml2temp=liste2[indexl2]
        coefmax=0
        coefTemp=0
        for indexl1 in range(lenl1):
            iteml1temp=liste1[indexl1]
            coefTemp=SequenceMatcher(None,iteml1temp,iteml2temp).ratio()
            if coefTemp>coefmax:
                coefmax = coefTemp
        listeCoeff[indexl2]=coefmax
    return listeCoeff
    
def createMatriceSimPredicat(PrevMatrice,PrevListItem,itemNewGraph):
    #On initialise la matrice pour la 1ère fois avec les 2 premiers graphes à merger
    matrice=[]
    #on merge les deux listes
    listeItem = list(set(PrevListItem) | set(itemNewGraph))
    listCoeff = merge2liste(itemNewGraph,listeItem)
    lenItem=len(listeItem)
    lenNewItem=len(itemNewGraph)
    matrice=np.zeros((PrevMatrice.shape[0]+1,lenItem))
    matrice[:-1,:-lenNewItem]=PrevMatrice
    matrice[-1,:]=listCoeff
    return(listeItem,matrice)


def  searchByCritere(resultSim,parametreQuery,precision):
    #IMPORTANT : Le paramètre matrice est [SVO, Matrice]
    #IMPORTANT : la précision est un pourcentage
    #renvoie une matrice dont on a rogner les colones et on a pris seulement celles en rapport avec le critère
    SVOItem = resultSim[0]
    matriceSim = resultSim[1]
    listeIndex=[]
     #On cherche les index des colonnes qui ont les SVO qui correspondent au critère
    for indexItem in range(len(SVOItem)):
        coefTemp = SequenceMatcher(None,parametreQuery,SVOItem[indexItem]).ratio()
        if coefTemp>=precision:
            listeIndex.append(indexItem)
    #On créé une nouvelle matrice (Item,graphe) 
    #La matrice aura les même ordonnées ( tous les graphes ) 
    #mais en abscisse il y aura les SVO qui correspondent aux critères
    matriceCritere = np.zeros((matriceSim.shape[0],len(listeIndex)))
    for i in range(len(listeIndex)):
        #on récupere les colones qu'on veut de la grosse matrice de similarité
        matriceCritere[:,[i]]=matriceSim[:,[listeIndex[i]]]
    return matriceCritere
    
def grouperGraphes(matrice,precision):
    #IMPORTANT : la précision est un pourcentage 
    #IMPORTANT : doit être utilisé après avoir trié la matrice via searchByCritere
    listeGraphe=[]
    NbItem = matrice.shape[1]
    NbGraph = matrice.shape[0]
    for indexGraphs in range(NbGraph):
        coefSimTemp=matrice[indexGraphs:].sum(axis=1)
        if percentage(coefSimTemp,NbItem)>=precision :
            listeGraphe.append(indexGraphs)
    return listeGraphe
        
def percentage(part, whole):
  return 100 * float(part)/float(whole)
    
    
def routineMatrice(dictGraphe,parametreQueryList,precision):
    listeGraphe=dictGraphe.keys()
    initMatrice,Inititems = initMatriceSim(listeGraphe|[0],getSVO(listeGraphe[0]))
    matricePrevTemp = initMatrice
    itemsPrevTemp = initItems
    #Creation matrice similarité avec tout les graphes 
    for indexMatrice in range (1,len(listeGraphe)):
        itemSuivTemp = getSVO(listeGraphe[indexMatrice])
        itemsPrevTemp,matricePrevTemp = createMatriceSimPredicat(matricePrevTemp,itemsPrevTemp,itemSuivTemp)
    #Regroupement par rapport au critère(parametreQuery) et à la précision 
    result = [itemsPrevTemp,matricePrevTemp]
    #QUEL RESULTAT JE DOIS AVOIR ?
    listMatrice =[]
    listListGraph=[]
    for itemQuery in paramatereQuery :
        listMatrice.append(searchByCritere(result,itemQuery,precision))
        listeGraphe.append(grouperGraphes(matriceCritere,precision))
    return listMatrice,listListGraph

