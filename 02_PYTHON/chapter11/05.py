# httpx 실습(chap11-3)

import httpx
import asyncio

async def get_post(num):
    async with httpx.AsyncClient() as client: # with 구문으로 httpx 가져오기, 비동기로 열고 닫을 때 async 붙이기
        url = f"https://jsonplaceholder.typicode.com/posts/{num}" # 작업할 url 지정하기, num은 포스트 넘버

        res = await client.get(url) # 제어권 가져가므로 await 붙이기, 작업할 url 불러오기
        result = res.json() # json화 시킨 result 지정

        return result['id'], result['title'] # result에서 id, title만 지정



# tuple (1~10까지 차례대로)
# async def main():
#     for i in range(1, 11):
#         result = await get_post(i)
#         print(result)


# 10개를 한꺼번에 리스트로 받아오기
async def main():
    get_posts = [get_post(i) for i in range(1, 11)] # list comprehension

    results = await asyncio.gather(*get_posts)
    print(results)


asyncio.run(main())
