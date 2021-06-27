import copy
import re

class Node:
    def __init__(self, param):
        self.param = param
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)

    def printNode(self):
        for nodes in self.nodes:
            print(nodes)

    def getNodes(self):
        return self.nodes

    def getParam(self):
        return self.param


class Parser:
	def __init__(self, token_list):
		self.token_list = copy.deepcopy(token_list)
		self.root = ''#объявляем, что корень дерева будет

	def startParser(self):
		#print('Abstract Syntax Tree:')
		self.root = self.lang()
		return printAST(self.root)
        #self.printTokens(self.root, 0)

	def getTokens(self):
		return self.token_list

	def getTree(self):
		return copy.deepcopy(self.root)

	def lang(self):
		node = Node('lang')
		while len(self.token_list) > 0:
			node.addNode(self.expr())
		return node

	def expr(self):
		node = Node('expr')
		if self.token_list[0][0] == 'VARIABLE':
			node.addNode(self.assign_expr())
		elif self.token_list[0][0] == 'if_KW':
			node.addNode(self.if_expr())
		elif self.token_list[0][0] == 'while_KW':
			node.addNode(self.while_expr())        
		elif re.match('(print_KW)|(rem_KW)|(put_KW)|(clear_KW)|(hashmap_KW)|(doubleLinkedList_KW)',self.token_list[0][0]):
			node.addNode(self.func())
		else:
			raise Exception("No expression found")
		return node

	def func(self):
		node = Node('func')
		if self.token_list[0][0] == 'print_KW':
			node.addNode(self.print_expr())
		elif self.token_list[0][0] == 'rem_KW':
			node.addNode(self.remove())
		elif self.token_list[0][0] == 'put_KW':
			node.addNode(self.put())
		elif self.token_list[0][0] == 'clear_KW':
			node.addNode(self.clear())
		elif self.token_list[0][0] == 'hashmap_KW':
			node.addNode(self.hashmap_init())
		elif self.token_list[0][0] == 'doubleLinkedList_KW':
			node.addNode(self.doublelinkedlist_init())
		else:
			raise Exception
		return node

	def doublelinkedlist_init(self):
		node = Node('doubleLinkedList_init')
		node.addNode(self.match('doubleLinkedList_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.match('VARIABLE'))
		node.addNode(self.match('R_BR'))
		return node

	def hashmap_init(self):
		node = Node('hashmap_init')
		node.addNode(self.match('hashmap_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.match('VARIABLE'))
		node.addNode(self.match('R_BR'))
		return node

	def remove(self):
		node = Node('remove_func')
		node.addNode(self.match('rem_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.value())
		node.addNode(self.value())
		node.addNode(self.match('R_BR'))
		return node

	def put(self):
		node = Node('put_func')
		node.addNode(self.match('put_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.value())
		node.addNode(self.value())
		node.addNode(self.value())
		node.addNode(self.match('R_BR'))
		return node

	def print_expr(self):
		node = Node('print_func')
		node.addNode(self.match('print_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.value_expr())
		node.addNode(self.match('R_BR'))
		return node

    # IF_EXPR
	def if_expr(self):
		node = Node('if_expr')
		node.addNode(self.if_head())
		node.addNode(self.body('if_body'))
		try:
			node.addNode(self.match('else_KW'))
			node.addNode(self.body('else_KW'))
		except Exception:
			None
		return node

	def if_head(self):
		node = Node('if_head')
		node.addNode(self.match('if_KW'))
		node.addNode(self.if_condition())
		return node

	def if_condition(self):
		node = Node('if_condition')
		node.addNode(self.match('L_BR'))
		node.addNode(self.logical_expr())
		node.addNode(self.match('R_BR'))
		return node

	def match(self, input_str):
		node = Node(self.token_list[0])
		if input_str == self.token_list[0][0]:
			self.token_list.pop(0)
			return node
		else:
			raise Exception('Unknown symbol' + self.token_list[0][0])

    # WHILE_EXPR
	def while_expr(self):
		node = Node('while_expr')
		node.addNode(self.while_head())
		node.addNode(self.body('while_body'))
		return node

	def while_head(self):
		node = Node('while_head')
		node.addNode(self.match('while_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.logical_expr())
		node.addNode(self.match('R_BR'))
		return node

    # ASSIGN_EXPR
	def assign_expr(self):
		node = Node('assign_expr')
		node.addNode(self.match('VARIABLE'))
		node.addNode(self.match('ASSIGN_OP'))
		node.addNode(self.value_expr())
		return node

	def value_expr(self):
		node = Node('value_expr')
		err = ''
		try:
			node.addNode(self.value_expr_brackets())
		except Exception:
			err = 'Error'
		try:
			node.addNode(self.value())
		except Exception:
			err = err + ' Found'
		try:
			node.addNode(self.match('OPERATION'))
			node.addNode(self.value_expr())
		except Exception:
			None

		try:
			node.addNode(self.match('OPERATION'))
			node.addNode(self.value_expr())
		except Exception:
			None

		if err == 'Error Found':
			raise Exception('Error')

		return node

	def value_expr_brackets(self):
		node = Node('value_expr_brackets')
		node.addNode(self.match('L_BR'))
		node.addNode(self.value_expr())
		node.addNode(self.match('R_BR'))
		return node

    # LOGICAL_EXPR
	def logical_expr(self):
		node = Node('logical_expr')
		node.addNode(self.value())
		while re.match('LOGICAL_OP', self.token_list[0][0]):
			node.addNode(self.match('LOGICAL_OP'))
			node.addNode(self.value())
		return node

    # VALUE -> VAR | NUMBER
	def value(self):
		node = Node('VALUE')
		if self.token_list[0][0] == 'NUMBER':
			node.addNode(self.match('NUMBER'))
			return node
		elif self.token_list[0][0] == 'VARIABLE':
			node.addNode(self.match('VARIABLE'))
			return node
		elif self.token_list[0][0] == 'get_KW':
			node.addNode(self.get_func())
			return node
		else:
			raise Exception('Unknown symbol' + self.token_list[0][0])

	def get_func(self):
		node = Node('get_func')
		node.addNode(self.match('get_KW'))
		node.addNode(self.match('L_BR'))
		node.addNode(self.value())
		node.addNode(self.value())
		node.addNode(self.match('R_BR'))
		return node

	def body(self, KW):
		node = Node(KW)
		node.addNode(self.match('L_CUR_BR'))
		node.addNode(self.expr())
		while re.match('(VARIABLE)|(if_KW)|(while_KW)|(print_KW)|(hashmap_KW)|(doublelinkedlist_KW)', self.token_list[0][0]):
			node.addNode(self.expr())
		node.addNode(self.match('R_CUR_BR'))
		return node

	def printTokens(self, tree, level):
		tab = ''
		if isinstance(tree.getParam(), tuple):
			for i in range(level):
				tab = tab + '     '
			print(tab, tree.getParam())

		if len(tree.getNodes()) == 1:
			for l in tree.getNodes():
				self.printTokens(l, level)
		else:
			for l in tree.getNodes():
				self.printTokens(l, level + 1)

# AST PRINT
def printAST(tree, level = 0, s = ''):
    tab = ''
    for i in range(level):
        tab = tab + '     '
    #print(tab, tree.getParam())
    
    s+=f"{tab + str(tree.getParam())}\n"

    for leaf in tree.getNodes():
        s = printAST(leaf, level + 1,s)
    return s
