import geopandas as gpd
import networkx as nx
import numpy as np
from shapely.geometry import Point, LineString, Polygon
import rasterio as rio
import rasterstats as rs


def read_data(fp):
    data = gpd.read_file(fp)

def p2g(data):

    graph1 = nx.Graph()

    for i in data["geometry"]:
        first = 0
        for j in list(i.coords):
            if first == 0:
                first += 1
                n1 = j
            else:
                n2 = j
                graph1.add_edge(n1, n2, weight=np.linalg.norm(np.array((n1[0], n1[1])) - np.array((n2[0], n2[1]))))
                n1 = j

    return graph1

def g2p(graph,data):
    bet = nx.edge_betweenness_centrality(graph,k=750,weight="weight")
    layer = gpd.GeoDataFrame()
    layer.crs = data.crs
    uzun = nx.get_edge_attributes(graph, "weight")
    for i in list(graph.edges):
        n1 = Point(i[0][0], i[0][1])
        n2 = Point(i[1][0], i[1][1])
        line = LineString([n1, n2])
        layer = layer.append({'geometry': line, 'weight': bet[i]*10000000000000, "uzun": uzun[i]}, ignore_index=True)
    return layer

def rasterRead(fp):
    dem = rio.open(fp)
    array = dem.read(1)
    return dem, array

def sampling(row,dem,array):
    n = row["geometry"]
    return array[dem.index(n.x,n.y)]

def fil(row, target_column="majority"):
    if not np.isfinite(row[target_column]):
        return 0
    else:
        return row[target_column]

def sample(data,dem):
    data = data.to_crs(crs=dem.crs)
    data = rs.zonal_stats(data, dem.read(1), affine=dem.transform, stats=['majority'], geojson_out=True)
    data = gpd.GeoDataFrame.from_features(data)
    data["dem"] = data.apply(fil, axis=1)
    return data


def scenario(data):
    list = [0,5,10,15]
    for i in list:
        filtered = data["dem"] > i
        data2 = data[filtered]
        data2 = g2p(p2g(data2),data2)
        data2.to_file("betweenness"+str(i))
        







