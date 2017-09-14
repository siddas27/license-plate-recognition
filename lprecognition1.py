
# coding: utf-8

# In[1]:
def getdata(file):
	from skimage.io import imread
	import numpy as np
	from skimage.filters import threshold_otsu
	import matplotlib.pyplot as plt
	#get_ipython().magic(u'matplotlib inline')


# In[2]:

	car_image = imread(file, as_grey=True)
	# it should be a 2 dimensional array
	#print(car_image.shape)


	# In[3]:

	gray_car_image = car_image * 255
	fig, (ax1, ax2) = plt.subplots(1, 2)
	ax1.imshow(gray_car_image, cmap="gray")
	threshold_value = threshold_otsu(gray_car_image)
	binary_car_image = gray_car_image > threshold_value
	ax2.imshow(binary_car_image, cmap="gray")
	plt.show()


	# In[4]:

	from skimage import measure
	from skimage.measure import regionprops
	import matplotlib.pyplot as plt
	import matplotlib.patches as patches

	# this gets all the connected regions and groups them together
	label_image = measure.label(binary_car_image)
	fig, (ax1) = plt.subplots(1)
	ax1.imshow(gray_car_image, cmap="gray");

	# regionprops creates a list of properties of all the labelled regions
	for region in regionprops(label_image):
	    if region.area < 50:
		#if the region is so small then it's likely not a license plate
		continue

	    # the bounding box coordinates
	    minRow, minCol, maxRow, maxCol = region.bbox
	    rectBorder = patches.Rectangle((minCol, minRow), maxCol-minCol, maxRow-minRow, edgecolor="red", linewidth=2, fill=False)
	    ax1.add_patch(rectBorder)
	    # let's draw a red rectangle over those regions

	plt.show()


	# In[15]:

	from skimage import measure
	from skimage.measure import regionprops
	import matplotlib.pyplot as plt
	import matplotlib.patches as patches

	# this gets all the connected regions and groups them together
	label_image = measure.label(binary_car_image)

	# getting the maximum width, height and minimum width and height that a license plate can be
	plate_dimensions = (0.06*label_image.shape[0], 0.10*label_image.shape[0], 0.15*label_image.shape[1], 0.4*label_image.shape[1])
	min_height, max_height, min_width, max_width = plate_dimensions
	plate_objects_cordinates = []
	plate_like_objects = []
	fig, (ax1) = plt.subplots(1)
	ax1.imshow(gray_car_image, cmap="gray");

	# regionprops creates a list of properties of all the labelled regions
	for region in regionprops(label_image):
	    if region.area < 50:
		#if the region is so small then it's likely not a license plate
		continue

	    # the bounding box coordinates
	    min_row, min_col, max_row, max_col = region.bbox
	    region_height = max_row - min_row
	    region_width = max_col - min_col
	    # ensuring that the region identified satisfies the condition of a typical license plate
	    if region_height >= min_height and region_height <= max_height and region_width >= min_width and region_width <= max_width and region_width > region_height:
		plate_like_objects.append(binary_car_image[min_row:max_row,
		                          min_col:max_col])
		plate_objects_cordinates.append((min_row, min_col,
		                                      max_row, max_col))
		rectBorder = patches.Rectangle((min_col, min_row), max_col-min_col, max_row-min_row, edgecolor="red", linewidth=2, fill=False)
		ax1.add_patch(rectBorder)
	    # let's draw a red rectangle over those regions

	plt.show()


	# In[66]:

	from skimage.transform import resize

	license_plate = np.invert(plate_like_objects[0])

	labelled_plate = measure.label(license_plate)

	fig, ax1 = plt.subplots(1)
	ax1.imshow(license_plate, cmap="gray")

	character_dimensions = (0.35*license_plate.shape[0], 0.70*license_plate.shape[0], 0.04*license_plate.shape[1], 0.70*license_plate.shape[1])
	min_height, max_height, min_width, max_width = character_dimensions

	characters = []
	counter=0
	column_list = []
	for regions in regionprops(labelled_plate):
	    y0, x0, y1, x1 = regions.bbox
	    region_height = y1 - y0
	    region_width = x1 - x0

	    if region_height > min_height and region_height < max_height and region_width > min_width and region_width < max_width:
		roi = license_plate[y0:y1, x0:x1]

		# draw a red bordered rectangle over the character.
		rect_border = patches.Rectangle((x0, y0), x1 - x0, y1 - y0, edgecolor="red",linewidth=2, fill=False)
		ax1.add_patch(rect_border)

		# resize the characters to 20X10 and then append each character into the characters list
		resized_char = resize(roi, (20, 10))
		characters.append(resized_char)

		# this is just to keep track of the arrangement of the characters
		column_list.append(x1)
	#print(column_list)
	plt.show()


	# In[38]:

	import os
	import numpy as np
	from sklearn.svm import SVC
	from sklearn.model_selection import cross_val_score
	from sklearn.externals import joblib
	from skimage.io import imread
	from skimage.filters import threshold_otsu

	letters = [
		    '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D',
		    'E', 'F', 'G', 'H', 'J', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T',
		    'U', 'V', 'W', 'X', 'Y', 'Z'
		]

	def read_training_data(training_directory):
	    image_data = []
	    target_data = []
	    for each_letter in letters:
		for each in range(10):
		    image_path = os.path.join(training_directory, each_letter, each_letter + '_' + str(each) + '.jpg')
		    # read each image of each character
		    img_details = imread(image_path, as_grey=True)
		    # converts each character image to binary image
		    binary_image = img_details < threshold_otsu(img_details)
		    flat_bin_image = binary_image.reshape(-1)
		    image_data.append(flat_bin_image)
		    target_data.append(each_letter)
	    return (np.array(image_data), np.array(target_data))

	def cross_validation(model, num_of_fold, train_data, train_label):
	    accuracy_result = cross_val_score(model, train_data, train_label,cv=num_of_fold)
	    #print("Cross Validation Result for "+ str(num_of_fold)+ " -fold")

	    #print(accuracy_result * 100)


	current_dir = os.path.dirname(os.path.realpath('__file__'))

	training_dataset_dir = os.path.join(current_dir, 'train')

	image_data, target_data = read_training_data(training_dataset_dir)


	svc_model = SVC(kernel='linear', probability=True)

	cross_validation(svc_model, 4, image_data, target_data)

	# let's train the model with all the input data
	svc_model.fit(image_data, target_data)


	# In[67]:

	classification_result = []
	for each_character in characters:
	    # converts it to a 1D array
	    each_character = each_character.reshape(1, -1);
	    result = svc_model.predict(each_character)
	    classification_result.append(result)

	#print(classification_result)

	plate_string = ''
	for eachPredict in classification_result:
	    plate_string += eachPredict[0]



	column_list_copy = column_list[:]
	column_list.sort()
	rightplate_string = ''
	for each in column_list:
	    rightplate_string += plate_string[column_list_copy.index(each)]

	#print(rightplate_string)


	# In[47]:

	import pandas as pd
	df=pd.read_csv('sdata.csv')
	dfs=pd.read_csv('mh.csv')


	# In[68]:
	v=''
	w=''
	for x in df['Code']:
	    if plate_string[0:2]==str(x):
		v=v+x
	g=df[df['Code']==v]
	#print(g['State'])
	plate_string1=rightplate_string[0:2]+'-'+rightplate_string[2:4]
	for y in dfs['code'] :
	    if plate_string1[0:5]==str(y):
		w=w+y
	h=dfs[dfs['code']==str(w)]
	#print(h['area'])
	s='license plate number '+rightplate_string #'State'+str(g.value)+'Area'+str(h.value)
	return s
	# In[ ]:

