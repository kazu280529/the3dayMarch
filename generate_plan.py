# -*- coding: utf-8 -*-
import os
import sys
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# フォント登録 (Meiryo / Meiryo-Bold)
FONT_REGULAR = 'Meiryo'
FONT_BOLD = 'Meiryo-Bold'
pdfmetrics.registerFont(TTFont(FONT_REGULAR, 'C:/Windows/Fonts/meiryo.ttc'))
pdfmetrics.registerFont(TTFont(FONT_BOLD, 'C:/Windows/Fonts/meiryob.ttc'))

OUTPUT_PDF = r'D:\Users\kazu\OneDrive\日本スりデーマーチ\ベルク50km補給計画_2026年版.pdf'
BACKUP_PDF = r'D:\Users\kazu\OneDrive\日本スりデーマーチ\ベルク50km補給計画_2026年版_73歳完走版.pdf'

def build_pdf():
    doc = SimpleDocTemplate(
        OUTPUT_PDF,
        pagesize=A4,
        leftMargin=26,
        rightMargin=26,
        topMargin=22,
        bottomMargin=22
    )

    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=13,
        leading=17,
        textColor=colors.HexColor('#1B365D'),
        alignment=1
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor('#D9381E'),
        alignment=1
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#FFFFFF')
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=8.8,
        leading=12,
        textColor=colors.HexColor('#1B365D')
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName=FONT_REGULAR,
        fontSize=7.6,
        leading=11,
        textColor=colors.HexColor('#222222')
    )

    cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName=FONT_REGULAR,
        fontSize=7.2,
        leading=10,
        textColor=colors.HexColor('#222222')
    )

    cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName=FONT_REGULAR,
        fontSize=7.2,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#222222')
    )

    cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=7.2,
        leading=10,
        textColor=colors.HexColor('#222222')
    )

    cell_bold_center = ParagraphStyle(
        'TableCellBoldCenter',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=7.2,
        leading=10,
        alignment=1,
        textColor=colors.HexColor('#222222')
    )

    cell_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName=FONT_BOLD,
        fontSize=7.3,
        leading=10.2,
        alignment=1,
        textColor=colors.white
    )

    story = []

    # ==========================================
    # PAGE 1: 精査分析と水分・カフェインフリー戦略
    # ==========================================
    story.append(Paragraph("第49回 日本スリーデーマーチ（2026年11月1日～3日）", subtitle_style))
    story.append(Paragraph("73歳・毎日50kmウォーク＆ラン（8分/km）安心安全・モルテン×ベルク完全補給計画【2026年改訂版】", title_style))
    story.append(Spacer(1, 5))

    profile_data = [
        [
            Paragraph("【参加者基本データ】", cell_bold),
            Paragraph("根岸 和弘 様（73歳 男性） 身長 172cm / 体重 77kg (BMI 26.0)", cell_style),
            Paragraph("目標種目", cell_bold_center),
            Paragraph("50km × 3日間連続（計150km走破）", cell_style)
        ],
        [
            Paragraph("【活動代謝・水分】", cell_bold),
            Paragraph("基礎代謝：1,490 kcal / 運動消費：3,850 kcal (総消費 5,340 kcal/日)", cell_style),
            Paragraph("1日水分目標", cell_bold_center),
            Paragraph("<b>3,000～3,500 ml</b>（走行中 2,500ml）", cell_style)
        ],
        [
            Paragraph("【想定ペース】", cell_bold),
            Paragraph("キロ8分ペース（時速7.5km/h） 想定所要時間：6時間40分", cell_style),
            Paragraph("安全管理方針", cell_bold_center),
            Paragraph("<b>完全カフェインフリー（動悸・心臓保護）</b>", cell_style)
        ]
    ]
    t_prof = Table(profile_data, colWidths=[90, 240, 75, 138])
    t_prof.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#F4F6F9')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t_prof)
    story.append(Spacer(1, 6))

    # 見出し1: 水分補給の徹底解明
    hdr1 = Table([[Paragraph("■ 水分補給の科学：モルテン500mlは「燃料」。走行中に別途2,000mlを必ず給水！", h1_style)]], colWidths=[543])
    hdr1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#2980B9')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hdr1)
    story.append(Spacer(1, 2))

    hydration_text = (
        "<b>① 500mlだけでは絶対不足！体重77kg・6時間40分の総発汗量は約2,500～3,000mlに達します:</b><br/>"
        "MAURTEN DRINK MIX 320（500mlボトル1本）は超高濃度の<b>「飲むエネルギー燃料（糖質80g/320kcal）」</b>です。<br/>"
        "これだけでは人間の生命維持に必要な水分としては全く足りません（重度の脱水・熱中症・足攣りの原因になります）。<br/>"
        "本計画では、モルテン500mlとは別に、<b>スポーツドリンク1,000ml ＋ 天然水1,000ml（計2,000ml）を走行中に別途給水</b>します。<br/>"
        "<b>走行中水分合計は「2,500ml（2.5リットル）」</b>、朝・昼・夕・就寝前を合わせた<b>1日の総水分摂取量は「3,500ml（3.5リットル）」</b>を厳格に確保します。<br/>"
        "<b>② 実践的な「ダブルボトル携行スタイル」:</b><br/>"
        "ボトル①：MAURTEN DRINK MIX 320（500ml・自前携帯用。15～20分おきに1口ずつ含む燃料）<br/>"
        "ボトル②：スポーツドリンクまたは水（500ml・基本給水用。空になったら大会給水所や自販機で補充しながら走行）"
    )
    p_hyd = Paragraph(hydration_text, body_style)
    t_hyd = Table([[p_hyd]], colWidths=[543])
    t_hyd.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF5FB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#AED6F1')),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_hyd)
    story.append(Spacer(1, 6))

    # 見出し2: 4大安全戦略
    hdr2 = Table([[Paragraph("■ 2026年改訂版：3日間連続50km完全走破のための「4大安全戦略」", h1_style)]], colWidths=[543])
    hdr2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1B365D')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hdr2)
    story.append(Spacer(1, 2))

    strategy_data = [
        [
            Paragraph("<b>① 走行中水分 2,500ml<br/>＆ 電解質ダブル補給</b>", cell_bold),
            Paragraph(
                "モルテン(500ml)＋スポドリ(1,000ml)＋水(1,000ml)＝<b>計2,500ml</b>を15～20分おきに約100～120mlずつ定時給水。"
                "1時間ごとに塩分タブレット・干し梅を摂り、低ナトリウム血症と脱水性筋痙攣を完全遮断。",
                cell_style
            )
        ],
        [
            Paragraph("<b>② 10km毎 GEL100配置<br/>（完全カフェインフリー）</b>", cell_bold),
            Paragraph(
                "手元のモルテンGEL100（カフェイン無）を<b>10km・20km・30km・40km</b>の10km間隔で均等投入（4袋/日）。"
                "動悸・心臓負担のリスクを完全根絶し、追加購入0円で最高峰の糖質エネルギーを胃腸負荷ゼロで供給。",
                cell_style
            )
        ],
        [
            Paragraph("<b>③ 胃の空虚感防止＆粘り<br/>【薄皮あんぱん＋羊羹】</b>", cell_bold),
            Paragraph(
                "液体・ジェルだけでは「胃が空っぽになる感覚」が出るため、<b>中間点（25km）でヤマザキ薄皮つぶあんぱん1個</b>（脂質わずか1g）、"
                "<b>15kmで井村屋スポーツようかん</b>を投入。咀嚼による脳の満足感と腹持ちを両立。",
                cell_style
            )
        ],
        [
            Paragraph("<b>④ ゴール後30分以内の<br/>「黄金期超回復」</b>", cell_bold),
            Paragraph(
                "ゴール後30分以内に<b>「牛乳200ml＋カステラ2切れ」</b>（糖質3：タンパク質1）を即摂取。"
                "筋破壊を止め、翌日の燃料を急速再充填。昼・夕食も揚げ物を全廃し、親子丼や豚生姜焼き定食で内臓を休めます。",
                cell_style
            )
        ]
    ]
    t_strat = Table(strategy_data, colWidths=[150, 393])
    t_strat.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FFFFFF')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('BACKGROUND', (0,0), (0,-1), colors.HexColor('#F4F6F9')),
        ('TOPPADDING', (0,0), (-1,-1), 3.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3.5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_strat)
    story.append(Spacer(1, 6))

    # 栄養・水分比較表
    hdr3 = Table([[Paragraph("■ 1日あたり走行中・総水分＆エネルギー比較（旧計画 vs 2026年安心安全版）", h2_style)]], colWidths=[543])
    story.append(hdr3)
    story.append(Spacer(1, 2))

    comp_data = [
        [
            Paragraph("項目", cell_header),
            Paragraph("旧計画（2025年版）", cell_header),
            Paragraph("2026年改訂版（推奨値）", cell_header),
            Paragraph("改善の効果と科学的根拠", cell_header)
        ],
        [
            Paragraph("走行中 給水量", cell_bold),
            Paragraph("約 1,000 ml（不足気味）", cell_center),
            Paragraph("<b>約 2,500 ml（2.5リットル）</b>", cell_bold_center),
            Paragraph("モルテン500ml＋スポドリ1L＋水1L。発汗量に見合う万全の給水設計", cell_style)
        ],
        [
            Paragraph("1日総水分摂取量", cell_bold),
            Paragraph("3.0～3.5L（曖昧な表記）", cell_center),
            Paragraph("<b>約 3,500 ml（3.5リットル）</b>", cell_bold_center),
            Paragraph("朝・走中・昼・夕・夜の全体で3.5Lを確実に管理し脱水を根絶", cell_style)
        ],
        [
            Paragraph("走行中 摂取熱量", cell_bold),
            Paragraph("約 660 kcal", cell_center),
            Paragraph("<b>約 1,200 ～ 1,250 kcal</b>", cell_bold_center),
            Paragraph("モルテン(720kcal)＋あんぱん・羊羹・ゼリーで時速185kcal確保", cell_style)
        ],
        [
            Paragraph("走行中 糖質量", cell_bold),
            Paragraph("約 160 g（1時間 24g）", cell_center),
            Paragraph("<b>約 275 ～ 290 g（1時間 42g）</b>", cell_bold_center),
            Paragraph("国際基準（30～60g/h）に完全合致。失速・ガス欠ゼロへ", cell_style)
        ],
        [
            Paragraph("カフェイン安全性", cell_bold),
            Paragraph("BARK X缶（動悸リスク）", cell_center),
            Paragraph("<b>完全ゼロ（安心安全設計）</b>", cell_bold_center),
            Paragraph("動悸・頻脈・不整脈リスクを根絶。心臓を保護し安全走破", cell_style)
        ]
    ]
    t_comp = Table(comp_data, colWidths=[80, 115, 135, 213])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('LEFTPADDING', (0,0), (-1,-1), 5),
        ('RIGHTPADDING', (0,0), (-1,-1), 5),
        ('BACKGROUND', (2,1), (2,-1), colors.HexColor('#FEF9E7')),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 8))

    # 見出し4: 天候別補給調整マトリクス
    hdr4 = Table([[Paragraph("■ 天候別（晴れ・曇り・雨）補給調整マトリクス（気温と発汗に応じた現場判断）", h2_style)]], colWidths=[543])
    story.append(hdr4)
    story.append(Spacer(1, 2))

    weather_data = [
        [
            Paragraph("天候・環境", cell_header),
            Paragraph("想定気温", cell_header),
            Paragraph("走行中給水量", cell_header),
            Paragraph("塩分・電解質", cell_header),
            Paragraph("エネルギー・胃腸・現場の対策ポイント", cell_header)
        ],
        [
            Paragraph("<b>☀️ 晴れ</b><br/>（直射日光・高温）", cell_bold_center),
            Paragraph("18～23℃<br/>体感高め", cell_center),
            Paragraph("<b>2,800～3,200 ml</b><br/>（＋300～700ml増量）", cell_bold_center),
            Paragraph("<b>6～8 粒</b><br/>（1時間1粒必須）", cell_center),
            Paragraph("発汗激増。スポドリ比率を高め脱水・熱中症・足攣りを防止。暑さで食欲低下時はジェル中心に移行。", cell_style)
        ],
        [
            Paragraph("<b>☁️ 曇り</b><br/>（基準・走りやすい）", cell_bold_center),
            Paragraph("14～18℃<br/>適温", cell_center),
            Paragraph("<b>約 2,500 ml</b><br/>（計画通り）", cell_bold_center),
            Paragraph("<b>4～5 粒</b><br/>（計画通り）", cell_center),
            Paragraph("最も走りやすい天候。15～20分おきに100mlの定時給水を守り、タイムテーブルを忠実に実行。", cell_style)
        ],
        [
            Paragraph("<b>🌧️ 雨</b><br/>（低温・雨風・冷え）", cell_bold_center),
            Paragraph("8～13℃<br/>体感極寒", cell_center),
            Paragraph("<b>1,800～2,000 ml</b><br/>（やや控えめ）", cell_bold_center),
            Paragraph("<b>3～4 粒</b><br/>（摂りすぎ注意）", cell_center),
            Paragraph("<b>【重要】寒さで体温維持のため糖質消費が激増！</b> 糖質（ジェル・羊羹）は絶対に減らさず必食。常温水を飲む。", cell_style)
        ]
    ]
    t_weather = Table(weather_data, colWidths=[85, 55, 105, 80, 218])
    t_weather.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (0,1), colors.HexColor('#FFF7ED')), # 晴
        ('BACKGROUND', (0,2), (0,2), colors.HexColor('#F8FAFC')), # 曇
        ('BACKGROUND', (0,3), (0,3), colors.HexColor('#F0FDF4')), # 雨
    ]))
    story.append(t_weather)

    # ==========================================
    # PAGE 2: 実践補給タイムテーブル (8分/km)
    # ==========================================
    story.append(PageBreak())

    story.append(Paragraph("【実践編】50kmウォーク＆ラン 補給タイムテーブル（8分/kmペース）", title_style))
    story.append(Paragraph("6:00スタート → 12:40ゴール（所要6時間40分）｜走行中水分2,500ml・熱量1,240kcal完全連動", subtitle_style))
    story.append(Spacer(1, 5))

    sched_headers = [
        Paragraph("時間", cell_header),
        Paragraph("区間/距離", cell_header),
        Paragraph("補給品目（モルテン＋ベルク）", cell_header),
        Paragraph("給水量・摂取目安", cell_header),
        Paragraph("熱量/糖質", cell_header),
        Paragraph("補給の目的・科学的ポイント", cell_header)
    ]

    sched_rows = [
        sched_headers,
        # スタート前
        [
            Paragraph("03:00", cell_bold_center),
            Paragraph("前3時間", cell_center),
            Paragraph("<b>朝食：白米180g ＋ チキンカレー</b><br/>＋<b>ホット野菜ジュース 200ml</b>", cell_style),
            Paragraph("白米180g＋ルー1人前<br/><b>温野菜ジュース 200ml</b>", cell_style),
            Paragraph("約 550 kcal<br/>糖質 95g", cell_center),
            Paragraph("温野菜ジュースで胃腸を温め、カリウム（足攣り予防）と糖質を優しく補給。3時間で完全消化。", cell_style)
        ],
        [
            Paragraph("04:30", cell_bold_center),
            Paragraph("前90分", cell_center),
            Paragraph("バナナ1本 ＋ ミネラル水", cell_style),
            Paragraph("バナナ1本<br/><b>水 200ml</b>", cell_style),
            Paragraph("約 100 kcal<br/>糖質 25g", cell_center),
            Paragraph("吸収の速い果糖・ブドウ糖＋カリウム（足攣り予防）のプレチャージ。", cell_style)
        ],
        [
            Paragraph("05:30", cell_bold_center),
            Paragraph("前30分", cell_center),
            Paragraph("<b>くらしにベルク インチャージゼリー</b><br/>（エネルギー マスカット味）", cell_style),
            Paragraph("ゼリー1パック(180g)<br/>（水分約150ml含む）", cell_style),
            Paragraph("約 180 kcal<br/>糖質 45g", cell_center),
            Paragraph("胃に固形物を残さず血糖値を安定化。スタート直後の筋分解を即座にブロック。", cell_style)
        ],
        # 走行中
        [
            Paragraph("<b>06:00</b>", cell_bold_center),
            Paragraph("<b>0 km</b>", cell_bold_center),
            Paragraph("<b>【スタート】東松山中央会場 出発</b>", cell_bold),
            Paragraph("ペース：8分/km<br/><b>給水体制スタート</b>", cell_style),
            Paragraph("―", cell_center),
            Paragraph("キロ8分巡航へ。<b>DRINK MIX 320（燃料）＋ スポドリ/水（基本給水）</b>の定期摂取開始。", cell_style)
        ],
        [
            Paragraph("06:40", cell_bold_center),
            Paragraph("約 5 km", cell_center),
            Paragraph("DRINK MIX 320 ＋ スポドリ<br/>＋ 塩分タブレット 1粒", cell_style),
            Paragraph("モルテン 100ml<br/>スポドリ 100ml<br/><b>（計200ml）</b>", cell_style),
            Paragraph("約 67 kcal<br/>糖質 16g", cell_center),
            Paragraph("喉の渇きに関係なく定時給水。発汗初期の電解質流出を先手でカバー。", cell_style)
        ],
        [
            Paragraph("07:20", cell_bold_center),
            Paragraph("<b>約 10 km</b>", cell_bold_center),
            Paragraph("<b>★ MAURTEN GEL 100【第1弾】</b><br/>＋ DRINK MIX 320 ＋ 天然水", cell_style),
            Paragraph("GEL 1袋(40g)<br/>モルテン 50ml / 水 150ml<br/><b>（計200ml）</b>", cell_style),
            Paragraph("<b>約 132 kcal<br/>糖質 33g</b>", cell_center),
            Paragraph("<b>【10km地点】</b> 噛まずにつるんと吸収。体内グリコーゲンの温存をスタート。", cell_style)
        ],
        [
            Paragraph("08:00", cell_bold_center),
            Paragraph("約 15 km", cell_center),
            Paragraph("<b>井村屋 スポーツようかん</b><br/>＋ DRINK MIX 320 ＋ スポドリ", cell_style),
            Paragraph("羊羹1本(40g)<br/>モルテン 100ml / スポ 150ml<br/><b>（計250ml）</b>", cell_style),
            Paragraph("約 177 kcal<br/>糖質 44g", cell_center),
            Paragraph("持続性糖質パラチノース＋塩分補給。固形の食感で脳の満足感を刺激。", cell_style)
        ],
        [
            Paragraph("08:40", cell_bold_center),
            Paragraph("<b>約 20 km</b>", cell_bold_center),
            Paragraph("<b>★ MAURTEN GEL 100【第2弾】</b><br/>＋ DRINK MIX 320 ＋ 天然水 ＋ 塩タブ", cell_style),
            Paragraph("GEL 1袋(40g)<br/>モルテン 100ml / 水 150ml<br/><b>（計250ml）</b>", cell_style),
            Paragraph("<b>約 164 kcal<br/>糖質 41g</b>", cell_center),
            Paragraph("<b>【20km地点】</b> 前半戦の疲労蓄積を遮断。糖質血中濃度を高水準キープ。", cell_style)
        ],
        [
            Paragraph("09:20", cell_bold_center),
            Paragraph("<b>約 25 km<br/>（中間点）</b>", cell_bold_center),
            Paragraph("<b>ヤマザキ 薄皮つぶあんぱん 1個</b><br/>＋ DRINK MIX 320 ＋ スポドリ", cell_style),
            Paragraph("あんぱん1個<br/>モルテン 150ml(完飲)<br/>スポドリ 150ml <b>(計300ml)</b>", cell_style),
            Paragraph("約 231 kcal<br/>糖質 50g", cell_center),
            Paragraph("<b>【中間点ケア】</b> 脂質1g！あんぱんで空腹防止。モルテン500mlをここで完飲！", cell_style)
        ],
        [
            Paragraph("10:00", cell_bold_center),
            Paragraph("<b>約 30 km</b>", cell_bold_center),
            Paragraph("<b>★ MAURTEN GEL 100【第3弾】</b><br/>＋ 天然水 ＋ スポドリ ＋ 干し梅 1粒", cell_style),
            Paragraph("GEL 1袋(40g)<br/>水 150ml / スポ 150ml<br/><b>（計300ml）</b>", cell_style),
            Paragraph("<b>約 120 kcal<br/>糖質 30g</b>", cell_center),
            Paragraph("<b>【魔の30kmの壁を突破】</b> 後半はエイド水・スポドリへ移行。干し梅のクエン酸で疲労回復。", cell_style)
        ],
        [
            Paragraph("10:45", cell_bold_center),
            Paragraph("約 35 km", cell_center),
            Paragraph("<b>カステラ 1切れ</b>（または一口羊羹）<br/>＋ スポドリ ＋ 天然水 ＋ 塩飴 1粒", cell_style),
            Paragraph("カステラ1切<br/>スポ 200ml / 水 100ml<br/><b>（計300ml）</b>", cell_style),
            Paragraph("約 145 kcal<br/>糖質 32g", cell_center),
            Paragraph("終盤の粘り。低脂質で超速吸収のカステラで燃料補給。発汗に応じしっかり給水。", cell_style)
        ],
        [
            Paragraph("11:20", cell_bold_center),
            Paragraph("<b>約 40 km<br/>（勝負所）</b>", cell_bold_center),
            Paragraph("<b>★ MAURTEN GEL 100【第4弾】</b><br/>＋ スポドリ ＋ 天然水", cell_style),
            Paragraph("GEL 1袋(40g)<br/>スポ 150ml / 水 150ml<br/><b>（計300ml）</b>", cell_style),
            Paragraph("<b>約 120 kcal<br/>糖質 30g</b>", cell_center),
            Paragraph("<b>【ラスト10km直前投入】</b> 動悸の心配ゼロ！純粋なハイドロゲル燃料でゴールまで失速完全ゼロ！", cell_style)
        ],
        [
            Paragraph("12:05", cell_bold_center),
            Paragraph("約 46 km", cell_center),
            Paragraph("天然水 または スポドリ 一口", cell_style),
            Paragraph("水またはスポドリ<br/><b>200ml</b>", cell_style),
            Paragraph("約 20 kcal", cell_center),
            Paragraph("ラスト4km。口を潤し脱水を防ぎつつ、ゴールへのラストスパート。", cell_style)
        ],
        [
            Paragraph("<b>12:40</b>", cell_bold_center),
            Paragraph("<b>50 km</b>", cell_bold_center),
            Paragraph("<b>【ゴール】中央会場 到着！</b>", cell_bold),
            Paragraph("所要時間：6時間40分", cell_style),
            Paragraph("―", cell_center),
            Paragraph("<b>走行中：水分計2,500ml / 熱量約1,240kcal 摂取完遂！脱水・動悸・ガス欠ゼロでゴール！</b>", cell_style)
        ],
        # ゴール後・リカバリー
        [
            Paragraph("12:55", cell_bold_center),
            Paragraph("ゴール後<br/>30分以内", cell_center),
            Paragraph("<b>【超重要】黄金期回復セット</b><br/>牛乳200ml ＋ カステラ 2切れ ＋ 水200ml", cell_style),
            Paragraph("牛乳 200ml<br/>水 200ml <b>(計400ml)</b>", cell_style),
            Paragraph("約 330 kcal<br/>糖質 50g / 蛋白 9g", cell_center),
            Paragraph("<b>筋破壊抑制＆グリコーゲン急速再合成！</b> 3連戦を可能にする最重要儀式。明日への回復。", cell_style)
        ],
        [
            Paragraph("13:30", cell_bold_center),
            Paragraph("昼食<br/>（回復）", cell_center),
            Paragraph("<b>ベルク 親子丼</b><br/>（または肉うどん＋おにぎり）＋ 味噌汁", cell_style),
            Paragraph("1人前<br/><b>温かい麦茶 300ml</b>", cell_style),
            Paragraph("約 650 kcal<br/>糖質 100g / 蛋白 25g", cell_center),
            Paragraph("揚げ物を排除。卵と鶏肉の消化の良いタンパク質と出汁で温め、胃腸を労わる。", cell_style)
        ],
        [
            Paragraph("18:00", cell_bold_center),
            Paragraph("夕食<br/>（充填）", cell_center),
            Paragraph("<b>豚生姜焼き定食風</b>（大盛りご飯＋豚肉<br/>＋具沢山豚汁＋冷奴＋カット野菜）", cell_style),
            Paragraph("ご飯大盛り(250g)<br/>豚汁・<b>お茶 300ml</b>", cell_style),
            Paragraph("約 850 kcal<br/>糖質 120g / 蛋白 30g", cell_center),
            Paragraph("豚肉のビタミンB1で糖代謝促進。ご飯を大盛りにし、明朝の筋肉へグリコーゲンを再充填。", cell_style)
        ],
        [
            Paragraph("21:00", cell_bold_center),
            Paragraph("就寝前", cell_center),
            Paragraph("ホットミルク または ヨーグルト＋バナナ", cell_style),
            Paragraph("<b>ホットミルク 200ml</b>", cell_style),
            Paragraph("約 150 kcal", cell_center),
            Paragraph("睡眠中の筋修復タンパク質と快眠アミノ酸の補給。ストレッチ後就寝。", cell_style)
        ]
    ]

    t_sched = Table(sched_rows, colWidths=[38, 52, 142, 90, 65, 156])
    t_sched.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#1B365D')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#1B365D')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 1.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.6),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
        # 背景ハイライト
        ('BACKGROUND', (0,1), (-1,3), colors.HexColor('#F4F6F9')), # 朝
        ('BACKGROUND', (0,4), (-1,4), colors.HexColor('#E8F8F5')), # スタート
        ('BACKGROUND', (0,6), (-1,6), colors.HexColor('#E8F8F5')), # 10km GEL1
        ('BACKGROUND', (0,8), (-1,8), colors.HexColor('#E8F8F5')), # 20km GEL2
        ('BACKGROUND', (0,10), (-1,10), colors.HexColor('#E8F8F5')), # 30km GEL3
        ('BACKGROUND', (0,12), (-1,12), colors.HexColor('#E8F8F5')), # 40km GEL4
        ('BACKGROUND', (0,14), (-1,14), colors.HexColor('#E8F8F5')), # ゴール
        ('BACKGROUND', (0,15), (-1,15), colors.HexColor('#FEF9E7')), # 黄金期回復
        ('BACKGROUND', (0,16), (-1,18), colors.HexColor('#F4F6F9')), # 昼夕夜
    ]))
    story.append(t_sched)

    # ==========================================
    # PAGE 3: 完全手持ち品＆ベルク調達リスト
    # ==========================================
    story.append(PageBreak())

    story.append(Paragraph("【調達・管理編】3日間完全準備リスト ＆ 連戦水分・体調管理ガイド", title_style))
    story.append(Paragraph("手元モルテン ＋ ベルク調達品｜走行中2,500ml・1日3,500mlの完全水分管理仕様", subtitle_style))
    story.append(Spacer(1, 5))

    hdr_shop = Table([[Paragraph("■ 3日間まとめ準備リスト（手元モルテン ＆ ベルク前日購入チェックシート）", h1_style)]], colWidths=[543])
    hdr_shop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#27AE60')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hdr_shop)
    story.append(Spacer(1, 2))

    shop_headers = [
        Paragraph("区分", cell_header),
        Paragraph("商品名・品目", cell_header),
        Paragraph("3日間総量", cell_header),
        Paragraph("1日分使用目安", cell_header),
        Paragraph("主な役割・摂取＆給水携帯のポイント", cell_header)
    ]

    shop_rows = [
        shop_headers,
        [
            Paragraph("<b>モルテン<br/>（手元品）</b>", cell_bold_center),
            Paragraph("<b>MAURTEN DRINK MIX 320</b><br/>（高濃度ハイドロゲルドリンク粉末 80g）", cell_bold),
            Paragraph("<b>3 袋</b><br/>（全量使用）", cell_bold_center),
            Paragraph("1袋/日<br/>（500ml水に溶解）", cell_center),
            Paragraph("<b>【燃料専用ボトル】</b>毎朝軟水500mlに溶かす。6:00～9:20（25km）にかけて15～20分おきに含む。糖質80g/320kcal供給。", cell_style)
        ],
        [
            Paragraph("<b>モルテン<br/>（手元品）</b>", cell_bold_center),
            Paragraph("<b>MAURTEN GEL 100</b><br/>（エナジージェル 40g・カフェイン無）", cell_bold),
            Paragraph("<b>12 袋</b><br/>（1箱全量使用）", cell_bold_center),
            Paragraph("<b>4袋/日</b><br/>（10, 20, 30, 40km）", cell_bold_center),
            Paragraph("<b>【主燃料・追加購入ゼロ！】</b> 10km毎にポケットから取り出し補給。動悸リスク皆無。胃を素通りして腸で即時吸収。計400kcal補給。", cell_style)
        ],
        [
            Paragraph("<b>基本給水<br/>（ベルク）</b>", cell_bold_center),
            Paragraph("<b>ポカリスエット 500ml ＆ ベルク天然水</b><br/>※モルテン溶解用は必ず軟水を選ぶ", cell_bold),
            Paragraph("スポドリ 6本<br/>水 6本<br/><b>（計12本）</b>", cell_bold_center),
            Paragraph("スポドリ 1L/日<br/>水 1L/日<br/><b>（計2,000ml）</b>", cell_bold_center),
            Paragraph("<b>【必須！走行中基本給水】</b> モルテン500mlとは別に走行中に2L給水！ダブルボトル携行＋大会エイド・自販機で補充して飲み切る。", cell_style)
        ],
        [
            Paragraph("ベルク PB<br/>ゼリー", cell_bold_center),
            Paragraph("<b>くらしにベルク インチャージゼリー</b><br/>（エネルギー マスカット味 180kcal）", cell_style),
            Paragraph("<b>3 本</b>", cell_bold_center),
            Paragraph("1本/日<br/>（スタート前30分）", cell_center),
            Paragraph("毎朝5:30に摂取。朝食後の血糖値を整え、スタート直後の燃料を確保するベルクPB名品。", cell_style)
        ],
        [
            Paragraph("主補給パン<br/>（ベルク）", cell_bold_center),
            Paragraph("<b>ヤマザキ 薄皮つぶあんぱん</b>（4個入）", cell_style),
            Paragraph("<b>1 袋</b>（計4個）", cell_bold_center),
            Paragraph("1個/日<br/>（25km中間点）", cell_center),
            Paragraph("脂質わずか1g！モルテンに加える唯一の固形パン。中間点での胃の空虚感を防ぎ満足感を与える。", cell_style)
        ],
        [
            Paragraph("主補給和菓子<br/>（ベルク）", cell_bold_center),
            Paragraph("<b>井村屋 スポーツようかん</b><br/>（または ベルクひとくち羊羹）", cell_style),
            Paragraph("<b>3～6 本</b>", cell_bold_center),
            Paragraph("1～2本/日<br/>（15km等）", cell_center),
            Paragraph("片手で押し出し食べられる高密度糖質＋塩分。小豆の持続性糖質で血糖値を安定維持。", cell_style)
        ],
        [
            Paragraph("塩分・電解質<br/>（ベルク）", cell_bold_center),
            Paragraph("<b>塩分チャージタブレッツ ＆ 無種 干し梅</b>", cell_style),
            Paragraph("各 1 袋", cell_bold_center),
            Paragraph("タブレット3粒<br/>干し梅1粒/日", cell_center),
            Paragraph("大量発汗に対応。1時間に1粒目安で水・スポドリと共に補給し、低ナトリウム血症を防止。", cell_style)
        ],
        [
            Paragraph("回復食<br/>（ベルク）", cell_bold_center),
            Paragraph("<b>牛乳 200mlパック ＆ カステラ切り落とし</b>", cell_style),
            Paragraph("牛乳 3本<br/>カステラ 1パック", cell_bold_center),
            Paragraph("牛乳1本<br/>カステラ2切/日", cell_center),
            Paragraph("<b>【ゴール後30分以内】</b>超回復スイッチ。低脂質高糖質（カステラ）＋良質乳タンパク質で翌日へ備える。", cell_style)
        ],
        [
            Paragraph("果物・朝食<br/>（ベルク）", cell_bold_center),
            Paragraph("<b>バナナ ＆ カレー ＆ 野菜ジュース</b><br/>（野菜生活や充実野菜など900mlボトル）", cell_style),
            Paragraph("バナナ 6本<br/>カレー 3食<br/>ジュース 1本", cell_bold_center),
            Paragraph("バナナ 2本/日<br/>カレー 1食/日<br/>ジュース200ml", cell_center),
            Paragraph("毎朝3:00に温めてホット野菜ジュース200mlとして飲む。胃腸を温め、カリウム（攣り防止）・糖質補給。", cell_style)
        ],
        [
            Paragraph("昼・夕食惣菜<br/>（ベルク）", cell_bold_center),
            Paragraph("<b>親子丼、豚生姜焼き弁当、肉うどん等</b><br/>※揚げ物（唐揚げ・フライ）は絶対NG！", cell_style),
            Paragraph("各日購入", cell_bold_center),
            Paragraph("昼 1食<br/>夕 1食", cell_center),
            Paragraph("内臓疲労を考慮し、煮物・焼き物・うどんを選択。ご飯は大盛りで炭水化物を確保。", cell_style)
        ],
        [
            Paragraph("【推奨携行薬】", cell_bold_center),
            Paragraph("<b>ツムラ68番 芍薬甘草湯</b>（ドラッグストア等）", cell_style),
            Paragraph("<b>3～6 包</b>", cell_bold_center),
            Paragraph("頓服（攣り時）", cell_center),
            Paragraph("ふくらはぎや太ももがピクついた時にすぐ飲む。足攣り・こむら返りへの特効薬。", cell_style)
        ]
    ]

    t_shop = Table(shop_rows, colWidths=[62, 148, 68, 64, 201])
    t_shop.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#27AE60')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#27AE60')),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor('#D0D7DE')),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BACKGROUND', (0,1), (-1,2), colors.HexColor('#E8F8F5')), # モルテン行ハイライト
        ('BACKGROUND', (0,3), (-1,3), colors.HexColor('#FEF9E7')), # 給水行ハイライト
        ('BACKGROUND', (0,11), (-1,11), colors.HexColor('#FDEDEC')), # 薬行
    ]))
    story.append(t_shop)
    story.append(Spacer(1, 5))

    # 水分管理とモルテンの鉄則
    hdr_m_rule = Table([[Paragraph("■ 失敗しない「ダブルボトル給水法」＆ モルテン溶解ルール", h2_style)]], colWidths=[543])
    story.append(hdr_m_rule)
    story.append(Spacer(1, 2))

    rule_text = (
        "<b>1. 「燃料ボトル」と「水分ボトル」を明確に分ける（ダブルボトル体制）:</b><br/>"
        "・ボトル①（燃料）：MAURTEN DRINK MIX 320（500ml・軟水で前夜溶解）。15～20分おきに1口ずつ含む「飲むエネルギー」。25kmまでに完飲。<br/>"
        "・ボトル②（水分）：水またはスポーツドリンク（500ml）。喉の渇きを潤す基本給水用。空になったら大会給水所や自販機で補充しながら走行。<br/>"
        "<b>2. 走行中に「合計2,500ml（2.5リットル）」を飲み切る目安:</b><br/>"
        "1時間（約7.5km）あたり約350～400mlのペースで給水します。5kmごとの目安で約200～250mlをこまめに飲むことで、胃に負担をかけずに脱水を完全防止します。<br/>"
        "<b>3. DRINK MIX 320は必ず「軟水500ml」で溶かす:</b><br/>"
        "モルテンは硬度40mg/L未満の軟水（ベルクの日本の一般的な天然水）で溶かしてください。硬水で溶かすとゲルが固まりすぎます。"
    )
    p_rule = Paragraph(rule_text, body_style)
    t_rule = Table([[p_rule]], colWidths=[543])
    t_rule.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#FEF9E7')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#F5B041')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_rule)
    story.append(Spacer(1, 5))

    # コンディショニング極意
    hdr_adv = Table([[Paragraph("■ 73歳・3日間合計150km完全走破のための「コンディショニング極意」", h1_style)]], colWidths=[543])
    hdr_adv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#1B365D')),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(hdr_adv)
    story.append(Spacer(1, 2))

    advice_text = (
        "<b>① 1日の総水分3,500ml管理:</b> 朝(500ml)＋走中(2,500ml)＋午後・夜(500ml)＝計3,500ml。脱水による血液ドロドロと足攣りを根絶。<br/>"
        "<b>② 脂質制限の徹底:</b> 食事で揚げ物（唐揚げ・カツ）を摂ると胃腸がストップします。食事は親子丼、うどん、豚生姜焼きを徹底。<br/>"
        "<b>③ 入浴時の温冷交代浴＆脚上げ就寝:</b> ゴール後はぬるめの湯舟と冷水シャワーで交代浴を行い、就寝時は足を10cm高くして眠りましょう。"
    )
    p_adv = Paragraph(advice_text, body_style)
    t_adv = Table([[p_adv]], colWidths=[543])
    t_adv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#EBF3FB')),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#AED6F1')),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_adv)

    doc.build(story)
    shutil.copyfile(OUTPUT_PDF, BACKUP_PDF)
    print(f"PDF successfully generated: {OUTPUT_PDF}")

if __name__ == '__main__':
    build_pdf()
