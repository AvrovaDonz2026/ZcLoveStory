# 社长恋爱物语

WebGAL 版网页端 galgame 骨架，面向 Cloudflare Pages 静态部署。

## 当前状态

- 使用 WebGAL 4.6.1 网页发行包。
- `木头` 是社长。
- v1 包含半匿名完整主线、第一版视觉资产包和 WebGAL 模板微调。
- 公开包只包含匿名化/改绘/生成资产，不包含原始资料截图或原始 PDF。
- 入口目录：`site`

## 本地预览

```bash
python3 -m http.server 4173 --directory site
```

打开 `http://127.0.0.1:4173`。

## Cloudflare Pages

- Build command：留空或 `exit 0`
- Build output directory：`site`

更多说明见 `docs/deploy.md`。
