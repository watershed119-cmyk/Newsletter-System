# 글로벌 물환경 동향 뉴스레터 (자동 발송)

5개국(미국·EU·일본·한국·호주) 물환경 뉴스를 RSS로 수집하고, 관련성 분류 후 **신규 자료가 있을 때만** SMTP 이메일로 발송하는 Python 앱입니다.

기존 `agents/`·`skills/`는 편집 가이드로 유지되며, 실제 자동 실행은 `water_newsletter` 패키지와 GitHub Actions가 담당합니다.

## 기능

- Google News RSS 기반 5개국 물환경 자료 수집
- 키워드·기관 도메인 기준 1티어/2티어 분류
- 주간(월요일)·월간(말일) 뉴스레터 형식 자동 편집
- 신규 관련 자료 없으면 메일 생략
- GitHub Actions 평일/월말 예약 실행
- (선택) `ANTHROPIC_API_KEY`로 1티어 한국어 3줄 요약 품질 향상

## 스케줄

| 유형 | 실행 시각 | 조건 |
|------|-----------|------|
| 주간 | 매주 월요일 07:00 KST | 관련 자료 1건 이상 |
| 월간 | 매월 말일 07:00 KST | 관련 자료 1건 이상 |

## 준비물

1. Gmail SMTP(앱 비밀번호) 또는 SMTP 계정
2. (선택) Anthropic API 키 — 한국어 요약 품질 향상

## 환경 변수

| 변수 | 필수 | 설명 |
| --- | --- | --- |
| `EMAIL_TO` | 예* | 수신자 CSV (*`config.json` recipients 대체) |
| `SMTP_HOST` | 예 | SMTP 서버 |
| `SMTP_PORT` | 아니오 | 기본 587 |
| `SMTP_USERNAME` | 권장 | SMTP 로그인 |
| `SMTP_PASSWORD` | 권장 | SMTP 비밀번호 |
| `SMTP_SENDER` | 아니오 | 발신자 주소 |
| `ANTHROPIC_API_KEY` | 아니오 | 1티어 한국어 요약용 |
| `STATE_FILE` | 아니오 | 호수 이력 파일 (기본 `.state/newsletter.json`) |

수신자 기본값은 `config.json`의 `recipients`입니다.

## 로컬 실행

```bash
python -m venv .venv
.venv\Scripts\activate
pip install ".[dev]"

copy .env.example .env
# .env에 SMTP 값 입력

water-newsletter weekly --dry-run
water-newsletter weekly
water-newsletter monthly --force --dry-run
```

## GitHub Actions 설정

저장소 **Settings → Secrets → Actions**에 등록:

- `EMAIL_TO`
- `SMTP_HOST`, `SMTP_PORT`, `SMTP_USERNAME`, `SMTP_PASSWORD`
- `SMTP_SENDER` (선택)
- `ANTHROPIC_API_KEY` (선택)

Actions → **Water newsletter** → **Run workflow**로 수동 테스트:

- `weekly` — 주간 뉴스레터
- `monthly` — 월간 뉴스레터

### 실행·오류 확인

- **관련 자료 없음**: 메일 없음, Actions **초록색**, 로그 `No relevant articles; email skipped`
- **오류**: Actions **빨간색** — SMTP/API 문제 확인
- GitHub **Settings → Notifications → Actions** 실패 알림 권장

## 프로젝트 구조

```
agents/          # 기존 Claude Agent 정의 (참고용)
skills/          # 뉴스레터 형식·분류 가이드
config.json      # 수신자, 발행 호수, 시스템명
water_newsletter/  # 자동 실행 Python 패키지
.github/workflows/newsletter.yml
```

## 운영 팁

- RSS 수집량은 Google News 결과에 따라 달라질 수 있습니다.
- 한국어 요약 품질이 중요하면 `ANTHROPIC_API_KEY`를 Secrets에 등록하세요.
- API 키·비밀번호는 README나 git에 넣지 마세요.
