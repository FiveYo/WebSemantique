from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

if __name__ == "__main__":

    def graphRDF(param):
        return blabla

    gra = Graph()
    gra2 = Graph()
    graInter = Graph()
    
    # Create an identifier to use as the subject for Donna.
    donna = BNode()
    rick = BNode()

    # Add triples using store's add method.
    gra.add( (donna, RDF.type, FOAF.Person) )
    gra.add( (donna, FOAF.nick, Literal("donna", lang="foo")) )
    gra.add( (donna, FOAF.name, Literal("Donna Fales")) )
    gra.add( (donna, FOAF.mbox, URIRef("mailto:donna@example.org")) )
    gra.add( (rick, RDF.type, FOAF.Person) )
    gra.add( (rick, FOAF.nick, Literal("rick", lang="foo")) )
    gra.add( (rick, FOAF.name, Literal("Rick Carter")) )
    gra.add( (rick, FOAF.mbox, URIRef("mailto:rick@example.org")) )

    gra2.add( (rick, RDF.type, FOAF.Person) )
    gra2.add( (rick, FOAF.nick, Literal("rick", lang="foo")) )
    gra2.add( (rick, FOAF.name, Literal("Rick Carter")) )
    gra2.add( (rick, FOAF.mbox, URIRef("mailto:rick@example.org")) )

    #permettra de mettre dans le graph d'intersection que ce qui nous interesse comme prédicat! HEAVEN
    #à parcourir pour chaque prédicat du GraphGeneral
    #gra c'est le graph généré pour chaque url de mathieu
    graInter += gra.triples( (None, FOAF.name, None) )
    graInter += gra.triples( (None, FOAF.nick, None) )
    graInter += gra.triples( (None, RDF.type, None) )

    # Iterate over triples in store and print them out.
    print("--- printing raw triples ---")
    for s, p, o in gra:
        print((s, p, o))

    # For each foaf:Person in the store print out its mbox property.
    print("--- printing mboxes ---")
    for person in gra.subjects(RDF.type, FOAF.Person):
        for mbox in gra.objects(person, FOAF.mbox):
            print(mbox)

    # Bind a few prefix, namespace pairs for more readable output
    gra.bind("dc", DC)
    gra.bind("foaf", FOAF)

    gra2.bind("dc", DC)
    gra2.bind("foaf", FOAF)

    print( gra.serialize(format='n3') )

    if ( None, FOAF.name, None ) in gra:
        print(None, FOAF.name, Literal("Donna Fales"))
        print("This graph knows that donna is a person")


    text_file = open("Output2.txt", "w")

    text_file.write( (graInter.serialize(format='n3')).decode("utf-8") )

    text_file.close()
