##split up subreddit and moderator graph

import networkx as nx
from networkx.algorithms import bipartite

while(True):
    print "Export graphs? y or n"
    choice = raw_input()
    yeses = ["y","Y","yes","Yes"]
    nos = ["n","N","no","No"]
    if choice in yeses:
        export = True
        print "Will export."
        break
    if choice in nos:
        export = False
        print "Won't export."
        break

print "reading GML"
G = nx.read_gml("C:\\Users\\Theseus\\Documents\\moderatorproject\\prenetworkx.gml").to_undirected()

for n,d in G.nodes_iter(data=True):
    d["Subscribers"] = int(d["Subscribers"])
    if d['Class']=="Moderator":
        d['bipartite']=1
        for N in G.neighbors_iter(n):
            d["Subscribers"] = d["Subscribers"] + int(G.node[N]["Subscribers"])
    else:
        d['bipartite']=0

top_nodes = set(n for n,d in G.nodes(data=True) if d['bipartite']==0)
bottom_nodes = set(G) - top_nodes

def mymean(degreeiter):
    Sum = 0.0
    count = 0 
    for n,d in degreeiter:
        Sum += d
        count += 1
    return Sum / count


print "is bottom_nodes a bipartite set?",bipartite.is_bipartite_node_set(G, bottom_nodes) 	
print "is top_nodesa  bipartite set?",bipartite.is_bipartite_node_set(G, top_nodes) 	

print len(bottom_nodes)," bottom nodes",len(top_nodes)," top nodes"

print "Average subreddits moderated per moderator: ",mymean(G.degree_iter(bottom_nodes))
print "Average moderators per subreddit: ",mymean(G.degree_iter(top_nodes))
if export:
    nx.write_gexf(G,"C:\\Users\\Theseus\\Documents\\moderatorproject\\untouched.gexf")
    print "gexf exported"

pg1 = bipartite.projected_graph(G, bottom_nodes)
print "Unweighted moderator to moderator projection made"
print "Average unweighted degree: ",mymean(pg1.degree_iter())
if export:
    nx.write_gexf(pg1,"C:\\Users\\Theseus\\Documents\\moderatorproject\\bottoms.gexf")
    print "gexf exported"

pg2 = bipartite.projected_graph(G, top_nodes)
print "Unweighted subreddit to subreddit projection made"
print "Average unweighted degree: ",mymean(pg2.degree_iter())
if export:
    nx.write_gexf(pg2,"C:\\Users\\Theseus\\Documents\\moderatorproject\\tops.gexf")
    print "gexf exported"

wpg1 = bipartite.weighted_projected_graph(G, bottom_nodes)
print "Weighted bottom node projection made"
print "Average weighted moderator-moderator degree: ",mymean(wpg1.degree_iter(weight='weight'))
if export:
    nx.write_gexf(wpg1,"C:\\Users\\Theseus\\Documents\\moderatorproject\\weightedbottoms.gexf")
    print "gexf exported"

wpg2 = bipartite.weighted_projected_graph(G, top_nodes)
print "Weighted top node projection made"
print "Average weighted subreddit-subreddit degree: ",mymean(wpg2.degree_iter(weight='weight'))
if export:
    nx.write_gexf(wpg2,"C:\\Users\\Theseus\\Documents\\moderatorproject\\weightedtops.gexf")
    print "gexf exported"

print "done"
