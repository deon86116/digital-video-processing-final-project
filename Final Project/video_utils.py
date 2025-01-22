import os, cv2
import numpy as np

def frame_extraction_with_fps(video):
    vid = cv2.VideoCapture(video)
    success, image = vid.read()
    count = 0
    file_name  = os.path.basename(os.path.splitext(video)[0])
    image_name = "./%s/%s.jpeg" % (file_name,str(count).zfill(6))
    
    if not os.path.isdir("./" + file_name):
        os.mkdir("./" + file_name)
    
    while success:
        cv2.imwrite(image_name, image)
        success, image = vid.read()
        count += 2
        
    return vid.get(cv2.CAP_PROP_FPS) #Return frame rate of the video
    
def image_pad(image, h, w):
    pad_h = h//2, h//2 if h%2 == 0 else h//2 + 1
    pad_w = w//2, w//2 if w%2 == 0 else w//2 + 1
    
    #np.pad(images, ((0,0), (top, bottom), (left, right), (0,0))
    return np.pad(image, ((0,0), pad_h, pad_w, (0,0)), 'constant')
        
def frame_interpolation(image, model, batch=16, predh=128, predw=128):
    pad_h = 0
    pad_w = 0
    
    if(image.shape[1] % predh != 0): #Code has % predw, check if thats correct
        pad_h = int((1-(image.shape[1]/predh - image.shape[1]//predh))*predh)
                
    if(image.shape[2] % predw != 0): 
        pad_w = int((1-(image.shape[2]/predw - image.shape[1]//predw))*predw)
        
    image = image_pad(image, int(pad_h), int(pad_w))
    image_interpolated = np.zeros((1,image.shape[1],image.shape[2],3))
    image = image/255.
    
    for row in range(image.shape[1]//predh):
        for col in range(image.shape[2]//predw):
            prediction = model.predict(image[:,row*predh:row*predh+predh,col*predw:col*predw+predw,:], batch_size=batch, use_multiprocessing=True)
            image_interpolated[:,row*predh:row*predh+predh,col*predw:col*predw+predw,:] = prediction
    
    return image_interpolated
    

def generate_frames(frames_filepath, model, batch, video):
    batches = []
    batch_size = 0
    file_name  = os.path.basename(os.path.splitext(video)[0])
    count = 1
    frames_filepath = sorted(frames_filepath) #Unsure if this line is needed
    
    for i in range(len(frames_filepath) - 1):
        first_image_filepath = video[i]
        first_image = cv2.imread(first_image_filepath)
        second_image_filepath = video[i + 1]
        second_image = cv2.imread(second_image_filepath)
        
        image = np.concatenate([first_image, second_image], axis=-1)
        image = np.expand_dims(image, axis=0)
        height = image.shape[1]
        width = image.shape[2]
        
        if(batch_size < batch - 1):
            batch_size += 1
            if(type(batches) == list):
                batches = image
            else:
                batches = np.concatenate([batches, image], axis = 0)
            continue
        else:
            batch_size += 1
            if(type(batches) == list):
                batches = image
            else:
                batches = np.concatenate([image],axis = 0) if type(batches)==list else np.concatenate([batches,image])
            images_interpolated = frame_interpolation(batches, model, batch)
            
            for j in range(batch):
                image_name = "./%s/%s.jpeg" % (file_name,str(count).zfill(6))
                cv2.imwrite(image_name, images_interpolated[j,:,:,:]*255.)
                cut_extra_padding(image_name, height, width)
                count += 2
            
            batch_size = 0
            batches = []
            
        
def cut_extra_padding(frame_filepath, height, width):
    image = cv2.imread(frame_filepath)
    image = image[int((image.shape[0]-height)/2):height+int((image.shape[0]-height)/2),int((image.shape[1]-width)/2):width+int((image.shape[1]-width)/2),:]
    cv2.imwrite(frame_filepath, image)

def generate_video(frames_filepath, outPath, fps):
    frames = []
    frames_filepath = sorted(frames_filepath) #Unsure if this line is needed
    
    for i in range(len(frames_filepath)):
        image = cv2.imread(frames_filepath[i])
        size = (image.shape[0], image.shape[1]) #This may be incorrect
        frames.append(image)
        
    video = cv2.VideoWriter(outPath, cv2.VideoWriter_fourcc(*'DIVX'), fps, size)
    for i in range(len(frames)):
        video.write(frames[i])
    
    video.release()
