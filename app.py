
# Streamlit 라이브러리를 가져온다. 웹 화면을 만드는 데 사용한다.
import streamlit as st

# 기존 위험 분석 파일에서 분석 함수와 의심 단어 목록을 가져온다.
from risk_analyzer import calculate_risk, suspicious_words

# 웹 페이지의 제목과 브라우저 탭 아이콘을 설정한다.
st.set_page_config(
    page_title="PhishGuard AI",
    page_icon="🛡️",
    layout="centered"
)

# 웹 페이지의 제목을 표시한다.
st.title("🛡️ PhishGuard AI")

# 프로그램의 간단한 설명을 표시한다.
st.write("피싱 문자 메시지의 위험 요소를 분석하는 프로그램입니다.")

# 사용자가 분석할 문자 메시지를 입력할 수 있는 상자를 만든다.
message = st.text_area(
    "분석할 문자 메시지를 입력하세요.",
    placeholder="예: 긴급! 계정이 정지됩니다. 링크를 클릭하세요.",
    height=160
)

# 사용자가 분석 버튼을 누르면 아래 코드를 실행한다.
if st.button("피싱 위험 분석하기", type="primary"):

    # 입력한 내용이 비어 있는지 확인한다.
    if not message.strip():
        # 내용이 없으면 안내 메시지를 표시한다.
        st.warning("먼저 분석할 문자 메시지를 입력해 주세요.")

    else:
        # 기존 분석 함수를 사용해 위험 점수와 분석 이유를 계산한다.
        risk_score, risk_reasons, found_words, risk_reason_scores = (
            calculate_risk(message, suspicious_words)
        )

        # 분석 결과 제목을 표시한다.
        st.subheader("분석 결과")

        # 위험 점수를 숫자와 진행 막대로 표시한다.
        st.metric("위험 점수", f"{risk_score} / 100")
        st.progress(risk_score)

        # 위험 점수에 따라 위험 등급을 결정한다.
        if risk_score >= 80:
            # 점수가 80점 이상이면 매우 위험으로 표시한다.
            st.error("위험 등급: 매우 위험")
        elif risk_score >= 40:
            # 점수가 40점 이상이면 주의로 표시한다.
            st.warning("위험 등급: 주의")
        else:
            # 점수가 40점 미만이면 낮음으로 표시한다.
            st.success("위험 등급: 낮음")

        # 탐지된 의심 단어를 표시한다.
        st.write("### 탐지된 의심 단어")
        if found_words:
            # 의심 단어가 있으면 목록으로 보여 준다.
            st.write(", ".join(found_words))
        else:
            # 의심 단어가 없으면 안내 문구를 보여 준다.
            st.write("등록된 의심 단어가 발견되지 않았습니다.")

        # 위험 요소와 각 요소의 점수를 표시한다.
        st.write("### 위험 요소")
        if risk_reasons:
            # 위험 요소를 하나씩 목록에 표시한다.
            for reason in risk_reasons:
                st.write(f"- {reason}")
        else:
            # 위험 요소가 없으면 안내 문구를 보여 준다.
            st.write("등록된 위험 요소가 발견되지 않았습니다.")

        # 사용자에게 안전 수칙을 안내한다.
        st.info(
            "안전 수칙: 의심스러운 링크를 누르거나 비밀번호, "
            "인증번호, 금융 정보를 입력하지 마세요."
        )

# 화면 하단에 프로그램의 한계를 안내한다.
st.caption(
    "주의: 이 프로그램은 규칙 기반 분석 도구이며, "
    "모든 피싱 문자를 정확하게 탐지한다고 보장하지 않습니다."
)
