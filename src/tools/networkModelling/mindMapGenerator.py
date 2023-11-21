import graphviz
import json


def add_nodes(g, parent, sections, used_nodes, remove_topics):
    keys = sections
    for key in keys:
        if key == "title" or (remove_topics and key == "text"):
            continue
        elif key != "text":
            if key not in used_nodes:
                g.node(key)
                g.edge(parent, key)
                used_nodes.append(key)

            if isinstance(sections, dict):
                g = add_nodes(g, key, sections[key], used_nodes, remove_topics)
        else:
            for item in sections["text"]:
                g.node(item)
                g.edge(parent, item)
                used_nodes.append(item)

    return g


def create_mind_map(filepath, remove_topics=False):
    with open(filepath, 'r') as j:
        sections = dict(json.loads(j.read()))

    title = sections["title"]

    # Initialize the graph
    g = graphviz.Graph(title, filename=f"./data/{title}.gv", engine='sfdp', graph_attr={'overlap': 'scale'})

    # create the central node and set the node attribute to be ellipse shape
    g.attr('node', shape='ellipse')
    g.node(title)

    # create the topics and set the node attributes to be box shape
    g.attr('node', shape='box')

    used_nodes = ["leopard", "title"]

    return add_nodes(g, title, dict(sections), used_nodes, remove_topics)
