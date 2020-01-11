from tkinter import *
from PIL import ImageTk,Image
import sqlite3
from tkinter import messagebox
import webbrowser

root = Tk()
root.title("IFE Home")
text = Text(root)

# myFont = Font(family="Times New Roman", size=12)
# text.configure(font=myFont)


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
    #Will need this on #3 check to see if a subject already exists in My_Subjects
    conn = sqlite3.connect("IFE_APP.db")
    dupl=conn.cursor()
    dupl.execute("SELECT COUNT(RealID) FROM My_Subjects WHERE RealID = " + add_subj_entry.get())
    duplcheck = dupl.fetchall()
    conn.commit()
    #Checking MARK input
    # 1-Checking if the given value is in range(5,11) and is an int (and not a float) but allowing labs to be passed in without a score
    if (subj_mark_entry.get() == "" or int(subj_mark_entry.get()) not in range(5,11,1)) and int(add_subj_entry.get()) not in range (100,102):
        messagebox.showerror("Invalid Input", "Your mark should be in range (5,10)")
    # 2-Checking if subject ID is in range(1,102) and is an int (and not a float)
    elif int(add_subj_entry.get()) not in [i for i in range(1,102,1)]:
        messagebox.showerror("Invalid Input", "The subject ID does not exist")
    # 3-Checking if subject already exists in My_Subjects (I will create a list)
    elif duplcheck[0][0] == 1:
        messagebox.showerror("Invalid Input", "The subject is already registered")

    # 4-Everything is ok - proceeding with the query
    else:
        if int(add_subj_entry.get()) in range (100,102):
            c = conn.cursor()

            #Getting subject form All_Subjects and Score from entry 
            c.execute("INSERT INTO My_Subjects (Code, Name, Orientation, Points,  RealID) SELECT *, '"+add_subj_entry.get()+"' FROM All_Subjects WHERE oid = " + str(add_subj_entry.get()))

            conn.commit()
            conn.close()
        else:
            c = conn.cursor()

            #Getting subject form All_Subjects and Score from entry 
            c.execute("INSERT INTO My_Subjects (Code, Name, Orientation, Points, Score, RealID) SELECT *, '"+ subj_mark_entry.get() + "', '"+add_subj_entry.get()+"' FROM All_Subjects WHERE oid = " + str(add_subj_entry.get()))

            conn.commit()
            conn.close()
            print(duplcheck)
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
    #Launching Mathimata.txt file in web browser
    webbrowser.open("Mathimata.txt")

    conn.commit()
    conn.close()

def myquery():
    conn = sqlite3.connect("IFE_APP.db")
    passed = conn.cursor()

    #Getting all passed classes
    passed.execute("SELECT * FROM My_Subjects")
    records = passed.fetchall()
    conn.commit()

    #Getting avarage score(grade)
    avg = conn.cursor()
    avg.execute("SELECT AVG(Score) FROM My_Subjects")
    avgscore = avg.fetchall()
    conn.commit()

    #Getting total Points (ECTS)
    point = conn.cursor()
    point.execute("SELECT SUM(Points) FROM My_Subjects")
    totalpoints = point.fetchall()
    conn.commit()

    #Getting passed core curriculum
    #'Y' is greek
    ypo = conn.cursor()
    ypo.execute("SELECT COUNT(RealID) FROM My_Subjects WHERE Orientation = 'Υ'")
    totalypo = ypo.fetchall()
    conn.commit()

    #Getting optional core corriculumn
    ypoi = conn.cursor()
    ypoi.execute("SELECT COUNT(RealID) FROM My_Subjects WHERE Orientation = 'ΥEΙ'")
    totalypoi = ypoi.fetchall()
    conn.commit()

    ypof = conn.cursor()
    ypof.execute("SELECT COUNT(RealID) FROM My_Subjects WHERE Orientation = 'ΥEΦ'")
    totalypof = ypof.fetchall()
    conn.commit()

    #Getting optional core corriculumn
    epi = conn.cursor()
    epi.execute("SELECT COUNT(RealID) FROM My_Subjects WHERE Orientation = 'Ε'")
    totalepil= epi.fetchall()
    conn.commit()

    #Getting lab courses
    lab = conn.cursor()
    lab.execute("SELECT COUNT(RealID) FROM My_Subjects WHERE Orientation = 'Ερ'")
    totallab= lab.fetchall()
    conn.commit()
    conn.close()


    print_records=""
    for record in records:
        #Printing All Subjects
        print_records += "Κωδικός:" + str(record[0])+ " Βαθμός:"+str(record[4]) + " Όνομα:" + str(record[1])+ " ID:" + str(record[5]) +"\n" 
    # print(print_records)
    f= open("Lista Mou.txt","w+", encoding="utf-8")
    f.write("-Μέσος Όρος: " + str("%.2f" % avgscore[0][0]))
    f.write("\n-Διδακτικές Μονάδες (ECTS): " + str(totalpoints[0][0]) + "/240")
    f.write("\n-Ποσοστό ολοκλήρωσης της σχολής: " + str("%.2f" % ((totalpoints[0][0]/240)*100))+"%")
    f.write("\n-Περασμένα Υποχρεωτικά: " +str(totalypo[0][0])+"/21")
    f.write("\n-Περασμένα Υποχρεωτικά Επιλογής Ιστορίας: " +str(totalypoi[0][0]))
    f.write("\n-Περασμένα Υποχρεωτικά Επιλογής Φιλοσοφίας: " +str(totalypof[0][0]))
    f.write("\n-Περασμένα Επιλογής: " +str(totalepil[0][0])+"/9")
    f.write("\n-Περασμένα Εργαστήρια: " +str(totallab[0][0])+"/2")
    f.write("\n\n\n-Αναλυτικά:\n" + print_records)
    f.close()
    #Launching Lista Mou.txt file in web browser
    webbrowser.open("Lista Mou.txt")

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

root.mainloop()