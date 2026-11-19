import csv


def try_read_file(file_path, encodings=('utf-8', 'euc-kr')):
    """CSV 형식 텍스트 파일을 주어진 인코딩 순서대로 시도하여 읽는다."""
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return list(csv.reader(file))
        except UnicodeDecodeError:
            continue
    raise ValueError(f"파일 인코딩을 판별할 수 없습니다: {file_path} (시도: {', '.join(encodings)})")
