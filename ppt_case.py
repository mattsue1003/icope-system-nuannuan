# 由 ppt_build.py exec：議程、個案討論、休息、結尾，最後依議程重排並加頁碼。
N_SYS = len(prs.slides)  # 27 張系統討論（含封面、流程與舊結尾）

# ── 議程
s = new("開場｜議程", "今日議程：先看個案，再看系統")
rows = [["時間", "議程", "主持人／主講者"],
        ["09:30–10:00", "報到", ""],
        ["10:00–10:05", "開場與人員介紹", "衛生局"],
        ["10:05–11:15", "共學主題報告（一）案例討論與反饋\n營養個案：初評 → 複評 → 介入 → 後測", "報告：暖暖區衛生所 李麗芳 主任\n專家委員・講師主持人"],
        ["11:15–11:20", "休息", ""],
        ["11:20–12:15", "共學主題報告（二）數據分析與策略研討\n暖暖衛生所 646 筆數據 → 反思自己單位", "專家委員・講師主持人"],
        ["12:15–12:30", "滿意度調查、大合照", ""]]
t = table(s, 0.55, 1.7, W - 1.1, rows, [2.2, 6.5, 3.53], rowh=0.66, size=17)
for i in (3, 5):
    t.rows[i].height = Inches(1.0)
    for j in range(3):
        t.cell(i, j).fill.solid(); t.cell(i, j).fill.fore_color.rgb = TEALBG
notes(s, "第一段個案討論 70 分鐘，第二段系統討論 55 分鐘。", "兩段都是：先看資料 → 分組討論 → 第一組完整報告、第二組補充 → 專家回饋。")

# ── C1 個案簡介（主任簡介，一頁看完）
s = new("第一段｜10:05–11:15 案例討論與反饋", "營養個案：69 歲女性，食慾不振、體重下降")
prof = [("性別／年齡", "女性，69 歲"), ("慢性病史", "無"),
        ("初評六力", "認知、行動（起立坐下 7 秒）、視力、聽力、憂鬱皆正常；營養異常（3 個月內食慾不振：是；體重減輕 ≥3 公斤：否）"),
        ("複評", "MNA-SF 9 分，有營養不良風險"), ("用藥評估", "無 10 種以上藥物、無止痛藥或安眠藥、無用藥後不適"),
        ("社會照護", "日常生活、居住財務、孤獨社交皆無困難；過去一年無跌倒")]
items = [("個案基本資料與評估結果", {"size": 14, "bold": True, "color": INK3})]
for k, v in prof: items.append((f"{k}｜{v}", {"size": 16, "space": 10}))
tb(s, 0.55, 1.65, 6.6, 5.3, items, line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
tl = [("2026/05/08・Day 0", "初評＋複評＋用藥／社會照護評估", "營養異常，MNA-SF 9 分"),
      ("2026/05/08", "介入", "轉介社區營養推廣中心"),
      ("2026/06/30・Day 53", "追蹤", "確認是否成功轉介營養中心"),
      ("2026/08/28・Day 112", "後測 MNA-SF", "9 分 → 12 分（正常營養狀況）")]
ln = s.shapes.add_connector(1, Inches(7.6), Inches(1.8), Inches(7.6), Inches(6.2)); ln.line.color.rgb = TEAL; ln.line.width = Pt(3)
for i, (d_, h_, b_) in enumerate(tl):
    yy = 1.65 + i * 1.17
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(7.48), Inches(yy + 0.12), Inches(0.24), Inches(0.24)); dot.fill.solid(); dot.fill.fore_color.rgb = TEAL; dot.line.fill.background()
    tb(s, 7.9, yy, 4.9, 1.1, [(d_, {"size": 12, "color": INK3}), (h_, {"size": 18, "bold": True}), (b_, {"size": 15, "color": INK2})])
tb(s, 7.9, 6.45, 4.9, 0.4, "報告：暖暖區衛生所 李麗芳 主任｜個案已去識別化", 12, INK3)
notes(s, "六力中只有營養異常；初評體重題門檻 3 公斤，她回答否，讓她進入複評的是食慾不振。", "社會照護評估與初評同一天（05/08）。6/30 追蹤確認轉介營養中心情形；後測第 112 天，落在 3–6 個月窗口內。")

# ── C2 MNA-SF 逐項＋討論
s = new("第一段｜個案 MNA-SF 複評 → 後測", "MNA-SF 逐項：9 分 → 12 分")
rows = [["MNA-SF 題目", "複評 2026/05/08", "後測 2026/08/28"],
        ["A 過去三個月內有沒有因為食慾不振、消化問題、咀嚼或吞嚥困難而減少食量？", "1／2　食量中度減少", "2／2　食量沒有改變"],
        ["B 過去三個月內體重下降的情況", "2／3　體重下降 1–3 公斤", "3／3　體重沒有下降"],
        ["C 活動能力", "2／2　可以外出", "2／2　可以外出"],
        ["D 過去三個月內有沒有受到心理創傷或患上急性疾病？", "2／2　沒有", "2／2　沒有"],
        ["E 精神心理問題", "2／2　沒有精神心理問題", "2／2　沒有精神心理問題"],
        ["F1 身體質量指數（BMI）", "0／3　BMI 低於 19", "1／3　BMI 19 至低於 21"],
        ["總分（12–14 正常・8–11 有營養不良風險・0–7 營養不良）", "9／14　有營養不良風險", "12／14　正常營養狀況"]]
t = table(s, 0.55, 1.6, W - 1.1, rows, [6.4, 2.92, 2.91], rowh=0.5, size=15)
t.rows[1].height = Inches(0.85)
for i in (1, 2, 6):
    for j in range(3):
        c_ = t.cell(i, j); c_.fill.solid(); c_.fill.fore_color.rgb = ORANGEBG
for j in range(3):
    for p_ in t.cell(7, j).text_frame.paragraphs:
        for r_ in p_.runs: r_.font.bold = True
ask(s, 0.55, 6.05, W - 1.1, 0.9, "討論", "要是你，會怎麼提供這位長輩相關的介入和轉介？", ORANGEINK)
notes(s, "複評扣分在 A 食量、B 體重、F1 BMI；C、D、E 都滿分。", "後測三項都進步；12 分剛進入正常範圍，BMI 仍只拿 1 分（滿分 3）。", "主任簡介完，請專家委員與講師主持討論。")

# ── 休息
s = divider("11:15–11:20", "休息 5 分鐘", "BREAK", "回來後進入第二段：數據分析與策略研討。請準備好自己單位的平台報表或匯出檔。", [])
notes(s, "休息時準備第二段的資料。")

# ── 結尾
s = divider("共學結束", "謝謝大家", "THANK YOU", "系統讓我們看見流程，個案讓我們看見一個人。兩個都顧到，介入才接得住。",
            [("問得準", "初評與複評"), ("給得多元", "衛教、轉介、醫療"), ("追得到", "確認到位"), ("說得清", "後測與改善原因")])
notes(s, "請大家繳回行動承諾卡與討論單。")

# ── 依議程重排：封面→議程→流程→個案 2 張→休息→系統（目的、指標、看見暖暖…資料說明）→結尾；舊「謝謝暖暖」移除
lst = prs.slides._sldIdLst; ids = list(lst)
A = N_SYS                          # 議程
CASE = [A + 1, A + 2]             # 個案 2 張
BRK, END = A + 3, A + 4
order = [0, A, 2] + CASE + [BRK, 1, 3, 4] + list(range(5, 26)) + [END]
for e in ids: lst.remove(e)
for i in order: lst.append(ids[i])
drop = ids[26]
prs.part.drop_rel(drop.rId)
for n, sl in enumerate(prs.slides, 1):
    tb(sl, W - 1.6, 0.22, 1.05, 0.42, f"{n:02d}", 12, INK3, align=PP_ALIGN.RIGHT)
PAGE[0] = len(prs.slides)
