from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

# {'http://dbpedia.org/resource/Partition': [{'p': {'value': 'http://dbpedia.org/ontology/wikiPageExternalLink', 'type': 'uri'},
#  'o': {'value': 'https://urresearch.rochester.edu/viewContributorPage.action?personNameId=664', 'type': 'uri'}, 
#  's': {'value': 'http://dbpedia.org/resource/Wolfgang_Amadeus_Mozart', 'type': 'uri'}},
#   {'p': {'value': 'http://www.w3.org/2002/07/owl#sameAs', 'type': 'uri'}, 
#   'o': {'value': 'http://eu.dbpedia.org/resource/Wolfgang_Amadeus_Mozart', 'type': 'uri'}, 
#   's': {'value': 'http://dbpedia.org/resource/Wolfgang_Amadeus_Mozart', 'type': 'uri'}}]}

def graphRDF(donneeEntree):
    graphUrl = {}
    graGeneral = Graph()
    graGeneral.parse("GraphGeneral.txt",format="n3") 
    for key,value in donneeEntree.items():
        gra = Graph()
        #result = gra.parse(data["URI"])
        try:
            result = gra.parse(key) # (traitement pour enlever les "=")
        except Exception:
            next
        # else:
        #     for t in value:
        #         a = b = c = ""
        #         for k,v in t.items():
        #             if k=='s':
        #                 if v['type']=='uri':
        #                     a = URIRef(v['value'])
        #                 elif v['type']=='literal':
        #                     a = Literal(v['value'])
        #                 elif v['type']=='uri':
        #                     a = BNode(v['value'])
        #             elif k=='p':
        #                 if v['type']=='uri':
        #                     b = URIRef(v['value'])
        #                 elif v['type']=='literal':
        #                     b = Literal(v['value'])
        #                 elif v['type']=='uri':
        #                     b = BNode(v['value'])
        #             elif k=='o':
        #                 if v['type']=='uri':
        #                     c = URIRef(v['value'])
        #                 elif v['type']=='literal':
        #                     c = Literal(v['value'])
        #                 elif v['type']=='uri':
        #                     c = BNode(v['value'])
        #         gra.add( (a,b,c) )
            graInter = Graph()
            for s, p, o in graGeneral:
                #print(str(p).split(":",1)[1]) 
                graInter += gra.triples( (None, p, None) )
                
            graFinal = Graph()
            graphEpurer = Graph()
            graphEpurer.parse("graphEpurer.txt",format="n3") 
            graFinal = graInter - graphEpurer
            graphUrl[str(key)] = graFinal   
    return graphUrl 

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
    #print(graphGeneral)

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
     
