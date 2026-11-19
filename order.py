# parts/slides.html（系統）＋ parts/case.html（個案）＋ parts/agenda_break.html
# → parts/deck_order.html。順序依議程：封面→議程→流程→個案→休息→系統→結尾
import re
def split(path, pat):
    out = {}
    for p in re.split(r'(?=<!-- ───────── (?:%s))' % pat, open(path).read()):
        m = re.match(r'<!-- ───────── (%s)' % pat, p)
        if m: out[m.group(1)] = p
    return out
d = split('parts/slides.html', r'\d\d'); c = split('parts/case.html', r'C\d+'); x = split('parts/agenda_break.html', r'AG|BR')
c0 = c['C0'].replace('<span class="sec">個案討論</span>', '<span class="sec">第一段｜10:05–11:15</span>').replace('PART 3 · CASE CONFERENCE', 'PART 1 · 案例討論與反饋')
d['05'] = d['05'].replace('<span class="sec">第一段</span>', '<span class="sec">第二段｜11:20–12:15</span>').replace('PART 1 · SEE THE SYSTEM', 'PART 2 · 數據分析與策略研討')
d['02'] = d['02'].replace('開場｜系統討論的目的', '第二段｜系統討論的目的').replace('今天分兩段：第一段看見暖暖，第二段反思自己；每段都有討論時間。', '系統討論分兩部分：先看見暖暖，再反思自己；每部分都有討論時間。')
d['04'] = d['04'].replace('開場｜指標定義', '第二段｜指標定義')
d['20'] = d['20'].replace('<span class="sec">第二段</span>', '<span class="sec">第二段｜反思自己</span>')
d['01'] = d['01'].replace('共學活動・系統討論', '共學活動・案例討論＋系統討論').replace('<p class="cover-sub">系統討論：以<b>暖暖衛生所</b>的服務數據為例</p>', '<p class="cover-sub">個案討論＋系統討論：以<b>暖暖衛生所</b>的服務為例</p>').replace('<h1>看見別人的流程<br>調整自己的流程</h1>', '<h1>看見一個人<br>看見一套流程</h1>')
order = [d['01'], x['AG'], d['03'], c0] + [c[f'C{i}'] for i in range(1, 11)] + [x['BR'], d['02'], d['04'], d['05']] + [d[f'{i:02d}'] for i in range(6, 27)] + [c['C11']]
open('parts/deck_order.html', 'w').write(''.join(order))
print('slides', len(order))
