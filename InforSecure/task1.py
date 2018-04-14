import cv2
import random

MSG_TO_HIDE = 'InformationSecurity'
LENGTH_TO_HIDE = len(MSG_TO_HIDE)
HIDED_FILE_NAME = 'Jobs_hided.avi'
LAYER_TO_HIDE = 0

four_cc = cv2.VideoWriter_fourcc(*'DIVX')


def encode() -> int:
    cap = cv2.VideoCapture('Jobs.avi')
    fps = cap.get(cv2.CAP_PROP_FPS)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)

    target = random.randint(0, len(frames) - 1)
    for idx, ch in enumerate(MSG_TO_HIDE):
        frames[target][0, idx, LAYER_TO_HIDE] = ord(ch)

    cv2.imwrite('test.jpg', frames[target])
    img = cv2.imread('test.jpg')
    print(img[0, 0:LENGTH_TO_HIDE, LAYER_TO_HIDE])

    size = frames[0].shape[1], frames[0].shape[0]
    hide = cv2.VideoWriter(HIDED_FILE_NAME, four_cc, fps, size, True)
    for frame in frames:
        hide.write(frame)
    hide.release()
    cap.release()
    return target


def decode(target: int) -> str:
    cap = cv2.VideoCapture(HIDED_FILE_NAME)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    frame = frames[target]

    message = [i for i in frame[0, 0:LENGTH_TO_HIDE, LAYER_TO_HIDE]]
    message = ''.join([chr(i) for i in message])
    return message


if __name__ == '__main__':
    tar = encode()
    msg = decode(tar)
    print(msg)
