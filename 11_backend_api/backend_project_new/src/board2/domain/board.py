# board entity
# 비즈니스 요구사항부터 분석하고, 이를 바탕으로 코드 구성

"""
[비즈니스 요구사항 분석]

1. 게시판은 무한대로 생성 가능하다. 게시판 설정 하나가 게시판 하나가 된다.
2. 게시판은 비회원, 회원, 관리자 모두 사용 가능하다.
3. 비회원, 회원, 관리자의 역할에 따라서 이용 제한을 설정할 수 있다.
4. 권한은 다음과 같다.
    - 게시글 수정 가능 권한(edit_role, editable): 글 쓰기, 글 수정, 글 삭제 가능
    - 게시글 상세 보기 가능 권한(view_role, viewable): 글 상세 열람 가능
    - 게시글 목록 보기 가능 권한(list_role, listable): 글 목록 열람 가능
    - 댓글 목록 보기 가능 권한(comment_list_role, comment_listable): 댓글 목록 열람 가능하다
    - 댓글 수정 가능 권한(comment_edit_role, comment_editable): 댓글 쓰기, 댓글 수정, 댓글 삭제 권한
5. 비회원으로 글 또는 댓글 작성시에는 비밀번호(6자리 이상)를 등록해야 하며, 글 또는 댓글 수정, 삭제시에 작성시에 등록한 비밀번호를 검증해야 한다.
6. 회원 게시글의 경우 직접 글 또는 댓글을 등록한 회원만 수정이 가능하며, 관리자는 상관없이 가능하다.
7. 게시글 목록에서 노출될 게시글 갯수는 설정 가능해야 하며 기본값은 20이다.
8. 게시판 ID는 영문 소문자로 시작, 영문 소문자/숫자/하이픈/언더스코어 허용 (2~30자)
9. 게시판 설정은 소프트 삭제를 하며 삭제된 게시판은 수정할 수 없다.
"""

from dataclasses import dataclass

@dataclass
class Author: # VO - Post context 안에서는 작성자, 밖에서는 그냥 회원
    author_id: str
    author_name: str

# 엔티티 정의시에는 dataclass로 정의하기
# DB나 API프레임워크에 의존하지 않는 순수한 비즈니스 객체를 만들 수 있음
@dataclass
class Post: # Entity
    post_id: int # 게시글 번호
    author: Author # VO 불러오기


