from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox
import mysql.connector
import dashboard
import os

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

class ManagerLogin:
    def __init__(self, root):
            self.root = root
            self.w_dir = os.getcwd()
            self.root.title("Meal Management System | Manager Login")
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            x = int((screen_width / 2) - (880 / 2))
            y = int((screen_height / 2) - (540 / 2))

            self.root.geometry(f"880x540+{x}+{y}")
            self.root.resizable(False, False)

            # ============ background image ============
            img1 = Image.open("images\login_bg.png")
            img1 = img1.resize((880,540))
            self.photimg1 = ImageTk.PhotoImage(img1)

            lblimg = Label(self.root, image=self.photimg1, bd=4,relief=RIDGE)
            lblimg.place(x=0, y=0, width=880, height=540)

            
            # ============= Form ======================
            title = Label(self.root, text="Manager Login Form", font=("Bahnschrift", 18, "bold"), padx=100, pady=25, bd=5, relief=RIDGE, foreground="#00B0F0")
            title.place(x=400, y=80)

            frame = Frame(self.root, width=350, height=350, bg="white")
            frame.place(x=420, y=200)
            
            #....User Name....#
            self.monthname = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
            self.monthname.place(x=30, y=10)
            self.monthname.insert(0, 'Month Name')

            Frame(frame, width=350, height=2, bg='black').place(x=30, y = 40)

            #....Password....#
            self.password = Entry(frame, width=25, fg="black", border=0, bg="white", font=("Microsoft YaHei UI Light", 11))
            self.password.place(x=30, y=80)
            self.password.insert(0, 'Password')

            Frame(frame, width=350, height=2, bg='black').place(x=30, y = 110)


            #.....Submit....#
            Button(frame, command=self.login ,text="Login", padx=40, pady=8, border=0, background="#880015", foreground="white", font=("Bahnschrift", 15)).place(x = 120, y = 160)
    

    def login(self):
        if self.monthname.get() == "" or self.password.get() == "":
            messagebox.showerror("Error", "All field required!")  
        else:
            
            cursor.execute("select * from manager_info where month_name=%s and password=%s", (
                 self.monthname.get(), self.password.get()
            ))
            row = cursor.fetchone()
            if row == None:
                messagebox.showerror("Invalid", "Invalid monthname and password")          
            else:
                messagebox.showinfo("Success","Successfully Logged in!")

                file = open("mname.txt", "w")
                file.write(f"{self.monthname.get()}")
                file.close()
                self.new_window = Toplevel(self.root)
                self.root.withdraw()
                self.app = dashboard.Dashboard(self.new_window)
if __name__ == "__main__":
    root = Tk()
    obj = ManagerLogin(root)
    root.mainloop()