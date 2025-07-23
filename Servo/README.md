# 서보모터의 신호로 Turtle 제어하기
- 아두이노의 버튼과 서보모터의 신호를 받아 `turtle` GUI 내에서 거북이(Turtle)가 이동하는 시뮬레이터
- 참고문서
  - [서보모터 연결](https://docs.arduino.cc/learn/electronics/servo-motors/)
  - [버튼 연결](https://docs.arduino.cc/built-in-examples/digital/Button/)

---

## 1. MVP(Minimum Viable Product) : 최소기능
- 아두이노에서 동작 수행 후 `serial` 신호를 받아 turtle 그래픽에서 거북이가 전진한다.
- MVP 기능
  - 센서 연결 및 거리 데이터 수신 (pyserial)
  - 거북이(Turtle)의 움직임 제어

---

## 2. 목표

- **아두이노(Arduino)**
  - 버튼을 누르면 서보모터가 2번 회전한다.
  - 동작이 완료되었음을 나타내는 메세지를 `serial`로 전달한다.
- **파이썬(Python)**
  - GUI를 멈추지 않고 serial 데이터를 실시간으로 반영
  - 사용자가 버튼을 누를 때마다 turtle이 전진한다.

<img width="470" height="380" alt="image" src="https://github.com/user-attachments/assets/f3b95285-c419-43e0-b670-9e62dfada079" />


---
## 3. 동작 설명

### 전체 동작 요약 흐름
```css
[버튼] → [서보모터 동작] → [serial 메세지 전달] 
                                ↓
                          [listen_serial 함수]
                                ↓
                           🐢──  → 전진(move_forward)
                                ↓
                          [ontimer(100ms)로 재호출]

```

>
> #### 아두이노(Arduino)
> 1) 버튼, 서보모터와 아두이노를 연결한다.
> 2) 사용자가 버튼을 누르면 서보모터가 2회 작동한다.(버튼 `INPUT_PULLUP` 적용)
> 3) `serial` 통신으로 작동완료 메세지를 전달한다.
> #### 파이썬(Python)
> 1) `listen_serial()`: 아두이노와 시리얼 통신으로 연결하여 신호값을 받는다. (1초마다 재실행)
> 2) `move_forward()`: 신호값으로 `go`를 받으면 거북이가 앞으로 전진한다.

---

## 4. 설치 및 실행방법

#### 1. 의존성 설치
```bash
pip install pyserial
```

#### 2. 아두이노 센서 연결
- 아두이노 보드에 버튼, 서보모터를 연결
- 시리얼 통신 속도: 9600bps
- 서보모터 회로도

  <img width="400" height="442" alt="image" src="https://github.com/user-attachments/assets/57e596a4-ff58-4ef0-b5a3-d19526fa6222" />
- 버튼 회로도

  <img width="400" height="573" alt="image" src="https://github.com/user-attachments/assets/65938f35-5e9b-4cfb-9ad4-ea30d6cc170e" />


#### 3. 아두이노 파일 업로드
#### 4. 파이썬 코드 실행
```bash
python go_turtle.py
```
