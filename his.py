import networkx as nx
import numpy as np
import itertools
import pprint
import csv

def use_pagerank(read_file_name, write_file_name):
	G = nx.Graph()

	with open(read_file_name) as fp:
		for num, line in enumerate(fp):
			if num < 4:
				continue
			items = line.split('\t')
			i = int(items[0])
			j = int(items[1])
			G.add_edge(i, j)
			if num % 100000 == 0:
				print 'line', num

	pr = nx.pagerank(G)
	
	with open(write_file_name, 'w') as fp:
		for id, rank in pr.items():
			fp.write(str(id) + ',' + str(rank) + '\n')


def stat_community():
	with open('com-youtube.all.cmty.txt') as fp:
		node_dict = {}
		max = 0
		for community_id, line in enumerate(fp):
			nodes = map(int, line.split('\t'))
			for node in nodes:
				node_dict.setdefault(node, []).append(community_id)
			max = community_id
		print max
			
	with open('youtube.community.txt', 'w') as fp:
		for node in sorted(node_dict.keys()):
			community_list = node_dict[node]
			fp.write(str(node) + ',')
			str_list = map(str, sorted(community_list))
			fp.write(','.join(str_list) + '\n')


def stat_community2():
	import numpy as np

	with open('../dataset/dblp.all.cmty.txt') as fp:
		node_dict = {}
		for community_id, line in enumerate(fp):
			num = len(line.split('\t'))
			try:
				node_dict[num] += 1
			except KeyError:
				node_dict[num] = 1
			
	keys = node_dict.keys()
	keys.sort(reverse=True)
	values = np.array([node_dict[key] for key in keys])
	values = np.cumsum(values)
	new_lines = [str(key) + ',' + str(value) + '\n' for key, value in zip(keys, values)]

	with open('statistics.csv', 'w') as fp:
		fp.writelines(new_lines) 


alpha = 0.3
beta = 0.49
epsilon = 1e-10

community_num = 14
S_list = []
for i in range(2, community_num):
	for combination in itertools.combinations(range(community_num), i):
		S_list.append(combination)
S_num = len(S_list)

C_indexes = [[j for j, S in enumerate(S_list) if i in S] for i in range(community_num)]


class Node:
	def __init__(self):
		self.P_array = np.zeros(community_num)
		self.I_array = np.zeros(community_num)
		self.H_array = np.zeros(S_num)
		self.neighbors = []

	def add_neighbor(self, neighbor):
		self.neighbors.append(neighbor)

	def set_community(self, community, weight):
		self.I_array[community] = weight
		
	def update_P(self):
		for community, I_value in enumerate(self.I_array):
			self.P_array[community] = alpha * I_value + beta * max(self.H_array[C_indexes[community]])

	def update_I(self, node_dict):
		diff_abs = 0
		for community, I_value in enumerate(self.I_array):
			max_num = I_value
			for neighbor in self.neighbors:
				P_u = node_dict[neighbor].P_array[community]
				if P_u > max_num:
					max_num = P_u
			self.I_array[community] = max_num
			diff_abs += abs(I_value - max_num)
		return diff_abs

	def update_H(self):
		for i in range(S_num):
			self.H_array[i] = min(self.I_array[list(S_list[i])])


def read_file(community_file, neighbor_file):
	node_dict = {}
	with open(community_file) as fp:
		for i, line in enumerate(fp):
			items = line.split(',')
			node_id = int(items[0])
			community_id = int(items[1])
			weight = float(items[2])

			node_dict[node_id] = Node()
			node_dict[node_id].set_community(community_id, weight)
			if i % 100000 == 0:
				print 'community file line', i
			# if i > 1:
				# break
	
	with open(neighbor_file) as fp:
		for i, line in enumerate(fp):
			items = line.split(',')
			fm = int(items[0])
			to = int(items[1])
			
			node_dict[fm].add_neighbor(to)
			node_dict[to].add_neighbor(fm)
	
			if i % 100000 == 0:
				print 'neighbor file line', i

	return node_dict


def write_file(result_file, node_dict):
	with open(result_file, 'w') as fp:
		for id, node in node_dict.items():
			fp.write(str(id))
			for S, H_value in zip(S_list, node.H_array):
				if H_value > 0:
					fp.write(',(' + ','.join(map(str, S)) + '):')
					fp.write(str(H_value))
			fp.write('\n')


def main():
	community_file = '../dataset/egp.all.cmty.csv'
	neighbor_file = '../dataset/egp.ungraph.csv'
	result_file = 'dblp_his.csv'

	node_dict = read_file(community_file, neighbor_file)

	print 'initial H'
	for i, node in enumerate(node_dict.values()):
		node.update_H()
		if i % 30 == 0:
			print 'update H', i


	while 1:
		diff_count = 0
		print 'update P'
		for node in node_dict.values():
			node.update_P()
		print 'update I, H'
		for node in node_dict.values():
			diff_count += node.update_I(node_dict)
			node.update_H()

		print 'difference', diff_count
		if diff_count < epsilon:
			break

	write_file(result_file, node_dict)


if __name__ == '__main__':
	main()