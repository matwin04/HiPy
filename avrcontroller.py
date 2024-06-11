import serial
import customtkinter as ctk
import tkinter as tk
def pw_on():
    ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
    ser.write(b'PWON\r')
    ser.close()
def pw_off():
    ser = serial.Serial(port='/dev/ttyUSB0',baudrate=9600)
    ser.write(B'PWSTANDBY\r')
    ser.close()
root = tk.Tk()
root.title("Analog and Digital Clocks")

# Create a frame for digital clock
digital_clock_frame = tk.Frame(root)
digital_clock_frame.pack()

pwr_btn = tk.Button(digital_clock_frame,command=pw_on,text='ON')
pwr_btn.pack()
pwr_btn2 = tk.Button(digital_clock_frame,command=pw_off,text='OFF')
pwr_btn2.pack()
# Create digital clock label
digital_clock_label = tk.Label(digital_clock_frame, font=('calibri', 40, 'bold'), foreground='black')
digital_clock_label.pack()


root.mainloop()