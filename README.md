# 초음파 거리에 따른 Turtle봇 시뮬레이터
- 초음파 거리센서로부터 실시간 거리 데이터를 수신하여, `turtle` GUI 내에서 장애물을 감지하고 거북이(Turtle)가 멈춤동작을 수행하는 시뮬레이터
- 참고문서 : [HC-SR04 회로연결](https://projecthub.arduino.cc/Isaac100/getting-started-with-the-hc-sr04-ultrasonic-sensor-7cabe1)

---

## 1. MVP(Minimum Viable Product) : 최소기능
- 초음파 거리센서로부터 수신한 거리값에 따라 turtle 그래픽에서 거북이가 전진하다가 장애물을 감지하면 정지한다.
- MVP 기능
  - 센서 연결 및 거리 데이터 수신 (pyserial)
  - 실시간 거리값에 따라 거북이(Turtle)의 움직임 제어
  - 일정 거리 이하에 장애물 감지 시 Turtle 멈춤
  - GUI 내부에서 반복적으로 움직이는 기본 경로(네모 트랙)

---

## 2. 목표

- Turtle 로봇이 사각형 경로를 따라 이동
- 이동 중 초음파 센서가 장애물을 감지하면 멈춤
- GUI를 멈추지 않고 센서 데이터를 실시간으로 반영
- 장애물이 사라지면 자동으로 이동 재개

<img width="400" height="410" alt="image" src="https://github.com/user-attachments/assets/26a4f4b5-6265-4c77-84a8-d840bb82c1d5" />

---
## 3. 동작 설명

### 전체 동작 요약 흐름
```css
[센서] → [거리값 수신] → [current_distance 업데이트] 
              ↓
         [move_square 함수]
              ↓
     ┌─────────────┐
     │ 거리 > 20cm │ → 전진
     │ 거리 ≤ 20cm │ → 멈춤 + 빨간 점 표시
     └─────────────┘
              ↓
   [ontimer(300ms)로 재호출]

```

### 1. 초기 설정
- 거북이 초기값 설정 : 크기, 위치 등
- 장애물 표시값 설정 : 장애물 발생 위치 표시 용도
- 장애물 판단 초음파 센서값 정의 : 20cm

### 2. 센서 연결 및 거리 읽기 루프
- `connect_sensor()`: 지정된 포트(COM3)에 아두이노 초음파 센서를 시리얼 통신으로 연결한다.
- `read_distance()`: 초음파 센서에서 거리를 주기적으로 읽어 `current_distance` 전역 변수에 저장한다. 충돌 없으면 forward(10) 실행

### 3. 거리 읽기 백그라운드 루프 (sensor_loop 스레드)
```python
def sensor_loop():
    while True:
        read_distance()
        time.sleep(0.1)
```

- 역할: 메인 GUI 루프를 방해하지 않고, 초음파 거리 데이터를 지속적으로 읽어오는 백그라운드 루프

### 4. 거북이 이동 알고리즘 (`move_square`)
```python
def move_square():
    ...
    if current_distance <= DISTANCE_THRESHOLD:
        ...
    else:
        ...
```

- 장애물 감지 시 (`current_distance <= DISTANCE_THRESHOLD`)
  - 이동을 멈추고, 현재 위치 근처에 빨간 점(도트)으로 장애물 표시
  - 일정 시간 동안 멈춘 뒤 거북이 이동 함수를 재실행 (`ontimer` 사용)

- 안전한 경우
  - 앞으로 전진(`robot.forward(MOVE_STEP)`)
  - 한 변(`SIDE_LENGTH`, 300픽셀)을 다 이동하면 왼쪽으로 90도 회전
  - 사각형 모양으로 계속 회전하며 장애물이 없을 때만 이동

## 4. 사용 기술

| 분류    | 내용                                 |
| ----- | ---------------------------------- |
| 언어    | Python 3.10.11                         |
| 하드웨어  | Arduino, 초음파 센서(HC-SR04), USB 연결 |
| 라이브러리 | `pyserial`, `turtle`, `threading`,  `time`              |
| 플랫폼   | Windows  |
| 개발환경   | Thonny  |


## 5. 설치 및 실행방법

#### 1. 의존성 설치
```bash
pip install pyserial
```

#### 2. 아두이노 센서 연결
- 아두이노 보드에 초음파 센서를 연결
- 시리얼 통신 속도: 9600bps
- 거리값(cm)을 텍스트 형태로 전송
<img width="500" height="500" alt="image" src="https://github.com/user-attachments/assets/6e8503e3-0b31-4136-b055-c66885d8fe23" />

#### 3. 파이썬 코드 실행
```bash
python move_turtle.py
```
