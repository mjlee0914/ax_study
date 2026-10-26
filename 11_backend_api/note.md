# FastAPI 기초 학습 노트

> 목표: FastAPI, Uvicorn, 비동기 처리, 로깅, `uv`의 역할을 이해하고 직접 서버를 실행할 수 있다.

## 0. 먼저 기억할 핵심

이름이 비슷하지만 서로 다른 도구다.

| 도구        | 역할                                                    | 쉬운 비유                           |
| ----------- | ------------------------------------------------------- | ----------------------------------- |
| **FastAPI** | API의 주소와 처리 방법을 작성하는 Python web 프레임워크 | 주문 처리 규칙                      |
| **Uvicorn** | FastAPI 앱을 실행하고 요청을 받는 ASGI 서버             | 손님의 주문을 받는 직원             |
| **uv**      | Python 프로젝트, 가상환경, 라이브러리를 관리하는 도구   | 프로젝트 관리 도구 (`npm`과 비슷함) |

전체 흐름은 다음과 같다.

```text
브라우저가 요청함
      ↓
Uvicorn이 요청을 받음
      ↓
FastAPI가 알맞은 함수를 실행함
      ↓
FastAPI가 결과를 JSON으로 응답함
```

---

## 1. FastAPI란?

FastAPI는 Python으로 **백엔드 API 서버**를 만들 때 사용하는 프레임워크다.

예를 들어 브라우저가 서버에 상품 목록을 요청하면 FastAPI는 다음 작업을 수행한다.

```text
브라우저: "상품 목록을 주세요."
FastAPI: 요청 주소를 확인함
FastAPI: 해당 Python 함수를 실행함
FastAPI: 실행 결과를 브라우저에 응답함
```

### 첫 번째 FastAPI 코드

```python
import logging
from fastapi import FastAPI

# 로그의 최소 레벨과 출력 형식을 설정한다.
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

# "app"이라는 이름의 로거를 만든다.
logger = logging.getLogger("app")

# FastAPI 애플리케이션을 만든다.
app = FastAPI()


# GET / 요청을 처리할 함수를 연결한다.
@app.get("/")
async def hello_world() -> dict:
    logger.info("Hello World 요청을 받았습니다.")

    return {
        "message": "Hello World",
    }
```

### 코드 실행 흐름

```text
브라우저가 GET / 요청
        ↓
@app.get("/")가 요청을 발견
        ↓
hello_world() 함수 실행
        ↓
Python 딕셔너리 반환
        ↓
FastAPI가 JSON으로 변환하여 응답
```

```python
app = FastAPI()
```

- FastAPI 애플리케이션 객체를 만든다.
- 아래의 주소와 함수들은 이 `app`에 등록된다.

```python
@app.get("/")
```

- `/` 주소로 들어오는 `GET` 요청을 바로 아래 함수와 연결한다.
- 이러한 주소를 **엔드포인트(endpoint)**라고 한다.

```python
async def hello_world() -> dict:
```

- 요청이 들어왔을 때 실행할 비동기 함수다.
- `-> dict`는 이 함수가 딕셔너리를 반환한다는 타입 힌트다.

---

## 2. Uvicorn이란?

FastAPI는 요청을 어떻게 처리할지 정하지만, 혼자서 네트워크 요청을 기다리지는 못한다.  
**Uvicorn**이 서버를 실행하고 브라우저의 요청을 실제로 받아 FastAPI에 전달한다.

### 서버 실행 명령어

```bash
uv run uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

| 명령어             | 의미                                                |
| ------------------ | --------------------------------------------------- |
| `uv run`           | 현재 프로젝트의 가상환경에서 명령어를 실행한다.     |
| `uvicorn`          | Uvicorn 서버를 실행한다.                            |
| `main:app`         | `main.py` 파일 안의 `app` 객체를 사용한다.          |
| `--reload`         | 코드가 변경되면 개발 서버를 자동으로 다시 시작한다. |
| `--host 127.0.0.1` | 내 컴퓨터에서 요청을 받는다.                        |
| `--port 8000`      | 8000번 포트를 사용한다.                             |

`main:app`은 다음처럼 읽는다.

```text
main : app
  ↓     ↓
main.py 파일의 app 변수
```

서버를 실행한 후 다음 주소로 접속한다.

```text
http://localhost:8000
```

또는:

```text
http://127.0.0.1:8000
```

### localhost, IP, Port

```text
http://127.0.0.1:8000
└─규칙─┘ └─주소─┘ └포트┘
```

- `localhost`: 내 컴퓨터를 가리키는 이름
- `127.0.0.1`: 내 컴퓨터를 가리키는 IP 주소
- `8000`: 서버 프로그램이 사용하는 출입문 번호

일반적인 로컬 개발에서는 `localhost`와 `127.0.0.1`이 같은 컴퓨터를 가리킨다.

> `--reload`는 개발용 옵션이다. 배포 환경에서는 사용하지 않는다.

---

## 3. 동기와 비동기

### 동기 방식

한 작업이 끝날 때까지 기다린 다음 다음 작업을 처리하는 방식이다.

```text
물을 올림
→ 물이 끓을 때까지 아무것도 하지 않고 기다림
→ 라면을 넣음
```

서버에서도 한 요청이 외부 결과를 기다리는 동안 다른 일을 하지 못하면 시간이 낭비될 수 있다.

### 비동기 방식

한 작업의 결과를 기다리는 동안 다른 작업을 처리하는 방식이다.

```text
물을 올림
→ 물이 끓는 동안 파를 썰음
→ 물이 끓으면 다시 라면을 넣음
```

서버에서는 다음과 같이 작동할 수 있다.

```text
요청 A: DB 조회 시작 → 결과를 기다림
요청 B: A가 기다리는 동안 처리
요청 C: 다른 작업을 기다리는 동안 처리
요청 A: DB 결과 도착 → 나머지 작업 처리
```

여러 작업을 같은 순간에 계산하는 것과는 다르다. 기다리는 시간을 활용해 작업을 빠르게 번갈아 처리하는 **동시성**이다.

### Blocking과 Non-blocking

- **Blocking**: 작업이 끝날 때까지 실행 흐름을 막고 기다림
- **Non-blocking**: 기다리는 동안 다른 작업을 처리할 수 있음

---

## 4. I/O Bound와 CPU Bound

### I/O Bound

- 연산량은 비교적 적다.
- 외부 작업의 결과를 기다리는 시간이 길다.
- 비동기 처리에 적합하다.

예:

- 데이터베이스 조회
- 외부 API 요청
- 네트워크 통신
- 파일 읽기

```text
계산: ██
대기: ███████████████
```

### CPU Bound

- 기다리는 시간보다 CPU가 직접 계산하는 시간이 길다.
- `async`를 사용한다고 자동으로 빨라지지 않는다.

예:

- 큰 이미지 처리
- 동영상 변환
- 복잡한 수학 계산
- 머신러닝 모델 실행

```text
계산: ███████████████
대기: ██
```

| 구분               | I/O Bound               | CPU Bound                 |
| ------------------ | ----------------------- | ------------------------- |
| 시간이 걸리는 이유 | 외부 결과를 기다림      | 계산량이 많음             |
| 대표적인 예        | DB, API, 네트워크, 파일 | 이미지, 영상, 복잡한 계산 |
| `async`의 효과     | 큼                      | 거의 없음                 |

> **I/O Bound = 기다리는 일이 많음**  
> **CPU Bound = 계산할 일이 많음**

---

## 5. `async`, `await`, Coroutine, Event Loop

### `async def`

잠시 멈췄다가 나중에 이어서 실행할 수 있는 비동기 함수를 선언한다.

```python
async def get_products():
    ...
```

`async`만 붙인다고 모든 코드가 자동으로 빨라지는 것은 아니다. 기다리는 작업이 비동기를 지원해야 효과가 있다.

### `await`

비동기 I/O 작업의 결과를 기다릴 때 사용한다.

```python
async def get_products():
    products = await database.get_products()
    return products
```

`await`의 뜻:

> 이 결과는 기다려야 하지만, 기다리는 동안 다른 작업을 먼저 처리해도 된다.

### Coroutine

`async def` 함수를 호출했을 때 만들어지는, **중간에 멈췄다가 다시 실행할 수 있는 작업**이다.

### Event Loop

어떤 코루틴을 실행하고, 멈추고, 다시 시작할지 관리하는 교통정리 담당자다.

```text
요청 A 실행
→ A가 DB 결과를 기다림
→ 요청 B 실행
→ B가 API 결과를 기다림
→ 요청 C 실행
→ A의 결과 도착
→ 요청 A를 이어서 실행
```

### 핵심 용어 정리

```text
async def = 비동기 함수를 선언
await     = 기다리는 동안 실행 차례를 넘김
Coroutine = 멈추고 재개할 수 있는 작업
Event Loop = 작업 순서를 관리하는 담당자
```

---

## 6. WSGI와 ASGI

WSGI와 ASGI는 Python 웹 서버와 Python 웹 애플리케이션이 서로 대화하는 방법을 정한 **규칙**이다.

### WSGI

- 전통적인 동기 Python 웹 애플리케이션을 위한 규격이다.
- 오래 기다리는 요청이 많으면 처리 자원이 대기 상태로 묶일 수 있다.

```text
웹 서버 ↔ WSGI 규칙 ↔ Python 웹 앱
```

### ASGI

- 비동기 처리를 지원하는 Python 웹 애플리케이션 규격이다.
- HTTP 동시 요청이나 WebSocket 같은 통신을 효율적으로 처리할 수 있다.
- FastAPI와 Uvicorn이 ASGI 규격을 사용한다.

```text
Uvicorn ↔ ASGI 규칙 ↔ FastAPI
```

> WSGI가 항상 정확히 "요청 하나당 스레드 하나"를 사용한다는 뜻은 아니다. 실제 실행 구조는 사용하는 서버 설정에 따라 달라진다. 핵심은 **WSGI는 동기 중심, ASGI는 비동기까지 지원**한다는 점이다.

---

## 7. FastAPI의 `async def`와 `def`

FastAPI에서는 두 종류의 함수를 모두 사용할 수 있다.

```python
@app.get("/products")
async def get_products():
    ...
```

```python
@app.get("/images")
def get_images():
    ...
```

- 비동기를 지원하는 DB 또는 HTTP 라이브러리를 사용하면 주로 `async def`를 사용한다.
- 블로킹 방식의 라이브러리를 호출한다면 일반 `def`를 사용할 수 있다.
- FastAPI는 일반 `def` 엔드포인트를 별도의 스레드 풀에서 실행한다.

주의할 점:

- 아주 무거운 CPU 작업은 `def`로 바꾼다고 해결되지 않는다.
- 그런 작업은 별도 프로세스나 작업 큐가 필요할 수 있다.

---

## 8. Thread와 Call Stack

주방에 비유하면 다음과 같다.

| 컴퓨터 용어 | 주방 비유   | 의미                                         |
| ----------- | ----------- | -------------------------------------------- |
| Thread      | 요리사      | 실제로 명령을 실행하는 일꾼                  |
| Function    | 레시피      | 실행할 작업의 절차                           |
| Computation | 조리 과정   | 실제 계산 또는 처리                          |
| Call Stack  | 개인 조리대 | 함수의 변수와 실행 위치를 임시 보관하는 공간 |

비동기 방식에서는 한 요리사가 오븐 앞에서 계속 기다리지 않는다.

```text
빵을 오븐에 넣음
→ 기다리는 동안 샐러드를 만듦
→ 빵이 다 구워지면 다시 돌아옴
```

이 요리사가 어떤 작업으로 이동할지 정리하는 역할이 이벤트 루프다.

---

## 9. Logging

로그는 서버에 무슨 일이 있었는지 남기는 **일기 또는 블랙박스**다.

`print()`도 문자를 출력하지만, 로그는 중요도, 시간, 발생 위치 등을 정해진 형식으로 기록하고 필터링할 수 있다.

### 로그 레벨

```text
DEBUG → INFO → WARNING → ERROR → CRITICAL
```

| 레벨       | 사용 시점                          | 예시                          |
| ---------- | ---------------------------------- | ----------------------------- |
| `DEBUG`    | 개발 중 자세한 확인                | 변수 값, SQL 쿼리 확인        |
| `INFO`     | 정상적인 작동 기록                 | 서버 시작, 요청 처리 완료     |
| `WARNING`  | 작동은 하지만 주의가 필요함        | 응답 지연, 만료 임박          |
| `ERROR`    | 특정 기능이 실패함                 | API 요청 실패, 파일 저장 실패 |
| `CRITICAL` | 시스템 전체에 치명적인 문제가 있음 | DB 연결 불가, 메모리 부족     |

### 기본 설정

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] (%(name)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
```

`level=logging.INFO`는 `INFO` 이상의 로그만 출력한다는 뜻이다.

```text
DEBUG       출력하지 않음
INFO        출력함
WARNING     출력함
ERROR       출력함
CRITICAL    출력함
```

### 로그 포맷

| 포맷            | 의미                   |
| --------------- | ---------------------- |
| `%(asctime)s`   | 로그가 발생한 시간     |
| `%(levelname)s` | 로그 레벨              |
| `%(name)s`      | 로거의 이름            |
| `%(message)s`   | 개발자가 작성한 메시지 |
| `%(filename)s`  | 로그가 발생한 파일명   |
| `%(funcName)s`  | 로그가 발생한 함수명   |
| `%(lineno)d`    | 로그가 발생한 줄 번호  |

예상 출력:

```text
2026-10-26 14:30:10 [INFO] (app) - Hello World 요청을 받았습니다.
```

### 로깅 설정을 분리하는 이유

프로젝트가 커지면 `logger.py` 같은 별도 파일에서 로그 설정을 관리할 수 있다.

- 모든 파일이 같은 로그 형식을 사용한다.
- 개발 환경과 배포 환경의 로그 레벨을 다르게 설정하기 쉽다.
- API 처리 코드와 시스템 설정 코드가 섞이지 않는다.

---

## 10. `uv`와 가상환경

`uv`는 Python 프로젝트와 패키지를 관리하는 도구다. JavaScript의 `npm`과 비슷한 역할을 한다.

```text
npm install react
uv add fastapi
```

### 프로젝트 만들기

```bash
uv init chapter01 --python 3.13
cd chapter01
```

- `chapter01`이라는 프로젝트를 만든다.
- Python 3.13을 사용하도록 설정한다.

### 라이브러리 설치하기

```bash
uv add fastapi uvicorn
```

- FastAPI와 Uvicorn을 프로젝트에 추가한다.
- 필요한 의존성을 계산하고 설치한다.
- 설치 버전을 프로젝트 파일과 락파일에 기록한다.

### `.venv`

현재 프로젝트만 사용하는 독립적인 Python 환경이다.

```text
프로젝트 A의 라이브러리
프로젝트 B의 라이브러리
```

프로젝트마다 가상환경을 사용하면 서로 다른 라이브러리와 버전이 섞이지 않는다.

### `uv.lock`

프로젝트에서 사용하는 라이브러리의 **정확한 버전**을 기록한다. 다른 컴퓨터에서도 같은 의존성 구성을 재현하는 데 도움을 준다.

### 캐시와 하드링크

- 한 번 다운로드한 패키지를 전역 캐시에 보관한다.
- 다른 프로젝트에서 같은 패키지가 필요하면 캐시를 재사용한다.
- 가능한 경우 파일을 다시 복사하지 않고 하드링크로 연결한다.
- 따라서 설치 시간과 디스크 사용량을 줄일 수 있다.

---

## 11. 처음부터 실행하기

```bash
# 1. Python 프로젝트 생성
uv init chapter01 --python 3.13

# 2. 생성된 프로젝트 폴더로 이동
cd chapter01

# 3. FastAPI와 Uvicorn 설치
uv add fastapi uvicorn

# 4. main.py 작성 후 개발 서버 실행
uv run uvicorn main:app --reload
```

브라우저에서 접속:

```text
http://localhost:8000
```

FastAPI가 자동으로 만들어주는 API 문서:

```text
http://localhost:8000/docs
```

---

## 12. 전체 요청 처리 과정

```text
① uv로 프로젝트와 라이브러리를 관리함
                  ↓
② Uvicorn으로 서버를 실행함
                  ↓
③ 브라우저가 localhost:8000으로 요청함
                  ↓
④ Uvicorn이 네트워크 요청을 받음
                  ↓
⑤ ASGI 규칙을 통해 FastAPI에 전달함
                  ↓
⑥ FastAPI가 주소와 HTTP 메서드에 맞는 함수를 실행함
                  ↓
⑦ Python 딕셔너리를 JSON으로 변환함
                  ↓
⑧ 브라우저에 응답함
                  ↓
⑨ 처리 과정은 logger를 통해 기록할 수 있음
```

---

## 13. 자주 헷갈리는 부분

### `uv`와 Uvicorn은 같은 도구인가?

아니다.

- `uv`: 프로젝트와 라이브러리 관리
- Uvicorn: 웹 서버 실행

### `async`를 붙이면 모든 코드가 빨라지는가?

아니다. DB 조회나 네트워크 요청처럼 기다리는 작업에서 주로 효과가 있다. CPU 계산이 많은 작업은 `async`만으로 빨라지지 않는다.

### 비동기는 여러 작업을 완전히 동시에 계산하는 것인가?

반드시 그런 것은 아니다. 한 작업이 기다리는 동안 다른 작업으로 빠르게 이동하여 시간을 효율적으로 사용하는 방식이다.

### FastAPI와 Uvicorn 중 누가 요청을 받는가?

- Uvicorn이 네트워크 요청을 받는다.
- FastAPI가 요청에 맞는 Python 함수를 찾아 실행한다.

### `localhost`는 인터넷 주소인가?

내 컴퓨터 자신을 가리키는 특별한 주소다. 다른 사람의 컴퓨터에서 내 `localhost`로 접속할 수는 없다.

---

## 14. 복습 문제

### Q1. FastAPI, Uvicorn, uv의 역할은 각각 무엇인가?

<details>
<summary>정답 보기</summary>

- FastAPI: API 주소와 처리 로직 작성
- Uvicorn: FastAPI 앱을 실행하고 네트워크 요청 수신
- uv: Python 프로젝트, 가상환경, 라이브러리 관리

</details>

### Q2. I/O Bound 작업의 예시를 두 가지 말해보자.

<details>
<summary>정답 보기</summary>

데이터베이스 조회, 외부 API 요청, 네트워크 통신, 파일 읽기 등이 있다.

</details>

### Q3. `await`를 만나면 어떤 일이 일어나는가?

<details>
<summary>정답 보기</summary>

해당 I/O 결과를 기다리는 동안 이벤트 루프에 실행 차례를 넘겨서 다른 작업을 처리할 수 있게 한다.

</details>

### Q4. CPU Bound 작업에 `async`만 붙이면 빨라지는가?

<details>
<summary>정답 보기</summary>

아니다. CPU가 계속 계산해야 하므로 `async`만으로는 해결되지 않는다.

</details>

### Q5. 다음 명령어의 `main:app`은 무엇을 의미하는가?

```bash
uv run uvicorn main:app --reload
```

<details>
<summary>정답 보기</summary>

`main.py` 파일 안의 `app` 객체를 찾아 실행하라는 의미다.

</details>

---

> **Uvicorn이 요청을 받고, FastAPI가 요청을 처리하며, `async`와 `await`는 외부 결과를 기다리는 동안 다른 요청을 처리할 수 있게 해준다.**

---

http://localhost:8000 = http://127.0.0.1:8000

---

REST(Representational State Transfer): 표현적 상태 전이

표현적:

- URI(Uniform Resource Identifier): 자원을 식별(명사)
  - uniform: 통일된 형식을 사용함(URI라는 공통 형식)
  - ex) 전화번호 사람마다 다름 but +82-10-1234-5678의 공통 규칙을 따름

```
https://example.com:443/boards/1?sort=recent#comments
```

```
https       → scheme: 어떤 통신 방식을 사용할지
example.com → host: 어느 서버인지
443         → port: 어느 출입문인지
/boards/1   → path: 어떤 자원인지
sort=recent → query: 추가 조건
comments    → fragment: 문서 내부의 특정 위치
```

- resource: 식별하려는 자원
- identifier: 자원을 구별하는 식별자
- URL: 위치를 이용해 자원을 식별. URI가 더 큰 개념

상태:

- 요청 메서드 (GET, PUT, PATCH, ...) (동사)

```
REST API

GET  /boards/1
POST /boards

/boards/1 → 자원, 즉 명사
GET       → 조회 행동
POST      → 생성 행동
```

---

멱등성: 동일한 요청을 여러번 했을 때 동일한 결과를 받는 것을 보장
PATCH보다는 PUT 추천

---

Backend Project와 Domain

Backend Architecture

- 아키텍처는 코드의 역할을 나누고 연결하는 구조이다.
- 프로젝트가 커져도 코드를 쉽게 이해하고 수정할 수 있게 해준다.
- 비즈니스 로직, API 처리, DB 접근 등의 책임을 분리한다.
- 목적은 복잡한 구조를 만드는 것이 아니라 요구사항의 변경을 안전하게 반영하는 것이다.

Domain

Domain은 소프트웨어가 해결하려는 업무 분야와 그 분야의 지식이다.

```
예:

- 쇼핑몰: 상품, 장바구니, 주문, 결제, 배송
- 은행: 계좌, 입금, 출금, 대출
- 병원: 환자, 예약, 진료, 처방
```

코딩 지식과 도메인 지식은 서로 다르다.

- 코딩 지식: 요구사항을 프로그램으로 구현하는 방법
- 도메인 지식: 무엇을 구현하고 어떤 업무 규칙을 지켜야 하는지

Business Requirement

회사가 소프트웨어를 통해 해결하려는 요구사항이다.

```
예:

- 고객은 재고가 있는 상품만 주문할 수 있다.
- 결제가 완료되면 주문 상태가 변경된다.
- 배송을 시작한 주문은 취소할 수 없다.
```

개발자는 비즈니스 요구사항과 규칙을 코드로 구현한다.

Domain Model

도메인의 중요한 개념을 코드로 표현한 모델이다.

다음 내용을 포함할 수 있다.

- 데이터
- 행동
- 비즈니스 규칙
- 다른 개념과의 관계

예:

- Order의 데이터: 주문 상태, 주문 상품
- Order의 행동: 주문, 결제, 취소
- Order의 규칙: 배송을 시작한 주문은 취소할 수 없음

Domain Analysis

비즈니스 요구사항을 분석하여 다음을 찾는 과정이다.

```
1. 주요 도메인 개념을 찾는다.
2. 각 개념의 데이터와 행동을 찾는다.
3. 비즈니스 규칙을 찾는다.
4. 개념 사이의 관계를 찾는다.
5. 이를 모델과 코드로 설계한다.
```

Ubiquitous Language

기획자, 도메인 전문가, 개발자가 동일한 도메인 용어를 사용하는 것이다.

도메인 용어를 클래스, 함수, 변수 이름에도 일관되게 사용한다.

```python
order.cancel()
payment.refund()
product.decrease_stock()
shipment.start_delivery()
```

---

chapter01-2/src/book/domain/

---

FastAPI 데이터 처리 삼총사 (Body, Query, Field)

Body(...)

- 요청의 "본문(Payload)"에서 데이터를 꺼내옴
- request body data (POST, PUT, PATCH, ...) 전달받을 때
- Content-Type: application/json

Form(...)

- 일반 양식 application/x-www-form-urlencoded: 이름=값&이름=값 형태의 폼 데이터 가져올 때

Query(...)

- 쿼리스트링 값 - CURL에 포함된(주소창 맨 뒤의) `? 이름=값` 가져올 때
- 주소창 맨 뒤의 "물음표 뒤(?status=AVAILABLE)"에 붙는 쿼리 스트링에서 데이터를 꺼내올 때

Field(...)

- 데이터 모델 스키마 내부의 개별 속성을 검증하고 설명할 때 사용

---

curl ( cleint url)

```
curl -i -X POST "http://127.0.0.1:8000/books" \
     -H "Content-Type: application/json" \
     -d '{"title": "쉽게 배우는 파이썬 백엔드", "author": "스파르타 튜터"}'
```

- -i: 자세한정보
- -X: 요청 메서드
- -H: 요청 헤더
- -d: 요청 본문에 담을 데이터

---

book.py와 main.py의 연결관계

```
main.py  ─── 사용함 ───▶  book.py
FastAPI 영역               도메인 영역
```

- main.py : 웹 요청과 응답 담당
- book.py : 도서 데이터와 비즈니스 규칙 담당

```
전체 연결 구조
클라이언트
    │
    │ POST /books
    ▼
Uvicorn
    ▼
FastAPI app
    ▼
main.py의 create_book()
    │
    │ Book.create(...)
    ▼
book.py의 Book 클래스
    │
    ├── 제목 검사
    ├── 저자 검사
    ├── 상태 검사
    └── Book 객체 생성
    │
    ▼
main.py로 결과 반환
    ▼
FastAPI가 JSON 응답
    ▼
클라이언트
```

FastAPI를 붙인 핵심 이유:
브라우저의 HTTP 요청을 main.py의 Python 함수와 연결하고, 함수의 결과를 HTTP·JSON 응답으로 돌려주기 위해서입니다.

```
main.py = 외부 요청과 응답을 담당하는 입구
book.py = 도서의 데이터와 업무 규칙을 담당
FastAPI = HTTP 요청과 Python 함수를 연결
Uvicorn = 네트워크에서 서버를 실제로 실행
```
