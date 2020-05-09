import geopandas as gpd
import networkx as nx
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import rasterio as rio
import rasterstats as rs
import jenkspy


def read_data(fp):
    "reads the file for network data, data needs to be linestring layer"
    data = gpd.read_file(fp)
    return data

def p2g(data):
    "transforms the geopandas dataframe to networkx graph, length of the lines calculated with numpy norm function"
    graph1 = nx.Graph()

    for count, i in enumerate(data["geometry"]):
        first = 0
        filtre = data.iloc[count]["ref"]
        for j in list(i.coords):
            if first == 0:
                first += 1
                n1 = j
            else:
                n2 = j
                graph1.add_edge(n1, n2, weight=np.linalg.norm(np.array((n1[0], n1[1])) - np.array((n2[0], n2[1]))),filtre = filtre )
                "buraya yeni olarak filtre eklendi konuştuğumuz ana yolları bu şekilde immune yapmayı düşünüyordum"
                "osm datasının içinde ref olarak sütunda geçiyor bu filtrenin kaynağı"
                n1 = j

    return graph1

def g2p(graph,data):
    "after calculating the edge betweenness for the lines transforms the networkx graph to geopandas dataframe "
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

fp = "/Users/graus/PycharmProjects/network_centrality/kadikoy/edges.shp"

data = read_data(fp)

graph = p2g(data)

sonuc = g2p(graph, data)

breaks = jenkspy.jenks_breaks(sonuc["weight"], nb_class=5)

for count, i in enumerate(breaks[::-1][:-1]):
    "yukarıdaki liste ters çevrilmiş büyükten küçüğe sıralamak için öyle yaptım "
    "aşağıdaki iterasyon konuştuğumuz gibi sonları dikkate almayacaktı onu henüz yazmadım değişecek aşağısı"
    filtered = (sonuc["weight"] > breaks[count]) & (sonuc["weight"] < breaks[count+1])
    data2 = sonuc[~filtered]
    data2 = g2p(p2g(data2), sonuc)
    data2.to_file("testooo" + str(count))


