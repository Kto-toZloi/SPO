import re

terminals = \
    [
        ('if_KW', '^(if)$', 1),
        ('else_KW', '^(else)$', 1),
        ('while_KW', '^(while)$', 1),
        ('VARIABLE', '^-?[a-zA-Z]{1}[a-zA-Z_0-9]{0,}$', 0),#унарный минус?????
        ('NUMBER', '^0|-?[1-9][0-9]*$', 0),
        ('ASSIGN_OP', '^(:=)$', 0),
        ('OPERATION', '^(\+|\-|\*|\/)$', 0),
        ('L_BR', '^\($', 0),
        ('R_BR', '^\)$', 0),
        ('L_CUR_BR', '^{$', 0),
        ('R_CUR_BR', '^}$', 0),
        ('WhiteSpace', '\s*', 0),
        ('LOGICAL_OP', '^((&)|(||)|(xor)|(nor)|(=>)|(==)|(<>)|(>)|(>=)|(<)|(<=))$', 0),
        ('print_KW', '^(print)$', 1),        
        ('rem_KW', '^(rem)$', 1),
        ('put_KW', '^(put)$', 1),
        ('clear_KW', '^(clear)$', 1),
        ('size_KW', '^(size)$', 1),
        ('get_KW', '^(get)$', 1),
        ('is_empty_KW', '^(isEmpty)$', 1),
        ('clear_KW', '^(clear)$', 1),
        ('hashmap_KW', '^(HashMap)$', 1),
        ('doubleLinkedList_KW', '^(DoubleLinkedList)$', 1),
    ]


class Lexer:
	def __init__(self, file):
		print('Input file:')
		self.file = file
		self.f = open(file)
		self.q = self.f.read()
		print(self.q)		
		self.data = self.q.replace('\n', ' ')
		self.tokens = [[], []]#имя терминала, значение
		#self.f.close()

	def startLexer(self):
		print('Lexer:')
		tokens = self.nextLexeme(self.data)
		print(tokens)		
		return tokens

	def nextLexeme(self, string_file):
		tokens = []
		while len(string_file) > 0:
			buf = self.lexeme(string_file)
			
			#print(f"buf = {buf}")
			
			string_file = string_file[len(buf[1]):]
			#пробелы не появляются в итоговом списке токенов для 
			#удобства построения дерева и по той причине, что они несут 
			#нагрузку смысловую только при разборе строки на токены			
			if buf[0] != 'WhiteSpace':
				tokens.append(buf[:2])
		return tokens

	def lexeme(self, input_string):
		buf = ''
		buf += input_string[0]
		if buf == ":" or buf == "=": 
			buf += input_string[1]
			return self.matcher(buf)[0]
		elif len(self.matcher(buf)) > 0:
			while len(self.matcher(buf)) > 0 and len(buf) < len(input_string):
				buf += input_string[len(buf)]
			if len(buf) > 1:
				buf = buf[:len(buf) - 1]
			return max(self.matcher(buf))
		else:
			print(f"buf = {buf}")
			q = open(self.file).readlines()
			num = 0
			for i in iter(q):
				if buf in i:
					st = i
					break
				else:
					num += 1
			#Делаем Exception с номером строки и строкой в которой произошла ошибка
			raise Exception(f'Incorrect input "{buf}" in file {self.file} at str №{num} "{st.rstrip()}"')

	def matcher(self, buf):
		'''Возвращает совпадения с терминалами'''
		matches = []
		for terminal in terminals:
			match = re.fullmatch(terminal[1], buf)
			
			if match is not None:
				matches.append((terminal[0], match.string, terminal[2]))
		return matches
		#return[(terminal[0], re.fullmatch(terminal[1], buf).string, terminal[2]) for terminal in terminals if re.fullmatch(terminal[1], buf) is not None]
