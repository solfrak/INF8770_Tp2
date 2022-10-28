# importing libraries
import cv2
import numpy as np
from matplotlib import pyplot as plt

import utils_tp as utils

# 1 - OPEN THE VIDEO
# Create a VideoCapture object and read from input file
cap = cv2.VideoCapture('video.mp4')
# Check if camera opened successfully
if (cap.isOpened()== False): 
  print("Error opening video  file")

# 2 - ISOLATE THE SEQUENCES WE WANT
frame_no_1 = 16
frame_no_2 = 150
frame_sequence_1 = utils.extract_sequence(cap, frame_no_1)
frame_sequence_2 = utils.extract_sequence(cap, frame_no_2)

# 3 - FOR EACH FRAME, CUT THE FRAME IN MACROBLOC
nb_frame = len(frame_sequence_1)
for n in range(nb_frame):
    frame = frame_sequence_1[n]
    list_of_macrobloc = utils.macroblock(frame)

    # 4 - ESTIMATE VECTOR OF MOVEMENT
    if n>0: # The first frame is an type I, we estimate the movement only for type P
        prev_frame = frame_sequence_1[n-1]
        list_of_macrobloc = utils.update_vect_mouvement(list_of_macrobloc, frame, prev_frame)

    print(list_of_macrobloc[25])





# Read until video is completed
# while(cap.isOpened()):
      
#   # Capture frame-by-frame
#   if ret == True:
   
#     # Display the resulting frame
#     #cv2.imshow('Frame', frame)
#     # Press Q on keyboard to  exit
#     if cv2.waitKey(25) & 0xFF == ord('q'):
#       break
   
#   # Break the loop
#   else: 
#     break
   
# When everything done, release 
# the video capture object
cap.release()
   
# Closes all the frames
cv2.destroyAllWindows()


macroblock = {
    "ADDR": [0, 1],
    "TYPE": "I",
    "VECT": [0, 1],
    "BCP": 0b0000,
    "BLOCK": [0,0,0,0]
}