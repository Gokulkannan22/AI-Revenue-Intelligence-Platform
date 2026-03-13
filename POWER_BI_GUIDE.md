# AI Revenue Intelligence - Power BI Dashboard Design

This document outlines the professional Power BI dashboard design based on the `monthly_revenue.csv` dataset. It details the required DAX measures, visual configurations, and layout recommendations suitable for a high-end B2B SaaS analytics portfolio project.

## 1. Data Preparation

**Dataset:** `data/raw/monthly_revenue.csv`
**Columns Available:**
- `month` (Date)
- `total_revenue` (Whole Number)
- `active_customers` (Whole Number)
- `churn_count` (Whole Number)

*Note: In Power Query, ensure the `month` column is formatted as a Date data type.*

## 2. DAX Measures

To create dynamic, accurate KPIs, create the following measures in Power BI:

### Core Metrics

```dax
Total Revenue = SUM('monthly_revenue'[total_revenue])
```

```dax
Total Active Customers = SUM('monthly_revenue'[active_customers])
```

```dax
Total Churn = SUM('monthly_revenue'[churn_count])
```

### Calculated Metrics

```dax
ARPU (Average Revenue Per User) = 
DIVIDE(
    [Total Revenue], 
    [Total Active Customers], 
    0
)
```

### Growth & Variance Measures (Optional for advanced tooltips)

```dax
MoM Revenue Growth = 
VAR CurrentRev = [Total Revenue]
VAR PrevRev = CALCULATE([Total Revenue], PREVIOUSMONTH('monthly_revenue'[month]))
RETURN DIVIDE(CurrentRev - PrevRev, PrevRev, 0)
```

## 3. Dashboard Layout & Visuals

A clean, modern SaaS layout should be divided into a Top KPI Section and a Main Chart Area.

### Section A: KPI Cards (Top Row)
Place four standard KPI Cards across the top.
1. **Total Revenue:** Format as Currency (e.g., `$45.4M`).
2. **Total Active Customers:** Format as Whole Number, comma-separated (e.g., `20,000`).
3. **ARPU:** Format as Currency (e.g., `$2,271`).
4. **Total Churn:** Format as Whole Number, color-coded red to indicate a negative metric.

### Section B: Trend Analysis (Main Body)
Divide the remaining space into four quadrants for the charts:

1. **Revenue Trend (Top Left - Line Chart)**
   - **X-axis:** `month`
   - **Y-axis:** `[Total Revenue]`
   - **Formatting:** Smooth line, gradient fill below the line, data markers on hover.

2. **Active Customer Growth (Top Right - Line/Area Chart)**
   - **X-axis:** `month`
   - **Y-axis:** `[Total Active Customers]`
   - **Formatting:** distinct color (e.g., Teal), smooth area chart mapping the steady increase.

3. **ARPU Trend (Bottom Left - Line Chart)**
   - **X-axis:** `month`
   - **Y-axis:** `[ARPU]`
   - **Formatting:** Add a constant trendline or average line to show stability over time.

4. **Churn Trend (Bottom Right - Column Chart)**
   - **X-axis:** `month`
   - **Y-axis:** `[Total Churn]`
   - **Formatting:** Use strong/alert colors (e.g., deep orange or red) to signify lost accounts.

## 4. Theme and Aesthetics Recommendation

For a professional Data Science portfolio:
- **Background:** Dark mode (e.g., `#0F172A` - Slate 900) or ultra-clean light mode (`#F8FAFC`).
- **Accent Colors:** Use high-contrast modern palettes like Cyan (`#06B6D4`) for revenue and Purple (`#8B5CF6`) for user growth. 
- **Borders:** Enable visual borders with a 10px radius (rounded corners) and a subtle drop shadow to separate charts clearly from the background.
- **Interactivity:** Enable Cross-filtering so that clicking a specific month in the Churn chart highlights the exact Revenue drop in the trend lines.
