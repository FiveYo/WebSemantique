import rdflib
#On récupère du json de mathieu, qui contiendra plusieurs adresses url.  
#On génère un graph pour chaque adresse url.
#Pour chaque graph on fait l'intersection avec GraphGeneral
#On envoie chaque graph à milly
#646 pour ascii
if __name__ == "__main__":

    gra = rdflib.Graph()
    #gra.parse("http://www.w3.org/People/Berners-Lee/card") 
    gra.parse("http://dbpedia.org/resource/Cat")
    gra.parse("http://dbpedia.org/resource/Dog")
    gra.parse("http://dbpedia.org/resource/Computer")
    gra.parse("http://dbpedia.org/resource/Chair")
    gra.parse("http://dbpedia.org/resource/Milk")
    gra.parse("http://dbpedia.org/resource/Electricity")
    gra.parse("http://dbpedia.org/resource/Desk")
    gra.parse("http://dbpedia.org/resource/Sister")
    gra.parse("http://dbpedia.org/resource/Country")


    #gra.parse("OutputTest.txt",format="n3") 
    #owl:sameAs à la place de "=" 

    print("graph has %s statements." % len(gra))
    # prints the number of statements in gra

    ser = gra.serialize(format='n3')

    text_file = open("GraphEpurer.txt", "w")

    text_file.write( ser.decode("646", "ignore") )

    text_file.close() 
