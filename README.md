# 🎭 AI MBTI 성격 테스트

OpenAI API를 활용한 최신 트렌드 디자인의 MBTI 성격 테스트 웹 애플리케이션입니다.

## ✨ 주요 기능

- **16개의 MBTI 질문**: 각 지표(E/I, S/N, T/F, J/P)당 4문항씩 구성
- **AI 기반 분석**: OpenAI GPT-4를 활용한 개인화된 성격 분석
- **최신 트렌드 디자인**: 
  - 애니메이션 그라데이션 배경
  - 부드러운 페이드 인/아웃 효과
  - 글래스모피즘 카드 디자인
  - 반응형 레이아웃
- **사용자 친화적 인터페이스**: 진행률 표시 및 직관적인 네비게이션

## 📋 요구사항

- Python 3.8 이상
- OpenAI API 키

## 🚀 설치 및 실행 방법

### 1. 패키지 설치

```bash
pip install -r requirements.txt
```

### 2. 앱 실행

```bash
streamlit run mbti_app.py
```

### 3. OpenAI API 키 준비

- [OpenAI 플랫폼](https://platform.openai.com/)에서 API 키 발급
- 앱 첫 화면에서 API 키 입력

## 🎨 디자인 특징

### 색상 팔레트
- **주요 색상**: Purple-Pink 그라데이션 (#667eea → #764ba2)
- **강조 색상**: Cyan-Blue 그라데이션 (#4facfe → #00f2fe)
- **배경**: 멀티 컬러 애니메이션 그라데이션

### 타이포그래피
- **헤드라인**: Playfair Display (세리프 폰트)
- **본문**: Poppins (산세리프 폰트)

### 애니메이션
- 페이드 인/아웃 효과
- 스무스 트랜지션
- 호버 효과
- 프로그레스 바 애니메이션

## 📱 화면 구성

1. **API 입력 화면**: OpenAI API 키 입력
2. **테스트 화면**: 16개 질문에 대한 답변
3. **로딩 화면**: AI 분석 진행 중
4. **결과 화면**: MBTI 유형 및 AI 분석 결과

## 🔒 개인정보 보호

- API 키는 세션에만 저장되며 서버에 저장되지 않습니다
- 테스트 결과는 로컬에서만 처리됩니다

## 💡 사용 팁

- 질문에 솔직하게 답변할수록 정확한 결과를 얻을 수 있습니다
- 각 질문은 충분히 생각한 후 답변하세요
- 이전 버튼으로 답변 수정이 가능합니다

## 📝 MBTI 16가지 유형

- **분석가**: INTJ, INTP, ENTJ, ENTP
- **외교관**: INFJ, INFP, ENFJ, ENFP
- **관리자**: ISTJ, ISFJ, ESTJ, ESFJ
- **탐험가**: ISTP, ISFP, ESTP, ESFP

## 🤝 기여

이 프로젝트는 교육 목적으로 제작되었습니다.

## ⚠️ 주의사항

- 이 테스트는 전문적인 심리 평가를 대체할 수 없습니다
- 결과는 참고용으로만 활용하세요
- OpenAI API 사용에 따른 비용이 발생할 수 있습니다

## 📄 라이센스

Educational Use Only

---

Made with ❤️ using Streamlit and OpenAI API
