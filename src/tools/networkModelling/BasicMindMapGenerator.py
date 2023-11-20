import graphviz
import random


def create_star_graph(central_text, topic_texts, num_topic_ideas, topics_ideas_texts):
    # initialize the graph
    g = graphviz.Graph('mind_map', filename='./data/basic_mind_map.gv', engine='neato')

    # create the central node and set the node attribute to be ellipse shape
    g.attr('node', shape='ellipse')
    g.node(central_text)

    # create the topics and set the node attributes to be box shape

    for i in range(len(topic_texts)):
        g.node(topic_texts[i])
        g.edge(central_text, topic_texts[i])

    # add topic ideas to randomly selected topics
    while True:
        node = random.choice(topic_texts)
        topic_texts = list(set(topic_texts) - {node})

        for i in range(num_topic_ideas):
            node_idea = random.choice(topics_ideas_texts)
            topics_ideas_texts = list(set(topics_ideas_texts) - {node_idea})
            g.node(node_idea)
            g.edge(node, node_idea)

        if len(topic_texts) == 0:
            break

    return g


if __name__ == '__main__':
    g = create_star_graph(
        'Central Text',
        ['Topic 1', 'Topic 2', 'Topic 3', 'Topic 4', 'Topic 5'],
        3,
        ['Idea {}'.format(i + 1) for i in range(30)])
    g.view()
