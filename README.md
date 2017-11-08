# xs-face
Headcam video analysis

The face detections are located inside data/face_detections.csv. There is a row for every face detected in both the normal and inverted orientations (0 and 180 degrees, respectively, found in the angle column). If a face was not detected, the row will have is_face = FALSE. The w and h fields are width and height of the face, so we can do cool stuff with how close the face is to the child.
