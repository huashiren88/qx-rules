"""把 MetaCubeX 规则集转换成 Quantumult X 格式，输出到 rules/ 目录。
GitHub Actions 每天运行一次（见 .github/workflows/update.yml）。"""
import os
import urllib.request

BASE = "https://raw.githubusercontent.com/MetaCubeX/meta-rules-dat/meta"

# 与 Nikki 配置里用到的规则集一一对应
GEOSITE = [
    "private", "google-gemini", "category-ai-!cn", "telegram", "youtube", "netflix",
    "apple-intelligence", "apple@cn", "apple", "twitter", "instagram", "facebook", "tiktok", "disney",
    "spotify", "amazon", "paypal", "github", "category-cryptocurrency", "bilibili",
    "linkedin", "onedrive", "xbox", "google-scholar", "category-scholar-!cn",
    "microsoft", "nvidia", "google", "fastly", "duolingo", "steam@cn", "steam",
    "nintendo@cn", "nintendo", "epicgames", "playstation", "hbo", "mytvsuper",
    "bahamut", "primevideo", "talkatone", "category-emby", "category-communication",
    "category-social-media-!cn", "category-game-platforms-download", "xunlei",
    "speedtest", "category-speedtest", "tencent", "bytedance", "alibaba", "baidu",
    "xiaohongshu", "jd", "pinduoduo", "meituan", "kuaishou", "sina", "zhihu",
    "category-games@cn", "netease", "mihoyo", "taptap", "iqiyi", "youku", "douyu",
    "huya", "huawei", "xiaomi", "category-pt", "category-public-tracker", "cn",
    "reddit", "category-porn", "category-games", "category-ecommerce",
    "category-entertainment", "category-dev", "geolocation-!cn",
    # 国内大厂的海外业务（@!cn 标签，2026-11-01 加）：放在各公司直连规则前走代理
    "bilibili@!cn", "bytedance@!cn", "tencent@!cn", "alibaba@!cn", "huawei@!cn", "sina@!cn",
    "jd@!cn", "xiaohongshu@!cn", "xiaomi@!cn", "netease@!cn", "taptap@!cn", "iqiyi@!cn",
]
# (输出名, 源路径)
GEOIP = [
    ("private", "geo/geoip/private"), ("cn", "geo/geoip/cn"), ("telegram", "geo/geoip/telegram"),
    ("twitter", "geo/geoip/twitter"), ("facebook", "geo/geoip/facebook"),
    ("google", "geo/geoip/google"), ("netflix", "geo/geoip/netflix"),
    ("apple", "geo-lite/geoip/apple"),
]


def fetch(path):
    url = f"{BASE}/{path}.list"
    with urllib.request.urlopen(url, timeout=60) as r:
        return [l.strip() for l in r.read().decode("utf-8").splitlines()
                if l.strip() and not l.startswith("#")]


def write(name, lines, src):
    os.makedirs("rules", exist_ok=True)
    with open(f"rules/{name}.list", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# NAME: {name}\n# SOURCE: MetaCubeX/meta-rules-dat {src}\n# TOTAL: {len(lines)}\n")
        f.write("\n".join(lines) + "\n")


def main():
    for n in GEOSITE:
        out = []
        for d in fetch(f"geo/geosite/{n}"):
            if d.startswith("+."):
                out.append(f"host-suffix, {d[2:]}, {n}")
            else:
                out.append(f"host, {d}, {n}")
        write(f"geosite-{n}", out, f"geosite/{n}")
    for name, path in GEOIP:
        out = []
        for c in fetch(path):
            kind = "ip6-cidr" if ":" in c else "ip-cidr"
            out.append(f"{kind}, {c}, geoip-{name}, no-resolve")
        write(f"geoip-{name}", out, path)


if __name__ == "__main__":
    main()
