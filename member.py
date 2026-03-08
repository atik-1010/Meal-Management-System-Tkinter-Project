from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import dashboard

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

class Members:
    def __init__(self, root):
        self.root = root
        self.w_dir = os.getcwd()
        self.root.title("Meal Management System | Member Info")
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

        top_lbl = Label(self.root, text="Members Info", font=("Bahnschrift", 15, "bold"), bg="#3473B9", fg="white")
        top_lbl.place(x=60, y = 10)

        # ==============Search Box ============== #
        self.var_search = StringVar()

        self.text_search_name = Entry(self.root, textvariable=self.var_search, font=("Microsoft YaHei UI Light", 11), bg="#FFFFFF")
        self.text_search_name.insert(10, "Search By Name")
        self.text_search_name.place(x=50, y=80, width=220, height=40)

        img_src = Image.open("images\search.png")
        
        self.search_img = ImageTk.PhotoImage(img_src)

        btn_search = Button(self.root, image=self.search_img, command=self.search)
        btn_search.place(x = 260, y = 80, height=41)
        
        
        # ============== Members Data Table ============== #
        self.C_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_frame.place(x=10, y=150, width=350, height=300)

        scrolly = Scrollbar(self.C_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_frame, orient=HORIZONTAL)

        self.course_Table = ttk.Treeview(self.C_frame, columns=("mid", "name", "phone", "credit"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_Table.xview)
        scrolly.config(command=self.course_Table.yview)

        self.course_Table.heading("mid", text="ID")
        self.course_Table.heading("name", text="Name")
        self.course_Table.heading("phone", text="Phone")
        self.course_Table.heading("credit", text="Credit")

        self.course_Table["show"] = 'headings'
        self.course_Table.column("mid", width=10)
        self.course_Table.column("name", width=100)
        self.course_Table.column("phone", width=100)
        self.course_Table.column("credit", width=100)

        self.course_Table.pack(fill=BOTH, expand=1)
        self.course_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        # self.fetch_course()


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
        self.var_name = StringVar()
        self.var_phone = StringVar()
        self.var_credit = StringVar()

        lbl_id = Label(self.root, text="ID         : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=100)
        lbl_name = Label(self.root, text="Name  : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=150)
        lbl_phone = Label(self.root, text="Phone  : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=210)
        lbl_credit = Label(self.root, text="Credit : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=500, y=270)

        text_id = Entry(self.root, textvariable=self.var_id, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0", state="disabled").place(x=580, y=100, width=250, height=40)
        text_name = Entry(self.root, textvariable=self.var_name, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=150, width=250, height=40)
        text_phone = Entry(self.root, textvariable=self.var_phone, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=210, width=250, height=40)
        text_credit = Entry(self.root, textvariable=self.var_credit, font=("gBahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=270, width=250, height=40)

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
    def search(self):
        try:
            cursor.execute(f"select *  from member_info where name='{self.var_search.get()}'")
            row = cursor.fetchone()
            if(row!=None):
                self.course_Table.delete(*self.course_Table.get_children())
                self.course_Table.insert('', END, values=row)
            else:
                messagebox.showerror("Error","No Record Found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.var_id.set("")
        self.var_name.set("")
        self.var_phone.set("")
        self.var_credit.set("")
    def delete(self):
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cursor.execute(f"delete from member_info where mid={self.var_id.get()}")
                conn.commit()
                cursor.execute(f"delete from meal_table where meal_mid={self.var_id.get()}")
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
        self.var_name.set(row[1]),
        self.var_phone.set(row[2]),
        self.var_credit.set(row[3])

    def add(self):
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Name is not be empty!", parent=self.root)
            elif self.var_phone.get() == "":
                messagebox.showerror("Error", "Phone is not be empty!", parent=self.root)
            elif self.var_credit.get() == "":
                messagebox.showerror("Error", "Credit is not be empty!", parent=self.root)
            else:

                cursor.execute(f"insert into member_info(name, phone, credit) values('"+self.var_name.get()+"', '"+self.var_phone.get()+"', '"+self.var_credit.get()+"')")
                conn.commit()
                messagebox.showinfo("Success", "Added Successfully!", parent=self.root)
                self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def show(self):
        try:
            cursor.execute("select mid, name, phone, credit  from member_info")
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
            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Name is not be empty!", parent=self.root)
            elif self.var_phone.get() == "":
                messagebox.showerror("Error", "Phone is not be empty!", parent=self.root)
            elif self.var_credit.get() == "":
                messagebox.showerror("Error", "Credit is not be empty!", parent=self.root)
            else:
                cursor.execute("select mid  from member_info where mid='"+self.var_id.get()+"'")
                row = cursor.fetchone()
                if (row == None):
                    messagebox.showerror("Error", "Invalid Data!", parent=self.root)
                else:
                    cursor.execute(f"update member_info set name='{self.var_name.get()}', phone = '{self.var_phone.get()}', credit = {self.var_credit.get()} where mid={row[0]}")
                    conn.commit()
                    messagebox.showinfo("Success", "Updated Successfully!", parent=self.root)
                    self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = Members(root)
    root.mainloop()
