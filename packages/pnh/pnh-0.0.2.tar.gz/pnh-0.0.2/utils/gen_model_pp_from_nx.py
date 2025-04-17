import pandapipes as pp
import networkx as nx

def gen_model_pp_from_nx(
        g=nx.Graph()
       ,fluid='water'
):
    """ Returns a pandapipes model from a networkx graph."""

    pass

    net = pp.create_empty_network(fluid=fluid)

    return net 