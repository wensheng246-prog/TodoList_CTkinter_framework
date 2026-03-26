# To-do List
>Hi, this is my first project!
A simple todo list built with **Python** and **C**

## Tech Stack
| Technology | Purpose |
|----------------------|---------|
| **Python** | main application logic |
| **CustomTkinter** | GUI Framework |
| **C** | data stroage backend |
| **PyInstaller** | package to executable |

## clone project
https://github.com/wensheng246-prog/TodoList_CTkinter_framework

## install dependencies
pip install customtkinter
pip install pyinstaller

## run the application
>>Please change the file location in main.py (line 4)
main.py

## built application
>>In cmd prompt cd to your "../todolist/src" file and run the command below
pyinstaller --onefile --windowed --name "TodoList" --add-data "..\include\libtd.dll;." --hidden-import customtkinter --hidden-import ctypes main.py
>>After run the first command run the command below
pyinstaller TodoList.spec