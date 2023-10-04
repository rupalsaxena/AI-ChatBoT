from rdflib.namespace import Namespace, RDF, RDFS, XSD
from rdflib.term import URIRef, Literal
import rdflib



def load_graphs():
    graph = rdflib.Graph()
    print("Please wait while graph is loading ...")
    graph.parse('./data/14_graph.nt', format="turtle")
    print("Graph loaded")
    return graph