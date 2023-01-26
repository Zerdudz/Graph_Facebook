import networkx as nx

G = nx.Graph()

ff = open("all_links.txt", 'r',encoding="utf-8")
for f in ff.readlines():
    f=f.replace("\n","")
    first = f.split("/")[0]
    second = f.split("/")[1]

    G.add_node(first)
    G.add_node(second)
    G.add_edge(first, second)

for p in nx.all_shortest_paths(G, "Lucas Crt","Tony Lbr"):
    print(p)

print(nx.info(G))


#nx.write_gexf(G, "extracted_lastt.gexf")
#nx.write_graphml(G, "extracted_last.graphml")