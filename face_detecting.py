import cv2
import serial
def detect_and_label_face():
    #加载已有模型
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    # 连接相机（0，自带；1，接口。。。）
    cap = cv2.VideoCapture(1)
    # 初始化技术求和变量
    count=1
    face_sum=0
    #设置串口
    arduino_port = 'COM8'  # 设置串口名称
    arduino_baudrate = 9600  # 要与Arduino代码中的波特率相匹配
    ser = serial.Serial(arduino_port, arduino_baudrate)
    while True:
        # 相机取帧
        ret, frame = cap.read()
        if ret:
            # 转化灰度图
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 找脸
            faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=3, minSize=(80, 80))

            # 找最大脸
            largest_face = None
            largest_area = 0
            for (x, y, w, h) in faces:
                face_area = w * h
                if face_area > largest_area:
                    largest_face = (x, y, w, h)
                    largest_area = face_area

            # 脸周围画框
            if largest_face is not None:
                x, y, w, h = largest_face
                face_center_x = x + w // 2
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)  # Draw rectangle around the face
                cv2.putText(frame, f'Face (X: {face_center_x})', (x, y - 10),cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255, 0, 0), 2)  # Label the face with face_center_x                
                count=count+1
                face_sum=face_sum+face_center_x
                #平均五帧响应一次
                if count%5==0:
                    face_sum = face_sum / 4
                    face_sum=int(face_sum)
                    if(face_sum<310):
                        ser.write(b"0")#ser.write在于向串口中写入数据
                    if(face_sum>330):
                        ser.write(b"1")
                    count = 1
                    print(face_sum)
                    face_sum = 0

            # 展示帧
            cv2.imshow('Camera', frame)

        # 按‘q'退出
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # 释放
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    detect_and_label_face()
