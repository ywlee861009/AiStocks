# AiStocks

> AI 기반 주식 분석 애플리케이션

## 프로젝트 소개

AiStocks는 인공지능을 활용하여 주식 데이터를 분석하고 인사이트를 제공하는 애플리케이션입니다.

## 주요 기능

- 주식 데이터 수집 및 분석
- AI 기반 예측 모델
- 데이터 시각화
- 자동 리포트 생성

## 환경 설정

### 1. 저장소 클론

```bash
git clone <repository-url>
cd AiStocks
```

### 2. 환경 변수 설정

프로젝트 루트 디렉토리에 `.env` 파일을 생성하고 필요한 환경 변수를 설정합니다.

```bash
# .env 파일 예시
API_KEY=your_api_key_here
DATABASE_URL=your_database_url_here
```

### 3. 가상환경 생성 및 활성화

```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화 (macOS/Linux)
source venv/bin/activate

# 가상환경 활성화 (Windows)
venv\Scripts\activate
```

### 4. 의존성 설치

```bash
pip install -r requirements.txt
```

## 실행 방법

```bash
python main.py
```

## 프로젝트 구조

```
AiStocks/
├── README.md
├── requirements.txt
├── .env
├── venv/
└── src/
    ├── models/
    ├── utils/
    └── main.py
```

## 기술 스택

- Python 3.x
- 주요 라이브러리: (requirements.txt 참조)

## 라이선스

MIT License

## 기여하기

프로젝트에 기여하고 싶으시다면 Pull Request를 보내주세요!

## 문의

프로젝트 관련 문의사항이 있으시면 Issue를 등록해주세요.