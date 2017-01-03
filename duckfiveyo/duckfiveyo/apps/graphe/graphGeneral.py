import rdflib
#On récupère du json de mathieu, qui contiendra plusieurs adresses url.  
#On génère un graph pour chaque adresse url.
#Pour chaque graph on fait l'intersection avec GraphGeneral
#On envoie chaque graph à milly
#646 pour ascii
if __name__ == "__main__":

    gra = rdflib.Graph()
    #gra.parse("http://www.w3.org/People/Berners-Lee/card") 
    gra.parse("http://dbpedia.org/resource/Musique")
    gra.parse("http://dbpedia.org/resource/Cover")
    gra.parse("http://dbpedia.org/resource/Album")
    gra.parse("http://dbpedia.org/resource/Partition")
    gra.parse("http://dbpedia.org/resource/Song")
    gra.parse("http://dbpedia.org/resource/Instrumental")
    gra.parse("http://dbpedia.org/resource/Composition")
    gra.parse("http://dbpedia.org/resource/Guest_appearance")
    gra.parse("http://dbpedia.org/resource/Artist")
    gra.parse("http://dbpedia.org/resource/Guitar")
    gra.parse("http://dbpedia.org/resource/Piano")
    gra.parse("http://dbpedia.org/resource/Drum_kit")
    gra.parse("http://dbpedia.org/resource/Saxophone")
    gra.parse("http://dbpedia.org/resource/Violin")
    gra.parse("http://dbpedia.org/resource/Bass_guitar")
    gra.parse("http://dbpedia.org/resource/Flute")
    gra.parse("http://dbpedia.org/resource/Trumpet")
    gra.parse("http://dbpedia.org/resource/Clarinet")
    gra.parse("http://dbpedia.org/resource/Keyboard_instrument")
    gra.parse("http://dbpedia.org/resource/Cello")
    gra.parse("http://dbpedia.org/resource/Bagpipes")
    gra.parse("http://dbpedia.org/resource/Human_voice")
    gra.parse("http://dbpedia.org/resource/Ukulele")
    gra.parse("http://dbpedia.org/resource/Harp")
    gra.parse("http://dbpedia.org/resource/Xylophone")
    gra.parse("http://dbpedia.org/resource/Harmonica")

    #gra.parse("OutputTest.txt",format="n3") 
    #owl:sameAs à la place de "=" 

    print("graph has %s statements." % len(gra))
    # prints the number of statements in gra

    ser = gra.serialize(format='n3')

    text_file = open("GraphGeneral.txt", "w")

    text_file.write( ser.decode("646", "ignore") )

    text_file.close() 
