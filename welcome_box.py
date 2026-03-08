from tkinter import *
from PIL import Image, ImageTk
import create_meal_table
import manager_login

class WelcomeBox:
    def __init__(self, root):
            self.root = root
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()

            x = int((screen_width / 2) - (880 / 2))
            y = int((screen_height / 2) - (540 / 2))

            self.root.title("Meal Management System")
            self.root.geometry(f"880x540+{x}+{y}")
            self.root.resizable(False, False)

            # ============ background image ============
            img1 = Image.open("images\welcome_bg1.jpeg")
            img1 = img1.resize((880,540))
            self.photimg1 = ImageTk.PhotoImage(img1)

            lblimg = Label(self.root, image=self.photimg1, bd=4,relief=RIDGE)
            lblimg.place(x=0, y=0, width=880, height=540)

            # ============= title =======================
            lbl_title = Label(self.root, text="Meal Management System", font=("Bahnschrift", 35, "bold"), bg="black", fg="white", padx=170, pady=25, bd=5, relief=RIDGE)
            lbl_title.place(x=0, y=80)

            # ============= button ======================
            mngr_login = Button(self.root, command=self.mngr_login, text="Manager Login", background="#880015", foreground="white", padx=18, pady=20, font=("arial", 13, "bold"), borderwidth=0)
            create_table = Button(self.root, command=self.user_login, text="Create Meal Table", background="#880015", foreground="white", padx=22, pady=20, font=("arial", 13, "bold"), borderwidth=0)

            mngr_login.place(x=240, y=300)
            create_table.place(x=440, y=300)
    def user_login(self):
         self.root.withdraw()
         self.new_window = Toplevel(self.root)
         self.app = create_meal_table.CreateMealTable(self.new_window)
    def mngr_login(self):
        self.root.withdraw()
        self.new_window = Toplevel(self.root)
        self.app = manager_login.ManagerLogin(self.new_window)