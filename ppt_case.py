# 由 ppt_build.py exec：議程、個案討論、休息、結尾，最後依議程重排並加頁碼。
N_SYS = len(prs.slides)  # 27 張系統討論（含封面、流程與舊結尾）

# ── 議程
s = new("開場｜議程", "今日議程：先看個案，再看系統")
rows = [["時間", "議程", "主持人／主講者"],
        ["09:30–10:00", "報到", ""],
        ["10:00–10:05", "開場與人員介紹", "衛生局"],
        ["10:05–11:15", "共學主題報告（一）案例討論與反饋\n營養個案：初評 → 複評 → 介入 → 後測", "報告：暖暖區衛生所 李麗芳 主任\n專家委員・講師主持人"],
        ["11:15–11:20", "休息", ""],
        ["11:20–12:15", "共學主題報告（二）數據分析與策略研討\n暖暖衛生所 646 筆數據 → 反思自己單位", "報告：暖暖區衛生所 李麗芳 主任\n專家委員・講師主持人"],
        ["12:15–12:30", "滿意度調查、大合照", ""]]
t = table(s, 0.55, 1.7, W - 1.1, rows, [2.2, 6.5, 3.53], rowh=0.66, size=17)
for i in (3, 5):
    t.rows[i].height = Inches(1.0)
    for j in range(3):
        t.cell(i, j).fill.solid(); t.cell(i, j).fill.fore_color.rgb = TEALBG
notes(s, "第一段個案討論 70 分鐘，第二段系統討論 55 分鐘。", "兩段都是：先看資料 → 分組討論 → 第一組完整報告、第二組補充 → 專家回饋。")

# ── C0 divider
s = divider("第一段｜10:05–11:15", "個案討論", "PART 1 · 案例討論與反饋", "69 歲的她吃得少、瘦了。要是你，會怎麼介入、轉給誰？\n報告：暖暖區衛生所 李麗芳 主任",
            [("認識她", "初評、複評、用藥社會"), ("先想再看", "你會給什麼"), ("看結果", "實際做法與後測"), ("補完整", "更完整的介入計畫")])
notes(s, "營養是暖暖做得最好的面向，現在用一位長輩看細節。", "個案已去識別化，只保留性別、年齡與評估結果。")

# ── C1 認識個案
s = new("個案討論｜認識個案", "她是誰？69 歲女性，無慢性病，只有營養亮紅燈")
prof = [("性別／年齡", "女性，69 歲"), ("慢性病史", "無"), ("用藥", "無多重用藥、無止痛或安眠藥"), ("跌倒", "過去一年無"), ("初評異常", "營養"), ("複評異常", "營養 MNA-SF 9 分")]
items = [("個案基本資料", {"size": 14, "bold": True, "color": INK3})]
for k, v in prof: items.append((f"{k}　{v}", {"size": 18, "space": 12}))
tb(s, 0.55, 1.7, 5.3, 4.2, items, line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
tl = [("2026/05/08・Day 0", "初評＋MNA-SF 複評", "營養異常，轉介社區營養推廣中心", False),
      ("Day 30 之後", "追蹤", "確認是否成功轉介營養中心", False),
      ("Day 91–183", "後測窗口", "評估後 3–6 個月", False),
      ("2026/08/28・Day 112", "後測 MNA-SF", "9 分 → 12 分", False)]
ln = s.shapes.add_connector(1, Inches(6.35), Inches(1.85), Inches(6.35), Inches(5.65)); ln.line.color.rgb = TEAL; ln.line.width = Pt(3)
for i, (d_, h_, b, gap) in enumerate(tl):
    yy = 1.7 + i * 1.05
    dot = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(6.23), Inches(yy + 0.12), Inches(0.24), Inches(0.24))
    if gap: dot.fill.solid(); dot.fill.fore_color.rgb = WHITE; dot.line.color.rgb = ORANGE; dot.line.dash_style = 4
    else: dot.fill.solid(); dot.fill.fore_color.rgb = TEAL; dot.line.fill.background()
    tb(s, 6.65, yy, 6.15, 1.0, [(d_, {"size": 12, "color": INK3}), (h_, {"size": 19, "bold": True, "color": ORANGEINK if gap else INK}), (b, {"size": 14, "color": ORANGEINK if gap else INK2})])
ask(s, 0.55, 6.05, W - 1.1, 0.95, "先想一下", "只看到「營養異常」四個字時，你腦中第一個想到的介入是什麼？", ORANGEINK)
notes(s, "看起來很健康的長輩：沒有慢性病、用藥問題，行動和認知都好。", "後測第 112 天完成，落在 3–6 個月窗口內；暖暖有追蹤，確認是否成功轉介營養中心。")

# ── C2 初評
s = new("個案討論｜初評", "初評六力：只有「食慾不振」回答是")
rows = [["面向", "初評題目", "她的結果", "判定"],
        ["A 認知", "記憶 3 項物品、日期、地點", "3 題都答對", "正常"],
        ["B 行動", "起立坐下 5 次是否 >12 秒", "7 秒", "正常"],
        ["C 營養", "① 3 個月體重無意減輕 ≥3 公斤\n② 3 個月內食慾不振", "① 否\n② 是", "異常"],
        ["D 視力", "自覺困難＋WHO 遠／近距離", "無困難，遠近都通過", "正常"],
        ["E 聽力", "氣音測試", "兩耳都聽得到", "正常"],
        ["F 憂鬱", "心煩沒希望、活動興趣減少", "兩題都否", "正常"]]
t = table(s, 0.55, 1.65, W - 1.1, rows, [1.8, 5.2, 3.6, 1.63], rowh=0.6, size=17)
t.rows[3].height = Inches(0.95)
for j in range(4):
    c_ = t.cell(3, j); c_.fill.solid(); c_.fill.fore_color.rgb = ORANGEBG
    for p_ in c_.text_frame.paragraphs:
        for r_ in p_.runs: r_.font.bold = True
ask(s, 0.55, 6.08, W - 1.1, 0.95, "討論", "體重減輕題回答「否」，但 MNA-SF 顯示體重下降 1–3 公斤。初評時要怎麼問，長輩才答得準？")
notes(s, "初評門檻是 3 公斤，掉 1–3 公斤的長輩會回答否；讓她進入複評的是食慾不振。", "建議問法：最近衣服、褲頭有沒有變鬆？跟過年比有沒有瘦？")

# ── C3 MNA-SF
s = new("個案討論｜複評", "MNA-SF 9 分：有營養不良風險，BMI 是最低分的一項")
bar_chart(s, 0.45, 1.6, 7.9, 5.3, ["A 食量（滿分 2）", "B 體重（滿分 3）", "C 活動（滿分 2）", "D 急病（滿分 2）", "E 精神（滿分 2）", "F BMI（滿分 3）"],
          [("得分", (1, 2, 2, 2, 2, 0)), ("滿分", (2, 3, 2, 2, 2, 3))], gap=40, overlap=-5, legend=True, colors=[ORANGE, GREY], size=15, maxv=3.4, numfmt='0')
bignum(s, 8.6, 1.6, 4.2, "9", " / 14", "MNA-SF 總分", "12–14 正常・8–11 有營養不良風險・0–7 營養不良", color=ORANGEINK, fill=ORANGEBG, h=1.9)
card(s, 8.6, 3.65, 4.2, 1.5, None, "扣分點連在一起看：吃得少＋瘦了＋本來就偏瘦（BMI 低於 19）。活動、急病、精神都滿分。", fill=LIGHT, size=15)
ask(s, 8.6, 5.3, 4.2, 1.6, "討論", "沒有慢性病的 69 歲女性，食慾變差又變瘦，你會想先排除什麼？", ORANGEINK)
notes(s, "食量 1 分＝中度減少；體重 2 分＝下降 1–3 公斤；BMI 0 分＝低於 19。", "非預期體重下降＋食慾不振，在沒有已知慢性病的長輩身上，值得請醫師評估口腔牙齒、腸胃、甲狀腺或其他問題。")

# ── C4 用藥社會
s = new("個案討論｜用藥＋社會照護", "用藥、社會照護、跌倒都是「否」，評估日期要一起更新")
lst = [("用藥評估", {"size": 15, "bold": True, "color": INK3})] + [("否　" + x, {"size": 16, "space": 6}) for x in ["每天 10 種以上藥物", "止痛藥、安眠藥", "用藥後頭暈、口乾等症狀"]]
lst += [("社會照護與支持", {"size": 15, "bold": True, "color": INK3, "space": 14})] + [("否　" + x, {"size": 16, "space": 6}) for x in ["日常生活（如廁、穿衣、進食…）有困難", "居住或財務有困難", "感覺孤獨、沒有固定社交活動"]]
lst += [("跌倒", {"size": 15, "bold": True, "color": INK3, "space": 14}), ("否　過去一年跌倒", {"size": 16, "space": 6})]
tb(s, 0.55, 1.65, 6.0, 5.3, lst, line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.25, anchor=MSO_ANCHOR.MIDDLE)
card(s, 6.85, 1.65, 5.95, 1.9, "資料提醒", ["匯出的社會照護評估日期是 2026/01/06；經暖暖確認，實際與初評同一天（05/08），是日期欄位沒改到。", ("日期沒更新，匯出後看起來就像沿用舊紀錄；登打完記得核對。", {"size": 15, "color": INK2, "space": 4})], fill=ORANGEBG, headc=ORANGEINK, size=17)
card(s, 6.85, 3.7, 5.95, 1.5, None, "對營養個案來說，社會評估特別重要：誰備餐、錢夠不夠、是否一個人吃飯，都會影響「吃得少」。", fill=LIGHT, size=16)
ask(s, 6.85, 5.35, 5.95, 1.6, "討論", "如果社會評估是 4 個月前的答案，你會相信它嗎？要補問哪幾句？", ORANGEINK)
notes(s, "初評任一項異常就要當次做用藥與社會照護評估；這位長輩當天有做，只是日期欄位沒改到。", "補問：一天吃幾餐？誰煮？一個人吃還是和家人吃？最近生活有沒有變化？")

# ── C5 討論①
s = new("個案討論｜討論① 先想再看", "要是你：會給她哪些介入？轉給誰？")
tb(s, 0.55, 1.55, 8.4, 0.45, "在你會做的項目打勾（可複選），再和旁邊的人比一比。", 15, INK2)
opts = [("居家健康管理衛教", "少量多餐、蛋白質、體重紀錄"), ("社區營養推廣中心", "營養師諮詢、團體課"), ("轉介醫療院所", "家醫科：體重下降原因"), ("社區據點・共餐", "有人一起吃、活動量"),
        ("牙科／口腔評估", "咀嚼、假牙、吞嚥"), ("單位直接介入", "衛生所自辦課程、電訪"), ("長照管理中心", "備餐、送餐需求"), ("其他：＿＿＿＿＿＿", "寫在下方空白處")]
for i, (a, b) in enumerate(opts):
    xx = 0.55 + (i % 2) * 4.25; yy = 2.05 + (i // 2) * 1.2
    box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(xx + 0.15), Inches(yy + 0.33), Inches(0.32), Inches(0.32)); box.fill.background(); box.line.color.rgb = INK2; box.line.width = Pt(1.5)
    tb(s, xx + 0.55, yy, 3.55, 1.1, [(a, {"size": 18, "bold": True}), (b, {"size": 14, "color": INK2, "space": 2})], anchor=MSO_ANCHOR.MIDDLE)
    fr = s.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(xx), Inches(yy), Inches(4.1), Inches(1.1)); fr.adjustments[0] = 0.08; fr.fill.background(); fr.line.color.rgb = RULE
tb(s, 9.3, 1.55, 3.5, 1.3, [("個人思考", {"size": 14, "bold": True, "color": INK3}), ("5 分鐘", {"size": 36, "bold": True, "color": TEAL})], line=RULE, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.18, anchor=MSO_ANCHOR.MIDDLE)
tb(s, 9.3, 3.0, 3.5, 3.95, [("介入前，你還想多問她什麼？", {"size": 16, "bold": True})] + [(x, {"size": 15, "space": 10}) for x in ["① 一天吃幾餐、誰煮", "② 牙口、咀嚼、吞嚥", "③ 體重什麼時候開始掉", "④ 最近生活有沒有變化", "⑤ 有沒有看過醫師"]],
   fill=LIGHT, shape=MSO_SHAPE.ROUNDED_RECTANGLE, pad=0.22, anchor=MSO_ANCHOR.MIDDLE)
notes(s, "先不要翻下一頁，讓大家獨立想 5 分鐘再分享。", "注意有沒有人想到醫療：非預期體重下降不只是營養問題。")

# ── C6 實際介入
s = new("個案討論｜實際介入", "實際上：轉介社區營養推廣中心並追蹤，衛教與醫療沒有紀錄")
acts = [("有紀錄", "社區營養推廣中心", "介入點類型 8「社區營養推廣中心」，名稱寫「營養推廣中心」。", False),
        ("沒有紀錄", "居家健康管理衛教", "沒有勾選衛教指導，不確定是否給了單張或飲食建議。", True),
        ("沒有紀錄", "醫療評估", "非預期體重下降＋BMI 偏低，沒有轉介醫療或建議就醫的紀錄。", True),
        ("有追蹤", "追蹤", "暖暖有追蹤，確認她是否成功轉介營養中心；匯出資料沒有追蹤欄位，需單位補充。", False)]
for i, (tag, h_, b, miss) in enumerate(acts):
    xx = 0.55 + i * 3.08
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(xx), Inches(1.75), Inches(2.9), Inches(0.08)); bar.fill.solid(); bar.fill.fore_color.rgb = ORANGE if miss else TEAL; bar.line.fill.background()
    tb(s, xx, 1.95, 2.9, 3.9, [(tag, {"size": 15, "bold": True, "color": ORANGEINK if miss else TEAL}), (h_, {"size": 22, "bold": True, "space": 10}), (b, {"size": 17, "color": INK2, "space": 12})], anchor=MSO_ANCHOR.MIDDLE)
ask(s, 0.55, 6.05, W - 1.1, 0.9, "討論", "你的選擇和實際做法差在哪裡？少做的是「沒做」還是「沒記錄」？")
notes(s, "轉介營養推廣中心是對的方向，也是暖暖的強項。", "如果現場其實有給衛教或建議就醫，一定要記錄。", "暖暖有追蹤轉介是否成功；可再多問營養師建議與她回家後的改變。")

# ── C7 後測
s = new("個案討論｜後測", "第 112 天後測：MNA-SF 從 9 分進步到 12 分")
bar_chart(s, 0.45, 1.6, 7.9, 5.3, ["A 食量", "B 體重", "F BMI", "C 活動", "D 急病", "E 精神"], [("複評 05/08", (1, 2, 0, 2, 2, 2)), ("後測 08/28", (2, 3, 1, 2, 2, 2))],
          gap=40, overlap=-5, legend=True, colors=[AMBER, TEAL], size=15, maxv=3.4, numfmt='0')
bignum(s, 8.6, 1.6, 4.2, "9 → 12", " / 14", "MNA-SF 總分", "12 分已進入「正常營養狀況」範圍", h=1.9)
card(s, 8.6, 3.65, 4.2, 1.6, "又一個要確認的地方", "後測檔「後測異常項目」仍寫「營養」：是後測的面向，還是系統判定仍異常？", fill=ORANGEBG, headc=ORANGEINK, size=15)
ask(s, 8.6, 5.4, 4.2, 1.5, "討論", "BMI 從低於 19 變成 19–21，你會怎麼跟她說？要不要結案？")
notes(s, "食量恢復、體重不再下降、BMI 往上一級：體重有回升。", "12 分在正常範圍邊緣，BMI 只拿 1 分（滿分 3），還不算安全。")

# ── C8 分組討論
s = qslide("個案討論｜討論② 分組", "分組討論：如果重來一次，你會怎麼幫她？",
           [("她進步了，是誰的功勞？", "營養中心、她自己、家人，還是時間？追蹤時還要問到什麼才能回答"), ("除了營養中心，還應該加上哪一項介入或轉介？", "醫療、牙科、共餐據點、衛教；排出優先順序"),
            ("第 1 個月的追蹤電話，你會問哪 3 句？", "有沒有去、吃得怎樣、體重多少"), ("12 分之後：結案、持續追蹤，還是明年再評？", "BMI 仍偏低時要給她什麼提醒")],
           "產出", ["一份完整的個人介入計畫", "今天做什麼 → 1 個月追蹤 → 3–6 個月後測", "第一組完整報告，第二組只補充"], 20)
notes(s, "Q1 是最好的提問：追蹤確認了轉介，但要說明改善和介入的關係，還需要知道她後來做了什麼改變。", "Q2 期待聽到：建議就醫、牙口評估、共餐據點，並說明誰負責、怎麼聯繫。")

# ── C9 參考計畫
s = new("個案討論｜參考做法", "一份更完整的介入計畫：分三段時間")
plan = [("評估當天・Day 0", "衛教＋轉介＋約好時間", ["衛教：少量多餐、每餐有蛋白質、點心補充", "轉介社區營養推廣中心（留下窗口與日期）", "建議家醫科評估體重下降原因", "補問備餐、牙口；需要時連結共餐據點", "約好追蹤日與後測日"]),
        ("1 個月追蹤・Day 30–60", "確認有沒有到位", ["有沒有去營養中心？營養師建議什麼？", "有沒有看醫師？結果如何？", "這週吃幾餐、體重多少", "沒去的原因：交通、時間、不想去", "記錄追蹤方式與結果"]),
        ("後測・Day 91–183", "同一份量表再測", ["MNA-SF 後測，和複評逐項比較", "用藥、社會評估一併確認", "BMI 仍偏低：持續衛教與定期量體重", "說明改善與哪一項介入有關", "提醒隔年再評估"])]
for i, (n_, h_, li) in enumerate(plan):
    xx = 0.55 + i * 4.1
    bar = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(xx), Inches(1.7), Inches(3.95), Inches(0.08)); bar.fill.solid(); bar.fill.fore_color.rgb = TEAL; bar.line.fill.background()
    tb(s, xx, 1.9, 3.95, 4.8, [(n_, {"size": 14, "bold": True, "color": TEAL}), (h_, {"size": 21, "bold": True, "space": 6})] + [("・" + x, {"size": 16, "color": INK2, "space": 9}) for x in li])
foot(s, "本頁為討論用的參考做法，非唯一標準；轉介單位依各區資源調整。")
notes(s, "各組報告完之後再放這頁對照，不要一開始就給答案。", "重點不是做得多，而是每一項都有誰、何時、確認了沒。")

# ── C10 檢核表
s = new("個案討論｜帶回去用", "營養異常個案：六個檢核點")
chk = [("初評問法", "除了「瘦 3 公斤」，再問衣服有沒有變鬆、食慾有沒有變差", "初評"), ("MNA-SF 逐項看", "找出扣分在哪一項：食量、體重、BMI，還是活動、急病、精神", "複評"),
       ("當次完成用藥＋社會評估", "特別問備餐、經濟、一個人吃飯；日期要和初評同一天", "評估"), ("至少兩種介入", "衛教＋營養中心；體重非預期下降時建議就醫", "介入"),
       ("追蹤確認到位", "1 個月內電訪：有沒有去、吃得怎樣、體重多少，並記錄", "追蹤"), ("後測逐項比較並說明", "改善了什麼、和哪項介入有關；分數正常但 BMI 偏低仍要提醒", "後測")]
for i, (h_, b, tag) in enumerate(chk):
    yy = 1.65 + i * 0.88
    box = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(yy + 0.18), Inches(0.3), Inches(0.3)); box.fill.background(); box.line.color.rgb = INK2; box.line.width = Pt(1.5)
    tb(s, 1.05, yy, 10.0, 0.85, [(h_, {"size": 18, "bold": True}), (b, {"size": 14, "color": INK2, "space": 2})])
    tb(s, 11.2, yy, 1.6, 0.65, tag, 17, ORANGEINK, bold=True, align=PP_ALIGN.RIGHT, anchor=MSO_ANCHOR.MIDDLE)
    if i < 5:
        l = s.shapes.add_connector(1, Inches(0.55), Inches(yy + 0.85), Inches(W - 0.55), Inches(yy + 0.85)); l.line.color.rgb = RULE
notes(s, "這六點可以直接當成營養個案的自我檢核表。")

# ── 休息
s = divider("11:15–11:20", "休息 5 分鐘", "BREAK", "回來後進入第二段：數據分析與策略研討。請準備好自己單位的平台報表或匯出檔。", [])
notes(s, "休息時準備第二段的資料。")

# ── 結尾
s = divider("共學結束", "謝謝大家", "THANK YOU", "系統讓我們看見流程，個案讓我們看見一個人。兩個都顧到，介入才接得住。",
            [("問得準", "初評與複評"), ("給得多元", "衛教、轉介、醫療"), ("追得到", "確認到位"), ("說得清", "後測與改善原因")])
notes(s, "請大家繳回行動承諾卡與討論單。")

# ── 依議程重排：封面→議程→流程→個案 11 張→休息→系統（目的、指標、看見暖暖…資料說明）→結尾；舊「謝謝暖暖」移除
lst = prs.slides._sldIdLst; ids = list(lst)
A = N_SYS                          # 議程
CASE = list(range(A + 1, A + 12))  # C0–C10
BRK, END = A + 12, A + 13
order = [0, A, 2] + CASE + [BRK, 1, 3, 4] + list(range(5, 26)) + [END]
for e in ids: lst.remove(e)
for i in order: lst.append(ids[i])
drop = ids[26]
prs.part.drop_rel(drop.rId)
for n, sl in enumerate(prs.slides, 1):
    tb(sl, W - 1.6, 0.22, 1.05, 0.42, f"{n:02d}", 12, INK3, align=PP_ALIGN.RIGHT)
PAGE[0] = len(prs.slides)
