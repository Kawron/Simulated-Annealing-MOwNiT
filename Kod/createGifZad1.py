import networkx as nx
import matplotlib.pyplot as plt
import imageio
import os

def createGif(nodes, name):

    def createCityGraph(node):
        G = nx.Graph()
        i = 0
        for city in node.cities:
            G.add_node(i, cord = city)
            i += 1
        n = len(node.cities)
        for i in range(n-1):
            G.add_edge(i, i+1)
        G.add_edge(0, n-1)
        return G

    def plotCityGraph(G, name):
        fig, ax = plt.subplots(figsize=(8, 8))
        # ax.set_facecolor('#95A4AD')
        pos = nx.get_node_attributes(G, "cord")
        nx.draw_networkx(G, pos, node_size=14, with_labels=False)
        plt.savefig(name)
        plt.close()

    fileNames = []
    n = len(nodes)
    for i in range(n):
        G = createCityGraph(nodes[i])
        plotCityGraph(G, f"./{name}/{i}.png")
        fileNames.append(f"./{name}/{i}.png")
    name = name + "/" + name + ".gif"
    with imageio.get_writer(name, mode='I') as writer:
        for filename in fileNames:
            image = imageio.imread(filename)
            writer.append_data(image)