import cv2
from matplotlib import pyplot as plt

TRAIN_IMAGES = 12
images = ['images/train/{num}.jpg'.format(num=i) for i in range(1, TRAIN_IMAGES + 1)]

H_pixels = list()
S_pixels = list()
V_pixels = list()
R_pixels = list()
G_pixels = list()
B_pixels = list()

# 读取图像并统计每张图像HSV/RGB色域下，各个通道的像素值均值
# 原本采用获取最小/最大像素值的方法，但是发现会有少数色素的
# 干扰，使用先求均值，再对各张图像的均值求阈值的方法，肤色区
# 域的检测效果会更好
for image in images:
    orig = cv2.imread(image)
    # python opencv的默认色域是BGR
    # 转换到HSV色域
    hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    H_pixels.append(h.mean())
    S_pixels.append(s.mean())
    V_pixels.append(v.mean())
    rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    r, g, b = cv2.split(rgb)
    R_pixels.append(r.mean())
    G_pixels.append(g.mean())
    B_pixels.append(b.mean())

H_min, H_max = min(H_pixels), max(H_pixels)
S_min, S_max = min(S_pixels), max(S_pixels)
V_min, V_max = min(V_pixels), max(V_pixels)
R_min, R_max = min(R_pixels), max(R_pixels)
G_min, G_max = min(G_pixels), max(G_pixels)
B_min, B_max = min(B_pixels), max(B_pixels)

SAMPLE_IMAGES = 7
samples = ['images/test/{num}.jpg'.format(num=i) for i in range(0, SAMPLE_IMAGES)]

for sample in samples:
    orig = cv2.imread(sample)
    hsv = cv2.cvtColor(orig, cv2.COLOR_BGR2HSV)
    rgb = cv2.cvtColor(orig, cv2.COLOR_BGR2RGB)
    # 均一化: HSV: 非肤色范围的像素全部置为同一颜色(转换得(0,0,100)应是白色,
    #              可能是opencv的问题,实际上并不是白色)
    #         RGB: 非肤色范围的像素全部置白
    hsv[:, :, 0][hsv[:, :, 0] < H_min] = 0
    hsv[:, :, 0][hsv[:, :, 0] > H_max] = 0
    hsv[:, :, 1][hsv[:, :, 1] < S_min] = 0
    hsv[:, :, 1][hsv[:, :, 1] > S_max] = 0
    hsv[:, :, 2][hsv[:, :, 2] < V_min] = 100
    hsv[:, :, 2][hsv[:, :, 2] > V_max] = 100

    rgb[:, :, 0][rgb[:, :, 0] < R_min] = 255
    rgb[:, :, 0][rgb[:, :, 0] > R_max] = 255
    rgb[:, :, 1][rgb[:, :, 1] < G_min] = 255
    rgb[:, :, 1][rgb[:, :, 1] > G_max] = 255
    rgb[:, :, 2][rgb[:, :, 2] < B_min] = 255
    rgb[:, :, 2][rgb[:, :, 2] > B_max] = 255
    _, subs = plt.subplots(1, 3)
    subs[0].imshow(orig)
    subs[0].set_title('Origin')
    subs[1].imshow(hsv)
    subs[1].set_title('HSV')
    subs[2].imshow(rgb)
    subs[2].set_title('RGB')
    plt.savefig('test_{}.png'.format(sample[-5:-4]))
    # plt.show()
