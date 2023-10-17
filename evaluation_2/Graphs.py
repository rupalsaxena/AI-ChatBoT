import rdflib
from rdflib import URIRef

class Graphs:
    def __init__(self):
        self.load_graphs()
    
    def load_graphs(self):
        self.graph = rdflib.Graph()
        print("Please wait while graph is loading ...")
        self.graph.parse('data/14_graph.nt', format="turtle")
        print("Graph loaded")
    
    def get_graph(self):
        return self.graph
    
    def queryFactual(self, id, p):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/> 
        SELECT ?item WHERE {
            wd:%s wdt:%s ?element .
            ?element rdfs:label ?item
        }''' % (id, p)
        responses = self.graph.query(query)
        res_list = [str(result.item) for result in responses]
        return res_list
    
    def queryActor(self, id):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        SELECT DISTINCT ?item ?element WHERE {
            ?element wdt:P161 wd:%s.
            ?element rdfs:label ?item.
            FILTER((LANG(?item)) = "en")
            }
            LIMIT 10
        '''%(id)
        responses = self.graph.query(query)
        res_list = [str(result.item) for result in responses]
        return res_list
    
    def queryMoviesfromGenres(self, id):
        query = '''
        PREFIX wd: <http://www.wikidata.org/entity/>
        PREFIX wdt: <http://www.wikidata.org/prop/direct/>

        select distinct ?item ?element ?elementLabel where {
            ?element wdt:P136 wd:%s . 
            ?element rdfs:label ?elementLabel . 
            filter(lang(?elementLabel) = "en")
        } limit 10 
        '''%(id)
        responses = self.graph.query(query)
        res_list = [str(result.elementLabel) for result in responses]
        return res_list


if __name__=="__main__":
    g = Graphs()
    g.queryMultimedia("Q1033016")
    g.queryFactual("Q223596", "P162")