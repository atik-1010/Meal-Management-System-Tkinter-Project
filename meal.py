from tkinter import *
import welcome_box
import mysql.connector

conn = mysql.connector.connect(host="localhost", user="root", password="123shuvadev", database="mealmanagmentsystem")
cursor = conn.cursor()

def main():
     win = Tk()
     app = welcome_box.WelcomeBox(win)
     win.mainloop()


if __name__ == "__main__":
      main()