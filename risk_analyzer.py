# 위험 문자 분석에 필요한 단어 목록과 함수를 관리하는 파일이다.

# 피싱이나 스미싱에서 자주 등장하는 의심 단어 목록이다.
suspicious_words = [
    "긴급", "인증", "계정", "송금", "입금",
    "링크", "클릭", "보안", "정지", "당첨"
]


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
        "클릭해주세요": {
            "score": 15,
            "description": "링크나 버튼을 클릭하도록 유도하는 표현입니다."
        },
        "입력해주세요": {
            "score": 15,
            "description": "사용자에게 정보를 입력하도록 유도하는 표현입니다."
        },
        "송금해주세요": {
            "score": 25,
            "description": "금전을 보내도록 유도하는 표현입니다."
        },
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

    # 발견된 의심 단어 개수에 따라 점수를 계산한다.
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