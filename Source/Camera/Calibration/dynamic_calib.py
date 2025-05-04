import cv2
import numpy as np
import glob

width=1920
height=1080

cam_left_idx=4
cam_right_idx=6

#1= manual 0=auto
auto_exposure=1

scale_coefficient=2

cam_left=cv2.VideoCapture(cam_left_idx)
cam_right=cv2.VideoCapture(cam_right_idx)

cam_left.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('G', 'R', 'E', 'Y'))
cam_right.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('G', 'R', 'E', 'Y'))

cam_left.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam_left.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cam_right.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cam_right.set(cv2.CAP_PROP_FRAME_HEIGHT, height)

cam_left.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)
cam_right.set(cv2.CAP_PROP_AUTO_EXPOSURE, auto_exposure)

cam_left.set(cv2.CAP_PROP_EXPOSURE,  75)
cam_right.set(cv2.CAP_PROP_EXPOSURE, 75)

cam_left.set(cv2.CAP_PROP_GAIN, 0)
cam_right.set(cv2.CAP_PROP_GAIN, 0)




# Calibration parameters

CHECKERBOARD=(6,9)
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# Kare boyutu (isteğe bağlı, gerçek dünya birimi cinsinden, örneğin mm)
# Bu, dışsal parametrelerin (rotasyon, translasyon) ölçeğini belirler.
# Eğer sadece içsel parametrelerle ilgileniyorsanız, 1.0 olarak bırakabilirsiniz.
SQUARE_SIZE = 1.0

# 3D noktalar
left_objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
left_objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
left_objp = left_objp * SQUARE_SIZE # Kare boyutuna göre ölçekle

right_objp = np.zeros((CHECKERBOARD[0] * CHECKERBOARD[1], 3), np.float32)
right_objp[:, :2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)
right_objp = right_objp * SQUARE_SIZE # Kare boyutuna göre ölçekle

left_objpoints = []  # 3D dünya noktaları
right_objpoints = []  # 3D dünya noktaları

left_imgpoints = []  # 2D görüntü düzlemi noktaları
right_imgpoints = []  # 2D görüntü düzlemi noktaları

def calibrate_camera(left_frame,right_frame):
    left_ret, left_corners = cv2.findChessboardCorners(left_frame, CHECKERBOARD, 
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH + 
                   cv2.CALIB_CB_NORMALIZE_IMAGE + 
                   cv2.CALIB_CB_FAST_CHECK)

    right_ret, right_corners = cv2.findChessboardCorners(right_frame, CHECKERBOARD,
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH + 
                   cv2.CALIB_CB_NORMALIZE_IMAGE + 
                   cv2.CALIB_CB_FAST_CHECK)
    if left_ret and right_ret:
        # Save images with date
        cv2.imwrite(f'left_{len(left_imgpoints)}.jpg', left_frame)
        cv2.imwrite(f'right_{len(right_imgpoints)}.jpg', right_frame)

        left_objpoints.append(left_objp)
        right_objpoints.append(right_objp)

        # Refine the corners
        left_corners2 = cv2.cornerSubPix(left_frame, left_corners, (11, 11), (-1, -1), criteria)
        right_corners2 = cv2.cornerSubPix(right_frame, right_corners, (11, 11), (-1, -1), criteria)

        left_imgpoints.append(left_corners2)
        right_imgpoints.append(right_corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(left_frame, CHECKERBOARD, left_corners2, left_ret)
        cv2.drawChessboardCorners(right_frame, CHECKERBOARD, right_corners2, right_ret)

        cv2.imshow('Left Frame', left_frame)
        cv2.imshow('Right Frame', right_frame)
        cv2.waitKey(500)
        cv2.destroyWindow('Left Frame')
        cv2.destroyWindow('Right Frame')
        print("Corners found and added to the list.")

        
    else:
        print("Corners not found in one or both frames.")



def calculate_and_save_camera_parameters(image_size):
    # Kalibrasyon verilerini kontrol et
    if len(left_imgpoints) == 0 or len(right_imgpoints) == 0:
        print("Not enough calibration images.")
        return

    # Tekil kamera kalibrasyonu
    ret_left, mtx_left, dist_left, rvecs_left, tvecs_left = cv2.calibrateCamera(left_objpoints, left_imgpoints, image_size, None, None)
    ret_right, mtx_right, dist_right, rvecs_right, tvecs_right = cv2.calibrateCamera(right_objpoints, right_imgpoints, image_size, None, None)

    print("Left Calibration RMS error:", ret_left)
    print("Right Calibration RMS error:", ret_right)

    # Stereo kalibrasyon
    flags = cv2.CALIB_FIX_INTRINSIC
    retval, mtx_left, dist_left, mtx_right, dist_right, R, T, E, F = cv2.stereoCalibrate(
        objectPoints=left_objpoints,
        imagePoints1=left_imgpoints,
        imagePoints2=right_imgpoints,
        cameraMatrix1=mtx_left,
        distCoeffs1=dist_left,
        cameraMatrix2=mtx_right,
        distCoeffs2=dist_right,
        imageSize=image_size,
        criteria=criteria,
        flags=flags
    )

    print("Stereo Calibration RMS error:", retval)

    # Kayıt
    np.savez('stereo_calib.npz', 
             mtx_left=mtx_left,
             dist_left=dist_left,
             mtx_right=mtx_right,
             dist_right=dist_right,
             R=R,
             T=T,
             E=E,
             F=F)
    print("Camera parameters saved.")

    

while True:
    cam_left.grab()
    cam_right.grab()

    
    ret_left, frame_left = cam_left.retrieve()
    ret_right, frame_right = cam_right.retrieve()

    if not ret_left or not ret_right:
        print("Failed to grab frames")
        break

    # Convert to grayscale
    gray_left = cv2.cvtColor(frame_left, cv2.COLOR_BGR2GRAY)
    gray_right = cv2.cvtColor(frame_right, cv2.COLOR_BGR2GRAY)

    # Scale the images to 1/4 of their original size
    scale_left = cv2.resize(gray_left, (width // scale_coefficient, height // scale_coefficient))
    scale_right = cv2.resize(gray_right, (width // scale_coefficient, height // scale_coefficient))
        
    # Concatenate the images horizontally
    combined = np.hstack((scale_left, scale_right))

    # Display the combined image
    cv2.imshow('Combined', combined)
    # Wait for a key press
    key = cv2.waitKey(1)
    if key == 27:  # ESC key
        break
    # If key is c capture frame and cal calibrate_camera
    elif key == ord('c'):
        calibrate_camera(gray_left, gray_right)
    # Finish calibration
    elif key == ord('z'):
        calculate_and_save_camera_parameters(gray_left.shape[::-1])
        
    
    
# Release the cameras and close all OpenCV windows
cam_left.release()
cam_right.release()
cv2.destroyAllWindows()
# Terminate the program
print("Program terminated.")





