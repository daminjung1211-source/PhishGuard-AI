
# .env 파일에서 환경 변수를 불러오는 기능을 가져온다.
from dotenv import load_dotenv

# 운영체제의 환경 변수에 접근하는 기능을 가져온다.
import os

# OpenAI API를 사용하기 위한 클래스를 가져온다.
from openai import OpenAI

# 별도 파일에 있는 위험 분석 기능을 가져온다.
from risk_analyzer import calculate_risk, suspicious_words

# 피싱 문자에서 자주 발견되는 의심 단어 목록을 만든다.
suspicious_words = [
    "긴급", "인증", "계정", "송금", "입금",
    "링크", "클릭", "보안", "정지", "당첨"
]


# OpenAI를 이용한 문자 분석 기능을 만든다.
def run_ai_analysis(message):

    # .env 파일에 저장된 환경 변수를 불러온다.
    load_dotenv()

    # 환경 변수에서 OpenAI API 키를 가져온다.
    api_key = os.getenv("OPENAI_API_KEY")

    # API 키가 없는 경우 AI 분석을 건너뛴다.
    if not api_key:
        print("\n===== AI 분석 결과 =====")
        print("API 키를 찾을 수 없어 AI 분석을 건너뜁니다.")
        print("기본 규칙 분석을 계속 진행합니다.")
        return

    # API 요청 중 발생할 수 있는 오류를 처리한다.
    try:
        # API 키를 이용해 OpenAI 클라이언트를 만든다.
        client = OpenAI(api_key=api_key)

        # 입력한 문자에 대한 AI 분석을 요청한다.
        response = client.responses.create(
            # 사용할 AI 모델을 지정한다.
            model="gpt-5-mini",
            # AI에게 분석할 문자와 요청 내용을 전달한다.
            input=f"""
            다음 문자가 피싱 또는 스미싱 문자일 가능성을 분석해줘.

            분석할 문자:
            {message}

            다음 내용을 포함해서 답변해줘.
            1. 피싱 가능성
            2. 의심되는 부분
            3. 사용자가 주의해야 할 점
            """
        )

        # AI 분석 결과의 제목을 출력한다.
        print("\n===== AI 분석 결과 =====")

        # AI가 반환한 분석 결과를 출력한다.
        print(response.output_text)

    # API 요청에 실패하면 실행한다.
    except Exception:
        # AI 분석 결과 영역의 제목을 출력한다.
        print("\n===== AI 분석 결과 =====")

        # AI 분석을 사용할 수 없다고 안내한다.
        print("현재 AI 분석을 사용할 수 없습니다.")

        # 기본 규칙 분석은 계속된다고 안내한다.
        print("기본 규칙 분석을 계속 진행합니다.")


# 문자에서 발견된 위험 요소와 위험 점수를 계산하는 함수를 만든다.
def calculate_risk(message, suspicious_words):

    # 위험 점수를 0점으로 시작한다.
    risk_score = 0

    # 위험 요소의 설명을 저장할 목록을 만든다.
    risk_reasons = []

    # 위험 요소의 설명과 개별 점수를 저장할 목록을 만든다.
    risk_reason_scores = []

    # 의심 단어 하나가 발견될 때 추가할 점수를 설정한다.
    suspicious_word_score = 10

    # 링크가 발견될 때 추가할 점수를 설정한다.
    link_score = 30

    # 긴급 표현이 발견될 때 추가할 점수를 설정한다.
    urgency_score = 20

    # 인증이나 개인정보 요구가 발견될 때 추가할 점수를 설정한다.
    personal_info_score = 20

    # 위험 행동 패턴과 점수 및 설명을 저장한다.
    risk_patterns = {
        # 특정 위치를 누르도록 유도하는 표현이다.
        "여기를 눌러주세요": {
            "score": 15,
            "description": "특정 위치나 링크를 누르도록 유도하는 표현입니다."
        },
        
        # 클릭을 유도하는 표현과 점수를 저장한다.
        "클릭해주세요": {
            "score": 15,
            "description": "링크나 버튼을 클릭하도록 유도하는 표현입니다."
        },

        # 정보 입력을 유도하는 표현과 점수를 저장한다.
        "입력해주세요": {
            "score": 15,
            "description": "사용자에게 정보를 입력하도록 유도하는 표현입니다."
        },

        # 송금을 유도하는 표현과 점수를 저장한다.
        "송금해주세요": {
            "score": 25,
            "description": "금전을 보내도록 유도하는 표현입니다."
        },

        # 비밀번호 입력을 유도하는 표현과 점수를 저장한다.
        "비밀번호를 입력": {
            "score": 25,
            "description": "비밀번호와 같은 중요한 정보를 요구하는 표현입니다."
        }
    }

    # 발견된 의심 단어를 저장할 빈 목록을 만든다.
    found_words = []

    # 의심 단어 목록에서 단어를 하나씩 확인한다.
    for word in suspicious_words:

        # 입력한 문자에 현재 의심 단어가 있는지 확인한다.
        if word in message:

            # 발견된 단어를 목록에 추가한다.
            found_words.append(word)

    # 발견된 의심 단어 개수에 따라 점수를 추가한다.
    word_risk_score = len(found_words) * suspicious_word_score

    # 계산한 의심 단어 점수를 전체 점수에 더한다.
    risk_score += word_risk_score

    # 의심 단어가 발견된 경우 위험 요소를 기록한다.
    if found_words:

        # 의심 단어 위험 요소의 설명을 만든다.
        reason = f"의심 단어 발견 (+{word_risk_score}점)"

        # 위험 요소 설명을 목록에 추가한다.
        risk_reasons.append(reason)

        # 위험 요소 설명과 점수를 함께 저장한다.
        risk_reason_scores.append((reason, word_risk_score))

    # 문자에 HTTP 또는 HTTPS 링크가 있는지 확인한다.
    if "http://" in message or "https://" in message:

        # 링크 위험 점수를 전체 점수에 더한다.
        risk_score += link_score

        # 링크 위험 요소의 설명을 만든다.
        reason = f"링크 포함 (+{link_score}점)"

        # 링크 위험 요소를 목록에 추가한다.
        risk_reasons.append(reason)

        # 링크 위험 요소의 설명과 점수를 저장한다.
        risk_reason_scores.append((reason, link_score))

    # 긴급성을 나타내는 표현이 있는지 확인한다.
    if "긴급" in message or "즉시" in message or "지금" in message:

        # 긴급 표현 위험 점수를 전체 점수에 더한다.
        risk_score += urgency_score

        # 긴급 표현 위험 요소의 설명을 만든다.
        reason = f"긴급한 표현 사용 (+{urgency_score}점)"

        # 긴급 표현 위험 요소를 목록에 추가한다.
        risk_reasons.append(reason)

        # 긴급 표현의 설명과 점수를 저장한다.
        risk_reason_scores.append((reason, urgency_score))

    # 인증이나 개인정보를 요구하는 표현이 있는지 확인한다.
    if (
        "인증" in message
        or "비밀번호" in message
        or "개인정보" in message
    ):

        # 개인정보 관련 위험 점수를 전체 점수에 더한다.
        risk_score += personal_info_score

        # 개인정보 관련 위험 요소의 설명을 만든다.
        reason = f"인증 또는 개인정보 요구 (+{personal_info_score}점)"

        # 개인정보 관련 위험 요소를 목록에 추가한다.
        risk_reasons.append(reason)

        # 개인정보 관련 설명과 점수를 저장한다.
        risk_reason_scores.append((reason, personal_info_score))

    # 등록된 위험 행동 패턴을 하나씩 확인한다.
    for pattern, pattern_info in risk_patterns.items():

        # 현재 위험 패턴의 점수를 가져온다.
        pattern_score = pattern_info["score"]

        # 현재 위험 패턴의 설명을 가져온다.
        pattern_description = pattern_info["description"]

        # 입력한 문자에 현재 위험 패턴이 있는지 확인한다.
        if pattern in message:

            # 발견한 위험 패턴의 점수를 전체 점수에 더한다.
            risk_score += pattern_score

            # 위험 패턴의 설명과 점수를 문자열로 만든다.
            reason = (
                f"위험 행동 유도: {pattern} "
                f"(+{pattern_score}점) - {pattern_description}"
            )

            # 발견한 위험 패턴을 위험 요소 목록에 추가한다.
            risk_reasons.append(reason)

            # 위험 패턴의 설명과 점수를 함께 저장한다.
            risk_reason_scores.append((reason, pattern_score))

    # 전체 위험 점수가 100점을 초과하는지 확인한다.
    if risk_score > 100:

        # 전체 위험 점수를 최대 100점으로 제한한다.
        risk_score = 100

    # 계산한 결과 네 가지를 호출한 곳으로 반환한다.
    return risk_score, risk_reasons, found_words, risk_reason_scores


# 프로그램의 전체 실행을 담당하는 함수를 만든다.
def main():

    # 사용자에게 분석할 문자를 입력받는다.
    message = input("분석할 문자를 입력하세요: ")

    # 입력한 문자에 대한 AI 분석을 시도한다.
    run_ai_analysis(message)

    # 입력한 문자를 화면에 출력한다.
    print("\n입력한 문자:")
    print(message)

    # 기본 규칙 분석이 시작되었음을 안내한다.
    print("\n[PhishGuard AI] 기본 규칙 검사를 시작합니다.")

    # 위험 점수와 분석 결과를 계산한다.
    risk_score, risk_reasons, found_words, risk_reason_scores = (
        calculate_risk(message, suspicious_words)
    )

    # 발견된 의심 단어 영역의 제목을 출력한다.
    print("\n발견된 의심 단어:")

    # 의심 단어가 발견되었는지 확인한다.
    if found_words:

        # 발견된 의심 단어를 쉼표로 구분하여 출력한다.
        print(", ".join(found_words))

    # 의심 단어가 하나도 없는 경우 실행한다.
    else:

        # 발견된 의심 단어가 없다고 안내한다.
        print("발견되지 않았습니다.")

    # 기본 규칙 검사가 완료되었음을 출력한다.
    print("\n[PhishGuard AI] 기본 규칙 검사가 완료되었습니다.")

    # 분석 결과의 제목을 출력한다.
    print("\n===== PhishGuard 분석 결과 =====")

    # 최종 위험 점수를 출력한다.
    print("위험 점수:", risk_score, "점")

    # 위험 요소 영역의 제목을 출력한다.
    print("\n위험 요소:")

    # 위험 요소가 존재하는지 확인한다.
    if risk_reasons:

        # 위험 요소를 하나씩 꺼내서 출력한다.
        for reason in risk_reasons:

            # 위험 요소 앞에 하이픈을 붙여 출력한다.
            print("-", reason)

    # 위험 요소가 없는 경우 실행한다.
    else:

        # 위험 요소가 없다고 안내한다.
        print("- 특별한 위험 요소가 발견되지 않았습니다.")

    # 개별 위험 점수 목록이 비어 있지 않은지 확인한다.
    if risk_reason_scores:

        # 가장 높은 개별 위험 점수를 0점으로 시작한다.
        highest_risk_score = 0

        # 각 위험 요소의 점수를 확인한다.
        for reason, score in risk_reason_scores:

            # 현재 점수가 최고 점수보다 높은지 확인한다.
            if score > highest_risk_score:

                # 더 높은 점수를 최고 점수로 저장한다.
                highest_risk_score = score

        # 가장 큰 위험 요소 영역의 제목을 출력한다.
        print("\n[가장 큰 위험 요소]")

        # 가장 높은 점수와 같은 위험 요소를 찾는다.
        for reason, score in risk_reason_scores:

            # 현재 점수가 최고 점수와 같은지 확인한다.
            if score == highest_risk_score:

                # 가장 큰 위험 요소를 출력한다.
                print("-", reason)

    # 개별 위험 점수가 없는 경우 실행한다.
    else:

        # 가장 큰 위험 요소 영역의 제목을 출력한다.
        print("\n[가장 큰 위험 요소]")

        # 위험 요소가 없다고 안내한다.
        print("발견된 위험 요소가 없습니다.")

    # 위험 점수가 80점 이상인지 확인한다.
    if risk_score >= 80:

        # 위험 수준을 매우 위험으로 설정한다.
        risk_level = "매우 위험"

        # 분석 결과를 한 문장으로 요약한다.
        risk_summary = (
            "여러 위험 요소가 발견되었습니다. "
            "피싱 또는 스미싱 문자일 가능성을 주의 깊게 확인하세요."
        )

        # 매우 위험한 문자에 대한 안전 안내를 만든다.
        safety_advice = [
            "링크를 클릭하지 마세요.",
            "비밀번호나 인증번호를 입력하지 마세요.",
            "이미 정보를 입력했다면 해당 서비스의 공식 고객센터에 문의하세요."
        ]

    # 위험 점수가 40점 이상인지 확인한다.
    elif risk_score >= 40:

        # 위험 수준을 주의로 설정한다.
        risk_level = "주의"

        # 분석 결과를 한 문장으로 요약한다.
        risk_summary = (
            "일부 위험 요소가 발견되었습니다. "
            "발신자와 문자 내용을 신중하게 확인하세요."
        )

        # 주의 단계에 필요한 안전 안내를 만든다.
        safety_advice = [
            "문자 발신자를 확인하세요.",
            "개인정보나 금융정보를 입력하지 마세요.",
            "해당 기관의 공식 홈페이지나 고객센터에서 확인하세요."
        ]

    # 위험 점수가 40점보다 낮으면 실행한다.
    else:

        # 위험 수준을 낮음으로 설정한다.
        risk_level = "낮음"

        # 분석 결과를 한 문장으로 요약한다.
        risk_summary = (
            "현재 규칙 검사에서 발견된 위험 요소가 적습니다. "
            "다만 안전한 문자라고 확정할 수는 없습니다."
        )

        # 낮은 위험 단계에서도 주의할 점을 안내한다.
        safety_advice = [
            "출처가 불분명한 링크는 주의하세요.",
            "개인정보를 요구하는 문자는 공식 경로로 확인하세요."
        ]

    # 분석 결과 요약 영역의 제목을 출력한다.
    print("\n[분석 요약]")

    # 분석 결과 요약을 출력한다.
    print(risk_summary)

    # 최종 위험 수준을 출력한다.
    print("\n위험 수준:", risk_level)

    # 안전 안내 영역의 제목을 출력한다.
    print("\n[안전 안내]")

    # 안전 안내 목록에서 문구를 하나씩 가져온다.
    for advice in safety_advice:

        # 각 안전 안내 문구를 출력한다.
        print("-", advice)


# 이 파일을 직접 실행했을 때만 main()을 실행한다.
if __name__ == "__main__":

    # 프로그램의 전체 실행 함수를 호출한다.
    main()
