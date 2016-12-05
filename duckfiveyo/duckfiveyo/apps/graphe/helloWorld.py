import rdflib

if __name__ == "__main__":
    print("hello world")

    gra = rdflib.Graph()
    #result = gra.parse("http://www.w3.org/People/Berners-Lee/card") utf-8
    result = gra.parse("http://dbpedia.org/resource/Schroter") 
    #gra.load('https://fr.wikipedia.org/wiki/Vin') nope
    #owl:sameAs à la place de "=" 

    print("graph has %s statements." % len(gra))
    # prints graph has 79 statements.

    for subj, pred, obj in gra:
        if (subj, pred, obj) not in gra:
            raise Exception("It better be!")

    ser = gra.serialize(format='n3')

    text_file = open("Output1.txt", "w")

    text_file.write( (gra.serialize(format='n3')).decode("646", "ignore") )

    text_file.close()
