# Power BI Build Guide — Executive Dashboards

Files in this folder:

| File | Use |
|---|---|
| `viksit_bharat_theme.json` | Report theme (colours, fonts, transparent visuals) |
| `urban_cleanliness_background.png` | Canvas background, Page 1 |
| `ganga_water_quality_background.png` | Canvas background, Page 2 |
| `make_backgrounds.py` | Re-generates the backgrounds (edit titles, or blend a photo into the header) |

Every visual below has an exact **X, Y, Width, Height**. Enter them in
*Format visual → General → Properties → Size and position*. They line up with the white cards on the background.

---

## 0. One-time report setup

1. **Theme:** View → Themes → *Browse for themes* → `viksit_bharat_theme.json`.
2. **Indian number format (lakh/crore):** File → Options and settings → Options → *Current file → Regional settings* → Locale = **English (India)**.
3. **For each page:** Format page (click empty canvas) →
   - *Canvas settings*: Type **16:9**, (1280 × 720), Vertical alignment **Top**.
   - *Canvas background*: **Image** → browse the page's PNG → Image fit **Fit** → Transparency **0%**.
   - *Wallpaper*: colour `#E2E8F0`, transparency 0%.
4. Rename pages: **Urban Cleanliness** and **Ganga Water Quality**.
5. View → untick *Snap to grid* (so typed positions are not rounded).

The theme already makes every visual transparent with no border, so the white cards and shadows come from the background image.

---

## 1. Power Query preparation (Transform data)

**combined_city_clean** — no changes needed. Check `total_score`, `ss2024_score`, `gfc_star_rating_score`, `odf_score` are *Whole Number*.

**ganga_water_quality_clean** — do these in this order:
1. Select `state` → Transform → *Replace values*: `Uttaranchal` → `Uttarakhand` (current official name; matters for a national audience).
2. Add Column → *Index Column → From 1*. Rename it **River Sequence**. The file is already ordered from Gangotri (1) to Diamond Harbour (66), so this index is the river's course. Do **not** sort the table before this step.
3. Close & Apply. Then select `River Sequence` → Column tools → Summarization **Don't summarize**.

---

## 2. Dashboard 1 — Urban Cleanliness

### 2a. Calculated columns (Table tools → New column, table `combined_city_clean`)

```DAX
Performance Band =
SWITCH (
    TRUE (),
    combined_city_clean[total_score] >= 10000, "Excellent",
    combined_city_clean[total_score] >= 8000, "Good",
    combined_city_clean[total_score] >= 6000, "Average",
    "Critical"
)
```

```DAX
Band Order =
SWITCH ( combined_city_clean[Performance Band],
    "Excellent", 1, "Good", 2, "Average", 3, 4 )
```

```DAX
Certification Score =
combined_city_clean[gfc_star_rating_score] + combined_city_clean[odf_score]
```

Select `Performance Band` → Column tools → **Sort by column → Band Order**.

### 2b. Measures (Home → New measure)

```DAX
Cities Assessed = COUNTROWS ( combined_city_clean )

Avg Total Score = AVERAGE ( combined_city_clean[total_score] )

Cleanest City =
VAR TopRow = TOPN ( 1, combined_city_clean, combined_city_clean[total_score], DESC )
RETURN MAXX ( TopRow, combined_city_clean[city_clean] )

GFC Certified % =
DIVIDE (
    CALCULATE ( [Cities Assessed], combined_city_clean[gfc_star_rating_score] > 0 ),
    [Cities Assessed]
)

Critical Cities =
CALCULATE ( [Cities Assessed], combined_city_clean[Performance Band] = "Critical" ) + 0

National Average =
CALCULATE ( [Avg Total Score], REMOVEFILTERS ( combined_city_clean[state_ut] ) )

State Bar Color =
IF ( [Avg Total Score] < [National Average], "#B3261E", "#1D4E89" )
```

Formats: `Avg Total Score`, `National Average` → Whole number with thousands separator. `GFC Certified %` → Percentage, 1 decimal.

### 2c. Slicers (left filter panel)

| Slicer | Field | Style | X | Y | W | H |
|---|---|---|---|---|---|---|
| Population Category | `population_category` | Tile (buttons) | 20 | 122 | 184 | 92 |
| State / UT | `state_ut` | Dropdown, *Search* on, *Select all* on | 20 | 222 | 184 | 64 |
| Performance Band | `Performance Band` | Vertical list | 20 | 294 | 184 | 150 |
| Clear button | Insert → Buttons → **Clear all slicers** | fill `#1D4E89`, text white | 20 | 452 | 184 | 32 |

### 2d. KPI cards (Card visual, category label ON)

| # | Measure | Rename to (category label) | X | Y | W | H | Expected (all data) |
|---|---|---|---|---|---|---|---|
| 1 | Cities Assessed | Cities Assessed | 234 | 80 | 185 | 90 | 135 |
| 2 | Cleanest City | Cleanest City | 445 | 80 | 185 | 90 | Ahmedabad |
| 3 | Avg Total Score | Average Total Score | 656 | 80 | 185 | 90 | 8,750 |
| 4 | GFC Certified % | Garbage-Free City Certified | 867 | 80 | 185 | 90 | 51.1% |
| 5 | Critical Cities | Critical Cities (< 6,000) | 1078 | 80 | 185 | 90 | 9 |

Card 2: set callout font size to **20** (city names are long). Card 5: callout colour `#B3261E`.
Rename a field in a visual by double-clicking it in the *Fields* well.

### 2e. The 5 charts

**Chart 1 — State/UT Average Score vs National Average** · *Line and clustered column chart* · X 224, Y 182, W 516, H 258
- X-axis: `state_ut` · Column y-axis: `Avg Total Score` · Line y-axis: `National Average`
- Sort: `Avg Total Score` descending.
- Columns → Colour → **fx** → Format style *Field value* → `State Bar Color` (states below the national average turn red).
- Line colour `#E07A1F`, width 2, dashed. Tooltips: add `Cities Assessed`.

**Chart 2 — Top 10 Cleanest Cities** · *Clustered bar chart* · X 752, Y 182, W 516, H 258
- Y-axis: `city_clean` · X-axis: `total_score` (Sum)
- Filters pane → `city_clean` → Filter type **Top N** → Top **10** by `total_score` → Apply.
- Bar colour `#138808`. Data labels **On**. Tooltips: `state_ut`, `population_category`.

**Chart 3 — 10 Cities Requiring Urgent Intervention** · *Clustered bar chart* · X 224, Y 452, W 340, H 256
- Same as Chart 2 but Top N → **Bottom 10**. Sort ascending by `total_score`.
- Bar colour `#B3261E`. Data labels **On**.

**Chart 4 — Cities by Performance Band** · *Donut chart* · X 576, Y 452, W 340, H 256
- Legend: `Performance Band` · Values: `Cities Assessed`
- Slice colours (same as legend in filter panel): Excellent `#138808`, Good `#1D4E89`, Average `#E07A1F`, Critical `#B3261E`.
- Detail labels: *Category, percent of total*. Inner radius ~60%.

**Chart 5 — Survey Score vs Certification Score** · *Scatter chart* · X 928, Y 452, W 340, H 256
- Values: `city_clean` · X-axis: `ss2024_score` (Sum) · Y-axis: `Certification Score` (Sum) · Legend: `population_category`
- Analytics pane → **Average line** on X and on Y (grey, dashed). This splits cities into four quadrants.
- Cities in the bottom-right quadrant (high survey score, low certification) are quick wins: they are clean on the ground but not yet certified.

---

## 3. Dashboard 2 — Ganga Water Quality

Table name below is `ganga_water_quality_clean` (abbreviated as **G** only in this text; use the full name in DAX).

### 3a. Calculated columns

```DAX
Compliance Status =
VAR DissolvedO2 = ganga_water_quality_clean[dissolved_oxygen_mean_mg_l]
VAR BOD = ganga_water_quality_clean[bod_mean_mg_l]
VAR PH = ganga_water_quality_clean[ph_mean]
VAR FecalColi = ganga_water_quality_clean[fecal_coliform_mean_mpn_100ml]
RETURN
    IF (
        ISBLANK ( DissolvedO2 ) || ISBLANK ( BOD ) || ISBLANK ( FecalColi ),
        "Insufficient Data",
        IF (
            DissolvedO2 >= 5 && BOD <= 3 && PH >= 6.5 && PH <= 8.5 && FecalColi <= 2500,
            "Fit for Bathing",
            "Unfit for Bathing"
        )
    )
```

The `ISBLANK` checks matter: in DAX a blank counts as 0, so a station with missing BOD would otherwise pass `BOD <= 3` and appear safe.

```DAX
State Order =
CALCULATE (
    MIN ( ganga_water_quality_clean[River Sequence] ),
    ALLEXCEPT ( ganga_water_quality_clean, ganga_water_quality_clean[state] )
)
```

Select `state` → **Sort by column → State Order** (states now appear upstream → downstream: Uttarakhand, Uttar Pradesh, Bihar, West Bengal).

### 3b. Measures

```DAX
Stations Monitored = COUNTROWS ( ganga_water_quality_clean )

Avg Dissolved Oxygen = AVERAGE ( ganga_water_quality_clean[dissolved_oxygen_mean_mg_l] )

Avg BOD = AVERAGE ( ganga_water_quality_clean[bod_mean_mg_l] )

Peak Fecal Coliform = MAX ( ganga_water_quality_clean[fecal_coliform_mean_mpn_100ml] )

Bathing Compliance % =
DIVIDE (
    CALCULATE ( [Stations Monitored], ganga_water_quality_clean[Compliance Status] = "Fit for Bathing" ),
    [Stations Monitored]
)

BOD KPI Color = IF ( [Avg BOD] > 3, "#B3261E", "#138808" )

DO KPI Color = IF ( [Avg Dissolved Oxygen] < 5, "#B3261E", "#138808" )

FC Chart Title =
"Most Contaminated Stations — worst is "
    & FORMAT ( DIVIDE ( [Peak Fecal Coliform], 2500 ), "#,0" )
    & "× the safe limit"
```

Formats: `Avg Dissolved Oxygen`, `Avg BOD` → 2 decimals. `Peak Fecal Coliform` → whole number with separator. `Bathing Compliance %` → Percentage, 1 decimal.

### 3c. Slicers

| Slicer | Field | Style | X | Y | W | H |
|---|---|---|---|---|---|---|
| State | `state` | Tile (buttons) | 20 | 122 | 184 | 120 |
| Compliance Status | `Compliance Status` | Vertical list | 20 | 250 | 184 | 96 |
| Monitoring Station | `station_location` | Dropdown, *Search* on | 20 | 354 | 184 | 64 |
| Clear button | Insert → Buttons → **Clear all slicers** | fill `#0E6E8C`, text white | 20 | 452 | 184 | 32 |

### 3d. KPI cards

| # | Measure | Category label | X | Y | W | H | Expected (all data) |
|---|---|---|---|---|---|---|---|
| 1 | Stations Monitored | Monitoring Stations | 234 | 80 | 185 | 90 | 66 |
| 2 | Avg Dissolved Oxygen | Avg Dissolved Oxygen (mg/L) | 445 | 80 | 185 | 90 | 7.97 |
| 3 | Avg BOD | Avg BOD (mg/L) — limit 3 | 656 | 80 | 185 | 90 | 3.11 (red) |
| 4 | Peak Fecal Coliform | Peak Fecal Coliform (MPN/100mL) | 867 | 80 | 185 | 90 | 4,93,750 |
| 5 | Bathing Compliance % | Stations Fit for Bathing | 1078 | 80 | 185 | 90 | 28.8% |

Card 2 callout → Colour **fx** → Field value → `DO KPI Color`. Card 3 → `BOD KPI Color`. Card 4 callout colour `#B3261E`.

### 3e. The 5 charts

**Chart 1 — Oxygen vs Organic Load Along the River (Gangotri → Diamond Harbour)** · *Line chart* · X 224, Y 182, W 516, H 258
- X-axis: `River Sequence` (axis type *Continuous*) · Y-axis: `Avg Dissolved Oxygen`, `Avg BOD`
- Tooltips: `station_location`, `state`.
- Line colours: DO `#1A936F`, BOD `#D97706`. Markers On, size 3.
- Analytics → **Constant line** Y = 5, `#1A936F`, dashed, label "DO minimum 5". Second constant line Y = 3, `#B3261E`, dashed, label "BOD limit 3".
- X-axis title On: "Monitoring stations, upstream → downstream".

**Chart 2 — Most Contaminated Stations** · *Clustered bar chart* · X 752, Y 182, W 516, H 258
- Y-axis: `station_location` · X-axis: `Peak Fecal Coliform`
- Filters → `station_location` → **Top N 10** by `Peak Fecal Coliform`.
- Bar colour `#B3261E`, data labels On. Analytics → Constant line X = 2500, label "Safe limit 2,500".
- Title → **fx** → Field value → `FC Chart Title` (title updates when slicers change).

**Chart 3 — State-wise Dissolved Oxygen vs BOD (mg/L)** · *Clustered column chart* · X 224, Y 452, W 340, H 256
- X-axis: `state` (sort axis by `state` ascending → follows river order) · Y-axis: `Avg Dissolved Oxygen`, `Avg BOD`
- Colours: DO `#1A936F`, BOD `#D97706`. Constant line Y = 3 (red, dashed). Data labels On.

**Chart 4 — Bathing-Water Compliance (CPCB Class B)** · *Donut chart* · X 576, Y 452, W 340, H 256
- Legend: `Compliance Status` · Values: `Stations Monitored`
- Colours: Fit for Bathing `#138808`, Unfit for Bathing `#B3261E`, Insufficient Data `#9AA5B1`.
- Expected: 19 fit, 39 unfit, 8 insufficient data.

**Chart 5 — Risk Matrix: BOD vs Dissolved Oxygen** · *Scatter chart* · X 928, Y 452, W 340, H 256
- Values: `station_location` · X-axis: `bod_mean_mg_l` (Average) · Y-axis: `dissolved_oxygen_mean_mg_l` (Average) · Legend: `state` · Size: `fecal_coliform_mean_mpn_100ml` (Average)
- Analytics → X-axis constant line 3 (red, dashed) and Y-axis constant line 5 (green, dashed).
- Stations to the right of the red line are over the BOD limit; bubble size shows sewage contamination.

---

## 4. Finishing touches

- **Consistent titles:** all chart titles are sentence case, 11 pt Segoe UI Semibold (set by the theme).
- **Alt text** (General → Alt text) on each chart: one-line description, for accessibility.
- **Hide visual headers in reading mode:** Format → Visual header Off, if you present without interaction.
- **Page navigator (optional):** Insert → Buttons → Navigator → *Page navigator*, place in the header at X 760, Y 22, W 280, H 26, fill transparent, text white.
- **Export for the report/PPT:** File → Export → *Export to PowerPoint* or *PDF* gives crisp slides at 16:9.

---

## 5. Headline insights to quote in the pitch

**Urban cleanliness**
- 41 of 135 cities (30%) are *Excellent* (≥ 10,000); 9 cities are *Critical* (< 6,000).
- All 10 lowest-ranked cities have **zero Garbage-Free City certification**; 4 of them are in Tamil Nadu.
- Highest state averages: Madhya Pradesh (11,684), Chhattisgarh (11,310), Gujarat (10,422). Lowest: Tripura, Tamil Nadu, Punjab, Kerala.
- Only 51% of cities hold any GFC certification. Certification is the fastest lever to raise scores.

**Ganga water quality**
- Only **19 of 66 stations (29%)** meet all CPCB bathing criteria; 39 fail; 8 lack data.
- Average BOD (3.11 mg/L) is already above the 3 mg/L bathing limit.
- West Bengal (Kolkata stretch) has the lowest oxygen (6.7 mg/L) and an average fecal coliform near 1,25,000 MPN/100mL, about 50× the safe limit. Dakshineswar peaks at 4,93,750 (about 198×).
- Dissolved oxygen stays healthy (> 5 mg/L) across the river; the problem is sewage (coliform) and organic load (BOD), not oxygen.

> Check before presenting: the year labels ("Swachh Survekshan 2024", "CPCB 2012") come from the dataset/column names. Confirm them against your source documents; edit `PAGES` in `make_backgrounds.py` and re-run if they differ.
