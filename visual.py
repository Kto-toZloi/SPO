from tkinter import *
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfile
from tkinter.filedialog import asksaveasfile
import Lexer
import TuringMachine
import Parser
import RPN



root = Tk()
root.title("ДЕМО интерпретатор")
root.geometry('900x530')
root.resizable(width=False, height=False)

def fun(text):
	
	save(text)
	print(cur_file)
	
	view = Tk()
	view.title(f"Результат работы программы из файла {cur_file}")
	view.geometry('800x600')
	view.resizable(width=False, height=False)
	
	frame = Frame(view)
	frame.pack()
	scroll = Scrollbar(frame, command=text.yview)
	scroll.pack(side=RIGHT, fill=Y)
	lab = Label(frame, text="Текст введённого файла")
	inserted = Text(frame, width=50, height=20)	
	
	res = Text(frame, width = 200, height = 20)	 

	
	L = Lexer.Lexer(cur_file) # Указать название файла с кодом
	tokens = L.startLexer()

	inserted.insert(INSERT, L.q)
	inserted.configure(state='disabled')
	
	lab.pack()
	inserted.pack()	
	
	P = Parser.Parser(tokens)
	p = P.startParser()

	RePoNa = RPN.RPN(P.getTree(), tokens)
	RePoNa.start()

	TM = TuringMachine.Turing(RePoNa.getStack())
	res_tm = TM.start()
	
	
	res.insert(INSERT, f"Lexer: {tokens}\n\nAbstract Syntax Tree: \n{p}\n\nReverse Polish Notation:\n{RePoNa.getStack()}\n\nConsole output:\n{res_tm}\n\nVar memory:\n{TM.memory}")
	res.configure(state='disabled')
	
	lab1 = Label(frame, text="Вывод интерпретатора")
	lab1.pack()
	res.pack()
	
def open_file(text):
	file = askopenfile(mode ='r', filetypes =[('My Language files', '*.mylang')])
	if file is not None:
		content = file.read()
		text.delete(1.0, END)
		text.insert(1.0, content)
	pass
	
def save(text):
	files = [('My Language files', '*.mylang')]
	file = asksaveasfile(filetypes = files, defaultextension = files)
	file.write(text.get(1.0, END))
	global cur_file
	cur_file = file.name
	file.close()
    
def quit_program():	
	answer = mb.askyesno(
        title="Вопрос", 
        message="Вы точно хотите выйти?")
	if answer:
		root.destroy()

fr_in = Frame()
fr_in.pack(side=TOP)

mainmenu = Menu(root) 
root.config(menu=mainmenu) 


text = Text(fr_in, width=100, height=30)
text.pack(side=LEFT)
 
scroll = Scrollbar(fr_in, command=text.yview)
scroll.pack(side=LEFT, fill=Y)
 
text.config(yscrollcommand=scroll.set)

frame = Frame()
frame.pack(side=TOP)

Button(frame, text="Выполнить", command=lambda:fun(text)).pack(side=LEFT)


filemenu = Menu(mainmenu, tearoff=0)
filemenu.add_command(label="Открыть...", command = lambda: open_file(text))
filemenu.add_command(label="Сохранить...", command = lambda: save(text))
filemenu.add_command(label="Выход", command = lambda: quit_program())

mainmenu.add_cascade(label="Файл", menu=filemenu)

root.mainloop()


