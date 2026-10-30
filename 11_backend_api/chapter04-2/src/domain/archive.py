import datetime


class MultimediaAsset:
    """
    저장소에 보관될 개별 미디어 파일의 정보를 담는 객체입니다.
    데이터에 오류가 없는지 스스로 검사하고 상태를 변경합니다.
    """

    def __init__(
        self,
        asset_id: int,
        filename: str,
        file_size: int,
        content_type: str,
        status: str = "PENDING",
    ):
        if not filename or not filename.strip():
            raise ValueError("파일 이름은 공백일 수 없습니다.")

        if file_size <= 0:
            raise ValueError("파일의 크기는 반드시 0바이트보다 커야 합니다.")

        self.id = asset_id
        self.filename = filename.strip()
        self.file_size = file_size
        self.content_type = content_type
        self.status = status
        self.created_at = datetime.datetime.now()

    def mark_as_processing(self) -> None:
        """상태를 대기 중에서 처리 중으로 변경합니다."""
        if self.status != "PENDING":
            raise ValueError(
                "대기 상태(PENDING)일 때만 처리 단계로 진입할 수 있습니다."
            )

        self.status = "PROCESSING"

    def mark_as_completed(self) -> None:
        """상태를 처리 중에서 완료로 변경합니다."""
        if self.status != "PROCESSING":
            raise ValueError(
                "처리 상태(PROCESSING)일 때만 완료할 수 있습니다."
            )

        self.status = "COMPLETED"

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "filename": self.filename,
            "file_size": self.file_size,
            "content_type": self.content_type,
            "status": self.status,
            "created_at": self.created_at.isoformat(),
        }