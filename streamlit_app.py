import streamlit as st
import openai
from typing import Dict, List
import time

# 페이지 설정
st.set_page_config(
    page_title="AI MBTI 성격 테스트",
    page_icon="🎭",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 커스텀 CSS - 최신 트렌드 디자인
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&family=Playfair+Display:wght@700&display=swap');
    
    /* 전체 배경 */
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #4facfe 75%, #00f2fe 100%);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    
    @keyframes gradient {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    /* 메인 컨테이너 */
    .main-container {
        max-width: 900px;
        margin: 0 auto;
        padding: 2rem;
    }
    
    /* 카드 스타일 */
    .card {
        background: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(10px);
        border-radius: 24px;
        padding: 3rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.15);
        margin-bottom: 2rem;
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    /* 타이틀 */
    .main-title {
        font-family: 'Playfair Display', serif;
        font-size: 3.5rem;
        font-weight: 700;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
        animation: fadeIn 1s ease-out;
    }
    
    @keyframes fadeIn {
        from { opacity: 0; }
        to { opacity: 1; }
    }
    
    .subtitle {
        font-family: 'Poppins', sans-serif;
        font-size: 1.2rem;
        text-align: center;
        color: #555;
        margin-bottom: 3rem;
    }
    
    /* 질문 카드 */
    .question-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 16px;
        padding: 2rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.08);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    
    .question-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
    }
    
    .question-text {
        font-family: 'Poppins', sans-serif;
        font-size: 1.3rem;
        font-weight: 500;
        color: #2d3748;
        margin-bottom: 1.5rem;
    }
    
    /* 버튼 스타일 */
    .stButton > button {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        font-weight: 500;
        padding: 0.8rem 2rem;
        border-radius: 12px;
        border: none;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        cursor: pointer;
        transition: all 0.3s ease;
        width: 100%;
        margin-top: 1rem;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
    }
    
    /* 라디오 버튼 커스텀 */
    .stRadio > label {
        font-family: 'Poppins', sans-serif;
        font-size: 1rem;
        color: #2d3748;
    }
    
    /* 텍스트 입력 */
    .stTextInput > div > div > input {
        font-family: 'Poppins', sans-serif;
        border-radius: 12px;
        border: 2px solid #e2e8f0;
        padding: 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    /* 결과 카드 */
    .result-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 24px;
        padding: 3rem;
        text-align: center;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
        animation: scaleIn 0.5s ease-out;
    }
    
    @keyframes scaleIn {
        from {
            opacity: 0;
            transform: scale(0.9);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    .mbti-type {
        font-family: 'Playfair Display', serif;
        font-size: 4rem;
        font-weight: 700;
        margin: 1rem 0;
        letter-spacing: 0.1em;
    }
    
    .result-description {
        font-family: 'Poppins', sans-serif;
        font-size: 1.1rem;
        line-height: 1.8;
        margin-top: 2rem;
    }
    
    /* 프로그레스 바 */
    .progress-container {
        background: rgba(255, 255, 255, 0.3);
        border-radius: 10px;
        height: 8px;
        margin: 2rem 0;
        overflow: hidden;
    }
    
    .progress-bar {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        transition: width 0.5s ease;
    }
    
    /* 애니메이션 딜레이 */
    .delay-1 { animation-delay: 0.1s; }
    .delay-2 { animation-delay: 0.2s; }
    .delay-3 { animation-delay: 0.3s; }
    
    /* 스피너 */
    .loading-spinner {
        text-align: center;
        padding: 2rem;
    }
    
    .spinner {
        border: 4px solid rgba(102, 126, 234, 0.1);
        border-left-color: #667eea;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        animation: spin 1s linear infinite;
        margin: 0 auto;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* 숨기기 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# MBTI 질문 데이터 (16문항)
MBTI_QUESTIONS = [
    # E/I (외향/내향)
    {
        "id": 1,
        "question": "새로운 사람들과의 만남이 있는 파티에 초대받았습니다. 당신은?",
        "options": [
            ("기대되고 즐겁다! 새로운 사람들을 만나는 게 좋아요.", "E"),
            ("조금 부담스럽지만 가볼까 합니다.", "I")
        ]
    },
    {
        "id": 2,
        "question": "에너지를 충전하는 방법은?",
        "options": [
            ("친구들과 함께 시간을 보내며 활력을 얻습니다.", "E"),
            ("혼자만의 시간을 가지며 에너지를 회복합니다.", "I")
        ]
    },
    {
        "id": 3,
        "question": "대화할 때 당신은?",
        "options": [
            ("말하면서 생각을 정리하고, 즉흥적으로 대화합니다.", "E"),
            ("생각을 먼저 정리한 후 신중하게 말합니다.", "I")
        ]
    },
    {
        "id": 4,
        "question": "주말에 친구가 갑자기 놀러 오자고 합니다. 당신은?",
        "options": [
            ("좋아요! 바로 만나요!", "E"),
            ("미리 계획하는 걸 선호하지만... 괜찮아요.", "I")
        ]
    },
    # S/N (감각/직관)
    {
        "id": 5,
        "question": "새로운 프로젝트를 시작할 때 당신은?",
        "options": [
            ("구체적인 세부사항과 실행 계획부터 세웁니다.", "S"),
            ("큰 그림과 가능성부터 생각합니다.", "N")
        ]
    },
    {
        "id": 6,
        "question": "정보를 받아들일 때 더 중요하게 생각하는 것은?",
        "options": [
            ("실제 경험과 구체적인 사실들", "S"),
            ("숨겨진 의미와 미래의 가능성", "N")
        ]
    },
    {
        "id": 7,
        "question": "문제를 해결할 때 당신은?",
        "options": [
            ("검증된 방법을 사용하고 단계별로 진행합니다.", "S"),
            ("새로운 방법을 시도하고 창의적으로 접근합니다.", "N")
        ]
    },
    {
        "id": 8,
        "question": "이야기를 할 때 당신은?",
        "options": [
            ("사실과 세부사항을 정확하게 전달합니다.", "S"),
            ("전체적인 맥락과 의미를 중심으로 이야기합니다.", "N")
        ]
    },
    # T/F (사고/감정)
    {
        "id": 9,
        "question": "결정을 내릴 때 더 중요하게 생각하는 것은?",
        "options": [
            ("논리적 분석과 객관적 사실", "T"),
            ("사람들의 감정과 관계", "F")
        ]
    },
    {
        "id": 10,
        "question": "친구가 문제로 힘들어할 때 당신은?",
        "options": [
            ("문제의 원인을 분석하고 해결책을 제시합니다.", "T"),
            ("공감하고 위로하며 감정을 이해하려 합니다.", "F")
        ]
    },
    {
        "id": 11,
        "question": "피드백을 줄 때 당신은?",
        "options": [
            ("직설적이고 정확하게 개선점을 말합니다.", "T"),
            ("상대방의 기분을 고려하며 부드럽게 전달합니다.", "F")
        ]
    },
    {
        "id": 12,
        "question": "비판을 받을 때 당신은?",
        "options": [
            ("내용이 논리적으로 타당한지 분석합니다.", "T"),
            ("상대방이 나를 어떻게 생각하는지 신경 쓰입니다.", "F")
        ]
    },
    # J/P (판단/인식)
    {
        "id": 13,
        "question": "하루 일과를 계획할 때 당신은?",
        "options": [
            ("미리 계획을 세우고 그대로 실행합니다.", "J"),
            ("그때그때 상황에 맞춰 유연하게 대응합니다.", "P")
        ]
    },
    {
        "id": 14,
        "question": "여행을 준비할 때 당신은?",
        "options": [
            ("일정표를 만들고 예약을 미리 완료합니다.", "J"),
            ("대략적인 계획만 세우고 즉흥적으로 즐깁니다.", "P")
        ]
    },
    {
        "id": 15,
        "question": "업무 마감이 다가올 때 당신은?",
        "options": [
            ("미리미리 준비해서 여유 있게 완료합니다.", "J"),
            ("마감 압박이 있을 때 집중력이 발휘됩니다.", "P")
        ]
    },
    {
        "id": 16,
        "question": "방 정리에 대한 당신의 생각은?",
        "options": [
            ("정리정돈된 깔끔한 공간을 선호합니다.", "J"),
            ("약간 어질러져 있어도 편안합니다.", "P")
        ]
    }
]

# MBTI 유형별 설명
MBTI_DESCRIPTIONS = {
    "ISTJ": "신중하고 책임감 있는 관리자",
    "ISFJ": "따뜻하고 헌신적인 수호자",
    "INFJ": "통찰력 있는 이상주의자",
    "INTJ": "전략적이고 독립적인 설계자",
    "ISTP": "논리적이고 실용적인 장인",
    "ISFP": "감성적이고 유연한 예술가",
    "INFP": "이상적이고 창의적인 중재자",
    "INTP": "논리적이고 창의적인 사색가",
    "ESTP": "대담하고 활동적인 사업가",
    "ESFP": "자유롭고 즐거운 엔터테이너",
    "ENFP": "열정적이고 창의적인 활동가",
    "ENTP": "영리하고 호기심 많은 발명가",
    "ESTJ": "실용적이고 체계적인 경영자",
    "ESFJ": "사교적이고 협력적인 지원자",
    "ENFJ": "카리스마 있는 리더",
    "ENTJ": "대담하고 전략적인 지휘관"
}

def calculate_mbti(answers: Dict[int, str]) -> str:
    """답변을 기반으로 MBTI 유형 계산"""
    scores = {"E": 0, "I": 0, "S": 0, "N": 0, "T": 0, "F": 0, "J": 0, "P": 0}
    
    for answer in answers.values():
        scores[answer] += 1
    
    mbti = ""
    mbti += "E" if scores["E"] >= scores["I"] else "I"
    mbti += "S" if scores["S"] >= scores["N"] else "N"
    mbti += "T" if scores["T"] >= scores["F"] else "T"
    mbti += "J" if scores["J"] >= scores["P"] else "P"
    
    return mbti

def get_ai_analysis(api_key: str, mbti_type: str, answers: Dict[int, str]) -> str:
    """OpenAI API를 사용하여 개인화된 MBTI 분석 생성"""
    try:
        client = openai.OpenAI(api_key=api_key)
        
        # 답변 패턴 분석
        answer_summary = "\n".join([
            f"질문 {q_id}: {MBTI_QUESTIONS[q_id-1]['question'][:30]}... → {answer}"
            for q_id, answer in answers.items()
        ])
        
        prompt = f"""당신은 전문 심리 상담사입니다. 다음 MBTI 테스트 결과를 바탕으로 상세하고 개인화된 성격 분석을 제공해주세요.

MBTI 유형: {mbti_type}
유형 설명: {MBTI_DESCRIPTIONS[mbti_type]}

사용자의 답변 패턴:
{answer_summary}

다음 내용을 포함하여 작성해주세요:
1. 이 유형의 핵심 특징과 강점 (3-4문장)
2. 성장을 위한 구체적인 조언 (2-3문장)
3. 이 유형에게 어울리는 직업이나 환경 (2-3문장)
4. 대인관계에서의 특징과 팁 (2-3문장)

따뜻하고 긍정적인 톤으로 작성하되, 구체적이고 실용적인 조언을 포함해주세요.
"""
        
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "당신은 따뜻하고 전문적인 심리 상담사입니다."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )
        
        return response.choices[0].message.content
    
    except Exception as e:
        return f"분석 생성 중 오류가 발생했습니다: {str(e)}"

def main():
    # 세션 상태 초기화
    if 'page' not in st.session_state:
        st.session_state.page = 'api_input'
    if 'api_key' not in st.session_state:
        st.session_state.api_key = None
    if 'current_question' not in st.session_state:
        st.session_state.current_question = 0
    if 'answers' not in st.session_state:
        st.session_state.answers = {}
    if 'mbti_result' not in st.session_state:
        st.session_state.mbti_result = None
    if 'ai_analysis' not in st.session_state:
        st.session_state.ai_analysis = None
    
    # API 입력 페이지
    if st.session_state.page == 'api_input':
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown('<h1 class="main-title">🎭 AI MBTI 성격 테스트</h1>', unsafe_allow_html=True)
        st.markdown('<p class="subtitle">AI가 분석하는 당신만의 성격 유형을 발견하세요</p>', unsafe_allow_html=True)
        
        st.markdown("### 🔑 OpenAI API 키 입력")
        st.markdown("테스트 결과에 대한 AI 기반 상세 분석을 제공하기 위해 OpenAI API 키가 필요합니다.")
        
        api_key = st.text_input(
            "API Key",
            type="password",
            placeholder="sk-...",
            help="OpenAI API 키를 입력하세요. 키는 저장되지 않으며 이번 세션에만 사용됩니다."
        )
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("✨ 테스트 시작하기", use_container_width=True):
                if api_key and api_key.startswith('sk-'):
                    st.session_state.api_key = api_key
                    st.session_state.page = 'test'
                    st.rerun()
                else:
                    st.error("올바른 OpenAI API 키를 입력해주세요.")
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #666; font-size: 0.9rem;'>
        <p>💡 <strong>16개의 질문</strong>으로 당신의 성격 유형을 분석합니다</p>
        <p>🤖 <strong>AI 분석</strong>으로 개인화된 상세 결과를 제공합니다</p>
        <p>🎨 <strong>5분 소요</strong> - 빠르고 정확한 테스트</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 테스트 페이지
    elif st.session_state.page == 'test':
        progress = (st.session_state.current_question) / len(MBTI_QUESTIONS)
        
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        # 프로그레스 바
        st.markdown(f"""
        <div class="progress-container">
            <div class="progress-bar" style="width: {progress * 100}%"></div>
        </div>
        <p style="text-align: center; font-family: 'Poppins', sans-serif; color: #667eea; font-weight: 500;">
            질문 {st.session_state.current_question + 1} / {len(MBTI_QUESTIONS)}
        </p>
        """, unsafe_allow_html=True)
        
        # 현재 질문
        if st.session_state.current_question < len(MBTI_QUESTIONS):
            current_q = MBTI_QUESTIONS[st.session_state.current_question]
            
            st.markdown(f'<div class="question-card">', unsafe_allow_html=True)
            st.markdown(f'<p class="question-text">Q{current_q["id"]}. {current_q["question"]}</p>', unsafe_allow_html=True)
            
            # 답변 선택
            answer = st.radio(
                "답변을 선택하세요:",
                options=[opt[0] for opt in current_q["options"]],
                key=f"q_{current_q['id']}",
                label_visibility="collapsed"
            )
            
            st.markdown('</div>', unsafe_allow_html=True)
            
            # 다음/이전 버튼
            col1, col2 = st.columns(2)
            
            with col1:
                if st.session_state.current_question > 0:
                    if st.button("⬅️ 이전", use_container_width=True):
                        st.session_state.current_question -= 1
                        st.rerun()
            
            with col2:
                if st.button("➡️ 다음" if st.session_state.current_question < len(MBTI_QUESTIONS) - 1 else "✅ 완료", use_container_width=True):
                    # 답변 저장
                    selected_option = [opt for opt in current_q["options"] if opt[0] == answer][0]
                    st.session_state.answers[current_q["id"]] = selected_option[1]
                    
                    if st.session_state.current_question < len(MBTI_QUESTIONS) - 1:
                        st.session_state.current_question += 1
                        st.rerun()
                    else:
                        # 모든 질문 완료
                        st.session_state.mbti_result = calculate_mbti(st.session_state.answers)
                        st.session_state.page = 'loading'
                        st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 로딩 페이지
    elif st.session_state.page == 'loading':
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        st.markdown('<div class="card">', unsafe_allow_html=True)
        
        st.markdown("""
        <div class="loading-spinner">
            <div class="spinner"></div>
            <p style="font-family: 'Poppins', sans-serif; font-size: 1.2rem; color: #667eea; margin-top: 1rem;">
                AI가 당신의 성격을 분석하고 있습니다...
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # AI 분석 실행
        if st.session_state.ai_analysis is None:
            with st.spinner(""):
                st.session_state.ai_analysis = get_ai_analysis(
                    st.session_state.api_key,
                    st.session_state.mbti_result,
                    st.session_state.answers
                )
                time.sleep(1)  # 자연스러운 로딩 효과
                st.session_state.page = 'result'
                st.rerun()
        
        st.markdown('</div></div>', unsafe_allow_html=True)
    
    # 결과 페이지
    elif st.session_state.page == 'result':
        st.markdown('<div class="main-container">', unsafe_allow_html=True)
        
        # 결과 카드
        st.markdown('<div class="result-card">', unsafe_allow_html=True)
        st.markdown(f'<p style="font-family: Poppins, sans-serif; font-size: 1.5rem;">당신의 MBTI 유형은</p>', unsafe_allow_html=True)
        st.markdown(f'<h1 class="mbti-type">{st.session_state.mbti_result}</h1>', unsafe_allow_html=True)
        st.markdown(f'<p style="font-family: Poppins, sans-serif; font-size: 1.8rem; font-weight: 600;">{MBTI_DESCRIPTIONS[st.session_state.mbti_result]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # AI 분석 결과
        st.markdown('<div class="card delay-1">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI 성격 분석")
        st.markdown(f'<div class="result-description">{st.session_state.ai_analysis}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # 재시작 버튼
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("🔄 다시 테스트하기", use_container_width=True):
                # 세션 초기화
                st.session_state.page = 'api_input'
                st.session_state.current_question = 0
                st.session_state.answers = {}
                st.session_state.mbti_result = None
                st.session_state.ai_analysis = None
                st.session_state.api_key = None
                st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()
