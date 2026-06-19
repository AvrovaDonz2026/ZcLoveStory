# 《社长恋爱物语》资产计划

本项目首版 WebGAL 骨架与第一版视觉包已经收口。后续使用 GPT Image 2 或其他流程产出的公开资产，必须先完成匿名化和隐私审核，再放入 `site/game`。

## 目录约定

- 背景：`site/game/background/<group>/`
- 立绘：`site/game/figure/<character>/`
- CG：`site/game/background/cg/`
- 证据全屏图：`site/game/background/evidence/`
- 证据道具/浮层：`site/game/figure/props/evidence/`
- 头像：`site/game/figure/avatar/`

WebGAL 台本引用时不要写 `game/`、`background/` 或 `figure/` 前缀。播放器会按命令类型自动补目录：

- `changeBg:clubroom/bg_clubroom_night_v01.webp;` -> `site/game/background/clubroom/bg_clubroom_night_v01.webp`
- `changeFigure:sz/fig_mutou_neutral_v01.png -right;` -> `site/game/figure/sz/fig_mutou_neutral_v01.png`

文件名使用小写 ASCII、数字、`-`、`_`，避免中文、空格、冒号和全角符号。

## 命名示例

- `bg_clubroom_day_v01.webp`
- `bg_campus_gate_evening_v01.webp`
- `fig_mutou_neutral_v01.png`
- `fig_recorder_thinking_v01.png`
- `cg_ch02_vote-night_v01.webp`
- `ev_ch03_chat-redacted_01.webp`

## 生成规格

- 背景/CG：16:9，建议 1920x1080，WebP。
- 证据全屏图：16:9，建议 1920x1080 或 1600x900，WebP。
- 立绘：透明背景 PNG，建议长边 2400-3000，保留腰部以上和全身裁切空间。
- 道具/浮层：透明背景 PNG，建议 1024-2048，方便 WebGAL 叠加。
- 头像：1:1，建议 512x512，PNG 或 WebP。
- 图中文字尽量少。需要可读文本时优先留空白框，由 WebGAL 文本或后期排版覆盖，避免 AI 生成错字。

## Prompt 文档

- 第一轮 16 张绿幕参考图已生成：`site/game/reference/round1/`
- 第一轮男生角色 v02 区分版已生成：木头=黑夹克灰资料夹，记录者=浅米工装马甲+夹板笔记本，旁观者=蓝灰长开衫+眼镜+斜挎包。
- 第一批 WebGAL 可用透明 PNG 已生成：四名角色、灰色资料夹、四标签、关键词卡、评价表、匿名聊天气泡、项目卡、4月9日日期页、4月19日时间条、分开后便签。
- 第一批正式背景已生成并接入台本：活动室夜景、证据桌、证据柜、标题桌面。
- 第一版收口补充资产已生成并接入：雨天校园走廊、木头柔和立绘、记录者思考立绘、旁观者担忧立绘、同学 A 提问立绘、四个头像、标题牌 UI、文字版标题牌 UI、选择按钮 UI。
- 章节 CG / 证据图已生成并接入台本：hub、人物关系、时间线、六卡证据、第一到第六章章节图、第一/二/三/五/六章资料页、最终合上资料夹。
- 非最终图隔离目录：`site/game/reference/round1_gemini_preview/`、`site/game/reference/round1_gpt_image2_text_style_only/`
- 第一轮绿幕参考图 prompts：`docs/reference_prompts_round1.md`
- `site/game/reference/` 是本地中间资产目录，默认不提交到部署仓库；最终运行图已放入 `background`、`figure` 和 `template/assets`。
- 第一轮目标：先锁定角色、道具、资料卡、UI 壳和环境模块；后续再用这些参考图生成正式大图。

## 角色区分规则

- 木头/社长：黑色短款立领夹克、灰色衬衫、深色长裤、白鞋、灰色资料夹。
- 记录者：浅米色工装马甲、白色卷袖衬衫、橄榄棕长裤、红棕夹板笔记本、录音笔、手表。
- 旁观者：蓝灰长针织开衫、米白高领衫、圆眼镜、 tan 帆布斜挎包、小螺旋本。
- 同学 A：暖棕或砖红 hoodie / 开衫、浅色内搭、空白角色卡或松散纸张。

后续正式立绘和 CG 必须沿用这套服装/配件识别，不再让男生们只靠发型或表情区分。

## MVP 必需资产

这些是第一版“能看起来像作品”的最低图片包，优先生成。

| asset_id | category | webgal_path | scene_usage | priority | prompt_brief | privacy_review | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| bg_title_folder_table | background | `game/background/title/bg_title_folder_table_v01.webp` | 标题页、开场 | P0 | 雨夜活动室桌面，灰色资料夹、台灯、克制悬疑感，无真实标识 | passed | generated |
| bg_clubroom_night | background | `game/background/clubroom/bg_clubroom_night_v01.webp` | 序章、主线收束、人物关系 | P0 | 夜晚社团活动室，窗外雨痕，桌面有资料夹和散落纸页 | passed | generated |
| bg_archive_table | background | `game/background/evidence/bg_archive_table_v01.webp` | 第1-3章资料整理场景 | P0 | 档案室长桌，卡盒、透明夹页、便签、柔和台灯 | passed | generated |
| bg_evidence_cabinet | background | `game/background/evidence/bg_evidence_cabinet_v01.webp` | 资料陈列室 | P0 | 低光玻璃证据柜，六格卡片陈列，无真实截图 | passed | generated |
| bg_corridor_rain | background | `game/background/campus/bg_corridor_rain_v01.webp` | 4月9日旁观者视角、过场 | P1 | 校园走廊雨后傍晚，空走廊，匿名校园氛围 | passed | generated |
| fig_mutou_neutral | figure | `game/figure/sz/fig_mutou_neutral_v01.png` | 木头默认立绘 | P0 | 半匿名男生社长，沉静、克制，普通社团服装，无校徽 | passed | generated |
| fig_mutou_tired | figure | `game/figure/sz/fig_mutou_tired_v01.png` | 高压对话、4月19日 | P0 | 木头疲惫低头，眼神压住情绪，透明背景 | passed | generated |
| fig_mutou_soft | figure | `game/figure/sz/fig_mutou_soft_v01.png` | 安抚、日常回落 | P1 | 木头轻微放松、温和回应，透明背景 | passed | generated |
| fig_recorder_neutral | figure | `game/figure/protagonist/fig_recorder_neutral_v01.png` | 记录者 | P0 | 记录者半匿名立绘，拿笔记本或录音笔，冷静整理资料 | passed | generated |
| fig_recorder_thinking | figure | `game/figure/protagonist/fig_recorder_thinking_v01.png` | 记录者思考、证据核对 | P1 | 记录者拿笔记本沉思，透明背景 | passed | generated |
| fig_witness_neutral | figure | `game/figure/witness/fig_witness_neutral_v01.png` | 旁观者 | P0 | 旁观者半匿名立绘，站在侧光里，不全知但敏锐 | passed | generated |
| fig_witness_concerned | figure | `game/figure/witness/fig_witness_concerned_v01.png` | 旁观者担忧、4月9日视角 | P1 | 旁观者担忧但克制，透明背景 | passed | generated |
| fig_classmate_a_neutral | figure | `game/figure/avatar/fig_classmate_a_neutral_v01.png` | 同学A | P1 | 普通社团同学，略紧张但愿意提问，透明背景 | passed | generated |
| fig_classmate_a_question | figure | `game/figure/avatar/fig_classmate_a_question_v01.png` | 同学A提问 | P1 | 暖棕 hoodie / 开衫，拿纸提问，透明背景 | passed | generated |

## 章节 CG 与证据图

这些图负责让六章“有章节记忆点”。MVP 可先每章 1 张，后续再拆成更多细节图。

| asset_id | category | webgal_path | scene_usage | priority | prompt_brief | privacy_review | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| cg_hub_tabs | cg | `game/background/cg/cg_hub_tabs_v01.webp` | hub 菜单 | P0 | 资料夹摊开，人物关系、时间线、资料陈列室、完整主线四枚标签 | passed | generated |
| cg_cast_blank_cards | cg | `game/background/cg/cg_cast_blank_cards_v01.webp` | 人物关系 | P1 | 四张无照片角色卡并排，只有代称和职责栏，桌面台灯 | passed | generated |
| ev_timeline_index | evidence | `game/background/evidence/ev_timeline_index_v01.webp` | 时间线页 | P1 | 六章时间线索引卡，日期和章节色条，文本留空或伪字 | passed | generated |
| ev_evidence_six_cards | evidence | `game/background/evidence/ev_evidence_six_cards_v01.webp` | 资料陈列室 | P0 | 六格证据柜：关键词、具体评价、共同叙事、4月9日、4月19日、分开之后 | passed | generated |
| cg_ch01_keyword_box | cg | `game/background/cg/cg_ch01_keyword_box_v01.webp` | 第一章关键词 | P0 | 灰色卡盒，黑色索引卡与浅色对照卡，台灯下证据感 | passed | generated |
| ev_ch01_keyword_cards | evidence | `game/background/evidence/ev_ch01_keyword_cards_v01.webp` | 第一章关键词资料图 | P1 | 匿名关键词卡组，黑卡与浅卡并排，具体文字可留空后期覆盖 | passed | generated |
| cg_ch02_evaluation_table | cg | `game/background/cg/cg_ch02_evaluation_table_v01.webp` | 第二章具体评价 | P0 | 桌面表格，左栏“事情”右栏“人”的视觉结构，聊天气泡改绘 | passed | generated |
| ev_ch02_chat_bubbles | evidence | `game/background/evidence/ev_ch02_chat_bubbles_v01.webp` | 第二章资料图 | P1 | 灰白匿名聊天气泡、红线、便签，不含头像昵称时间戳 | passed | generated |
| cg_ch03_shared_story_cards | cg | `game/background/cg/cg_ch03_shared_story_cards_v01.webp` | 第三章共同叙事 | P0 | 项目表、歌单、约稿记录、通话复盘、台阶标签排成一列 | passed | generated |
| ev_ch03_project_song_commission | evidence | `game/background/evidence/ev_ch03_project_song_commission_v01.webp` | 第三章资料图 | P1 | 项目、曲子、约稿三类匿名资料卡，所有金额与外部标识留空 | passed | generated |
| cg_ch04_apr9_fold | cg | `game/background/cg/cg_ch04_apr9_fold_v01.webp` | 第四章4月9日 | P0 | 写着4月9日的折痕纸页，分开复盘、旁观者视角、同日互动三组卡片 | passed | generated |
| ev_ch04_apr11_footer | evidence | `game/background/evidence/ev_ch04_apr11_footer_v01.webp` | 第四章4月11日参照 | P2 | 4月11日作为页脚标注的小卡，不抢过4月9日主视觉 | required | needed |
| cg_ch05_night_to_day | cg | `game/background/cg/cg_ch05_night_to_day_v01.webp` | 第五章4月19日 | P0 | 从凌晨到下午的聊天时间轴，灰色气泡、上午/中午/下午标签、蓝色书签 | passed | generated |
| ev_ch05_gift_bookmark | evidence | `game/background/evidence/ev_ch05_gift_bookmark_v01.webp` | 第五章礼物与日常 | P1 | 蓝色书签、小礼物、短聊天气泡，情绪从高压转向日常 | passed | generated |
| cg_ch06_after_sticky_notes | cg | `game/background/cg/cg_ch06_after_sticky_notes_v01.webp` | 第六章分开之后 | P0 | 五张便签：5月1日、线下活动、组织事务、商品消费、后续牵连 | passed | generated |
| ev_ch06_route_and_items | evidence | `game/background/evidence/ev_ch06_route_and_items_v01.webp` | 第六章资料图 | P1 | 被擦淡的路线、会议记录边角、周边小物、便签叠放 | passed | generated |
| cg_final_closed_folder | cg | `game/background/cg/cg_final_closed_folder_v01.webp` | 完整主线收束 | P1 | 合上的灰色资料夹，六枚章节标签压平，台灯光落在封面 | passed | generated |

## 道具与浮层

这些适合做透明 PNG，用 `changeFigure` 或后续自定义 UI 叠在背景上。

| asset_id | category | webgal_path | scene_usage | priority | prompt_brief | privacy_review | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| prop_folder_gray | prop | `game/figure/props/evidence/prop_folder_gray_v01.png` | 全局资料夹 | P0 | 灰色资料夹，封面无现实标识，可放在桌面前景 | passed | generated |
| prop_tabs_four | prop | `game/figure/props/evidence/prop_tabs_four_v01.png` | hub | P0 | 四枚资料标签：完整主线、人物关系、时间线、资料陈列室 | passed | generated |
| prop_keyword_cards | prop | `game/figure/props/evidence/prop_keyword_cards_v01.png` | 第一章 | P1 | 黑色索引卡和浅色对照卡组，文字留空 | passed | generated |
| prop_table_thing_person | prop | `game/figure/props/evidence/prop_table_thing_person_v01.png` | 第二章 | P1 | 两栏评价表透明 PNG，栏目可后期覆盖文字 | passed | generated |
| prop_chat_bubbles_redacted | prop | `game/figure/props/evidence/prop_chat_bubbles_redacted_v01.png` | 第二、五章 | P0 | 匿名灰白聊天气泡组，无头像、昵称、时间戳 | passed | generated |
| prop_project_cards | prop | `game/figure/props/evidence/prop_project_cards_v01.png` | 第三章 | P1 | 项目表、歌单、约稿卡、通话复盘卡一组透明 PNG | passed | generated |
| prop_date_cards_apr9 | prop | `game/figure/props/evidence/prop_date_cards_apr9_v01.png` | 第四章 | P1 | 4月9日日期卡、折痕纸页、页脚箭头 | passed | generated |
| prop_time_labels_apr19 | prop | `game/figure/props/evidence/prop_time_labels_apr19_v01.png` | 第五章 | P1 | 凌晨、上午、中午、下午四个时间标签 | passed | generated |
| prop_blue_bookmark | prop | `game/figure/props/evidence/prop_blue_bookmark_v01.png` | 第五章 | P1 | 蓝色书签或小礼物，日常回落意象 | required | needed |
| prop_after_sticky_notes | prop | `game/figure/props/evidence/prop_after_sticky_notes_v01.png` | 第六章 | P0 | 五张便签透明 PNG，标题留空或只写抽象图形 | passed | generated |

## 头像与 UI 增强

不是第一批必须，但有了之后对 WebGAL 阅读体验提升明显。

| asset_id | category | webgal_path | scene_usage | priority | prompt_brief | privacy_review | status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| av_mutou | avatar | `game/figure/avatar/av_mutou_v01.webp` | 对话头像 | P2 | 木头头像，半匿名，不像现实照片 | passed | generated |
| av_recorder | avatar | `game/figure/avatar/av_recorder_v01.webp` | 对话头像 | P2 | 记录者头像，笔记本、冷静视角 | passed | generated |
| av_witness | avatar | `game/figure/avatar/av_witness_v01.webp` | 对话头像 | P2 | 旁观者头像，侧光、保持距离 | passed | generated |
| av_classmate_a | avatar | `game/figure/avatar/av_classmate_a_v01.webp` | 对话头像 | P2 | 同学A头像，普通社团成员感 | passed | generated |
| ui_title_logo | ui | `game/template/assets/ui_title_logo_text_v01.webp` | 标题 UI | P2 | 文字版标题牌，本地字体渲染标题字，避免真实事件标识和 AI 错字 | passed | generated |
| ui_choice_tabs | ui | `game/template/assets/ui_choice_tabs_v01.webp` | 选择 UI | P2 | 纸质标签风格选择按钮底图，灰、蓝、浅黄点缀 | passed | generated |

## 隐私规则

- 原始截图、PDF、聊天记录不进入 `site/game/`。
- Cloudflare Pages 构建产物只包含匿名化、改绘、重排版或虚构化资产。
- 证据图保留“证据感”，但不保留头像、QQ 号、真实姓名、群名、学校/社团真实标识、订单和账号信息。
- 更新公开图片时改文件名版本号，不覆盖同名文件，配合 `_headers` 的长缓存策略。

## 体积建议

- 背景/CG：单文件约 2-5 MiB 以内。
- 立绘：单文件尽量小于 2 MiB。
- 证据图：单文件约 1-3 MiB 以内。
- 大视频或长音频不要放入 Pages 包，后续使用 R2 或独立静态域名。
