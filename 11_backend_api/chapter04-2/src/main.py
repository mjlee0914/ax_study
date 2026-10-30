import os
# 파일명 추출과 오류 발생 시 파일 삭제에 사용
# os.path.basename(), os.remove()

import logging
import asyncio
from typing import Annotated, AsyncGenerator
# 타입에 FastAPI용 추가 정보를 붙이는 문법

from pathlib import Path
# 파일과 디렉터리 경로를 객체로 다루는 클래스

from fastapi import (
    FastAPI,        
    UploadFile,     # 사용자가 업로드한 파일을 나타내는 타입
    File,           # 요청값을 업로드 파일로 받도록 지정
    HTTPException,  
    status,
    BackgroundTasks        
)
from fastapi.responses import StreamingResponse # 서버에 저장된 파일을 HTTP 응답으로 반환
import aiofiles # 파일을 async/await 방식으로 저장
from domain.archive import MultimediaAsset # 업로드된 미디어 자산의 데이터와 상태를 관리
from schemas.archive import AssetResponseSchema # 파일 업로드 성공 응답의 데이터 형식

logging.basicConfig(
    level=logging.INFO
)

logger = logging.getLogger(
    "aiofiles" # 로거 구분하는 이름
)

app = FastAPI(
    title="aiofiles practice"
)


MEDIA_STORAGE_DIR = Path(
    "storage/image" # 업로드된 파일이 실제로 저장될 폴더
)

MEDIA_STORAGE_DIR.mkdir(
    parents=True,
    # 부모 폴더인 storage가 없어도 함께 생성

    exist_ok=True,
    # 폴더가 이미 존재해도 오류를 발생시키지 않음
)


asset_repository: dict[int, MultimediaAsset] = {}
# 데이터베이스 대신 사용하는 메모리 저장소
#
# 예:
# {
#     1: MultimediaAsset 객체,
#     2: MultimediaAsset 객체,
# }

asset_id_sequence = 1
# 다음 업로드 파일에 부여할 ID
# 서버가 재시작되면 다시 1로 초기화

@app.post(
    "/assets",
    response_model=AssetResponseSchema, # 반환값을 AssetResponseSchema 형식으로 검증
    status_code=status.HTTP_201_CREATED, # 정상적으로 생성되면 HTTP 201 반환
)
async def upload_asset(
    file: Annotated[
        UploadFile,
        # file 변수의 실제 Python 타입
        File(description="업로드 파일"),
        # FastAPI에 multipart/form-data 파일이라고 알려줌
    ],
):
    global asset_id_sequence
    # 함수 밖의 ID 값을 읽고 변경하겠다는 선언

    logger.info(f"업로드 파일 정보: {file}")
    # 파일명, 파일 크기, MIME 타입 등을 터미널에 기록

    raw_filename = os.path.basename(file.filename or "unknown")
    # 경로가 포함된 파일명에서 순수 파일명만 추출
    # 예:
    # "../../photo.jpg" → "photo.jpg"

    physical_target_path = (
        MEDIA_STORAGE_DIR
        / f"seq_{asset_id_sequence}_{raw_filename}"
    )
    # 실제 저장 경로 생성
    # 예:
    # storage/image/seq_1_photo.jpg

    try:
        async with aiofiles.open(
            physical_target_path,
            "wb", # 실제 저장 경로에 바이너리 쓰기 모드로 파일 열기
        ) as local_disk_file:
            while True:
                binary_chunk = await file.read(1024 * 1024 * 5)
                # 업로드 파일을 최대 5MB씩 읽음: 큰 파일 전체를 한꺼번에 메모리에 올리지 않음
                if not binary_chunk:
                    # 더 읽을 데이터가 없으면 반복 종료
                    break
                await local_disk_file.write(binary_chunk)
                # 읽은 데이터를 실제 디스크 파일에 기록

        await file.close()
        # async with가 끝나면 자동으로 파일을 닫음
        # FastAPI가 전달한 UploadFile 자원을 닫음

        new_asset = MultimediaAsset(
            asset_id=asset_id_sequence,
            # 현재 ID를 자산 ID로 사용
            filename=raw_filename,
            # 사용자가 업로드한 원본 파일명 저장
            file_size=physical_target_path.stat().st_size,
            # 디스크에 저장된 파일의 실제 크기 조회
            content_type=(
                file.content_type or "application/octet-stream"
            ),
            # image/jpeg 같은 MIME 타입 저장
            # MIME 타입이 없으면 일반 바이너리 타입 사용
        )

        asset_repository[asset_id_sequence] = new_asset
        # 메모리 저장소에 자산 객체 저장
        # 예:
        # asset_repository[1] = new_asset

        asset_id_sequence += 1
        # 다음 파일을 위해 ID 증가
        # 1 → 2

        return new_asset.to_dict()
        # 자산 객체를 딕셔너리로 변환하여 반환
        # AssetResponseSchema 검증 후 JSON 응답


    except Exception as err:
        # 파일 저장이나 자산 생성 중 발생한 오류 처리

        if physical_target_path.exists():
            # 오류가 났지만 파일이 만들어졌다면

            os.remove(physical_target_path)
            # 불완전하게 저장된 파일 삭제

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            # HTTP 500 응답

            detail=f"파일 업로드 실패: {err}",
            # 실제 오류 내용
        )

async def get_file_chunk(file_path:Path, chunk_size:int =1024 * 1024) -> AsyncGenerator[bytes, None]:
    async with aiofiles.open(file_path, "rb") as out_file:
        while True:
            chunk = await out_file.read(chunk_size) # 1MB씩 끊어서 가져온다
            if not chunk:
                break
            yield chunk

# asset 다운
@app.get("/assets/{asset_id}/download")
async def file_download(asset_id: int):
    asset=asset_repository.get(asset_id)
    if not asset:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일을 찾을 수 없습니다"
        )

    physical_target_path = MEDIA_STORAGE_DIR / f"seq_{asset_id}_{asset.filename}"

    if not physical_target_path.exists():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="파일을 찾을 수 없습니다"
        )

    headers = {
        "Content-Disposition": f'attachment; filename="{asset.filename}"', # content 출력 방향 
        "Content-Length":str(asset.file_size),
        "Cache-Control": "no-cache"
    }

    return StreamingResponse(
        get_file_chunk(physical_target_path),
        media_type=asset.content_type,
        headers=headers
    )

async def send_email(email:str):
    await asyncio.sleep(3)
    logger.info("회원가입 안내 메일 전송 완료...")


@app.get("/signup")
async def signup_done(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email, "test@test.org")
    return {"message": "회원가입이 완료 되었습니다."}



# @app.get("/assets/{asset_id}/image")
# # GET /assets/1/image처럼 자산 ID로 이미지 요청
# async def get_asset_image(
#     asset_id: int,
#     # URL의 {asset_id} 값을 정수로 받음
#     #
#     # GET /assets/3/image
#     # → asset_id = 3
# ):
#     asset = asset_repository.get(asset_id)
#     # 메모리 저장소에서 ID에 해당하는 자산 조회
#     #
#     # 존재하면 MultimediaAsset 객체
#     # 존재하지 않으면 None


#     if asset is None:
#         # 해당 ID의 자산 정보가 메모리에 없으면

#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             # HTTP 404 Not Found 반환

#             detail="미디어 자산을 찾을 수 없습니다.",
#             # 클라이언트에게 전달할 오류 내용
#         )


#     physical_filename = f"seq_{asset.id}_{asset.filename}"
#     # 업로드할 때 만든 실제 파일명을 다시 조합
#     #
#     # asset.id = 1
#     # asset.filename = photo.jpg
#     #
#     # 결과:
#     # seq_1_photo.jpg


#     physical_path = MEDIA_STORAGE_DIR / physical_filename
#     # 저장 폴더와 실제 파일명을 결합
#     #
#     # 결과:
#     # storage/image/seq_1_photo.jpg


#     if not physical_path.exists():
#         # 자산 정보는 메모리에 있지만
#         # 실제 디스크 파일이 존재하지 않으면

#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND,
#             detail="저장된 이미지 파일을 찾을 수 없습니다.",
#         )


#     return FileResponse(
#         path=physical_path,
#         # 클라이언트에게 전송할 실제 파일 경로

#         media_type=asset.content_type,
#         # 브라우저가 파일 종류를 알 수 있도록 MIME 타입 지정
#         #
#         # 예:
#         # image/jpeg
#         # image/png

#         filename=asset.filename,
#         # 응답 파일명 지정
#         # 이 값을 지정하면 브라우저가 다운로드 파일로 처리할 수 있음
#     )