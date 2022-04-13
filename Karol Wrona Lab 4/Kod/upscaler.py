import cv2
import imageio
 

def main(dirPath):
    print(dirPath)

    for i in range(127):
        filePath = dirPath + "/" + str(i) +".png"
        print(filePath)
        img = cv2.imread(filePath, cv2.IMREAD_UNCHANGED)
        
        scale_percent = 1000 # percent of original size
        width = int(img.shape[1] * scale_percent / 100)
        height = int(img.shape[0] * scale_percent / 100)
        dim = (width, height)
        
        # resize image
        resized = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

        cv2.imwrite(filePath, resized)

    gifName = dirPath+"/"+"animation"+".gif"
    print(gifName)
    with imageio.get_writer(gifName, mode='I') as writer:
        for i in range(127):
            filePath = dirPath + "/" + str(i) +".png"
            image = imageio.imread(filePath)
            writer.append_data(image)