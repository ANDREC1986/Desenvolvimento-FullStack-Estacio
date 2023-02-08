from pandas import DataFrame
import tkinter as tk
from tkinter import ttk
import csv_loader
import random

ferramentas = csv_loader.ferramentas
funcionarios = csv_loader.funcionarios
reservas = csv_loader.reservas

def left_zero_fix(value, int):
    item = str(value)
    while len(item) < int:
        item = '0'+item
    return item

class data_manager:
    def data_add(item,target,func):
        target.append(item)
        func()

    def data_delete(ids,target,func):
        for item in target:
            if str(ids) == item[0]:
                target.remove(item)
        func()

    def data_upd(ids,list,target,func):
        for n in range(len(target)):
            if target[n][0] == str(ids):
                target[n] = list
        func()

    def export_exel():
        file = []
        for item in ferramentas:
            file.append([item[0],item[1]])
        file = DataFrame(file)
        file.to_excel('ferramentas.xlsx', index=False)

class make_tree:
    def __init__(self,lista,master,minwidit, width, strech):
        self.selection = []
        self.clipboard = []
        self._item_list = lista
        self._tree = ttk.Treeview(master, columns=self._item_list[0], show='headings')
        self._headings = self._item_list[0]
        for n in range(len(self._headings)): 
            if self._headings[n] == 'id':
                self._tree.heading(''.join(self._headings[n]), text=''.join(self._headings[n]).upper())
            else:
                self._tree.heading(''.join(self._headings[n]), text=''.join(self._headings[n]).capitalize())
            self._tree.column(self._headings[n], minwidth=minwidit[n], width=width[n], stretch=strech[n])
        for item in self._item_list[1:]:
            self.insert_item(item)
        self._tree.bind('<<TreeviewSelect>>', self.item_selected)

    def pack(self):
        self._tree.pack(padx=2, pady=2, expand=True, fill='both', side='left')

    def grid(self,i):
        self._tree.grid(column=i, row=1, sticky='nswe')
    
    def insert_item(self,item):
        self._tree.insert('','end', iid=item[0], values=item)

    def item_selected(self,event=''):
        self.selection = []
        for selected_item in self._tree.selection():
            self.selection.append(self._tree.item(selected_item)['values'])

    def wipe_colmuns(self,list):
        for n in list:
            self._tree.column(f'#{n}', width=0)
    
    def get_selected(self):
        if len(self.selection) > 0:
            self.item_selected()
            return self.selection[-1]

    def update_tree(self,uid,item):
        self._tree.item(str(uid), values=item)
    
    def delete_tree(self,uid):
        self._tree.delete(uid)
    
    def tree_copy(self):
        self.clipboard = []
        for selection in self._tree.selection():
            self.clipboard.append(self._tree.item(selection)['values'])
            self._tree.delete(selection)
        return self.clipboard

    def tree_paste(self,values):
        self._clipboard = values
        for item in self._clipboard:
            self._tree.insert('','end',values=item)
    
    def get_index(self):
        self.result = []
        for line in self._tree.get_children():
                self.result.append(self._tree.item(line)['values'][0])
        self.result = list(map(lambda i: left_zero_fix(i,7),self.result))
        return self.result  

class update_kit():
    def __init__(self, master, labels, positions):
        self.limit, self.typed = '',''
        self.frames, self.entrys, self.labels = [],[],[]
        self.master = master
        self.elements = labels
        self.entry_frame = tk.Frame(self.master)
        for i in range(len(self.elements)):
            self.frames.append(tk.Frame(self.entry_frame))
            self.labels.append(tk.Label(self.frames[i], text=self.elements[i]))
            self.entrys.append(tk.Entry(self.frames[i]))
            self.labels[i].pack(fill='both', expand=False, side='left')
            self.entrys[i].pack(fill='both', expand=True, side='left')
        self.positions = positions
        for item in self.positions:
            column = item[0]
            row = item[1]
            frame = item[2]
            try: columnspan = item[3]
            except: columnspan = 1
            self.frames[frame].grid(column=column, row=row, columnspan=columnspan, stick='nswe', padx=4, pady=2)
        for item in self.entrys: item.bind('<KeyRelease>', self.binds)

    def lock(self,_int):
        self.entrys[_int].config(state='disable')
    
    def save_block(self):
        if list(filter(lambda e: e.get() == '', self.entrys)) == []: return True
                   
    def pack(self):
        self.entry_frame.grid(column=0, row=0, sticky='nswe')
        
    def get_entrys(self):
        return list(map(lambda e: e.get(), self.entrys))
      
    def set_entrys(self,item):
        if item != '':
            for i in range(len(item)):
                self.entrys[i].insert(0, item[i])
        else: 
            self.master.destroy()

    def set_limits(self,limits):
        self.limit = limits
    
    def binds(self,event):
        for n in range(len(self.entrys)):
            if self.limit != '': self.char_limit(self.entrys[n], self.limit[n])
            if self.typed != '': 
                for item in self.typed: 
                    if n == item: self.typer(self.entrys[n])
            if self.elements[0] == 'CPF':
                if len(self.entrys[0].get()) == 11 and self.valida_cpf(self.entrys[0].get()) == False:
                    self.entrys[0].config(foreground='red')
                else: self.entrys[0].config(foreground='black')
        
    def typer(self,element):
            try:
                float(element.get())
            except ValueError:
                element.delete(len(element.get())-1, tk.END)

    def char_limit(self,element,limit):
        characters = len(element.get())
        if characters > limit:
            element.delete(limit, tk.END)

    def valida_cpf(self, cpf):
        self.numbers = cpf.replace('.','')
        self.numbers = cpf.replace('-','')
        self.numeros = self.numbers[:-2]
        self.valida1 = self.numbers[-2]
        self.valida2 = self.numbers[-1]
        self.numbers = 10
        self.resultado = 0
        for c in self.numeros:
            self.resultado = self.resultado + int(c)*self.numbers
            self.numbers -= 1
        self.resultado = self.resultado * 10
        self.resultado = self.resultado % 11
        if self.resultado == 10: self.resultado = 0
        if str(self.resultado) != str(self.valida1):
            return False
        self.numbers = cpf.replace('.','')
        self.numbers = cpf.replace('-','')
        self.numeros = self.numbers[:-1]
        self.numbers = 11
        self.resultado = 0
        for c in self.numeros:
            self.resultado = self.resultado + int(c)*self.numbers
            self.numbers -= 1
        self.resultado = self.resultado * 10
        self.resultado = self.resultado % 11
        if self.resultado == 10: self.resultado = 0
        if str(self.resultado) != str(self.valida2):
            return False
            
class ferramentas_update():
    def __init__(self,mode,master,vars='', tree =''):
        self.vars = vars
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.tree = tree
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.form = update_kit(self.window, ['Nome - Descrição', 'Fabricante','Part Num','Tipo','Voltagem ','Tamanho','U.Medida','Material','Tempo Limite'],
                                            [[0,0,0,3],[0,1,1],[1,1,2],[2,1,3],[0,2,4],[1,2,5],[2,2,6],[0,3,7],[1,3,8]])
        self.form.pack()
        self.menu = tk.Frame(self.window)
        if mode == 'add':
            self.window.title('Adicionar Ferramenta')
            self.bnt_submit = tk.Button(self.menu, text='Adicionar Ferramenta', command=self.add_ferramenta)
        if mode == 'edit':
            self.window.title('Editar Ferramenta')
            self.item = vars[1:]
            if self.item != []:
                self.form.set_entrys(self.item)
            self.bnt_submit = tk.Button(self.menu, text='Editar Ferramenta', command=self.edit_ferramenta)
        self.bnt_cancel = tk.Button(self.menu, text='Cancelar', command=self.window.destroy)
        self.menu.grid(column=0, row=1, sticky='e')
        self.bnt_submit.pack(fill='both', side='left')
        self.bnt_cancel.pack(fill='both', side='left')
        self.form.set_limits([60,30,25,15,25,20,15,15,2])
        self.form.typed = [2,5,8]

    def add_ferramenta(self):
        global ferramentas_window
        if self.form.save_block() == True:
            self.item = list(map(lambda e: e, self.form.get_entrys()))
            self.item.insert(0, self.unid())
            self.tree.insert_item(self.item)
            ferramentas_window.add(self.item)
            self.window.destroy()

    def edit_ferramenta(self):
        global ferramentas_window
        if self.form.save_block() == True:
            self.item = list(map(lambda e: e, self.form.get_entrys()))
            self.item.insert(0, (left_zero_fix(self.vars[0],7)))
            ferramentas_window.upd(self.item[0],self.item)
            self.tree.update_tree(self.item[0],self.item)
            self.window.destroy()

    def id(self):
        id = ''
        for i in range(7):
            id += ''.join(str(random.randint(0,9)))
        return id

    def unid(self):
        match = False
        check = False
        while check == False:
            unid = self.id()
            for item in ferramentas:
                if item[0] == unid:
                    match = True
            if match == False:
                check = True
        return unid

class funcionarios_update:
    def __init__(self, mode, master, vars='', tree =''):
        self.vars = vars
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.tree = tree
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.form = update_kit(self.window, ['CPF','Nome','Equipe','Turno','Contato'],
                                            [[0,0,0],[1,0,1,2],[0,2,2],[1,2,3],[2,2,4]])
        self.form.pack()
        self.menu = tk.Frame(self.window)
        if mode == 'add':
            self.window.title('Adicionar Funcionário')
            self.bnt_submit = tk.Button(self.menu, text='Adicionar Funcionário', command=self.add_funcionario)
        if mode == 'edit':
            self.window.title('Editar Funcionário')
            self.item = vars
            if self.item != []:
                self.item[0] = left_zero_fix(self.item[0],11)
                self.form.set_entrys(self.item)
            self.bnt_submit = tk.Button(self.menu, text='Editar Funcionário', command=self.edit_funcionario)
            self.form.lock(0)
        self.bnt_cancel = tk.Button(self.menu, text='Cancelar', command=self.window.destroy)
        self.menu.grid(column=0, row=1, sticky='e')
        self.bnt_submit.pack(fill='both', side='left')
        self.bnt_cancel.pack(fill='both', side='left')
        self.form.limit = [11,40,5,30,9]
        self.form.typed = [0,4]

    def add_funcionario(self):
        global funcionarios_window
        if self.form.save_block() == True:
            self.item = self.form.get_entrys()
            self.item[0] = left_zero_fix(self.item[0],11)
            self.tree.insert_item(self.item)
            funcionarios_window.add(self.item)
            self.window.destroy()

    def edit_funcionario(self):
        global funcionarios_window
        if self.form.save_block() == True:
            self.value = self.form.get_entrys()
            funcionarios_window.upd(self.value[0],self.value)
            self.tree.update_tree(left_zero_fix(self.value[0],11),self.value)
            self.window.destroy()

class reservas_update:
    def __init__(self, mode, master,  vars = [], tree =''):
        self.clip_board = ''
        self.reservadas = []
        self.vars = vars
        self.window = tk.Toplevel(master)
        self.window.resizable(0,0)
        self.tree = tree
        self.window.columnconfigure(0, weight=1)
        self.window.rowconfigure(0, weight=1)
        self.form = update_kit(self.window, ['Funcionario','Decrição','Retirada','Devolução'],
                                            [[0,0,0],[1,0,1,2],[0,2,2],[1,2,3]])
        self.form.pack()
        self.menu = tk.Frame(self.window)
        self.column_minwidth = [0,0,0,0,0,0,0,0,0,0]
        self.column_width = [80,200,80,80,80,80,80,80,80,80]
        self.colmun_strech = [False,True,False,False,False,False,False,False,False,False]
        self.frame2 = tk.Frame(self.window)
        self.frame2.grid(column=0, row=1, sticky='nswe', pady=(5,0))
        self.ferramentas_tree = make_tree(ferramentas,self.frame2,self.column_minwidth,self.column_width,self.colmun_strech)
        self.ferramentas_tree.wipe_colmuns([3,4,5,6,7,8,9,10])
        self.ferramentas_tree.grid(0)
        self.fram_switch = tk.Frame(self.frame2)
        self.bnt_add = tk.Button(self.fram_switch, text='>', command=self.add_ferramenta)
        self.bnt_del = tk.Button(self.fram_switch, text='<', command=self.del_ferramenta)
        self.fram_switch.grid(column=1, row=1, sticky='nswe')
        self.bnt_add.pack(pady=(80,0))
        self.bnt_del.pack()
        if mode == 'add':
            self.window.title('Criar Reserva')
            self.bnt_submit = tk.Button(self.menu, text='Criar Reserva', command=self.add_reserva)
            self.reservas = make_tree(ferramentas[:1],self.frame2,self.column_minwidth,self.column_width,self.colmun_strech)
            self.reservas.wipe_colmuns([3,4,5,6,7,8,9,10])
            self.reservas.grid(2)
        if mode == 'edit':
            self.window.title('Editar Reserva')
            self.item = vars[:-1]
            if self.item != []:
                self.form.set_entrys(self.item)
                self.reservadas.append(ferramentas[0])
                if vars[4] != str:
                    self.items = str(vars[4])
                else: self.items = vars[4]
                self.items = self.items.split()
                for item in self.items:
                    for ferramenta in ferramentas:
                        if ferramenta[0] == item:
                            self.reservadas.append(ferramenta)
                            self.ferramentas_tree.delete_tree(item)
            self.bnt_submit = tk.Button(self.menu, text='Editar Reserva', command=self.edit_reserva)
            self.reservas = make_tree(self.reservadas,self.frame2,self.column_minwidth,self.column_width,self.colmun_strech)
            self.reservas.wipe_colmuns([3,4,5,6,7,8,9,10])
            self.reservas.grid(2)
        self.bnt_cancel = tk.Button(self.menu, text='Cancelar', command=self.window.destroy)
        self.menu.grid(column=0, row=2, sticky='e')
        self.bnt_submit.pack(fill='both', side='left')
        self.bnt_cancel.pack(fill='both', side='left')
    
    def add_ferramenta(self):
        self.clipboard = self.ferramentas_tree.tree_copy()
        self.clipboard[0][0] = left_zero_fix(self.clipboard[0][0],7)
        self.reservas.tree_paste(self.clipboard)

    def del_ferramenta(self):
        self.clipboard = self.reservas.tree_copy()
        self.clipboard[0][0] = left_zero_fix(self.clipboard[0][0],7)
        self.ferramentas_tree.tree_paste(self.clipboard)

    def add_reserva(self):
        global reserva_window
        if self.form.save_block() == True:
            self.item = self.form.get_entrys()
            self.item.append(self.reservas.get_index())
            self.tree.insert_item(self.item)
            reserva_window.add(self.item)
            self.window.destroy()

    def edit_reserva(self):
        global reserva_window
        if self.form.save_block() == True:
            self.item = self.form.get_entrys()
            self.item.append(self.reservas.get_index())
            reserva_window.upd(self.item[0],self.item)
            self.tree.update_tree(self.item[0],self.item)
            self.window.destroy()

class main_window:
    def __init__(self, **kwargs):
        self.master = kwargs['master']
        self.target = kwargs['target']
        self.title = kwargs['window']
        self.column_minwidth = [80,200,80,80,80,80,80,80,80,80]
        self.column_width = [80,200,80,80,80,80,80,80,80,80]
        self.colmun_strech = [False,True,False,False,False,False,False,False,False,False]
        self.frame1 = tk.Frame(self.master)
        self.tree = make_tree(self.target, self.frame1, self.column_minwidth, self.column_width, self.colmun_strech)
        self.tree.pack()
        self.frame1.grid(column=0, row=0, sticky='nswe')
        self.frame2 = tk.Frame(self.master)
        self.frame2.grid(column=0, row=1, sticky='nswe')
        self.bnt_add = tk.Button(self.frame2, text='Criar ' + kwargs['window'], command=self.add)
        self.bnt_edit = tk.Button(self.frame2, text='Editar ' + kwargs['window'], command=self.edit)
        self.bnt_del = tk.Button(self.frame2, text='Deletar ' + kwargs['window'], command=self.delete)
        self.bnt_add.pack(side='left', padx=(5,3), pady=(3,5), ipadx=3, ipady=5)
        self.bnt_edit.pack(side='left', padx=3, pady=(3,5), ipadx=5, ipady=5)
        self.bnt_del.pack(side='left', padx=3, pady=(3,5), ipadx=5, ipady=5)
        if self.title == 'Ferramentas':
            self.bnt_export = tk.Button(self.frame2, text='Export Excel', command=data_manager.export_exel)
            self.bnt_export.pack(side='right', padx=(3,5), pady=(3,5), ipadx=10, ipady=5)
            self.update=ferramentas_update
        if self.title == 'Reservas':
            self.update=reservas_update
        if self.title == 'Funcionários':
            self.update=funcionarios_update

    def add(self):
        self.update('add',self.master,'',self.tree)
   
    def edit(self):
        self.item = self.tree.get_selected()
        if self.item:
            self.update('edit',self.master,self.item,self.tree)
    
    def delete(self):
        if self.title == 'Ferramentas':
            global ferramentas_window
            self.item = self.tree.get_selected()[0]
            self.tree.delete_tree(self.item)
            ferramentas_window.delete(self.item)
        if self.title == 'Reservas':
            global reserva_window
            self.item = self.tree.get_selected()[0]
            self.tree.delete_tree(self.item)
            reserva_window.delete(self.item)
        if self.title == 'Funcionários':
            global funcionarios_window
            self.item = self.tree.get_selected()[0]
            self.tree.delete_tree(self.item)
            funcionarios_window.delete(self.item)

class root_window:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Ferramentaria')
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.root.resizable(0,0)
        self.title_frame = tk.Frame(self.root, relief='solid')
        self.title_frame.grid(column=0, row=0, sticky='nswe')
        self.title_label = tk.Label(self.title_frame, text='Ferramentaria',font=25)
        self.title_label.pack(side='left', padx=5, pady=(5,5))
        self.menu_frame = tk.Frame(self.root)
        img_ferramentas = tk.PhotoImage(file='./res/ferramenta.png', width=150, height=150,)
        img_funcionarios = tk.PhotoImage(file='./res/funcionario.png', width=150, height=150,)
        img_reservas = tk.PhotoImage(file='./res/agenda.png', width=150, height=150)
        bnt_ferramentas = tk.Button(self.menu_frame, image=img_ferramentas, command=self.abrir_ferramentas)
        bnt_ferramentas.pack(fill='x', expand=True, side='left', padx=2, pady=2)
        bnt_funcionarios = tk.Button(self.menu_frame, image=img_funcionarios, command=self.abrir_funcionarios)
        bnt_funcionarios.pack(fill='x', expand=True, side='left', padx=2, pady=2)
        bnt_reservas = tk.Button(self.menu_frame, image= img_reservas, command=self.abrir_reservas)
        bnt_reservas.pack(fill='x', expand=True, side='left', padx=2, pady=2)
        self.menu_frame.grid(column=0,row=1)
        self.buttons_frame = tk.Frame(self.root)
        self.buttons_frame.grid(column=0, row=2,sticky='nswe')
        self.root.mainloop()
       
    class window:
        def __init__(self,**kwargs):
            self.master = kwargs['master']
            self.func = kwargs['func']
            self.target = kwargs['target']
            self.main_window = tk.Toplevel()
            self.main_window.title(kwargs['title'])
            self.main_window.columnconfigure(0, weight=1)
            self.main_window.rowconfigure(0, weight=1)
            self.main_window.resizable(0,0)
            self.target_window = main_window(master=self.main_window,window=kwargs['title'],target=self.target)

        def add(self,item):
            data_manager.data_add(item, self.target, self.func)
        def upd(self,uid, list):
            data_manager.data_upd(uid, list, self.target, self.func)
        def delete(self, uid):
            data_manager.data_delete(uid, self.target, self.func)
        def close(self):
            self.main_window.destroy()

    def abrir_reservas(self):
        global reserva_window
        try:
            reserva_window.close()
        except:
            pass
        finally:
            reserva_window = self.window(master=self.root,title='Reservas',func=csv_loader.save_reservas,target=reservas)

    def abrir_funcionarios(self):
        global funcionarios_window
        try:
            funcionarios_window.close()
        except:
            pass
        finally:
            funcionarios_window = self.window(master=self.root,title='Funcionários',func=csv_loader.save_funcionarios,target=funcionarios)

    def abrir_ferramentas(self):
        global ferramentas_window
        try:
            ferramentas_window.close()
        except:
            pass
        finally:
            ferramentas_window = self.window(master=self.root,title='Ferramentas',func=csv_loader.save_ferramentas,target=ferramentas)
root_window()