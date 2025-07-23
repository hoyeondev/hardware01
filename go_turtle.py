import turtle
import serial
import time

# 시리얼 포트 설정 (COM 포트 번호는 아두이노 환경에 맞게 수정)
connection = serial.Serial('COM3', 9600, timeout=1)
time.sleep(2)  # 아두이노 초기화 대기

# 거북이 셋업
robot = turtle.Turtle()
robot.hideturtle()
robot.shape("turtle")
robot.shapesize(2,2)
robot.speed(1)  # 속도 설정
robot.penup()
robot.goto(-400, 0)
robot.showturtle()
robot.pendown()
robot.color('sky blue')

# 앞으로 전진하는 함수
def move_forward():
    robot.forward(80)  # 50픽셀 전진

# 시리얼 수신 루프
def listen_serial():
    if connection.in_waiting:
        data = connection.readline().decode().strip()
        if data == "go":
            move_forward()
    turtle.ontimer(listen_serial, 100)  # 0.1초마다 반복 실행

# 실행
listen_serial()
turtle.mainloop()
