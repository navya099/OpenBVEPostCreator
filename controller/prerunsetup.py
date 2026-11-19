from config import ALIGNMENT_TYPES, POST_TYPES


class PreRunSetup:
    """실행 전 옵션 선택 및 필수 설정 검증"""
    def __init__(self, dialogs, state, logger):
        self.dialogs = dialogs
        self.state = state
        self.log = logger

    def run(self) -> bool:
        """모든 사전 단계가 성공하면 True, 취소/검증 실패 시 False"""
        try:
            return (self.preset_alignment_type()
                    and self.preset_posttype()
                    and self.validate())
        except Exception as e:
            self.log(f"사전 설정 중 오류: {e}")
            return False

    def preset_alignment_type(self) -> bool:
        alignment = self.dialogs.select_option_list(ALIGNMENT_TYPES)
        if alignment is None:
            self.log("노선 선택 취소")
            return False
        self.state.alignment_type = alignment
        return True

    def preset_posttype(self) -> bool:
        posttype = self.dialogs.select_option_list(POST_TYPES)
        if posttype is None:
            self.log("제표 종류 선택 취소")
            return False
        self.state.posttype = posttype
        return True

    def validate(self) -> bool:
        """실행 중간에 KeyError/TypeError로 터지던 누락 설정을 미리 확인"""
        missing = []
        if not self.state.target_directory:
            missing.append("대상 디렉터리")
        if not self.state.structure_excel_path:
            missing.append("구조물 엑셀 파일")
        if not self.state.offset:
            missing.append("오프셋 설정")
        if not self.state.track_mode or not self.state.track_direction or not self.state.track_index:
            missing.append("선로 설정")
        if self.state.posttype in ('곡선표', '기울기표') and not self.state.info_path:
            missing.append("INFO 파일")

        if missing:
            self.log(f"❌ 다음 설정이 필요합니다: {', '.join(missing)}")
            return False
        return True
