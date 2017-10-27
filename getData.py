import numpy as np
import scipy.io
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
from PIL import Image





if __name__ == "__main__":
	mat = scipy.io.loadmat('registered2b.mat')

	#for key, value in mat.items():
	#	print key

	data = mat['data']
	print len(data[0])		# this file has 62 patients
	print len(data[0][0])	# each patient has 8 structs 


	#for i in data[0][0]: 
	#	print type(i)
	
	
	i = 1
	for patient in data[0]:	# for each patient
		picName = 'slide_roi/slide_roi_patient_' + str(i) + '.png'
		scipy.misc.imsave(picName, patient[0])
		picName = 't2/t2_patient_' + str(i) + '.png'
		scipy.misc.imsave(picName, patient[1])
		i = i + 1

	
