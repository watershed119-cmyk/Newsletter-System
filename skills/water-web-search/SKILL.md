---
name: water-web-search
description: |
  5개국(미국·EU·일본·한국·호주) 지정 물환경 소스에서 최신 콘텐츠를
  검색·수집하는 방법을 안내합니다.
  사용 시점: web-collector Agent가 주간 또는 월간 수집 작업을 시작할 때.
---
## 수집 소스 목록
| 국가 | 기관·소스 | URL | 우선순위 |
|-----|---------|-----|------|
| USA | US EPA Water | https://www.epa.gov/environmental-topics/water-topics | 높음 |
| USA | USGS Water Resources | https://www.usgs.gov/water-resources | 높음 |
| USA | Water Environment Federation | https://www.wef.org/news-hub | 중간 |
| EU | European Environment Agency | https://www.eea.europa.eu/themes/water | 높음 |
| EU | EC Environment – Water | https://environment.ec.europa.eu/topics/water | 높음 |
| Japan | 環境省 水・土壌環境 | https://www.env.go.jp/water | 높음 |
| Japan | 国立環境研究所 (NIES) | https://www.nies.go.jp/whatsnew | 중간 |
| Korea | 환경부 | https://www.me.go.kr | 높음 |
| Korea | 국립환경과학원 | https://www.nier.go.kr | 높음 |
| Korea | 물환경정보시스템 | https://water.nier.go.kr | 중간 |
| Australia | DCCEEW Water | https://www.dcceew.gov.au/water | 높음 |
| Australia | CSIRO Water | https://www.csiro.au/en/research/natural-environment/water | 중간 |
| Academic | Water Research (Elsevier) | https://www.sciencedirect.com/journal/water-research | 중간 |
| Academic | Environmental Science & Technology | https://pubs.acs.org/journal/esthag | 중간 |
## 검색어 세트
### 영어 (EPA, EEA, DCCEEW, WEF, 학술)
"water quality" OR "water pollution" OR "watershed management"
OR "nonpoint source pollution" OR "aquatic ecosystem"
OR "PFAS water" OR "microplastics water" OR "water regulation" OR "water standard"
### 일본어 (env.go.jp, nies.go.jp)
水質 OR 水環境 OR 流域管理 OR 非点源汚染 OR 水生態系 OR 底質
### 한국어 (me.go.kr, nier.go.kr, water.nier.go.kr)
수질 OR 수환경 OR 유역관리 OR 비점오염 OR 수생태계 OR 수생태 OR 하천 OR 호소 OR 오염총량
## 수집 절차
1. 각 소스별 web_search 실행 (검색어 조합 + 소스 도메인 키워드)
2. 결과 중 관련성 높아 보이는 URL에 web_fetch 적용
3. 발행일 확인 → 기간 필터 미충족 시 제외
4. 제목·URL·발행일·기관·요약 추출
5. 중복 URL 제거 후 반환
## 기간 필터
- weekly 수집: 최근 7일 이내
- monthly 수집: 최근 30일 이내
## 수집 목표량
- 주간: 15~30건 (우선순위 '높음' 소스 먼저)
- 월간: 20~40건
