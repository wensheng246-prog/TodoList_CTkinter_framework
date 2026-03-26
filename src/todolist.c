#include <stdio.h>
#include <string.h>
#include <windows.h>
#include <stdbool.h>
#define RED "\033[31m"
#define WHITE "\033[37m"

struct TOD{
    char todo[100];
    bool done;
};

int sztodo = sizeof(struct TOD);

struct TOD todo;
char todo_a[260];

char* get_path(){
    GetModuleFileName(GetModuleHandle(NULL), todo_a, 260);
    char* last = NULL;
    for (char* p = todo_a; *p; p++) {
        if (*p == '\\') *p = '/';
    }
    for(int i = 0;i<1;++i){
        last = strrchr(todo_a,'/');
        if(last){
            *last = '\0';
        }
    }
    strcat(todo_a,"/todo.dat");
    return todo_a;
}

bool tips(){
    int result = MessageBoxW(NULL,L"Do you want to reset?",L"Reset Notice",MB_YESNO|MB_ICONQUESTION|MB_DEFBUTTON2);
    switch (result){
        case IDYES:
            return true;
        case IDNO:
            return false;
    }
    return false;
}

void notice(){
    printf("\n"RED"If you are testing this application, after this please delete the file show below\n"WHITE);
    printf(todo_a);
}

void create(){
    fopen(todo_a,"wb");
}

void databasederr(){
    int result = MessageBoxW(NULL,L"Databased doesn't exist. Do you want to create a databased?",L"Error Notice",MB_YESNO|MB_ICONERROR|MB_DEFBUTTON2);
    switch (result){
        case IDYES:
            create();
            return;
        case IDNO:
            return;
    }
}

char * read(int i){
    strcpy(todo.todo,"\0");
    FILE * fp = fopen(get_path(),"r+b");
    if(fp == NULL){
        databasederr();
        return todo.todo;
    }

    char * tmp = 0;
    fseek(fp,i*sztodo,SEEK_SET);
    if(fread(&todo,sztodo,1,fp)){
        return todo.todo;
    }
    return todo.todo;
}

bool readb(int i){
    strcpy(todo.todo,"\0");
    FILE * fp = fopen(get_path(),"r+b");
    if(fp == NULL){
        return todo.done;
    }

    char * tmp = 0;
    fseek(fp,i*sztodo,SEEK_SET);
    if(fread(&todo,sztodo,1,fp)){
        return todo.done;
    }
    return todo.done;
}

void write(char * in,bool done){
    FILE * fp = fopen(get_path(),"a+b");
    if (fp==NULL){
        databasederr();
    }
    fseek(fp,0,SEEK_END);
    fwrite(in,sizeof(char[100]),1,fp);
    fwrite(&done,sizeof(bool),1,fp);
    fclose(fp);
}

// D:\todo_list\databased\todo.dat
//gcc -m64 -shared -o D:\\todo_list\\include\\libtd.dll D:\todo_list\src\todolist.c