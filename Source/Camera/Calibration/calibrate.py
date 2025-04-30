import cv2
import numpy as np
import glob

def calibrate_camera(images, checkerboard=(6,9)):
    # Köşe bulma kriterleri
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
    
    # 3D noktalar
    objp = np.zeros((checkerboard[0] * checkerboard[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:checkerboard[1], 0:checkerboard[0]].T.reshape(-1, 2)
    
    objpoints = []  # 3D dünya noktaları
    imgpoints = []  # 2D görüntü düzlemi noktaları
    
    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # Köşeleri bul
        ret, corners = cv2.findChessboardCorners(gray, checkerboard, 
            flags=cv2.CALIB_CB_ADAPTIVE_THRESH + 
                   cv2.CALIB_CB_NORMALIZE_IMAGE + 
                   cv2.CALIB_CB_FAST_CHECK)
        
        if ret:
            # Köşeleri hassaslaştır
            corners2 = cv2.cornerSubPix(gray, corners, (11,11), (-1,-1), criteria)
            
            objpoints.append(objp)
            imgpoints.append(corners2)
            
            # Köşeleri çiz (görselleştirme)
            cv2.drawChessboardCorners(img, checkerboard, corners2, ret)
            cv2.imshow('Corners', img)
            cv2.waitKey(100)
    
    # Kamerayı kalibre et
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    mean_error = 0
    for i in range(len(objpoints)):
        imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        mean_error += error
 
    print( "total error: {}".format(mean_error/len(objpoints)) )
    return mtx, dist

# Kullanım
images = glob.glob('*.jpg')
mtx, dist = calibrate_camera(images)

# Düzeltme ve gösterme
for fname in images:
    img = cv2.imread(fname)
    undistorted = cv2.undistort(img, mtx, dist)
    
    # Yan yana göster
    combined = np.hstack((img, undistorted))
    cv2.imshow('Original vs Undistorted', combined)
    cv2.waitKey(0)

