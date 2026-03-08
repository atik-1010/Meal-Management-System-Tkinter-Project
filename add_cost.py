from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import dashboard

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

class AddCost:
    def __init__(self, root):
        self.root = root
        self.w_dir = os.getcwd()
        self.root.title("Meal Management System | Add Cost")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (880 / 2))
        y = int((screen_height / 2) - (540 / 2))

        self.root.geometry(f"880x540+{x}+{y}")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ============= Top Frame ============== #
        top_frame = Frame(self.root, width=880, height=55, bg="#3473B9", bd=0)
        top_frame.place(x=0, y=0)

        img2 = Image.open("images\member.png")
        img2 = img2.resize((45, 45))
        self.photimg2 = ImageTk.PhotoImage(img2)

        lblimg2 = Label(self.root, image=self.photimg2, bd=0)
        lblimg2.place(x=10, y=5)

        self.back_btn = Button(self.root, text="Back", font=("Bahnschrift", 13), bg="#A0D568", fg="white", cursor="hand2", command=self.goToBack, bd=0)
        self.back_btn.place(x=770, y=8, width=80, height=35)

    # ====================== Left Frame ==================== #
        self.left_frame = Frame(self.root, width=380, height=500, bg="#002347")
        self.left_frame.place(x=0, y=50)

        top_lbl = Label(self.root, text="Add Cost", font=("Bahnschrift", 15, "bold"), bg="#3473B9", fg="white")
        top_lbl.place(x=60, y = 10)
        
        
        # ============== Members Data Table ============== #
        self.C_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_frame.place(x=10, y=150, width=350, height=300)

        scrolly = Scrollbar(self.C_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_frame, orient=HORIZONTAL)

        self.course_Table = ttk.Treeview(self.C_frame, columns=("cid", "title", "cost"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_Table.xview)
        scrolly.config(command=self.course_Table.yview)

        self.course_Table.heading("cid", text="CID")
        self.course_Table.heading("title", text="Title")
        self.course_Table.heading("cost", text="Cost")

        self.course_Table["show"] = 'headings'
        self.course_Table.column("cid", width=10)
        self.course_Table.column("title", width=200)
        self.course_Table.column("cost", width=100)

        self.course_Table.pack(fill=BOTH, expand=1)
        self.course_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()


    # ====================== Main Frame ==================== #

        self.main_frame = Frame(self.root, width=330, height=465, bg="white")
        self.main_frame.place(x=400, y=50)
        img1 = Image.open("images\dashboard-background.png")
        img1 = img1.resize((630,462))
        self.photimg1 = ImageTk.PhotoImage(img1)

        lblimg = Label(self.root, image=self.photimg1)
        lblimg.place(x=380, y=50)


        # ============= Form ================ #
        self.var_id = StringVar()
        self.var_title = StringVar()
        self.var_cost = StringVar()

        lbl_id = Label(self.root, text="ID         : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=100)
        lbl_title = Label(self.root, text="Title  : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=150)
        lbl_cost = Label(self.root, text="Cost  : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=210)

        text_id = Entry(self.root, textvariable=self.var_id, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0", state="disabled").place(x=580, y=100, width=250, height=40)
        text_title = Entry(self.root, textvariable=self.var_title, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=150, width=250, height=40)
        text_cost = Entry(self.root, textvariable=self.var_cost, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=210, width=250, height=40)

        # ============ Buttons ============= #
        self.btn_add = Button(self.root, text="Add", font=("Bahnschrift", 13), bg="#AC92EB", fg="white", cursor="hand2", command=self.add, bd=0)
        self.btn_add.place(x=410, y=450, width=100, height=40)

        self.btn_update = Button(self.root, text="Update", font=("Bahnschrift", 13), bg="#A0D568", fg="white", cursor="hand2", command=self.update, bd=0)
        self.btn_update.place(x=520, y=450, width=100, height=40)

        self.btn_delete = Button(self.root, text="Delete", font=("Bahnschrift", 13), bg="#FFCE54",fg="white", cursor="hand2", command=self.delete, bd=0)
        self.btn_delete.place(x=630, y=450, width=100, height=40)

        self.btn_clear = Button(self.root, text="Clear", font=("Bahnschrift", 13), bg="#ED5564", fg="white", cursor="hand2", command=self.clear, bd=0)
        self.btn_clear.place(x=740, y=450, width=100, height=40)

        
        self.bottom_frame = Frame(self.root, width=880, height=35, bg="#EFF5FB")
        self.bottom_frame.place(x=380, y=505)
        

    # ========================================================
    def goToBack(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = dashboard.Dashboard(self.new_window)
    
    def clear(self):
        self.show()
        self.var_id.set("")
        self.var_title.set("")
        self.var_cost.set("")
    def delete(self):
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cursor.execute(f"delete from cost_table where cid={self.var_id.get()}")
                conn.commit()
                messagebox.showinfo("Delete", "Delete Successfully !!!", parent=self.root)
                self.clear()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def get_data(self, ev):
        # self.text_roll.config(state='readonly')
        r = self.course_Table.focus()
        content = self.course_Table.item(r)
        row = content["values"]

        self.var_id.set(row[0]),
        self.var_title.set(row[1]),
        self.var_cost.set(row[2])
    def add(self):
        try:
            if self.var_title.get() == "":
                messagebox.showerror("Error", "Title can't be empty!", parent=self.root)
            elif self.var_cost.get() == "":
                messagebox.showerror("Error", "Cost can't be empty!", parent=self.root)
            else:
                cursor.execute(f"insert into cost_table(title, cost) values('{self.var_title.get()}', {self.var_cost.get()})")
                conn.commit()
                messagebox.showinfo("Success", "Added Successfully!", parent=self.root)
                self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def show(self):
        try:
            cursor.execute("select * from cost_table")
            rows = cursor.fetchall()
            self.course_Table.delete(*self.course_Table.get_children())
            for row in rows:
                self.course_Table.insert('', END, values=row)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")



    def update(self):
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Invalid Input!", parent=self.root)
            elif self.var_title.get() == "":
                messagebox.showerror("Error", "Title can't be empty!", parent=self.root)
            elif self.var_cost.get() == "":
                messagebox.showerror("Error", "Cost can't be empty!", parent=self.root)
            else:
                cursor.execute(f"select cid  from cost_table where cid={self.var_id.get()}")
                row = cursor.fetchone()
                if (row == None):
                    messagebox.showerror("Error", "Invalid Data!", parent=self.root)
                else:
                    cursor.execute(f"update cost_table set title='{self.var_title.get()}', cost = {self.var_cost.get()} where cid={self.var_id.get()}")
                    conn.commit()
                    messagebox.showinfo("Success", "Updated Successfully!", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = AddCost(root)
    root.mainloop()
