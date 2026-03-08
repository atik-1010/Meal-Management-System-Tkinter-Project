from tkinter import *
from PIL import Image, ImageTk
import datetime as dt
import os
from tkinter import ttk, messagebox
import welcome_box
import member
import update_meal
import meal_report
import add_cost
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

class Dashboard:
    def __init__(self, root):
            self.root = root
            self.w_dir = os.getcwd()
            self.root.title("Meal Management System | Dashboard")
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            x = int((screen_width / 2) - (880 / 2))
            y = int((screen_height / 2) - (540 / 2))

            self.root.geometry(f"880x540+{x}+{y}")
            self.root.resizable(False, False)

            top_frame = Frame(self.root, width=880, height=40, bg="#3473B9")
            top_frame.place(x=0, y=0)

            self.left_frame1 = Frame(self.root, width=250, height=200, bg="#3473B9")
            self.left_frame1.place(x=0, y=40)

            self.left_frame2 = Frame(self.root, width=250, height=300, bg="#EFF5FB")
            self.left_frame2.place(x=0, y=240)

            self.bottom_frame = Frame(self.root, width=880, height=35, bg="#EFF5FB")
            self.bottom_frame.place(x=250, y=505)

            self.main_frame = Frame(self.root, width=630, height=465, bg="blue")
            self.main_frame.place(x=250, y=40)

            #------ Top Frame Design -------
            top_lbl = Label(self.root, text="Dashboard", font=("arial", 15, "bold"), bg="#3473B9", fg="white")
            top_lbl.place(x=45, y = 10)

            date = dt.datetime.now()
            date_label = Label(self.root, text=f"{date:%A, %B %d, %Y}", font="Calibri, 12", bg="#3473B9", fg="white")
            date_label.place(x=650, y = 10)

            #----- Main frame design -------
            img1 = Image.open("images\dashboard-background.png")
            img1 = img1.resize((630,462))
            self.photimg1 = ImageTk.PhotoImage(img1)

            lblimg = Label(self.root, image=self.photimg1)
            lblimg.place(x=250, y=40)

            # ----- Meal summary ------- #
            cursor.execute("select sum(meal) from meal_table")
            tmeal = cursor.fetchone()[0]
            cursor.execute("select count(mid) from member_info")
            tmember = cursor.fetchone()[0]
            cursor.execute("select sum(cost) from cost_table")
            tcost = cursor.fetchone()[0]

            if tmeal == None:
                Label(self.root, text=f"Total Meal : 0", background="#023047", fg="white", padx=5, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 260, y = 50)
            else:
                Label(self.root, text=f"Total Meal : {int(tmeal)}", background="#023047", fg="white", padx=5, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 260, y = 50)
            if tmember == None:
                Label(self.root, text=f"Total Member : 0", background="#ffb703", fg="black", padx=5, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 400, y = 50)
            else:
                Label(self.root, text=f"Total Member : {int(tmember)}", background="#ffb703", fg="black", padx=5, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 400, y = 50)
            if tcost == None:
                Label(self.root, text=f"Total Cost : 0", background="#219ebc", fg="white", padx=5, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 560, y = 50)
            else:
                Label(self.root, text=f"Total Cost : {int(tcost)}", background="#219ebc", fg="white", padx=5, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 560, y = 50)
            
            # ---- Caclulate Meal Rate ------ #
            cursor.execute("select sum(cost) from cost_table")
            total_bazar_cost = cursor.fetchone()[0]
            if total_bazar_cost == None:
                total_bazar_cost = 0

            cursor.execute("select sum(meal) from meal_table")
            total_meal = cursor.fetchone()[0]
            if total_meal == None:
                total_meal = 0
            meal_rate = round(total_bazar_cost / total_meal, 2)
            # ---------------------------------- #
            Label(self.root, text=f"Meal Rate : {meal_rate}", background="#D52027", fg="white", padx=10, pady=10,  font=("Bahnschrift", 13, "bold")).place(x = 712, y = 50)
            #----------------------------#

            member_info= PhotoImage(file="images\member_info.png")
            member_info_btn= Button(self.root, image=member_info,borderwidth=0, cursor="hand2", command=self.memberInfo)
            member_info_btn.place(x = 350, y = 170)

            bazar_cost= PhotoImage(file="images\\bazar_cost.png")
            bazar_cost_btn= Button(self.root, image=bazar_cost,borderwidth=0, cursor="hand2", command=self.addCost)
            bazar_cost_btn.place(x = 580, y = 170)

            meal_report= PhotoImage(file="images\meal_report.png")
            meal_report_btn= Button(self.root, image=meal_report,borderwidth=0, cursor="hand2", command=self.mealReport)
            meal_report_btn.place(x = 350, y = 320)

            update_meal= PhotoImage(file="images\\update.png")
            update_meal_btn= Button(self.root, image=update_meal,borderwidth=0, cursor="hand2", command=self.updateMeal)
            update_meal_btn.place(x = 580, y = 320)

            #-------Left Frame 1 Design -----------
            img2 = Image.open("images\con_ico.png")
            img2 = img2.resize((100,100))
            self.photimg2 = ImageTk.PhotoImage(img2)

            lblimg2 = Label(self.root, image=self.photimg2, border=0)
            lblimg2.place(x=50, y=60)

            file = open("mname.txt", "r")

            month_name = Button(self.root, text=file.readline(), border=0, bg="#3473B9", fg="white", padx=25, pady=8, font=("arial", 13, "bold"))
            month_name.place(x = 40, y = 160)
            
            cursor.execute("select sum(credit) from member_info")
            balance = cursor.fetchone()[0]
            month_name = Button(self.root, text=f"Balance : {balance}", border=0, bg="#9BCC5F", fg="black", padx=23, pady=8, font=("arial", 13, "bold"), width=20)
            month_name.place(x = 0, y = 220)

            #------- Left Frame 2 Design --------
            logout_button = Button(self.root, text="Logout", border=0, bg="#9BCC5F", fg="white", padx=25, pady=8, font=("arial", 13, "bold"), cursor="hand2", command=self.logout)
            logout_button.place(x = 60, y = 470)

            self.root.mainloop()
    def logout(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = welcome_box.WelcomeBox(self.new_window)
    def memberInfo(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = member.Members(self.new_window)
    def updateMeal(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = update_meal.UpdateMeal(self.new_window)
    def mealReport(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = meal_report.MealReport(self.new_window)
    def addCost(self):
        self.new_window = Toplevel(self.root)
        self.root.withdraw()
        self.app = add_cost.AddCost(self.new_window)
if __name__ == "__main__":
      root = Tk()
      Dashboard(root)