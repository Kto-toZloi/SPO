import HashMap
import DoubleLinkedList

op_count = (
    ['DoubleLinkedList'],
    ['get'],
    ['remove'],
    ['print'],
    ['put'],
    ['HashMap'],
    [':='],
    ['||'],
    ['&'],
    ['~'],
    ['<'],
    ['>'],
    ['=='],
    ['<='],
    ['>='],
    ['<>'],
    ['+'],
    ['-'],
    ['*'],
    ['/'],
    ['goto'],
    ['false goto']
)


class Turing:
	def __init__(self, input_stack):
		self.input_stack = input_stack
		self.iterator = 0
		self.stack = []
		self.memory = {}
		self.op_buff = []

	def start(self):
		buf=''
		print('Console output: ')
		while self.iterator < len(self.input_stack):
			if self.isOperand(self.input_stack[self.iterator]):
				buf += str(self.calculate())
			else:
				self.stack.append(self.input_stack[self.iterator])
			self.iterator = self.iterator + 1
		print('Var memory:')
		print(self.memory)
		return buf

	def isOperand(self, operand):
		self.op_buff = None
		for oper in op_count:
			if operand == oper[0]:
				self.op_buff = oper
		if self.op_buff is not None:
			return True
		else:
			return False

	def calculate(self):
		buf = ''
		if self.op_buff[0] == ':=':
			self.add_var(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '+':
			self.add(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '*':
			self.multiply(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '/':
			self.divide(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == 'goto':
			self.goto(self.stack.pop(-1))
		if self.op_buff[0] == 'false goto':
			self.false_goto(self.stack.pop(-1))
		if self.op_buff[0] == '>':
			self.greater(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '<':
			self.less(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '-':
			self.minus(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '==':
			self.equals(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '>=':
			self.greater_equals(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '<=':
			self.less_equals(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '<>':
			self.not_equals(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '&':
			self.and_ex(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == '||':
			self.or_ex(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == 'print':
			buf = self.print(self.stack.pop(-1))
		if self.op_buff[0] == 'HashMap':
			self.hashMap(self.stack.pop(-1))
		if self.op_buff[0] == 'DoubleLinkedList':
			self.doubleLinkedList(self.stack.pop(-1))
		if self.op_buff[0] == 'put':
			if self.get_type(self.stack[-3]) == 'HashMap':
				self.hashMapPut(self.stack.pop(-1), self.stack.pop(-1), self.stack.pop(-1))
			elif self.get_type(self.stack[-3]) == 'DoubleLinkedList':
				self.doubleLinkedListPut(self.stack.pop(-1), self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == 'get':
			if self.get_type(self.stack[-2]) == 'HashMap':
				self.hashMapGet(self.stack.pop(-1), self.stack.pop(-1))
			elif self.get_type(self.stack[-2]) == 'DoubleLinkedList':
				self.doubleLinkedListGet(self.stack.pop(-1), self.stack.pop(-1))
		if self.op_buff[0] == 'rem':
			if self.get_type(self.stack[-2]) == 'HashMap':
				self.hashMapRemove(self.stack.pop(-1), self.stack.pop(-1))
			elif self.get_type(self.stack[-2]) == 'DoubleLinkedList':
				self.doubleLinkedListRemove(self.stack.pop(-1), self.stack.pop(-1))
		return buf
		
	def get_type(self, var):
		if isinstance(self.memory[var], HashMap.HashTable) is True:
			return 'HashMap'
		elif isinstance(self.memory[var], DoubleLinkedList.DoubleLL) is True:
			return 'DoubleLinkedList'

	def print(self, value):
		ret_value = self.convert(value)
		out = ''
		if ret_value is not None:
			out = ret_value
		else:
			out = value
		print(out)
		return str(out)+'\n'
        

	def goto(self, iterator):
		counter = -1
		for tokens in self.input_stack:
			counter = counter + 1
			if tokens == iterator + ':':
				self.iterator = counter

	def false_goto(self, iterator):
		counter = -1
		if self.stack.pop(-1) is False:
			for tokens in self.input_stack:
				counter = counter + 1
				if tokens == iterator + ':':
					self.iterator = counter

	def divide(self, op2, op1):
		self.stack.append(self.convert(op1) / self.convert(op2))

	def add(self, op2, op1):
		self.stack.append(self.convert(op1) + self.convert(op2))

	def minus(self, op2, op1):
		self.stack.append(self.convert(op1) - self.convert(op2))

	def multiply(self, op2, op1):
		self.stack.append(self.convert(op1) * self.convert(op2))

	def greater(self, op2, op1):
		self.stack.append(self.convert(op1) > self.convert(op2))

	def greater_equals(self, op2, op1):
		self.stack.append(self.convert(op1) >= self.convert(op2))

	def less_equals(self, op2, op1):
		self.stack.append(self.convert(op1) <= self.convert(op2))

	def equals(self, op2, op1):
		self.stack.append(self.convert(op1) == self.convert(op2))

	def not_equals(self, op2, op1):
		self.stack.append(self.convert(op1) != self.convert(op2))

	def less(self, op2, op1):
		self.stack.append(self.convert(op1) < self.convert(op2))

	def and_ex(self, op2, op1):
		self.stack.append(op1 and op2)

	def or_ex(self, op2, op1):
		self.stack.append(op1 or op2)

	def add_var(self, value, var):
		value = self.convert(value)
		self.memory[var] = value

	def convert(self, op):
		if op in self.memory:
			return self.memory.get(op)
		elif isinstance(op, str):
			for var, value in self.memory.items():
				if op == var:
					op = value
					return float(op)
				elif op == '-' + var:
					op = -value
					return float(op)
				else:
					return None
		return float(op)

	def doubleLinkedList(self, var):
		self.memory[var] = DoubleLinkedList.DoubleLL()

	def doubleLinkedListPut(self, value, key, var):
		self.memory[var].insert(key, DoubleLinkedList.DllNode(value))

	def doubleLinkedListGet(self, value, var):
		self.stack.append(self.memory[var].get(value))

	def doubleLinkedListRemove(self, value, var):
		if self.memory[var].delete(value) is False:
			raise Exception("Key not found")

	def hashMap(self, var):
		self.memory[var] = HashMap.HashTable()

	def hashMapPut(self, value, key, var):
		self.memory[var].set_val(key, value)

	def hashMapGet(self, key, var):
		if self.memory[var].get_val(key) is False:
			raise Exception("Key not found")
		else:
			self.stack.append(self.memory[var].get_val(key))

	def hashMapRemove(self, key, var):
		if self.memory[var].delete_val(key) is False:
			raise Exception("Key not found")
