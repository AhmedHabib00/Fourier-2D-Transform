import logging
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import functools
from tkinter import StringVar, Tk,Button
import tkinter as tk
from PIL import Image
import matplotlib.pyplot as plt
from Image_Class import ImageClass
from tkinter import *
import matplotlib.cm as cm
logging.basicConfig(filename='log.log',level=logging.DEBUG)

class GUI:
    def __init__(self,window):
        logging.info('Program Started')
        self.component_list = ["Select Component","Mag","Phase","Real","Imag",]
        self.mixer_list = ["Mag","UniMag","Real","Imag","Phase","UniPhase",]
        self.img_list = ["Image 1","Image 2"]
        self.out_list = ["Output 1","Output 2"]
        self.selected_first_img_component = StringVar()
        self.selected_first_img_component.set(self.component_list[0])
        self.selected_second_img_component = StringVar()
        self.selected_second_img_component.set(self.component_list[0])
        self.selected_first_mixer_component = StringVar()
        self.selected_first_mixer_component.set(self.mixer_list[0])
        self.selected_second_mixer_component = StringVar()
        self.selected_second_mixer_component.set(self.mixer_list[4])
        self.selected_first_img_select = StringVar()
        self.selected_first_img_select.set(self.img_list[0])
        self.selected_second_img_select = StringVar()
        self.selected_second_img_select.set(self.img_list[1])
        self.selected_output = StringVar()
        self.selected_output.set(self.out_list[0])


        self.fig = plt.figure(figsize=(10.0, 5.0), linewidth=30.0)
        self.ax = self.fig.add_subplot(111)


        self.frameimg1 = self.generate_frame(80,0,window)
        self.frameimg2 = self.generate_frame(80,450,window)

        self.framemixer =self.generate_frame(800,0,window)

        self.frameoutput =self.generate_frame(800,450,window)
        
        self.labelimg1 = Label(self.frameimg1, text="Image 1", fg="black", font="25")
        self.labelimg1.place(x=5, y=5)

        self.Browsebutton = Button(self.frameimg1, height=2, width=25, text='Open File', command=functools.partial(self.loadimage, 0))
        self.Browsebutton.place(x=300, y=10)

        self.drop1 = OptionMenu(self.frameimg1, self.selected_first_img_component, *self.component_list, command=functools.partial(self.update, 0))
        self.drop1.place(x=520, y=15)

        self.canvas1 = FigureCanvasTkAgg(self.fig, self.frameimg1)
        self.canvas1.get_tk_widget().place(height=300, width=300, x=50, y=90)
        self.canvas1.OGimg1 = plt.subplot()
        plt.axis('off')

        self.canvas2 = FigureCanvasTkAgg(self.fig, self.frameimg1)
        self.canvas2.get_tk_widget().place(height=300, width=300, x=350, y=90)
        self.canvas2.Modimg1 = plt.subplot()

        self.labelimg2 = Label(self.frameimg2, text="Image 2", fg="black", font="25")
        self.labelimg2.place(x=5, y=5)

        self.Browsebutton2 = Button(self.frameimg2, height=2, width=25, text='Open File', command=functools.partial(self.loadimage, 1))
        self.Browsebutton2.place(x=300, y=10)

        self.drop2 = OptionMenu(self.frameimg2, self.selected_second_img_component, *self.component_list, command=functools.partial(self.update, 1))
        self.drop2.place(x=520, y=15)

        self.canvas3 = FigureCanvasTkAgg(self.fig, self.frameimg2)
        self.canvas3.get_tk_widget().place(height=300, width=300, x=50, y=90)
        self.canvas3.OGimg2 = plt.subplot()


        plt.axis('off')
        self.selected_first_img_select.get()
        self.canvas4 = FigureCanvasTkAgg(self.fig, self.frameimg2)
        self.canvas4.get_tk_widget().place(height=300, width=300, x=350, y=90)
        self.canvas4.Modimg2 = plt.subplot()
        self.selected_second_img_component.get()
        self.labelmixer = Label(self.framemixer, text="Mixer Output to: ", fg="black", font="25")
        self.labelmixer.place(x=5, y=5)

        self.labelcomp1 = Label(self.framemixer, text="Component 1: ", fg="black", font="25")
        self.labelcomp1.place(x=5, y=100)
        if self.selected_second_mixer_component.get() == 'Imag':
            self.comp1options = OptionMenu(self.framemixer, self.selected_first_mixer_component, *self.mixer_list[2])
        else:
            self.comp1options = OptionMenu(self.framemixer, self.selected_first_mixer_component, *self.mixer_list[0:3])
        self.comp1options.place(x=520, y=150)


        self.comp1setimg = OptionMenu(self.framemixer, self.selected_first_img_select, *self.img_list)
        self.comp1setimg.place(x=150, y=100)

        self.comp1 = Scale(self.framemixer, from_=0, to=100, orient=HORIZONTAL, command=functools.partial(self.pre_mix, 0))
        self.comp1.place(x=500, y=100)

        self.labelcomp2 = Label(self.framemixer, text="Component 2: ", fg="black", font="25")
        self.labelcomp2.place(x=5, y=225)

        self.comp2 = Scale(self.framemixer, from_=0, to=100, orient=HORIZONTAL, command=functools.partial(self.pre_mix, 1))
        self.comp2.place(x=500, y=225)

        self.comp2setimg = OptionMenu(self.framemixer, self.selected_second_img_select, *self.img_list)
        self.comp2setimg.place(x=150, y=225)

        self.comp2options = OptionMenu(self.framemixer, self.selected_second_mixer_component, *self.mixer_list[3:])
        self.comp2options.place(x=520, y=275)

        self.outputlist = OptionMenu(self.framemixer, self.selected_output, *self.out_list)
        self.outputlist.place(x=500, y=5)
        self.selected_first_mixer_component.get()
        self.selected_second_mixer_component.get()
        self.selected_first_img_select.get()
        self.selected_second_img_select.get()
        self.selected_output.get()

        self.diplay_mix = None
        ##########################Frame Output###################################

        self.labelout1 = Label(self.frameoutput, text="Output 1", fg="black", font="25")
        self.labelout1.place(x=150, y=50)

        self.labelout2 = Label(self.frameoutput, text="Output 2", fg="black", font="25")
        self.labelout2.place(x=450, y=50)

        self.canvas5 = FigureCanvasTkAgg(self.fig, self.frameoutput)
        self.canvas5.get_tk_widget().place(height=300, width=300, x=50, y=90)
        self.canvas5.Output1 = plt.subplot()
        plt.axis('off')
        self.image1 = None
        self.image2 = None
        self.canvas6 = FigureCanvasTkAgg(self.fig, self.frameoutput)
        self.canvas6.get_tk_widget().place(height=300, width=300, x=350, y=90)
        self.canvas6.Output2 = plt.subplot()
        plt.axis('off')
    def loadimage(self,x):
        if x==0:
            self.image1 = ImageClass()
            selected_image = self.image1.load_image()
            self.canvas1.OGimg1.imshow(selected_image, cmap=cm.Greys_r)
            self.canvas1.draw()
        if x==1:
            self.image2 = ImageClass()
            selected_image = self.image2.load_image()
            self.canvas3.OGimg2.imshow(selected_image, cmap=cm.Greys_r)
            self.canvas3.draw()
    def update(self,x,y):
        if x ==0:
            display = self.image1.select_component(self.selected_first_img_component.get())
            self.canvas2.Modimg1.imshow(display, cmap=cm.Greys_r)
            self.canvas2.draw()
        if x==1:
            display = self.image2.select_component(self.selected_second_img_component.get())
            self.canvas4.Modimg2.imshow(display, cmap=cm.Greys_r)
            self.canvas4.draw()
    def pre_mix(self,x,y):

        if self.selected_first_img_select.get() == "Image 1":
            component = self.selected_first_mixer_component.get()
            self.diplay_mix = self.image1.mixer(self.image2,component,self.comp1.get(),self.comp2.get())
        elif self.selected_first_img_select.get() == "Image 2":
            component = self.selected_second_mixer_component.get()
            self.diplay_mix =self.image2.mixer(self.image1,component,self.comp1.get(),self.comp2.get())

        if self.selected_second_img_select.get() == "Image 1":
            component = self.selected_second_mixer_component.get()
            self.diplay_mix =self.image1.mixer(self.image2,component,self.comp1.get(),self.comp2.get())
        elif self.selected_second_img_select.get() == "Image 2":
            component = self.selected_second_mixer_component.get()
            self.diplay_mix =self.image2.mixer(self.image1,component,self.comp1.get(),self.comp2.get())
        if self.selected_output.get() == 'Output 1':
            self.canvas5.Output1.imshow(self.diplay_mix, cmap=cm.Greys_r)
            self.canvas5.draw()
        if self.selected_output.get() == 'Output 2':
            self.canvas6.Output2.imshow(self.diplay_mix, cmap=cm.Greys_r)
            self.canvas6.draw()
    def generate_frame(self,x,y,window):
        temp_frame = tk.Frame(master=window, highlightbackground="black", highlightcolor="black", highlightthickness=2)
        temp_frame.place(height=400, width=680, x=x, y=y)
        temp_frame.config(background="white")
        return temp_frame




