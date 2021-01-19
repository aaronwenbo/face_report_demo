from service.face_pose import facePose
from service.display import line, show
from service.utils import cal_proportion, cal_angle
import cv2 as cv
import base64
import os

_BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class faceReport(facePose):
    def __init__(self, image_path):
        super().__init__(image_path)
        self.src = self.img.copy()
        self.proportion = {}
        self.type = {}
        self.data = {}
        self.face_height_and_width()

    def display_(self, mode=None):
        src = self.src.copy()
        # 长度
        if mode == 'height':
            print("红色：脸长为", self.face_length)
            print("绿色：颧骨高为", self.cheekbone_height)
            print("蓝色：腮部转折点高为", self.cheek_height)
            # 脸长可视化
            line(src,
                 (self.face_pose['face_location']['left'] - 1, self.face_pose['chin_center'][1]),
                 (self.face_pose['face_location']['right'], self.face_pose['chin_center'][1]),
                 (0, 0, 255))
            line(src,
                 (self.face_pose['face_location']['left'] - 1, self.face_pose['forehead'][1]),
                 (self.face_pose['face_location']['right'], self.face_pose['forehead'][1]),
                 (0, 0, 255))
            # 颧骨高可视化
            line(src,
                 (
                     self.face_pose['face_location']['left'] - 1,
                     self.face_pose['chin_center'][1] - self.cheekbone_height),
                 (self.face_pose['face_location']['right'], self.face_pose['chin_center'][1] - self.cheekbone_height))
            # 腮部转折点高可视化
            line(src,
                 (self.face_pose['face_location']['left'] - 1, self.face_pose['chin_center'][1] - self.cheek_height),
                 (self.face_pose['face_location']['right'], self.face_pose['chin_center'][1] - self.cheek_height),
                 (255, 0, 0))

        # 宽度
        if mode == 'width':
            print("红色：颧骨宽为", self.zygoma_width)
            print("绿色：下颌宽为", self.cheek_width)
            print("蓝色：颞骨宽为", self.temple_width)
            print("淡蓝色：嘴宽为", self.mouth_width)
            print("黄色：瞳距为", self.eye_distance)
            # 脸宽可视化
            line(src,
                 (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['top']),
                 (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['bottom'] - 1),
                 (0, 0, 255))
            line(src,
                 (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['top']),
                 (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['bottom'] - 1),
                 (0, 0, 255))
            # 下颌宽
            line(src,
                 (self.face_pose['cheek_left'][0],
                  self.face_pose['face_location']['top'] + int(0.35 * self.face_length)),
                 (self.face_pose['cheek_left'][0],
                  self.face_pose['face_location']['bottom'] - int(0.1 * self.face_length)),
                 )
            line(src,
                 (self.face_pose['cheek_right'][0],
                  self.face_pose['face_location']['top'] + int(0.35 * self.face_length)),
                 (self.face_pose['cheek_right'][0],
                  self.face_pose['face_location']['bottom'] - int(0.1 * self.face_length)),
                 )
            # 颞骨宽
            line(src,
                 (self.face_pose['temple_left'][0],
                  self.face_pose['face_location']['top'] + int(0.01 * self.face_length)),
                 (self.face_pose['temple_left'][0],
                  self.face_pose['face_location']['bottom'] - int(0.4 * self.face_length)),
                 (255, 0, 0)
                 )
            line(src,
                 (self.face_pose['temple_right'][0],
                  self.face_pose['face_location']['top'] + int(0.01 * self.face_length)),
                 (self.face_pose['temple_right'][0],
                  self.face_pose['face_location']['bottom'] - int(0.4 * self.face_length)),
                 (255, 0, 0)
                 )
            # 嘴宽
            line(src,
                 (self.face_pose['mouth_left'][0],
                  self.face_pose['face_location']['top'] + int(0.6 * self.face_length)),
                 (self.face_pose['mouth_left'][0],
                  self.face_pose['face_location']['bottom'] - int(0.04 * self.face_length)),
                 (255, 255, 0)
                 )
            line(src,
                 (self.face_pose['mouth_right'][0],
                  self.face_pose['face_location']['top'] + int(0.6 * self.face_length)),
                 (self.face_pose['mouth_right'][0],
                  self.face_pose['face_location']['bottom'] - int(0.04 * self.face_length)),
                 (255, 255, 0)
                 )
            # 瞳距
            line(src,
                 (int((self.face_pose['corner_of_eye_left'][0] + self.face_pose['outer_corner_of_eye_left'][0]) / 2),
                  int((self.face_pose['corner_of_eye_left'][1] + self.face_pose['outer_corner_of_eye_left'][1]) / 2)),
                 (int((self.face_pose['corner_of_eye_right'][0] + self.face_pose['outer_corner_of_eye_right'][0]) / 2),
                  int((self.face_pose['corner_of_eye_right'][1] + self.face_pose['outer_corner_of_eye_right'][1]) / 2)),
                 (0, 255, 255)
                 )

        # 标准五眼
        if mode == 'standard_five_eye':
            for i in [0, 0.2, 0.4, 0.6, 0.8, 1]:
                line(src, (
                    int(self.face_pose['cheekbone_left'][0] + self.zygoma_width * i),
                    self.face_pose['face_location']['top'] - 1),
                     (int(self.face_pose['cheekbone_left'][0] + self.zygoma_width * i),
                      self.face_pose['face_location']['bottom'] - 1))

        # 用户五眼
        if mode == 'user_five_eye':
            line(src, (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['bottom'] - 1), (255, 255, 0), 2)
            line(src, (self.face_pose['outer_corner_of_eye_left'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['outer_corner_of_eye_left'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['corner_of_eye_left'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['corner_of_eye_left'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['outer_corner_of_eye_right'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['outer_corner_of_eye_right'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['corner_of_eye_right'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['corner_of_eye_right'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['bottom'] - 1), (255, 255, 0),
                 2)

        # 标准三庭
        if mode == 'standard_three_ting':
            for i in [0, 0.33, 0.66, 1]:
                line(src,
                     (self.face_pose['face_location']['left'] - 1,
                      int(self.face_pose['forehead'][1] + self.face_length * i)),
                     (self.face_pose['face_location']['right'],
                      int(self.face_pose['forehead'][1] + self.face_length * i))
                     )

        # 标准小三庭
        if mode == 'standard_small_three_ting':
            for i in [0, 0.33, 1]:
                line(src,
                     (self.face_pose['face_location']['left'] - 1, int(self.face_pose['nose_tip'][2][1] + abs(
                         self.face_pose['nose_tip'][2][1] - self.face_pose['chin_center'][1]) * i)),
                     (self.face_pose['face_location']['right'], int(self.face_pose['nose_tip'][2][1] + abs(
                         self.face_pose['nose_tip'][2][1] - self.face_pose['chin_center'][1]) * i)),
                     (255, 255, 0)
                     )

        # 用户三庭
        if mode == 'user_three_ting':
            pass
        self.src = src
        # show(src)

    def draw(self, mode=None):
        src = self.src.copy()
        # 长度
        if mode == 'height':
            print("红色：脸长为", self.face_length)
            print("绿色：颧骨高为", self.cheekbone_height)
            print("蓝色：腮部转折点高为", self.cheek_height)
            # 脸长可视化
            line(src,
                 (self.face_pose['face_location']['left'] - 1, self.face_pose['chin_center'][1]),
                 (self.face_pose['face_location']['right'], self.face_pose['chin_center'][1]),
                 (0, 0, 255))
            line(src,
                 (self.face_pose['face_location']['left'] - 1, self.face_pose['forehead'][1]),
                 (self.face_pose['face_location']['right'], self.face_pose['forehead'][1]),
                 (0, 0, 255))
            # 颧骨高可视化
            line(src,
                 (
                     self.face_pose['face_location']['left'] - 1,
                     self.face_pose['chin_center'][1] - self.cheekbone_height),
                 (self.face_pose['face_location']['right'], self.face_pose['chin_center'][1] - self.cheekbone_height))
            # 腮部转折点高可视化
            line(src,
                 (self.face_pose['face_location']['left'] - 1, self.face_pose['chin_center'][1] - self.cheek_height),
                 (self.face_pose['face_location']['right'], self.face_pose['chin_center'][1] - self.cheek_height),
                 (255, 0, 0))

        # 宽度
        if mode == 'width':
            # print("红色：颧骨宽为", self.zygoma_width)
            # print("绿色：下颌宽为", self.cheek_width)
            # print("蓝色：颞骨宽为", self.temple_width)
            # print("淡蓝色：嘴宽为", self.mouth_width)
            # print("黄色：瞳距为", self.eye_distance)
            # 脸宽可视化
            line(src,
                 (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['top']),
                 (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['bottom'] - 1),
                 (0, 0, 255))
            line(src,
                 (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['top']),
                 (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['bottom'] - 1),
                 (0, 0, 255))
            # 下颌宽
            line(src,
                 (self.face_pose['cheek_left'][0],
                  self.face_pose['face_location']['top'] + int(0.35 * self.face_length)),
                 (self.face_pose['cheek_left'][0],
                  self.face_pose['face_location']['bottom'] - int(0.1 * self.face_length)),
                 )
            line(src,
                 (self.face_pose['cheek_right'][0],
                  self.face_pose['face_location']['top'] + int(0.35 * self.face_length)),
                 (self.face_pose['cheek_right'][0],
                  self.face_pose['face_location']['bottom'] - int(0.1 * self.face_length)),
                 )
            # 颞骨宽
            line(src,
                 (self.face_pose['temple_left'][0],
                  self.face_pose['face_location']['top'] + int(0.01 * self.face_length)),
                 (self.face_pose['temple_left'][0],
                  self.face_pose['face_location']['bottom'] - int(0.4 * self.face_length)),
                 (255, 0, 0)
                 )
            line(src,
                 (self.face_pose['temple_right'][0],
                  self.face_pose['face_location']['top'] + int(0.01 * self.face_length)),
                 (self.face_pose['temple_right'][0],
                  self.face_pose['face_location']['bottom'] - int(0.4 * self.face_length)),
                 (255, 0, 0)
                 )
            # # 嘴宽
            # line(src,
            #      (self.face_pose['mouth_left'][0],
            #       self.face_pose['face_location']['top'] + int(0.6 * self.face_length)),
            #      (self.face_pose['mouth_left'][0],
            #       self.face_pose['face_location']['bottom'] - int(0.04 * self.face_length)),
            #      (255, 255, 0)
            #      )
            # line(src,
            #      (self.face_pose['mouth_right'][0],
            #       self.face_pose['face_location']['top'] + int(0.6 * self.face_length)),
            #      (self.face_pose['mouth_right'][0],
            #       self.face_pose['face_location']['bottom'] - int(0.04 * self.face_length)),
            #      (255, 255, 0)
            #      )
            # # 瞳距
            # line(src,
            #      (int((self.face_pose['corner_of_eye_left'][0] + self.face_pose['outer_corner_of_eye_left'][0]) / 2),
            #       int((self.face_pose['corner_of_eye_left'][1] + self.face_pose['outer_corner_of_eye_left'][1]) / 2)),
            #      (int((self.face_pose['corner_of_eye_right'][0] + self.face_pose['outer_corner_of_eye_right'][0]) / 2),
            #       int((self.face_pose['corner_of_eye_right'][1] + self.face_pose['outer_corner_of_eye_right'][1]) / 2)),
            #      (0, 255, 255)
            #      )

        # 标准五眼
        if mode == 'standard_five_eye':
            for i in [0, 0.2, 0.4, 0.6, 0.8, 1]:
                line(src, (
                    int(self.face_pose['cheekbone_left'][0] + self.zygoma_width * i),
                    self.face_pose['face_location']['top'] - 1),
                     (int(self.face_pose['cheekbone_left'][0] + self.zygoma_width * i),
                      self.face_pose['face_location']['bottom'] - 1))

        # 用户五眼
        if mode == 'user_five_eye':
            line(src, (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['cheekbone_left'][0], self.face_pose['face_location']['bottom'] - 1), (255, 255, 0), 2)
            line(src, (self.face_pose['outer_corner_of_eye_left'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['outer_corner_of_eye_left'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['corner_of_eye_left'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['corner_of_eye_left'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['outer_corner_of_eye_right'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['outer_corner_of_eye_right'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['corner_of_eye_right'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['corner_of_eye_right'][0], self.face_pose['face_location']['bottom'] - 1),
                 (255, 255, 0), 2)
            line(src, (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['top'] - 1),
                 (self.face_pose['cheekbone_right'][0], self.face_pose['face_location']['bottom'] - 1), (255, 255, 0),
                 2)

        # 标准三庭
        if mode == 'standard_three_ting':
            for i in [0, 0.33, 0.66, 1]:
                line(src,
                     (self.face_pose['face_location']['left'] - 1,
                      int(self.face_pose['forehead'][1] + self.face_length * i)),
                     (self.face_pose['face_location']['right'],
                      int(self.face_pose['forehead'][1] + self.face_length * i))
                     )

        # 标准小三庭
        if mode == 'standard_small_three_ting':
            for i in [0, 0.33, 1]:
                line(src,
                     (self.face_pose['face_location']['left'] - 1, int(self.face_pose['nose_tip'][2][1] + abs(
                         self.face_pose['nose_tip'][2][1] - self.face_pose['chin_center'][1]) * i)),
                     (self.face_pose['face_location']['right'], int(self.face_pose['nose_tip'][2][1] + abs(
                         self.face_pose['nose_tip'][2][1] - self.face_pose['chin_center'][1]) * i)),
                     (255, 255, 0)
                     )

        # 用户三庭
        if mode == 'user_three_ting':
            line(src, (self.face_pose['face_location']['left'] - 1,
                       int(self.face_pose['forehead'][1])),
                 (self.face_pose['face_location']['right'],
                  int(self.face_pose['forehead'][1])),
                 (255, 255, 0))
            line(src,
                 (self.face_pose['face_location']['left'] - 1,
                  int(min(self.face_pose['eyebrow_left'][2][1], self.face_pose['eyebrow_right'][2][1]))),
                 (self.face_pose['face_location']['right'],
                  int(min(self.face_pose['eyebrow_left'][2][1], self.face_pose['eyebrow_right'][2][1]))),
                 (255, 255, 0))
            line(src,
                 (self.face_pose['face_location']['left'] - 1,
                  int(self.face_pose['nose_tip'][2][1])),
                 (self.face_pose['face_location']['right'],
                  int(self.face_pose['nose_tip'][2][1])),
                 (255, 255, 0))
            line(src,
                 (self.face_pose['face_location']['left'] - 1,
                  int(self.face_pose['chin_center'][1])),
                 (self.face_pose['face_location']['right'],
                  int(self.face_pose['chin_center'][1])),
                 (255, 255, 0))

        # 鼻比例
        if mode == 'nose':
            line(src, self.face_pose['nose_tip'][0],
                 self.face_pose['nose_tip'][4]
                 )
            line(src, self.face_pose['nose_bridge'][0],
                 self.face_pose['nose_tip'][2]
                 )
        return src

    def face_height_and_width(self):
        """
        长度与宽度
        :return: face_length, face_width
        """
        # ---------------------------------长度-----------------------------------------
        # 脸长
        self.face_length = int(abs(self.face_pose['forehead'][1] - self.face_pose['chin_center'][1]))
        # 颧骨高
        self.cheekbone_height = int(abs(
            (self.face_pose['cheekbone_left'][1] + self.face_pose['cheekbone_right'][1]) / 2 -
            self.face_pose['chin_center'][1]))
        # 腮部转折点高
        self.cheek_height = int(abs(
            (self.face_pose['cheek_left'][1] + self.face_pose['cheek_right'][1]) / 2 - self.face_pose['chin_center'][
                1]))
        # ---------------------------------宽度-----------------------------------------
        # 颧骨宽
        self.zygoma_width = int(abs(self.face_pose['cheekbone_left'][0] - self.face_pose['cheekbone_right'][0]))
        # 下颌宽度
        self.cheek_width = int(abs(self.face_pose['cheek_left'][0] - self.face_pose['cheek_right'][0]))
        # 颞骨宽度
        self.temple_width = int(abs(self.face_pose['temple_left'][0] - self.face_pose['temple_right'][0]))
        # 脸宽
        self.face_width = max(self.zygoma_width, self.cheek_width, self.temple_width)
        # 嘴角宽度
        self.mouth_width = int(abs(self.face_pose['mouth_left'][0] - self.face_pose['mouth_right'][0]))
        # 瞳距
        self.eye_distance = int(abs(
            (self.face_pose['corner_of_eye_left'][0] + self.face_pose['outer_corner_of_eye_left'][0]) / 2 -
            (self.face_pose['corner_of_eye_right'][0] + self.face_pose['outer_corner_of_eye_right'][0]) / 2
        ))

        # self.display_(mode='height')
        # self.display_(mode='width')

    def three_ting(self):
        """
        三庭比例
        :return: 
        """
        # 标准三庭
        src = self.img.copy()
        for i in [0, 0.33, 0.66, 1]:
            line(src, (
                self.face_pose['face_location']['left'] - 1, int(self.face_pose['forehead'][1] + self.face_length * i)),
                 (self.face_pose['face_location']['right'], int(self.face_pose['forehead'][1] + self.face_length * i)))
        # show(src)

    def get_proportion(self):
        """
        比例
        :return:
        """
        # 脸长宽比
        self.proportion['face_height_width'] = cal_proportion([self.face_length, self.face_width])
        self.proportion['proportion_temple_zygoma_cheek'] = cal_proportion(
            [self.temple_width, self.zygoma_width, self.cheek_width])
        # 五眼比例
        eye_one = abs(self.face_pose['cheekbone_left'][0] - self.face_pose['outer_corner_of_eye_left'][0])
        eye_two = abs(self.face_pose['outer_corner_of_eye_left'][0] - self.face_pose['corner_of_eye_left'][0])
        eye_three = abs(self.face_pose['corner_of_eye_left'][0] - self.face_pose['corner_of_eye_right'][0])
        eye_four = abs(self.face_pose['corner_of_eye_right'][0] - self.face_pose['outer_corner_of_eye_right'][0])
        eye_five = abs(self.face_pose['outer_corner_of_eye_right'][0] - self.face_pose['cheekbone_right'][0])
        self.proportion['proportion_five_yan'] = cal_proportion([eye_one, eye_two, eye_three, eye_four, eye_five])
        # 三庭比例
        ting_one = abs(self.face_pose['forehead'][1] - min(self.face_pose['eyebrow_left'][2][1],
                                                           self.face_pose['eyebrow_right'][2][1]))
        ting_two = abs(min(self.face_pose['eyebrow_left'][2][1], self.face_pose['eyebrow_right'][2][1]) -
                       self.face_pose['nose_tip'][2][1])
        ting_three = abs(self.face_pose['nose_tip'][2][1] - self.face_pose['chin_center'][1])
        self.proportion['proportion_three_ting'] = cal_proportion([ting_one, ting_two, ting_three])
        # 小三庭比例
        small_ting_one = abs(self.face_pose['nose_tip'][2][1] - 0.5 * (
                    self.face_pose['top_lip'][3][1] + self.face_pose['bottom_lip'][3][1]))
        small_ting_two = abs(0.5 * (
                    self.face_pose['top_lip'][3][1] + self.face_pose['bottom_lip'][3][1])-self.face_pose['chin_center'][1])
        self.proportion['proportion_small_three_ting'] = cal_proportion([small_ting_one, small_ting_two])
        # 鼻比例
        length_nose_bridge = abs(self.face_pose['nose_bridge'][0][1]-self.face_pose['nose_tip'][2][1])
        length_nose_tip = abs(self.face_pose['nose_tip'][0][0]-self.face_pose['nose_tip'][4][0])
        self.proportion['proportion_nose'] = cal_proportion([length_nose_bridge, length_nose_tip])
        #

    def jaw_type(self):
        """
        下巴类型
        :return: 尖下巴、圆下巴、方下巴 其中之一
        """
        # 小下巴角度，下三点夹角
        small_jaw_angle = cal_angle(self.face_pose['jaw'][1], self.face_pose['jaw'][2], self.face_pose['jaw'][3])
        if small_jaw_angle > 170 and small_jaw_angle < 180:
            return {"jaw_type": "方下巴"}
        elif small_jaw_angle < 160:
            return {"jaw_type": "尖下巴"}
        else:
            return {"jaw_type": "圆下巴"}

    def face_type(self):
        """
        脸型判断
        :return: 长脸、心形脸、菱形脸、圆脸、方形脸、鹅蛋脸 其中之一
        """
        # 脸长宽比转为数字
        proportion_face_list = list(map(lambda x: float(x), self.proportion['face_height_width'].split(":")))
        # 颞骨、颧骨、下颌骨比转为数字
        proportion_temple_zygoma_cheek_list = list(
            map(lambda x: float(x), self.proportion['proportion_temple_zygoma_cheek'].split(":")))
        # 脸型判断
        if proportion_face_list[0] >= 1.5:
            return {"face_type": "长形脸", "reason": "面部长宽比例为{}".format(round(proportion_face_list[0], 2))}

        if max(proportion_temple_zygoma_cheek_list) / min(proportion_temple_zygoma_cheek_list) < 1.13:
            return {"face_type": "方形脸",
                    "reason": "颞骨、颧骨、下颌比例为{}，非常相近，判断为方形脸".format(self.proportion['proportion_temple_zygoma_cheek'])}

        if proportion_temple_zygoma_cheek_list.index(max(proportion_temple_zygoma_cheek_list)) == 1:
            # 颧骨最宽 备选为 心形脸 or 菱形脸
            # 下颌角角度
            angle_of_cheek_and_chinCenter = cal_angle(self.face_pose['cheek_left'], self.face_pose['chin_center'],
                                                      self.face_pose['cheek_right'])
            if angle_of_cheek_and_chinCenter < 110:
                return {"face_type": "心形脸",
                        "reason": "颧骨最宽，下颌角为{}，下巴较尖，判断为心形脸，".format(str(round(angle_of_cheek_and_chinCenter, 2)))}
            return {"face_type": "菱形脸", "reason": "颧骨最宽，额头、下巴较窄，判断为菱形脸"}
        return {"face_type": "鹅蛋脸", "reason": "女性最想要的鹅蛋脸！"}

    def save_img(self):
        """
        保存各个类型的图片
        :return:
        """
        # 三庭
        three_ting = self.draw(mode="user_three_ting")
        image_three_ting = cv.imencode('.jpg', three_ting)[1]
        self.data['img_three_ting'] = str(base64.b64encode(image_three_ting))[2:-1]
        # cv.imwrite(r'D:\work_git\face_report_demo\static\result\three_ting.jpg', three_ting)
        # 五眼
        five_yan = self.draw(mode="user_five_eye")
        image_five_yan = cv.imencode('.jpg', five_yan)[1]
        self.data['img_five_eye'] = str(base64.b64encode(image_five_yan))[2:-1]
        # cv.imwrite(r'D:\work_git\face_report_demo\static\result\five_yan.jpg', five_yan)
        # 小三庭
        small_three_ting = self.draw(mode="standard_small_three_ting")
        image_small_three_ting = cv.imencode('.jpg', small_three_ting)[1]
        self.data['img_small_three_ting'] = str(base64.b64encode(image_small_three_ting))[2:-1]
        # cv.imwrite(r'D:\work_git\face_report_demo\static\result\small_three_ting.jpg', small_three_ting)
        # 脸型
        face_type = self.draw(mode="width")
        image_face_type = cv.imencode('.jpg', face_type)[1]
        self.data['img_face_type'] = str(base64.b64encode(image_face_type))[2:-1]
        # 鼻比例
        nose_proportion = self.draw(mode="nose")
        image_nose_proportion = cv.imencode('.jpg', nose_proportion)[1]
        self.data['img_nose_proportion'] = str(base64.b64encode(image_nose_proportion))[2:-1]



    def get_data(self):
        self.data['face'] = self.face_type()
        self.data['mouth'] = self.jaw_type()
        self.data['five_eye'] = self.proportion['proportion_five_yan']
        self.data['three_ting'] = self.proportion['proportion_three_ting']
        self.data['small_three_ting'] = self.proportion['proportion_small_three_ting']
        self.data['nose'] = self.proportion['proportion_nose']
        return self.data


if __name__ == '__main__':
    image_path = './images/11.jpg'
    face_report = faceReport(image_path)
    face_report.save_img()
    face_report.get_proportion()
    data = face_report.get_data()
    print(data)
    # face_report.three_ting()
