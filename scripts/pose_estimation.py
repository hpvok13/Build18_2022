import numpy as np
import cv2
import time
import os
import argparse

class PoseEstimator:
    def __init__(self, mode='mpi'):
        # Specify the paths for the 2 files
        if mode == 'coco':
            self.proto_file = "../models/pose/coco/pose_deploy_linevec.prototxt"
            self.weights_file = "../models/pose/coco/pose_iter_440000.caffemodel"
            self.n_points = 18
            self.pose_pairs = [ [1,0],[1,2],[1,5],[2,3],[3,4],[5,6],[6,7],[1,8],[8,9],[9,10],[1,11],[11,12],[12,13],[0,14],[0,15],[14,16],[15,17]]
        elif mode == 'mpi' :
            self.proto_file = "../models/pose/mpi/pose_deploy_linevec_faster_4_stages.prototxt"
            self.weights_file = "../models/pose/mpi/pose_iter_160000.caffemodel"
            self.n_points = 15
            self.pose_pairs = [[0,1], [1,2], [2,3], [3,4], [1,5], [5,6], [6,7], [1,14], [14,8], [8,9], [9,10], [14,11], [11,12], [12,13] ]
        else:
            raise Exception('PoseEstimator mode not "coco" or "mpi"')
        
        # Read the network into Memory
        self.net = cv2.dnn.readNetFromCaffe(self.proto_file, self.weights_file)

    def estimate(self, frame, threshold=0.1):
        frame_height, frame_width = frame.shape[:2]
        # Specify the input image dimensions
        in_width = 368
        in_height = 368
        
        # Prepare the frame to be fed to the network
        inp_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (in_width, in_height), (0, 0, 0), swapRB=False, crop=False)
        
        # Set the prepared object as the input blob of the network
        self.net.setInput(inp_blob)

        out = self.net.forward()

        H = out.shape[2]
        W = out.shape[3]

        # assert out.shape[1] == self.nPoints
        # Empty list to store the detected keypoints
        points = []
        for i in range(self.n_points):
            # confidence map of corresponding body's part.
            prob_map = out[0, i, :, :]
        
            # Find global maxima of the probMap.
            min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)
        
            # Scale the point to fit on the original image
            x = (frame_width * point[0]) / W
            y = (frame_height * point[1]) / H
        
            if prob > threshold :
                # Add the point to the list if the probability is greater than the threshold
                assert x >= 0 and y >= 0
                points.append((int(x), int(y)))
            else :
                points.append((-1, -1))

        return np.array(points)

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('vid_path', help='Video File Path for Pose Tracking', nargs='*')

    args = parser.parse_args()

    if len(args.vid_path) == 0:
        # Webcam Capture
        cap = cv2.VideoCapture(0)
        rotate_code = None
        output_path = '../output/webcam.mp4'
    else:
        # Video File Capture
        cap = cv2.VideoCapture(args.vid_path[0])
        rotate_code = cv2.ROTATE_180
        output_path = '../output/' + os.path.splitext(os.path.split(args.vid_path[0])[1])[0] + '_pose.mp4'
    
    if not cap.isOpened():
        raise Exception("VideoCapture object cannot be opened")

    frame_width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))   # float `width`
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # float `height`
    fps = cap.get(cv2.CAP_PROP_FPS)
    assert fps > 10
    
    vid_writer = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (frame_width, frame_height))

    pose = PoseEstimator(mode='mpi')
    
    while True:
        t = time.time()
        ret, frame = cap.read()
        # if frame is read correctly ret is True
        if not ret:
            print("Can't receive frame (stream end?). Exiting ...")
            break

        if rotate_code is not None:
            frame = cv2.rotate(frame, rotate_code) 

        points = pose.estimate(frame)

        # Draw Skeleton
        for pair in pose.pose_pairs:
            partA = pair[0]
            partB = pair[1]

            if (points[partA,:] >= 0).all() and (points[partB,:] >= 0).all():
                cv2.line(frame, points[partA,:], points[partB,:], (0, 255, 255), 3, lineType=cv2.LINE_AA)
                cv2.circle(frame, points[partA,:], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
                cv2.circle(frame, points[partB,:], 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
        
        # for i, point in enumerate(points):
        #     # cv2.circle(frame, point, 8, (0, 0, 255), thickness=-1, lineType=cv2.FILLED)
        #     cv2.putText(frame, str(i), point, cv2.FONT_HERSHEY_COMPLEX, .5, (0, 0, 255), 1, lineType=cv2.LINE_AA)

        cv2.putText(frame, "time taken = {:.2f} sec".format(time.time() - t), (50, 50), cv2.FONT_HERSHEY_COMPLEX, .8, (255, 50, 0), 2, lineType=cv2.LINE_AA)
        
        vid_writer.write(frame)

        cv2.imshow('Output Pose', frame)
        if cv2.waitKey(1) == ord('q'):
            break

    vid_writer.release()

if __name__ == '__main__':
    main()
