import json
from pathlib import Path
import networkx as nx
import matplotlib.pyplot as plt

class Node():
    
    def __init__(self, node, gid):
        self.gid = gid
        self.uid = node['resourceId']
        self.labels = [node['stencil']['id']]
        
        self.property = node['properties']
        self.propertyType = node['propertyTypes']

        self.outgoing = node['outgoing']
        self.incoming = node['incoming']
        
        _bb = node['bounds']
        self.bbox = _bb
        self.pos = ((_bb['lowerRight']['x']+_bb['upperLeft']['x'])/2,
                    (_bb['lowerRight']['y']+_bb['upperLeft']['y'])/2)
        self.dock = node['dockers']
    
    def expand(self, factor):
        self.pos = (factor*self.pos[0], 
                    factor*self.pos[1])
        
    def dict_arrows(self, use_gid=False):
        if use_gid:
            _id = self.gid
        else:
            _id = self.uid

        return {
            "id": _id,
            "position": {
                "x": self.pos[0],
                "y": self.pos[1]
            },
            "caption": "",
            "labels": self.labels,
            "properties": self.property,
            "style": {}
        }
        
class Edge():
    
    def __init__(self, edge, gid):
        
        self.gid = gid
        self.uid = edge['resourceId']
        self.type = edge['stencil']['id']
        self.name = edge['properties']['name']
        self.property = edge['properties']
        del self.property['name']
        self.propertyType = edge['propertyTypes']
        
        if len(edge['outgoing']) == 1:
            self.outgoing = edge['outgoing'][0]['resourceId']
        else:
            print("ERROR: Incorrect outgoing count on edge.")
            exit(2)
        if len(edge['incoming']) == 1:
            self.incoming = edge['incoming'][0]['resourceId']
        else:
            print("ERROR: Incorrect incoming count on edge.")
            exit(2)
            
        self.target = edge['target']['resourceId']
        
        self.bbox = edge['bounds']
        self.dock = edge['dockers']
        
    def dict_arrows(self, gid_map, use_gid=False):
        if use_gid:
            _id = self.gid
            _fr = gid_map[self.incoming]
            _to = gid_map[self.outgoing]
        else:
            _id = self.uid
            _fr = self.incoming
            _to = self.outgoing
        return {
            "id": _id,
            "fromId": _fr,
            "toId": _to,
            "type": self.type,
            "properties": self.property,
            "style": {}
        }

    
class Graph():
    
    def __init__(self,eda_fname = 'model'):
        self.load_eda(eda_fname = eda_fname)
        self.assemble()

    def node(self,uid):
        return self.__n[uid]

    def edge(self,uid):
        return self.__e[uid]
    
    def nodes(self):
        return self.__n
    
    def edges(self):
        return self.__e

    def load_lists(self, nodes, edges):
        self.__n = {}
        i=0
        for _n in nodes:
            _ntmp = Node(_n, f"n{i}")
            self.__n[_ntmp.uid] = _ntmp
            i+=1
        self.__e = {}
        i=0
        for _e in edges:
            _etmp = Edge(_e, f"e{i}")
            self.__e[_etmp.uid] = _etmp
            i+=1
            
    def load_eda(self, eda_fname = 'model'):
        with open(eda_fname, 'r') as f:
            j = json.load(f)

        nodes = []
        edges = []
        for _j in j['childShapes']:
            if 'target' in _j.keys():
                edges.append(_j)
            else:
                nodes.append(_j)

        self.load_lists(nodes, edges)
        
    def expand(self, factor):
        for _n in self.__n.values():
            _n.expand(factor)

    def create_map(self):
        self.__gid = {}
        for _n in self.nodes().values():
            self.__gid[_n.uid] = _n.gid
        for _e in self.edges().values():
            self.__gid[_e.uid] = _e.gid
    
    def create_nx_graph(self):
        self.__G = nx.Graph()
        self.__label = {
            'node': {},
            'edge': {}}
        self.__position = {}
        for _n in self.nodes().values():
            _uid = _n.uid    
            self.__G.add_node(_uid)
            self.__label['node'][_uid] = _n.labels
            self.__position[_uid] = _n.pos
        for _e in self.edges().values():
            _in = _e.incoming
            _out = _e.outgoing
            self.__G.add_edge(_in,_out)
            self.__label['edge'][(_in,_out)] = _e.type

    def assemble(self):
        self.create_map()
        self.create_nx_graph()
    
    def visualize(self):
        plt.figure()
        nx.draw(
            self.__G, 
            pos = self.__position,
            labels = self.__label['node'],
            node_size = 500
               )
        nx.draw_networkx_edge_labels(
            self.__G, 
            self.__position, 
            edge_labels=self.__label['edge'])
        plt.axis('off')
        plt.show()
        
    def export_arrows(self, fpath=None, indent=None, use_gid=False):
        _dtmp = {
            "nodes": [],
            "relationships": [],
            "style": {}
                }
        for _n in self.nodes().values():
            _dtmp['nodes'].append(_n.dict_arrows(use_gid))
        for _e in self.edges().values():
            _dtmp['relationships'].append(_e.dict_arrows(self.__gid, use_gid))
            
        _dtmp['style'] = {
                "font-family": "sans-serif",
                "background-color": "#ffffff",
                "background-image": "",
                "background-size": "100%",
                "node-color": "#ffffff",
                "border-width": 4,
                "border-color": "#000000",
                "radius": 50,
                "node-padding": 5,
                "node-margin": 2,
                "outside-position": "auto",
                "node-icon-image": "",
                "node-background-image": "",
                "icon-position": "inside",
                "icon-size": 64,
                "caption-position": "inside",
                "caption-max-width": 200,
                "caption-color": "#000000",
                "caption-font-size": 50,
                "caption-font-weight": "normal",
                "label-position": "inside",
                "label-display": "pill",
                "label-color": "#000000",
                "label-background-color": "#ffffff",
                "label-border-color": "#000000",
                "label-border-width": 4,
                "label-font-size": 40,
                "label-padding": 5,
                "label-margin": 4,
                "directionality": "directed",
                "detail-position": "inline",
                "detail-orientation": "parallel",
                "arrow-width": 5,
                "arrow-color": "#000000",
                "margin-start": 5,
                "margin-end": 5,
                "margin-peer": 20,
                "attachment-start": "normal",
                "attachment-end": "normal",
                "relationship-icon-image": "",
                "type-color": "#000000",
                "type-background-color": "#ffffff",
                "type-border-color": "#000000",
                "type-border-width": 0,
                "type-font-size": 16,
                "type-padding": 5,
                "property-position": "outside",
                "property-alignment": "colon",
                "property-color": "#000000",
                "property-font-size": 16,
                "property-font-weight": "normal"
        }
        _darrows = {"graph": _dtmp}
        
        if fpath is None:
            return _darrows
        else:
            with open(fpath, 'w') as _of:
                json.dump(_darrows, _of, indent=indent)
