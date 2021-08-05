###############################################################################
'''
This code was wrote by Stéfano Frizzo Stefenon
If you use it, please reference our papers.
Thank you, enjoy!
'''
###############################################################################

# Import libraries to compile
import numpy as np
import cv2 
import mahotas
import glob
import time

###############################################################################
# Time of the simulation
start = time.time()

# If you wish to sabe the pictures (y)
y1=0
y1=str(input('Do you wanna SAVE all the pictures? (y): '))

###############################################################################
# Read the files
img_o = [cv2.imread(file) for file in glob.glob("*.jpg")]

# Vector size
ln=len(img_o)

# Matrices
img = suave = {}
result1 = result2 = result3 = result4 = result5 = result6 = {}
MEANa = MEANb = MEAN1 = MEAN2 = MEAN3 = MEAN4 = MEAN5 = {}

###############################################################################
# RGB to Gray
for i in range(0,ln):
    img[i] = cv2.cvtColor(img_o[i], cv2.COLOR_BGR2GRAY) 
    MEANa[i] = np.mean(img[i])
    print(MEANa[i])              
    #if y1=='y' or y1=='Y':
        #cv2.imwrite('I1_%02i.jpg' %i, img[i]) # BGR2GRAY

###############################################################################
# Apply blur 
for i in range(0,ln):
    suave[i] = cv2.GaussianBlur(img[i], (5, 5), 0)
    MEANb[i] = np.mean(suave[i])
    print(MEANb[i])
    if y1=='y' or y1=='Y':
        cv2.imwrite('I2_%02i.jpg' %i, suave[i]) # GaussianBlur

###############################################################################
# Binarization with threshold
for i in range(0,ln):
    (T, binI) = cv2.threshold(suave[i], 160, 255, cv2.THRESH_BINARY_INV)
    result1[i] = np.vstack([np.hstack([cv2.bitwise_and(img[i], img[i], 
        mask = binI)])])
    MEAN1[i] = np.mean(result1[i])
    print(MEAN1[i])
    if y1=='y' or y1=='Y': 
        cv2.imwrite('I3_%02i.jpg' %i, result1[i]) # Binarization 

###############################################################################
# Adaptive threshold
for i in range(0,ln):
    bin2 = cv2.adaptiveThreshold(suave[i], 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 21, 5)
    result2[i] = np.vstack([np.hstack([bin2])])
    MEAN2[i] = np.mean(result2[i])
    print(MEAN2[i])
    if y1=='y' or y1=='Y':
        cv2.imwrite('I4_%02i.jpg' %i, result2[i]) # Adaptive threshold
     
###############################################################################
# Threshold with Otsu and Riddler-Calvard
for i in range(0,ln):
    T = mahotas.thresholding.otsu(suave[i])
    temp = img[i].copy()
    temp[temp > T] = 255
    temp[temp < 255] = 0
    temp = cv2.bitwise_not(temp)
    T = mahotas.thresholding.rc(suave[i])
    temp2 = img[i].copy()
    temp2[temp2 > T] = 255
    temp2[temp2 < 255] = 0
    temp2 = cv2.bitwise_not(temp2)
    result3[i] = np.vstack([np.hstack([temp2])]) 
    MEAN3[i] = np.mean(result3[i])
    print(MEAN3[i])
    if y1=='y' or y1=='Y':
        cv2.imwrite('I5_%02i.jpg' %i, result3[i]) # Bin. (Thres.) Otsu and Rid.
     
###############################################################################
# Canny
for i in range(0,ln):
    canny1 = cv2.Canny(suave[i], 20, 100)
    result4[i] = np.vstack([canny1])
    MEAN4[i] = np.mean(result4[i])
    print(MEAN4[i])
    if y1=='y' or y1=='Y':
        cv2.imwrite('I6_%02i.jpg' %i, result4[i]) # Cany
   
###############################################################################
# Sobel
for i in range(0,ln):
    sobelX = cv2.Sobel(suave[i], cv2.CV_64F, 1, 0)
    sobelY = cv2.Sobel(suave[i], cv2.CV_64F, 0, 1)
    sobelX = np.uint8(np.absolute(sobelX))
    sobelY = np.uint8(np.absolute(sobelY))
    sobel = cv2.bitwise_or(sobelX, sobelY)
    result5[i] = np.vstack([sobel]) 
    MEAN5[0] = np.mean(result5[0])
    MEAN5[i] = np.mean(result5[i])
    print(MEAN5[i])
    if y1=='y' or y1=='Y':
        cv2.imwrite('I7_%02i.jpg' %i, result5[i]) # Sobel

###############################################################################
# Show the pictures

y=str(input('Do you wanna SEE all the pictures? (y): '))
if y=='y' or y=='Y': # It is 8 pictures for each file
    n=int(input('How many perspectives do you need: '))
    for i in range(0,n):
        cv2.imshow('Binarization_Limiar', result1[i]) # Binarization_Limiar
        cv2.imshow('Binar._Threshold', result2[i]) # Binarization_Threshold
        cv2.imshow('Binar._Thr._O&R', result3[i]) # Binar._Thres. Otsu & Rid
        cv2.imshow('Cany', result4[i]) # Cany
        cv2.imshow('Sobel', result5[i]) # Sobel
        cv2.imshow('GaussianBlur', suave[i]) # GaussianBlur
        cv2.imshow('GrayScale', img[i]) # BGR2GRAY
        cv2.waitKey(0)

###############################################################################
# Print the simulation time
end = time.time()
print('Simulation time: ')
print(end - start)



    
    

        




    
       

