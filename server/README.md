# 실서비스 연결 설계

## 데이터 수집
1. TikTok: Creative Center의 공개 Trends/허용 API 범위에서 JP + food/K-Food 신호 수집
2. Instagram: Meta/Instagram Graph API에서 허용된 Business/Creator 및 미디어 범위 수집
3. Google Trends: JP 검색 급상승/관심도 데이터를 합법적 접근 방식으로 수집
4. Japan Web: RSS/공개 검색으로 韓国グルメ, 韓国食品, 韓国お菓子, 韓国ラーメン, 韓国スイーツ 등을 매일 수집
5. Qoo10: QAPI 인증 후 상품/경쟁상품 정보를 수집

## 권장 백엔드
FastAPI + PostgreSQL + Redis(선택) + cron/GitHub Actions/Cloud Scheduler

## 엔드포인트
GET /api/trends?geo=JP&category=food
GET /api/trends/{entity_id}
GET /api/qoo10/competition?q=...
POST /api/collect/run

## DB 핵심
trend_entity: canonical_name, japanese_names, category, created_at
signal_snapshot: entity_id, source, metric, value, captured_at
qoo10_snapshot: entity_id, seller_count, median_price, review_count, captured_at
trend_score: entity_id, score, delta_24h, delta_7d, confidence, captured_at

## 점수
Trend Priority =
TikTok 30
Instagram 20
Search 20
Japan Media 15
Novelty 10
Qoo10 competition inverse 5

점수는 상품 성공확률이 아니라 '조사 우선순위'다.
