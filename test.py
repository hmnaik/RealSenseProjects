## License: Apache 2.0. See LICENSE file in root directory.
## Copyright(c) 2015-2017 Intel Corporation. All Rights Reserved.

#####################################################
## librealsense tutorial #1 - Accessing depth data ##
#####################################################

# First import the library
import pyrealsense2 as rs
import cv2 as cv
import numpy as np

outputVideo = cv.VideoWriter('05252018\\testColor_device1_pg_scene1_pt5.mp4',0x00000020, 30.0, (1280,720), True)
outputDepth = cv.VideoWriter('05252018\\testDepth_device1_pg_scene1_pt5.mp4',0x00000020, 30.0, (1280,720), True)

windowName = 'combinedImages'
cv.namedWindow(windowName,cv.WINDOW_NORMAL)

record = False
#alignedWindowName = 'alignedWindow'
#cv.namedWindow(alignedWindowName,cv.WINDOW_NORMAL)

try:
    # Create a context object. This object owns the handles to all connected realsense devices
    pipeline = rs.pipeline()

    # Create a config and configure the pipeline to stream
    #  different resolutions of color and depth streams
    config = rs.config()
    config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

    # Starting to stream data
    pipeline.start(config)

    align_to = rs.stream.color
    align = rs.align(align_to)

    while True:
        # This call waits until a new coherent set of frames is available on a device
        # Calls to get_frame_data(...) and get_frame_timestamp(...) on a device will return stable values until wait_for_frames(...) is called
        frames = pipeline.wait_for_frames()

        #Get aligned Frames i.e. Pixel to Depth mapping is done.
        aligned_frames = align.process(frames)
        aligned_depth = aligned_frames.get_depth_frame();
        aligned_color = aligned_frames.get_color_frame();

        if not aligned_depth or not aligned_color:
            continue

        # Conver the image to ocv readable array format
        depth_img = np.asanyarray(aligned_depth.get_data())
        color_img = np.asanyarray(aligned_color.get_data())

        depth_img_3d = np.dstack((depth_img,depth_img,depth_img))
        depth_img_colormap = cv.applyColorMap(cv.convertScaleAbs(depth_img, alpha=0.03), cv.COLORMAP_JET)
        combinedImages = np.hstack((color_img, depth_img_colormap))

        if record:
            cv.circle(combinedImages, (20,20), 5 , (0,0,255), -1 )
            outputVideo.write(color_img)
            outputDepth.write(depth_img_colormap)

        # Show the combined image
        cv.imshow(windowName, combinedImages)

        key = cv.waitKey(1)
        if key == ord('q'):
            outputVideo.release()
            outputDepth.release()
            cv.destroyAllWindows()
            break

        if key == ord('r'):
            record = not record


except Exception as e:
    print(e)
    pass

finally:
    pipeline.stop()