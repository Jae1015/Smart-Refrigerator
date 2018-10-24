# this script captures image with Pi Camera
# performs image recognition using AWS Rekognition Engine
# and then calls AWS Polly Speech Synthesis API to describe the items found in the image

# function to capture image with Pi Camera
#def capture_image(image_file):
#	import picamera
#	camera = picamera.PiCamera()
#	camera.vflip = True
#	camera.capture(image_file)
#	camera.close()


# image recognition code
# takes an image file as input and
# returns the list of items recognized in the image
def image_recognition(image_file):

	# import aws boto3 library
	import boto3

	items = []

	# list of labels to be ignored as stop-words
	# mostly generic words like fruit, vegetable, food etc.
	stoplist = ['Fruit', 'Produce', 'Plant', 'Vegetable', 'Food','Flora','Nut','Leaf','Citrus Fruit','Grapefruit']

	# calling aws rekognition api on image-file
	client = boto3.client('rekognition',region_name='us-east-2')
	with open(image_file, "rb") as image:
		# object recognition from the image
		print "opened"
		result = client.detect_labels(Image={'Bytes': image.read()}, MaxLabels=20, MinConfidence=50)
		print "1"
		# processing json output to get image labels
		for label in result['Labels']:
			if label['Name'] not in stoplist:
				items.append(label['Name'])
				print "2"

	return items

# capture image and identify objects in the image
image_file = "im.jpg"
#capture_image(image_file)
print "function called"
items = image_recognition(image_file)
print "function returned"
print items

