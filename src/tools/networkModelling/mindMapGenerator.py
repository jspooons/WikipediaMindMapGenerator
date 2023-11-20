import graphviz
import json


def create_topics(g, parent, sections, used_nodes):
    keys = sections
    for key in keys:
        if key == "title": continue
        if key != "text":
            if key not in used_nodes:
                g.node(key)
                g.edge(parent, key)
                used_nodes.append(key)

            if isinstance(sections, dict):
                g = create_topics(g, key, sections[key], used_nodes)
        else:
            for item in sections["text"]:
                g.node(item)
                g.edge(parent, item)
                used_nodes.append(item)

    return g


def create_mind_map(filepath):
    with open(filepath, 'r') as j:
        sections = dict(json.loads(j.read()))

    title = sections["title"]
    print(title)

    # Initialize the graph
    g = graphviz.Graph(title, filename=f"./data/{title}.gv", engine='circo')

    # create the central node and set the node attribute to be ellipse shape
    g.attr('node', shape='ellipse')
    g.node(title)

    # create the topics and set the node attributes to be box shape
    g.attr('node', shape='box')

    used_nodes = ["leopard", "title"]

    return create_topics(g, title, dict(sections), used_nodes)
