import face_recognition
import cv2 as cv


class facePose():
    def __init__(self, image_path):
        self.img = cv.imread(image_path)
        # 脸部关节点
        self.face_pose = {}
        self.get_hairline()
        self.get_face_locations()
        self.get_face_front()

    def get_hairline(self):
        # 发际线位置判定
        landmarks = face_recognition.face_landmarks(self.img, num_landmarks=81)[0]
        self.face_pose['forehead'] = landmarks['forehead'][3]
        # 左右太阳穴
        self.face_pose['temple_left'] = landmarks['forehead'][7]
        self.face_pose['temple_right'] = landmarks['forehead'][6]

    def get_face_locations(self):
        """
        脸部位置
        :return: face_location
        """
        face_location = {}
        face_locations = face_recognition.face_locations(self.img)
        top, right, bottom, left = face_locations[0]
        face_location['top'] = top
        face_location['right'] = right
        face_location['bottom'] = bottom
        face_location['left'] = left
        self.face_pose['face_location'] = face_location

    def get_face_front(self):
        """
        颧骨 下巴 眼角 眼尾 腮部转折点
        :return: 脸部正面关键点判定
        """
        landFeature = face_recognition.face_landmarks(cv.cvtColor(self.img, cv.COLOR_BGR2RGB), num_landmarks=68)[0]
        # 左右颧骨
        self.face_pose['cheekbone_left'] = landFeature['chin'][1]
        self.face_pose['cheekbone_right'] = landFeature['chin'][-2]

        # 下巴中心点
        self.face_pose['chin_center'] = landFeature['chin'][8]
        # 判断下巴类型的五个点
        self.face_pose['jaw'] = landFeature['chin'][6:11]

        # 左右眼角
        self.face_pose['corner_of_eye_left'] = landFeature['left_eye'][3]
        self.face_pose['corner_of_eye_right'] = landFeature['right_eye'][0]

        # 左右眼尾
        self.face_pose['outer_corner_of_eye_left'] = landFeature['left_eye'][0]
        self.face_pose['outer_corner_of_eye_right'] = landFeature['right_eye'][3]

        # 左右腮部转折点
        self.face_pose['cheek_left'] = landFeature['chin'][4]
        self.face_pose['cheek_right'] = landFeature['chin'][-5]

        # 左右嘴角
        self.face_pose['mouth_left'] = landFeature['top_lip'][-1]
        self.face_pose['mouth_right'] = landFeature['top_lip'][7]

        # nose
        self.face_pose['nose_tip'] = landFeature['nose_tip']
        self.face_pose['nose_bridge'] = landFeature['nose_bridge']

        # eyebrow
        self.face_pose['eyebrow_left'] = landFeature['left_eyebrow']
        self.face_pose['eyebrow_right'] = landFeature['right_eyebrow']

        # 上嘴唇
        self.face_pose['top_lip'] = landFeature['top_lip']
        # 下嘴唇
        self.face_pose['bottom_lip'] = landFeature['bottom_lip']
