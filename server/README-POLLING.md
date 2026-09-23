# API Polling v1

현재 저장소의 기존 설계(`/api/trends`, `/api/collect/run` 등)에 맞춰
서버 측 수집 오케스트레이션을 먼저 추가한 버전입니다.

## 구조

POST /api/collect/run
        ↓
수집 오케스트레이터
        ↓
TikTok / Instagram / Qoo10 collector
        ↓
정규화
        ↓
DB
        ↓
GET /api/trends
        ↓
웹사이트

Google Trends는 비공식 페이지 스크래핑을 넣지 않고,
사용 가능한 합법적/허용된 데이터 접근 방식을 확정한 뒤 별도 collector로 연결합니다.

## 중요한 보안 원칙

- API Key는 GitHub에 올리지 않습니다.
- 실제 키는 배포 환경의 Environment Variables에 넣습니다.
- `.env.example`은 빈 값만 포함합니다.
- `/api/collect/run`에는 `POLLING_SECRET`을 설정할 수 있습니다.

## Polling 실행기

Vercel에서 장시간 실행되는 프로세스를 띄우는 대신,
배포 환경의 Cron / GitHub Actions / Cloud Scheduler 중 하나가
주기적으로 `POST /api/collect/run`을 호출하도록 연결합니다.

현재 파일은 "수집 API가 준비된 상태"까지 구현합니다.
실제 TikTok/Meta/Qoo10 API 필드 매핑과 PostgreSQL 저장은
각 API의 승인된 스펙에 맞춰 다음 단계에서 연결합니다.
