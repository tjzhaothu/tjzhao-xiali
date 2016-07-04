import csv
import louvain
import  igraph as ig
import networkx as nx



def readfile(filename):

    csvfile=file(filename)
    csvread=csv.reader(csvfile)
    edge_list=[]
    with open(filename) as rf:
        for num,line in enumerate(rf):
            node=line.split(',')
            edge_list.append((int(node[0]),int(node[1].strip('\n'))))
    return edge_list

def writefile(filename,graph_dict):
    #with open(filename,"w") as wf:
        for node in graph_dict.items():
            print node


def main(readfile_name,writefile_name):

    edge_list=readfile(readfile_name)
    gra=ig.Graph(0,edge_list)
    gra.es['weight']=1.0
    part=louvain.find_partition(graph=gra,method="Modularity",weight='weight')


    #print louvain.quality(gra, part, method='Significance')
    print gra.summary()
    print pa

if __name__=='__main__':
    readfile_name='egp.ungraph.csv'
    writefile_name='new_community.csv'
    main(readfile_name,writefile_name)