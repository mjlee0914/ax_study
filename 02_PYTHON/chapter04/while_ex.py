while True: #무한 루프
    print("아무 메시지 입력 (q - 종료)", end="")
    message = input()

    if message == "q":
        print("종료합니다.")
        break

    print("입력 메시지:", message)
    
