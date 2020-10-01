import matplotlib.pyplot as plt
import matplotlib.image as mpimg

path = 'C:/Users/RbRb/Desktop/monitor1.png'
while 1:
	plt.figure("scope")
	scr = mpimg.imread(path, 0)
	plt.imshow(scr)
	plt.show()