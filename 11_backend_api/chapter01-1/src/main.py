# application logging 기록 남기기 -> pirnt x, logging 사용
# 향후 문제 발생시 문제 상황 파악에 사용
import logging 

from fastapi import FastAPI

logging.basicConfig(
    # 출력할 최소 로그 레벨의 하한선을 정함
    level=logging.INFO,
    # 로깅시 날짜와 시간 기록: 로깅에서 정해진 패턴, 문법 x
    format="%(asctime)s [%(levelname)s] (%(name)s) - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

logger = logging.getLogger("app")
"""
로깅 하한선 참고. info일 경우 debug는 출력되지 않음.
.critical(..)
.error(..)
.warning(..)
.info(..)
.debug(..)
"""

app = FastAPI() # 변수명 관례

@app.get("/") # main 경로 
async def hello_world() -> dict:
    # 시스템이 정상적으로 작동됨을 알리는 비즈니스 흐름 기록
    logger.info("이거 뜨면 로깅 연습 성공. hello world")
    return {
        "message":"Hello World"
    }
    