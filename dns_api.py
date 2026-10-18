#!/usr/bin/env python3
"""DNS-API: Cloudflare / Hostinger / Blogger DNS helper (stdlib only)."""

import argparse
import json
import os
import sys
import urllib.error
import urllib.request

CF_BASE = "https://api.cloudflare.com/client/v4"
HS_BASE = "https://developers.hostinger.com/api"
BLOGGER_A = [
    "216.239.32.21",
    "216.239.34.21",
    "216.239.36.21",
    "216.239.38.21",
]
BLOGGER_CNAME = "ghs.google.com"


def out(value):
    print(json.dumps(value, indent=2, ensure_ascii=False))


def api(method, url, token, body=None):
    data = json.dumps(body).encode("utf-8") if body is not None else None
    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Authorization", "Bearer " + token)
    req.add_header("Accept", "application/json")
    req.add_header("User-Agent", "dns-api/1.0")
    if data is not None:
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            raw = resp.read().decode("utf-8")
            return resp.status, json.loads(raw) if raw else None
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        try:
            payload = json.loads(raw)
        except ValueError:
            payload = raw
        return exc.code, payload


def need(name):
    value = os.environ.get(name)
    if not value:
        sys.exit("environment variable %s is required" % name)
    return value


def cf_token():
    return need("CF_API_TOKEN")


def cf_account():
    return need("CF_ACCOUNT_ID")


def cf_zones(_args):
    code, payload = api("GET", CF_BASE + "/zones?per_page=50", cf_token())
    if code != 200:
        out(payload)
        return 1
    rows = [
        {"id": z["id"], "name": z["name"], "status": z["status"]}
        for z in payload["result"]
    ]
    out(rows)
    return 0


def resolve_zone(zone):
    """Return a zone id; accept either an id or a zone name."""
    if len(zone) == 32 and all(c in "0123456789abcdef" for c in zone.lower()):
        return zone
    code, payload = api(
        "GET", CF_BASE + "/zones?name=" + zone + "&per_page=50", cf_token()
    )
    if code != 200:
        sys.exit("cannot resolve zone %s: %s" % (zone, payload))
    matches = payload.get("result") or []
    if not matches:
        sys.exit("zone not found: " + zone)
    return matches[0]["id"]


def cf_records(args):
    zone = resolve_zone(args.zone)
    code, payload = api(
        "GET",
        CF_BASE + "/zones/" + zone + "/dns_records?per_page=100",
        cf_token(),
    )
    if code != 200:
        out(payload)
        return 1
    rows = [
        {
            "type": r["type"],
            "name": r["name"],
            "content": r["content"],
            "proxied": r.get("proxied"),
            "ttl": r.get("ttl"),
            "id": r["id"],
        }
        for r in payload["result"]
    ]
    out(rows)
    return 0


def cf_find(zone, rtype, name):
    code, payload = api(
        "GET",
        CF_BASE
        + "/zones/"
        + zone
        + "/dns_records?type="
        + rtype
        + "&name="
        + name
        + "&per_page=100",
        cf_token(),
    )
    if code != 200:
        return None
    found = payload.get("result") or []
    return found[0] if found else None


def cf_find_all(zone, rtype, name):
    code, payload = api(
        "GET",
        CF_BASE
        + "/zones/"
        + zone
        + "/dns_records?type="
        + rtype
        + "&name="
        + name
        + "&per_page=100",
        cf_token(),
    )
    if code != 200:
        return []
    return payload.get("result") or []


def cf_record_set(args):
    zone = resolve_zone(args.zone)
    body = {
        "type": args.type,
        "name": args.name,
        "content": args.content,
        "ttl": args.ttl,
        "proxied": args.proxied,
    }
    existing = cf_find(zone, args.type, args.name)
    token = cf_token()
    if existing:
        url = CF_BASE + "/zones/" + zone + "/dns_records/" + existing["id"]
        code, payload = api("PUT", url, token, body)
    else:
        url = CF_BASE + "/zones/" + zone + "/dns_records"
        code, payload = api("POST", url, token, body)
    out(payload)
    return 0 if code in (200, 201) else 1


def cf_record_delete(args):
    zone = resolve_zone(args.zone)
    existing = cf_find(zone, args.type, args.name)
    if not existing:
        sys.exit("record not found: %s %s" % (args.type, args.name))
    url = CF_BASE + "/zones/" + zone + "/dns_records/" + existing["id"]
    code, payload = api("DELETE", url, cf_token())
    out(payload)
    return 0 if code == 200 else 1


def cf_tunnels(_args):
    url = CF_BASE + "/accounts/" + cf_account() + "/cfd_tunnel?is_deleted=false"
    code, payload = api("GET", url, cf_token())
    if code != 200:
        out(payload)
        return 1
    rows = [
        {
            "id": t["id"],
            "name": t["name"],
            "status": t["status"],
            "connections": len(t.get("connections") or []),
            "config_src": t.get("config_src"),
        }
        for t in payload["result"]
    ]
    out(rows)
    return 0


def cf_tunnel_delete(args):
    url = (
        CF_BASE
        + "/accounts/"
        + cf_account()
        + "/cfd_tunnel/"
        + args.id
        + "?cascade=true"
    )
    code, payload = api("DELETE", url, cf_token())
    out(payload)
    return 0 if code == 200 else 1


def cf_tunnel_config(args):
    url = (
        CF_BASE
        + "/accounts/"
        + cf_account()
        + "/cfd_tunnel/"
        + args.id
        + "/configurations"
    )
    code, payload = api("GET", url, cf_token())
    out(payload)
    return 0 if code == 200 else 1


def hs_domains(_args):
    code, payload = api(
        "GET", HS_BASE + "/domains/v1/portfolio", need("HOSTINGER_API_TOKEN")
    )
    if code != 200:
        out(payload)
        return 1
    out(payload)
    return 0


def hs_domain(args):
    url = HS_BASE + "/domains/v1/portfolio/" + args.domain
    code, payload = api("GET", url, need("HOSTINGER_API_TOKEN"))
    out(payload)
    return 0 if code == 200 else 1


def hs_ns_set(args):
    url = HS_BASE + "/domains/v1/portfolio/" + args.domain + "/nameservers"
    body = {"ns1": args.ns1, "ns2": args.ns2}
    code, payload = api("PUT", url, need("HOSTINGER_API_TOKEN"), body)
    out(payload)
    return 0 if code == 200 else 1


def blogger_setup(args):
    """Point a Cloudflare zone at Blogger (Google) with DNS-only records."""
    token = cf_token()
    zone = resolve_zone(args.zone)
    results = []

    existing = cf_find_all(zone, "A", args.zone)
    for index, ip in enumerate(BLOGGER_A):
        body = {
            "type": "A",
            "name": args.zone,
            "content": ip,
            "ttl": 3600,
            "proxied": False,
        }
        if index < len(existing):
            url = CF_BASE + "/zones/" + zone + "/dns_records/" + existing[index]["id"]
            code, payload = api("PUT", url, token, body)
        else:
            url = CF_BASE + "/zones/" + zone + "/dns_records"
            code, payload = api("POST", url, token, body)
        results.append({"record": "A " + args.zone + " -> " + ip, "status": code})

    extra = existing[len(BLOGGER_A):]
    for record in extra:
        url = CF_BASE + "/zones/" + zone + "/dns_records/" + record["id"]
        code, payload = api("DELETE", url, token)
        results.append(
            {"record": "DELETE A " + args.zone + " -> " + record["content"], "status": code}
        )

    body = {
        "type": "CNAME",
        "name": "www." + args.zone,
        "content": BLOGGER_CNAME,
        "ttl": 3600,
        "proxied": False,
    }
    existing_cname = cf_find(zone, "CNAME", "www." + args.zone)
    if existing_cname:
        url = CF_BASE + "/zones/" + zone + "/dns_records/" + existing_cname["id"]
        code, payload = api("PUT", url, token, body)
    else:
        url = CF_BASE + "/zones/" + zone + "/dns_records"
        code, payload = api("POST", url, token, body)
    results.append(
        {"record": "CNAME www." + args.zone + " -> " + BLOGGER_CNAME, "status": code}
    )
    out(results)
    return 0 if all(r["status"] in (200, 201) for r in results) else 1


def build_parser():
    parser = argparse.ArgumentParser(prog="dns-api", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("cf-zones", help="list Cloudflare zones")
    p.set_defaults(func=cf_zones)

    p = sub.add_parser("cf-records", help="list DNS records of a zone")
    p.add_argument("--zone", required=True, help="zone id or name")
    p.set_defaults(func=cf_records)

    p = sub.add_parser("cf-record-set", help="create or update a DNS record")
    p.add_argument("--zone", required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--name", required=True)
    p.add_argument("--content", required=True)
    p.add_argument("--ttl", type=int, default=3600)
    p.add_argument("--proxied", action="store_true")
    p.set_defaults(func=cf_record_set)

    p = sub.add_parser("cf-record-delete", help="delete a DNS record by name/type")
    p.add_argument("--zone", required=True)
    p.add_argument("--type", required=True)
    p.add_argument("--name", required=True)
    p.set_defaults(func=cf_record_delete)

    p = sub.add_parser("cf-tunnels", help="list Cloudflare tunnels")
    p.set_defaults(func=cf_tunnels)

    p = sub.add_parser("cf-tunnel-config", help="show tunnel ingress config")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cf_tunnel_config)

    p = sub.add_parser("cf-tunnel-delete", help="delete a tunnel (cascade)")
    p.add_argument("--id", required=True)
    p.set_defaults(func=cf_tunnel_delete)

    p = sub.add_parser("hs-domains", help="list Hostinger domain portfolio")
    p.set_defaults(func=hs_domains)

    p = sub.add_parser("hs-domain", help="show one Hostinger domain")
    p.add_argument("domain")
    p.set_defaults(func=hs_domain)

    p = sub.add_parser("hs-ns-set", help="set nameservers of a Hostinger domain")
    p.add_argument("domain")
    p.add_argument("--ns1", required=True)
    p.add_argument("--ns2", required=True)
    p.set_defaults(func=hs_ns_set)

    p = sub.add_parser(
        "blogger-setup",
        help="create Blogger A/CNAME records in a Cloudflare zone (DNS only)",
    )
    p.add_argument("--zone", required=True, help="zone name, e.g. example.com")
    p.set_defaults(func=blogger_setup)

    return parser


def main(argv=None):
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    raise SystemExit(main())
