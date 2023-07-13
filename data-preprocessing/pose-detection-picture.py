import cv2
import mediapipe as mp


class poseDetector():
    
    def __init__(self,mode=False,modComplex=1,smooth_land=True,enable_Seg=False,smooth_seg=True,detectionCon=0.9,trackCon=0.9):
        self.mode=mode
        self.smooth_land=smooth_land
        self.enable_Seg=enable_Seg
        self.smooth_seg=smooth_seg
        self.detectionCon=detectionCon
        self.trackCon=trackCon
        self.modComplex=modComplex
        
        
        self.mpDraw=mp.solutions.drawing_utils
        self.mpPose=mp.solutions.pose
        self.pose=self.mpPose.Pose(self.mode,self.smooth_land,self.enable_Seg,self.smooth_seg, self.detectionCon,self.trackCon)
        
        
    def findPose(self,img,draw=True):
        imgRGB= cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
        self.results=self.pose.process(imgRGB)
        
        if self.results.pose_landmarks:
            if draw:
                self.mpDraw.draw_landmarks(img,self.results.pose_landmarks,self.mpPose.POSE_CONNECTIONS)
            
        return img 
    
    def boxAroundPart(self,img,part,draw=True):
        if self.results.pose_landmarks:
            leg=[25,27,29,31]
            # bounding box around the leg ladmarks
            xList=[]
            yList=[]
            for id,lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                cx,cy= (int)(lm.x * w) ,(int)(lm.y*h)
                if id in leg:
                    xList.append(cx)
                    yList.append(cy)
                if draw:
                    cv2.circle(img,(cx,cy),3,(255,0,0),cv2.FILLED)
            xmin,xmax=min(xList),max(xList)
            ymin,ymax=min(yList),max(yList)
            if draw:
                cv2.rectangle(img,(xmin-20,ymin-20),(xmax+20,ymax+20),(0,0,255),2)
                
            box=img[ymin-20:ymax+20,xmin-20:xmax+20]
                
        return box
    
    
    
    def findPosition(self, img, draw=True):
        
        lmlist=[]
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h,w,c=img.shape
                cx,cy= (int)(lm.x * w) ,(int)(lm.y*h)
                lmlist.append((id,cx,cy))
                if draw:
                    cv2.circle(img,(cx,cy),3,(255,0,0),cv2.FILLED)
                    
        return lmlist
            

 
def main():
    file_path="data-preprocessing/test.jpg"
    img=cv2.imread(file_path)
    detector=poseDetector()
    
        
    img=detector.findPose(img,draw=True)
    
    lmlist=detector.findPosition(img,draw=True)
    if(len(lmlist)!=0):
        cv2.circle(img,(lmlist[0][1],lmlist[0][2]),1,(255,0,0),cv2.FILLED)
    box=detector.boxAroundPart(img,0,draw=True)

    cv2.imshow("Image",img)    
    cv2.imshow("box",box)    
    cv2.waitKey(5000)
    
    
    
    
    
if __name__ == "__main__":
    main()
    
    