from tkinter import *
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import mysql.connector
import os
import dashboard

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

class MealReport:
    def __init__(self, root):
        self.root = root
        self.w_dir = os.getcwd()
        self.root.title("Meal Management System | Meal Report")
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

        top_lbl = Label(self.root, text="Meal Report", font=("Bahnschrift", 15, "bold"), bg="#0F2F49", fg="white")
        top_lbl.place(x=60, y = 10)

        self.back_btn = Button(self.root, text="Back", font=("Bahnschrift", 13), bg="#A0D568", fg="white", cursor="hand2", command=self.goToBack, bd=0)
        self.back_btn.place(x=770, y=8, width=80, height=35)

    # ====================== Main Frame ==================== #
        self.left_frame = Frame(self.root, width=880, height=500, bg="#202124")
        self.left_frame.place(x=0, y=50)
        
        
        # ============== Members Data Table ============== #
        style = ttk.Style()
        style.theme_use('default')
        
        self.C_frame = Frame(self.root, bd=2, relief=RIDGE)
        self.C_frame.place(x=50, y=80, width=770, height=400)

        scrolly = Scrollbar(self.C_frame, orient=VERTICAL)
        scrollx = Scrollbar(self.C_frame, orient=HORIZONTAL)

        self.course_Table = ttk.Treeview(self.C_frame, columns=("name", "credit", "meal", "mrate", "abill", "cost", "due"), xscrollcommand=scrollx.set, yscrollcommand=scrolly.set)

        scrollx.pack(side=BOTTOM, fill=X)
        scrolly.pack(side=RIGHT, fill=Y)
        scrollx.config(command=self.course_Table.xview)
        scrolly.config(command=self.course_Table.yview)

        self.course_Table.tag_configure('oddrow', background="white")
        self.course_Table.tag_configure('evenrow', background="lightblue")

        self.course_Table.heading("name", text="Name")
        self.course_Table.heading("credit", text="Total Credit")
        self.course_Table.heading("meal", text="Total Meal")
        self.course_Table.heading("mrate", text="Meal Rate")
        self.course_Table.heading("abill", text="Additional Bill")
        self.course_Table.heading("cost", text="Total Cost")
        self.course_Table.heading("due", text="Total Due")

        self.course_Table["show"] = 'headings'
        self.course_Table.column("name", width=100)
        self.course_Table.column("credit", width=100)
        self.course_Table.column("meal", width=100)
        self.course_Table.column("mrate", width=100)
        self.course_Table.column("abill", width=100)
        self.course_Table.column("cost", width=100)
        self.course_Table.column("due", width=100)

        self.course_Table.pack(fill=BOTH, expand=1)
        self.show()

        

    # ========================================================
    def goToBack(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = dashboard.Dashboard(self.new_window)


    def show(self):
        try:
            global count
            count = 0
            
            cursor.execute("select mid, name, credit from member_info")
            rows = cursor.fetchall()

            for row in rows:
                lst = list(row)
                mid = lst[0]
                total_credit = lst[2]
                del lst[0]
                
                cursor.execute(f"select sum(meal) from meal_table where meal_mid = {mid}")
                total_mmeal = cursor.fetchone()[0]
                if total_mmeal == None:
                    total_mmeal = 0
                
                # -------- Meal rate calculation ------- #
                cursor.execute("select sum(cost) from cost_table")
                total_bazar_cost = cursor.fetchone()[0]
                if total_bazar_cost == None:
                    total_bazar_cost = 0

                cursor.execute("select sum(meal) from meal_table")
                total_meal = cursor.fetchone()[0]
                if total_meal == None:
                    total_meal = 0
                meal_rate = round(total_bazar_cost / total_meal, 2)
                # -------------------------------------- #

                additional_bill = 300
                total_cost = round(meal_rate * total_mmeal, 2) + additional_bill
                total_due = total_credit - total_cost

                lst.append(total_mmeal)
                lst.append(meal_rate)
                lst.append(additional_bill)
                lst.append(total_cost)
                lst.append(total_due)
                lst = tuple(lst)


                if(count % 2 == 0):
                    self.course_Table.insert('', END, values=lst, tags=('evenrow', ))
                else:
                    self.course_Table.insert('', END, values=lst, tags=('oddrow', ))
                count = count + 1

        except Exception as ex:
            messagebox.showerror("Error", f"Error due to {str(ex)}")



if __name__ == "__main__":
    root = Tk()
    obj = MealReport(root)
    root.mainloop()
