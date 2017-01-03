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