import cv2
import pytesseract
import re
import pypyodbc
import serial
import time
from tkinter import *
import json
from tkinter import messagebox
from PIL import Image, ImageTk

tk = Tk()
tk.title("Plate Recognize System")
tk.geometry("1000x500")
icon = Image.open("icon.png")
tk.iconphoto(True, ImageTk.PhotoImage(icon))

with open("data.json", "r") as dosya:
        data = json.load(dosya)

servername = data["servername"]
databasename = data["databasename"]
serialport = data["serialport"]
baudrate = data["baudrate"]
opentime = data["opentime"]

try:
    ser = serial.Serial(f'{serialport}', baudrate, timeout=1) 
except serial.serialutil.SerialException:
    messagebox.showerror("Error", "Please connect the serial port device.")


def main():

    db = pypyodbc.connect(
        'Driver={SQL Server};'
        f'Server={servername};'
        f'Database={databasename};'
        'Trusted_Connection=True;'
    )

    mycursor = db.cursor()

    mycursor.execute('SELECT * FROM dbo.platerecapp_car')

    plates = mycursor.fetchall()

    cam = cv2.VideoCapture(0)

    pytesseract.pytesseract.tesseract_cmd = "Tesseract-OCR\\tesseract.exe"

    while True:
        
        ret,frame=cam.read()
        try:
            cv2.imshow("Camera",frame)
        except cv2.error:
            messagebox.showerror("Error", "Please connect the camera.")

        text = pytesseract.image_to_string(frame)
        pltfilt = filterr(text)
        plt = delheadchars(pltfilt)

        if plt:
            print(plt)

        for plate in plates:
            if plt == filterr(plate['plate']):
                matched()
                

        if cv2.waitKey(1) & 0xFF == ord("q"):
            exit()

    cam.release()

def mainmenu():
    frame1 = Frame(tk, bg="#055384")
    frame1.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    l1 = Label(frame1, text="Plate Recognize System", bg="#055384", fg="white", font="Arial 20 bold")
    l1.pack(padx=10, pady=10, anchor=S)

    btn1 = Button(frame1, text="START", bg="#000000", fg="white", font="Arial 18 bold", command=main)
    btn1.pack(padx=5, pady=60)

    btn2 = Button(frame1, text="SETTINGS", bg="#000000", fg="white", font="Arial 18 bold", command=settings)
    btn2.pack(padx=5, pady=90)

    tk.mainloop()

def settings():
    frame2 = Frame(tk, bg="#055384")
    frame2.place(relx=0, rely=0, relwidth=1.0, relheight=1.0)

    l2 = Label(frame2, text="Plate Recognize System", bg="#055384", fg="white", font="Arial 20 bold")
    l2.pack(padx=10, pady=10, anchor=S)

    btn3 = Button(frame2, text="BACK", bg="#000000", fg="white", font="Arial 15 bold", command=mainmenu)
    btn3.place(x=50, y=30)

    l3 = Label(frame2, text="Database:", bg="#055384", fg="white", font="Arial 15 bold")
    l3.place(x=150,y=90)

    l4 = Label(frame2, text="Server Name:", bg="#055384", fg="white", font="Arial 12 bold")
    l4.place(x=200,y=120)
    e = Entry(frame2, bd=3, relief=FLAT)
    e.place(x=310,y=120)

    l5 = Label(frame2, text="Database Name:", bg="#055384", fg="white", font="Arial 12 bold")
    l5.place(x=200,y=150)
    e1 = Entry(frame2, bd=3, relief=FLAT)
    e1.place(x=330,y=150)

    l6 = Label(frame2, text="Serial:", bg="#055384", fg="white", font="Arial 15 bold")
    l6.place(x=150,y=180)

    l7 = Label(frame2, text="Serial Port:", bg="#055384", fg="white", font="Arial 12 bold")
    l7.place(x=200,y=210)
    e2 = Entry(frame2, bd=3, relief=FLAT)
    e2.place(x=290,y=210)

    l8 = Label(frame2, text="Baudrate:", bg="#055384", fg="white", font="Arial 12 bold")
    l8.place(x=200,y=245)
    e3 = Entry(frame2, bd=3, relief=FLAT)
    e3.place(x=280,y=245)

    l9 = Label(frame2, text="Open Time:", bg="#055384", fg="white", font="Arial 12 bold")
    l9.place(x=200,y=280)
    e4 = Entry(frame2, bd=3, relief=FLAT)
    e4.place(x=292,y=280)

    btn4 = Button(frame2, text="SAVE", bg="#000000", fg="white", font="Arial 15 bold", command=lambda: config(e,e1,e2,e3,e4))
    btn4.place(x=550, y=400)

    tk.mainloop()

def filterr(text):
        pl = text.replace(" ", "")
        pl2 = pl.strip()
        plt = re.sub(r'[^a-zA-Z0-9]', '', pl2)
        return plt

def delheadchars(string):
    bosluk_index = 0
    for i in range(len(string)):
        if not string[i].isalpha():
            bosluk_index = i
            break
    return string[bosluk_index:]

def config(e,e1,e2,e3,e4):
    data = {
        "servername": e.get(),
        "databasename": e1.get(),
        "serialport": e2.get(),
        "baudrate": int(e3.get()),
        "opentime": int(e4.get()),
    }

    with open("data.json", "w") as dosya:
        json.dump(data, dosya)

def matched():
    ser.write("1".encode()) 
    time.sleep(opentime)
    ser.write("0".encode()) 
    ser.close()

mainmenu()