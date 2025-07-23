import serial
import time
import turtle
import threading

# 전역 변수
connection = None
current_distance = 100  # 초기값 (충돌 방지용)
DISTANCE_THRESHOLD = 20  # cm 이하면 장애물로 간주하고 정지

MOVE_STEP = 10
SIDE_LENGTH = 300  # 한 변의 길이 (픽셀 단위)
moved_distance = 0

# 터틀 설정
robot = turtle.Turtle()
robot.hideturtle()
robot.shape("turtle")
robot.shapesize(1.5,1.5) # 터틀 사이즈
robot.color("green")
robot.penup()
robot.speed(1)

      # 거북이 숨김
robot.goto(-400, 0)      # 왼쪽으로 이동
robot.setheading(0)      # 오른쪽 방향 설정
robot.showturtle()  
robot.pendown()

# 장애물 표시용 터틀
obstacle = turtle.Turtle()
obstacle.hideturtle()
obstacle.penup()
obstacle.color("red")

# 초음파 센서 연결
def connect_sensor(port='COM3'):
    global connection
    try:
        connection = serial.Serial(port, 9600)
        time.sleep(2)
        print("✅ 센서 연결 성공")
        return True
    except:
        print("❌ 센서 연결 실패")
        return False

# 거리 읽기
def read_distance():
    global connection, current_distance
    if connection and connection.in_waiting > 0:
        data = connection.readline().decode().strip()
        try:
            distance = float(data)
            current_distance = distance
            return distance
        except:
            pass
    return None

# read_distance 함수를 0.1초 간격으로 계속 실행
def sensor_loop():
    while True:
        read_distance()
        time.sleep(0.1)

# 로봇 움직임 함수
def move_square():
    global moved_distance

    read_distance()

    if current_distance <= DISTANCE_THRESHOLD:
        print("🛑 장애물 감지: 멈춤")
        obstacle.goto(robot.xcor() + 10, robot.ycor())
        obstacle.dot(10)
        turtle.ontimer(move_square, 300)
        return

    # 한 변을 아직 다 이동하지 않은 경우
    if moved_distance < SIDE_LENGTH:
        robot.forward(MOVE_STEP)
        moved_distance += MOVE_STEP
    else:
        # 방향 전환
        robot.left(90)
        moved_distance = 0

    turtle.ontimer(move_square, 300)
    
# 거북이 이동 함수
def move_robot():
    # 거북이는 계속 이동한다.
    while True:
        # current_distance는 read_distance에서 업데이트 됨
        # DISTANCE_THRESHOLD : 장애물 판단 기준 값
        if current_distance > DISTANCE_THRESHOLD:
            robot.forward(10) # 전진
        else:
            print("🛑 장애물 감지됨, 정지!")
            # 현재 위치 근처에 장애물 표시
            obstacle.goto(robot.xcor() + 15, robot.ycor())
            obstacle.dot(15)
            time.sleep(1)
        time.sleep(0.3)

def main():
    if connect_sensor():
        # 거리 센서 읽기 스레드 시작
        t_sensor = threading.Thread(target=sensor_loop)
        # 데몬 스레드 설정(메인 프로그램 종료시 함께 종료)
        t_sensor.daemon = True
        t_sensor.start()

        # 거북이 움직임 시작
        #move_robot()
        move_square()

if __name__ == "__main__":
    main()
