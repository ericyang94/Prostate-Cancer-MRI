import numpy as np
import scipy.io
from matplotlib import pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import scipy.misc
import sys
from sklearn.metrics import roc_auc_score
from sklearn.ensemble import RandomForestClassifier



if __name__ == "__main__":

	if (len(sys.argv) != 2):
		print "wrong number of arguments"
		print "Usage: python run.py <filter_degree>"
		print "Exmaple: python run.py 2"
		exit(1)

	mat = scipy.io.loadmat('registered2b.mat')

	data = mat['data']
	#print len(data[0])		# this file has 62 patients
	#print len(data[0][0])	# each patient has 8 structs 
	#print data[0][0][0][1,10]						# each struct is (256 x 256) numpy array


	filter_degree = int(sys.argv[1])
	#print filter_degree

	# User can add more to this filtered list of patients with accurate data 
	filtered_list = [1, 4, 19, 46, 62] 
	score_list = []

	# cross-validation
	for test_subject in filtered_list:
		print "Starting cross-validation with test_subject is patient number", test_subject
		# get traning and testing data 
		index = 1 
		x_training = []
		y_training = []
		for patient in data[0]:
			# patient[0] = slide_roi
			# patient[1] = t2
			if (index not in filtered_list):
				index = index + 1
				continue

			x_values = []
			y_values = []
			for i in range(filter_degree, 255 - filter_degree):
				for j in range(filter_degree, 255 - filter_degree):
					if (patient[0][i,j] != 0):			
						x_values.append(patient[1][i-filter_degree : i+filter_degree+1 , j-filter_degree : j+filter_degree+1].flatten())
						if (round(patient[0][i,j]) == 2.0):
							y_values.append(1)
						else:
							y_values.append(0)

			if (test_subject == index):
				x_test = x_values
				y_test = y_values 
			else:
				x_training = x_training + x_values
				y_training = y_training + y_values
			print "done with patient", index
			index = index + 1
			

		# use machine learning
		machineLearning = RandomForestClassifier()
		machineLearning.fit(x_training, y_training)
		y_result = machineLearning.predict(x_test)
		score = roc_auc_score(y_test, y_result)
		score_list.append(score)
		print "score for this round is:", score


	myAve = 0.0
	for score in score_list:
		myAve = myAve + score
	myAve = myAve / len(score_list)
	print "Average score is:", myAve
	



	