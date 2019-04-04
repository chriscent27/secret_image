Purpose: 
	Steganography is the technique of hiding secret messages within 
	  an ordinary, non-secret, image, in order to avoid detection. 

 	  The secret message is then extracted at its destination without loss in data.
	  The difference in the original image and the modified image cannot be spotted by 
	  the naked eye.

	  Please note that this module only works with '.png' files. This is because,
	  they use lossless compression techniques to store and read images.

Requirements:
	Python(3.4 or greater)
	PIL(module in Python)


Steps to:
	Create Secret image:
		Step 1 : Put the .png file in the '/image/' directory.
		Step 2 : Put the message text in the file 'message.txt'.
		Step 3 : Run the script, when the input prompt comes. Select '1' and press Enter.
		Step 4 : The modified image will be saved in the parent folder. 
				 The image will have the same filename as the source image.

	Read from Secret image:
		Step 1 : Put the image in the '/image/' directory.
		Step 2 : Run the script, when the input prompt comes. Select '2' and press Enter.
				  The secret message will be displayed on the screen.

PS: Please note that if you are planning to send the image through the internet. It is recommended
	 that you zip the image file and then send. If you try to upload the image directly, majority of the web sites compress the image  before sending and this will modify the pixel data. This may modify the message data stored. To avoid please zip the file.