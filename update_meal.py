from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import dashboard
from tkcalendar import *

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

class UpdateMeal:
    def __init__(self, root):
        self.root = root
        self.root.title("Meal Management System | Meal Table")
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = int((screen_width / 2) - (880 / 2))
        y = int((screen_height / 2) - (540 / 2))

        self.root.geometry(f"880x540+{x}+{y}")
        self.root.resizable(False, False)
        self.root.focus_force()

        # ============= Top Frame ============== #
        top_frame = Frame(self.root, width=880, height=55, bg="#0F2F49", bd=0)
        top_frame.place(x=0, y=0)

        img2 = Image.open("images\meal.png")
        img2 = img2.resize((45, 45))
        self.photimg2 = ImageTk.PhotoImage(img2)
        lblimg2 = Label(self.root, image=self.photimg2, bd=0)
        lblimg2.place(x=10, y=5)

        top_lbl = Label(self.root, text="Meal Table", font=("Bahnschrift", 15, "bold"), bg="#0F2F49", fg="white")
        top_lbl.place(x=60, y = 10)

        self.back_btn = Button(self.root, text="Back", font=("Bahnschrift", 13), bg="#A0D568", fg="white", cursor="hand2", command=self.goToBack, bd=0)
        self.back_btn.place(x=770, y=8, width=80, height=35)

    # ====================== Left Frame ==================== #
        self.left_frame = Frame(self.root, width=380, height=500, bg="#202124")
        self.left_frame.place(x=0, y=50)


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
        style = ttk.Style()
        style.theme_use('default')
        
        self.C_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_frame.place(x=10, y=150, width=350, height=300)

        scrolly = Scrollbar(self.C_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_frame, orient=HORIZONTAL)

        self.course_Table = ttk.Treeview(self.C_frame, columns=("mid", "name", "date", "meal"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_Table.xview)
        scrolly.config(command=self.course_Table.yview)

        self.course_Table.tag_configure('oddrow', background="white")
        self.course_Table.tag_configure('evenrow', background="lightblue")

        self.course_Table.heading("mid", text="ID")
        self.course_Table.heading("name", text="Name")
        self.course_Table.heading("date", text="Date")
        self.course_Table.heading("meal", text="Meal")

        self.course_Table["show"] = 'headings'
        self.course_Table.column("mid", width=10)
        self.course_Table.column("name", width=100)
        self.course_Table.column("date", width=100)
        self.course_Table.column("meal", width=100)

        self.course_Table.pack(fill=BOTH, expand=1)
        self.course_Table.bind("<ButtonRelease-1>", self.get_data)
        self.show()
        # self.fetch_course()


    # ====================== Main Frame ==================== #

        self.main_frame = Frame(self.root, width=330, height=465, bg="white")
        self.main_frame.place(x=400, y=50)
        img1 = Image.open("images\\bg1.jpeg")
        img1 = img1.resize((800,950))
        self.photimg1 = ImageTk.PhotoImage(img1)

        lblimg = Label(self.root, image=self.photimg1)
        lblimg.place(x=380, y=50)


        # ============= Form ================ #
        self.var_id = StringVar()
        self.var_name = StringVar()
        self.var_date = StringVar()
        self.var_meal = StringVar()

        lbl_id = Label(self.root, text="ID               : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=450, y=100)
        lbl_name = Label(self.root, text="Date           : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=450, y=150)
        lbl_date = Label(self.root, text="Name         : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=450, y=210)
        lbl_meal = Label(self.root, text="Total Meal : ", font=("Bahnschrift", 15, "bold"), bg="white", fg="#002347").place(x=450, y=270)

        text_id = Entry(self.root, textvariable=self.var_id, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0", state="disabled").place(x=580, y=100, width=250, height=40)
        text_name = Entry(self.root, textvariable=self.var_name, font=("Bahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=150, width=210, height=40)

        clndr = DateEntry(root, selectmode="day", date_pattern="dd/mm/y", textvariable = self.var_date)
        clndr.place(x = 580, y = 148, height=42, width=250)

        self.nameList = []
        self.nameList.append("Select")
        self.fetch_name()

        self.txt_name = (ttk.Combobox(self.root, textvariable=self.var_name, font=("Bahnschrift", 13, "bold"),
        state='readonly', values=(self.nameList))).place(x=580, y=210, width=250, height=40)

        text_meal = Entry(self.root, textvariable=self.var_meal, font=("gBahnschrift", 15, "bold"), bg="#FAF7F0").place(x=580, y=270, width=250, height=40)

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
    def fetch_name(self):
        try:
            cursor.execute("select name  from member_info")
            rows = cursor.fetchall()

            if len(rows)>0:
                for row in rows:
                    self.nameList.append(row[0])

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")
    def nameList(self):
        pass
    def goToBack(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = dashboard.Dashboard(self.new_window)
    def search(self):
        try:
            cursor.execute(f"select mid, name from member_info where name='{self.var_search.get()}'")
            row = cursor.fetchone()
            if(row!=None):
                self.course_Table.delete(*self.course_Table.get_children())

                cursor.execute(f"select * from meal_table where meal_mid = {row[0]} order by date")
                minfo = cursor.fetchall()
                
                global count
                count = 0
                for info in minfo:
                    lst = list(info)
                    lst[1] = row[1]
                    info = tuple(lst)
                    if(count % 2 == 0):
                        self.course_Table.insert('', END, values=info, tags=('evenrow', ))
                    else:
                        self.course_Table.insert('', END, values=info, tags=('oddrow', ))
                    count = count + 1
                # self.course_Table.insert('', END, values=row)
            else:
                messagebox.showerror("Error","No Record Found",parent=self.root)
        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def clear(self):
        self.show()
        self.var_id.set("")
        self.var_name.set("")
        self.var_date.set("")
        self.var_meal.set("")
    def delete(self):
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "ID should be required", parent=self.root)
            else:
                cursor.execute(f"delete from meal_table where meal_id={self.var_id.get()}")
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
        self.var_date.set(row[2]),
        self.var_meal.set(row[3])

    def add(self):
        try:
            if self.var_name.get() == "":
                messagebox.showerror("Error", "Name is not be empty!", parent=self.root)
            elif self.var_date.get() == "":
                messagebox.showerror("Error", "Date is not be empty!", parent=self.root)
            elif self.var_meal.get() == "":
                messagebox.showerror("Error", "Meal is not be empty!", parent=self.root)
            else:
                cursor.execute(f"select mid from member_info where name='{self.var_name.get()}'")
                row = cursor.fetchone()

                if(row!=None):    
                    cursor.execute(f"select * from meal_table where meal_mid={row[0]} and date = '{self.var_date.get()}'")
                    r1 = cursor.fetchone()

                    if(r1 == None) :
                        cursor.execute(f"insert into meal_table(meal_mid, date, meal) values({row[0]}, '{self.var_date.get()}', {self.var_meal.get()})")
                        conn.commit()
                        messagebox.showinfo("Success", "Added Successfully!", parent=self.root)
                    else:
                        messagebox.showerror("Error","Your meal already added!",parent=self.root)

                else:
                    messagebox.showerror("Error","No Record Found",parent=self.root)
                self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")

    def show(self):
        try:
            global count
            count = 0
            cursor.execute("select meal_id, meal_mid, date, meal from meal_table order by date asc")
            rows = cursor.fetchall()
            self.course_Table.delete(*self.course_Table.get_children())

            for row in rows:
                lst = list(row)
                cursor.execute(f"select name from member_info where mid={lst[1]}")
                mname = cursor.fetchone()
                lst[1] = mname[0]
                row = tuple(lst)
                if(count % 2 == 0):
                    self.course_Table.insert('', END, values=row, tags=('evenrow', ))
                else:
                    self.course_Table.insert('', END, values=row, tags=('oddrow', ))
                count = count + 1

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")



    def update(self):
        try:
            if self.var_id.get() == "":
                messagebox.showerror("Error", "Invalid Input!", parent=self.root)
            elif self.var_name.get() == "":
                messagebox.showerror("Error", "Name can't be empty!", parent=self.root)
            elif self.var_date.get() == "":
                messagebox.showerror("Error", "Date can't be empty!", parent=self.root)
            elif self.var_meal.get() == "":
                messagebox.showerror("Error", "Meal can't be empty!", parent=self.root)
            else:
                
                cursor.execute(f"update meal_table set meal = {self.var_meal.get()} where meal_id={self.var_id.get()}")
                conn.commit()
                messagebox.showinfo("Success", "Updated Successfully!", parent=self.root)
                self.show()

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")


if __name__ == "__main__":
    root = Tk()
    obj = UpdateMeal(root)
    root.mainloop()
