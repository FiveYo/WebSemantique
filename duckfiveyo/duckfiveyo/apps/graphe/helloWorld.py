import rdflib
#On récupère du json de mathieu, qui contiendra plusieurs adresses url.  
#On génère un graph pour chaque adresse url.
#Pour chaque graph on fait l'intersection avec GraphGeneral
#On envoie chaque graph à milly
if __name__ == "__main__":

    gra = rdflib.Graph()
    gra2 = rdflib.Graph()
    #result1 = gra.parse("http://www.w3.org/People/Berners-Lee/card") #utf-8
    result2 = gra.parse("http://www.wimp.com/heart-covers-stairway-to-heaven/") #646 c'est ascii
    #gra.parse("OutputTest.txt",format="n3") 
    #owl:sameAs à la place de "=" 

    print("graph has %s statements." % len(gra))
    # prints the number of statements in gra

    for subj, pred, obj in gra:
        if (subj, pred, obj) not in gra:
            raise Exception("It better be!")

    ser = gra.serialize(format='n3')

    text_file = open("Output1.txt", "w")

    text_file.write( ser.decode("utf-8", "ignore") )

    text_file.close() 
