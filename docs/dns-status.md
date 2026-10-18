# DNS 현황 스냅샷

- 생성 시각: 2026-10-18T03:51:57Z
- 원본 데이터: `docs/dns-snapshot.json` (`python dns_api.py snapshot`으로 갱신)
- 자격증명: `local/credentials.json` (Git 제외, 절대 커밋 금지)

## Cloudflare

계정 ID: `ff5fa9397a04ab0bd090bf26626f024f`

| Zone | 레코드 수 | 네임서버 |
|---|---|---|
| amazone9shop.com | 8 | david/julissa.ns.cloudflare.com |
| beautheart.com | 7 | david/julissa.ns.cloudflare.com |
| deepstronglove.com | 7 | david/julissa.ns.cloudflare.com |
| hotheartlove.com | 7 | david/julissa.ns.cloudflare.com |
| notemptme.com | 7 | david/julissa.ns.cloudflare.com |
| shutupquick.com | 6 | david/julissa.ns.cloudflare.com |
| uotoma.com | 10 | david/julissa.ns.cloudflare.com |

- Tunnel: 없음 (`my-home-server` 삭제됨)
- R2 버킷: amazone9shop, beautheart, deepstronglove, hotheartlove, notemptme, shutupquick, techlifeworld, uotoma

## Hostinger

| 도메인 | 유형 | 만료 | 네임서버 |
|---|---|---|---|
| techlifeworld.com | domain | 2027-04-09 | dns-parking.com |
| shutupquick.com | domain | 2027-04-16 | Cloudflare |
| notemptme.com | domain | 2027-04-16 | Cloudflare |
| beautheart.com | domain | 2027-04-16 | Cloudflare |
| hotheartlove.com | domain | 2027-04-16 | Cloudflare |
| deepstronglove.com | domain | 2027-04-16 | Cloudflare |
| lovetovideo.com | free_domain | - | 확인 불가 (API 404) |
| uotoma.com | domain | 2027-05-17 | Cloudflare |
| onemetalht.com | domain | 2027-06-13 | dns-parking.com |
| amazone9shop.com | domain | 2027-07-09 | Cloudflare |

## Blogger (techlifeworld.com → prfom.blogspot.com)

| 항목 | 상태 |
|---|---|
| www CNAME → ghs.google.com | 정상 |
| apex A 4개 → Google IP | 정상 |
| http://www | 200 |
| http://apex | 404 (도메인 리디렉션 미설정) |
| https | 인증서 미발급 (Blogger HTTPS 설정/발급 대기) |
