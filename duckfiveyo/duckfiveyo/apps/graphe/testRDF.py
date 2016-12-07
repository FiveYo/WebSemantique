from rdflib import Graph, Literal, BNode, Namespace, RDF, URIRef
from rdflib.namespace import DC, FOAF

if __name__ == "__main__":

    gra = Graph()

    # Create an identifier to use as the subject for Donna.
    donna = BNode()

    # Add triples using store's add method.
    gra.add( (donna, RDF.type, FOAF.Person) )
    gra.add( (donna, FOAF.nick, Literal("donna", lang="foo")) )
    gra.add( (donna, FOAF.name, Literal("Donna Fales")) )
    gra.add( (donna, FOAF.mbox, URIRef("mailto:donna@example.org")) )

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

    print( gra.serialize(format='n3') )

    text_file = open("Output2.txt", "w")

    text_file.write( (gra.serialize(format='n3')).decode("utf-8") )

    text_file.close()
