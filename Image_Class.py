import logging
import scipy.fftpack
from tkinter.filedialog import askopenfilename
from PIL import Image
import numpy as np
from tkinter import messagebox

logging.basicConfig(filename='log.log',level=logging.DEBUG)
class ImageClass:
    no_imgs = 0
    ref_width = 0
    ref_height =0 
    def __init__(self):
        self.no_imgs = ImageClass.no_imgs
        ImageClass.no_imgs +=1
        self.is_imaginary = False
        logging.info('num_imgs is ',self.no_imgs)

    #@classmethod
    def load_image(self):
        if self.no_imgs ==0:
            filename = askopenfilename()
        else:
            filename = askopenfilename()
            temp = Image.open(filename)
            while temp.size[0] != ImageClass.ref_width and temp.size[1] !=ImageClass.ref_height:
                print(temp.size[0])
                logging.debug(ImageClass.ref_width)
                messagebox.showerror("Size Error!","Please select images of tha same size.")
                logging.error("Size Error. Choose same size of the image")
                filename = askopenfilename()
                temp = Image.open(filename)
        self.image_data = Image.open(filename)
        self.width,self.height = self.image_data.size
        ImageClass.ref_height = self.height
        ImageClass.ref_width = self.width
        self.image_data = np.asarray(self.image_data)
        self.gray_image = np.mean(self.image_data,axis=2)
        self.img_fft = scipy.fftpack.fftshift(scipy.fftpack.fft2(self.gray_image))
        self.img_mag = np.abs(self.img_fft) # khod el log hena 3lshan haga tezhar
        self.img_phase = np.angle(self.img_fft)
        logging.info('Image loaded')
        return self.gray_image


    def select_component(self,component):

        logging.debug(component)
        if component == 'Mag':
            self.img_display = np.log(self.img_mag)
        elif component == "Phase":
            self.img_display = self.img_phase
        elif component == "Real":
            self.img_display = Image.fromarray(self.img_fft.real)
        elif component == "Imag":
            self.img_display = Image.fromarray(self.img_fft.imag) 
        return self.img_display


    def mixer(self, img1,selected_component,slider_value1,slider_value2):

        slider_value1 = slider_value1/100
        slider_value2 = slider_value2/100
        #out_img = self.gray_image + img1.gray_image
        #output_img = scipy.fftpack.fftshift(scipy.fftpack.fft2(out_img))
        if selected_component == "Mag":
            self.reconst_img_fft_mag = slider_value1*self.img_mag + (1-slider_value1)*img1.img_mag
            self.reconst_img_fft_phase = slider_value2*img1.img_phase + (1-slider_value2)*self.img_phase
        elif selected_component == "Phase":
            self.reconst_img_fft_mag = slider_value1 * img1.img_mag + (1 - slider_value1) * self.img_mag
            self.reconst_img_fft_phase = slider_value2 * self.img_phase + (1 - slider_value2) * img1.img_phase

        elif selected_component == "Real":
            self.reconst_img_fft_real = slider_value1*self.img_fft.real + (1-slider_value1) * img1.img_fft.real
            self.reconst_img_fft_imag = slider_value2*img1.img_fft.imag + (1-slider_value2)*self.img_fft.imag
            self.is_imaginary = True
        elif selected_component == "Imag":
            self.reconst_img_fft_imag = slider_value2*self.img_fft.imag + (1-slider_value2) * img1.img_fft.imag
            self.reconst_img_fft_real = slider_value1*img1.img_fft.real + (1-slider_value1)*self.img_fft.real
            self.is_imaginary = True
        elif selected_component == "UniMag":
            self.reconst_img_fft_mag = 1*slider_value1+ (1-slider_value1)*img1.img_mag
            self.reconst_img_fft_phase = slider_value2*img1.img_phase + (1-slider_value2)*self.img_phase

        elif selected_component == "UniPhase":
            self.reconst_img_fft_phase = slider_value2* img1.img_phase
            self.reconst_img_fft_mag = slider_value1 * img1.img_mag + (1 - slider_value1) * self.img_mag
        if self.is_imaginary:
            self.reconst_img_fft = np.add(self.reconst_img_fft_real,(1j*self.reconst_img_fft_imag))
        else:
            self.reconst_img_fft = np.multiply(self.reconst_img_fft_mag,np.exp(1j*self.reconst_img_fft_phase))
        self.reconst_img = scipy.fftpack.ifft2(scipy.fftpack.fftshift(self.reconst_img_fft)).real
        self.reconst_img = Image.fromarray(self.reconst_img)
        return self.reconst_img



