import ctypes

try:
    td = ctypes.cdll.LoadLibrary("D:\\todo_list\\include\\libtd.dll")
except OSError as e:
    print("Error:{e}")
    exit(1)

td.notice.argtypes = []
td.notice.restype = ctypes.c_bool

td.get_path.argtypes = []
td.get_path.restype = ctypes.c_char_p

td.write.argtypes = [ctypes.c_char_p,ctypes.c_bool]
td.write.restype = None

td.tips.argtypes = []
td.tips.restype = ctypes.c_bool

td.create.argtypes = []
td.create.restype = None

td.readb.argtypes = [ctypes.c_int]
td.readb.restype = ctypes.c_bool

td.read.argtypes = [ctypes.c_int]
td.read.restype = ctypes.c_char_p

td.get_path()
if not td.notice():
    exit(1)
#----------------------------------
import customtkinter as tk

class Todo:
    def __init__(self):
        self.root = tk.CTk()
        self.root.title("Todo List")
        self.root.geometry("400x380")

        #tmp for saving data
        self.todolist = []
        self.tododone = []
        self.read()

        #division
        self.title = tk.CTkFrame(self.root)
        self.title.pack(side="top", anchor='w',fill="x",padx=10, pady=5)
        self._title()

        self.todoside = tk.CTkScrollableFrame(self.root)
        self.todoside.pack( anchor='w',expand = True,fill="both",padx=10, pady=5)
        self._todoside()

        self.btmpart = tk.CTkFrame(self.root)
        self.btmpart.pack(side = "top",anchor = 'w',fill="x",padx=10, pady=5)
        self._bottom()

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    #when closing
    def on_closing(self):
        td.create()
        for i in range(len(self.todolist)):
            if not self.tododone[i]:
                td.write(self.todolist[i],self.tododone[i])
        self.root.destroy()

    #title area
    def _title(self):
        label = tk.CTkLabel(self.title, text="To-do list", font=("Impact", 50), text_color="blue", justify="left")
        label.pack(side="top")

    #todo area
    def _todoside(self):
        for widget in self.todoside.winfo_children():
            widget.destroy()

        self.todoside_todo = tk.CTkFrame(self.todoside)
        self.todoside_todo.pack(side = "left",fill = "both")

        self.todoside_destroy = tk.CTkFrame(self.todoside,width=40)
        self.todoside_destroy.pack(side = "right")

        self._todoside_todo()
        #self._todoside_destroy()

    #show todo area
    def _todoside_todo(self):
        if len(self.todolist) == 0:
            no_work = tk.CTkLabel(self.todoside_todo, text="hmmmm...\n     seems like you no need to do anything.", font = ("Arial", 15), text_color="black", justify="left")
            no_work.pack()
        for i in range(len(self.todolist)):
            todol = tk.CTkCheckBox(self.todoside_todo,text=self.todolist[i], font=("Arial", 20),variable = tk.BooleanVar(value=self.tododone[i]),command = lambda x = i:self.done(x),height = 20,width = 20 )
            todol.pack(side = "top",pady = 5,anchor = "w")

    """
    #del_button area
    def _todoside_destroy(self):
        for i in range(len(self.todolist)):
            del_bttn = tk.CTkButton(self.todoside_destroy,text = "X",fg_color="red", text_color="white",height = 25,width = 25,command = lambda x = i:self.delete(x))
            del_bttn.pack(side = "top",pady = 4)
    """

    #bottom area
    def _bottom (self):
        self.add = tk.CTkEntry(self.btmpart, placeholder_text="Add some To-do...", width=300)
        self.add.pack(padx=3, pady=5, anchor='sw', fill='x')
        add_bttn = tk.CTkButton(self.btmpart, text="ADD TO-DO", fg_color="blue", text_color="white", font=("Arial", 12),width=25, command=self.add_todo)
        add_bttn.pack(side="left", pady=5, padx = 3, anchor="sw")
        reset_bttn = tk.CTkButton(self.btmpart, text="RESET", command=self.reset, fg_color="blue", text_color="white",font=("Arial", 12), width=25)
        reset_bttn.pack(side="left", pady=5, padx = 3, anchor="sw")
        self.add.bind("<Return>", lambda e: self.add_todo())


    def read(self):
        self.todolist.clear()
        i = 0
        tmp_todo = td.read(i)
        tmp_done = td.readb(i)
        while tmp_todo!=b'':
            self.todolist.append(tmp_todo)
            self.tododone.append(tmp_done)
            i+=1
            tmp_todo = td.read(i)
            tmp_done = td.readb(i)

    def done(self,index):
        self.tododone[index]=not(self.tododone[index])

    def delete(self,index):
        self.todolist.pop(index)
        self.tododone.pop(index)
        self._todoside()

    def reset(self):
        if td.tips():
            self.todolist.clear()
            self.tododone.clear()
            self._todoside()

    def add_todo(self):
        a_todo = self.add.get()
        self.todolist.append(bytes(a_todo,"utf-8"))
        self.tododone.append(False)
        self._todoside()
        self.add.delete(0, "end")

    def run(self):
        self.root.mainloop()
    #################################################

if __name__ == "__main__":
    app = Todo()
    app.run()

# pyinstaller --onefile --windowed --name "TodoList" --add-data "..\include\libtd.dll;." --hidden-import customtkinter --hidden-import ctypes main.py
# pyinstaller TodoList.spec