'''
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
#####
Katie Chiu
Quick Lunch
Version 1.0
Last updated 17 December 2018
Program that lets cashiers calculate each employees' total price and let them checkout in the cafeteria.
'''

from tkinter import *
from tkinter import ttk

class App:
    def __init__(self):
        self.x=20
        self.y=[]

        self.prices = [1,1,.75,1.25,1,3,4,3.75,4,15,20]
        self.albums = ["soda","tea","milk","juice","water","Sandwich - $3","Pizza - $4","Chicken Nuggets - $3.75","Chicken - $4","Tofu - $15","Clam Chowder - $20"]

        self.content = Frame()  # frame to hold widgets together
        self.frame=Frame(self.content)

        self.drinkslabel = Label(self.content, text="Drinks")  # label for question
        self.drink = StringVar()
        self.drink.set(0)  # nothing selected
        self.soda = Radiobutton(self.frame, text="Soda - $1", variable=self.drink,
                                 value="soda",command=self.progressdrink)  # radiobuttons with possible answers
        self.tea = Radiobutton(self.frame, text="Tea - $1", variable=self.drink, value="tea",command=self.progressdrink)
        self.milk = Radiobutton(self.frame, text="Milk - $.75", variable=self.drink, value="milk",command=self.progressdrink)
        self.juice = Radiobutton(self.frame, text="Juice - $1.25", variable=self.drink, value="juice",command=self.progressdrink)
        self.water=Radiobutton(self.frame,text="Bottled Water - $1", variable=self.drink,value="water",command=self.progressdrink)

        self.entreelabel = Label(self.content, text="Entrees")  # label for question
        self.entrees = Listbox(self.content, height=9,width=25, selectmode="SINGLE",exportselection=FALSE)  # listbox for items on sale
        self.entrees.bind("<<ListboxSelect>>",self.progressentree)
        for b in ["Sandwich - $3","Pizza - $4","Chicken Nuggets - $3.75","Chicken - $4","Tofu - $15","Clam Chowder - $20"]:
            self.entrees.insert(END, b)  # Adds values to listbox
        self.warning=Label(self.content,text="Chowder is Gluten, soy, and shellfish free")

        self.spinval = StringVar()
        self.s = Spinbox(self.content, values=(
        "Monday", "Tuesday", "Wednesday", "Thursday", "Friday"), textvariable=self.spinval, wrap=True, width=20, state="readonly")

        self.paymentval=StringVar()
        self.payment = ttk.Combobox(self.content, state="readonly", textvariable=self.paymentval,width=19)  # combobox
        self.payment["values"] = ["Credit", "Cash", "Check"]  # values
        self.payment.bind("<<ComboboxSelected>>",self.addpayment)  # applies selected value
        self.payment.bind("<FocusIn>", self.restart)

        self.employee=Label(self.content,text="Employee ID:")
        self.id = StringVar()
        self.id.set("")
        self.employeeid = Entry(self.content, textvariable=self.id,width=20)  # entry for last name

        self.menubar = Menu(root)  # menubar
        self.filemenu = Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="File", menu=self.filemenu)  # creates option in menubar
        self.filemenu.add_command(label="Clear",command=self.clear)
        self.filemenu.add_command(label="Calculate",command=self.add)
        self.filemenu.add_command(label="Checkout",command=self.finish)
        self.filemenu.add_command(label="Exit", command=root.quit)

        self.menubar2 = Menu(root)  # 2nd menu for "help"
        self.helpmenu = Menu(self.menubar2, tearoff=0)
        self.menubar.add_cascade(label="Help", menu=self.helpmenu)  # creates option in menubar
        self.helpmenu.add_command(label="About", command=self.about)  # option in help
        self.helpmenu.add_command(label="Instructions",command=self.instruct)
        root.config(menu=self.menubar)

        self.progress = ttk.Progressbar(self.content, orient=VERTICAL, length=200, mode='determinate')  # progressbar
        self.progress["value"] = self.x

        self.calc=Button(self.content,text="CALCULATE",command=self.add)
        self.check=Button(self.content,text="CHECKOUT",command=self.finish)
        self.price=Label(self.content,text="Total: $0")
        self.error=Label(self.content,text="")

        self.gridall()

    def gridall(self):
        self.content.grid(column=0, row=0,sticky=NSEW)
        self.frame.grid(column=0,row=1,rowspan=5,sticky=NSEW)
        self.drinkslabel.grid(column=0,row=0,sticky=NSEW)
        self.entreelabel.grid(column=1,row=0,columnspan=2,sticky=NSEW)
        self.soda.grid(column=0,row=0,sticky=W)
        self.tea.grid(column=0,row=1,sticky=W)
        self.milk.grid(column=0,row=2,sticky=W)
        self.juice.grid(column=0,row=3,sticky=W)
        self.water.grid(column=0,row=4,sticky=W)
        self.entrees.grid(column=1,row=1,rowspan=5,columnspan=2,sticky=NSEW,padx=10)
        self.s.grid(column=0,row=6,pady=10,sticky=NSEW,padx=5)
        self.payment.grid(column=0,row=7,sticky=NSEW,padx=5)
        self.employee.grid(column=1,row=7,sticky=NSEW,padx=10)
        self.employeeid.grid(column=2,row=7,sticky=NSEW,padx=10)
        self.progress.grid(column=3,row=1,rowspan=7,padx=10,sticky=NSEW)
        self.warning.grid(column=1,columnspan=2,row=6,padx=10,sticky=NSEW)
        self.price.grid(column=1, row=8,pady=10,sticky=NSEW)
        self.calc.grid(column=0,row=8,sticky=NSEW,pady=(30,0),padx=10)
        self.check.grid(column=0,row=9,sticky=NSEW,pady=0,padx=10)
        self.error.grid(column=1,row=9,sticky=NSEW,columnspan=2)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        self.content.columnconfigure(0,weight=1)
        self.content.columnconfigure(1,weight=1)
        self.content.columnconfigure(2,weight=1)
        self.content.columnconfigure(3,weight=1)
        self.content.rowconfigure(0,weight=1)
        self.content.rowconfigure(1, weight=1)
        self.content.rowconfigure(2, weight=1)
        self.content.rowconfigure(3, weight=1)
        self.content.rowconfigure(4, weight=1)
        self.content.rowconfigure(5, weight=1)
        self.content.rowconfigure(6, weight=1)
        self.content.rowconfigure(7, weight=1)
        self.content.rowconfigure(8,weight=1)
        self.content.rowconfigure(9,weight=1)
        self.frame.columnconfigure(0,weight=1)
        self.frame.rowconfigure(0,weight=1)
        self.frame.rowconfigure(1,weight=1)
        self.frame.rowconfigure(2,weight=1)
        self.frame.rowconfigure(3,weight=1)
        self.frame.rowconfigure(4,weight=1)
        self.frame.rowconfigure(5,weight=1)

    def restart(self, event):  # leaves combobox blank
        event.widget.master.focus_set()

    def progressdrink(self):
        if "drink" not in self.y:
            self.x = self.x+20
            self.progress["value"] = self.x
            self.y.append("drink")

    def progressentree(self,root):
        if "entree" not in self.y:
            self.x=self.x+20
            self.progress["value"]=self.x
            self.y.append("entree")

    def addpayment(self,root):
        if "payment" not in self.y:
            self.x=self.x+20
            self.progress["value"]=self.x
            self.y.append("payment")

    def about(self):
        top = Toplevel(root)
        top.title("About")
        label = Label(top,text="Katie Chiu\nQuick Lunch\nVersion 1.0")
        label.pack()
        button = Button(top, text="Close", command=top.destroy)
        button.pack()
        top.geometry("250x150")
        top.resizable(width=False, height=False)

    def add(self):
        chosen=[]
        total=0
        values = [self.entrees.get(idx) for idx in self.entrees.curselection()]
        if values!=[] and self.drink.get!="0":
            values.append(self.drink.get())
            for y in values:
                z = self.albums.index(y)
                chosen.append(z)
            for y in chosen:
                a = self.prices[y]
                total = total + a
            tax=int(total)*.0825
            total=total+tax
            self.price.config(text="Total: $" + str(total))
        else:
            self.error.config(text="Please select a drink and meal")

    def finish(self):
        print(self.drink.get())
        values = [self.entrees.get(idx) for idx in self.entrees.curselection()]
        if self.id.get()=="":
            self.error.config(text="Please enter ID")
        elif self.drink.get()=="0":
            self.error.config(text="Please select a drink")
        elif values==[]:
            self.error.config(text="Please select a meal")
        elif self.paymentval.get()=="":
            self.error.config(text="Please select payment option")
        else:
            self.clear()

    def clear(self):
        self.id.set("")
        self.drink.set(0)
        self.entrees.bind(self.entrees.selection_clear(0, END))
        self.progress["value"] = 20
        self.error.config(text="")
        self.paymentval.set("")
        self.spinval.set("Monday")

    def instruct(self):
        top = Toplevel(root)
        top.title("How to Use")
        label = Label(top,text="Select your drink and meal\nThe button calculate will calculate your total\nThe button checkout will allow you to order your meal\nand drink\nPlease fill out all the information")
        label.pack()
        button = Button(top, text="Close", command=top.destroy)
        button.pack()
        top.geometry("300x150")
        top.resizable(width=False, height=False)


root = Tk()
app = App()
root.title("Quick Lunch")
root.mainloop()
root.destroy()