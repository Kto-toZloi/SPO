import copy
import re
from Parser import Node

op = (
    ['if', 0],
    ['while', 0],
    ['(', 0],
    ['{', 0],
    [')', 1],
    ['{', 1],
    ['else', 1],
    [':=', 2],
    ['||', 2],
    ['&', 3],
    ['~', 4],
    ['<', 5],
    ['>', 5],
    ['==', 5],
    ['<=', 5],
    ['>=', 5],
    ['<>', 5],
    ['+', 6],
    ['-', 6],
    ['*', 7],
    ['/', 7]
)

#Класс Reversive Polish Notation
class RPN:
    def __init__(self, tree, tokens):
        self.stack = []
        self.out = []
        self.tokens = tokens
        self.mi = 1
        self.tree = Node('')
        self.tree = copy.deepcopy(tree)

    # Начало создания RPN
    def start(self):
        print('RPN:')
        newtree = self.tree.getNodes()
        for node in newtree:
            for child in node.getNodes():
                self.expr(child)
        print(self.out)

    def getStack(self):
        return self.out

    # RPN для expr
    def expr(self, node):
        if node.getParam() == 'assign_expr':
            self.assign_expr(generateTokenList(node, []))
        elif node.getParam() == 'if_expr':
            self.if_expr(node)
        elif node.getParam() == 'while_expr':
            self.while_expr(node)
        elif node.getParam() == 'func':
            self.func(node.getNodes()[0])

    def func(self, node):
        if node.getParam() == 'print_func':
            self.print_func(generateTokenList(node, []))
        elif node.getParam() == 'hashmap_init':
            self.hashmap_init(generateTokenList(node, []))
        elif node.getParam() == 'doubleLinkedList_init':
            self.doublelinkedlist_init(generateTokenList(node, []))
        elif node.getParam() == 'put_func':
            self.put_func(generateTokenList(node, []))
        elif node.getParam() == 'remove_func':
            self.remove_func(generateTokenList(node, []))

    def hashmap_init(self, token_buff):
        self.stack.append(token_buff.pop(0)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(self.stack.pop(0))
        self.stack.clear()

    def doublelinkedlist_init(self, token_buff):
        self.stack.append(token_buff.pop(0)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(self.stack.pop(0))
        self.stack.clear()

    def put_func(self, token_buff):
        self.stack.append(token_buff.pop(0)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(self.stack.pop(0))
        self.stack.clear()

    def print_func(self, token_buff):
        self.stack.append([token_buff.pop(0)[1], 1])
        self.assign_expr(token_buff)
        self.stack.clear()

    def remove_func(self, token_buff):
        self.stack.append(token_buff.pop(0)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(token_buff.pop(1)[1])
        self.out.append(self.stack.pop(0))
        self.stack.clear()

    # RPN для логических и арифметических операций
    def assign_expr(self, token_buff):
        # print(token_buff)
        while len(token_buff) > 0:
            # print('STACK', self.stack, ' OUT:', self.out)

            if token_buff[0][0] == 'VARIABLE' or token_buff[0][0] == 'NUMBER':
                if token_buff[0][0] == 'NUMBER':
                    token_buff[0] = (token_buff[0][0], float(token_buff[0][1]))
                self.out.append(token_buff.pop(0)[1])

            elif token_buff[0][0] == 'ASSIGN_OP' or token_buff[0][0] == 'OPERATION' or token_buff[0][0] == 'LOGICAL_OP':
                for oper in op:
                    if token_buff[0][1] == oper[0]:
                        op_buff = oper

                while (len(self.stack) > 0) and (self.stack[-1][1] > op_buff[1]) and self.stack[-1][0] != '(':
                    self.out.append(self.stack.pop(-1)[0])

                token_buff.pop(0)
                self.stack.append(op_buff)

            elif token_buff[0][1] == '(':
                for oper in op:
                    if token_buff[0][1] == oper[0]:
                        op_buff = oper

                token_buff.pop(0)
                self.stack.append(op_buff)

            elif token_buff[0][1] == ')':
                for oper in op:
                    if token_buff[0][1] == oper[0]:
                        op_buff = oper
                token_buff.pop(0)

                while self.stack[-1][0] != '(':
                    self.out.append(self.stack.pop(-1)[0])
                if self.stack[-1][0] == '(':
                    self.stack.pop(-1)
            elif token_buff[0][1] == 'get':
                self.stack.append([token_buff.pop(0)[1], 1])
                token_buff.pop(0)
                self.out.append(token_buff.pop(0)[1])
                self.out.append(token_buff.pop(0)[1])
                token_buff.pop(0)
                self.out.append(self.stack.pop(-1)[0])
        while len(self.stack) > 0:
            self.out.append(self.stack.pop(-1)[0])

    # RPN для условного оператора
    def if_expr(self, node):
        self.tokens.pop(0)
        buff_mi = copy.deepcopy(self.mi)
        self.assign_expr(generateTokenList(node.getNodes()[0].getNodes()[1], []))
        self.out.append('M' + str(buff_mi))
        self.out.append('false goto')
        self.mi = self.mi + 2
        for nodes1 in node.getNodes()[1].getNodes():
            for nodes2 in nodes1.getNodes():
                self.expr(nodes2)
        if len(node.getNodes()) > 2:
            self.out.append('M' + str(buff_mi + 1))
            self.out.append('goto')
            self.out.append('M' + str(buff_mi) + ':')
            for nodes1 in node.getNodes()[3].getNodes():
                for nodes2 in nodes1.getNodes():
                    self.expr(nodes2)
            self.out.append('M' + str(buff_mi + 1) + ':')
        else:
            self.out.append('M' + str(buff_mi) + ':')

    def while_expr(self, node):
        self.tokens.pop(0)
        buff_mi = copy.deepcopy(self.mi)
        self.out.append('M' + str(buff_mi) + ':')
        self.assign_expr(generateTokenList(node.getNodes()[0].getNodes()[2], []))
        self.out.append('M' + str(buff_mi + 1))
        self.out.append('false goto')
        self.mi = self.mi + 2
        for nodes1 in node.getNodes()[1].getNodes():
            for nodes2 in nodes1.getNodes():
                self.expr(nodes2)
        self.out.append('M' + str(buff_mi))
        self.out.append('goto')
        self.out.append('M' + str(buff_mi + 1) + ':')


# Использование дерева токенов для отделения выражений в блоки
def generateTokenList(tree, genTokenList):
    if isinstance(tree.getParam(), tuple):
        genTokenList.append(tree.getParam())
    if len(tree.getNodes()) == 1:
        for l in tree.getNodes():
            generateTokenList(l, genTokenList)
    else:
        for l in tree.getNodes():
            generateTokenList(l, genTokenList)
    return genTokenList
