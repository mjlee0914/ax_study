"""
[busniness requirements]
1. 도서 대여점의 도서는 2가지 상태로 관리가 된다. (대출중(RENTED), 대출 가능(AVAILABLE))
2. 대출중인 도서는 대여 불가능
3. 소규모 대여점이므로 도서별 재고는 1개 뿐 -> 도서 재고 관리는 하지 않음.
4. 도서 번호, 제목, 저자의 정보를 확인 가능 (이후 요구사항 추가)
"""
# book.py 역할: 도서 데이터를 관리하고 도서 대여점의 비즈니스 규칙을 지키는 것
from datetime import datetime

class Book:
    def __init__(self, book_id:int, title:str, author:str, status:str):
        self.id = book_id
        self.title = title
        self.author = author
        self.status = status
        self.created_at = datetime.now()

    @classmethod # 정적 접근하여 객체 생성 가능,  Book 객체를 만드는 역할. 
                # 붙이면 객체가 없어도 클래스에서 바로 호출 가능
    def create(self, book_id:int, title:str, author:str, status:str):
        # status = AVALIABLE | RENTED
        if status not in ['AVAILABLE', 'RENTED']:
            raise ValueError("허용되지 않는 도서 상태입니다.")

        # 작가명, 제목이 없을 때 (공백제거시 포함) 에러 raise
        if not title or not title.strip():
            raise ValueError("도서 제목은 필수 항목입니다.")

        if not author or not author.strip():
            raise ValueError("도서 저자는 필수 항목입니다.")

        book = Book(book_id, title, author, status)
        book.created_at = datetime.now()
        
        return book

    def rent(self):
        if self.status != 'AVALIABLE':
            raise ValueError("대출 가능한 도서가 아닙니다.")

        self.status = "RENTED"

    def returnBook(self):
        if self.status != "RENTED":
            raise ValueError("대출 중인 도서가 아닙니다.")

        self.status = "AVAILABLE"

    # 만들어진 Book 객체를 딕셔너리로 바꾸는 역할, FastAPI가 JSON으로 응답
    def to_dict(self) -> dict:
        """
        네트워크로 전송할 수 있도록 도메인 객체를 기본 딕셔너리로 가공합니다.
        """
        return {
            "id": self.id,
            "title": self.title,
            "author": self.author,
            "status": self.status,
            "created_at": self.created_at.isoformat()
        }

    