import os
# 운영체제(OS) 기능을 사용하기 위한 모듈
# 여기서는 환경변수 값을 가져오기 위해 사용

from dotenv import load_dotenv
# .env 파일에 저장된 환경변수를 불러오는 함수

from langchain.chat_models import init_chat_model
# LangChain에서 채팅 모델을 초기화하는 함수


load_dotenv()
# 현재 프로젝트의 .env 파일을 읽어서 환경변수로 등록


config = {
    "model_provider": os.getenv("MODEL_PROVIDER"),
    # .env의 MODEL_PROVIDER 값을 가져옴
    # 예: "openai", "ollama"

    "model": os.getenv("MODEL_NAME")
    # .env의 MODEL_NAME 값을 가져옴
    # 예: "gpt-4o-mini", "llama3.2"
}


api_key = os.getenv("OPENAI_API_KEY")
# .env에서 OPENAI_API_KEY 값을 가져옴
# 값이 없으면 None


if api_key:
    # api_key가 존재하는 경우에만 실행

    config["api_key"] = api_key
    # 기존 config 딕셔너리에
    # "api_key": 실제_API_KEY 값을 추가


def get_model(temperature=0):
    # 모델을 만들어서 반환하는 함수
    # temperature 기본값은 0

    config["temperature"] = temperature
    # config 딕셔너리에 temperature 설정 추가
    # 0에 가까울수록 일관된 답변
    # 높을수록 답변이 다양해짐

    return init_chat_model(**config)
    # config 딕셔너리의 값을 keyword argument로 풀어서 전달
    #
    # 예:
    # config = {
    #     "model_provider": "openai",
    #     "model": "gpt-4o-mini",
    #     "temperature": 0
    # }
    #
    # **config
    # ↓
    # init_chat_model(
    #     model_provider="openai",
    #     model="gpt-4o-mini",
    #     temperature=0
    # )


model = get_model()
# get_model() 함수를 실행해서
# 실제 사용할 LangChain 모델 객체를 model 변수에 저장