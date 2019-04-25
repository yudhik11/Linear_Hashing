from __future__ import print_function
import sys

class LinearHash:
	def __init__(self):
		self.bucks = dict()
		self.bucks[0] = list()
		self.bucks[1] = list()
		self.idx_hash = 1
		self.total_blocks = 2
		self.keys = 0
		self.split_idx = 0
		self.bucks[0].append([])
		self.bucks[1].append([])

	def getlen(self, x):
		return len(x)

	def calc_mod(self, x, mod):
		return x % (1<<mod)
	
	def add_bucket(self):
		add_idx = len(self.bucks)
		self.bucks[add_idx] = list()
		self.total_blocks+=1		
		to_update = list()
		self.bucks[add_idx].append([])
		if (self.getlen(self.bucks) == (1 << (self.idx_hash+1)+1)):
			self.idx_hash+=1
			self.split_idx = 0
		get_rem_idx = 1<<self.idx_hash

		# while get_rem_idx <= add_idx:
		upd_idx = add_idx - get_rem_idx
		get_rem_idx += get_rem_idx/2
		for i in range(0, self.getlen(self.bucks[upd_idx])):
			self.total_blocks-=1
			for val in self.bucks[upd_idx][i]:
				to_update.append(val)
		self.bucks[upd_idx] = list()
		self.bucks[upd_idx].append([])
		self.total_blocks+=1

		self.split_idx+=1
		
		for val in to_update:
			hash_val = self.calc_mod(val, self.idx_hash)
			
			if hash_val < self.split_idx:
				hash_val = self.calc_mod(val, self.idx_hash + 1)
				last_block_idx = self.getlen(self.bucks[hash_val]) - 1
				
				if 4*(len(self.bucks[hash_val][last_block_idx])+1) > B:
					last_block_idx+=1
					self.total_blocks+=1
					self.bucks[hash_val].append(list())
				self.bucks[hash_val][last_block_idx].append(val)
		

	def insert(self, val):
		global output_buffer
		hash_val = self.calc_mod(val, self.idx_hash)
		
		if hash_val < self.split_idx:
			hash_val = self.calc_mod(val, self.idx_hash + 1)

		for i in range(0, self.getlen(self.bucks[hash_val])):
			if val in self.bucks[hash_val][i]:
				return 1

		self.keys+=1
		last_block_idx = self.getlen(self.bucks[hash_val]) - 1

		if 4*(len(self.bucks[hash_val][last_block_idx])+1) > B:
			self.total_blocks += 1
			self.bucks[hash_val].append(list())
			last_block_idx += 1

		self.bucks[hash_val][last_block_idx].append(val)
		output_buffer.append(val)
		
		if len(output_buffer)*4 >= B:
			for num in output_buffer:
				print(num)
			output_buffer = list()

		if((self.keys * 4) / (self.total_blocks * B)*1.0 > 0.75):
			self.add_bucket()

	def print_bucks(self):
		for key in self.bucks:
			print(key, "=>")
			for block in self.bucks[key]:
				print(block)

def main():
	input_buffer = []
	global output_buffer
	with open(file, 'r') as f:
		for line in f:
			input_buffer.append(int(line.strip()))

			if len(input_buffer) * 4 >= ((M-1) * B):
				for num in input_buffer:
					hash_obj.insert(num)
					# hash_obj.print_bucks()
				input_buffer = []

	if(len(input_buffer) > 0):
		for val in input_buffer:
			hash_obj.insert(val)
		input_buffer = []

	if(len(output_buffer) > 0):
		for val in output_buffer:
			print(val)
		output_buffer = []
	

output_buffer = list()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		sys.exit("Usage: python file.py input_file M B")
	
	args = sys.argv
	file = args[1]
	M = int(args[2])
	B = int(args[3])

	if(M<2):
		sys.exit("M should be greater than or equal to 2")
	if(B<4):
		sys.exit("Insufficient size for node")
	if (M*B > 1000000):
		sys.exit("M * B should be less than 1000000")
	hash_obj = LinearHash()
	main()