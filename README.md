# DNS-API

Cloudflare / Hostinger DNS를 터미널에서 다루는 단일 파일 CLI입니다. 외부 패키지 없이 Python 3.8+ 표준 라이브러리만 사용합니다.

## 환경 변수

```powershell
$env:CF_API_TOKEN       = "Cloudflare API 토큰"
$env:CF_ACCOUNT_ID      = "Cloudflare 계정 ID"
$env:HOSTINGER_API_TOKEN = "Hostinger API 토큰"
```

`.env` 파일은 지원하지 않습니다. 셸 환경 변수나 시크릿 매니저를 사용하세요.

## 사용법

```powershell
python dns_api.py cf-zones
python dns_api.py cf-records --zone example.com
python dns_api.py cf-record-set --zone example.com --type TXT --name example.com --content "v=spf1 ~all"
python dns_api.py cf-record-delete --zone example.com --type TXT --name example.com
python dns_api.py cf-tunnels
python dns_api.py cf-tunnel-config --id <tunnel-id>
python dns_api.py cf-tunnel-delete --id <tunnel-id>
python dns_api.py hs-domains
python dns_api.py hs-domain example.com
python dns_api.py hs-ns-set example.com --ns1 ns1.example.net --ns2 ns2.example.net
python dns_api.py blogger-setup --zone example.com
```

## Blogger 연결

`blogger-setup`은 Cloudflare zone에 다음 레코드를 만듭니다. 모두 **프록시 끔(DNS only)** 입니다.

| 타입 | 이름 | 값 |
|---|---|---|
| A | `example.com` | `216.239.32.21`, `216.239.34.21`, `216.239.36.21`, `216.239.38.21` |
| CNAME | `www.example.com` | `ghs.google.com` |

DNS 이후 단계는 Blogger UI에서만 가능합니다.

1. 설정 → 게시중단 → 맞춤 도메인에 `www.example.com` 입력 후 저장
2. `example.com` → `www.example.com` 리디렉션 켜기
3. HTTPS 사용 설정 (인증서 발급까지 최대 24시간)

Hostinger API는 도메인 DNS 레코드 편집 기능을 제공하지 않습니다(네임서버 변경만 가능). DNS 레코드를 API로 관리하려면 zone을 Cloudflare로 이전해야 합니다.

## 주의

- 자격증명을 코드나 저장소에 커밋하지 마세요.
- `cf-tunnel-delete`, `hs-ns-set`, `cf-record-delete`는 되돌릴 수 없는 작업입니다.
- Blogger 연결 시 Cloudflare 프록시를 켜면 Google 인증서 발급·검증이 실패할 수 있습니다.
