"""A simple Text-editor and a pad beside it"""

from tkinter import *
from tkinter import messagebox, ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.colorchooser import askcolor
from PIL import ImageGrab, ImageDraw, Image, ImageTk
import time
import os
import subprocess

class AppTextPad():
    def __init__(self, master):
        self.master = master
        self.brush_width = 5
        self.brush_color = "black"
        self.old_x = None
        self.old_y = None
        self.count = 0
        self.img_dict= {}
        self.window_main()
        self.canvas()

    #function to adjust the background-color of the text-box
    def color_adjustment_bg(self):
        color = askcolor()[1]
        self.text_box["bg"] = color

    #function to adjust the text color of the text-box
    def color_adjustment(self):
        color = askcolor()[1]
        self.text_box["fg"] = color

    #function to adjust the blue color of text in menu-bar
    def blue_func(self):
        color = askcolor(color="blue")[1]
        self.text_box["fg"] = color

    #function to adjust the red color of text in menu-bar
    def red_func(self):
        color = askcolor(color="red")[1]
        self.text_box["fg"] = color

    #function to adjust the yellow color of text in menu-bar
    def yellow_func(self):
        color = askcolor(color="yellow")[1]
        self.text_box["fg"] = color

    #function to adjust the cyan color of text in menu-bar
    def cyan_func(self):
        color = askcolor(color="cyan")[1]
        self.text_box["fg"] = color

    #function to adjust the magenta color of text in menu-bar
    def magenta_func(self):
        color = askcolor(color="magenta")[1]
        self.text_box["fg"] = color

    #function to adjust the black color of text in menu-bar
    def black_func(self):
        color = askcolor(color="black")[1]
        self.text_box["fg"] = color

    #function to adjust the white color of text in menu-bar
    def white_func(self):
        color = askcolor(color="white")[1]
        self.text_box["fg"] = color

    #function to clean all the text
    def clean_text_box(self):
        self.text_box.delete("1.0", END)

    #function to open a file and copy the text into the text-box
    def open_file(self):
        path = askopenfilename(defaultextension="*.*",filetypes=[("All Files", "*.*"), ("Text File", ".txt"), ("PDF File", ".pdf")])
        if not path:
            return self.error_box()
        with open(path, mode="r", encoding="utf-8") as file:
            text = file.readlines()
            for line in text:
                line.rstrip()
                self.text_box.insert(END, line) 
        #self.master.title(f"Simple Text Editor - {path}")

    #method to add image into text_box
    def import_img_into_text(self):
        path = askopenfilename(defaultextension=".jpg", filetypes=[("All Files", "*.*"), ("PS Files", ".ps")])
        if path:
            img = ImageTk.PhotoImage(Image.open(path))
            self.text_box.insert(END, "\n")
            self.text_box.image_create(END, image= img)
            self.text_box.image= img
            self.text_box.insert(END, "\n")
        else:
            messagebox.showerror("Path-Error", "The path doesn´t exist")

    #method to save the file 
    def saveas_file(self):
        path = asksaveasfilename(defaultextension="*.txt", filetypes=[("Text File", ".txt"),("PDF File", ".pdf"), ("All Files", "*.*")])
        if not path:
            return self.error_box()
        with open(path, "w") as file:
            text = self.text_box.get("1.0", END)
            file.write(text)
        #self.master.title(f"Simple Text Editor -{path}")

    #method of save as button and then exit the text-editor
    def save_and_exit(self):
        self.saveas_file()
        self.master.destroy()

    #method to show a pop-up window, in case you havenot opened or saved the file correctly
    def error_box(self):
        messagebox.showerror("Upps", "something went wrong, Maybe not opened or saved correctly!")

    #a pop-up window to show the basic info about open-source code
    def message_box(self):
        messagebox.showinfo("About this app", "This Application is developed by\
                            Ismail Mostafanejad in 2022 - aim of portfolio. It is an open source code/ writtten in Python!")

    #method to erase the text-box (Page)
    def clear_page(self):
        self.text_box.delete("1.0", END)

    #method to find the searched keyword
    def find(self, input_entry):
        input_box = self.text_box.get("1.0", END).split("\n")
        dict = {}
        for i, line in enumerate(input_box):
            count = line.count(input_entry)
            idx = 0
            for j in range(count):
                idx = line.find(input_entry, idx, len(line))
                if i+1 not in dict: 
                    dict[i+1] = []
                    dict[i+1].append(idx)
                else:
                    dict[i+1].append(idx)
                idx +=len(input_entry)
        return dict

    #function to search the keyword. it is needs above function: find
    def search(self):
        input_entry = self.entry_search.get()
        dict= self.find(input_entry)
        for key, val in dict.items():
            for v in val:
                idx_start, idx_end = f"{key}.{v}", f"{key}.{v + len(input_entry)}"
                self.text_box.tag_config("start", foreground="red")
                self.text_box.tag_add("start", idx_start, idx_end)

    #complicated method to replace all. Simple method is below. it needs find function.
    def replaceall(self):
        input_entry_search = self.entry_search.get()
        input_entry_replace = self.entry_replace.get()
        length = len(input_entry_search) - len(input_entry_replace)
        dict = self.find(input_entry_search)
        for key, val in dict.items():
            diff = 0
            for v in val:
                idx_start, idx_end = f"{key}.{v+diff}", f"{key}.{v + len(input_entry_search)+diff}"
                self.text_box.delete(idx_start, idx_end)
                self.text_box.insert(idx_start , input_entry_replace)
                diff -= length

    #simple function of replace. the complicated function is above! this replaces first found word 
    def replace(self):
        input_search = self.entry_search.get()
        input_replace= self.entry_replace.get()
        text = self.text_box.get("1.0", END).split("\n")
        i = 0
        for line in text:
            if input_search not in line:
                i+=1
            else:
                idx_start, idx_end = "", ""
                idx_start = line.find(input_search)
                idx_end = idx_start + len(input_search)
                idx_start, idx_end = f"{i+1}.{idx_start}", f"{i+1}.{idx_end}"
                self.text_box.delete(str(idx_start), str(idx_end))
                self.text_box.insert(idx_start, input_replace)
                i+=1
                break

    #function for undo in menu-Edite
    def undo(self):
        self.text_box.edit_undo()

    #function for redo in menu-Edite
    def redo(self):
        self.text_box.edit_redo()

    #function for most common converters, which will be added later
    def converters(self):
        pass

    #a new window for archive
    def open_new_win(self):
        new_win= Tk()
        new_win.title("Archive")
        text_b = Text(new_win)
        text_b.grid(row=0, column=0)
        butt= Button(new_win, text="Close Window", command=new_win.destroy)
        butt.grid(row=1, column=0, sticky=EW)
        f= open("archive.txt", "r")
        list=[]
        lines= f.readlines()
        for line in lines:
            word = line.rstrip()
            if word not in list:
                list.append(word)
        text_b.insert("1.0", "A list of archieve: "+str(list))
        f.close()

    #Two Methods to hide and show the Menu-Ffame at LEFT of window
    def hide_frame_left(self):
        self.frame_left.grid_forget()

    def show_frame_left(self):
        self.frame_left.grid(row=0, column=0, rowspan=20, columnspan=1, sticky=NSEW)
            
    def window_main(self):
        #code of the main window
        self.win= Frame(self.master)
        self.win.pack(side=LEFT, fill=BOTH, expand=True)
        self.win.rowconfigure([0,1,2,3,4,5,6,7,8,9], weight=1, minsize=1)
        self.win.columnconfigure([0,1,2], weight=1, minsize=5)

        #LabelFrame for all buttons and entries in left-menu, in column 0
        self.frame_left= LabelFrame(self.win)
        for i in range(50):
            self.frame_left.rowconfigure([i], weight=1, minsize=0)
        #Buttons and Entries within frame_left
        self.entry_search= Entry(self.frame_left, width=17)
        button_search= Button(self.frame_left, text="Search ", relief=GROOVE, command=self.search)

        self.entry_replace = Entry(self.frame_left, width=17)
        button_replace= Button(self.frame_left, text="Replace", command=self.replace)
        button_replaceall= Button(self.frame_left, text="Rep. All ", relief=GROOVE, command=self.replaceall)

        sep1= ttk.Separator(self.frame_left, orient="horizontal")

        labels_space= Label(self.frame_left, text=" ", padx=50, pady=50)

        sep2= ttk.Separator(self.frame_left, orient="horizontal")

        button_info = Button(self.frame_left, text="About         ", relief=RAISED, command=self.message_box)
        button_saveexit = Button(self.frame_left, text="Save & Exit", relief=RAISED, command=self.save_and_exit)
        button_exit=Button(self.frame_left, text="Hide Text    ", relief=RAISED, command=self.win.destroy)
        button_hide_frame_left= Button(self.frame_left, text="\N{LEFTWARDS ARROW}- Hide menu", command=self.hide_frame_left)

        button_search.grid(row=4, column=1, rowspan=1, sticky=EW)
        self.entry_search.grid(row=4, column=0, rowspan=1, sticky=EW)
        self.entry_replace.grid(row= 5, column=0, rowspan=1, sticky=EW)
        button_replace.grid(row=5, column=1, sticky=EW)
        button_replaceall.grid(row=6, column=1, rowspan=1, sticky=EW)
        sep1.grid(row=7, column=0, rowspan=1, columnspan=2, sticky=EW)
        labels_space.grid(row= 9, sticky=EW)
        sep2.grid(row=45, column=0, columnspan=2, rowspan=1, sticky=EW)
        button_info.grid(row=46, column=1, sticky=EW)
        button_saveexit.grid(row=47, column=1, sticky=EW)
        button_exit.grid(row=48, column=1, rowspan=1, columnspan=1, sticky=EW)
        button_hide_frame_left.grid(row=49, column=0, sticky=W)
        self.frame_left.grid(row=0, column=0, rowspan=20, columnspan=1, sticky=NS ,padx=2, pady=5)


        #Text-box and its scrollbar in column 1 and 2
        self.text_box = Text(self.win, bg="white", undo=True, maxundo=-1, font="Helvetica")
        scroll_bar = Scrollbar(self.win, orient="vertical")

        self.text_box.grid(row=0, column=1, rowspan=10, sticky=NSEW, padx=0)
        scroll_bar.grid(row=0, column=2, rowspan=10, sticky=NS, padx=0)

        self.text_box.config(yscrollcommand = scroll_bar.set)
        scroll_bar.config(command=self.text_box.yview)

        menubar = Menu(self.win)
        root.config(menu=menubar)

        file = Menu(menubar, activebackground="cyan", tearoff=0)
        menubar.add_cascade(menu=file, label="FILE")
        file.add_command(label="New File", command=self.clean_text_box)
        file.add_command(label="Import File", command=self.open_file)
        file.add_command(label="Import image", command= self.import_img_into_text)
        file.add_command(label="Save As", command=self.saveas_file)
        file.add_separator()
        file.add_command(label="Exit", command=self.master.destroy)

        editing = Menu(menubar, activebackground="light blue", tearoff=0)
        menubar.add_cascade(menu=editing, label="EDIT")
        editing.add_command(label="Undo", command=self.undo)
        editing.add_command(label="Redo", command=self.redo)
        editing.add_command(label="Show Archive", command=self.open_new_win)
        #editing.add_command(label="Edit", command=None)
        editing.add_command(label="Clear page", command=self.clear_page)

        tools = Menu(menubar)
        tools.add_cascade(menu=tools,label="TOOLS")
        tools.add_command(label="Pen", command=None)
        tools.add_command(label="Brush", command=None)
        tools.add_separator()
        tools.add_command(label="Erase", command=None)

        #the methods for fontsize-adjustment are defined inside the menu to avoid extra place
        size = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=size, label="SIZE")
        size.add_command(label="0.5x", command=lambda: self.text_box.config(font=("Helvetica",10)))
        size.add_command(label="1x", command=lambda: self.text_box.configure(font=("Helvetica", 11)))
        size.add_command(label="2x", command=lambda: self.text_box.config(font=("Helvetica", 12)))
        size.add_command(label="3x", command=lambda: self.text_box.config(font=("Helvetica", 13)))

        color = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=color, label="COLOR")
        color.add_command(label="Blue", command= self.blue_func)
        color.add_command(label="Red", command=self.red_func)
        color.add_command(label="Yellow", command=self.yellow_func)
        color.add_command(label="Cyan", command=self.cyan_func)
        color.add_command(label="Magenta", command=self.magenta_func)
        color.add_separator()
        color.add_command(label="Color Bar", command=self.color_adjustment)

        color_background = Menu(menubar, tearoff=0)
        menubar.add_cascade(label="BG-COLOR", menu=color_background)
        color_background.add_command(label="Color Chooser", command=self.color_adjustment_bg)
        
        #SHOW/HIDE in menubar
        self.show_hide = Menu(menubar, tearoff=0)
        menubar.add_cascade(menu=self.show_hide, label="HIDE/SHOW")
        self.show_hide.add_command(label="Hide left-menu", command=self.hide_frame_left)
        self.show_hide.add_command(label="Show lrftmenu", command=self.show_frame_left)
        self.show_hide.add_command(label="Hide Pad", command=self.hide_frame_canvas)
        self.show_hide.add_command(label="Show Pad", command=self.show_frame_canvas)

        #popup-menu on the textbox
        self.menu_popup = Menu(self.win, tearoff=0)
        self.menu_popup.add_command(label="copy", command= lambda: self.copy())
        self.menu_popup.add_command(label="paste", command=lambda: self.paste())
        self.menu_popup.add_command(label="cut", command= lambda: self.cut())
        self.menu_popup.add_command(label="Archive", command=lambda: self.archive())
        self.text_box.bind("<Button-3>", self.do_popup)

    #Methods of pupup menu for text-pad are below until Canvas to avoid many methods together
    #Method of popup with right-click on text_box
    def do_popup(self, event):
        try:
            self.menu_popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.menu_popup.grab_release()

    #Method to copy selected text
    def copy(self):
        if self.text_box.selection_get():
            self.data= self.text_box.selection_get()
        #e.bind("<Control-c>")

    #Method to cut selected text
    def cut(self):
        if self.text_box.selection_get():
            self.data= self.text_box.selection_get()
            self.text_box.delete("sel.first", "sel.last")
        #text_box.bind("<Control+x>")

    #Method to paste selected text
    def paste(self):
        self.text_box.insert(END, self.data)

    #Method to archive selected text for later use. This is connected with show-archive butten
    def archive(self):
        if self.text_box.selection_get():
            word= self.text_box.selection_get()
            word= str(word)
            filename= "archive.txt"
            if filename:
                with open(filename, "a") as f:
                    f.write("\n")
                    f.write(word)
            else:
                with open(filename, "w"):
                    f.write(word)


    """Canvas code beside the Text_box. the methods belonging to Canvas
    are below it to avoid many confusion of many methods within text_pad"""
                        
    def canvas(self):
        #all labels, buttons and scales on the pad
        self.frame_canvas= LabelFrame(self.master, text= "Write or paint on the pad")
        self.frame_canvas.pack(side=RIGHT, fill=BOTH, expand=True)

        self.c = Canvas(self.frame_canvas, bg="white", height=580)
        self.c.pack(side=TOP , expand=True, fill=BOTH)

        #all buttons, scale in a labelframe
        frame_all_butts= LabelFrame(self.frame_canvas)
        label_import_img= Button(frame_all_butts, text="Save Photo", relief=RAISED, command=self.save_image_as)
        label_control = Label(frame_all_butts, width=15, text="Pen Width \N{RIGHTWARDS ARROW}")
        scale_control = ttk.Scale(frame_all_butts, from_=5, to=100,  command= self.brush_size_change)
        scale_control.set(self.brush_width)

        button_brush_color= Button(frame_all_butts, text="Brush Color ", command=self.brushcolor)
        button_bg_color= Button(frame_all_butts, text="BG Color   ", relief=SUNKEN, command=self.background_color)
        button_canvas_clear = Button(frame_all_butts, text="Clear Pad    ", relief=FLAT, command=self.clear_canvas)
        button_canvas_into_text= Button(frame_all_butts, text="\N{LEFTWARDS ARROW}--- Push image into text", command=self.push_img_into_text)
        hide_show_butt_canvas= Button(frame_all_butts, text="Hide Pad -\N{RIGHTWARDS ARROW}", command=self.hide_frame_canvas)

        frame_all_butts.pack(side=BOTTOM, expand=True, fill=BOTH, padx=5, pady=5)
        label_import_img.grid(row=0, column=0, sticky=W, pady=5)
        label_control.grid(row=0, column=1, pady=5)
        scale_control.grid(row=0, column=2, sticky=E, pady=5)
        button_brush_color.grid(row= 1, column=0, sticky=W)
        button_bg_color.grid(row=1, column=1)
        button_canvas_clear.grid(row=1 ,column=2 ,sticky=E)
        button_canvas_into_text.grid(row=2, columnspan=3, sticky=EW, pady=5)
        hide_show_butt_canvas.grid(row=3, column=2, sticky=E, pady=5)

        self.c.bind("<B1-Motion>", self.paint)
        self.c.bind("<ButtonRelease-1>", self.reset)

        #canvas popup-menu separately from textbox menu
        self.canvas_popup = Menu(self.c, tearoff=0)
        self.canvas_popup.add_command(label="Push into text", command=self.push_img_into_text)
        self.canvas_popup.add_command(label="import imgae", command=self.import_img)
        self.canvas_popup.add_command(label="Save image", command=self.save_image_as)
        self.canvas_popup.add_command(label="clear Pad", command=self.clear_canvas)
        self.canvas_popup.add_command(label="Exit Pad", command=self.c.destroy)
        self.c.bind("<Button-3>", self.do_canvas_popup)

    #Method to change pen-color
    def brushcolor(self):
        color = askcolor()[1]
        self.brush_color = color

    #Method to change background-color of the pad
    def background_color(self):
        color = askcolor()[1]
        self.c["bg"] = color

    #Method to change the size of the pen
    def brush_size_change(self, width):
        self.brush_width= width

    #Method to paint on the pad
    def paint(self, e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x, self.old_y, e.x, e.y, width= self.brush_width, fill=self.brush_color, capstyle="round")
            #self.coords.extend((int(self.old_x), int(self.old_y)))
        self.old_x = e.x
        self.old_y = e.y

    #Method, which resets the pad as soon as you finish a line
    def reset(self, e):
        e.x = None
        e.y = None
        self.old_x, self.old_y = None, None

    #Method to erase the pad
    def clear_canvas(self):
        self.c.delete(ALL)

    #Method push image from canvas into the text
    def push_img_into_text(self, file_name="push"):
        self.c.postscript(file=f"{file_name}{self.count}.ps", colormode="color")
        process = subprocess.Popen(["ps2pdf", f"{file_name}{self.count}.ps", "sth.pdf"], shell=True)
        process.wait(1)
        img = ImageTk.PhotoImage(Image.open(f"{file_name}{self.count}.ps"))
        self.text_box.insert(END, "\n")
        self.text_box.image_create(END, image= img)
        #collecting the images in a dictionary
        if self.count not in self.img_dict:
            self.img_dict[f"{file_name}{self.count}"] = img
        self.text_box.insert(END, "\n")
        self.count +=1

    #Method of a pop-up window to insert the file-name. it will bind with creat_img function.
    def save_image_as(self):
        self.win_save_as = Tk()
        self.win_save_as.title("Enter file-name")
        self.entry_save_as = Entry(self.win_save_as)
        self.entry_save_as.grid(row=0, column=0)
        button_save_as= Button(self.win_save_as,text="Save", command=self.creat_img)
        button_save_as.grid(row=0, column=1)

    #Method to save the image as .ps
    def create_img(self, file_name="temp"):
        file_name= self.entry_save_as.get()
        self.c.postscript(file=f"{file_name}.ps", colormode="color")
        process = subprocess.Popen(["ps2pdf", f"{file_name}.ps", "result.pdf"], shell=True)
        process.wait(1)
        self.win_save_as.destroy()

    #Method of importing image
    def import_img(self):
        path = askopenfilename(defaultextension=".jpg", filetypes=[("All Files", "*.*"), ("PS Files", ".ps")])
        if path:
            self.img = ImageTk.PhotoImage(Image.open(path))
            self.c.create_image(20, 20, anchor=NW, image= self.img)
            self.c.image= self.img
        else:
            messagebox.showerror("Path-Error", "The path doesn´t exist")

    #Method of popup with right-click on text_box
    def do_canvas_popup(self, event):
        try:
            self.canvas_popup.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.canvas_popup.grab_release()
    
    #methods hiding frame_canvas
    def hide_frame_canvas(self):
        self.frame_canvas.pack_forget()

    def show_frame_canvas(self):
        self.frame_canvas.pack(side=RIGHT, fill=BOTH, expand=True)


if __name__ == "__main__":
    root = Tk()
    root.title("Text Editor")
    AppTextPad(root)
    root.mainloop()