# import cv2
# import numpy as np
#
# def draw_landmarks(image, landmarks):
#     for point in landmarks:
#         cv2.circle(image, tuple(point), 3, (0, 0, 255), -1)
#     return image
#
# def draw_delaunay_blank(image_shape, subdiv):
#     blank_canvas = np.zeros(image_shape, dtype=np.uint8)
#     triangle_list = subdiv.getTriangleList()
#     for t in triangle_list:
#         pt1 = (int(t[0]), int(t[1]))
#         pt2 = (int(t[2]), int(t[3]))
#         pt3 = (int(t[4]), int(t[5]))
#
#         cv2.line(blank_canvas, pt1, pt2, (0, 255, 0), 1)
#         cv2.line(blank_canvas, pt2, pt3, (0, 255, 0), 1)
#         cv2.line(blank_canvas, pt3, pt1, (0, 255, 0), 1)
#     return blank_canvas
#
# def animate_expression(landmarks, expression='laugh', num_frames=5):
#     """Generate animated landmarks based on a given expression."""
#     animated_landmarks = [landmarks]
#
#     if expression == 'laugh':
#         # Landmark points
#         upper_lip_landmarks = list(range(50, 54))
#         lower_lip_landmarks = list(range(56, 60))
#         cheek_raise_landmarks = [28, 29]
#         outer_mouth_landmarks = [48, 54]
#         chin_landmark = [57]
#         eyebrows_landmarks = list(range(17, 27))
#         upper_eyelid_landmarks = list(range(37, 42)) + list(range(43, 48))
#
#         for i in range(20):
#             factor = (1 - abs(2 * i / num_frames - 1))
#             new_landmarks = animated_landmarks[-1].copy()
#
#             # Minor eyebrow adjustment
#             for idx in eyebrows_landmarks:
#                 new_landmarks[idx][1] -= 1 * factor  # slight upward movement
#
#             # Upper eyelid adjustment
#             for idx in upper_eyelid_landmarks:
#                 new_landmarks[idx][1] -= 1 * factor  # slight upward movement
#
#             # Upper lip adjustment
#             for idx in upper_lip_landmarks:
#                 new_landmarks[idx][1] -= 2 * factor  # more upward movement
#
#             # Lower lip adjustment
#             for idx in lower_lip_landmarks:
#                 new_landmarks[idx][1] += 2 * factor  # more downward movement
#
#             # Raise the cheeks
#             for idx in cheek_raise_landmarks:
#                 new_landmarks[idx][1] -= 2 * factor  # upward movement
#
#             # Widen the mouth, with constraints
#             for idx in outer_mouth_landmarks:
#                 movement = (-2 if idx == 48 else 2) * factor
#                 new_x = new_landmarks[idx][0] + movement
#                 if 0 <= new_x < image.shape[1]:  # ensure we don't move out of image bounds
#                     new_landmarks[idx][0] += movement
#
#             # Minor chin movement
#             for idx in chin_landmark:
#                 new_landmarks[idx][1] += 1 * factor  # slight downward movement
#
#             animated_landmarks.append(new_landmarks)
#
#     return animated_landmarks
#
#
#
#
#
#
#
#
#
# def warp_image(img, landmarks1, landmarks2):
#     # Create an empty image to store the morphed face
#     morphed_img = np.zeros_like(img)
#
#
#     # Get Delaunay triangles using original landmarks
#     rect = (0, 0, img.shape[1], img.shape[0])
#     subdiv = cv2.Subdiv2D(rect)
#     for landmark in landmarks1:
#         subdiv.insert(tuple(landmark.astype(np.float32)))
#
#     triangle_list = subdiv.getTriangleList()
#
#     # Warp each triangle
#     for t in triangle_list:
#         # Get vertices of triangle in the two images
#         tri1 = [landmarks1[np.where((landmarks1 == (t[0], t[1])).all(axis=1))[0][0]],
#                 landmarks1[np.where((landmarks1 == (t[2], t[3])).all(axis=1))[0][0]],
#                 landmarks1[np.where((landmarks1 == (t[4], t[5])).all(axis=1))[0][0]]]
#
#         tri2 = [landmarks2[np.where((landmarks1 == (t[0], t[1])).all(axis=1))[0][0]],
#                 landmarks2[np.where((landmarks1 == (t[2], t[3])).all(axis=1))[0][0]],
#                 landmarks2[np.where((landmarks1 == (t[4], t[5])).all(axis=1))[0][0]]]
#
#         # Affine warp triangle from img using tri1 and tri2
#         warp_mat = cv2.getAffineTransform(np.float32(tri1), np.float32(tri2))
#         warped_triangle = cv2.warpAffine(img, warp_mat, (img.shape[1], img.shape[0]))
#
#         # Mask the warped triangle and overlay onto morphed_img
#         mask = np.zeros_like(img)
#
#
#         cv2.fillConvexPoly(mask, np.int32(tri2), (1, 1, 1), 16, 0)
#         morphed_img += warped_triangle * mask
#
#
#
#     return morphed_img
#
# if __name__ == "__main__":
#     image_path = "Imron.JPG"
#     image = cv2.imread(image_path)
#
#     face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
#     landmark_detector = cv2.face.createFacemarkLBF()
#     landmark_detector.loadModel("lbfmodel.yaml")
#
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     faces = face_detector.detectMultiScale(gray)
#
#     for face in faces:
#         _, landmarks = landmark_detector.fit(gray, np.array([face]))
#         landmarks = landmarks[0][0]
#
#         image_with_landmarks = draw_landmarks(image.copy(), landmarks.astype(np.int32))
#         cv2.imshow("Landmarks", image_with_landmarks)
#         cv2.waitKey(0)
#
#         # Animate the landmarks
#         #mean_landmarks = np.mean(all_landmarks, axis=0)
#         animated_landmarks = animate_expression(landmarks, expression='laugh', num_frames=5)
#
#         """for landmark_frame in animated_landmarks:
#             rect = (0, 0, image.shape[1], image.shape[0])
#             subdiv = cv2.Subdiv2D(rect)
#             for landmark in landmark_frame:
#                 subdiv.insert(tuple(landmark.astype(np.float32)))
#             image_with_triangles = draw_delaunay(image.copy(), subdiv)
#
#             cv2.imshow("Animated Face", image_with_triangles)
#             cv2.waitKey(50)"""
#
#         for landmark_frame in animated_landmarks:
#             morphed_image = warp_image(image, landmarks, landmark_frame)
#
#             # Generate triangulated image without warping
#             rect = (0, 0, image.shape[1], image.shape[0])
#             subdiv = cv2.Subdiv2D(rect)
#             for landmark in landmark_frame:
#                     subdiv.insert(tuple(landmark.astype(np.float32)))
#             triangulated_image = draw_delaunay_blank(image.shape, subdiv)
#
#             # Combine the two images horizontally and show them
#             combined_image = np.hstack((morphed_image, triangulated_image))
#             cv2.imshow("Morphed Face and Triangles", combined_image)
#             cv2.waitKey(5)
#
#     cv2.destroyAllWindows()
