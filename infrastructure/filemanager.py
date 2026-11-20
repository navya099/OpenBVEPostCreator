# infrastructure/filemanager.py
import os
import shutil


class FileSystemService:
    @staticmethod
    def ensure_directory(path, logger=None):
        if not os.path.exists(path):
            os.makedirs(path)
            if logger:
                logger(f"디렉토리 생성: {path}")
        else:
            if logger:
                logger(f"디렉토리 존재: {path}")

    @staticmethod
    def join_string_and_path(path, string):
        return os.path.join(path, string + '/')

    @staticmethod
    def _check_safe_to_delete(path):
        """드라이브 루트, 홈 폴더, 빈 경로 같은 위험한 경로의 삭제를 막는다."""
        if not path or not str(path).strip():
            raise ValueError("삭제할 경로가 비어 있습니다.")
        real = os.path.realpath(path)
        if real in (os.path.realpath(os.sep), os.path.realpath(os.path.expanduser('~'))) \
                or os.path.dirname(real) == real:
            raise ValueError(f"보호된 경로는 삭제할 수 없습니다: {path}")

    @staticmethod
    def reset_directory(path):
        """폴더를 비우고 다시 만든다. 프로그램 전용 작업 폴더에만 사용할 것."""
        FileSystemService._check_safe_to_delete(path)
        if os.path.exists(path):
            shutil.rmtree(path)
        os.makedirs(path, exist_ok=True)

    @staticmethod
    def remove_directory(path):
        """폴더를 통째로 삭제한다. 프로그램 전용 작업 폴더에만 사용할 것."""
        FileSystemService._check_safe_to_delete(path)
        if os.path.exists(path):
            shutil.rmtree(path)

    @staticmethod
    def copy_files(source_directory, target_directory, include_extensions=None, exclude_extensions=None):
        """원본 폴더의 파일을 대상 폴더로 복사한다.

        대상 폴더의 기존 파일은 삭제하지 않으며, 같은 이름의 파일만 덮어쓴다.
        하위 폴더는 복사하지 않는다.

        :param source_directory: 원본 폴더 경로
        :param target_directory: 대상 폴더 경로 (없으면 생성)
        :param include_extensions: 복사할 확장자 목록 (예: ['.txt', '.csv'] → 이 확장자만 복사)
        :param exclude_extensions: 제외할 확장자 목록 (예: ['.log', '.tmp'] → 이 확장자는 복사 안 함)
        :return: (복사한 파일 수, 그중 덮어쓴 파일 수)
        """
        os.makedirs(target_directory, exist_ok=True)

        copied = overwritten = 0
        for filename in os.listdir(source_directory):
            source_path = os.path.join(source_directory, filename)
            if not os.path.isfile(source_path):
                continue

            file_ext = os.path.splitext(filename)[1].lower()
            if include_extensions and file_ext not in include_extensions:
                continue
            if exclude_extensions and file_ext in exclude_extensions:
                continue

            target_path = os.path.join(target_directory, filename)
            if os.path.exists(target_path):
                overwritten += 1
            shutil.copy2(source_path, target_path)  # 메타데이터 유지
            copied += 1

        return copied, overwritten

    @staticmethod
    def create_txt(output_file, data):
        with open(output_file, 'w', encoding='utf-8') as file:
            for line in data:
                file.write(line)
