import ctypes
from PIL import Image
from customtkinter import CTkCheckBox
import sys

try:
    td = ctypes.cdll.LoadLibrary("D:\\todo_list\\include\\libtd.dll")
except OSError as e:
    print("Error:{e}")
    exit(1)

td.get_pic_path.argtypes = []
td.get_pic_path.restype = ctypes.c_char_p

td.notice.argtypes = []
td.notice.restype = ctypes.c_bool

td.get_path.argtypes = []
td.get_path.restype = ctypes.c_char_p

td.write.argtypes = [ctypes.c_char_p,ctypes.c_bool]
td.write.restype = None

td.write_setting.argtypes = [ctypes.c_bool]
td.write_setting.restype = None

td.tips.argtypes = []
td.tips.restype = ctypes.c_bool

td.create.argtypes = []
td.create.restype = None

td.reads.argtypes = []
td.reads.restype = None

td.reads_.argtypes = [ctypes.c_int]
td.reads.restype = ctypes.c_bool

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
        tk.set_appearance_mode("dark")

        #tmp for saving data
        self.todolist = []
        self.tododone = []
        self.read()

        #division
        #title area
        self.title = tk.CTkFrame(self.root,fg_color = "transparent")
        self.title.pack(side="top", anchor='w',fill="x",padx=10, pady=5)
        self._title()

        #todo area
        self.todoside = tk.CTkScrollableFrame(self.root)
        self.todoside.pack( anchor='w',expand = True,fill="both",padx=10, pady=5)
        self._todoside(False)

        #bottom area
        self.btmpart = tk.CTkFrame(self.root,fg_color = "transparent")
        self.btmpart.pack(side = "top",anchor = 'w',fill="x",padx=10, pady=5)
        self._bottom()

        #when windows closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        #delete
        self.del_active = False

        #setting
        self.sett_active = False
        self.tmp_setting = []
        td.reads()
        for i in range(1):
            self.tmp_setting.append(bool(td.reads_(i)))

    #when app closing run the command below
    def on_closing(self):
        td.create()
        for i in range(len(self.tmp_setting)):
            td.write_setting(self.tmp_setting[i])
        for i in range(len(self.todolist)):
            if self.tododone[i] and self.tmp_setting[0]:
                continue
            td.write(self.todolist[i],self.tododone[i])
        self.root.destroy()

    #title area
    def _title(self):
        path = sys._MEIPASS + "/pictures/setting.png" if hasattr(sys, '_MEIPASS') else "../pictures/setting.png" #change to ../pictures/setting.png
        try:
            self.setting_img = tk.CTkImage(light_image=Image.open(path),
                                            dark_image=Image.open(path),
                                            size=(30, 30))
        except:
            self.setting_img = None
        label = tk.CTkLabel(self.title, text="To-do list", font=("Impact", 50), text_color="#3282F6", justify="left")
        label.pack(side="left")
        setting_bttn = tk.CTkButton(self.title, image=self.setting_img,text = "",height = 5,width =5,fg_color = "transparent",hover_color = "black",command = lambda: self.setting())
        setting_bttn.pack(side="right",fill="x",padx=5, pady=10)

    #todo area
    def _todoside(self,is_del):

        #destroy all widget
        for widget in self.todoside.winfo_children():
            widget.destroy()

        #put back the new widget
        self.todoside_todo = tk.CTkFrame(self.todoside)
        self.todoside_todo.pack(side = "left",fill = "both")

        #design show todo area
        self._todoside_todo(is_del)

    #show todo area
    def _todoside_todo(self,is_del):
        if len(self.todolist) == 0:
            no_work = tk.CTkLabel(self.todoside_todo, text="\n   hmmmm...\n           seems like you no need to do anything.", font = ("Arial", 15), text_color="white", justify="left")
            no_work.pack()

        for i in range(len(self.todolist)):
            todobox = tk.CTkFrame(self.todoside_todo,width = 40,fg_color = "transparent")
            todobox.pack(side = "top",fill = "x")

            if is_del:
                tododel = tk.CTkButton(todobox, text="X", command=lambda x=i: self.delete(x),width = 25,height = 25,hover_color = "#993030",fg_color="#C73F3F",text_color="white")
                tododel.pack(side = "left",padx = 5)

            todol = tk.CTkCheckBox(todobox,text=self.todolist[i], font=("Arial", 20),variable = tk.BooleanVar(value=self.tododone[i]),command = lambda x = i:self.done(x),height = 20,width = 20 )
            todol.pack(side = "top",pady = 5,anchor = "w")


    #bottom area
    def _bottom (self):
        self.add = tk.CTkEntry(self.btmpart, placeholder_text="Add some To-do...", width=300)
        self.add.pack(padx=3, pady=5, anchor='sw', fill='x')
        add_bttn = tk.CTkButton(self.btmpart, text="ADD", fg_color="#2D9CF6", text_color="white", font=("Arial", 12),width=25, command=self.add_todo)
        add_bttn.pack(side="left", pady=5, padx = 3, anchor="sw")
        reset_bttn = tk.CTkButton(self.btmpart, text="RESET", command=self.reset,hover_color = "#BA9103",fg_color="#DBAB03", text_color="white",font=("Arial", 12), width=25)
        reset_bttn.pack(side="left", pady=5, padx = 3, anchor="sw")
        del_bttn = tk.CTkButton(self.btmpart, text="DELETE", command=self.del_bttn_cmd,hover_color = "#993030",fg_color="#C73F3F",text_color="white", font=("Arial", 12), width=25)
        del_bttn.pack(side="left", pady=5, padx=3, anchor="sw")
        self.add.bind("<Return>", lambda e:self.add_todo())

    def setting(self):
        self.sett_active = not self.sett_active
        if self.sett_active:
            for widget in self.todoside.winfo_children():
                widget.destroy()
            autodelete = CTkCheckBox(self.todoside,text = "Delete completed task after close application",command=lambda:self.change_setting(0),variable = tk.BooleanVar(value=self.tmp_setting[0]))
            autodelete.pack(side="top", padx=5, pady=5, anchor="w")
        else:
            self._todoside(self.del_active)

    def change_setting(self,num):
        self.tmp_setting[num] = not self.tmp_setting[num]


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

    def del_bttn_cmd(self):
        self.del_active = not self.del_active
        self._todoside(self.del_active)


    def delete(self,index):
        self.todolist.pop(index)
        self.tododone.pop(index)
        self._todoside(True)

    def reset(self):
        if td.tips():
            self.todolist.clear()
            self.tododone.clear()
            self._todoside(self.del_active)

    def add_todo(self):
        a_todo = self.add.get()
        if a_todo == "":
            return
        self.todolist.append(bytes(a_todo,"utf-8"))
        self.tododone.append(False)
        self._todoside(self.del_active)
        self.add.delete(0, "end")

    def run(self):
        self.root.mainloop()

    #################################################

if __name__ == "__main__":
    app = Todo()
    app.run()

# built application
# pyinstaller --onefile --runtime-tmpdir "%TEMP%\TodoList_App" --windowed --name "TodoList" --add-data "..\include\libtd.dll;." --add-data "..\pictures;pictures" --hidden-import PIL --hidden-import customtkinter --hidden-import ctypes main.py
# pyinstaller TodoList.spec

# testing
# pyinstaller --onefile  --name "TodoList" --add-data "..\include\libtd.dll;." --add-data "..\pictures\setting.png;." --hidden-import PIL --hidden-import customtkinter --hidden-import ctypes main.py
# pyinstaller TodoList.spec