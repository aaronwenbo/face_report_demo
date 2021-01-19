import face_recognition
import cv2 as cv
import requests
import numpy as np


image_path = './images/10.jpg'

img = cv.imread(image_path)
print(img.shape)
height, width, _ = img.shape
# 脸位置判定
face_locations = face_recognition.face_locations(img)
top, right, bottom, left = face_locations[0]
# img = cv.rectangle(img, (left, top), (right, bottom), (0,255,255), 2)

# 脸部关键点
landFeature = face_recognition.face_landmarks(cv.cvtColor(img, cv.COLOR_BGR2RGB), num_landmarks=68)[0]
print(landFeature)
for key, value in landFeature.items():
    p = 0
    for point in value:
        cv.circle(img, (point[0], point[1]), 2, (0, 0, 255))
        cv.putText(img, str(p), (point[0], point[1]), cv.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
        p += 1
# cv.imwrite("12.jpg", img)
cv.imshow("output", img)
cv.waitKey(0)

# 五眼比例
# 左右颧骨
cheekbone_left = landFeature['chin'][1]
cheekbone_right = landFeature['chin'][-2]
# 下巴中心点
chin_center = landFeature['chin'][8]
jaw = landFeature['chin'][6:11]
print("------------------")
print(jaw)

# 左右眼角
corner_of_eye_left = landFeature['left_eye'][3]
corner_of_eye_right = landFeature['right_eye'][0]

# 左右眼尾
outer_corner_of_eye_left = landFeature['left_eye'][0]
outer_corner_of_eye_right = landFeature['right_eye'][3]

# 左右腮部转折点
cheek_left = landFeature['chin'][4]
cheek_right = landFeature['chin'][-5]

# 提取发际线点
def hairline(image_path):
    url = r"http://192.168.1.254:9897/bisenet"
    # 图片名
    file_name = image_path.split('/')[-1]
    src = cv.imread(image_path)
    h, w, _ = src.shape
    src_copy = cv.resize(src, (512, 512), interpolation=cv.INTER_NEAREST)
    src_byte = cv.imencode(".jpg", src_copy)[1].tobytes()
    # 拼接参数
    files = {'image': (file_name, src_byte, 'image/jpg')}
    res = requests.post(url, files=files)
    # 获取服务器返回的图片，字节流返回
    result = res.json()
    if result['success']:
        # 只有0-20的结果矩阵
        parsing = np.array(result['results'])
    else:
        parsing = None
    parsing = parsing.astype(np.uint8)
    parsing = cv.resize(parsing, (h, w), interpolation=cv.INTER_NEAREST)
    cv.imshow("output", parsing)
    cv.waitKey(0)
    # 0背景,1帽子,2头发,3手套,4太阳镜,5上装,6连衣裙,7外套,8袜子,9裤子,10皮肤,
    # 11围巾,12裙子,13脸,14左臂,15右臂,16左腿,17右腿,18左鞋,19右鞋。
    atts = ['skin', 'l_brow', 'r_brow', 'l_eye', 'r_eye', 'eye_g', 'l_ear', 'r_ear', 'ear_r',
            'nose', 'mouth', 'u_lip', 'l_lip', 'neck', 'neck_l', 'cloth', 'hair', 'hat']
    skin = parsing[parsing==1]
    pass


def draw_five_eye():
    # 标准五眼
    face_witdh = int(cheekbone_right[0]-cheekbone_left[0])
    for i in [0, 0.2, 0.4, 0.6, 0.8, 1]:
        cv.line(img, (int(cheekbone_left[0]+face_witdh*i), top-1), (int(cheekbone_left[0]+face_witdh*i), bottom-1), (0,255,0), 2)
    # user五眼
    # cv.line(img, (cheekbone_left[0],top-1), (cheekbone_left[0], bottom-1), (255,255,0), 2)
    # cv.line(img, (outer_corner_of_eye_left[0],top-1), (outer_corner_of_eye_left[0], bottom-1), (255,255,0), 2)
    # cv.line(img, (corner_of_eye_left[0],top-1), (corner_of_eye_left[0], bottom-1), (255,255,0), 2)
    # cv.line(img, (outer_corner_of_eye_right[0],top-1), (outer_corner_of_eye_right[0], bottom-1), (255,255,0), 2)
    # cv.line(img, (corner_of_eye_right[0],top-1), (corner_of_eye_right[0], bottom-1), (255,255,0), 2)
    # cv.line(img, (cheekbone_right[0],top-1), (cheekbone_right[0], bottom-1), (255,255,0), 2)
    cv.imshow("output", img)
    cv.waitKey(0)

def draw_three_ting():
    # 标准三庭
    face_height = 0

draw_five_eye()
cv.imshow("output", img)
cv.waitKey(0)

if __name__ == '__main__':
    pass
    # hairline(image_path)