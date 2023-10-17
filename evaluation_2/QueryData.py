import csv
import rdflib
from rdflib import URIRef

def load_graphs():
    graph = rdflib.Graph()
    print("Please wait while graph is loading ...")
    graph.parse('data/14_graph.nt', format="turtle")
    print("Graph loaded")
    return graph

def getAllMovies(graph):
    return [ [str(s), str(lbl)] for s, lbl in graph.query('''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        
        SELECT ?movie ?lbl WHERE {
                ?movie wdt:P31 wd:Q11424 .
                ?movie rdfs:label ?lbl .
            }
        ''')]

def getAllAwards(graph):
    return [ [str(s), str(lbl)] for s, lbl in graph.query('''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        
        SELECT ?movie ?lbl WHERE {
                ?movie wdt:P31 wd:Q618779 .
                ?movie rdfs:label ?lbl .
            }
        ''')]

def getAllHumans(graph):
    return [ [str(s), str(lbl)] for s, lbl in graph.query('''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        
        SELECT ?human ?lbl WHERE {
                ?human wdt:P31 wd:Q5 .
                ?human rdfs:label ?lbl .
            }
        ''')]

def getAllGenres(graph):
    return [ [str(s), str(lbl)] for s, lbl in graph.query('''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        
        SELECT ?movie ?lbl WHERE {
                ?movie wdt:P31 wd:Q483394 .
                ?movie rdfs:label ?lbl .
            }
        ''')]

def getAllCharacters(graph):
    return [ [str(s), str(lbl)] for s, lbl in graph.query('''
        PREFIX wd: <http://www.wikidata.org/entity/> 
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        
        SELECT ?movie ?lbl WHERE {
                ?movie wdt:P31 wd:Q95074 .
                ?movie rdfs:label ?lbl .
            }
        ''')]

if __name__=="__main__":
    graph = load_graphs()
    movies = getAllMovies(graph)
    with open('data/all_movies.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(["ids", "names"])
        write.writerows(movies)

    humans = getAllHumans(graph)
    with open('data/all_humans.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(["ids", "names"])
        write.writerows(humans)
    
    genres = getAllGenres(graph)
    with open('data/all_genres.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(["ids", "names"])
        write.writerows(genres)

    awards = getAllAwards(graph)
    with open('data/all_awards.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(["ids", "names"])
        write.writerows(awards)

    characters = getAllCharacters(graph)
    with open('data/all_character.csv', 'w') as f:
        write = csv.writer(f)
        write.writerow(["ids", "names"])
        write.writerows(characters)

    
