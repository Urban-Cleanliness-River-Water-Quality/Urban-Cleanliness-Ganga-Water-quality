"""
Script: generate_ppt.py
Course: Data Analytics and Visualization
Description: Generates an executive, 10-slide PowerPoint presentation (.pptx)
             covering Urban Cleanliness (Swachh Survekshan) & River Ganga Water Quality.
"""

import os
import sys
import subprocess

# Ensure python-pptx is installed in your environment
try:
    import pptx
except ImportError:
    print("[Info] Installing python-pptx...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "python-pptx"])
    import pptx

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE


def create_presentation(output_filename="Project_Presentation_Data_Analytics_and_Visualization.pptx"):
    prs = Presentation()
    # 16:9 Widescreen standard
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # Professional Theme Palette
    NAVY = RGBColor(26, 54, 93)       # #1A365D Primary accent
    DARK_BLUE = RGBColor(15, 32, 67)  # #0F2043 Header / Dark slide
    SLATE = RGBColor(74, 85, 104)     # #4A5568 Secondary accent
    TEXT_DARK = RGBColor(30, 41, 59)  # #1E293B Body text
    MUTED = RGBColor(100, 116, 139)   # #64748B Secondary text
    WHITE = RGBColor(255, 255, 255)
    LIGHT_BG = RGBColor(248, 250, 252)# #F8FAFC
    CARD_BG = RGBColor(241, 245, 249) # #F1F5F9
    BORDER_COLOR = RGBColor(226, 232, 240)
    CORAL = RGBColor(225, 29, 72)     # Alert / Highlight #E11D48
    TEAL = RGBColor(13, 148, 136)     # Positive #0D9488
    AMBER = RGBColor(217, 119, 6)     # Accent #D97706

    def set_slide_background(slide, color):
        bg_shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Inches(13.333), Inches(7.5))
        bg_shape.fill.solid()
        bg_shape.fill.fore_color.rgb = color
        bg_shape.line.fill.background()
        return bg_shape

    def add_header(slide, title_text, kicker="DATA ANALYTICS & VISUALIZATION"):
        # Kicker / Eyebrow
        tx_k = slide.shapes.add_textbox(Inches(0.8), Inches(0.45), Inches(11.7), Inches(0.35))
        tf_k = tx_k.text_frame
        tf_k.word_wrap = True
        p_k = tf_k.paragraphs[0]
        p_k.text = kicker.upper()
        p_k.font.name = "Calibri"
        p_k.font.size = Pt(11)
        p_k.font.bold = True
        p_k.font.color.rgb = TEAL

        # Main Title
        tx_t = slide.shapes.add_textbox(Inches(0.8), Inches(0.8), Inches(11.7), Inches(0.7))
        tf_t = tx_t.text_frame
        tf_t.word_wrap = True
        p_t = tf_t.paragraphs[0]
        p_t.text = title_text
        p_t.font.name = "Calibri"
        p_t.font.size = Pt(26)
        p_t.font.bold = True
        p_t.font.color.rgb = NAVY

    def add_card(slide, left, top, width, height, title, body_bullets, card_bg=CARD_BG, title_color=NAVY):
        card = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        card.fill.solid()
        card.fill.fore_color.rgb = card_bg
        card.line.color.rgb = BORDER_COLOR
        card.line.width = Pt(1)

        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.22)
        tf.margin_right = Inches(0.22)
        tf.margin_top = Inches(0.22)
        tf.margin_bottom = Inches(0.18)

        p0 = tf.paragraphs[0]
        p0.text = title
        p0.font.name = "Calibri"
        p0.font.size = Pt(14)
        p0.font.bold = True
        p0.font.color.rgb = title_color
        p0.space_after = Pt(8)

        for item in body_bullets:
            p = tf.add_paragraph()
            p.text = item
            p.font.name = "Calibri"
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_DARK
            p.space_after = Pt(4)
        return card

    def add_stat_box(slide, left, top, width, height, number_str, label_str, note_str="", accent_color=NAVY):
        box = slide.shapes.add_shape(
            MSO_SHAPE.ROUNDED_RECTANGLE,
            Inches(left), Inches(top), Inches(width), Inches(height)
        )
        box.fill.solid()
        box.fill.fore_color.rgb = WHITE
        box.line.color.rgb = BORDER_COLOR
        box.line.width = Pt(1)

        tf = box.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE

        p0 = tf.paragraphs[0]
        p0.text = number_str
        p0.font.name = "Calibri"
        p0.font.size = Pt(36)
        p0.font.bold = True
        p0.font.color.rgb = accent_color
        p0.alignment = PP_ALIGN.CENTER

        p1 = tf.add_paragraph()
        p1.text = label_str
        p1.font.name = "Calibri"
        p1.font.size = Pt(12)
        p1.font.bold = True
        p1.font.color.rgb = TEXT_DARK
        p1.alignment = PP_ALIGN.CENTER

        if note_str:
            p2 = tf.add_paragraph()
            p2.text = note_str
            p2.font.name = "Calibri"
            p2.font.size = Pt(9.5)
            p2.font.color.rgb = MUTED
            p2.alignment = PP_ALIGN.CENTER

    # ==================== SLIDE 1: TITLE SLIDE ====================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1, DARK_BLUE)

    tbox1 = s1.shapes.add_textbox(Inches(1.2), Inches(1.8), Inches(11.0), Inches(4.0))
    tf1 = tbox1.text_frame
    tf1.word_wrap = True

    p_k1 = tf1.paragraphs[0]
    p_k1.text = "DATA ANALYTICS & VISUALIZATION  |  COURSE PROJECT"
    p_k1.font.name = "Calibri"
    p_k1.font.size = Pt(13)
    p_k1.font.bold = True
    p_k1.font.color.rgb = TEAL
    p_k1.space_after = Pt(14)

    p_t1 = tf1.add_paragraph()
    p_t1.text = "Urban Cleanliness & River Ganga\nWater Quality Analytics"
    p_t1.font.name = "Calibri"
    p_t1.font.size = Pt(38)
    p_t1.font.bold = True
    p_t1.font.color.rgb = WHITE
    p_t1.space_after = Pt(18)

    p_sub1 = tf1.add_paragraph()
    p_sub1.text = "Benchmarking 135 Swachh Survekshan ULBs & 66 CPCB monitoring stations to expose the policy gap between municipal sanitation and river pollution."
    p_sub1.font.name = "Calibri"
    p_sub1.font.size = Pt(15)
    p_sub1.font.color.rgb = RGBColor(203, 213, 225)
    p_sub1.space_after = Pt(28)

    p_meta1 = tf1.add_paragraph()
    p_meta1.text = "Author: Aman Kumar Ray  |  B.Tech CSE, SR University, Warangal"
    p_meta1.font.name = "Calibri"
    p_meta1.font.size = Pt(12)
    p_meta1.font.bold = True
    p_meta1.font.color.rgb = AMBER

    # ==================== SLIDE 2: EXECUTIVE OVERVIEW ====================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2, LIGHT_BG)
    add_header(s2, "Executive Overview: Project Scale & Scope")

    add_stat_box(s2, 0.8, 1.8, 2.7, 1.7, "135", "CITIES BENCHMARKED", "40 Metros (>3M) + 95 Mid-Sized (3L-1M)", NAVY)
    add_stat_box(s2, 3.8, 1.8, 2.7, 1.7, "66", "RIVER STATIONS AUDITED", "CPCB stations across 4 riparian states", TEAL)
    add_stat_box(s2, 6.8, 1.8, 2.7, 1.7, "40.9%", "BOD VIOLATION RATE", "27 stations exceed safe limit (>3 mg/L)", CORAL)
    add_stat_box(s2, 9.8, 1.8, 2.7, 1.7, "8.32", "PEAK BOD (mg/L)", "Recorded at Kanpur Downstream", CORAL)

    add_card(s2, 0.8, 3.8, 5.7, 3.1, "Project Vision & Objectives", [
        "• Single Unified Scale: Merged disjointed MoHUA population cohorts into a single 1-to-135 national ranking.",
        "• Diagnostic Focus: Shifted spotlight from celebrating top-tier cities to diagnosing chronically lagging ULBs.",
        "• Environmental Linkage: Traced how high-scoring urban centers directly impact downstream river health.",
        "• Complete Submissions: Reproducible Python scripts + Power BI dashboard + comprehensive project report."
    ], WHITE)

    add_card(s2, 6.8, 3.8, 5.7, 3.1, "Primary Data Authorities", [
        "• MoHUA: Swachh Survekshan 2024 records (Total score: 12,500; SS2024: 10,000; ODF: 1,200).",
        "• CPCB: River Ganga Water Quality Monitoring Program across Uttarakhand, UP, Bihar, and West Bengal.",
        "• Rigorous Cleaning: Handled encoding issues (micro-siemens symbol) and stripped administrative noise."
    ], WHITE)

    # ==================== SLIDE 3: 8 PROBLEMS ADDRESSED ====================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3, LIGHT_BG)
    add_header(s3, "8 Core Problems Addressed by This Project")

    col_w = 2.8
    cards_p = [
        ("1. Cohort Fragmentation", "Merged disjointed >3M and 3L-1M datasets into a unified 1-to-135 national ranking."),
        ("2. Obscured Low Performers", "Diagnosed bottom-tier sanitation failure points (Madurai, Ludhiana, Erode, Mathura)."),
        ("3. High-Dimensional Noise", "Cleaned raw CPCB files, resolving encoding crashes and pruning 20+ empty parameters."),
        ("4. Riparian Blindspots", "Mapped longitudinal water quality from upper Himalayas down through West Bengal delta."),
        ("5. Unflagged BOD Hazards", "Flagged 27 stations violating 3.0 mg/L limit, peaking at Kanpur (8.32 mg/L)."),
        ("6. Aquatic Hypoxia Risks", "Assessed Dissolved Oxygen (DO) against the critical 4.0 mg/L aquatic survival threshold."),
        ("7. Urban-River Policy Gap", "Exposed contrast: top-scoring ODF cities discharging severe untreated effluent into Ganga."),
        ("8. No Unified Dashboard", "Built interactive Power BI model (Dashboard.pbix) for multi-tier civic decision-making.")
    ]

    for idx, (t, desc) in enumerate(cards_p):
        col = idx % 4
        row = idx // 4
        left = 0.8 + col * (col_w + 0.2)
        top = 1.8 + row * 2.6
        add_card(s3, left, top, col_w, 2.4, t, [desc], WHITE, NAVY)

    # ==================== SLIDE 4: DATA CLEANING ARCHITECTURE ====================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4, LIGHT_BG)
    add_header(s4, "Automated Pipeline & Cleaning Methodology")

    add_card(s4, 0.8, 1.8, 3.6, 5.0, "1. Municipal Data Cleaning", [
        "Script: clean_and_merge_cities.py",
        "",
        "• Schema Harmonization: Reconciled 'SS2025' and 'GFC' fields into 'gfc_star_rating_score'.",
        "• Entity Normalization: Stripped legal suffixes like '(M. Corp)', '(MC)', and '(M CL)' using regular expressions.",
        "• Acronym Disambiguation: Standardized bureaucratic names (e.g. 'BBMP', 'MCD', 'GVMC').",
        "• Unified Cohort Ranking: Assigned 1 to 135 national ranks based on descending total score."
    ], WHITE)

    add_card(s4, 4.8, 1.8, 3.6, 5.0, "2. River Data Cleaning", [
        "Script: clean_river_data.py",
        "",
        "• Latin-1 Encoding: Handled micro-siemens symbols (µmhos/cm) preventing parsing errors.",
        "• Parameter Extraction: Extracted mean DO, BOD, pH, temperature, and conductivity from bracketed headers.",
        "• Compliance Thresholds: Created Boolean flags:",
        "   - bod_polluted_flag: BOD > 3.0 mg/L",
        "   - do_critical_flag: DO < 4.0 mg/L",
        "• State Standardization: Corrected legacy names (e.g. Uttaranchal -> Uttarakhand)."
    ], WHITE)

    add_card(s4, 8.8, 1.8, 3.7, 5.0, "3. Analytics & Export Engine", [
        "Scripts: data_analysis.py & visualisation.py",
        "",
        "• Clean Deliverables Generated:",
        "   - combined_city_clean.csv (135 rows)",
        "   - ganga_water_quality_clean.csv (66 rows)",
        "• Automated Statistics: Calculated skewness, cohort quartiles, and state aggregates.",
        "• Multi-Panel Graphics: Rendered publication-ready 4-panel dashboard figure (project_dashboard.png).",
        "• Power BI Ready: Model pre-formatted for Dashboard.pbix."
    ], WHITE)

    # ==================== SLIDE 5: URBAN SANITATION FINDINGS ====================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5, LIGHT_BG)
    add_header(s5, "Urban Cleanliness: Cohort Disparity & Outliers")

    add_card(s5, 0.8, 1.8, 5.7, 5.0, "Cohort Performance Gap", [
        "Key Findings from 135 ULB Evaluations:",
        "",
        "• Metros (>3 Million, N=40):",
        "   - Mean Score: 9,711.12  |  Median: 10,607.00",
        "   - Top city: Ahmedabad (12,079 / 12,500)",
        "   - Higher capital access drives mechanized sweeping and solid waste processing infrastructure.",
        "",
        "• Mid-Sized Cities (3L-1M, N=95):",
        "   - Mean Score: 8,345.37  |  Median: 8,255.00",
        "   - Top city: Mira-Bhayandar (11,652 / 12,500)",
        "   - Average deficit of 1,365.75 points compared to metros.",
        "",
        "• Distribution Skew: Heavy negative skew (median > mean). Most cities score >8,000, but chronically lagging municipalities pull down national benchmarks."
    ], WHITE)

    add_card(s5, 6.8, 1.8, 5.7, 5.0, "National Extremes: Top 5 vs Bottom 5", [
        "TOP 5 PERFORMERS NATIONALLY:",
        "1. Ahmedabad (Gujarat): 12,079",
        "2. Bhopal (Madhya Pradesh): 12,067",
        "3. Lucknow (Uttar Pradesh): 12,001",
        "4. Raipur (Chhattisgarh): 11,996",
        "5. Jabalpur (Madhya Pradesh): 11,989",
        "",
        "BOTTOM 5 OUTLIERS (Action Required):",
        "131. Kollam (Kerala): 5,376",
        "132. Ludhiana (Punjab): 5,272",
        "133. Erode (Tamil Nadu): 4,911",
        "134. Madurai (Tamil Nadu): 4,823",
        "135. Mathura Cantt. (Uttar Pradesh): 3,452",
        "",
        "Diagnosis: Southern underperformers suffer from severe waste segregation bottlenecks and incomplete collection networks."
    ], WHITE)

    # ==================== SLIDE 6: GANGA WATER QUALITY ====================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6, LIGHT_BG)
    add_header(s6, "Ganga Water Quality: DO Health vs BOD Hotspots")

    add_card(s6, 0.8, 1.8, 5.7, 5.0, "Water Health Parameters (N = 66 Stations)", [
        "Core Chemical & Biological Indicators:",
        "",
        "• Dissolved Oxygen (DO):",
        "   - Station Mean: 7.83 mg/L (Baseline: >4.0 mg/L)",
        "   - Zero stations exhibited acute DO depletion (<4.0 mg/L).",
        "   - Rapid natural surface turbulence along mainstream sections maintains oxygenation despite pollution.",
        "",
        "• Biochemical Oxygen Demand (BOD):",
        "   - 27 out of 66 stations (40.9%) critically violate the safe limit of 3.0 mg/L.",
        "   - High organic waste and sewage severely reduce natural assimilative capacity in middle reaches.",
        "",
        "• Acidity & Conductivity: pH remains stable (7.88 - 7.97). Conductivity peaks in West Bengal (510.9 µmhos/cm) due to industrial and tidal runoff."
    ], WHITE)

    add_card(s6, 6.8, 1.8, 5.7, 5.0, "Most Polluted Reaches & State Comparison", [
        "CRITICAL POLLUTION HOTSPOTS (Peak BOD):",
        "1. Kanpur Downstream (Jajmau Pumping Station): 8.32 mg/L",
        "   - 2.8x higher than safe limit; heavy tannery & municipal discharge.",
        "2. Raiwala D/S (after Confl. with River Song, UK): 6.20 mg/L",
        "3. Prayagraj / Allahabad (Rasoolabad): 5.58 mg/L",
        "4. Haridwar Downstream: 5.30 mg/L",
        "5. Prayagraj (Sangam Downstream): 5.09 mg/L",
        "",
        "STATE-WISE AVERAGE BOD RANKING:",
        "• Uttar Pradesh: 3.90 mg/L (Severely Polluted)",
        "• West Bengal: 2.89 mg/L (Moderate)",
        "• Bihar: 2.74 mg/L (Moderate)",
        "• Uttarakhand: 2.51 mg/L (Within Safe Limit)"
    ], WHITE)

    # ==================== SLIDE 7: CROSS-DOMAIN SYNTHESIS ====================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7, LIGHT_BG)
    add_header(s7, "The Policy Paradox: Clean Cities, Polluted River")

    add_card(s7, 0.8, 1.8, 11.7, 2.5, "Municipal Swachh Scores vs. Downstream River Health", [
        "A direct comparison between urban Swachh Survekshan rankings and CPCB river water quality exposes an operational blindspot:",
        "• Prayagraj (National Rank 15): Total Score 11,292 | ODF 1,200/1,200  ==>  Downstream BOD: 5.09 - 5.58 mg/L (Polluted)",
        "• Kanpur (National Rank 20): Total Score 11,022 | ODF 1,200/1,200     ==>  Downstream BOD: 8.32 mg/L (Critical Outlier)",
        "• Varanasi (National Rank 24): Total Score 10,728 | ODF 1,200/1,200   ==>  Downstream BOD: 3.40 - 4.20 mg/L (Polluted)",
        "• Patna (National Rank 28): Total Score 10,584 | ODF 1,200/1,200      ==>  Downstream BOD: 2.60 - 2.90 mg/L (Moderate)"
    ], WHITE)

    add_card(s7, 0.8, 4.6, 5.7, 2.3, "The Core Diagnostic Finding", [
        "• Swachh Survekshan primarily measures terrestrial cleanliness: street sweeping, door-to-door trash collection, and public latrines.",
        "• It fails to audit Sewage Treatment Plant (STP) operational throughput or unmonitored point-source outfalls entering the Ganga.",
        "• A city can earn 'Five-Star Clean' status while discharging hundreds of millions of liters of untreated effluent daily."
    ], WHITE, CORAL)

    add_card(s7, 6.8, 4.6, 5.7, 2.3, "The Strategic Policy Shift Required", [
        "• Incorporate STP treatment volume and discharge BOD directly into municipal cleanliness ranking formulas.",
        "• Penalize Urban Local Bodies (ULBs) whose downstream river stations fail environmental safety limits.",
        "• Shift civic incentives from visual facade sweeping to closed-loop sewage infrastructure management."
    ], WHITE, TEAL)

    # ==================== SLIDE 8: DASHBOARD & POWER BI ====================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8, LIGHT_BG)
    add_header(s8, "Visual Analytics & Power BI Model (Dashboard.pbix)")

    if os.path.exists("project_dashboard.png"):
        s8.shapes.add_picture("project_dashboard.png", Inches(0.8), Inches(1.8), width=Inches(6.4))
        card_left = 7.5
        card_width = 5.0
    else:
        card_left = 0.8
        card_width = 11.7

    add_card(s8, card_left, 1.8, card_width, 5.0, "Dashboard Architecture & Visuals", [
        "Dual Visualization Engines:",
        "",
        "1. Python Multi-Panel Figure (project_dashboard.png):",
        "   • Cohort boxplot comparing >3M vs 3L-1M distributions.",
        "   • Top 10 cleanest cities horizontal bar chart.",
        "   • Riparian state BOD bar chart highlighting the 3.0 mg/L threshold.",
        "   • Bivariate scatter matrix correlating DO vs BOD across stations.",
        "",
        "2. Interactive Power BI Model (Dashboard.pbix):",
        "   • Page 1: Urban Sanitation Explorer (KPI cards, slicers for population tier and state, rank matrix).",
        "   • Page 2: River Ganga Health & Basin Hotspots (geographic station mapping, conditional color coding for BOD violations).",
        "   • Unified schema ready for real-time civic presentations."
    ], WHITE)

    # ==================== SLIDE 9: RECOMMENDATIONS ====================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9, LIGHT_BG)
    add_header(s9, "Actionable Policy Recommendations & Conclusion")

    add_card(s9, 0.8, 1.8, 3.6, 4.9, "1. Unified Governance Metric", [
        "Action: Integrate STP Efficiency",
        "",
        "• Tie 25% of municipal Swachh score directly to treated sewage quality.",
        "• Disqualify cities from top 10 national ranking if downstream river BOD exceeds 3.0 mg/L.",
        "• Align MoHUA civic incentives with CPCB environmental standards."
    ], WHITE)

    add_card(s9, 4.8, 1.8, 3.6, 4.9, "2. Targeted Support for Lagging ULBs", [
        "Action: Capital Restructuring",
        "",
        "• Reallocate infrastructure grants specifically to bottom-quartile municipalities (Madurai, Ludhiana, Erode).",
        "• Deploy decentralized biomethanation and composting units instead of capital-heavy centralized plants.",
        "• Reform waste segregation compliance in southern ULBs."
    ], WHITE)

    add_card(s9, 8.8, 1.8, 3.7, 4.9, "3. Real-Time Telemetry & Conclusion", [
        "Action: Continuous Monitoring",
        "",
        "• Install 24/7 automated IoT sensor telemetry at industrial confluences (Kanpur, Jajmau, Unnao).",
        "",
        "Summary:",
        "This project delivers an end-to-end, reproducible data analytics framework proving that genuine urban cleanliness cannot end at the riverbank."
    ], WHITE)

    # ==================== SLIDE 10: CLOSING / Q&A ====================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10, DARK_BLUE)

    tbox10 = s10.shapes.add_textbox(Inches(1.5), Inches(2.2), Inches(10.3), Inches(3.2))
    tf10 = tbox10.text_frame
    tf10.word_wrap = True

    p_c10 = tf10.paragraphs[0]
    p_c10.text = "Thank You"
    p_c10.font.name = "Calibri"
    p_c10.font.size = Pt(44)
    p_c10.font.bold = True
    p_c10.font.color.rgb = WHITE
    p_c10.alignment = PP_ALIGN.CENTER
    p_c10.space_after = Pt(14)

    p_s10 = tf10.add_paragraph()
    p_s10.text = "Comprehensive Analytics and Visual Profiling of Urban Cleanliness & River Ganga Water Quality in India"
    p_s10.font.name = "Calibri"
    p_s10.font.size = Pt(16)
    p_s10.font.color.rgb = RGBColor(203, 213, 225)
    p_s10.alignment = PP_ALIGN.CENTER
    p_s10.space_after = Pt(24)

    p_m10 = tf10.add_paragraph()
    p_m10.text = "Course: Data Analytics & Visualization  |  Student: Aman Kumar Ray  |  SR University, Warangal"
    p_m10.font.name = "Calibri"
    p_m10.font.size = Pt(13)
    p_m10.font.bold = True
    p_m10.font.color.rgb = AMBER
    p_m10.alignment = PP_ALIGN.CENTER

    prs.save(output_filename)
    print(f"[Done] Presentation successfully saved as '{output_filename}'!")


if __name__ == "__main__":
    create_presentation()