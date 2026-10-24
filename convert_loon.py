"""把 MetaCubeX 规则集转换成 Loon 规则格式，输出到 loon/ 目录。
规则清单直接复用 convert.py 里的 GEOSITE / GEOIP，保证和 QX 那套一致。
GitHub Actions 每天运行一次（见 .github/workflows/update-loon.yml）。"""
import os

from convert import GEOSITE, GEOIP, fetch


def write(name, lines, src):
    os.makedirs("loon", exist_ok=True)
    with open(f"loon/{name}.list", "w", encoding="utf-8", newline="\n") as f:
        f.write(f"# NAME: {name}\n# SOURCE: MetaCubeX/meta-rules-dat {src}\n# TOTAL: {len(lines)}\n")
        f.write("\n".join(lines) + "\n")


def main():
    for n in GEOSITE:
        out = []
        for d in fetch(f"geo/geosite/{n}"):
            if d.startswith("+."):
                out.append(f"DOMAIN-SUFFIX,{d[2:]}")
            else:
                out.append(f"DOMAIN,{d}")
        write(f"geosite-{n}", out, f"geosite/{n}")
    for name, path in GEOIP:
        out = []
        for c in fetch(path):
            kind = "IP-CIDR6" if ":" in c else "IP-CIDR"
            out.append(f"{kind},{c},no-resolve")
        write(f"geoip-{name}", out, path)


if __name__ == "__main__":
    main()
