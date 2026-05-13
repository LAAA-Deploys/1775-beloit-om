#!/usr/bin/env python3
"""
1775 Beloit Avenue - Investment Summary (OM-style)
Build script: produces self-contained index.html for deployment to LAAA-Deploys/1775-beloit-om
"""
import base64, io, os, sys

if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(SCRIPT_DIR, "images")
OUTPUT = os.path.join(SCRIPT_DIR, "index.html")

def img_b64(filename, max_w=600):
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        print(f"  MISSING: {filename}")
        return ""
    ext = filename.rsplit(".", 1)[-1].lower()
    mime = {"png": "image/png", "jpg": "image/jpeg", "jpeg": "image/jpeg", "webp": "image/webp"}.get(ext, "image/png")
    try:
        from PIL import Image
        im = Image.open(path)
        if im.mode in ("RGBA", "P") and ext != "png":
            im = im.convert("RGB")
        if im.width > max_w:
            r = max_w / im.width
            im = im.resize((max_w, int(im.height * r)), Image.LANCZOS)
        buf = io.BytesIO()
        if ext == "png":
            im.save(buf, format="PNG", optimize=True)
        else:
            im.save(buf, format="JPEG", quality=80, optimize=True)
        data = base64.b64encode(buf.getvalue()).decode("ascii")
    except ImportError:
        with open(path, "rb") as f:
            data = base64.b64encode(f.read()).decode("ascii")
    print(f"  Loaded: {filename} ({len(data)//1024}KB)")
    return f"data:{mime};base64,{data}"

print("Loading images...")
LOGO_WHITE  = img_b64("LAAA_Team_White.png", 600)
LOGO_BLUE   = img_b64("LAAA_Team_Blue.png", 600)
GLEN_IMG    = img_b64("Glen_Scher.png", 300)
FILIP_IMG   = img_b64("Filip_Niculete.png", 300)
# Hero + gallery
HERO_IMG       = img_b64("hero.jpg", 1600) if os.path.exists(os.path.join(IMAGES_DIR, "hero.jpg")) else ""
EXTERIOR_IMG   = img_b64("exterior1.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "exterior1.jpg")) else ""
RENDERING_IMG  = img_b64("rendering.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "rendering.jpg")) else ""
ROOFTOP_IMG    = img_b64("rooftop_view.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "rooftop_view.jpg")) else ""
PATIO_IMG      = img_b64("rooftop_patio.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "rooftop_patio.jpg")) else ""
STUDIO_IMG     = img_b64("interior_studio.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "interior_studio.jpg")) else ""
KITCHEN_IMG    = img_b64("interior_kitchen.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "interior_kitchen.jpg")) else ""
COLIVING_IMG   = img_b64("interior_coliving.jpg", 1400) if os.path.exists(os.path.join(IMAGES_DIR, "interior_coliving.jpg")) else ""

# ============================================================
# DEAL DATA
# ============================================================
ADDRESS = "1775 Beloit Avenue"
CITY_STATE_ZIP = "West Los Angeles, CA 90025"
SUBMARKET = "Sawtelle / Japantown"
CLIENT_NAME = "Category Company"
COVER_MONTH_YEAR = "May 2026"
LAT, LNG = 34.044988771715, -118.44576413383

# Building
UNITS_EXISTING = 16
UNITS_W_ADU = 18
BEDS_EXISTING = 48
BEDS_W_ADU = 50
GROSS_SF = 35198
GROSS_SF_W_ADU = 36398
RENTABLE_SF = 23670
YEAR_BUILT = 2023
CONSTRUCTION = "Type II Steel-Frame"
STORIES = "7 stories above grade + 1 subterranean"

# Finance
ACQ_PRICE = 8625000
DEV_COST = 22000000
SELLER_NOTE = 16000000
ACQ_LOAN = 5606250
ACQ_RATE = 6.25
PERM_LOAN = 7407396
PERM_RATE = 5.25
TOTAL_BUDGET_ACQ = 9431662
TOTAL_BUDGET_PERM = 9496662
PEAK_EQUITY_ACQ = 3980412
PEAK_EQUITY_PERM = 2089266

# Pro Forma
GPR = 1157355
VACANCY_PCT = 6.20
VACANCY_AMT = 71756
TOTAL_OPEX = 471559
OPEX_PCT = 38.37
OPEX_PER_BED_MO = 785.93
NOI = 626357
CAP_ON_COST_UNTRENDED = 6.64
CAP_ON_COST_TRENDED = 7.22

# CoC
COC_ACQ_IO = 6.93
COC_PERM_IO = 11.37
COC_ACQ_PI = 5.33
COC_PERM_PI = 6.49
CFDS_ACQ_IO = 275966
CFDS_PERM_IO = 237469
DS_ACQ_IO = 350391
DS_PERM_IO = 388888
DSCR_PERM_PI = 1.28
DSCR_ACQ_PI = 1.51

# Alternate basis scenario
ALT_PRICE = 7900000  # Effective basis / negotiated tax assessment / lower-basis scenario

def derive(price):
    return {
        "ppu_existing": price / UNITS_EXISTING,
        "ppu_w_adu":    price / UNITS_W_ADU,
        "ppb_existing": price / BEDS_EXISTING,
        "ppb_w_adu":    price / BEDS_W_ADU,
        "psf_rent":     price / RENTABLE_SF,
        "psf_gross":    price / GROSS_SF,
        "disc_repl":    1 - (price / DEV_COST),
        "cap_on_price": NOI / price,
        # Yield on cost = NOI / (PP + non-PP costs in acq scenario)
        "yoc_acq":      NOI / (price + (TOTAL_BUDGET_ACQ - ACQ_PRICE)),
        "yoc_perm":     NOI / (price + (TOTAL_BUDGET_PERM - ACQ_PRICE)),
    }

BASE = derive(ACQ_PRICE)
ALT  = derive(ALT_PRICE)

PPU_EXISTING = BASE["ppu_existing"]
PPU_W_ADU = BASE["ppu_w_adu"]
PPB_EXISTING = BASE["ppb_existing"]
PPB_W_ADU = BASE["ppb_w_adu"]
PRICE_PSF_RENT = BASE["psf_rent"]
PRICE_PSF_GROSS = BASE["psf_gross"]
DISCOUNT_TO_REPLACEMENT = BASE["disc_repl"]

# Comp benchmark math
UCLA_PPB = 250000
UCLA_DISCOUNT = 1 - (PPB_EXISTING / UCLA_PPB)
UCLA_DISCOUNT_ALT = 1 - (ALT["ppb_existing"] / UCLA_PPB)

def money(n, decimals=0):
    if n >= 1_000_000:
        if decimals == 0:
            return f"${n/1_000_000:,.2f}M"
        return f"${n/1_000_000:,.{decimals}f}M"
    return f"${n:,.0f}"

def usd(n):
    return f"${n:,.0f}"

def pct(n, decimals=2):
    return f"{n:.{decimals}f}%"

# ============================================================
# UNIT MIX TABLE
# ============================================================
UNIT_MIX_ROWS = [
    # type, count, sf, rent/bed, unit rent, gross rent
    ("Studio", 8, 400, None, 2450, 235200),
    ("5BR / 5BA Co-Living", 8, 1800, 1570, 7850, 753600),
    ("1BR (ADU - Planned)", 2, 550, None, 2600, 62400),
]

# ============================================================
# OPERATING STATEMENT
# ============================================================
INCOME_ITEMS = [
    ("Studio Rent (8 units)", 235200),
    ("Co-Living Rent (8 units / 40 beds @ $1,570/bed)", 753600),
    ("1BR ADU Rent (2 units @ $2,600/mo)", 62400),
    ("Less Concessions", -3602),
    ("Parking (19 spaces @ $150)", 34200),
    ("Trash & Internet (50 beds @ $30)", 18000),
    ("RUBS (50 beds @ $55)", 33000),
    ("Misc Fees (50 beds @ $41)", 24556),
]
GPR_SUM = sum(v for _, v in INCOME_ITEMS)

EXPENSE_ITEMS = [
    ("Bad Debt", "1.75% of revenue", 19192),
    ("Advertising & Marketing", "$143.75 / unit / mo", 27600),
    ("Contract Services", "Landscape, elevator, etc.", 18188),
    ("Cleaning", "$0.96 / SF", 22641),
    ("Turnover", "$107.14 / turned unit", 5143),
    ("Community & Shared Goods", "$13.00 / co-living bed / mo", 6240),
    ("General & Administrative", "$33.33 / unit / mo", 19998),
    ("Insurance", "$0.90 / SF", 21277),
    ("Payroll", "Lump sum", 83338),
    ("Professional Fees", "$42.67 / unit / mo", 25600),
    ("Repairs & Maintenance", "$1,761.90 / mo", 21143),
    ("Utilities + Internet", "$130.76 / unit / mo", 78457),
    ("Property Taxes", "1.11% on $7.9M assessed (per seller deal)", 95325),
    ("Management Fee", "2.50% of revenue (self-manage)", 27417),
]

# ============================================================
# HIGHLIGHTS
# ============================================================
HIGHLIGHTS = [
    ("Distressed Basis at 39% of Replacement Cost",
     [f"Acquisition at {money(ACQ_PRICE)} vs. {money(DEV_COST)} developer cost basis ({pct(DISCOUNT_TO_REPLACEMENT*100, 0)} discount)",
      f"Per-bed basis of {usd(PPB_EXISTING)} vs. UCLA's recent co-living acquisitions at $250,000 per bed ({pct(UCLA_DISCOUNT*100, 0)} discount)",
      f"Clean title delivered via lender foreclosure; $45M second-position note extinguished pre-close"]),
    ("New Construction, Premium Specification",
     ["Completed 2023 by NMS Properties at a ~$22M cost basis",
      "Type II steel-frame, 7 stories above grade + 1 subterranean level",
      "Two-story co-living residences with private bath, AC, fridge, microwave, and TV in every bedroom",
      "Above-standard amenity package for the co-living product class"]),
    ("Prime Sawtelle / Japantown Submarket",
     ["One block off Sawtelle Boulevard retail and dining corridor",
      "Direct access to UCLA, employment centers, and West LA amenities",
      "Comp: SW by CLG (California Landmark, 2 blocks south) achieving $2,300+/mo on 375 SF micro-units",
      "Durable rental demand from young professionals, students, and workforce renters"]),
    ("Operational Turnaround: Receiver to Specialist Operator",
     ["Asset partially vacated under receivership (UCLA direct-sale strategy abandoned); ~58% occupancy at close",
      "Receiver contract services running at ~3x Category's portfolio benchmark on 2x-size assets",
      "Category's in-house property management to assume immediately, shift to by-the-bed leasing",
      "Typical leasing velocity of 1-3 leases / week supports ~12-week path to stabilized occupancy"]),
    ("Density Expansion: Two Ground-Floor ADUs",
     ["Plan to add 2 x 1BR ADUs on the ground floor using underutilized space",
      "Projected $2,600 per unit per month in incremental rent",
      "Built with Category's in-house construction capability for minimal additional basis"]),
    ("Capital Structure: Attractive Acquisition Loan + Refi Path",
     [f"Acquisition: {money(ACQ_LOAN)} @ {pct(ACQ_RATE)} IO from RBB Bank (Prime - 50 bps), no prepay penalty, Sponsor PG",
      f"Stabilization refi target: ~{pct(PERM_RATE)} IO (matches Category's March 2026 co-living refi execution)",
      f"Refinance projected to return ~50% of invested equity and lift stabilized cash-on-cash to ~{pct(COC_PERM_IO)}"]),
    ("Specialist Sponsor: Largest Self-Managed Co-Living Portfolio in LA",
     ["Category Company operates the largest self-managed co-living portfolio in Los Angeles",
      "Multiple buildings in the immediate vicinity providing real-time submarket intelligence",
      "Low-cost vendor and service network extends to 1775 Beloit at marginal cost",
      "Prior NMS-conversion benchmark: Wilshire Margot achieved $2,000+ per bed (2018)"]),
    ("Rent Upside Optionality Above Underwriting",
     ["Base case underwrites $1,570 per bed (~$100 below in-place average of $1,648)",
      "Category portfolio has recently leased co-living rooms up to $1,850/mo - $280 above base case",
      "Each $100 / bed = ~50 bps to untrended YoC and ~20% to stabilized CoC"]),
]

# ============================================================
# Build HTML
# ============================================================
print("Building HTML...")

HEAD = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>1775 Beloit Avenue - Investment Summary</title>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
html {{ scroll-padding-top: 50px; }}
body {{ font-family: 'Inter', sans-serif; color: #333; line-height: 1.6; background: #fff; }}
p {{ margin-bottom: 16px; font-size: 14px; line-height: 1.7; }}

/* ---- COVER ---- */
.cover {{
  position: relative;
  min-height: 100vh;
  background: linear-gradient(135deg, #0f2640 0%, #1B3A5C 50%, #244a6e 100%);
  color: #fff; display: flex; flex-direction: column; justify-content: center; align-items: center;
  padding: 60px 40px;
}}
.cover::before {{
  content: ""; position: absolute; inset: 0;
  background:
    radial-gradient(ellipse at top right, rgba(197,162,88,0.12), transparent 60%),
    radial-gradient(ellipse at bottom left, rgba(197,162,88,0.08), transparent 60%);
  pointer-events: none;
}}
.cover-logo {{ width: 240px; margin-bottom: 28px; position: relative; }}
.cover-content {{ position: relative; text-align: center; max-width: 900px; }}
.cover-label {{ color: #C5A258; font-size: 13px; font-weight: 600; text-transform: uppercase; letter-spacing: 4px; margin-bottom: 18px; }}
.cover-title {{ font-size: 56px; font-weight: 700; letter-spacing: -1px; margin-bottom: 8px; }}
.cover-sub {{ font-size: 18px; color: #C5A258; margin-bottom: 4px; font-weight: 500; letter-spacing: 1px; }}
.cover-submarket {{ font-size: 14px; color: rgba(255,255,255,0.7); margin-bottom: 30px; text-transform: uppercase; letter-spacing: 2px; }}
.cover-price {{ font-size: 48px; font-weight: 700; color: #C5A258; margin-bottom: 8px; }}
.cover-price-label {{ font-size: 11px; color: rgba(255,255,255,0.6); text-transform: uppercase; letter-spacing: 2px; margin-bottom: 30px; }}
.cover-stats {{ display: flex; justify-content: center; flex-wrap: wrap; gap: 26px; margin: 30px 0; padding: 24px 0; border-top: 1px solid rgba(197,162,88,0.3); border-bottom: 1px solid rgba(197,162,88,0.3); }}
.cover-stats > div {{ display: flex; flex-direction: column; align-items: center; min-width: 80px; }}
.cv {{ font-size: 24px; font-weight: 700; color: #fff; }}
.cl {{ font-size: 10px; color: #C5A258; text-transform: uppercase; letter-spacing: 1.5px; margin-top: 4px; }}
.client-greeting {{ font-size: 16px; color: #fff; margin: 16px 0; font-weight: 500; }}
.cover-agent {{ font-size: 13px; color: rgba(255,255,255,0.85); margin-top: 6px; letter-spacing: 0.5px; }}
.cover-date {{ font-size: 12px; color: rgba(255,255,255,0.6); margin-top: 4px; letter-spacing: 1px; }}
.cover-nyse {{ font-size: 10px; color: rgba(255,255,255,0.35); margin-top: 22px; text-transform: uppercase; letter-spacing: 4px; }}

/* ---- TOC ---- */
.toc-nav {{ background: #1B3A5C; padding: 0 20px; display: flex; flex-wrap: nowrap; gap: 0; justify-content: center; align-items: stretch; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 8px rgba(0,0,0,0.15); overflow-x: auto; -webkit-overflow-scrolling: touch; }}
.toc-nav a {{ color: rgba(255,255,255,0.65); text-decoration: none; font-size: 10px; font-weight: 500; letter-spacing: 0.5px; text-transform: uppercase; padding: 13px 13px; border-bottom: 2px solid transparent; transition: all 0.2s ease; white-space: nowrap; display: flex; align-items: center; }}
.toc-nav a:hover {{ color: #fff; background: rgba(197,162,88,0.12); border-bottom-color: rgba(197,162,88,0.4); }}
.toc-nav a.toc-active {{ color: #C5A258; font-weight: 600; border-bottom-color: #C5A258; }}

/* ---- SECTIONS ---- */
.section {{ padding: 60px 40px; max-width: 1100px; margin: 0 auto; }}
.section-alt {{ background: #f8f9fa; }}
.section-title {{ font-size: 28px; font-weight: 700; color: #1B3A5C; margin-bottom: 6px; }}
.section-subtitle {{ font-size: 13px; color: #C5A258; text-transform: uppercase; letter-spacing: 1.5px; margin-bottom: 16px; font-weight: 500; }}
.section-divider {{ width: 60px; height: 3px; background: #C5A258; margin-bottom: 30px; }}
.sub-heading {{ font-size: 18px; font-weight: 600; color: #1B3A5C; margin: 30px 0 16px; }}

/* ---- METRIC CARDS ---- */
.mg4 {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 30px; }}
.mg5 {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 14px; margin-bottom: 30px; }}
.metric-card {{ background: #1B3A5C; border-radius: 12px; padding: 22px 16px; text-align: center; color: #fff; }}
.metric-value {{ display: block; font-size: 26px; font-weight: 700; }}
.metric-label {{ display: block; font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; color: rgba(255,255,255,0.65); margin-top: 6px; }}
.metric-sub {{ display: block; font-size: 11px; color: #C5A258; margin-top: 4px; }}

/* ---- TABLES ---- */
table {{ width: 100%; border-collapse: collapse; margin-bottom: 24px; font-size: 13px; }}
th {{ background: #1B3A5C; color: #fff; padding: 10px 12px; text-align: left; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }}
td {{ padding: 8px 12px; border-bottom: 1px solid #eee; }}
tr:nth-child(even) {{ background: #f5f5f5; }}
tr.hl {{ background: #FFF8E7 !important; border-left: 3px solid #C5A258; }}
tr.totalrow {{ background: #1B3A5C !important; color: #fff; font-weight: 700; }}
tr.totalrow td {{ color: #fff; border-bottom: none; }}
tr.subtotal {{ background: #e6ecf3 !important; font-weight: 600; }}
td.num, th.num {{ text-align: right; font-variant-numeric: tabular-nums; }}
.ts {{ overflow-x: auto; -webkit-overflow-scrolling: touch; margin-bottom: 24px; }}
.ts table {{ min-width: 560px; margin-bottom: 0; }}

/* ---- HIGHLIGHT BOXES ---- */
.hb-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 18px; }}
.hb {{ background: #1B3A5C; color: #fff; border-radius: 8px; padding: 22px 24px; }}
.hb h4 {{ color: #C5A258; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 12px; line-height: 1.3; }}
.hb ul {{ padding-left: 18px; margin: 0; }}
.hb li {{ margin-bottom: 8px; font-size: 13px; line-height: 1.55; color: rgba(255,255,255,0.92); }}
.hb li:last-child {{ margin-bottom: 0; }}

/* ---- CALLOUTS ---- */
.cn {{ background: #FFF8E7; border-left: 4px solid #C5A258; padding: 16px 20px; margin: 24px 0; border-radius: 0 4px 4px 0; font-size: 13px; line-height: 1.65; }}
.cn strong {{ color: #1B3A5C; }}
.bp {{ background: #f0f4f8; border-left: 4px solid #1B3A5C; padding: 22px 26px; margin: 24px 0; border-radius: 0 6px 6px 0; }}
.bp-label {{ font-size: 12px; font-weight: 700; text-transform: uppercase; letter-spacing: 1.5px; color: #1B3A5C; margin-bottom: 12px; }}
.bp ul {{ list-style: none; padding: 0; margin: 0; }}
.bp li {{ padding: 8px 0; border-bottom: 1px solid #dce3eb; font-size: 14px; line-height: 1.6; color: #333; }}
.bp li:last-child {{ border-bottom: none; }}
.bp li strong {{ color: #1B3A5C; }}

/* ---- INFO TABLE ---- */
.it {{ width: 100%; border-collapse: collapse; }}
.it td {{ padding: 9px 14px; border-bottom: 1px solid #eee; font-size: 13px; }}
.it td:first-child {{ font-weight: 600; color: #1B3A5C; width: 38%; }}

.two-col {{ display: grid; grid-template-columns: 1fr 1fr; gap: 30px; margin-bottom: 30px; }}

/* ---- BENCHMARK COMPS ---- */
.bench-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; margin-top: 20px; }}
.bench {{ background: #fff; border: 1px solid #e0e0e0; border-top: 4px solid #C5A258; padding: 20px; border-radius: 0 0 6px 6px; }}
.bench h5 {{ color: #1B3A5C; font-size: 14px; margin-bottom: 6px; }}
.bench .subj {{ color: #C5A258; font-size: 11px; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; font-weight: 600; }}
.bench .stat {{ font-size: 22px; color: #1B3A5C; font-weight: 700; margin-bottom: 4px; }}
.bench .stat-l {{ font-size: 11px; color: #666; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 14px; }}
.bench p {{ font-size: 12px; line-height: 1.55; margin: 0; color: #555; }}

/* ---- PHOTO GRID ---- */
.photo-grid {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin: 24px 0 30px; }}
.photo-grid .pg-item {{ position: relative; overflow: hidden; border-radius: 6px; aspect-ratio: 4 / 3; background: #1B3A5C; }}
.photo-grid .pg-item img {{ width: 100%; height: 100%; object-fit: cover; display: block; transition: transform 0.4s ease; }}
.photo-grid .pg-item:hover img {{ transform: scale(1.04); }}
.photo-grid .pg-caption {{ position: absolute; bottom: 0; left: 0; right: 0; padding: 10px 14px; background: linear-gradient(to top, rgba(0,0,0,0.7), transparent); color: #fff; font-size: 12px; font-weight: 500; letter-spacing: 0.5px; }}
.photo-grid .pg-hero {{ grid-column: span 2; grid-row: span 2; aspect-ratio: 8 / 6; }}

/* ---- SENSITIVITY ---- */
.sens-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 0; margin: 18px 0 28px; border-radius: 8px; overflow: hidden; box-shadow: 0 1px 4px rgba(0,0,0,0.06); }}
.sens-col {{ background: #fff; padding: 28px 26px; }}
.sens-col.headline {{ background: #1B3A5C; color: #fff; }}
.sens-col.alt {{ background: #fffaf0; border-left: 4px solid #C5A258; }}
.sens-label {{ font-size: 11px; text-transform: uppercase; letter-spacing: 2px; font-weight: 600; margin-bottom: 6px; opacity: 0.85; }}
.sens-col.headline .sens-label {{ color: #C5A258; opacity: 1; }}
.sens-col.alt .sens-label {{ color: #C5A258; }}
.sens-price {{ font-size: 38px; font-weight: 700; line-height: 1; margin-bottom: 6px; }}
.sens-col.headline .sens-price {{ color: #fff; }}
.sens-col.alt .sens-price {{ color: #1B3A5C; }}
.sens-sub {{ font-size: 12px; opacity: 0.7; margin-bottom: 20px; }}
.sens-rows {{ font-size: 13px; }}
.sens-rows .sens-row {{ display: flex; justify-content: space-between; padding: 7px 0; border-bottom: 1px solid rgba(0,0,0,0.07); }}
.sens-col.headline .sens-rows .sens-row {{ border-bottom-color: rgba(255,255,255,0.12); }}
.sens-rows .sens-row .k {{ opacity: 0.75; }}
.sens-rows .sens-row .v {{ font-weight: 600; font-variant-numeric: tabular-nums; }}

/* ---- VALUE CREATION ---- */
.vc {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 24px; margin-top: 18px; }}
.vc-card {{ background: #fff; border: 1px solid #e6e6e6; padding: 24px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.04); }}
.vc-num {{ font-size: 32px; font-weight: 700; color: #C5A258; line-height: 1; margin-bottom: 8px; }}
.vc-title {{ font-size: 16px; font-weight: 700; color: #1B3A5C; margin-bottom: 12px; }}
.vc-card p {{ font-size: 13px; line-height: 1.6; color: #444; margin-bottom: 0; }}

/* ---- LEAFLET MAP ---- */
.leaflet-map {{ height: 380px; border-radius: 6px; border: 1px solid #ddd; margin: 16px 0 30px; z-index: 1; }}
.map-fallback {{ display: none; font-size: 12px; color: #666; font-style: italic; margin-bottom: 30px; }}

/* ---- FOOTER ---- */
.footer {{ background: #1B3A5C; color: #fff; padding: 60px 40px; text-align: center; }}
.footer-logo {{ width: 200px; margin-bottom: 30px; }}
.footer-team {{ display: flex; justify-content: center; gap: 50px; margin-bottom: 36px; flex-wrap: wrap; }}
.fp {{ text-align: center; min-width: 240px; max-width: 320px; }}
.footer-headshot {{ width: 80px; height: 80px; border-radius: 50%; border: 2px solid #C5A258; object-fit: cover; margin-bottom: 14px; }}
.footer-name {{ font-size: 17px; font-weight: 600; }}
.footer-title {{ font-size: 12px; color: #C5A258; margin-bottom: 10px; letter-spacing: 0.5px; }}
.footer-contact {{ font-size: 12px; color: rgba(255,255,255,0.75); line-height: 1.8; }}
.footer-contact a {{ color: rgba(255,255,255,0.75); text-decoration: none; }}
.footer-contact a:hover {{ color: #C5A258; }}
.footer-office {{ font-size: 12px; color: rgba(255,255,255,0.55); margin-top: 20px; }}
.footer-disclaimer {{ font-size: 10px; color: rgba(255,255,255,0.35); margin-top: 24px; max-width: 880px; margin-left: auto; margin-right: auto; line-height: 1.6; }}

/* ---- DOWNLOAD ---- */
.download-btn {{ position: fixed; bottom: 24px; right: 24px; z-index: 200; background: #1B3A5C; color: #fff; border: 2px solid #C5A258; border-radius: 8px; padding: 12px 20px; cursor: pointer; font-family: 'Inter', sans-serif; font-size: 13px; font-weight: 600; display: flex; align-items: center; gap: 8px; box-shadow: 0 4px 16px rgba(0,0,0,0.2); transition: all 0.2s ease; }}
.download-btn:hover {{ background: #244a6e; transform: translateY(-2px); }}
.download-btn svg {{ color: #C5A258; }}

/* ---- MOBILE ---- */
@media (max-width: 768px) {{
  .cover {{ padding: 40px 20px; min-height: 90vh; }}
  .cover-title {{ font-size: 34px; }}
  .cover-price {{ font-size: 36px; }}
  .cover-logo {{ width: 180px; }}
  .cover-stats {{ gap: 16px; }}
  .cv {{ font-size: 18px; }}
  .cl {{ font-size: 9px; }}
  .section {{ padding: 36px 18px; }}
  .section-title {{ font-size: 22px; }}
  .mg4 {{ grid-template-columns: repeat(2, 1fr); }}
  .mg5 {{ grid-template-columns: repeat(2, 1fr); }}
  .hb-grid {{ grid-template-columns: 1fr; }}
  .vc {{ grid-template-columns: 1fr; }}
  .bench-grid {{ grid-template-columns: 1fr; }}
  .two-col {{ grid-template-columns: 1fr; }}
  .photo-grid {{ grid-template-columns: repeat(2, 1fr); }}
  .photo-grid .pg-hero {{ grid-column: span 2; }}
  .sens-grid {{ grid-template-columns: 1fr; }}
  .sens-price {{ font-size: 30px; }}
  .footer-team {{ flex-direction: column; align-items: center; gap: 36px; }}
  .leaflet-map {{ height: 300px; }}
  .toc-nav a {{ font-size: 10px; padding: 10px 8px; }}
}}
@media (max-width: 420px) {{
  .cover-title {{ font-size: 26px; }}
  .cover-price {{ font-size: 30px; }}
  .cover-stats {{ gap: 10px; }}
  .section-title {{ font-size: 20px; }}
  .metric-value {{ font-size: 20px; }}
  .leaflet-map {{ height: 240px; }}
  .download-btn span {{ display: none; }}
  .download-btn {{ padding: 10px 12px; }}
}}
@media print {{
  @page {{ margin: 0.6in 0.5in; }}
  .toc-nav, .download-btn {{ display: none !important; }}
  .leaflet-map {{ display: none !important; }}
  .map-fallback {{ display: block !important; }}
  .cover {{ min-height: auto; page-break-after: always; }}
  .section {{ page-break-before: always; }}
  thead {{ display: table-header-group; }}
  tr {{ page-break-inside: avoid; }}
  h2, h3, .section-title, .sub-heading {{ page-break-after: avoid; }}
  p {{ orphans: 3; widows: 3; }}
  body {{ background: #fff; }}
}}
</style>
</head>
<body>
"""

# Cover
hero_bg_style = (
    f"background: url('{HERO_IMG}') center/cover no-repeat, "
    f"linear-gradient(135deg, #0f2640 0%, #1B3A5C 50%, #244a6e 100%);"
    if HERO_IMG else ""
)
COVER = f"""
<div class="cover" style="{hero_bg_style}">
  <img src="{LOGO_WHITE}" class="cover-logo" alt="LAAA Team at Marcus & Millichap">
  <div class="cover-content">
    <div class="cover-label">Investment Summary</div>
    <h1 class="cover-title">{ADDRESS}</h1>
    <p class="cover-sub">{CITY_STATE_ZIP}</p>
    <p class="cover-submarket">{SUBMARKET}</p>
    <div class="cover-price">{money(ACQ_PRICE)}</div>
    <div class="cover-price-label">Acquisition Basis</div>
    <div class="cover-stats">
      <div><span class="cv">{UNITS_EXISTING}</span><span class="cl">Units</span></div>
      <div><span class="cv">{BEDS_EXISTING}</span><span class="cl">Beds</span></div>
      <div><span class="cv">{RENTABLE_SF:,}</span><span class="cl">Rentable SF</span></div>
      <div><span class="cv">{YEAR_BUILT}</span><span class="cl">Year Built</span></div>
      <div><span class="cv">{CAP_ON_COST_UNTRENDED}%</span><span class="cl">Stab. Yield on Cost</span></div>
    </div>
    <p class="client-greeting" id="client-greeting">Prepared for {CLIENT_NAME}</p>
    <p class="cover-agent">Glen Scher &nbsp;|&nbsp; Filip Niculete &nbsp;&nbsp;&nbsp; Senior Managing Directors of Investments</p>
    <p class="cover-date">{COVER_MONTH_YEAR}</p>
    <p class="cover-nyse">NYSE: MMI</p>
  </div>
</div>
"""

TOC = """
<nav class="toc-nav" id="toc-nav">
  <a href="#overview">Overview</a>
  <a href="#highlights">Highlights</a>
  <a href="#asset">The Asset</a>
  <a href="#location">Location</a>
  <a href="#value-creation">Value Creation</a>
  <a href="#submarket">Submarket Comps</a>
  <a href="#financials">Financials</a>
  <a href="#contact">Contact</a>
</nav>
"""

# ---- OVERVIEW ----
OVERVIEW = f"""
<section class="section" id="overview">
  <p class="section-subtitle">Section I</p>
  <h2 class="section-title">Investment Overview</h2>
  <div class="section-divider"></div>

  <div class="mg5">
    <div class="metric-card"><span class="metric-value">{money(ACQ_PRICE, 2)}</span><span class="metric-label">Acquisition Basis</span></div>
    <div class="metric-card"><span class="metric-value">{usd(PPB_EXISTING)}</span><span class="metric-label">$ / Bed</span><span class="metric-sub">vs. UCLA $250K</span></div>
    <div class="metric-card"><span class="metric-value">${PRICE_PSF_RENT:.0f}</span><span class="metric-label">$ / Rentable SF</span></div>
    <div class="metric-card"><span class="metric-value">{pct(CAP_ON_COST_UNTRENDED)}</span><span class="metric-label">Untrended YoC</span></div>
    <div class="metric-card"><span class="metric-value">{pct(COC_PERM_IO)}</span><span class="metric-label">Stabilized CoC (Perm IO)</span></div>
  </div>

  <p>1775 Beloit Avenue is a newly constructed, premium-specification co-living asset in the Sawtelle / Japantown submarket of West Los Angeles, being acquired by Category Company for <strong>{money(ACQ_PRICE, 2)}</strong> &mdash; a {pct(DISCOUNT_TO_REPLACEMENT*100, 0)} discount to the prior developer's all-in cost basis of approximately {money(DEV_COST, 0)}. The acquisition is executed via lender foreclosure out of receivership, delivering clean title and eliminating any successor liability.</p>

  <p>The 16-unit / 48-bed building was completed in 2023 by NMS Properties (the developer behind the Wilshire Margot conversion) but never reached stabilization. Adverse capital market conditions, the construction lender's insolvency, the developer's passing, and an abandoned direct sale to UCLA combined to leave the asset partially vacated (~58% occupied) and burdened with bloated receiver operating costs. At a stabilized return of cost of <strong>{pct(CAP_ON_COST_UNTRENDED)}</strong>, the in-place basis offers an exceptional risk-adjusted entry into a high-demand West LA submarket.</p>

  <p>Category Company is the largest self-managed co-living operator in Los Angeles, with several properties in the immediate vicinity of 1775 Beloit. The business plan combines (i) immediate operational turnaround under Category's in-house property management platform, (ii) two ground-floor ADUs adding ~$62,400 in incremental annual rent, and (iii) a stabilization refinance into ~5.25% IO debt projected to return approximately 50% of invested equity within 12 to 18 months.</p>

  <div class="bp">
    <div class="bp-label">Target Limited Partner Profile</div>
    <ul>
      <li><strong>Yield-Oriented Co-Investors</strong> &mdash; Seeking a stabilized {pct(COC_PERM_IO)} cash-on-cash with a credible 12-18 month path and refinance-driven capital return.</li>
      <li><strong>Distressed / Special Situations Capital</strong> &mdash; Recognizing the 39% discount to replacement cost as the central margin of safety regardless of further rent growth.</li>
      <li><strong>West LA / Co-Living Thesis Investors</strong> &mdash; Allocating to a niche where Category is the dominant operator with verified rent ceilings $280+/bed above underwriting.</li>
      <li><strong>1031 Exchange Participants</strong> &mdash; Deploying into a new-construction, low-cost-basis asset with structural rent upside.</li>
    </ul>
    <p style="font-size:13px; color:#555; margin-top:14px; font-style:italic; margin-bottom: 0;">Specialist sponsor, distressed entry, and verified submarket demand support a wide LP appeal across yield and value buckets.</p>
  </div>
</section>
"""

# ---- HIGHLIGHTS ----
hb_html = ""
for title, bullets in HIGHLIGHTS:
    lis = "".join(f"<li>{b}</li>" for b in bullets)
    hb_html += f'<div class="hb"><h4>{title}</h4><ul>{lis}</ul></div>'

HIGHLIGHTS_SECTION = f"""
<section class="section section-alt" id="highlights">
  <p class="section-subtitle">Section II</p>
  <h2 class="section-title">Investment Highlights</h2>
  <div class="section-divider"></div>
  <div class="hb-grid">
    {hb_html}
  </div>
</section>
"""

# ---- THE ASSET ----
ASSET = f"""
<section class="section" id="asset">
  <p class="section-subtitle">Section III</p>
  <h2 class="section-title">The Asset</h2>
  <div class="section-divider"></div>

  <div class="two-col">
    <div>
      <p>1775 Beloit Avenue was developed by NMS Properties as a ground-up co-living project. Construction began in 2019 and the building was completed in 2023 at a total development cost of approximately {money(DEV_COST, 0)}. The improvements consist of {CONSTRUCTION} construction across {STORIES}, an expensive high-rise typology that would be cost-prohibitive to replicate at today's construction pricing.</p>

      <p>All co-living units are configured as <strong>two-story residences</strong> &mdash; a complex and high-cost design execution in a multistory building &mdash; with each of the five bedrooms within a co-living unit featuring its own private bathroom, built-in refrigerator, microwave, flat-screen television, and dedicated air conditioning system. The amenity package sits meaningfully above the standard co-living offering in the LA market.</p>

      <p>The current footprint comprises 16 units and 48 bedrooms (8 studios at ~400 SF and 8 five-bedroom / five-bathroom co-living units at ~1,800 SF), with planned conversion of underutilized ground-floor space into two 1-bedroom ADUs, taking the property to <strong>18 units / 50 beds</strong>.</p>
    </div>
    <table class="it">
      <tr><td>Address</td><td>{ADDRESS}</td></tr>
      <tr><td>City, State, Zip</td><td>{CITY_STATE_ZIP}</td></tr>
      <tr><td>Submarket</td><td>{SUBMARKET}</td></tr>
      <tr><td>Year Built</td><td>{YEAR_BUILT} (completed; construction begun 2019)</td></tr>
      <tr><td>Developer</td><td>NMS Properties</td></tr>
      <tr><td>Construction</td><td>{CONSTRUCTION}</td></tr>
      <tr><td>Stories</td><td>{STORIES}</td></tr>
      <tr><td>Units (Existing)</td><td>{UNITS_EXISTING}</td></tr>
      <tr><td>Units (with ADUs)</td><td>{UNITS_W_ADU}</td></tr>
      <tr><td>Bedrooms (Existing)</td><td>{BEDS_EXISTING}</td></tr>
      <tr><td>Bedrooms (with ADUs)</td><td>{BEDS_W_ADU}</td></tr>
      <tr><td>Bathrooms</td><td>{BEDS_EXISTING} (private bath per bedroom)</td></tr>
      <tr><td>Rentable Floor Area</td><td>{RENTABLE_SF:,} SF</td></tr>
      <tr><td>Gross Building Area</td><td>{GROSS_SF:,} SF (incl. parking basement)</td></tr>
      <tr><td>Parking Spaces</td><td>19 (6 dedicated to ADU units)</td></tr>
      <tr><td>Developer Cost Basis</td><td>~{money(DEV_COST, 0)}</td></tr>
      <tr><td>Acquisition Basis</td><td><strong>{money(ACQ_PRICE, 2)}</strong></td></tr>
      <tr><td>Discount to Replacement</td><td><strong>{pct(DISCOUNT_TO_REPLACEMENT*100, 0)}</strong></td></tr>
    </table>
  </div>

  <h3 class="sub-heading">Unit Mix and Stabilized Rents</h3>
  <div class="ts">
  <table>
    <thead>
      <tr>
        <th>Unit Type</th>
        <th class="num">Units</th>
        <th class="num">Avg SF</th>
        <th class="num">Rent / Bed</th>
        <th class="num">Rent / Unit</th>
        <th class="num">Annual Gross Rent</th>
      </tr>
    </thead>
    <tbody>
"""
for label, ct, sf, rpb, ru, gr in UNIT_MIX_ROWS:
    rpb_str = usd(rpb) if rpb else "&mdash;"
    ASSET += f"""
      <tr>
        <td>{label}</td>
        <td class="num">{ct}</td>
        <td class="num">{sf:,}</td>
        <td class="num">{rpb_str}</td>
        <td class="num">{usd(ru)}</td>
        <td class="num">{usd(gr)}</td>
      </tr>"""
ASSET += f"""
      <tr class="subtotal">
        <td><strong>Total (with ADUs)</strong></td>
        <td class="num"><strong>{UNITS_W_ADU}</strong></td>
        <td class="num"></td>
        <td class="num"></td>
        <td class="num"></td>
        <td class="num"><strong>{usd(235200+753600+62400)}</strong></td>
      </tr>
    </tbody>
  </table>
  </div>

  <div class="cn">
    <strong>Operating Note:</strong> The asset is being acquired with <strong>~58% in-place occupancy</strong>, the residual state from an abandoned receiver-led strategy to fully vacate the property in advance of a direct sale to UCLA (subsequently abandoned due to tenant buy-out regulations). Re-leasing to stabilization is the central operating task in months 0-12. Category Company's portfolio velocity of 1-3 leases per week on comparable West LA co-living assets supports a ~12-week path to stabilized occupancy.
  </div>

  <h3 class="sub-heading">Property Photos</h3>
  <div class="photo-grid">
    <div class="pg-item pg-hero">
      <img src="{EXTERIOR_IMG}" alt="1775 Beloit Avenue exterior">
      <div class="pg-caption">Building Exterior &middot; Beloit Avenue Frontage</div>
    </div>
    <div class="pg-item">
      <img src="{RENDERING_IMG}" alt="Architectural rendering">
      <div class="pg-caption">Architectural Concept &middot; ShubinDonaldson</div>
    </div>
    <div class="pg-item">
      <img src="{HERO_IMG}" alt="Rooftop terrace">
      <div class="pg-caption">Rooftop Deck &middot; Century City Views</div>
    </div>
    <div class="pg-item">
      <img src="{COLIVING_IMG}" alt="Co-living suite">
      <div class="pg-caption">Co-Living Junior Suite</div>
    </div>
    <div class="pg-item">
      <img src="{KITCHEN_IMG}" alt="Kitchen">
      <div class="pg-caption">Studio Kitchen &middot; Boutique Spec</div>
    </div>
    <div class="pg-item">
      <img src="{PATIO_IMG}" alt="Rooftop patio">
      <div class="pg-caption">Rooftop Lounge &middot; Amenity Deck</div>
    </div>
  </div>
</section>
"""

# ---- LOCATION ----
LOCATION = f"""
<section class="section section-alt" id="location">
  <p class="section-subtitle">Section IV</p>
  <h2 class="section-title">The Location</h2>
  <div class="section-divider"></div>

  <p>1775 Beloit Avenue sits one block off <strong>Sawtelle Boulevard</strong>, the spine of the Sawtelle Japantown district &mdash; one of West LA's densest and most-tenanted retail and dining corridors. The location benefits from immediate access to UCLA, the major employment centers of West LA (Century City, Westwood, Santa Monica), and a dense concentration of dining, retail, and neighborhood amenities. Together these support durable rental demand from young professionals, students, and workforce renters &mdash; the core tenant profile for co-living product.</p>

  <div id="map" class="leaflet-map"></div>
  <p class="map-fallback">Interactive map available in the web version of this presentation.</p>

  <div class="bench-grid">
    <div class="bench">
      <h5>UCLA Co-Living Acquisitions</h5>
      <div class="subj">Institutional Bid &middot; 2026</div>
      <div class="stat">$250,000</div>
      <div class="stat-l">per Bed</div>
      <p>UCLA has been an active acquirer of co-living assets, most recently at $250,000 per bed in 2026. Category's per-bed basis at 1775 Beloit ({usd(PPB_EXISTING)}) sits {pct(UCLA_DISCOUNT*100, 0)} below that institutional benchmark, providing both an exit reference and a margin-of-safety floor.</p>
    </div>
    <div class="bench">
      <h5>SW by CLG (California Landmark)</h5>
      <div class="subj">Two Blocks South &middot; New Construction</div>
      <div class="stat">$2,300+</div>
      <div class="stat-l">/ Mo on 375 SF Studios</div>
      <p>A newly constructed apartment building by California Landmark, two blocks south of 1775 Beloit, achieves in-place rents exceeding $2,300 per month on 375 SF micro-units. Co-living rooms at 1775 Beloit at ~$1,648 in place represent a ~28% discount to that new-construction studio benchmark.</p>
    </div>
    <div class="bench">
      <h5>Wilshire Margot (NMS Properties)</h5>
      <div class="subj">Westwood Conversion &middot; 2018</div>
      <div class="stat">$2,000+</div>
      <div class="stat-l">/ Bed Achieved</div>
      <p>The same developer (NMS Properties) successfully converted the Wilshire Margot in Westwood to co-living in 2018, achieving rents in excess of $2,000 per bed. This validates the West LA co-living rent ceiling well above the conservative $1,570 / bed underwriting at 1775 Beloit.</p>
    </div>
  </div>
</section>
"""

# ---- VALUE CREATION ----
VALUE_CREATION = f"""
<section class="section" id="value-creation">
  <p class="section-subtitle">Section V</p>
  <h2 class="section-title">Value Creation Plan</h2>
  <div class="section-divider"></div>

  <p>Three concurrent levers drive the path from in-place ~58% occupancy and bloated receiver opex to a stabilized {pct(CAP_ON_COST_UNTRENDED)} yield on cost within 12 to 18 months.</p>

  <div class="vc">
    <div class="vc-card">
      <div class="vc-num">01</div>
      <div class="vc-title">Operations</div>
      <p>Category Management assumes immediately upon close. Receiver payroll and vendor contracts &mdash; currently running at approximately <strong>3x Category's portfolio benchmark</strong> on properties twice the size &mdash; are replaced by Category's in-house platform. Leasing converts to by-the-bed; typical velocity of 1-3 leases per week on adjacent properties supports stabilized occupancy in ~12 weeks.</p>
    </div>
    <div class="vc-card">
      <div class="vc-num">02</div>
      <div class="vc-title">Density</div>
      <p>Two 1-bedroom ADUs are constructed on the ground floor using underutilized space, executed by Category's in-house construction capability for minimal additional basis. Each ADU generates ~$2,600 per month, contributing <strong>~$62,400 annually</strong> in incremental gross rent. Total unit count rises from 16 to 18, bed count from 48 to 50.</p>
    </div>
    <div class="vc-card">
      <div class="vc-num">03</div>
      <div class="vc-title">Capital Structure</div>
      <p>Acquisition financing of {money(ACQ_LOAN, 2)} @ {pct(ACQ_RATE)} IO is locked from RBB Bank (Prime - 50 bps, no prepay penalty, Sponsor PG). Upon stabilization, refinance into ~{pct(PERM_RATE)} IO permanent debt &mdash; the same execution Category secured on a comparable co-living refinance in March 2026. The refi is projected to return <strong>~50% of invested equity</strong> and lift stabilized cash-on-cash to ~{pct(COC_PERM_IO)}.</p>
    </div>
  </div>

  <div class="cn">
    <strong>Rent Upside Optionality:</strong> Category's base case underwrites <strong>$1,570 per bed</strong> &mdash; roughly $100 below the in-place average of $1,648. Category has recently leased co-living rooms in its existing portfolio for as high as <strong>$1,850 per month</strong>, a $280 delta above the base case. For sensitivity, each $100 / bed in achieved rent translates to approximately 50 basis points of additional untrended yield on cost and a ~20% lift to stabilized cash-on-cash.
  </div>
</section>
"""

# ---- SUBMARKET / SOURCE OF DISLOCATION ----
SUBMARKET_SECTION = f"""
<section class="section section-alt" id="submarket">
  <p class="section-subtitle">Section VI</p>
  <h2 class="section-title">Source of Dislocation</h2>
  <div class="section-divider"></div>

  <p>The acquisition basis at 1775 Beloit is the direct product of a stacked sequence of distress drivers, none of which are reflective of the asset's underlying quality or submarket fundamentals. Understanding the path the asset traveled to today's pricing is central to the underwriting case.</p>

  <h3 class="sub-heading">Distress Timeline</h3>
  <div class="ts">
  <table>
    <thead>
      <tr><th style="width:18%">Period</th><th>Event</th></tr>
    </thead>
    <tbody>
      <tr><td><strong>2019 - 2023</strong></td><td>NMS Properties develops the asset ground-up at a total cost basis of approximately {money(DEV_COST, 0)}, encouraged by the 2018 success of the Wilshire Margot co-living conversion in Westwood (achieving $2,000+/bed).</td></tr>
      <tr><td><strong>2023</strong></td><td>Building delivers into a materially changed capital market. Lease-up cannot support the cost basis or associated debt service at then-prevailing rates.</td></tr>
      <tr><td><strong>2024</strong></td><td>Original construction lender (First Choice Bank) becomes insolvent. Debt assets &mdash; including the $16M note on 1775 Beloit &mdash; are sold to Enterprise Bank &amp; Trust, an out-of-state acquirer with limited LA exposure.</td></tr>
      <tr><td><strong>2024 - 2025</strong></td><td>The developer of the asset passes away. Enterprise Bank places the property into receivership.</td></tr>
      <tr><td><strong>2025</strong></td><td>Prior to broad marketing, Enterprise pursues a direct sale to UCLA (active co-living acquirer at $250K / bed). The receiver begins vacating the building to enable a vacant-sale transaction.</td></tr>
      <tr><td><strong>2025 - 2026</strong></td><td>Vacate strategy abandoned due to LA tenant buy-out regulations. Asset left at <strong>~58% occupancy</strong> with bloated receiver opex. Direct UCLA path collapses; broad marketing initiated.</td></tr>
      <tr><td><strong>2026 Q1</strong></td><td>Asset has no stabilized operating history; can't be priced on a cap-rate basis. Concurrently, Enterprise is navigating larger distressed positions from the First Choice acquisition &mdash; 1775 Beloit becomes a non-core resolution priority.</td></tr>
      <tr><td><strong>2026 Q2</strong></td><td>Category submits an aggressive 5-day diligence offer leveraging in-house product expertise. Initial contract via deed-in-lieu. During diligence, Category identifies a previously undisclosed <strong>$45M second-position note</strong> the lender itself was unaware of. Category re-trades the price and requires foreclosure prior to closing &mdash; delivering clean title and eliminating successor liability.</td></tr>
    </tbody>
  </table>
  </div>

  <div class="cn">
    <strong>The acquisition price is not a function of submarket weakness.</strong> It is the price at which an out-of-state, capacity-constrained workout group resolved a non-core distressed position into the hands of a specialist operator who could close on accelerated terms. New construction Sawtelle / Westwood comparables continue to lease at $2,300+ per studio and $2,000+ per co-living bed.
  </div>
</section>
"""

# ---- FINANCIALS ----
income_rows_html = ""
for label, val in INCOME_ITEMS:
    val_str = f"({usd(abs(val))})" if val < 0 else usd(val)
    income_rows_html += f'<tr><td>{label}</td><td class="num">{val_str}</td></tr>'
income_rows_html += f'<tr class="subtotal"><td><strong>Gross Potential Rent</strong></td><td class="num"><strong>{usd(GPR)}</strong></td></tr>'
income_rows_html += f'<tr><td>Less Vacancy / Collection Loss ({VACANCY_PCT}%)</td><td class="num">({usd(VACANCY_AMT)})</td></tr>'
income_rows_html += f'<tr class="subtotal"><td><strong>Effective Gross Income</strong></td><td class="num"><strong>{usd(GPR-VACANCY_AMT)}</strong></td></tr>'

exp_rows_html = ""
for label, basis, val in EXPENSE_ITEMS:
    exp_rows_html += f'<tr><td>{label}</td><td>{basis}</td><td class="num">{usd(val)}</td></tr>'
exp_rows_html += f'<tr class="subtotal"><td><strong>Total Operating Expenses</strong></td><td><strong>{OPEX_PCT}% of EGI &middot; {usd(OPEX_PER_BED_MO)} / bed / mo</strong></td><td class="num"><strong>{usd(TOTAL_OPEX)}</strong></td></tr>'

FINANCIALS = f"""
<section class="section" id="financials">
  <p class="section-subtitle">Section VII</p>
  <h2 class="section-title">Financial Summary</h2>
  <div class="section-divider"></div>

  <div class="mg4">
    <div class="metric-card"><span class="metric-value">{usd(NOI)}</span><span class="metric-label">Stabilized NOI</span></div>
    <div class="metric-card"><span class="metric-value">{pct(CAP_ON_COST_UNTRENDED)}</span><span class="metric-label">Untrended Yield on Cost</span></div>
    <div class="metric-card"><span class="metric-value">{pct(CAP_ON_COST_TRENDED)}</span><span class="metric-label">Trended YoC (3-Year)</span></div>
    <div class="metric-card"><span class="metric-value">{pct(COC_PERM_IO)}</span><span class="metric-label">Stab. CoC (Perm IO)</span></div>
  </div>

  <h3 class="sub-heading">Acquisition Basis Sensitivity</h3>
  <p>The headline acquisition price of {money(ACQ_PRICE, 2)} reflects the negotiated purchase contract. The County of Los Angeles tax assessor base, however, is being set at {money(ALT_PRICE, 2)} per a separate stipulation negotiated with the seller (a meaningful annual property-tax savings reflected in the pro forma). The matrix below shows key acquisition metrics at both basis points.</p>
  <div class="sens-grid">
    <div class="sens-col headline">
      <div class="sens-label">Headline Purchase Basis</div>
      <div class="sens-price">{money(ACQ_PRICE, 2)}</div>
      <div class="sens-sub">Contract purchase price</div>
      <div class="sens-rows">
        <div class="sens-row"><span class="k">$ / Bed (48 existing)</span><span class="v">{usd(BASE["ppb_existing"])}</span></div>
        <div class="sens-row"><span class="k">$ / Bed (50 with ADU)</span><span class="v">{usd(BASE["ppb_w_adu"])}</span></div>
        <div class="sens-row"><span class="k">$ / Unit (16 existing)</span><span class="v">{usd(BASE["ppu_existing"])}</span></div>
        <div class="sens-row"><span class="k">$ / SF Rentable</span><span class="v">${BASE["psf_rent"]:.0f}</span></div>
        <div class="sens-row"><span class="k">$ / SF Gross</span><span class="v">${BASE["psf_gross"]:.0f}</span></div>
        <div class="sens-row"><span class="k">Discount to Replacement Cost</span><span class="v">{pct(BASE["disc_repl"]*100, 0)}</span></div>
        <div class="sens-row"><span class="k">Discount to UCLA $250K / Bed</span><span class="v">{pct(UCLA_DISCOUNT*100, 0)}</span></div>
        <div class="sens-row"><span class="k">Cap Rate on Price</span><span class="v">{pct(BASE["cap_on_price"]*100)}</span></div>
        <div class="sens-row"><span class="k">Untrended YoC (Acq Loan)</span><span class="v">{pct(BASE["yoc_acq"]*100)}</span></div>
        <div class="sens-row"><span class="k">Untrended YoC (Perm Loan)</span><span class="v">{pct(BASE["yoc_perm"]*100)}</span></div>
      </div>
    </div>
    <div class="sens-col alt">
      <div class="sens-label">Effective Tax Basis</div>
      <div class="sens-price">{money(ALT_PRICE, 2)}</div>
      <div class="sens-sub">Property tax basis per seller stipulation</div>
      <div class="sens-rows">
        <div class="sens-row"><span class="k">$ / Bed (48 existing)</span><span class="v">{usd(ALT["ppb_existing"])}</span></div>
        <div class="sens-row"><span class="k">$ / Bed (50 with ADU)</span><span class="v">{usd(ALT["ppb_w_adu"])}</span></div>
        <div class="sens-row"><span class="k">$ / Unit (16 existing)</span><span class="v">{usd(ALT["ppu_existing"])}</span></div>
        <div class="sens-row"><span class="k">$ / SF Rentable</span><span class="v">${ALT["psf_rent"]:.0f}</span></div>
        <div class="sens-row"><span class="k">$ / SF Gross</span><span class="v">${ALT["psf_gross"]:.0f}</span></div>
        <div class="sens-row"><span class="k">Discount to Replacement Cost</span><span class="v">{pct(ALT["disc_repl"]*100, 0)}</span></div>
        <div class="sens-row"><span class="k">Discount to UCLA $250K / Bed</span><span class="v">{pct(UCLA_DISCOUNT_ALT*100, 0)}</span></div>
        <div class="sens-row"><span class="k">Cap Rate on Price</span><span class="v">{pct(ALT["cap_on_price"]*100)}</span></div>
        <div class="sens-row"><span class="k">Untrended YoC (Acq Loan)</span><span class="v">{pct(ALT["yoc_acq"]*100)}</span></div>
        <div class="sens-row"><span class="k">Untrended YoC (Perm Loan)</span><span class="v">{pct(ALT["yoc_perm"]*100)}</span></div>
      </div>
    </div>
  </div>

  <h3 class="sub-heading">Sources &amp; Uses</h3>
  <div class="ts">
  <table>
    <thead>
      <tr><th>Item</th><th class="num">Acquisition Loan</th><th class="num">Permanent Loan</th></tr>
    </thead>
    <tbody>
      <tr><td>Purchase Price</td><td class="num">{usd(ACQ_PRICE)}</td><td class="num">{usd(ACQ_PRICE)}</td></tr>
      <tr><td>Acquisition Fee (1.25%)</td><td class="num">$107,813</td><td class="num">&mdash;</td></tr>
      <tr><td>Working Capital (Closing, Lease-Up)</td><td class="num">$140,725</td><td class="num">&mdash;</td></tr>
      <tr><td>FFE &amp; Misc Improvements</td><td class="num">$50,000</td><td class="num">&mdash;</td></tr>
      <tr><td>ADU Hard &amp; Soft Costs</td><td class="num">$396,000</td><td class="num">&mdash;</td></tr>
      <tr><td>Financing &amp; Closing Fees</td><td class="num">$112,125</td><td class="num">$65,000</td></tr>
      <tr class="subtotal"><td><strong>Total Project Budget</strong></td><td class="num"><strong>{usd(TOTAL_BUDGET_ACQ)}</strong></td><td class="num"><strong>{usd(TOTAL_BUDGET_PERM)}</strong></td></tr>
      <tr><td>Loan Amount</td><td class="num">{usd(ACQ_LOAN)}</td><td class="num">{usd(PERM_LOAN)}</td></tr>
      <tr><td>Rate (Interest-Only)</td><td class="num">{pct(ACQ_RATE)}</td><td class="num">{pct(PERM_RATE)}</td></tr>
      <tr><td>Annual Debt Service (IO)</td><td class="num">{usd(DS_ACQ_IO)}</td><td class="num">{usd(DS_PERM_IO)}</td></tr>
      <tr><td>Cash Flow After Debt Service (IO)</td><td class="num">{usd(CFDS_ACQ_IO)}</td><td class="num">{usd(CFDS_PERM_IO)}</td></tr>
      <tr class="hl"><td><strong>Peak Equity Required</strong></td><td class="num"><strong>{usd(PEAK_EQUITY_ACQ)}</strong></td><td class="num"><strong>{usd(PEAK_EQUITY_PERM)}</strong></td></tr>
      <tr class="hl"><td><strong>Stabilized Cash-on-Cash (IO)</strong></td><td class="num"><strong>{pct(COC_ACQ_IO)}</strong></td><td class="num"><strong>{pct(COC_PERM_IO)}</strong></td></tr>
      <tr><td>Stabilized Cash-on-Cash (P&amp;I)</td><td class="num">{pct(COC_ACQ_PI)}</td><td class="num">{pct(COC_PERM_PI)}</td></tr>
      <tr><td>DSCR (P&amp;I)</td><td class="num">{DSCR_ACQ_PI}x</td><td class="num">{DSCR_PERM_PI}x</td></tr>
    </tbody>
  </table>
  </div>

  <h3 class="sub-heading">Stabilized Operating Pro Forma</h3>
  <div class="ts">
  <table>
    <thead><tr><th>Income</th><th class="num">Annual</th></tr></thead>
    <tbody>
      {income_rows_html}
    </tbody>
  </table>
  </div>

  <div class="ts">
  <table>
    <thead><tr><th>Operating Expense</th><th>Basis</th><th class="num">Annual</th></tr></thead>
    <tbody>
      {exp_rows_html}
    </tbody>
  </table>
  </div>

  <div class="ts">
  <table>
    <tbody>
      <tr class="totalrow"><td style="padding:14px 12px;">NET OPERATING INCOME (Stabilized)</td><td class="num" style="padding:14px 12px; font-size:18px;">{usd(NOI)}</td></tr>
    </tbody>
  </table>
  </div>

  <div class="cn">
    <strong>Pro Forma Basis:</strong> Stabilized year-1 figures reflect the asset operating at occupancy on the 18-unit / 50-bed footprint following the two-ADU buildout. The rent assumption of $1,570 / bed sits approximately $100 below the in-place average of $1,648 per bed. Property taxes are modeled at 1.11% of an assessed value of $7.9M, reflecting a negotiated re-assessment basis with the seller. The 2.50% management fee reflects Category's in-house property management economics; a third-party benchmark for a comparable LA co-living asset would underwrite ~4.0% of GSR.
  </div>
</section>
"""

# ---- FOOTER / CONTACT ----
FOOTER = f"""
<section class="footer" id="contact">
  <img src="{LOGO_WHITE}" class="footer-logo" alt="LAAA Team">
  <div class="footer-team">
    <div class="fp">
      <img src="{GLEN_IMG}" class="footer-headshot" alt="Glen Scher">
      <div class="footer-name">Glen Scher</div>
      <div class="footer-title">Senior Managing Director of Investments</div>
      <div class="footer-contact">
        (818) 212-2808<br>
        <a href="mailto:Glen.Scher@marcusmillichap.com">Glen.Scher@marcusmillichap.com</a><br>
        CA License 01962976
      </div>
    </div>
    <div class="fp">
      <img src="{FILIP_IMG}" class="footer-headshot" alt="Filip Niculete">
      <div class="footer-name">Filip Niculete</div>
      <div class="footer-title">Senior Managing Director of Investments</div>
      <div class="footer-contact">
        (818) 212-2748<br>
        <a href="mailto:Filip.Niculete@marcusmillichap.com">Filip.Niculete@marcusmillichap.com</a><br>
        CA License 01905352
      </div>
    </div>
  </div>
  <div class="footer-office">
    LAAA Team at Marcus &amp; Millichap &middot; 16830 Ventura Blvd, Ste. 100, Encino, CA 91436<br>
    <a href="https://marcusmillichap.com/laaa-team">marcusmillichap.com/laaa-team</a>
  </div>
  <div class="footer-disclaimer">
    This information has been secured from sources we believe to be reliable, but we make no representations or warranties, expressed or implied, as to the accuracy of the information. Recipient must verify the information and bears all risk for any inaccuracies. Projections, opinions, assumptions, and estimates are for illustrative purposes only and do not represent the current or future performance of the property. Marcus &amp; Millichap Real Estate Investment Services, Inc. &middot; License: CA 01930580.
  </div>
</section>
"""

DOWNLOAD = """
<button class="download-btn" onclick="window.print()" title="Download as PDF">
  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="7 10 12 15 17 10"/><line x1="12" y1="15" x2="12" y2="3"/></svg>
  <span>Download PDF</span>
</button>
"""

JS = f"""
<script>
// Client personalization via ?client= URL parameter
(function() {{
  var params = new URLSearchParams(window.location.search);
  var client = params.get('client');
  if (client) {{
    var el = document.getElementById('client-greeting');
    if (el) el.textContent = 'Prepared Exclusively for ' + client;
  }}
}})();

// Smooth scroll for TOC
document.querySelectorAll('.toc-nav a').forEach(function(link) {{
  link.addEventListener('click', function(e) {{
    e.preventDefault();
    var target = document.querySelector(this.getAttribute('href'));
    if (target) {{
      var navHeight = document.getElementById('toc-nav').offsetHeight;
      var targetPos = target.getBoundingClientRect().top + window.pageYOffset - navHeight - 4;
      window.scrollTo({{ top: targetPos, behavior: 'smooth' }});
    }}
  }});
}});

// Active TOC link on scroll
(function() {{
  var tocLinks = document.querySelectorAll('.toc-nav a');
  var tocSections = [];
  tocLinks.forEach(function(link) {{
    var id = link.getAttribute('href').substring(1);
    var section = document.getElementById(id);
    if (section) tocSections.push({{ link: link, section: section }});
  }});
  function update() {{
    var navHeight = document.getElementById('toc-nav').offsetHeight + 20;
    var scrollPos = window.pageYOffset + navHeight;
    var current = null;
    tocSections.forEach(function(item) {{
      if (item.section.offsetTop <= scrollPos) current = item.link;
    }});
    tocLinks.forEach(function(link) {{ link.classList.remove('toc-active'); }});
    if (current) current.classList.add('toc-active');
  }}
  window.addEventListener('scroll', update);
  update();
}})();

// Leaflet map: subject property pin
window.addEventListener('DOMContentLoaded', function() {{
  if (typeof L === 'undefined') return;
  var map = L.map('map', {{ scrollWheelZoom: false }}).setView([{LAT}, {LNG}], 16);
  L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
    attribution: '&copy; OpenStreetMap',
    maxZoom: 19
  }}).addTo(map);
  var icon = L.divIcon({{
    className: 'subject-marker',
    html: '<div style="width:32px;height:32px;border-radius:50%;background:#C5A258;border:3px solid #fff;box-shadow:0 2px 8px rgba(0,0,0,0.4);display:flex;align-items:center;justify-content:center;color:#fff;font-weight:700;">★</div>',
    iconSize: [32, 32],
    iconAnchor: [16, 16]
  }});
  L.marker([{LAT}, {LNG}], {{ icon: icon }}).addTo(map)
    .bindPopup('<strong>1775 Beloit Avenue</strong><br>West Los Angeles, CA 90025<br>Sawtelle / Japantown');
}});
</script>
</body>
</html>
"""

HTML = HEAD + COVER + TOC + OVERVIEW + HIGHLIGHTS_SECTION + ASSET + LOCATION + VALUE_CREATION + SUBMARKET_SECTION + FINANCIALS + FOOTER + DOWNLOAD + JS

with open(OUTPUT, "w", encoding="utf-8") as f:
    f.write(HTML)

size_kb = os.path.getsize(OUTPUT) // 1024
print(f"\nBuilt: {OUTPUT}")
print(f"Size:  {size_kb} KB")
print("Done.")
