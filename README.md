# qx-rules

每天自动把 [MetaCubeX/meta-rules-dat](https://github.com/MetaCubeX/meta-rules-dat)（与 mihomo / Nikki 同源）转换成 iOS 代理软件能用的规则。

| 文件夹 | 格式 | 用途 |
|---|---|---|
| `loon/` | Loon（`DOMAIN-SUFFIX,x` / `IP-CIDR,x,no-resolve`） | **主用** |
| `rules/` | Quantumult X（`host-suffix, x, 策略`） | 备用 / 给朋友 |

- 更新时间：QX 规则北京时间 04:00（`update.yml`），Loon 规则 04:30（`update-loon.yml`）。
- 引用地址：`https://testingcf.jsdelivr.net/gh/huashiren88/qx-rules@main/loon/<名>.list`（QX 把 `loon/` 换成 `rules/`）。
- 新增规则集：改 `convert.py` 里的 `GEOSITE` / `GEOIP` 列表，两种格式会一起生成。
- 仓库名保留 `qx-rules` 不改，避免所有配置里的规则地址失效。
