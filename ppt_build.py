# 可列印 PPT：python3 ppt_build.py → ICOPE系統討論_暖暖衛生所.pptx
# 白底、深字、大字；互動頁改成紙本填寫版。內容與 parts/slides.html 同步，改數字兩邊都要改。
import sys
from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE, XL_LEGEND_POSITION, XL_LABEL_POSITION
from PIL import ImageFont

FONT = "Microsoft JhengHei"
INK = RGBColor(0x12, 0x34, 0x3B); INK2 = RGBColor(0x44, 0x61, 0x6A); INK3 = RGBColor(0x72, 0x8B, 0x91)
TEAL = RGBColor(0x02, 0x80, 0x90); TEALBG = RGBColor(0xE0, 0xF0, 0xF1); TEALMID = RGBColor(0x7F, 0xC0, 0xC7)
ORANGE = RGBColor(0xE8, 0x55, 0x2D); ORANGEBG = RGBColor(0xFC, 0xE8, 0xE0); ORANGEINK = RGBColor(0xB8, 0x3A, 0x17)
AMBER = RGBColor(0xF4, 0xA9, 0x3C); AMBERBG = RGBColor(0xFD, 0xF0, 0xD8)
RULE = RGBColor(0xCF, 0xDC, 0xDB); GREY = RGBColor(0xB8, 0xC4, 0xC6); WHITE = RGBColor(0xFF, 0xFF, 0xFF)
DEEP = RGBColor(0x12, 0x34, 0x3B)
import os
MONO = os.environ.get("MONO") == "1"   # 白底黑字列印版
HEADFILL, HEADTXT, DIVBG = DEEP, RGBColor(0xFF, 0xFF, 0xFF), TEALBG
if MONO:
    K = RGBColor(0, 0, 0); G1 = RGBColor(0x40, 0x40, 0x40); G2 = RGBColor(0x70, 0x70, 0x70); G3 = RGBColor(0xA6, 0xA6, 0xA6)
    LT = RGBColor(0xF2, 0xF2, 0xF2)
    INK = K; INK2 = G1; INK3 = G2
    TEAL = K; TEALBG = LT; TEALMID = G3
    ORANGE = G1; ORANGEBG = LT; ORANGEINK = K
    AMBER = G3; AMBERBG = LT
    RULE = RGBColor(0xBF, 0xBF, 0xBF); GREY = RGBColor(0xD9, 0xD9, 0xD9); DEEP = K
    HEADFILL, HEADTXT, DIVBG = RGBColor(0xE6, 0xE6, 0xE6), K, RGBColor(0xFF, 0xFF, 0xFF)

LIGHT = RGBColor(0xF4, 0xF8, 0xF8) if not MONO else RGBColor(0xF7, 0xF7, 0xF7)
W, H = 13.333, 7.5
prs = Presentation(); prs.slide_width = Inches(W); prs.slide_height = Inches(H)
BLANK = prs.slide_layouts[6]
_fonts = {}
def _f(px, bold):
    k = (px, bold)
    if k not in _fonts:
        _fonts[k] = ImageFont.truetype("/System/Library/Fonts/STHeiti Medium.ttc" if bold else "/System/Library/Fonts/STHeiti Light.ttc", px)
    return _fonts[k]
WARN = []

def lines_needed(text, w_in, size, bold=False):
    """估計在寬 w_in 吋、size pt 下要幾行（1pt=1px@72dpi）。"""
    f = _f(int(size * 4), bold); maxw = (w_in - 0.2) * 72 * 4
    n = 0
    for para in text.split("\n"):
        cur = 0; n += 1
        for ch in para:
            cw = f.getlength(ch)
            if cur + cw > maxw: n += 1; cur = cw
            else: cur += cw
    return n

def check(text, w, h, size, bold, where, ls=1.25):
    need = lines_needed(text, w, size, bold) * size * ls / 72 + 0.12
    if need > h + 0.02: WARN.append(f"[{where}] 可能超出：需 {need:.2f}in > {h:.2f}in ｜ {text[:24]}")

PAGE = [0]
def new(sec, title=None, dark=False):
    s = prs.slides.add_slide(BLANK); PAGE[0] += 1
    if dark:
        bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
        bg.fill.solid(); bg.fill.fore_color.rgb = DIVBG; bg.line.fill.background()
    tb(s, 0.55, 0.22, 9, 0.42, sec, 12, TEAL, bold=True)
    ln = s.shapes.add_connector(1, Inches(0.55), Inches(0.66), Inches(W - 0.55), Inches(0.66))
    ln.line.color.rgb = RULE if not dark else TEALMID; ln.line.width = Pt(0.75)
    if title: tb(s, 0.55, 0.78, W - 1.1, 0.75, title, 28, INK, bold=True)
    return s

def tb(s, x, y, w, h, text, size=18, color=INK, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP,
       fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, pad=0.1, check_fit=True, ls=1.2):
    if fill is not None or line is not None:
        sh = s.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
        if shape == MSO_SHAPE.ROUNDED_RECTANGLE: sh.adjustments[0] = 0.06
        if fill is not None: sh.fill.solid(); sh.fill.fore_color.rgb = fill
        else: sh.fill.background()
        if line is not None: sh.line.color.rgb = line; sh.line.width = Pt(1)
        else: sh.line.fill.background()
        sh.shadow.inherit = False
    else:
        sh = s.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = sh.text_frame; tf.word_wrap = True; tf.vertical_anchor = anchor
    for side in ("left", "right"): setattr(tf, f"margin_{side}", Inches(pad + 0.05))
    tf.margin_top = tf.margin_bottom = Inches(pad)
    items = text if isinstance(text, list) else [text]
    first = True
    for it in items:
        # it: str 或 (str, dict)
        t, o = (it, {}) if isinstance(it, str) else it
        p = tf.paragraphs[0] if first else tf.add_paragraph(); first = False
        p.alignment = o.get("align", align); p.line_spacing = ls
        if o.get("space"): p.space_before = Pt(o["space"])
        r = p.add_run(); r.text = t
        f = r.font; f.name = FONT; f.size = Pt(o.get("size", size)); f.bold = o.get("bold", bold)
        f.color.rgb = o.get("color", color)
        rPr = r._r.get_or_add_rPr(); ea = rPr.makeelement("{http://schemas.openxmlformats.org/drawingml/2006/main}ea", {"typeface": FONT}); rPr.append(ea)
    if check_fit:
        need = 0
        for it in items:
            t, o = (it, {}) if isinstance(it, str) else it
            sz = o.get("size", size)
            need += lines_needed(t, w - 2 * pad, sz, o.get("bold", bold)) * sz * ls / 72 + o.get("space", 0) / 72
        if need + 2 * pad > h + 0.03: WARN.append(f"[p{PAGE[0]}] 可能超出：需 {need + 2*pad:.2f}in > {h:.2f}in ｜ {str(items[0])[:30]}")
    return sh

def card(s, x, y, w, h, head, body, fill=TEALBG, headc=TEAL, size=17, headsize=14, anchor=MSO_ANCHOR.MIDDLE, line=None):
    items = [(head, {"size": headsize, "bold": True, "color": headc})] if head else []
    for i, b in enumerate(body if isinstance(body, list) else [body]):
        if isinstance(b, tuple): items.append(b)
        else: items.append((b, {"size": size, "space": 6 if (items and i == 0) or i > 0 else 0}))
    return tb(s, x, y, w, h, items, fill=fill, line=line, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.18, anchor=anchor)

def ask(s, x, y, w, h, who, q, color=TEAL):
    sh = tb(s, x, y, w, h, [(who + "：", {"bold": True, "color": color, "size": 17}), (q, {"size": 17})],
            fill=WHITE, line=color, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.16, anchor=MSO_ANCHOR.MIDDLE)
    sh.line.dash_style = 4; sh.line.width = Pt(1.75)
    return sh

def bignum(s, x, y, w, num, unit, label, sub=None, color=TEAL, fill=TEALBG, h=1.6):
    items = [(label, {"size": 14, "bold": True, "color": INK2}), (num + unit, {"size": 40, "bold": True, "color": color, "space": 2})]
    if sub: items.append((sub, {"size": 15, "color": INK2, "space": 2}))
    return tb(s, x, y, w, h, items, fill=fill, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.18, anchor=MSO_ANCHOR.MIDDLE)

def style_chart(ch, legend=False, size=14):
    ch.font.name = FONT; ch.font.size = Pt(size); ch.font.color.rgb = INK
    ch.has_legend = legend; ch.has_title = False
    if legend:
        ch.legend.position = XL_LEGEND_POSITION.TOP; ch.legend.include_in_layout = False; ch.legend.font.size = Pt(13)

def bar_chart(s, x, y, w, h, cats, series, kind=XL_CHART_TYPE.BAR_CLUSTERED, colors=None, legend=False,
              labels=True, gap=60, overlap=0, numfmt='0', point_colors=None, size=14, maxv=None):
    cd = CategoryChartData(); cd.categories = cats
    for name, vals in series: cd.add_series(name, vals)
    gf = s.shapes.add_chart(kind, Inches(x), Inches(y), Inches(w), Inches(h), cd); ch = gf.chart
    style_chart(ch, legend, size)
    plot = ch.plots[0]; plot.gap_width = gap; plot.overlap = overlap
    va = ch.value_axis; va.visible = False; va.has_major_gridlines = False
    if maxv: va.maximum_scale = maxv
    va.minimum_scale = 0
    ca = ch.category_axis; ca.format.line.color.rgb = RULE; ca.tick_labels.font.size = Pt(size)
    if kind in (XL_CHART_TYPE.BAR_CLUSTERED, XL_CHART_TYPE.BAR_STACKED, XL_CHART_TYPE.BAR_STACKED_100): ca.reverse_order = True
    for i, ser in enumerate(plot.series):
        ser.format.fill.solid(); ser.format.fill.fore_color.rgb = (colors or [TEAL, ORANGE, AMBER, GREY, TEALMID])[i]
        if labels:
            ser.data_labels.show_value = True; ser.data_labels.number_format = numfmt; ser.data_labels.number_format_is_linked = False
            ser.data_labels.font.size = Pt(size); ser.data_labels.font.bold = True
            if kind in (XL_CHART_TYPE.BAR_STACKED, XL_CHART_TYPE.BAR_STACKED_100):
                ser.data_labels.position = XL_LABEL_POSITION.CENTER
                ser.data_labels.font.color.rgb = WHITE if i in (0, 3) else INK
            else:
                ser.data_labels.position = XL_LABEL_POSITION.OUTSIDE_END
    if point_colors:
        for j, c in point_colors.items():
            pt = plot.series[0].points[j]; pt.format.fill.solid(); pt.format.fill.fore_color.rgb = c
    return ch

def table(s, x, y, w, rows, colw, rowh=0.5, size=16, head_fill=None, hl_col=None):
    head_fill = head_fill or HEADFILL
    nr, nc = len(rows), len(rows[0])
    t = s.shapes.add_table(nr, nc, Inches(x), Inches(y), Inches(w), Inches(rowh * nr)).table
    for j, cw in enumerate(colw): t.columns[j].width = Inches(cw)
    for i, r in enumerate(rows):
        t.rows[i].height = Inches(rowh)
        for j, v in enumerate(r):
            c = t.cell(i, j); c.text = ""; c.vertical_anchor = MSO_ANCHOR.MIDDLE
            c.margin_left = c.margin_right = Inches(0.1)
            p = c.text_frame.paragraphs[0]; run = p.add_run(); run.text = str(v)
            run.font.name = FONT; run.font.size = Pt(size if i else size - 2); run.font.bold = (i == 0 or j == 0 or j == hl_col)
            run.font.color.rgb = HEADTXT if i == 0 else INK
            if j > 0 and j < nc - 1: p.alignment = PP_ALIGN.CENTER
            c.fill.solid()
            c.fill.fore_color.rgb = head_fill if i == 0 else (TEALBG if j == hl_col else (WHITE if i % 2 else LIGHT))
    return t

def notes(s, *lines): s.notes_slide.notes_text_frame.text = "\n".join("• " + l for l in lines)
def foot(s, text): tb(s, 0.55, H - 0.55, W - 1.1, 0.4, text, 11, INK3, check_fit=False)

# ───────────── 01 封面
s = new("115 年度 長者內在能力檢測服務｜共學活動・案例討論＋系統討論")
tb(s, 0.55, 1.15, 6.4, 0.45, "ICOPE · System Review", 14, TEAL, bold=True)
tb(s, 0.55, 1.6, 6.6, 2.0, [("看見一個人", {}), ("看見一套流程", {})], 44, INK, bold=True, ls=1.1)
tb(s, 0.55, 3.65, 6.6, 0.55, [("系統討論：以", {"size": 20, "bold": True, "color": INK2})], 20)
s.shapes[-1].text_frame.paragraphs[0].runs[0].text = "個案討論＋系統討論：以暖暖衛生所的服務為例"
meta = [("報告者", "暖暖區衛生所 李麗芳 主任"), ("資料", "2026/01–08・646 位長者（已去識別化）"), ("對象", "護理師・ICOPE 評估人員"), ("引導", "鍾孟修 職能治療師")]
for i, (k, v) in enumerate(meta):
    xx = 0.55 + (i % 2) * 2.5; yy = 4.45 + (i // 2) * 1.12
    tb(s, xx, yy, 2.45, 1.08, [(k, {"size": 12, "bold": True, "color": INK3}), (v, {"size": 15})])
s.shapes.add_picture("img/qr-web.png", Inches(5.6), Inches(4.5), Inches(1.45), Inches(1.45))
tb(s, 5.35, 5.98, 1.95, 0.6, "掃描開啟網頁版", 12, INK2, align=PP_ALIGN.CENTER)
tiles = [("646", "評估人數", "94 個評估日・14 場大型場次", TEAL), ("110", "初評異常", "初評異常率 17.0%", ORANGEINK),
         ("108", "用藥＋社會評估", "初評異常者 98% 完成", TEAL), ("39", "複評異常", "行動12・營養10・認知6・用藥15", ORANGEINK),
         ("25", "實際介入", "有衛教或轉介的人", ORANGEINK), ("29", "完成後測", "應後測 39 人，後測率 74%", TEAL)]
for i, (n, l, sub, c) in enumerate(tiles):
    xx = 7.25 + (i % 3) * 1.88; yy = 1.35 + (i // 3) * 2.75
    tb(s, xx, yy, 1.78, 2.55, [(n, {"size": 34, "bold": True, "color": c}), (l, {"size": 15, "bold": True, "space": 6}), (sub, {"size": 12, "color": INK2, "space": 4})],
       line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.14, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "今天的系統討論不是評比暖暖衛生所，而是借一個真實單位的資料，看流程哪裡順、哪裡卡。",
      "主線：646 → 110 → 39 → 25 → 29，最後請大家算自己的數字。", "資料已去識別化，不顯示個案代號與評估人員姓名。")

# ───────────── 02 目的
s = new("第二段｜系統討論的目的", "系統討論看的是「流程」，不是「人」")
steps = [("STEP 1", "看見對方", "用暖暖的數據走一遍：服務量、受檢對象、六力異常、介入、後測。", "他們怎麼做到的？"),
         ("STEP 2", "對照指標", "和全市、衛生所合計放在一起看，找出明顯比較好與比較弱的環節。", "差異從哪一站來？"),
         ("STEP 3", "反思自己", "把同一套指標套回自己單位，算出你們的數字。", "我們也有一樣的卡點嗎？"),
         ("STEP 4", "帶回調整", "每個單位挑一件 30 天內能改的事，寫成行動承諾卡。", "誰、哪一天、怎麼做？")]
for i, (n, h_, b, q) in enumerate(steps):
    xx = 0.55 + i * 3.08
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(xx), Inches(1.75), Inches(2.9), Inches(0.07)); bar.fill.solid(); bar.fill.fore_color.rgb = TEAL; bar.line.fill.background()
    tb(s, xx, 1.9, 2.9, 3.4, [(n, {"size": 13, "bold": True, "color": TEAL}), (h_, {"size": 22, "bold": True, "space": 6}),
                               (b, {"size": 16, "color": INK2, "space": 10}), ("問：" + q, {"size": 16, "bold": True, "space": 12})])
for i, (h_, b) in enumerate([("發言原則①", "先問「怎麼做到」，再問「為什麼沒有」。"), ("發言原則②", "每個發現都回到一個流程站點：誰、在哪、何時。"), ("發言原則③", "數字有疑問先當作「資料要確認」，不直接當缺失。")]):
    card(s, 0.55 + i * 4.1, 5.5, 3.95, 1.35, h_, b, size=16)
notes(s, "共學是 115 年服務單位要參加的學習成長活動，目的在互相學習流程，不是考核。", "今天分兩段：看見暖暖、反思自己。", "請暖暖同仁隨時補充實際做法。")

# ───────────── 03 流程
s = new("開場｜對齊規則", "先對齊 115 年的服務流程與時間窗")
flow = [("01", "前置說明", "確認資格（距上次評估滿 1 年）\n簽同意書\n加入長者量六力 LINE"), ("02", "初評六力", "認知、行動、營養、視力、聽力、憂鬱"),
        ("03", "用藥＋社會", "初評任 1 項異常就要做\n含跌倒"), ("04", "複評", "認知 BHT/AD8\n行動 SPPB\n營養 MNA-SF\n憂鬱 GDS-15\n視聽無複評，依狀況轉介"),
        ("05", "個人介入計畫", "居家健康管理衛教\n社區據點・營養中心\n醫療院所・長照・失智共照\n單位直接介入"), ("06", "追蹤", "評估滿 1 個月後至後測當日\n電訪或其他方式"),
        ("07", "後測", "評估後 3–6 個月\n需先完成追蹤\n用相同複評量表")]
for i, (n, h_, b) in enumerate(flow):
    xx = 0.55 + i * 1.77; key = n in ("03", "05")
    tb(s, xx, 1.75, 1.68, 4.15, [(n, {"size": 12, "color": INK3}), (h_, {"size": 17, "bold": True, "space": 4}), (b, {"size": 14, "color": INK2, "space": 8})],
       fill=TEALBG if key else WHITE, line=TEAL if key else RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.1, anchor=MSO_ANCHOR.MIDDLE, ls=1.25)
tb(s, 0.55, 6.0, W - 1.1, 0.82, "上傳：當月評估結果於次月底前上傳「成人預防保健暨慢性疾病防治資訊系統－長者功能評估」。用藥或社會評估異常者，後測時要一併後測。", 15, INK, fill=AMBERBG, pad=0.12, anchor=MSO_ANCHOR.MIDDLE)
foot(s, "依據：115 年長者內在能力檢測服務須知（縣市衛生局公告版）；如有異動以國健署函文為準。")
notes(s, "兩個綠框是今天的重點站：用藥＋社會評估、個人介入計畫。", "視力聽力沒有複評、不需後測，但要依狀況轉介，品質全看介入那一步。", "追蹤先於後測；後測窗口 3 到 6 個月。")

# ───────────── 04 指標
s = new("第二段｜指標定義", "今天用的指標：分子、分母先講清楚")
rows = [["指標", "分子", "分母", "篩選線"],
        ["初評異常率", "初評任 1 項異常人數", "評估人數", ""],
        ["複評完成率", "完成複評人數（含用藥及社會）", "初評異常人數", ""],
        ["異常率", "確認異常（複評異常＋視聽異常）", "評估人數", "<10%"],
        ["首篩比", "首次評估人數", "評估人數", ""],
        ["介入率", "有介入計畫紀錄人數", "確認異常人數", "<50%"],
        ["實際介入率（今天新增）", "有衛教或轉介介入點的人數", "確認異常人數", ""],
        ["後測率", "完成後測人數", "已到後測期的應後測人數", "<30%"]]
table(s, 0.55, 1.7, W - 1.1, rows, [3.2, 4.6, 3.3, 1.13], rowh=0.56, size=17)
tb(s, 0.55, 6.25, W - 1.1, 0.75, "「有紀錄」包含只填「未轉介原因」；「實際介入」要有衛教指導、介入點，或用藥處置。篩選線是衛生局找需要協助流程的參考，不是績效排名。", 15, INK2, check_fit=True)
notes(s, "定義和 10 月共學一樣，方便直接拿全市數字比較。", "今天多加「實際介入率」：填了未轉介原因也算有紀錄，但長輩不一定真的拿到東西。")

# ───────────── 05 divider
def divider(sec, big, sub, lead, qs):
    s = new(sec, dark=True)
    tb(s, 0.55, 1.6, W - 1.1, 1.8, big, 80, INK, bold=True)
    tb(s, 0.6, 3.35, W - 1.1, 0.5, sub, 16, TEAL, bold=True)
    tb(s, 0.55, 3.95, W - 1.1, 1.15, lead, 22, INK, bold=True)
    for i, (a, b) in enumerate(qs):
        xx = 0.55 + i * 3.08
        bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(xx), Inches(5.2), Inches(2.9), Inches(0.05)); bar.fill.solid(); bar.fill.fore_color.rgb = TEAL; bar.line.fill.background()
        tb(s, xx, 5.32, 2.9, 1.1, [(a, {"size": 20, "bold": True, "color": INK}), (b, {"size": 15, "color": INK2, "space": 4})])
    return s
s = divider("第二段｜11:20–12:15", "看見暖暖", "PART 2 · 數據分析與策略研討", "從 646 位長者的資料，看一個衛生所的服務流程長什麼樣子。\n報告：暖暖區衛生所 李麗芳 主任",
            [("量與節奏", "什麼時候、在哪裡做"), ("對象", "找到的是誰"), ("流程", "異常之後發生什麼"), ("資料", "數字能不能相信")])
notes(s, "接下來每頁最後都有一個問題留給暖暖或留給大家。")

# ───────────── 06 服務量
s = new("看見暖暖｜量與節奏", "8 個月 646 人：近一半來自 14 場大型場次")
tb(s, 0.55, 1.6, 8, 0.48, "每月評估人數（8 月資料至 8/11）", 14, INK3, bold=True)
bar_chart(s, 0.45, 1.95, 8.2, 3.3, ["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月"], [("人數", (143, 89, 121, 110, 37, 102, 43, 1))],
          kind=XL_CHART_TYPE.COLUMN_CLUSTERED, gap=45, point_colors={4: ORANGE, 6: ORANGE}, size=15)
tb(s, 0.55, 5.35, 8, 0.48, "星期分布（人數）", 14, INK3, bold=True)
bar_chart(s, 0.45, 5.65, 8.2, 1.55, ["一", "二", "三", "四", "五", "六", "日"], [("人數", (114, 140, 156, 113, 23, 18, 82))],
          kind=XL_CHART_TYPE.COLUMN_CLUSTERED, gap=35, point_colors={6: AMBER}, size=13)
bignum(s, 9.0, 1.6, 3.8, "94", " 天", "評估日", "平均每個評估日 6.9 人", h=1.6)
bignum(s, 9.0, 3.35, 3.8, "14", " 場", "單日 ≥15 人的大型場次", "共 291 人，占 45%；異常率 16.5%，與小場次 17.5% 相近", color=INK, fill=AMBERBG, h=2.0)
ask(s, 9.0, 5.55, 3.8, 1.55, "問暖暖", "5 月、7 月量少的原因？週日場和哪些社區活動合作？")
notes(s, "單日最多 28 人；大型場次異常率和小場次差不多，判讀沒有明顯放寬。", "大型場次的挑戰在後面：當天篩出異常，複評、介入能不能在現場做完。", "週日 82 人，可以請暖暖分享合作對象。")

# ───────────── 07 對象
s = new("看見暖暖｜受檢對象", "受檢者以 65–69 歲為主，75 歲以上只占 11%")
tb(s, 0.55, 1.6, 8, 0.48, "年齡分布（人數）", 14, INK3, bold=True)
bar_chart(s, 0.45, 1.9, 5.0, 4.2, ["65–69", "70–74", "75–79", "80 以上"], [("人數", (387, 187, 53, 19))], gap=45, point_colors={2: TEALMID, 3: ORANGE}, size=16)
tb(s, 5.6, 1.6, 3.2, 0.48, "各年齡層初評異常率", 14, INK3, bold=True)
bar_chart(s, 5.5, 1.9, 3.3, 4.2, ["65–69", "70–74", "75–79", "80 以上"], [("異常率", (0.140, 0.225, 0.189, 0.211))], gap=45, numfmt='0%', colors=[ORANGE], size=15, maxv=0.3)
tb(s, 0.55, 6.25, 8.3, 0.6, "平均 69.3 歲，最年長 91 歲。80 歲以上只有 19 人，異常率僅供參考。", 14, INK3)
bignum(s, 9.1, 1.6, 1.8, "60", "%", "女性", "390 / 646", color=INK, fill=LIGHT, h=1.65)
bignum(s, 11.05, 1.6, 1.75, "73", "%", "首次評估", "471 / 646", h=1.65)
card(s, 9.1, 3.45, 3.7, 1.65, None, "首篩比高，新長輩找得到；但 75 歲以上、少出門的長輩在社區場次比較難接觸。", fill=ORANGEBG, size=16)
ask(s, 9.1, 5.3, 3.7, 1.6, "問大家", "你們 75 歲以上的比例是多少？用什麼方法找到他們？", ORANGEINK)
notes(s, "70–74 歲異常率（22.5%）比 65–69 歲（14.0%）高。", "首篩 73% 是亮點。", "社區活動來的多半是健康、會出門的長輩；高風險者可能在家裡。")

# ───────────── 08 總覽
s = new("看見暖暖｜指標對照", "放進全市一起看：完成度高，介入的「質」要再看")
rows = [["指標", "暖暖衛生所", "衛生所合計", "全市 30 單位", "怎麼看"],
        ["初評異常率", "17.0%（110/646）", "—", "15.0%", "略高於全市，判讀沒有放寬"],
        ["複評完成率（含用藥及社會）", "98.2% ▲", "86.7%", "82.9%", "只差 2 人"],
        ["異常率", "14.7%（95/646）", "11.2%", "11.3%", "高於篩選線 10%"],
        ["介入率（有紀錄）", "92.6%（88/95）", "85.4%", "89.0%", "紀錄完整"],
        ["實際介入率", "26.3% ▼", "—", "—", "多數只填未轉介原因"],
        ["後測率", "74.4% ▲", "61.1%", "57.7%", "29/39；6 人已過窗口"]]
table(s, 0.55, 1.75, W - 1.1, rows, [3.4, 2.5, 1.7, 1.75, 2.88], rowh=0.62, size=17, hl_col=1)
tb(s, 0.55, 6.3, W - 1.1, 0.6, "衛生所合計與全市為 10 月共學使用的「2026 機構訪查篩選表」彙整，統計期間與暖暖本次資料不同，僅作方向參考。▲ 明顯較好　▼ 要討論", 13, INK3)
notes(s, "三個高於全市：複評、後測、紀錄完整度，值得請暖暖分享。", "介入率 92.6% 看起來很好，但只有 25 人有衛教或轉介；其他是已接受處置、自行就醫、拒絕等未轉介原因。")

# ───────────── 09 漏斗
s = new("看見暖暖｜流程漏斗", "漏斗看流失：真正變窄的是「介入」那一段")
ch = bar_chart(s, 0.45, 1.6, 8.3, 5.4, ["初評異常", "用藥＋社會評估", "確認異常", "有介入紀錄", "實際衛教／轉介", "完成後測（應後測 39）"],
               [("人數", (110, 108, 95, 88, 25, 29))], gap=35, point_colors={0: TEAL, 3: TEALMID, 4: ORANGE, 5: TEALMID}, size=16, maxv=125)
card(s, 9.0, 1.6, 3.8, 2.75, "三個流失點", ["初評異常未做用藥／社會：2 人", "確認異常完全沒有介入紀錄：7 人", "有紀錄但只有未轉介原因：63 人", "應後測未完成：10 人"], fill=ORANGEBG, headc=ORANGEINK, size=15, headsize=16)
card(s, 9.0, 4.5, 3.8, 1.2, None, "前段幾乎沒有流失；流失集中在「異常之後給什麼」。", fill=LIGHT, size=15)
ask(s, 9.0, 5.8, 3.8, 1.2, "問大家", "你們的漏斗，最窄的是哪一層？", ORANGEINK)
notes(s, "確認異常 95 人 = 複評異常 39 人＋只有視力或聽力異常的 56 人。", "63 人只有未轉介原因，下一頁拆開看。")

# ───────────── 10 六力
s = new("看見暖暖｜六力與複評", "聽力、視力最多；複評後行動與營養最常確認異常")
bar_chart(s, 0.45, 1.6, 8.4, 5.35, ["聽力", "視力", "認知", "行動", "營養", "憂鬱", "用藥（108 人中）", "社會（108 人中）"],
          [("初評異常人數", (45, 31, 22, 15, 11, 5, 0, 0)), ("複評確認異常", (0, 0, 6, 12, 10, 0, 15, 1))], gap=40, overlap=-10, legend=True, size=14, numfmt='0;;;')
card(s, 9.05, 1.6, 3.75, 1.55, None, "只有 1 項異常 94 人，2 項 14 人，3 項以上 2 人。介入可以很聚焦。", size=15)
card(s, 9.05, 3.3, 3.75, 1.55, None, "用藥異常 15 人中，14 人使用止痛藥或安眠藥；藥品 10 種以上 2 人。", fill=LIGHT, size=15)
ask(s, 9.05, 5.0, 3.75, 1.9, "問暖暖", "行動初評 15 人、複評 12 人異常，比例很高。現場怎麼施測 SPPB？")
foot(s, "視力、聽力沒有複評。憂鬱 5 人 GDS-15 為 3–6 分，未達複評異常。")
notes(s, "百分比：聽力 7.0%、視力 4.8%、認知 3.4%、行動 2.3%、營養 1.7%、憂鬱 0.8%（分母 646）。", "認知 22 人只有 6 人複評異常；行動 15 人有 12 人，比例很不一樣，數據品質頁再回來看。")

# ───────────── 11 亮點1
s = new("看見暖暖｜值得學的地方 ①", "亮點：該做的評估幾乎都做了")
for i, (n, d, h_, b) in enumerate([("47", " / 48", "需複評的人有複評", "認知、行動、營養、憂鬱初評異常 48 人，只有 1 人沒有 BHT/AD8。"),
                                    ("108", " / 110", "用藥＋社會評估", "初評任 1 項異常都要做；只漏 2 位聽力異常的長輩。"),
                                    ("29", " / 39", "後測率 74%", "高於全市 57.7%；營養組 10 人中 9 人完成後測。")]):
    tb(s, 0.55 + i * 4.1, 1.7, 3.95, 3.7, [(n + d, {"size": 44, "bold": True, "color": TEAL}), (h_, {"size": 22, "bold": True, "space": 10}), (b, {"size": 17, "color": INK2, "space": 10})],
       fill=TEALBG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
ask(s, 0.55, 5.65, W - 1.1, 1.25, "請暖暖分享", "①大型場次當天，誰負責複評？現場做完還是另約？　②後測日期什麼時候約？用什麼方式提醒？")
notes(s, "全市複評完成率 82.9%，暖暖 98.2%，最值得帶回去的流程。", "漏掉用藥／社會的 2 位都是只有聽力異常：常見誤會是「聽力只轉介」就不用往下做。")

# ───────────── 12 亮點2
s = new("看見暖暖｜值得學的地方 ②", "亮點：營養有固定轉介點，用藥有處置")
tb(s, 0.55, 1.6, 6, 0.48, "營養複評異常 10 人", 15, INK3, bold=True)
bar_chart(s, 0.45, 1.95, 6.1, 2.4, ["營養推廣中心", "自行就醫", "個案拒絕", "無紀錄"], [("人數", (6, 2, 1, 1))], gap=40, point_colors={1: AMBER, 2: ORANGE, 3: GREY}, size=15)
tb(s, 0.55, 4.45, 6.0, 1.6, [("MNA-SF 7–11 分的長輩，6 人轉介到營養推廣中心，是全份資料中轉介最完整的面向。", {"size": 16}),
                            ("介入點名稱寫成三種（營養推廣中心／社區營養推廣中心／轉介營養中心），統計時要統一。", {"size": 14, "color": INK2, "space": 6})])
tb(s, 6.85, 1.6, 6, 0.48, "用藥評估異常 15 人", 15, INK3, bold=True)
bar_chart(s, 6.75, 1.95, 6.1, 2.4, ["有用藥處置", "無紀錄"], [("人數", (14, 1))], gap=60, point_colors={1: GREY}, size=15)
tb(s, 6.85, 4.45, 6.0, 1.6, [("止痛藥、安眠藥是主要問題；處置以「請長者向原處方醫師諮詢」為主。", {"size": 16}), ("用藥異常也要一併後測：15 人中 12 人已完成。", {"size": 14, "color": INK2, "space": 6})])
ask(s, 0.55, 6.05, W - 1.1, 0.95, "問暖暖", "營養中心的轉介怎麼建立？有沒有回饋單讓你們知道長輩真的去了？")
notes(s, "營養是暖暖最「接得住」的面向：有固定的下一站。", "用藥可以討論能否和社區藥局或藥事照護計畫連結。")

# ───────────── 13 有紀錄≠有介入
s = new("看見暖暖｜可以優化的地方 ①", "有紀錄不等於有介入：各面向給了什麼？")
cats = ["聽力（45）", "視力（31）", "行動（複評異常 12）", "營養（複評異常 10）", "認知（複評異常 6）", "用藥（15）"]
ser = [("衛教或轉介介入點", (3, 5, 0, 6, 2, 14)), ("已接受處置", (11, 14, 9, 0, 1, 0)), ("自行就醫", (11, 10, 2, 2, 3, 0)),
       ("拒絕／其他", (11, 1, 0, 1, 0, 0)), ("沒有任何紀錄", (9, 1, 1, 1, 0, 1))]
ch = bar_chart(s, 0.45, 1.55, 10.3, 5.2, cats, ser, kind=XL_CHART_TYPE.BAR_STACKED_100, colors=[TEAL, TEALMID, AMBER, ORANGE, GREY], legend=True, gap=45, overlap=100, size=14)
for ser_ in ch.plots[0].series:
    ser_.data_labels.show_value = True; ser_.data_labels.number_format = '0;;;'; ser_.data_labels.number_format_is_linked = False
    ser_.data_labels.position = XL_LABEL_POSITION.CENTER
tb(s, 10.9, 1.6, 1.95, 0.45, "實際介入", 14, INK3, bold=True)
for i, v in enumerate(["7%", "16%", "0%", "60%", "33%", "93%"]):
    tb(s, 10.9, 2.18 + i * 0.75, 1.95, 0.6, v, 22, ORANGEINK if v in ("7%", "16%", "0%") else TEAL, bold=True, anchor=MSO_ANCHOR.MIDDLE)
foot(s, "未轉介代碼：1 已接受處置（如追蹤治療、配戴輔具）、2 自行就醫、3 個案拒絕、4 其他。認知「其他」1 人同時有衛教，計入衛教。")
notes(s, "聽力與行動幾乎沒有主動介入，營養與用藥做得好。", "已接受處置、自行就醫有時是真的，但有沒有確認？確認方式要寫下來。", "即使不轉介，也可以給衛教單張或 LINE 長者量六力資源。")

# ───────────── 14 視聽
s = new("看見暖暖｜可以優化的地方 ②", "視力、聽力異常 74 人：轉介介入點 0 筆")
tb(s, 0.55, 1.6, 8, 0.48, "76 個異常面向（2 人視聽都異常）怎麼處理", 14, INK3, bold=True)
bar_chart(s, 0.45, 1.95, 8.3, 4.9, ["已接受處置", "自行就醫", "個案拒絕（聽力 10）", "沒有紀錄（聽力 9）", "其他", "轉介介入點"], [("面向數", (30, 22, 11, 10, 3, 0))],
          gap=40, point_colors={0: TEALMID, 1: AMBER, 2: ORANGE, 3: ORANGE}, size=16)
card(s, 9.0, 1.6, 3.8, 1.75, None, "聽力拒絕常是「覺得是退化、不影響生活」。這時衛教比轉介更關鍵：聽損和跌倒、失智、社交退縮有關。", fill=LIGHT, size=15)
card(s, 9.0, 3.5, 3.8, 1.75, None, "視力異常且有糖尿病、未定期看眼科者，須知寫明應轉介醫療院所；高風險眼科調查「慢性疾病」勾選 92 人。", fill=LIGHT, size=15)
ask(s, 9.0, 5.4, 3.8, 1.45, "問大家", "聽力異常轉到哪裡？有合作的耳鼻喉科或聽力師嗎？", ORANGEINK)
foot(s, "另有 8 個面向同時給了衛教指導。")
notes(s, "視聽沒有複評也沒有後測，平台上很容易「填完原因就結束」。", "已接受處置 30 個：寫下是什麼處置（眼鏡、助聽器、定期回診）。")

# ───────────── 15 行動
s = new("看見暖暖｜可以優化的地方 ③", "行動複評異常 12 人：沒有一人接到運動資源")
for i, (n, h_, b, fc, nc) in enumerate([("0 / 12", "主動介入", "9 人填「已接受處置」、2 人「自行就醫」、1 人無紀錄；沒有據點、運動課或單位直接介入。", ORANGEBG, ORANGEINK),
                                        ("5 / 12", "沒有後測", "行動是後測流失最多的面向；其中 4 人的 6 個月窗口已過。", ORANGEBG, ORANGEINK),
                                        ("9 / 11", "跌倒卻行動正常", "用藥／社會評估中 11 人一年內跌倒，只有 2 人行動初評異常。", AMBERBG, INK)]):
    tb(s, 0.55 + i * 4.1, 1.7, 3.95, 3.55, [(n, {"size": 44, "bold": True, "color": nc}), (h_, {"size": 22, "bold": True, "space": 10}), (b, {"size": 17, "color": INK2, "space": 10})],
       fill=fc, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.55, 5.5, 6.05, 1.4, "可以連結的資源", "社區照顧關懷據點與 C 據點的預防及延緩失能方案、衛生所自辦運動班、肌力課程。", size=15)
ask(s, 6.75, 5.5, 6.05, 1.4, "問暖暖", "「已接受處置」指的是什麼？復健、長照，還是已參加運動班？", ORANGEINK)
notes(s, "行動是最能透過介入進步、也最容易在後測看見改善的面向，現在卻是最空的一格。", "跌倒的長輩即使起身在 12 秒內，也值得給防跌衛教。")

# ───────────── 16 數據品質
s = new("看見暖暖｜可以優化的地方 ④", "數字能不能相信？五個要先確認的資料問題")
items = [("「9999」代表什麼？", "起身測試 10 人填 9999；SPPB 有 8 人各項全是 9999、總分 0 分（65–74 歲）。是「無法完成」還是「沒測」？", "18 筆"),
         ("SPPB 0 分，社會評估卻正常", "若真的無法並排站 10 秒，日常行動應有困難；但社會評估中行動、如廁、穿衣有困難的只有 1 人。", "矛盾"),
         ("起身時間全是整數", "646 筆沒有小數；剛好 12 秒有 27 人（12 秒內算正常）；4 秒以內 10 人，其中 2 人 2 秒。", "計時方式"),
         ("流程漏項", "初評異常未做用藥／社會 2 人；認知異常未做 BHT/AD8 1 人；確認異常完全無介入紀錄 7 人。", "10 人"),
         ("自由文字不一致", "營養介入點寫成三種名稱；未轉介說明多數空白，只有 4 筆有文字。", "統計困難")]
for i, (h_, b, tag) in enumerate(items):
    yy = 1.65 + i * 1.06
    box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(yy + 0.18), Inches(0.3), Inches(0.3)); box.fill.background(); box.line.color.rgb = INK2; box.line.width = Pt(1.5)
    tb(s, 1.05, yy, 9.9, 1.0, [(h_, {"size": 18, "bold": True}), (b, {"size": 14, "color": INK2, "space": 2})])
    tb(s, 11.0, yy, 1.8, 0.7, tag, 17, ORANGEINK, bold=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    if i < 4:
        l = s.shapes.add_connector(1, Inches(0.55), Inches(yy + 1.0), Inches(W - 0.55), Inches(yy + 1.0)); l.line.color.rgb = RULE
notes(s, "9999 最重要：若代表無法完成，這 8 位 60 多歲長輩功能很差，應轉介醫療或長照；若代表沒測，平台算成 0 分就變成假異常，還要後測。",
      "建議：秒數記到小數點一位；無法完成與拒測分開記錄並寫在說明欄。", "請大家回去抽 10 筆自己的資料看看。")

# ───────────── 17 認知憂鬱社會
s = new("看見暖暖｜可以優化的地方 ⑤", "認知、憂鬱、社會：資源連結還可以更多元")
for i, (lab, n, b1, b2) in enumerate([("認知｜複評異常 6 人", "1 人轉醫療", "3 人自行就醫、1 人已接受處置、1 人其他。失智共照中心 0 筆。", "複評未達異常（或未複評）的 16 人，沒有任何衛教紀錄。"),
                                      ("憂鬱｜初評異常 5 人", "0 筆衛教", "GDS-15 都在 3–6 分，未達異常，因此沒有任何後續紀錄。", "初評有心煩或活動減少，仍值得給情緒衛教或據點資訊。"),
                                      ("社會照護與支持｜108 人", "1 人異常", "「孤獨／沒有固定社交活動」0 人；唯一異常者已申請長照。", "是長輩真的都很好，還是問法讓長輩不好意思說？")]):
    tb(s, 0.55 + i * 4.1, 1.7, 3.95, 3.75, [(lab, {"size": 14, "bold": True, "color": INK3}), (n, {"size": 30, "bold": True, "color": TEAL, "space": 6}),
                                            (b1, {"size": 16, "space": 10}), (b2, {"size": 15, "color": INK2, "space": 10})],
       line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.22, anchor=MSO_ANCHOR.MIDDLE)
ask(s, 0.55, 5.7, W - 1.1, 1.2, "問大家", "複評正常的長輩，你們會給什麼？「初評異常、複評正常」是不是被忽略的族群？", ORANGEINK)
notes(s, "初評異常但複評正常的長輩，是最適合做預防的人。", "社會評估第 3 題 0 人：可以補一句「平常一週出門幾次？」", "失智共照中心 0 筆：請衛生局提供各區窗口。")

# ───────────── 18 後測
s = new("看見暖暖｜追蹤與後測", "後測 29 / 39：6 人已錯過，4 人還來得及")
tb(s, 0.55, 1.6, 8, 0.48, "各面向後測完成（人）", 14, INK3, bold=True)
ch = bar_chart(s, 0.45, 1.95, 8.3, 4.5, ["營養（90%）", "只有用藥（83%）", "認知（67%）", "行動（58%）"], [("完成後測", (9, 10, 4, 7)), ("未完成", (1, 2, 2, 5))],
               kind=XL_CHART_TYPE.BAR_STACKED, colors=[TEAL, ORANGE], legend=True, gap=45, overlap=100, size=16)
foot(s, "1 人同時有認知與行動異常，兩列都計入。後測窗口以 2026/11/19 計算。")
card(s, 9.0, 1.6, 3.8, 1.65, "已超過 6 個月：6 人", "1 月評估 3 人、3–4 月評估 3 人；行動 4 人、認知 2 人。", fill=ORANGEBG, headc=ORANGEINK, size=15, headsize=17)
card(s, 9.0, 3.4, 3.8, 1.65, "窗口內還可完成：4 人", "最晚期限 12/28、1/22、1/29、2/11（跨年度依衛生局規定）。", size=15, headsize=17)
card(s, 9.0, 5.2, 3.8, 1.65, "匯出資料沒有追蹤欄位", "無法確認「先追蹤、再後測」，請暖暖補充追蹤紀錄。", fill=LIGHT, headc=INK, size=15, headsize=17)
notes(s, "後測 74% 已比全市好，流失集中在行動與 1 月的大量場次。", "建議：介入計畫當天就約好追蹤日（第 1–2 個月）與後測日（第 4 個月），每月第一週核對到期名單。")

# ───────────── 19 小結
s = new("看見暖暖｜小結", "暖暖衛生所：流程完整度高，下一步是讓介入「接得住」")
good = ["1. 複評＋用藥社會評估完成 98%", "2. 後測率 74%，營養組 90%", "3. 營養固定轉介到營養推廣中心", "4. 用藥異常 15 人中 14 人有處置", "5. 首篩比 73%，持續找到新長輩"]
gap_ = ["1. 視聽 74 人沒有轉介介入點，衛教只有 8 筆", "2. 行動 12 人沒有運動資源，後測流失 5 人", "3. 9999、整數秒等資料規則需要統一", "4. 初評異常、複評正常者沒有衛教", "5. 75 歲以上只占 11%"]
tb(s, 0.55, 1.7, 5.95, 5.2, [("值得帶回去學的", {"size": 22, "bold": True})] + [(g, {"size": 18, "space": 14}) for g in good], fill=TEALBG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.3, anchor=MSO_ANCHOR.MIDDLE)
tb(s, 6.85, 1.7, 5.95, 5.2, [("可以一起優化的", {"size": 22, "bold": True})] + [(g, {"size": 18, "space": 14}) for g in gap_], fill=ORANGEBG, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.3, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "請暖暖回應：右邊五點，哪些是資料呈現的問題、哪些是真的流程問題？")

# ───────────── 20 divider
s = divider("第二段｜反思自己", "反思自己", "PART 2 · REFLECT & ADJUST", "同一套指標，套回你們單位。找一個最大的缺口，帶一件事回去改。",
            [("同儕提問", "向暖暖請教做法"), ("自我診斷", "算出自己的指標"), ("分組討論", "原因與對策"), ("行動承諾", "30 天改一件事")])
notes(s, "請各單位拿出自己的平台報表或匯出檔。")

# ───────────── 21 同儕提問
def qslide(sec, title, qs, side_head, side, minutes, color=ORANGE):
    s = new(sec, title)
    for i, (q, sub) in enumerate(qs):
        yy = 1.7 + i * (5.2 / len(qs))
        tb(s, 0.55, yy + 0.05, 0.7, 0.45, f"Q{i+1}", 15, WHITE, bold=True, fill=color, shape=MSO_SHAPE.ROUNDED_RECTANGLE, align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE, pad=0.02)
        tb(s, 1.4, yy, 7.6, 5.2 / len(qs) - 0.05, [(q, {"size": 19, "bold": True}), (sub, {"size": 14, "color": INK3, "space": 3})])
    tb(s, 9.4, 1.7, 3.4, 1.4, [("討論時間", {"size": 14, "bold": True, "color": INK3}), (f"{minutes} 分鐘", {"size": 36, "bold": True, "color": TEAL})], line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.18, anchor=MSO_ANCHOR.MIDDLE)
    tb(s, 9.4, 3.3, 3.4, 3.6, [(side_head, {"size": 17, "bold": True})] + [(x, {"size": 16, "space": 12}) for x in side], fill=LIGHT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.22, anchor=MSO_ANCHOR.MIDDLE)
    return s
s = qslide("反思自己｜同儕提問", "先問「怎麼做到」：向暖暖請教 5 個問題",
           [("大型場次的動線怎麼排，讓複評、用藥、社會評估當天做完？", "人力配置、站點順序、AD8 由誰回答"), ("後測是什麼時候約、怎麼提醒的？", "約定時機、名單管理、電訪或面訪"),
            ("營養推廣中心的轉介是怎麼建立的？", "窗口、轉介單、回饋方式"), ("「已接受處置」「自行就醫」怎麼確認？", "看藥袋、問診所、看輔具，還是長輩口述"), ("9999 在你們單位的意思是什麼？", "無法完成、拒測、未測如何區分")],
           "記錄重點", ["① 可以直接照做的做法", "② 需要衛生局協助的資源", "③ 自己單位不適用的原因"], 10)
notes(s, "每題請暖暖用 1–2 分鐘回答，其他單位可以追問。", "主持人把可以直接照做的做法寫在白板。")

# ───────────── 22 自我診斷（紙本）
s = new("反思自己｜工具", "單位自我診斷：填入你們的數字，和暖暖放在一起看")
rows = [["指標", "算法", "暖暖", "全市", "我們的分子／分母", "我們的 %"],
        ["首篩比", "首次評估 ÷ 評估", "72.9%", "—", "＿＿＿ / ＿＿＿", ""],
        ["75 歲以上比例", "75 歲以上 ÷ 評估", "11.1%", "—", "＿＿＿ / ＿＿＿", ""],
        ["初評異常率", "初評異常 ÷ 評估", "17.0%", "15.0%", "＿＿＿ / ＿＿＿", ""],
        ["複評完成率", "完成複評 ÷ 初評異常", "98.2%", "82.9%", "＿＿＿ / ＿＿＿", ""],
        ["異常率", "確認異常 ÷ 評估", "14.7%", "11.3%", "＿＿＿ / ＿＿＿", ""],
        ["介入率", "有紀錄 ÷ 確認異常", "92.6%", "89.0%", "＿＿＿ / ＿＿＿", ""],
        ["實際介入率", "衛教或轉介 ÷ 確認異常", "26.3%", "—", "＿＿＿ / ＿＿＿", ""],
        ["後測率", "完成後測 ÷ 到期應後測", "74.4%", "57.7%", "＿＿＿ / ＿＿＿", ""]]
table(s, 0.55, 1.65, W - 1.1, rows, [2.3, 3.2, 1.3, 1.3, 2.75, 1.38], rowh=0.55, size=16, hl_col=2)
tb(s, 0.55, 6.7, W - 1.1, 0.4, "篩選線：異常率 <10%、介入率 <50%、後測率 <30%。網頁版有自動計算器。", 13, INK3)
notes(s, "請一個自願單位報數字，現場算一次。", "全市數字沒有首次評估、實際介入、75 歲以上欄位，留白。")

# ───────────── 23 分組討論
s = qslide("反思自己｜分組討論", "分組討論：我們也有一樣的卡點嗎？",
           [("你們的「實際介入率」大概是多少？", "扣掉只填未轉介原因的人，還剩幾成"), ("視力、聽力、行動異常，你們的固定下一站在哪？", "說出一個具體的單位名稱和聯絡方式"),
            ("抽 10 筆自己的資料：有沒有 9999、整數秒、空白說明？", "寫下要統一的記錄規則"), ("暖暖的哪一個做法，你們下個月就能試？", "選一個寫進行動承諾卡")],
           "分工", ["組長：帶討論、控時、上台報告", "記錄：卡點 → 原因 → 對策", "報告：第一組完整報告，第二組只補充沒提過的"], 20)
notes(s, "巡場時優先聽 Q2：要具體到單位名稱。", "剩 5 分鐘提醒寫行動承諾卡。")

# ───────────── 24 工具箱
s = new("反思自己｜可以帶回去的做法", "優化策略工具箱：依流程站點挑一個")
tools = [("1 場次動線", "對應：複評、用藥社會漏項", ["初評異常當場貼標，帶到複評站", "視聽異常也要走用藥＋社會", "離場前由一人核對漏項"]),
         ("2 介入清單", "對應：實際介入率", ["每個面向準備 1 張衛教＋1 個固定轉介點", "拒絕轉介也給衛教與 LINE 資源", "單位自辦課程勾「直接介入」"]),
         ("3 視聽與行動", "對應：轉介 0 筆、行動 0 介入", ["建立合作眼科、耳鼻喉科名單", "行動異常連結據點延緩失能方案", "跌倒者加給防跌衛教"]),
         ("4 記錄規則", "對應：9999、整數秒", ["秒數記到小數點一位", "無法完成／拒測／未測分開記錄", "「已接受處置」寫出是什麼"]),
         ("5 到期名單", "對應：後測流失", ["介入當天約好追蹤日與後測日", "每月第一週核對 3–6 個月到期名單", "大型場次後一週集中電訪"]),
         ("6 找到高齡者", "對應：75 歲以上 11%", ["結合居家訪視、門診、長照個案", "請據點推薦少出門的長輩", "家屬陪同場次填 AD8"])]
for i, (h_, tg, li) in enumerate(tools):
    xx = 0.55 + (i % 3) * 4.1; yy = 1.65 + (i // 3) * 2.68
    tb(s, xx, yy, 3.95, 2.55, [(h_, {"size": 20, "bold": True}), (tg, {"size": 13, "bold": True, "color": INK3, "space": 2})] + [("・" + x, {"size": 15, "color": INK2, "space": 6}) for x in li],
       line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.2, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "六格對應今天的六個發現；每個單位只要挑一格。", "匯出資料給他人前，記得刪除評估人員姓名、身分證字號等欄位。")

# ───────────── 25 行動承諾（紙本）
s = new("反思自己｜行動承諾", "30 天行動承諾卡")
fields = [("單位", 0.55, 1.7, 5.9, 0.9), ("要改善的指標", 6.75, 1.7, 6.05, 0.9), ("現況", 0.55, 2.8, 5.9, 0.9), ("30 天後目標", 6.75, 2.8, 6.05, 0.9),
          ("具體做法（誰、何時、怎麼做）", 0.55, 3.9, 12.25, 1.75), ("檢核日期", 0.55, 5.85, 5.9, 0.95), ("需要衛生局協助的事", 6.75, 5.85, 6.05, 0.95)]
for lab, x, y, w, h in fields:
    tb(s, x, y, w, h, lab, 14, INK3, bold=True, line=INK3, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.1)
tb(s, 0.55, 6.9, W - 1.1, 0.4, "寫法提醒：只選一個指標・目標要能在 30 天內看到・做法寫到「誰」和「哪一天」。這張卡會在下一次共學或訪查時一起回顧。", 12, INK3)
notes(s, "現場示範一個單位填寫；請各單位帶回。", "收卡後由主辦單位彙整，作為下次共學的開場。")

# ───────────── 26 資料說明
s = new("附錄", "資料說明與參考資料")
tb(s, 0.55, 1.7, 5.95, 5.2, [("資料與計算方式", {"size": 15, "bold": True, "color": INK3})] + [(x, {"size": 15, "space": 10}) for x in [
    "資料：暖暖衛生所 ICOPE 匯出檔，評估日期 2026/01/04–08/11，共 646 筆，個案以代號呈現。", "確認異常＝複評異常（含用藥、社會）＋視力或聽力異常。",
    "實際介入＝有衛教指導、介入點類型，或用藥介入內容。", "後測：以複評異常 39 人為應後測人數；窗口以 2026/11/19 計算。", "匯出檔中的評估人員姓名與身分證字號欄位未使用、未呈現。"]],
   line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
tb(s, 6.85, 1.7, 5.95, 5.2, [("參考資料", {"size": 15, "bold": True, "color": INK3})] + [(x, {"size": 15, "space": 10}) for x in [
    "115 年長者內在能力檢測服務須知（縣市衛生局公告版）：服務流程、追蹤 1 個月後、後測 3–6 個月、服務費。", "國民健康署 ICOPE 長者內在能力檢測量表（114 年 10 月修訂）與追蹤表：未轉介原因代碼、介入點類型。",
    "2026 基隆市機構訪查篩選表彙整（10 月共學）：全市與衛生所合計指標、篩選線。", "國民健康署新聞：114 年全國約 35.5 萬名長者接受評估。"]],
   line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "若暖暖對任何數字有不同的統計方式，以單位說明為準。")

# ───────────── 27 結尾
s = divider("系統討論結束", "謝謝暖暖", "THANK YOU FOR SHARING", "把別人做得好的流程帶回去，把自己卡住的地方說出來，這就是共學。",
            [("找得到", "首篩、高齡者"), ("做得完", "複評、用藥社會"), ("接得住", "衛教與轉介"), ("追得到", "追蹤與後測")])
notes(s, "接著進行個案討論；行動承諾卡請在活動結束前繳回。")

exec(open("ppt_case.py", encoding="utf-8").read())
out = sys.argv[1] if len(sys.argv) > 1 else ("ICOPE共學_個案＋系統討論_白底黑字.pptx" if MONO else "ICOPE共學_個案＋系統討論.pptx")
prs.save(out)
print("saved", out, "slides", len(prs.slides))
print("\n".join(WARN) if WARN else "no fit warnings")
