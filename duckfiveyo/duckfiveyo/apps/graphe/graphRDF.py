from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

#{url1: [(triplet RDF 1), (triplet RDF 2), ...],
#  url2: [(triplet RDF 1), (triplet RDF 2), ...],
#  ...
# }
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
        else:
            for t in value:
                print(t)
                gra.add( (BNode(t[0]),BNode(t[1]),Literal(t[2])) )
            graInter = Graph()
            for s, p, o in graGeneral:
                graInter += gra.triples( (None, p, None) )

            graphUrl[str(key)] = gra
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
     
