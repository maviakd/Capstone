import tkinter as tk
from tkinter import *
import rsa
from tkinter import filedialog, ttk
import tkinter.font as font
from PIL import Image, ImageTk
from stegano import lsb
# main gui window
interface = tk.Tk()
interface.title("Steganography")
interface.resizable(width=True, height=True)
interface.geometry("500x700")
interface.configure(bg='grey')
myFont = font.Font(family='Helvetica', size=14, weight='bold')
# creates tabbed widget
tabControl = ttk.Notebook(interface)
encodeTab = ttk.Frame(tabControl)
tabControl.add(encodeTab, text="Encode")
decodeTab = ttk.Frame(tabControl)
tabControl.add(decodeTab, text="Decode")
tabControl.pack(expand=1, fill="both")
# open file
def open_file():
    return filedialog.askopenfilename()
# open and display image in encode tab
def open_pic_encode():
    global pic
    x = open_file()
    pic = Image.open(x)
    pic.save("output.png")
    pic = pic.resize((200, 200), Image.ANTIALIAS)
    pic = ImageTk.PhotoImage(pic)
    panel = Label(encodeTab, image=pic)
    panel.image = pic
    panel.pack(side=TOP, padx=30, pady=30)
# open and display image in decode tab
def open_pic_decode():
    global pic
    x = open_file()
    pic = Image.open(x)
    pic.save("output.png")
    pic = pic.resize((200, 200), Image.ANTIALIAS)
    pic = ImageTk.PhotoImage(pic)
    panel = Label(decodeTab, image=pic)
    panel.image = pic
    panel.pack(side=TOP, padx=30, pady=30)
# select image button for encode tab
button = tk.Button(encodeTab, text="Open Image", font=myFont, command=open_pic_encode)
button.pack(side=TOP, padx=10, pady=10)
# select image button for decode tab
button = tk.Button(decodeTab, text="Open Image", font=myFont, command=open_pic_decode)
button.pack(side=TOP, padx=10, pady=10)
# encode image using stegano
def encode_pic():
    message = input.get(1.0, "end")
    encode = lsb.hide("output.png", hiddenMessage)
    encode.save("output.png")
# saves image
def save_file():
    image = Image.open("output.png")
    photo = ImageTk.PhotoImage(image)
    filename = filedialog.asksaveasfilename(defaultextension=".png")
    image.save(filename)
# decode image using stegano
def decode_pic():
    hiddenMessage = lsb.reveal("output.png")
    if hiddenMessage == None:
        l = Label(decodeTab, text="No hidden message found")
        l.pack()
    else:
        l = Label(decodeTab, text=hiddenMessage, font=myFont)
        l.pack()
publicKey, privateKey = rsa.newkeys(512)
def encrypt_message(message):
    print(message)
    encMessage = rsa.encrypt(message.encode(), publicKey)
    print(encMessage)
    return encMessage
def decrypt_message(hiddenmessage):
    encMessage = hiddenmessage
    decMessage = rsa.decrypt(encMessage, privateKey).decode()
    print(decMessage)
    return decMessage
# label for text box
label = Label(encodeTab, text="Enter message below", font=myFont)
label.pack()
# text box for user input
input = Text(encodeTab, height=10, width=50)
input.pack()
# encode button
button = tk.Button(encodeTab, text="Encode", font=myFont, bg='#808080', fg='#ffffff', command=encode_pic)
button.pack(side=TOP, padx=20, pady=20)
# decode button
button = tk.Button(decodeTab, text="Decode", font=myFont, bg='#808080', fg='#ffffff', command=decode_pic)
button.pack(side=BOTTOM, padx=20, pady=20)
# save button
button = tk.Button(interface, text="Save Image", font=myFont, command=save_file)
button.pack(side=BOTTOM, padx=10, pady=10)
interface.mainloop()
