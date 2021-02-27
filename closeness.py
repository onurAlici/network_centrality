import geopandas as gpd
import networkx as nx
import numpy as np
from shapely.geometry import Point, LineString, Polygon

fp = "original"
fp2 = "iteration_0"
fp3 = "iteration_1"
fp4 = "iteration_2"

liste = [fp,fp2,fp3,fp4]




def p2g(data):
    "transforms the geopandas dataframe to networkx graph, length of the lines calculated with numpy norm function"
    graph1 = nx.Graph()


    for count, i in enumerate(data["geometry"]):
        first = 0
        for j in list(i.coords):
            if first == 0:
                first += 1
                n1 = j
            else:
                n2 = j
                graph1.add_edge(n1, n2, weight=np.linalg.norm(np.array((n1[0], n1[1])) - np.array((n2[0], n2[1]))) )

                n1 = j

    return graph1
def g2p(graph,data):
    "after calculating the edge betweenness for the lines transforms the networkx graph to geopandas dataframe "
    clos = nx.closeness_centrality(graph,distance="weight")
    layer = gpd.GeoDataFrame()
    layer.crs = data.crs

    for i in list(graph.nodes):
        n1 = Point(i[0], i[1])

        layer = layer.append({'geometry': n1, 'closeness': clos[i]
                              }, ignore_index=True)
    return layer


def g2p2(graph,data):
    "after calculating the edge betweenness for the lines transforms the networkx graph to geopandas dataframe "
    clos = nx.closeness_centrality(graph,distance="weight")
    dlayer = {'geometry': [], 'closeness': [] }


    for i in list(graph.nodes):
        n1 = Point(i[0], i[1])

        dlayer["geometry"].append(n1)
        dlayer["closeness"].append(clos[i])
    gdf = gpd.GeoDataFrame(dlayer, crs=data.crs)
    return gdf

def yap(fp,b):

    data = gpd.read_file(fp)
    G = p2g(data)

    layer = g2p2(G, data)

    layer.to_file(b)

sira = 0
for i in liste:

    son = "test__closeness__" + str(sira)
    print(son + "in process")
    outPath =  son
    yap(i,outPath)
    print("yukarıdaki bitti.")
    sira = sira + 1

print("hepsi bitti....")
