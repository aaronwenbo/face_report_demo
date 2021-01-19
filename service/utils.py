"""
工具类
"""
import math

def get_median(data):
    data_temp = data.copy()
    data_temp.sort()
    half = len(data_temp) // 2
    return (data_temp[half] + data_temp[~half]) / 2

# 计算比例
def cal_proportion(_list):
    if len(_list) == 2:
        min_index = _list.index(min(_list))
        temp = round(max(_list)/min(_list),2)
        if min_index == 0:
            return "1.0:"+str(temp)
        else:
            return str(temp)+":1.0"
    # 找出最中间位置的值
    median = get_median(_list)
    result = ""
    for i in range(len(_list)):
        temp = round(_list[i] / median, 2)
        if i != len(_list) - 1:
            result += str(temp)+":"
            continue
        result += str(temp)
    return result

# 计算夹角
def cal_angle(point_1, point_2, point_3):
    """
    根据三点坐标计算夹角
    :param point_1: 点1坐标
    :param point_2: 点2坐标
    :param point_3: 点3坐标
    :return: 返回任意角的夹角值，这里只是返回点2的夹角
    """
    a=math.sqrt((point_2[0]-point_3[0])*(point_2[0]-point_3[0])+(point_2[1]-point_3[1])*(point_2[1] - point_3[1]))
    b=math.sqrt((point_1[0]-point_3[0])*(point_1[0]-point_3[0])+(point_1[1]-point_3[1])*(point_1[1] - point_3[1]))
    c=math.sqrt((point_1[0]-point_2[0])*(point_1[0]-point_2[0])+(point_1[1]-point_2[1])*(point_1[1]-point_2[1]))
    # A=math.degrees(math.acos((a*a-b*b-c*c)/(-2*b*c)))
    B=math.degrees(math.acos((b*b-a*a-c*c)/(-2*a*c)))
    # C=math.degrees(math.acos((c*c-a*a-b*b)/(-2*a*b)))
    return B


if __name__ == '__main__':
    _list = [199, 306, 96]
    num_proportion = cal_proportion(_list)
    print(list(map(lambda x: float(x), num_proportion.split(":"))))

    print(cal_angle((0,1), (0,0), (1,0)))
