from PIL import Image
import numpy as np
import face_recognition
from imagekit.processors import ResizeToFit


class DetectFaceAndResizeToFit(ResizeToFit):


    def process(self,img):
        # find face and crop
        im = np.array(img)

        # crop to face
        locations = face_recognition.face_locations(im)
        if len(locations)>0:
            lo = locations[0]
            width =lo[2]-lo[0]
            height = lo[1]-lo[3]
            padding = [ 
                        int(0.2*width),
                        int(0.2*width),
                        int(0.7*height),
                        int(0.2*height),
                        ]
            pos = (lo[3]- padding[0],lo[0]-padding[2])
            height = int (height+ padding[2]+ padding[3])
            width = int (width+  padding[0] +padding[1])

            im = im[max(0,pos[1]):min(im.shape[0]-1,(pos[1]+height)),max(0,pos[0]):min(im.shape[1]-1,(pos[0]+width))]

        im = Image.fromarray(im)
        return super().process(im)


