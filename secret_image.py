"""	Steganography is the technique of hiding secret messages within 
	an ordinary, non-secret, image in order to avoid detection. 

	The secret message is then extracted at its destination without loss in data.
	The difference in the original image and the modified image cannot be spotted by 
	the naked eye. 

	Please note that this module only works with '.png' files. This is because,
	they use lossless compression techniques to store and read images.
"""
import os
from PIL import Image

class Steganography(object):
	"""	This class simulates an easy way of achieving steganograpy.

		You can use it to hide messages in an image and also to retrieve it.
		There wont be any visible difference in the image due to this.
	"""
	image_obj = None
	pixel_data = None
	resolution = list()
	message = str()
	binary_message = str()
	filepath = str()

	def __init__(self, filepath=None):
		"""	The constructor of the class.
		"""
		self.filepath = filepath or self.get_image_filepath()

	def get_image_filepath(self):
		"""	Automatically detects the file in the image folder.

			Searches the image folder and returns the filepath of the image
			as a string. Checks if there is eactly one file in the folder.

			returns (str): Returns the filePath as a string.
		"""
		files = os.listdir(path='./image/')
		if len(files) != 1:
			print('\n\nPlease copy the picture in the image folder and then run the script..\n\n\n\n')
			exit()

		return "./image/{}".format(files[0])

	def set_image_data(self):
		"""	The image file is read here.

			The image is read and the pixel data and other values are 
			stored inside the class variables.
		"""
		try:
			self.image_obj = Image.open(self.filepath)
			self.pixel_data = self.image_obj.load()
			self.resolution = self.image_obj.size  # Get the width and height of the image for iterating over it.
		except :
			print('Please copy a ".png" file in the image folder and run the script!!')
			exit()

	def read_message_file(self):
		"""	The message file is read and is kept in the class variable.
		"""
		with open('message.txt', 'r') as f:
			self.message = f.read()

	def set_binary_message(self):
		"""	The message is converted to binary.

			Each letter in the message is converted to ascii value first.
			Then converted to binary of 7 bits each. This value is appended 
			to a string in the end.
		"""
		for string in self.message:
			ascii = ord(string)
			if ascii > 126:
				continue
			
			binary = bin(ascii)[2:].zfill(7)
			self.binary_message += binary

		self.binary_message += '1' * 13 # Denotes the end of string.

	def modify_pixel_data(self):
		"""	The red pixel value is modulated accordingly to the message data.

			Each pixel value is taken and the LSB(Least Significant Bit) is changed according to the
			message's binary data.
		"""
		width, height = self.resolution
		total_count = len(self.binary_message)
		if width * height < total_count:
			print('The picture resolution is too less to store message..')
			return

		index = 0
		for x in range(width):
			for y in range(height):
				bit_to_add = int(self.binary_message[index])
				pixel_value = list(self.pixel_data[x,y])
				
				if (pixel_value[0] % 2) != bit_to_add:
					if pixel_value[0] == 255:
						pixel_value[0] -= 1
					else:
						pixel_value[0] += 1

				self.pixel_data[x,y] = tuple(pixel_value)
				index += 1
				if index == total_count-1:
					return

	def save_modified_image(self):
		"""	Saves the modified image as a file in the parent folder.

			The modulated pixel data is used to create the new image and 
			it is saved with the same filename in the parent folder.
		"""
		filepath = self.filepath
		filepath = filepath.replace('/image', '')
		try:
			self.image_obj.save(filepath)
		except:
			filepath += ".png"
			self.image_obj.save(filepath)

		print('\n\n\nModified the image, and saved in parent folder!  \n\n')

	def create_image_with_message(self):
		""" Creates the image along with the message data.

			Reads the image data, modulates the pixel data according to the
			binary form of the message data and save the modified pixels as 
			the new image.
		"""
		self.set_image_data()
		self.modify_pixel_data()
		self.save_modified_image()

	def add_message_to_image(self):
		"""	Reads message and modifies the image accordingly.

			This is where the steganography processes is simulated. The message and 
			image is read first, then the message is converted to binary, then image pixel's
			RGB value is taken one by one. 

			The LSB of the red value for each pixel is modified to reflect the binary data of
			the message. Once this is done, a new image is created with the modified pixels.
		"""
		self.read_message_file()
		self.set_binary_message()
		self.create_image_with_message()

	def find_message(self):
		""" This method finds the text data from the image.

			The method iterates through the red component value of each pixel and
			stores the LSB one by one, once it stores 7 bits, it converts it to
			integer and then to character using ascii.

			These characters are appended to get the sored message.
		"""
		width, height = self.resolution
		byte = []
		message = str()
		for x in range(width):
			for y in range(height):
				pixel_value = self.pixel_data[x,y][0]
				bit = str(pixel_value % 2)
				byte.append(bit)
				if len(byte) == 7:
					binary = '0b' + "".join(byte)
					decimal = int(binary, 2)
					byte = []
					if decimal == 127:
						self.message = message
						return
					message += chr(decimal)

		print("Message not found. Please check the image!!!")

	def display_message(self):
		""" This method displays the message in a widget.

			The widget will show the text using tkinter and the text is scrollable.
		"""
		widget = MessageWidget(self.message)
		widget.show_message()

	def get_message_from_image(self):
		"""	This method finds and displays the message from the image provided.

			The image pixel data is read and set in class variables, from these
			the message is extracted and finally displayed in the widget.
		"""
		self.set_image_data()
		self.find_message()
		self.display_message()

class MessageWidget(object):
	""" Creates a message widget which can show long messages.

		The text display area is made scrollable so that long messages can be 
		displayed and scrolled.
	"""
	def __init__(self, message):
		""" Constructor of the class.
		"""
		self.message = message

	def show_message(self):
		""" This method displays the text message.
		"""
		from tkinter import (
			Tk,
			Scrollbar,
			Text,
			mainloop,
			RIGHT,
			LEFT,
			Y,
			END
		)
		root = Tk()
		S = Scrollbar(root)
		T = Text(root, height=100, width=150)
		S.pack(side=RIGHT, fill=Y)
		T.pack(side=LEFT, fill=Y)
		S.config(command=T.yview)
		T.config(yscrollcommand=S.set)
		T.insert(END, self.message)
		mainloop(  )

if __name__ == '__main__':
	st = Steganography()
	choice = int(input('Enter: \n1 to add message to image \n2 to read message from image\n\nEnter your choice: '))
	if choice == 1:
		st.add_message_to_image()
	elif choice == 2:
		st.get_message_from_image()
	else:
		print('Invalid choice...')