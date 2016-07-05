from __future__ import division
from time import clock
from numpy import mean

class Node:
	def __init__(self):
		self.neighbors = []
		self.neighbor_set = set()
		self.ES = 0.0
		
	def add_neighbor(self, neighbor):
		self.neighbors.append(neighbor)

	def initial(self, node_dict):
		self.neighbor_set = set(self.neighbors)

	def compute_ES(self, node_dict):
		t = 0
		for k in self.neighbor_set:
			node_k = node_dict[k]
			t += len(node_k.neighbor_set & self.neighbor_set)

		n = len(self.neighbors)

		self.ES = n - t / n


def read_file(file_name):
	import csv

	node_dict = {}
	with open(file_name) as fp:
		for i, line in enumerate(fp):
			if i < 4:
				continue
	
			items = line.split(',')
			fm = int(items[0])
			to = int(items[1])
	
			node_dict.setdefault(fm, Node()).add_neighbor(to)
			node_dict.setdefault(to, Node()).add_neighbor(fm)
	
			if i % 100000 == 0:
				print i

	return node_dict


def write_file(file_name, node_dict):
	with open(file_name, 'w') as fp:
		for id, node in node_dict.items():
			fp.write(str(id) + ',' + str(node.ES) + '\n')


def main():
	# read_file_name = '1285-7524-14/egp.ungraph.csv'
	# write_file_name = '1285-7524-14/es.csv'
	read_file_name = '76853-133445-/73989-117699-13/wordnet3.upgraph.csv'
	# write_file_name = '../dataset/twitter/es.csv'
	nums = []
	for i in range(5):
		node_dict = read_file(read_file_name)
		for node in node_dict.values():
			node.initial(node_dict)
		a = clock()
		for node in node_dict.values():
			node.compute_ES(node_dict)
		b = clock()
		nums.append(b - a)
		print b - a
	# write_file(write_file_name, node_dict)
	print 'mean', mean(nums)


if __name__ == '__main__':
	main()
