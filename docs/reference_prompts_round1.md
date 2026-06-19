# 《社长恋爱物语》第一轮绿幕参考图 Prompts

用途：先生成角色、道具、资料卡、UI 壳和环境模块的绿幕参考图；第二轮再把这些参考图作为 reference image，生成正式大图、CG、背景和可扣图素材。

## 风格锚点

生成时把这些旧图作为“文字化风格锚点”。当前使用 `/v1/images/generations` + `gpt-image-2` 时，脚本不会把本地图片作为 image input 传入，而是把下方风格描述写入 prompt。

- `/home/donz/assets_generated/bg/01_s02.png`：背景线条、光影、干净可读的 VN 构图。
- `/home/donz/assets_generated/remaining_pro_chara/01_s01.png`：人物立绘线条、肤色、衣料褶皱、克制表情。
- `/home/donz/assets_generated/style_anchor/cash_anchor.png`：道具近景、纸张质感、证据感物件表现。
- `/home/donz/assets_generated/compat_ui_p0/p_s03.png`：UI 壳、红点/手机界面的证据感。

文字化风格描述：

- 整体：日系视觉小说插画，现实校园题材，线条清晰、上色干净、低饱和配色，情绪克制，不做夸张奇幻和厚涂油画感。
- 人物：普通现代校园社团成员，脸部柔和但不偶像化，衣服朴素无品牌，表情轻压、疲惫或冷静，避免戏剧化崩坏。
- 背景：空间层次清楚，室内光柔和，构图留出 VN 对话框区域，物件边界干净，不做照片级写实。
- 道具：纸张、文件夹、卡片、票据、便签有轻微纸纹、磨损、折痕和手绘边线；证据感强但不是法医照片或产品摄影。
- UI：浅灰/米白界面，卡片分区清楚，像真实社媒或聊天壳但完全原创；红点或通知点作为少量跳色，避免赛博风和花哨渐变。

## 角色视觉区分规则

男生角色必须通过服装轮廓、主色块、配件和手持物一眼区分，不能只靠发型、眼神或表情区分。绿幕图里不要使用绿色衣服或绿色道具。

- 木头/社长：黑色短款立领夹克、灰色衬衫、深色长裤、白鞋、灰色资料夹。视觉关键词是“黑色、锐利、资料夹、主导者”。
- 记录者：浅米色工装马甲、白色卷袖衬衫、橄榄棕长裤、红棕夹板笔记本、录音笔、手表。视觉关键词是“浅色、多口袋、记录工具、整理者”。
- 旁观者：蓝灰长针织开衫、米白高领衫、圆眼镜、 tan 帆布斜挎包、小螺旋本。视觉关键词是“蓝灰、柔软、眼镜、旁观记录”。
- 同学 A：暖棕或砖红 hoodie / 开衫、浅色内搭、空白角色卡或松散纸张。视觉关键词是“暖色、略紧张、普通同学、提问者”。

负面规则：不要让两个男生同时穿黑夹克灰衬衫；不要让记录者戴圆眼镜或斜挎包；不要让旁观者拿灰色资料夹；不要让木头出现工装马甲、圆眼镜或帆布包。

## 通用前缀

把下面这段放在每条 item prompt 前面。

```text
Create exactly one green-screen reference image for the WebGAL visual novel "Shezhang Love Story".

Style reference: match the text-described style anchors from /home/donz/assets_generated/: Japanese visual novel illustration, grounded contemporary campus realism, clean linework, tidy flat-to-soft shading, controlled low-saturation color palette, restrained emotion, cinematic but not glamorous, realistic everyday props, readable silhouettes, and soft practical lighting.

This is NOT a final CG. This is a reference asset to be cut out and reused in later large scene generation.

Background requirement: pure solid chroma key green background (#00FF00), flat and textureless, no scenery, no gradient, no pattern, no green spill on the subject. Keep the subject cleanly separated from the green background. Use no green-colored clothing or green-colored props.

Image quality: sharp edges, clean silhouette, highly readable at VN scale, coherent anatomy or object geometry, no watermark, no logo, no border.

Text handling: do not render final readable Chinese text. Use blank label areas, pseudo-text blocks, blurred text bands, or empty cards. Final Chinese text will be typeset later in WebGAL or post-production.
```

## 通用负面约束

把下面这段放在每条 item prompt 末尾。

```text
Avoid: real names, real school logos, real club names, real chat app branding, real account IDs, QR codes, readable private messages, readable timestamps, readable Chinese text, random fake Chinese, watermarks, logos, brand cloning, muddy lighting, cluttered silhouette, excessive detail that hurts cutout use, fantasy design, cyberpunk interface, horror styling, glamorized suffering, melodramatic poster pose, fanservice, erotic framing, voyeuristic angle, exposed underwear, fetish elements, gore.
```

## 建议批次

- Batch A：角色参考图，建议 1024x1536 或 1536x2048。
- Batch B：道具/证据参考图，建议 1536x1536 或 2048x2048。
- Batch C：UI 壳参考图，建议 1080x1920 或 1440x1920。
- Batch D：环境模块参考图，建议 2048x1536。

## Batch A：角色参考图

### ref_mutou_neutral

```text
Subject: Mutou, the club president. Young adult East Asian male, calm and reserved. Distinct outfit: black short stand-collar jacket, medium gray button shirt, charcoal straight pants, white sneakers, gray evidence folder held at the side. No glasses, no utility vest, no cardigan, no crossbody bag. Pose: full-body front three-quarter standing pose, shoulders slightly guarded, neutral expression with slight unease. Clear VN sprite silhouette, transparent-background-friendly composition, centered on green screen.
```

### ref_mutou_tired

```text
Subject: Mutou, same identity as ref_mutou_neutral. Keep the same visual identity: black short stand-collar jacket, medium gray button shirt, charcoal pants, gray evidence folder or folder edge. No glasses, no utility vest, no cardigan, no crossbody bag. Pose: waist-up to knee-up, head slightly lowered, tired eyes, one hand touching the folder edge or sleeve cuff, restrained fatigue rather than dramatic despair. Keep him gentle, ordinary, and non-glamorous. Centered on pure green screen.
```

### ref_mutou_soft

```text
Subject: Mutou, same identity as ref_mutou_neutral. Keep the black short stand-collar jacket, medium gray button shirt, charcoal pants, and gray evidence folder continuity. No glasses, no utility vest, no cardigan, no crossbody bag. Pose: half-body or knee-up, softer expression, quietly reassuring, one hand open as if calming a conversation, no heroic pose. Emotion: tired but trying to be kind. Centered on pure green screen.
```

### ref_recorder_neutral

```text
Subject: the Recorder, the player-view narrator. Androgynous young adult campus-club member. Distinct outfit: light beige utility vest over a white rolled-sleeve shirt, dark olive or brown trousers, red-brown clipboard notebook, recorder pen clipped to the vest, small wristwatch. Hair can be tied back or neatly parted to avoid matching Mutou. No black jacket, no blue cardigan, no glasses, no crossbody bag. Pose: full-body or knee-up, calm posture, analytical expression, organizing evidence. Design should feel like a careful note-taker, not a detective costume. Centered on pure green screen.
```

### ref_recorder_thinking

```text
Subject: the Recorder, same identity as ref_recorder_neutral. Keep the light beige utility vest, white rolled-sleeve shirt, dark olive or brown trousers, red-brown clipboard notebook, recorder pen, and wristwatch. No black jacket, no blue cardigan, no glasses, no crossbody bag. Pose: half-body, one hand holding notebook open, the other hand near the chin or recorder pen, thoughtful and cautious. Emotion: restrained focus, avoiding judgment. Centered on pure green screen.
```

### ref_witness_neutral

```text
Subject: the Witness, a semi-anonymous observer outside the relationship. Young adult campus-club member. Distinct outfit: blue-gray long knit cardigan over an off-white turtleneck, round glasses, tan canvas crossbody bag, small spiral notepad and pen. No black jacket, no gray evidence folder, no beige utility vest. Pose: full-body or knee-up, standing slightly sideways as if near a corridor edge, attentive but not all-knowing. Expression: careful, uneasy, observant. Centered on pure green screen.
```

### ref_witness_concerned

```text
Subject: the Witness, same identity as ref_witness_neutral. Keep the blue-gray long knit cardigan, off-white turtleneck, round glasses, tan canvas crossbody bag, small spiral notepad and pen. No black jacket, no gray evidence folder, no beige utility vest. Pose: half-body, arms lightly folded or one hand near the notebook margin, concerned expression, looking toward unseen conversation. Emotion: "I saw something but cannot judge everything." Keep silhouette clean and cutout-friendly. Centered on pure green screen.
```

### ref_classmate_a_neutral

```text
Subject: Classmate A, an ordinary campus-club member who asks necessary awkward questions. Young adult East Asian student. Distinct outfit: warm rust-brown hoodie or brick-red cardigan, off-white inner shirt, simple dark pants, no school emblem, no memorable real-world identifiers. Handheld object: blank role card or loose paper. No black jacket, no beige utility vest, no blue-gray long cardigan, no glasses, no crossbody bag. Pose: knee-up, slightly nervous but sincere. Expression: confused but willing to understand. Centered on pure green screen.
```

## Batch B：道具与证据参考图

### ref_folder_gray_closed

```text
Subject: one closed gray evidence folder, object-first reference. Plain matte gray folder with no logo, no readable text, subtle paper texture, slightly worn edges, six small colored chapter tabs visible from the side. Camera: three-quarter top-down object view. Lighting: soft desk-lamp highlight. Background: pure chroma green.
```

### ref_folder_gray_open

```text
Subject: one open gray evidence folder with blank paper sheets, no readable text. Include four main tabs and six chapter tabs as blank label shapes, a few clipped pages, and a small recorder pen. Camera: clean three-quarter top-down view, all edges readable for cutout. Background: pure chroma green.
```

### ref_tabs_four

```text
Subject: four separate paper file tabs as a cutout prop set. The tabs represent "main route, cast, timeline, evidence room" but must not contain readable text; use blank label spaces and subtle color coding: gray, muted blue, pale yellow, off-white. Slight paper wear, clean silhouettes. Background: pure chroma green.
```

### ref_role_cards_blank

```text
Subject: four blank semi-anonymous character dossier cards, no portraits and no readable text. Each card has a simple layout area for name, role, and notes, but only blank blocks or pseudo-text. Cards arranged in a neat fan or row. Evidence-room tactile paper texture. Background: pure chroma green.
```

### ref_evidence_six_cards

```text
Subject: six evidence cards as a reusable prop set, representing keyword index, concrete evaluation, shared narrative, April 9, April 19, and after separation. No readable final text; use icon-like shapes, blank title bars, pseudo-text rows, small color tabs. Arrange as six separate cards with slight overlap, all edges visible. Background: pure chroma green.
```

### ref_keyword_box_cards

```text
Subject: a gray archival card box with black index cards and pale comparison cards. The black cards should feel heavier, the pale cards softer, but all text areas must be blank or pseudo-text. Include one folded gray paper strip in the box. Object-first documentary focus, tactile paper and metal divider edges. Background: pure chroma green.
```

### ref_evaluation_table_sheet

```text
Subject: one two-column evaluation table sheet as a prop. Left column and right column are visible but no readable labels; leave two large blank header areas for later text overlay. Include a few red line marks, sticky notes, and grey-white chat bubble printouts with all text blurred or blank. Camera: top-down paper reference. Background: pure chroma green.
```

### ref_redacted_chat_bubbles

```text
Subject: a set of anonymous gray and white chat bubble cutouts, no avatars, no names, no timestamps, no platform branding. Some bubbles are stacked, some crossed by redaction bars, some left blank for later text. Clean UI-like shapes with paper-print texture, evidence-like not decorative. Background: pure chroma green.
```

### ref_project_song_commission_cards

```text
Subject: three to five anonymous shared-narrative cards: a project checklist, a song/lyrics note, a commission/order-style record, a call review note, and a "step back / compromise" blank label. No money amounts, no account marks, no readable text. Use blank boxes, pseudo-text lines, paperclips, and muted color tags. Background: pure chroma green.
```

### ref_apr9_folded_date_page

```text
Subject: one folded date-page prop for the April 9 chapter. A thin paper page with a strong horizontal fold, blank date label area, four small blank subheading blocks, and an arrow-shaped footer note. It should visually imply contradiction and careful annotation, but contain no readable text. Background: pure chroma green.
```

### ref_apr11_footer_card

```text
Subject: a small footer reference card used as a later-public-note marker. Small paper card, arrow motif, tiny blank label area, understated and secondary. It must look like a page footnote, not the main title. No readable text. Background: pure chroma green.
```

### ref_apr19_timeline_strip

```text
Subject: one horizontal timeline strip for the April 19 chapter. Four blank time labels for deep night, morning, noon, afternoon; gray chat bubble clusters between them; a blue bookmark tucked near the afternoon segment. No readable text or timestamps. Camera: top-down evidence prop. Background: pure chroma green.
```

### ref_blue_bookmark_gift

```text
Subject: a small blue bookmark and simple small gift prop, ordinary and modest, not luxury. The bookmark is the main focal object, with a tiny blank note card and soft paper wrap. Emotion: daily-life object after a heavy conversation. Clean cutout silhouette. Background: pure chroma green.
```

### ref_after_sticky_notes

```text
Subject: five sticky notes as a prop set for the "after separation" chapter. Each sticky note has a blank title area and pseudo-text rows; visual categories are strong emotion, offline activity, organization task, item/consumption, follow-up. Use muted colors, no readable text, slight paper curl. Arrange as separate cutout pieces, all edges visible. Background: pure chroma green.
```

### ref_route_items_after

```text
Subject: a route-and-items prop cluster: a faint erased route line on a small paper, a cropped meeting note corner, a small anonymous merchandise item, and two stacked sticky notes. No real locations, no ticket details, no readable text. It should feel like practical aftermath, not adventure planning. Background: pure chroma green.
```

### ref_lamp_recorder_pen

```text
Subject: a small evidence desk prop cluster: warm desk lamp head, compact audio recorder pen, paperclips, and two blank page corners. Object-first, clean silhouette, useful as foreground insert. No readable labels or brand marks. Background: pure chroma green.
```

## Batch C：UI 壳参考图

### ref_phone_chat_shell

```text
Subject: one fictional mobile chat interface shell, front-facing phone screen only. Anonymous gray-white message bubbles, no avatars, no usernames, no timestamps, no brand icons. Show enough blank text bands for later Chinese typesetting. Add subtle unread indicator dots and archived-state feeling, but keep it grounded, not cyberpunk. Background outside phone: pure chroma green.
```

### ref_social_post_shell

```text
Subject: one fictional social post interface shell, front-facing screen card. Include blank avatar circle, blank username line, blank content blocks, comment area, and a small red notification dot. No real app branding, no readable text, no QR codes. Evidence-like clean hierarchy. Background outside UI: pure chroma green.
```

### ref_timeline_ui_shell

```text
Subject: one fictional timeline/index UI shell for six chapters. Six stacked cards with blank title bars, small date slots, and status markers. No readable text. It should feel like a private archive viewer, not a game menu splash screen. Background outside UI: pure chroma green.
```

### ref_evidence_card_ui_shell

```text
Subject: one fictional evidence card UI shell, full-screen card layout but isolated for cutout. Large blank title area, three blank rows for content/status/public handling, small tag chips, no readable text. Clean contemporary UI, evidence-like, fully original product style. Background outside UI: pure chroma green.
```

## Batch D：环境模块参考图

这些不是最终背景，而是后续大图生成时喂给模型的“场景部件锚点”。

### ref_clubroom_furniture_pack

```text
Subject: isolated campus clubroom furniture pack: one long table edge, two simple chairs, a window frame strip with rainy glass texture, and a blank noticeboard edge. Arrange as separate objects with clear silhouettes, not a full room. No school marks, no posters with readable text. 2D VN background asset style, but on pure chroma green.
```

### ref_archive_table_pack

```text
Subject: isolated archive table set: long wooden or laminate table slab, card box, transparent sleeves, clipped blank pages, small labels, and a warm desk-lamp light cone suggested on the objects. Do not draw a full room. Evidence sorting atmosphere, clean cutout shapes. Background: pure chroma green.
```

### ref_evidence_cabinet_module

```text
Subject: isolated glass evidence cabinet module with six empty compartments. The cabinet is low-light, clean, slightly reflective, with blank cards inside each compartment. No real screenshots, no readable text. Front three-quarter view, useful as a future scene reference. Background: pure chroma green.
```

### ref_corridor_rain_module

```text
Subject: isolated corridor module: a campus hallway window frame with rain streaks, a simple door edge, a floor reflection strip, and a blank wall notice panel. No school logos, no readable posters. It should imply a rainy evening corridor while remaining a cutout-friendly module on pure chroma green.
```

### ref_title_table_arrangement

```text
Subject: isolated title-table arrangement: gray folder at center, warm desk lamp glow, recorder pen, four blank tabs, six chapter tabs, and a few paper edges. This is a reusable composition reference for the title and hub large images. Keep the object cluster complete, readable, and cutout-friendly. Background: pure chroma green.
```

### ref_final_closed_folder

```text
Subject: closed gray folder with six flattened chapter tabs and a soft desk-lamp highlight. The mood is quiet completion, not victory. No readable cover text, no real identifiers. Object-first close-up, clean silhouette. Background: pure chroma green.
```

## 第一轮优先级

最先跑这 16 张，足够锁住后续大图：

1. `ref_mutou_neutral`
2. `ref_mutou_tired`
3. `ref_recorder_neutral`
4. `ref_witness_neutral`
5. `ref_folder_gray_open`
6. `ref_tabs_four`
7. `ref_evidence_six_cards`
8. `ref_keyword_box_cards`
9. `ref_evaluation_table_sheet`
10. `ref_redacted_chat_bubbles`
11. `ref_project_song_commission_cards`
12. `ref_apr9_folded_date_page`
13. `ref_apr19_timeline_strip`
14. `ref_after_sticky_notes`
15. `ref_title_table_arrangement`
16. `ref_evidence_cabinet_module`

其余项目作为同一轮补充批次继续跑。
