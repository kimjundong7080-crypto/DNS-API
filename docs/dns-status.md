# DNS 현황 스냅샷

- 생성 시각: 2026-10-18T10:12Z (techlifeworld.com Cloudflare 이전 → 원복)
- 원본 데이터: `docs/dns-snapshot.json` (`python dns_api.py snapshot`으로 갱신)
- 자격증명: `local/credentials.json` (Git 제외, 절대 커밋 금지)

## Cloudflare

계정 ID: `ff5fa9397a04ab0bd090bf26626f024f`

| Zone | 레코드 수 | 네임서버 |
|---|---|---|
| amazone9shop.com | 8 | david/julissa.ns.cloudflare.com |
| beautheart.com | 10 | david/julissa.ns.cloudflare.com |
| deepstronglove.com | 7 | david/julissa.ns.cloudflare.com |
| hotheartlove.com | 7 | david/julissa.ns.cloudflare.com |
| notemptme.com | 10 | david/julissa.ns.cloudflare.com |
| shutupquick.com | 6 | david/julissa.ns.cloudflare.com |
| uotoma.com | 10 | david/julissa.ns.cloudflare.com |

techlifeworld.com zone은 2026-10-18 삭제됨 (생성 후 원복).

- Tunnel: 없음 (`my-home-server` 삭제됨)
- R2 버킷: amazone9shop, beautheart, deepstronglove, hotheartlove, notemptme, shutupquick, techlifeworld, uotoma

## Hostinger

| 도메인 | 유형 | 만료 | 네임서버 |
|---|---|---|---|
| techlifeworld.com | domain | 2027-04-09 | dns-parking.com (원복) |
| shutupquick.com | domain | 2027-04-16 | Cloudflare |
| notemptme.com | domain | 2027-04-16 | Cloudflare |
| beautheart.com | domain | 2027-04-16 | Cloudflare |
| hotheartlove.com | domain | 2027-04-16 | Cloudflare |
| deepstronglove.com | domain | 2027-04-16 | Cloudflare |
| lovetovideo.com | free_domain | - | 확인 불가 (API 404) |
| uotoma.com | domain | 2027-05-17 | Cloudflare |
| onemetalht.com | domain | 2027-06-13 | dns-parking.com |
| amazone9shop.com | domain | 2027-07-09 | Cloudflare |

## Blogger 연결 (2건)

| 도메인 | 블로그 | A | www CNAME | 메일 | 상태 |
|---|---|---|---|---|---|
| beautheart.com | techpodto.blogspot.com | Google 4 IP (DNS only) | ghs.google.com | 유지 | Blogger 도메인 추가 대기 |
| notemptme.com | timemaina.blogspot.com | Google 4 IP (DNS only) | ghs.google.com | 유지 | Blogger 도메인 추가 대기 |

- CAA 없음 → Google 인증서 발급 가능
- Google 원본 직접 요청 시 404 (Blogger 매핑 전 정상)
- `mail.notemptme.com` A 레코드 없음 → MX 대상 미해석 (전환 전부터 존재한 상태)
- 기존 사이트 백업: `docs/backup-beautheart-20261018.json`, `docs/backup-notemptme-20261018.json`
