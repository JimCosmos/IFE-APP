from tkinter import *
from PIL import ImageTk,Image
import sqlite3
from tkinter.font import Font

root = Tk()
root.title("IFE Home")
text = Text(root)

myFont = Font(family="Times New Roman", size=12)
text.configure(font=myFont)


# conn = sqlite3.connect("IFE_APP.db")
# #Cursor instance to create table
# c = conn.cursor()
# Create table
# c.execute("""CREATE TABLE All_Subjects(
#     Code text,
#     Name text,
#     Orientation text,
#     Points text
#     )""")

#Querring delete from My_Subjects
def submit_delete():
    conn = sqlite3.connect("IFE_APP.db")
    c = conn.cursor()

    #Getting subject form All_Subjects and Score from entry 
    c.execute("DELETE from My_Subjects WHERE RealID = " + del_subj_entry.get())

    conn.commit()
    conn.close()
    #Clearing entries
    del_subj_entry.delete(0, END)



def submit_add():
    conn = sqlite3.connect("IFE_APP.db")
    c = conn.cursor()

    #Getting subject form All_Subjects and Score from entry 
    c.execute("INSERT INTO My_Subjects (Code, Name, Orientation, Points, Score, RealID) SELECT *, '"+ subj_mark_entry.get() + "', '"+add_subj_entry.get()+"' FROM All_Subjects WHERE oid = " + str(add_subj_entry.get()))

    conn.commit()
    conn.close()
    #Clearing entries
    add_subj_entry.delete(0, END)
    subj_mark_entry.delete(0, END)

def delete_subjects():
    global delete
    delete=Tk()
    delete.title("Delete a subject from your list")

    #Delete Label
    add_subj_name = Label(delete, text = "Subject's Code")
    add_subj_name.grid(row=0, column = 0, pady = (6,0), columnspan=2)

    #Delete Entry
    global del_subj_entry
    del_subj_entry = Entry(delete, width=30)
    del_subj_entry.grid(row=1, column=0, pady=5)

    #Delete Button
    delete_btn = Button(delete, text="Delete Subject", command = submit_delete)
    delete_btn.grid(row=2, column=0, pady=5)



#Creating pop-up window that allows you to add info to sumbit new passed subject
def add_subjects():
    global add
    add=Tk()
    add.title("Add a subject to your list")



    #Adding Labels
    add_subj_name = Label(add, text = "Subject's Code")
    add_subj_name.grid(row=0, column = 0, pady = (6,0), columnspan=2)
    add_your_mark = Label(add, text = "Your Mark")
    add_your_mark.grid(row=2, column=0, columnspan=2)

    #Adding entries
    global add_subj_entry
    add_subj_entry = Entry(add, width=30)
    add_subj_entry.grid(row=1, column=0, pady=5)
    global subj_mark_entry
    subj_mark_entry = Entry(add, width=30)
    subj_mark_entry.grid(row=3, column=0, pady=5)

    #Adding Submit Button
    submit_new_subj = Button(add, text = "Submit", command =submit_add)
    submit_new_subj.grid(row=4, column=0)

def allquery():
    conn = sqlite3.connect("IFE_APP.db")
    c = conn.cursor()

    # Query the database for all records + oid
    c.execute("SELECT *, oid FROM All_Subjects")
    #oid stands for the primary key

    records = c.fetchall()
    #print(records)
    print_records=""
    for record in records:
        #Printing all records
        print_records += "Κωδικός:" + str(record[0])+ " " + "ID:"+str(record[4]) + " " + "Όνομα:" + str(record[1])+"\n"
    # print(print_records)
    f= open("Mathimata.txt","w+", encoding="utf-8")
    f.write(print_records)
    f.close


    conn.commit()
    conn.close()

def myquery():
    # Tried to open txt file in tkinter window to display greek properly but didn't work
    # global my_window
    # my_window = Tk()
    # T = Text(my_window, state="normal", height=15, width=60)
    # T.pack()
    # T.insert(END, open("Lista Mou.txt").read())

    conn = sqlite3.connect("IFE_APP.db")
    c = conn.cursor()
    c.execute("SELECT * FROM My_Subjects")
    records = c.fetchall()

    print_records=""
    for record in records:
        #Printing All Subjects
        print_records += "Κωδικός:" + str(record[0])+ " " + "Βαθμός:"+str(record[4]) + " " + "Όνομα:" + str(record[1])+"\n"
    # print(print_records)
    f= open("Lista Mou.txt","w+", encoding="utf-8")
    f.write(print_records)
    f.close


    conn.commit()
    conn.close()


#Create a ShowAll Query Button
query_btn = Button(root, text="Show All Subjects", command=allquery)
query_btn.grid(row=1, column=0, columnspan=2, pady=10, padx=10, ipadx=92)

#Create a ShowMySubject Query Button
query_btn = Button(root, text="Show My Subjects", command=myquery)
query_btn.grid(row=2, column=0, columnspan=2, pady=10, padx=10, ipadx=92)

#Adding Add Subject Button
add_btn = Button(root, text="Add A Subject", command=add_subjects)
add_btn.grid(row=3, column=0, columnspan=2, pady=10, padx=10, ipadx=103)

#Delete from My Subjects
delete_btn = Button(root, text="Delete A Subject", command=delete_subjects)
delete_btn.grid(row=4, column=0, columnspan=2, pady=10, padx=10, ipadx=92)

# conn.commit()
# conn.close()


root.mainloop()