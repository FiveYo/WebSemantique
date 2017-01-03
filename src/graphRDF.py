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



#####################################################################GRAPHE####################################################################################################
def graphRDF(donneeEntree):
    listeGraph = []
    #for data in donneeEntree:
    gra = Graph()
    #result = gra.parse(data["URI"])
    result = gra.parse(donneeEntree)
    listeGraph.append(gra)
    return listeGraph 

def graphRDFVrai():
    listeGraph = []
    #TODO récupérer GraphGeneral et ne garder que ce qui est commun aux deux
    graphGeneral = Graph()
        # Create an identifier to use as the subject for Donna.
    donna = BNode()
    rick = BNode()

    # Add triples using store's add method.
    graphGeneral.add( (donna, RDF.type, FOAF.Person) )
    graphGeneral.add( (donna, FOAF.nick, Literal("donna", lang="foo")) )
    graphGeneral.add( (donna, FOAF.name, Literal("Donna Fales")) )
    graphGeneral.add( (donna, FOAF.mbox, URIRef("mailto:donna@example.org")) )
    graphGeneral.add( (rick, RDF.type, FOAF.Person) )
    graphGeneral.add( (rick, FOAF.nick, Literal("rick", lang="foo")) )
    graphGeneral.add( (rick, FOAF.name, Literal("Rick Carter")) )
    graphGeneral.add( (rick, FOAF.mbox, URIRef("mailto:rick@example.org")) )
    print(graphGeneral)

    graphGeneral.bind("dc", DC)
    graphGeneral.bind("foaf", FOAF)

    
    ##for data in donneeEntree:
    graInter = Graph()
    gra2 = Graph()
    result = gra2.parse("http://www.w3.org/People/Berners-Lee/card")

    ##result = gra.parse(data["URI"])
    for s, p, o in graphGeneral:
        graInter += gra2.triples( (None, p, None) )
    ##listeGraph.append(graInter)

    text_file = open("OutputTest.txt", "w")

    text_file.write( (graInter.serialize(format='n3')).decode("utf-8") )

    text_file.close()
     



#TODO POST TRAITEMENT SUJET VERBE OBJET OK BOF
#TODO POST TRAITEMENT SVO OK BOF
#TODO DICTIONNAIRE [album, artiste,...] OK BOF 

        
        
        
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
    listeGraphe=dictGraphe.values()
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
    dictMatrice = {}
    for itemQuery in parametreQueryList :
        matriceCritere = searchByCritere(result,itemQuery,precision)
        listeTemp=grouperGraphes(matriceCritere,precision)
        for items in range(len(listeTemp)):
            dictMatrice[itemQuery]=foundKeybyValue(dictGraphe,item)
    return dictMatrice


def foundKeybyValue(dict,value):
    for key,values in dict.items():
        if values == value:
            return key
        

# graphe1=graphRDF("http://www.azlyrics.com/lyrics/joeybada/waves.html")
# graphe2=graphRDF("http://www.lyricsmania.com/waves_lyrics_joey_badass.html")
# SVO1=getSVO(graphe1[0])
# SVO2=getSVO(graphe2[0])
# InitItem,InitMatrice=initMatriceSim(graphe1,SVO1)
# result=createMatriceSimPredicat(InitMatrice,InitItem,SVO2)


###############################################URL#########################################

# Pour utiliser tu fait 
# routineQuery(cequetuveuxchercher)
def createUrl(parametres):
    #genere l'url de google api en fonction des paramètre
    keyApi= 'AIzaSyDG6Nig_usu4seBML0F2Gn9eC58KeRSIW4'
    Cx = '011588310783855289769:6ld0iqjum24'
    Url = 'https://www.googleapis.com/customsearch/v1?key=AIzaSyDG6Nig_usu4seBML0F2Gn9eC58KeRSIW4&cx=011588310783855289769:6ld0iqjum24&q='
    newListParam = parametres.split(' ')
    for item in newListParam :
        Url = Url + item + "+"
    Url = Url[:-1]
    return Url
    
def recupJsonText(Url):
    #Recupere via une url le code Json
    st=time.time()
    page = requests.get(Url)
    jsonFile= json.loads(page.content.decode("utf-8"))
    print("CA A PRIS 2  : " ,(time.time()-st))
    return jsonFile

def recupUrlDataVIew (jsonFile):
    #TODO
    #Recupere les donnes clés (artiste ....) 
    
    return 0 
    
def recupUrlText(jsonFile):
    #Recupere l'Url via le code Json
    listeUrl=[]
    listeText = []
    DictItem = jsonFile["items"]
    for itemsIndex in range (len(DictItem)):
        listeUrl.append(DictItem[itemsIndex]["link"])
        listeText.append(DictItem[itemsIndex]["snippet"])
        
    return(listeUrl,listeText)
        

def recupHtmlText(Url):
    #AVec l'url du code Json, on recupere le text du site via Alchemy
    AlchemyObject = AlchemyAPI()
    response = AlchemyObject.text('url', Url)
    text= response["text"]
    if len(text.split(" ")) > 150 :
        text=text[:150]
    return response,text
    
    
def routineQuery(requete):
    
    liste_item_musique  = ["album","cover","partition"]#,"tablature","Unplugged","single","live","Acoustic"]
    st = time.time()
    urlGoogleApiList= []
    urlGoogleApiList.append(createUrl(requete))
    #On regarde si les éléments du dico sont dans la requète
    for item in liste_item_musique:
        if item not in requete:
            urlGoogleApiList.append(createUrl(requete+" "+item))
        else :
            liste_item_musique.remove(item)
            
    dico_query={}
    dico_error={}
    dico_view={}
    listeTemp=liste_item_musique[:]
    listeTemp.append('requete basique')
    #ON range le dictionnaire par nom d'item 
    #on a deux clés la première c'est le nom de la requète : REquète basique ( sans ajout d'item de la liste_item_basique) , Album, cover, partition....
    #la seconde clé c'est L'url qu'on aura trouvé via le parsage du Json 
    #et la value ce sera le text 
    #pour les Url à pb on va les save dans un dico_error et qu'on va refaire tourner plus tard 
    for item in listeTemp:
        for index in range (len(urlGoogleApiList)):
            jsonFile = recupJsonText(urlGoogleApiList[index])
            listTempUrl,listTempText = recupUrlText(jsonFile)
            for indexUrl in range (len(listTempUrl)):
                urlTemp = listTempUrl[indexUrl]
                txtTemp = listTempText[indexUrl]
                
                try : 
                    textTemp = recupHtmlText(urlTemp)[1]
                except KeyError :
                    print("On a ete deco du serv rip")
                    print("Url qui pose problème : ",urlTemp)
                    print("On tente de la relancer ....")
                    try : 
                        textTemp = recupHtmlText(urlTemp)[1]
                    except  KeyError : 
                        print("Nouvelle Erreur WTF ") 
                        dico_error[item][urlTemp]="Error"
                    print("Url OK ")
                    
                dico_view[urlTemp]=txtTemp
                dico_query[urlTemp]=textTemp
    print("CA A PRIS : " ,(time.time()-st))
    return dico_query,dico_view
            
        
        
    
            
    
    
    
    
