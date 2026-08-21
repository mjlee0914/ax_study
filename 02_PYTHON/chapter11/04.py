import asyncio

async def work():
    await asyncio.sleep(2) #
    print("작업 완료")

# await work() # 작동 x

asyncio.run(work()) # 이벤트 루프 생성 후 실행
