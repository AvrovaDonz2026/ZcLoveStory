# 部署说明

本项目使用 WebGAL 4.6.1 网页发行包作为静态运行时，游戏工程位于 `site/game`。

## Cloudflare Pages

- Build command：留空或 `exit 0`
- Build output directory：`site`
- Framework preset：None / Static HTML

`site/_redirects` 已配置为：

```txt
/* /index.html 200
```

`site/_headers` 对图片、音频、视频目录设置长期缓存，对 `game/config.txt` 和 `game/scene/*` 设置 `no-cache`。

## GitHub Pages

本仓库使用 GitHub Actions 部署 GitHub Pages，避免把 `site/` 搬到仓库根目录或 `/docs`。

- Workflow：`.github/workflows/pages.yml`
- 触发：推送到 `main`，或手动 `workflow_dispatch`
- Artifact path：`site`

GitHub 仓库设置里需要将 Pages 的 Build and deployment / Source 设为 `GitHub Actions`。之后每次推送 `main`，workflow 会把 `site/` 打包并通过 `actions/deploy-pages` 发布。

## 本地预览

在仓库根目录运行任意静态服务器，例如：

```bash
python3 -m http.server 4173 --directory site
```

然后打开：

```text
http://127.0.0.1:4173
```

## 内容编辑

- 入口脚本：`site/game/scene/start.txt`
- 人物关系：`site/game/scene/cast.txt`
- 时间线：`site/game/scene/timeline.txt`
- 资料陈列室：`site/game/scene/evidence_room.txt`
- 游戏配置：`site/game/config.txt`

可以使用 WebGAL Terre 打开或导出 `site/game` 兼容的工程内容。后续若替换 WebGAL 运行时，只替换 `site` 中的引擎文件，保留 `site/game`。
