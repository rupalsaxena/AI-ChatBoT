from rdflib.namespace import Namespace, RDF, RDFS, XSD
from rdflib.term import URIRef, Literal
import rdflib


def load_graphs():
    graph = rdflib.Graph()
    print("Please wait while graph is loading ...")
    graph.parse('./data/14_graph.nt', format="turtle")
    print("Graph loaded")
    return graph

def check_q_type(msg:str) -> str:
    """Check the type of the question

    Parameters:
    msg (str): The question from user

    Returns:
    str: Type of the question

    """
    EXP_START_WORD = ['PREFIX', 'SELECT']
    EXP_LAST_WORD = ['LIMIT', 'ORDER', 'GROUP', 'HAVING', '}']
    type = ""

    exp_start_idx = len(msg)
    for word in EXP_START_WORD:
        new_start_idx = msg.find(word)
        if new_start_idx < exp_start_idx:
            exp_start_idx = new_start_idx
    
    exp_last_idx = -1
    for word in EXP_LAST_WORD:
        new_last_idx = msg.find(word)
        if new_last_idx > exp_last_idx:
            exp_last_idx = new_last_idx
    
    if exp_last_idx - exp_start_idx > 0 :
        type = "SPARQL"

    return type

def sparql_parser(msg:str) -> str:
    """Parsing the SPARQL message in a right SPARQL format.

    Parameters:
    msg (str): Raw message from user

    Returns:
    str: valid SPAQRL message

    """
    START_WITH = ["PREFIX" , "SELECT"]
    EXCLUDE = ["'''","‘’’"]

    # Find the expected first SPARQL word and
    # filter out all other words appeared before the first SPARQL word .
    msg_words = msg.split()
    # print(f"\nCHECKPOINT:\n{msg_words}")
    start_idx = len(msg_words)
    for s in START_WITH:
        try:
            new_start_idx = msg_words.index(s)
        except:
            continue
        if start_idx > new_start_idx:
            start_idx = new_start_idx
    msg_words = msg_words[start_idx:]
    # print(f"\nCHECKPOINT:\n{start_idx}\n{msg_words}")
    # remove the specific symbol that makes some trouble.
    for x in EXCLUDE:
        c = msg_words.count(x) 
        for i in range(c): 
            msg_words.remove(x)
    
    # convert list of msg words to space separated string
    parsed_msg = str(' '.join(msg_words))
    print(f"\nCHECKPOINT:\n{parsed_msg}")
    return str(parsed_msg)