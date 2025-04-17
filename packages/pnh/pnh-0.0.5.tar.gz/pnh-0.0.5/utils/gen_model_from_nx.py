import pandapipes 
import networkx as nx

def pp(
        g=nx.Graph()
       ,fluid='water'
):
    """ Returns a pandapipes model from a networkx graph."""

    pass

    net = pandapipes.create_empty_network(fluid=fluid)

    return net 