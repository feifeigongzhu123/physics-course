# 初中 / 高中物理 · 动画精讲

统一入口：`index.html`（双击打开，本地运行，无需联网）

- 初中物理 **85 个完整知识点** → `junior.html`
- 高中物理 **124 个完整知识点** → `senior.html`

沿用化学动画课的结构：每个知识点 3 步 2D 动画、中文语音同步、5 道改编题与逐项解析。初中 85 点 + 高中 124 点 = **209 个知识点全部完成**；讲稿/语音层 627 段 MP3 全量就绪。

## 课程覆盖

| 学段 | 课程页知识点 | 语音层 |
|---|---|---|
| 初中 | 85（八上 26 + 八下 20 + 九年级 39） | 85 / 85 |
| 高中 | 124（必修 + 选择性必修全册） | 124 / 124 |
| 合计 | **209** | 209 / 209 |

初中 85 点覆盖八上全册、八下全册和九年级全一册：声光热力电、简单机械、内能、电功率、生活用电、电与磁、信息与能源。

每个知识点包含：

- 3 步 2D SVG 动画，器材、光线、电路、轨迹、读数均为该点专属；
- 3 段中文语音（Windows Huihui，MP3 16 kHz 单声道 48 kbps；WAV 只作临时文件），音频结束自动切下一步；
- 进度条由真实播放时间驱动，支持暂停 / 继续 / 重播；
- 手机端动画区可左右滑动，切换步骤时自动定位到当前讲解区域；
- 5 道题：初中标「中考真题改编」，高中标「高考真题改编」；4 个选项、逐项解析、可听讲解；
- 每个点 5 题答案覆盖 A/B/C/D，且不会连续两题同答案；
- localStorage 记录已学知识点、答题记录和错题，可重置。

## 规模

| | 知识点 | 步数 | 题数 | 语音 | MP3 大小 |
|---|---|---|---|---|---|
| 初中 | 85 | 255 | 425 | 255 段 | 约 26.7 MB |
| 高中 | 124 | 372 | 620 | 372 段 | 约 59.2 MB |
| 合计 | **209** | **627** | **1045** | 627 段 | **约 85.9 MB** |

讲稿/语音层全量：209 个点、627 段 MP3、85.9 MB（WAV 约 590 MB）。

## 高考真题加练（v1.2.0）

- 来源：2021–2025 辽宁 / 黑吉辽蒙高考物理 5 套 PDF，共 50 道选择题（35 单选 + 15 多选）全部收录；每套另有实验/计算非选择题，暂未纳入选择题模式。
- 挂载：50 道题分配到 29 个高中知识点；做完基础 5 题后出现“继续做真题”，可展开加练。
- 真题标识：每道真题显示红色“真题”徽标，并标注年份与来源（如“2021年辽宁高考物理”）。
- 带图题：30 道依赖原题图/图像选项的题，已从 PDF 裁出题目与选项图（`real/<id>.png`），页面直接显示；图像选项用 A/B/C/D 按钮选择。
- 交互：单选直接判，多选勾选后提交；正确答案和每个错误选项都给出原因；支持单题重做、重做全部真题、重做基础 5 题。
- 数据：`data/real_questions.json`；题目图：`real/`。

## 语音批进度（2026-11-21）

- 第一批：50 个知识点、150 段 MP3、18.3 MB。[试听](voice-bank.html)
- 第二批：53 个知识点、159 段 MP3、12.3 MB。[试听](voice-bank-b2.html)
- 第三批：52 个知识点、156 段 MP3、28.6 MB。[试听](voice-bank-b3.html)
- 第四批：51 个知识点、153 段 MP3、25.1 MB。[试听](voice-bank-b4.html)
- 四批合计 **206 个知识点、618 段 MP3、84.3 MB**；连同 3 个高中样例点（9 段），**209 个点、627 段、85.9 MB，讲稿/语音层 100% 覆盖**。
- **全部 209 个点**都已接入 3 步动画、读数、公式和 5 道题，没有只留语音的点。
- 讲稿分别在 `data/voice_bank_junior.json`、`voice_bank_batch2.json`、`voice_bank_batch3.json`、`voice_bank_batch4.json`。

## 文件结构

```
index.html                  # 统一入口：初中 85 / 高中 124
junior.html                 # 初中 85 点，数据/场景内联
senior.html                 # 高中 124 点，数据/场景内联
voice-bank.html             # 第一批试听页（50 点 / 150 段）
voice-bank-b2.html          # 第二批试听页（53 点 / 159 段）
voice-bank-b3.html          # 第三批试听页（52 点 / 156 段）
voice-bank-b4.html          # 第四批试听页（51 点 / 153 段）
VERSION                     # 当前版本号
serve.py                    # 局域网静态服务器（python serve.py）
data/junior.json            # 初中 3 点课程 + 题库
data/senior.json            # 高中 3 点课程 + 题库
data/voice_bank_junior.json # 第一批 50 点讲解稿
data/voice_bank_batch2.json # 第二批 53 点讲解稿
data/voice_bank_batch3.json # 第三批 52 点讲解稿
data/voice_bank_batch4.json # 第四批 51 点讲解稿
audio/pj-1/step1.mp3        # 初中样例语音：pj-1 ~ pj-3
audio/ps-1/step1.mp3        # 高中样例语音：ps-1 ~ ps-3
audio/pj-4/step1.mp3        # 语音批初中：pj-4 ~ pj-85
audio/ps-4/step1.mp3        # 语音批高中：ps-4 ~ ps-124
_build/
  content_junior.py         # 初中 3 个样例内容与题库
  content_senior.py         # 高中 3 个样例内容与题库
  content_auto_a.py         # 自动生成 pj-4 ~ pj-8
  content_auto_b.py         # 自动生成 pj-9 ~ pj-13
  content_auto_c.py         # 自动生成 pj-14 ~ pj-18
  content_auto_d.py         # 自动生成 pj-19 ~ pj-23
  content_auto_e.py         # 自动生成 pj-24 ~ pj-28
  content_auto_f.py         # 自动生成 pj-29 ~ pj-33
  content_auto_g.py         # 自动生成 pj-34 ~ pj-38
  content_auto_h.py         # 自动生成 pj-39 ~ pj-43
  content_auto_batch1.py    # 第一批 20 点装配
  content_auto_batch2.py    # 第二批 20 点装配
  validate_auto_module.py   # 自动内容模块校验器
  voice_bank_junior.py      # 第一批 17 点讲解稿源文件
  voice_bank_junior_b1.py   # 第一批补充 31 点
  voice_bank_junior_b2.py   # 第二批初中 34 点
  voice_bank_senior_b2.py   # 第二批高中必修一 18 点
  voice_bank_senior_b3a.py  # 第三批 ps-22 ~ ps-47
  voice_bank_senior_b3b.py  # 第三批 ps-48 ~ ps-73
  voice_bank_senior_b4a.py  # 第四批 ps-74 ~ ps-99
  voice_bank_senior_b4b.py  # 第四批 ps-100 ~ ps-124
  voice_bank_batch1.py      # 第一批 50 点装配
  voice_bank_batch2.py      # 第二批 53 点装配
  voice_bank_batch3.py      # 第三批 52 点装配
  voice_bank_batch4.py      # 第四批 51 点装配
  run_remaining.py          # 自动跑第三、四批音频与页面
  real/*.png                # 30 道带图真题的原题图
data/real_questions.json   # 50 道高考真题与逐项解析
  scenes/pj-*.svg           # 初中 85 个三步动画场景
  scenes/ps-*.svg           # 高中 124 个三步动画场景
  app.js / base_app.css / scenes.css / template.html
  build.py                  # 构建函数（直接运行会提示改用 build_full.py）
  build_full.py             # 构建初中 23 + 高中 3
  check_scenes.py           # 23 个 SVG 结构检查
  gen_audio.py              # 按学段/知识点批量生成 MP3（可断点续跑）
  gen_voice_bank.py         # 语音批生成：讲稿 -> manifest -> MP3（--batch 1|2|3|4）
  build_voice_bank.py       # 生成语音试听页（参数 1|2|3|4）
  tts.ps1                   # Huihui 合成 + ffmpeg 转 MP3
  mp3_tool.py               # 把已有 WAV 批量转 MP3
  cdp_check.py              # Edge 无头验收：页面/题库/音频
  cdp_shots.py              # 逐步截图 + 390px 手机布局检查
shots/                      # 验收截图
```

## 重新构建

```bat
cd /d D:\AI\ZCode\physics\_build
python build_full.py
```

`build_full.py` 会同时构建初中 23 点和高中 3 点；旧的 `build.py` 只保留函数，直接运行会提示改用 `build_full.py`。

构建时会校验：知识点数量、3 步结构、每步读数、5 题角度、4 选项、答案分布、逐项解析格式、解析长度（60–110 字）以及禁用词。

重新生成语音（MP3，已存在的自动跳过，可断点续跑）：

```bat
cd /d D:\AI\ZCode\physics\_build
python gen_audio.py --grade all            # 全部待生成
python gen_audio.py --grade junior         # 只做初中
python gen_audio.py --grade senior --only ps-4,ps-5
python gen_audio.py --grade all --dry-run  # 只估算段数与体积
```

`gen_audio.py` 会调用 `tts.ps1`：先用 Huihui 合成临时 WAV，再用 ffmpeg 转成 16 kHz 单声道 48 kbps MP3，成功后删除 WAV。单个知识点 3 段语音，几百 KB。

## 全量进度与下一步

- **讲稿/语音层已完成**：209 个点、627 段 MP3、85.9 MB，四批全部生成并校验，无缺失。
- **完整课程层已完成**：209 个点全部接入 3 步动画、读数、公式和 5 道题（初中 85 + 高中 124）。
- 没有待补的语音点或课程点。
- 体积实测：627 段共 85.9 MB（WAV 约 590 MB）。

## 测试

```bat
cd /d D:\AI\ZCode\physics\_build
python build_full.py       # 初中 85 + 高中 124，含数据/题目/场景校验
python check_scenes.py     # 初中 85 个 SVG 的 XML、三步、data-zone 检查
python cdp_check.py        # 原 6 个样例页深链、答题、音频
python cdp_full_check.py   # 初中 85 点：场景切换、读数、5 题、MP3、截图
python cdp_senior_check.py # 高中 124 点：场景切换、读数、5 题、MP3、截图
python cdp_real_check.py   # 真题加练、单选/多选、逐项错因、重做
python cdp_real_image.py   # 真题图、真题徽标、多选提交
python cdp_shots.py        # 逐步截图 + 390px 手机布局与自动定位
```

自动生成内容模块可单独校验：

```bat
python validate_auto_module.py content_auto_a.py
python validate_auto_module.py content_auto_b.py
python validate_auto_module.py content_auto_c.py
python validate_auto_module.py content_auto_d.py
```

## 分享给别人

1. **离线文件夹**：把整个 `physics` 文件夹压缩发送，解压后双击 `index.html`。不要只发 HTML，否则语音缺失。
2. **同一局域网**：在项目目录运行 `python serve.py`，手机与电脑连同一 Wi-Fi 后访问终端打印的局域网地址。
3. **公网静态托管**：整个文件夹上传即可，入口 `index.html`，无需后端。

## 后续扩展

新增一个知识点只需要四步：

1. 在 `_build/content_junior.py` 或 `content_senior.py` 里追加一个点（3 步 + 5 题）；
2. 在 `_build/scenes/` 画一个专属 SVG（三步用 `.s1/.s2/.s3` 类控制状态）；
3. 在 `_build/scenes.css` 补该点的显隐与动画规则；
4. 运行 `build.py` 生成数据与页面，再运行 `python gen_audio.py --grade junior --only 新id` 生成 3 段 MP3 语音。

扩展顺序与批次计划见 [PRODUCTION.md](PRODUCTION.md)。

题库只做「改编」，不写具体年份或原卷号，避免伪造出处。
