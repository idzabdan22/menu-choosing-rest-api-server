# import the opencv library
import cv2
import json
import os
# define a video capture object
vid = cv2.VideoCapture(0)

with open("output/runningPid.json", "r") as jsonFile:
	data = json.load(jsonFile)

pid = os.getpid()
data["running_pid"] = pid         

with open("output/runningPid.json", "w") as jsonFile:
	json.dump(data, jsonFile)

while(True):
	# Capture the video frame
	# by frame
	ret, frame = vid.read()

	# Display the resulting frame
	cv2.imshow('frame1', frame)
	cv2.setWindowProperty('frame1', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	
	cv2.imshow('frame2', frame)
	cv2.setWindowProperty('frame2`', cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
	cv2.moveWindow("frame", -10000, -50000)
	cv2.namedWindow('frame', flags=cv2.WINDOW_FULLSCREEN)
	
	# the 'q' button is set as the
	# quitting button you may use any
	# desired button of your choice
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
