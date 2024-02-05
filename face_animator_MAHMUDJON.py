# import cv2
# import numpy as np
# import mediapipe as mp
# import sys


# cap = cv2.VideoCapture('my_video.mp4')

# frame_rate = cap.get(cv2.CAP_PROP_FPS)


# image = cv2.imread('Imron.JPG')
# width = image.shape[1]
# height = image.shape[0]
# result1 = cv2.VideoWriter('output_1.mp4', cv2.VideoWriter_fourcc(
#     *'mp4v'), frame_rate, (width, height))

# # cap.set(3, width)
# # cap.set(4, height)

# mp_drawing = mp.solutions.drawing_utils
# mp_drawing_styles = mp.solutions.drawing_styles
# mp_face_mesh = mp.solutions.face_mesh


# def get_landmark_points(src_image):
#     with mp_face_mesh.FaceMesh(
#             static_image_mode=True,
#             max_num_faces=1,
#             refine_landmarks=True,
#             min_detection_confidence=0.5) as face_mesh:
#         results = face_mesh.process(cv2.cvtColor(src_image, cv2.COLOR_BGR2RGB))
#         if not results.multi_face_landmarks:
#             return None
#         if len(results.multi_face_landmarks) > 1:
#             sys.exit("There are too much face landmarks")

#         src_face_landmark = results.multi_face_landmarks[0].landmark
#         landmark_points = []
#         for i in range(468):
#             y = int(src_face_landmark[i].y * src_image.shape[0])
#             x = int(src_face_landmark[i].x * src_image.shape[1])
#             landmark_points.append((x, y))

#         return landmark_points


# def extract_index_nparray(nparray):
#     index = None
#     for num in nparray[0]:
#         index = num
#         break
#     return index


# def get_triangles(convexhull, landmarks_points, np_points):
#     rect = cv2.boundingRect(convexhull)
#     subdiv = cv2.Subdiv2D(rect)
#     subdiv.insert(landmarks_points)
#     triangles = subdiv.getTriangleList()
#     triangles = np.array(triangles, dtype=np.int32)

#     indexes_triangles = []
#     for t in triangles:
#         pt1 = (t[0], t[1])
#         pt2 = (t[2], t[3])
#         pt3 = (t[4], t[5])

#         index_pt1 = np.where((np_points == pt1).all(axis=1))
#         index_pt1 = extract_index_nparray(index_pt1)
#         index_pt2 = np.where((np_points == pt2).all(
#             axis=1))  # Corrected access to pt2
#         index_pt2 = extract_index_nparray(index_pt2)
#         index_pt3 = np.where((np_points == pt3).all(axis=1))
#         index_pt3 = extract_index_nparray(index_pt3)

#         if index_pt1 is not None and index_pt2 is not None and index_pt3 is not None:
#             triangle = [index_pt1, index_pt2, index_pt3]
#             indexes_triangles.append(triangle)

#     return indexes_triangles


# def triangulation(triangle_index, landmark_points, img=None):
#     tr1_pt1 = landmark_points[triangle_index[0]]
#     tr1_pt2 = landmark_points[triangle_index[1]]
#     tr1_pt3 = landmark_points[triangle_index[2]]
#     triangle = np.array([tr1_pt1, tr1_pt2, tr1_pt3], np.int32)

#     rect = cv2.boundingRect(triangle)
#     (x, y, w, h) = rect

#     cropped_triangle = None
#     if img is not None:
#         cropped_triangle = img[y: y + h, x: x + w]

#         cropped_triangle_mask = np.zeros((h, w), np.uint8)

#         points = np.array([[tr1_pt1[0] - x, tr1_pt1[1] - y],
#                            [tr1_pt2[0] - x, tr1_pt2[1] - y],
#                            [tr1_pt3[0] - x, tr1_pt3[1] - y]], np.int32)

#         cv2.fillConvexPoly(cropped_triangle_mask, points, 255)

#         return points, cropped_triangle, cropped_triangle_mask, rect


# def warp_triangle(rect, points1, points2, src_cropped_triangle, dest_cropped_triangle_mask):
#     (x, y, w, h) = rect
#     matrix = cv2.getAffineTransform(np.float32(points1), np.float32(points2))
#     warped_triangle = cv2.warpAffine(src_cropped_triangle, matrix, (w, h))

#     # cv2.imshow("warped_triangle", warped_triangle)
#     # cv2.imshow("warped_triangle", warped_triangle)
#     # cv2.waitKey(0)

#     warped_triangle = cv2.bitwise_and(
#         warped_triangle, warped_triangle, mask=dest_cropped_triangle_mask)
#     return warped_triangle


# def add_piece_of_new_face(new_face, rect, warped_triangle, mask_triangles_designed):
#     (x, y, w, h) = rect
#     new_face_rect_area = new_face[y: y + h, x: x + w]
#     new_face_rect_area_gray = cv2.cvtColor(
#         new_face_rect_area, cv2.COLOR_BGR2GRAY)

#     _, mask_triangles_designed = cv2.threshold(
#         new_face_rect_area_gray, 1, 255, cv2.THRESH_BINARY_INV)

#     if mask_triangles_designed.shape != warped_triangle.shape[:2]:
#         mask_triangles_designed = cv2.resize(
#             mask_triangles_designed, (warped_triangle.shape[1], warped_triangle.shape[0]))

#     warped_triangle = cv2.bitwise_and(
#         warped_triangle, warped_triangle, mask=mask_triangles_designed)

#     new_face_rect_area = cv2.add(new_face_rect_area, warped_triangle)
#     new_face[y: y + h, x: x + w] = new_face_rect_area



# def swap_new_face(dest_image, dest_image_gray, head_mask, center_face, result, dest_convexHull):
#     try:
#         if dest_image.shape != result.shape:
#             raise ValueError(
#                 "Shapes of destination image and result image must match")

#         if head_mask.dtype != np.uint8:
#             head_mask = head_mask.astype(np.uint8)

#         if center_face[0] < 0 or center_face[0] >= dest_image.shape[1] or \
#            center_face[1] < 0 or center_face[1] >= dest_image.shape[0]:
#             raise ValueError("Center coordinates are out of bounds")

#         # Ensure the images and masks are in the correct format and dimensions
#         print("Shapes: dest_image={}, result={}, head_mask={}".format(
#             dest_image.shape, result.shape, head_mask.shape))
#         print("Types: dest_image={}, result={}, head_mask={}".format(
#             dest_image.dtype, result.dtype, head_mask.dtype))

#         return cv2.seamlessClone(result, dest_image, head_mask, center_face, cv2.MIXED_CLONE)
#     except Exception as e:
#         print("Error in swap_new_face:", e)
#         return None


# def set_src_image(image):
#     global src_image, src_image_gray, src_mask, src_landmark_points, src_np_points, src_convexHull, indexes_triangles
#     src_image = image
#     src_image_gray = cv2.cvtColor(src_image, cv2.COLOR_BGR2GRAY)
#     src_mask = np.zeros_like(src_image_gray)

#     # cv2.imshow("src_image", src_image)
#     # cv2.waitKey(0)

#     src_landmark_points = get_landmark_points(src_image)

#     # print("src_landmark_points", src_landmark_points)
#     src_np_points = np.array(src_landmark_points)
#     src_convexHull = cv2.convexHull(src_np_points)
#     cv2.fillConvexPoly(src_mask, src_convexHull, 255)

#     indexes_triangles = get_triangles(convexhull=src_convexHull,
#                                       landmarks_points=src_landmark_points,
#                                       np_points=src_np_points)

#     # print("indexes_triangles", indexes_triangles)


# set_src_image(image)

# while True:
#     global src_image, src_image_gray, src_mask, src_landmark_points, src_np_points, src_convexHull, indexes_triangles

#     ret, dest_image = cap.read()
#     # dest_image = cv2.resize(dest_image, (width, height))

#     # cv2.imshow("dest_image", dest_image)
#     # cv2.waitKey(0)

#     if not ret:
#         break

#     dest_image_gray = cv2.cvtColor(dest_image, cv2.COLOR_BGR2GRAY)
#     dest_mask = np.zeros_like(dest_image_gray)

#     dest_landmark_points = get_landmark_points(dest_image)
#     # print(dest_landmark_points)
#     if dest_landmark_points is None:
#         continue
#     dest_np_points = np.array(dest_landmark_points)
#     dest_convexHull = cv2.convexHull(dest_np_points)

#     height, width, channels = src_image.shape
#     new_face = np.zeros((height, width, channels), np.uint8)

#     for triangle_index in indexes_triangles:
#         # print("inside of loop")

#         points, src_cropped_triangle, cropped_triangle_mask, _ = triangulation(
#             triangle_index=triangle_index,
#             landmark_points=src_landmark_points,
#             img=src_image)

#         points2, _, dest_cropped_triangle_mask, rect = triangulation(triangle_index=triangle_index,
#                                                                      landmark_points=dest_landmark_points, img=dest_image)

#         warped_triangle = warp_triangle(rect=rect, points1=points, points2=points2,
#                                         src_cropped_triangle=src_cropped_triangle,
#                                         dest_cropped_triangle_mask=dest_cropped_triangle_mask)

#         # cv2.imshow("warped_triangle", warped_triangle)
#         # cv2.waitKey(0)

#         add_piece_of_new_face(new_face=new_face, rect=rect, warped_triangle=warped_triangle,mask_triangles_designed=None)
#     # result = swap_new_face(dest_image=dest_image, dest_image_gray=dest_image_gray,
#     #                        dest_convexHull=src_convexHull, head_mask= dest_mask, result=new_face, center_face=new_face)

#     # result = cv2.medianBlur(result, 3)
#     # h, w, _ = src_image.shape
#     # rate = width / w

#     # cv2.imshow("Source image", cv2.resize(src_image, (int(w * rate), int(h * rate))))
#     # cv2.imshow("New face", new_face)
#     result1.write(new_face)
#     # cv2.imshow("Result", result)
#     k = cv2.waitKey(0)
#     if k == ord('q'):
#         break
#     cv2.destroyAllWindows()

# result1.release()
