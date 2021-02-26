import geopandas as gpd
import networkx as nx
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import rasterio as rio
import rasterstats as rs
import jenkspy


def read_data(fp):
    """reads the file for network data, data needs to be linestring layer"""
    data = gpd.read_file(fp)
    return data

def p2g(data):
    """transforms the geopandas dataframe to networkx graph, length of the lines calculated with numpy norm function"""
    graph1 = nx.Graph()

    for count, i in enumerate(data["geometry"]):
       #every geometry can be a multilinestring and I converted every multilinestring to separate linestring, to represent them in network 
        first = 0
        filtre = data.iloc[count]["ref"]
        #filter comes from openstreetmap(OSM) data which has a ref column. I mainly used osm as a source for tranportation networks.
        for j in list(i.coords):
            if first == 0:
                first += 1
                n1 = j
            else:
                n2 = j
               #every point of linestring used as vertex in graph and linestrings become edges.
                graph1.add_edge(n1, n2, weight=np.linalg.norm(np.array((n1[0], n1[1])) - np.array((n2[0], n2[1]))),filtre = filtre )
                
                n1 = j

    return graph1

def g2p(graph,data):
    """after calculating the edge betweenness for the lines transforms the networkx graph to geopandas dataframe """
    bet = nx.edge_betweenness_centrality(graph,k=750,weight="weight")
    layer = gpd.GeoDataFrame()
    layer.crs = data.crs
    uzun = nx.get_edge_attributes(graph, "weight")
    filtre = nx.get_edge_attributes(graph, "filtre")
    for i in list(graph.edges):
        n1 = Point(i[0][0], i[0][1])
        n2 = Point(i[1][0], i[1][1])
        line = LineString([n1, n2])
        layer = layer.append({'geometry': line, 'weight': bet[i]*10000000000000000000, "uzun": uzun[i],
                              "filtre": filtre[i]}, ignore_index=True)
    return layer

fp = "filepath"

data = read_data(fp)

graph = p2g(data)

sonuc = g2p(graph, data)

data2 = sonuc.copy()
sonuc.to_file("test.gpkg", layer = "orginal", driver="GPKG")

for i in range(3):
    """
    this is iteration part where in every iteration centrality of the network calculated again and edges are classified in five groups according to their 
    betweenness centrality. After classification of edges, top two classes extracted from network and a next iteration begins. 
    """
    print("cycle    " + str(i) + "    in progress")
    breaks = jenkspy.jenks_breaks(data2["weight"], nb_class=5)
    breaks.reverse()
    
    filtered = ((data2["weight"] > breaks[2]) & (data2["weight"] < breaks[0]))
    #filter can be used for granting immunity to some edges in the network, such as bridges or anything else too inconvenient to remove from network
    data2 = data2[~filtered]
    data2 = g2p(p2g(data2), sonuc)
    #every iteration saved to file
    data2.to_file("test.gpkg", layer=str(i), driver="GPKG")
