# <h3>네이버 뉴스 토픽 분석과 부동산 데이터 시각화</h2>

## 🚀 프로젝트 목적
- **뉴스 분석**: 주요 뉴스 주제를 빠르게 파악하고 관련 기사 확인 가능
- **부동산 정보 제공**: 사용자에게 유용한 부동산 시세 정보를 시각적으로 전달

---

## 📂 사이드바 메뉴
<img src="./assets/2.png" alt="이미지" width="500">
### 1. 네이버 뉴스
- **카테고리 선택**:
  - 정치, 경제, 사회, 생활/문화, IT/과학, 세계 섹션 중 사용자가 원하는 뉴스 섹션을 선택할 수 있습니다.
- **토픽 모델링 & 워드 클라우드**:
  - 최신 기사를 기반으로 **LDA 토픽 모델링**을 실행하여 주요 주제를 파악할 수 있습니다.
  - 각 주제(토픽)에 대해 워드 클라우드를 통해 키워드를 시각적으로 확인 가능합니다.
  - 특정 토픽을 선택하면 해당 주제와 관련된 기사를 볼 수 있습니다.
- **최신 기사 보기**:
  - ‘최신 뉴스 보기’ 버튼을 클릭하여 최신 뉴스의 제목과 추천 수를 확인할 수 있습니다.
  - 멀티페이지 구조로 구현되어 간편하게 뉴스 데이터를 탐색할 수 있으며, 제목을 클릭하면 기사 본문으로 연결됩니다.

### 2. 부동산 데이터
- **아파트 정보 확인**:
  - 서초구의 최신 아파트 정보를 크롤링하여 사용자에게 정보를 제공합니다.
  - 데이터를 시각적으로 효과적으로 전달하기 위해 다양한 그래프를 활용하였습니다.
  - 서초구의 동별 아파트 정보를 확인할 수 있습니다. (제공되는 정보: 단지명, 매매, 전세, 면적, 가격 등)
- **데이터 시각화**:
  - 평당 매매 아파트 가격을 그래프로 확인할 수 있습니다.
  - 동별 평균 매매/전세 데이터를 시각적으로 제공하여 이해도를 높였습니다.

---

## 💡 주요 기능 요약
### 사용자 친화적인 인터페이스:
- 사이드바를 통해 직관적으로 메뉴를 선택하고 탐색 가능
- 각 기능이 별도 페이지로 분리되어 깔끔하고 명확한 데이터 탐색 가능

### 데이터 기반 인사이트 제공:
- 네이버 뉴스의 최신 동향 및 주요 토픽 확인
- 부동산 데이터를 시각화하여 사용자 의사결정 지원

---

## 🔧 기술 스택
- **Frontend**: Streamlit  
- **Backend**: Python  
- **데이터 분석**: scikit-learn, Gensim, nltk, konlpy  
- **데이터 시각화**: WordCloud, Matplotlib, Plotly  
- **토픽 모델링**: LDA (Latent Dirichlet Allocation)
