# unittest는 Python에 기본으로 포함된 자동 테스트 도구입니다.
import unittest

# main.py에서 위험 점수를 계산하는 함수를 가져옵니다.
from main import calculate_risk

# main.py에서 사용하는 의심 단어 목록을 가져옵니다.
from main import suspicious_words


# PhishGuard AI의 자동 테스트를 담당하는 클래스를 만듭니다.
class TestPhishGuard(unittest.TestCase):

    # 일반적인 문자가 낮은 위험 점수로 분류되는지 검사합니다.
    def test_normal_message(self):
        # 위험 요소가 거의 없는 일반 문자를 준비합니다.
        message = "오늘 오후 3시에 학교 앞에서 만나자."

        # 준비한 문자로 위험 점수를 계산합니다.
        score, reasons, found_words, reason_scores = calculate_risk(
            message, suspicious_words
        )

        # 일반 문자의 점수가 40점 미만인지 확인합니다.
        self.assertLess(score, 40)

    # 의심 단어가 포함된 문자가 위험 점수를 받는지 검사합니다.
    def test_suspicious_words(self):
        # 의심 단어가 포함된 문자를 준비합니다.
        message = "긴급! 계정 인증이 필요합니다."

        # 위험 점수를 계산합니다.
        score, reasons, found_words, reason_scores = calculate_risk(
            message, suspicious_words
        )

        # 점수가 0점보다 큰지 확인합니다.
        self.assertGreater(score, 0)

        # 의심 단어가 실제로 탐지되었는지 확인합니다.
        self.assertTrue(found_words)

    # 인터넷 주소가 위험 점수에 반영되는지 검사합니다.
    def test_link_detection(self):
        # 인터넷 주소가 포함된 문자를 준비합니다.
        message = "아래 링크를 확인하세요. http://example.com"

        # 위험 점수를 계산합니다.
        score, reasons, found_words, reason_scores = calculate_risk(
            message, suspicious_words
        )

        # 링크가 포함되어 30점 이상인지 확인합니다.
        self.assertGreaterEqual(score, 30)

    # 최종 위험 점수가 100점을 넘지 않는지 검사합니다.
    def test_score_limit(self):
        # 다양한 위험 표현을 포함한 문자를 준비합니다.
        message = (
            "긴급! 계정 인증이 필요합니다. "
            "송금해주세요. 비밀번호를 입력해주세요. "
            "http://example.com"
        )

        # 위험 점수를 계산합니다.
        score, reasons, found_words, reason_scores = calculate_risk(
            message, suspicious_words
        )

        # 점수가 0점 이상인지 확인합니다.
        self.assertGreaterEqual(score, 0)

        # 점수가 100점을 넘지 않는지 확인합니다.
        self.assertLessEqual(score, 100)

        # 위험 행동을 유도하는 표현이 탐지되는지 검사한다.
    def test_risk_pattern_detection(self):
        # 클릭을 유도하는 테스트 문자를 만든다.
        message = "상품을 받으려면 클릭해주세요."

        # 위험 점수와 분석 결과를 계산한다.
        score, reasons, found_words, reason_scores = calculate_risk(
            message, suspicious_words
        )

        # 위험 행동 유도 항목이 있는지 확인한다.
        self.assertTrue(
            any("위험 행동 유도: 클릭해주세요" in reason for reason in reasons)
        )

        # 클릭 유도 패턴의 점수 15점이 반영되었는지 확인한다.
        self.assertGreaterEqual(score, 15)


# 이 파일을 직접 실행했을 때 테스트를 시작합니다.
if __name__ == "__main__":
    # 등록된 테스트를 실행하고 결과를 출력합니다.
    unittest.main()
