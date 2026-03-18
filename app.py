"""
Ohio Supreme Court — Roll of Attorneys
Lawyer lookup tool.

Run with:
    streamlit run app.py

Expects all_attorneys_normalized.csv in the same directory,
OR set DATA_PATH below to the full path.
"""

import os
import streamlit as st
import pandas as pd

# ── CONFIG ────────────────────────────────────────────────────────────────────

DATA_PATH = os.path.join(
    os.path.dirname(__file__),
    "all_attorneys_normalized.csv"
)

st.set_page_config(
    page_title="Ohio Roll of Attorneys",
    page_icon="⚖️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── STYLES ────────────────────────────────────────────────────────────────────
#
# Palette:
#   #141414  page background
#   #1d1d1d  sidebar, card background
#   #252525  card hover, input background
#   #333333  borders
#   #4a4a4a  muted borders
#   #707070  secondary / muted text
#   #b0b0b0  body text
#   #e8e8e8  primary text
#   #f5f5f5  headings / names

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;1,400&family=Source+Serif+4:ital,opsz,wght@0,8..60,300;0,8..60,400;1,8..60,300&display=swap');

html, body, [class*="css"] {
    font-family: 'Source Serif 4', Georgia, serif;
    color: #b0b0b0;
}

.stApp {
    background-color: #141414;
}

/* ── Header ── */
.app-header {
    text-align: center;
    padding: 2.5rem 1rem 1rem;
    border-bottom: 1px solid #333333;
    margin-bottom: 2rem;
}
.app-header h1 {
    font-family: 'Playfair Display', Georgia, serif;
    font-size: 2.6rem;
    font-weight: 700;
    color: #f5f5f5;
    letter-spacing: 0.02em;
    margin: 0 0 0.3rem;
    line-height: 1.15;
}
.app-header .subtitle {
    font-size: 0.9rem;
    font-weight: 300;
    font-style: italic;
    color: #707070;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.app-header .rule {
    width: 40px;
    height: 1px;
    background: #4a4a4a;
    margin: 1rem auto 0.5rem;
}

/* ── About block ── */
.about-block {
    background: #1d1d1d;
    border: 1px solid #333333;
    border-radius: 2px;
    padding: 1.4rem 1.8rem;
    margin-bottom: 2rem;
    display: flex;
    gap: 3rem;
    flex-wrap: wrap;
}
.about-intro {
    flex: 2;
    min-width: 220px;
}
.about-intro p {
    font-size: 0.88rem;
    color: #707070;
    line-height: 1.8;
    margin: 0;
    font-style: italic;
}
.about-fields {
    flex: 3;
    min-width: 280px;
    display: flex;
    flex-wrap: wrap;
    gap: 0.8rem 2.5rem;
    align-content: flex-start;
}
.field-item {
    min-width: 180px;
}
.field-name {
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #b0b0b0;
    margin-bottom: 0.15rem;
}
.field-desc {
    font-size: 0.82rem;
    color: #4a4a4a;
    line-height: 1.5;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background-color: #1d1d1d;
    border-right: 1px solid #333333;
}
[data-testid="stSidebar"] .sidebar-label {
    font-family: 'Playfair Display', serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #707070;
    margin-bottom: 0.3rem;
}
[data-testid="stSidebar"] [data-testid="stTextInput"] input {
    border: 1px solid #333333 !important;
    border-radius: 2px;
    background: #252525 !important;
    color: #e8e8e8 !important;
    font-family: 'Source Serif 4', serif;
    font-size: 0.95rem;
}
[data-testid="stSidebar"] [data-testid="stTextInput"] input:focus {
    border-color: #b0b0b0 !important;
    box-shadow: 0 0 0 2px rgba(176,176,176,0.12) !important;
}

/* ── Results meta ── */
.result-meta {
    font-size: 0.85rem;
    font-style: italic;
    color: #707070;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #333333;
}

/* ── Record card ── */
.record-card {
    background: #1d1d1d;
    border: 1px solid #333333;
    border-left: 3px solid #4a4a4a;
    border-radius: 2px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.6rem;
    transition: border-left-color 0.15s ease, background 0.15s ease;
}
.record-card:hover {
    border-left-color: #e8e8e8;
    background: #252525;
}
.record-name {
    font-family: 'Playfair Display', serif;
    font-size: 1.1rem;
    font-weight: 700;
    color: #f5f5f5;
    margin-bottom: 0.25rem;
}
.record-meta {
    font-size: 0.88rem;
    color: #b0b0b0;
    line-height: 1.7;
}
.record-meta .label {
    font-style: italic;
    color: #707070;
    margin-right: 0.3rem;
}
.record-meta .field {
    margin-right: 1.5rem;
}
.record-note {
    margin-top: 0.55rem;
    padding: 0.4rem 0.75rem;
    background: #252525;
    border-left: 2px solid #4a4a4a;
    font-size: 0.85rem;
    font-style: italic;
    color: #b0b0b0;
    border-radius: 1px;
}
.record-source {
    display: inline-block;
    font-size: 0.7rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #707070;
    border: 1px solid #333333;
    padding: 0.12rem 0.5rem;
    border-radius: 1px;
    margin-top: 0.5rem;
}
.orig-label {
    opacity: 0.45;
    font-size: 0.82em;
}

/* ── No results ── */
.no-results {
    text-align: center;
    padding: 3rem 1rem;
    color: #707070;
    font-style: italic;
}
.no-results .icon { font-size: 2rem; margin-bottom: 0.5rem; }

/* ── Export button ── */
[data-testid="stDownloadButton"] button {
    background-color: #1d1d1d !important;
    color: #e8e8e8 !important;
    border: 1px solid #4a4a4a !important;
    border-radius: 2px !important;
    font-family: 'Source Serif 4', serif !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.04em !important;
}
[data-testid="stDownloadButton"] button:hover {
    background-color: #333333 !important;
    border-color: #b0b0b0 !important;
}

/* ── Selectbox ── */
[data-testid="stSelectbox"] > div > div {
    border-color: #333333 !important;
    background: #252525 !important;
    border-radius: 2px !important;
    color: #e8e8e8 !important;
}

/* ── Checkbox ── */
[data-testid="stCheckbox"] label p {
    font-size: 0.88rem !important;
    color: #b0b0b0 !important;
}

/* ── Slider ── */
[data-testid="stSlider"] [data-testid="stThumbValue"] {
    color: #e8e8e8 !important;
}

/* ── Info box ── */
[data-testid="stAlert"] {
    background-color: #1d1d1d !important;
    border-color: #333333 !important;
    color: #b0b0b0 !important;
}

hr { border-color: #333333; }
</style>
""", unsafe_allow_html=True)

# ── DATA ──────────────────────────────────────────────────────────────────────

@st.cache_data
def load_data(path):
    df = pd.read_csv(path, dtype=str).fillna("")
    df["Year_int"] = pd.to_numeric(df["Year"], errors="coerce")
    return df

df = load_data(DATA_PATH)

valid_years = df["Year_int"].dropna().astype(int)
YEAR_MIN = int(valid_years.min())
YEAR_MAX = int(valid_years.max())
all_cities = sorted(df["Residence"].replace("", pd.NA).dropna().unique())

# ── HEADER ───────────────────────────────────────────────────────────────────

st.markdown("""
<div class="app-header">
    <div class="subtitle">Supreme Court of Ohio</div>
    <h1>Roll of Attorneys</h1>
    <div class="rule"></div>
    <div class="subtitle">Lawyer Lookup</div>
</div>
""", unsafe_allow_html=True)

# ── ABOUT BLOCK ───────────────────────────────────────────────────────────────

st.markdown("""
<div class="about-block">
    <div class="about-intro">
        <p>
            This tool searches the Ohio Supreme Court Roll of Attorneys,
            transcribed from the original admission ledgers. Records span
            1917&ndash;1971 across two ledger books. Use the filters on the
            left to search by name, city, or year of admission. Results can
            be exported as a CSV for further research.
        </p>
    </div>
    <div class="about-fields">
        <div class="field-item">
            <div class="field-name">Name</div>
            <div class="field-desc">Attorney name as recorded in the ledger at time of admission.</div>
        </div>
        <div class="field-item">
            <div class="field-name">Admitted</div>
            <div class="field-desc">Date the attorney was admitted to the Ohio bar.</div>
        </div>
        <div class="field-item">
            <div class="field-name">Residence</div>
            <div class="field-desc">City of residence at time of admission, normalized from the original transcription.</div>
        </div>
        <div class="field-item">
            <div class="field-name">As written</div>
            <div class="field-desc">Original transcribed value when it differs from the normalized city name.</div>
        </div>
        <div class="field-item">
            <div class="field-name">Notes</div>
            <div class="field-desc">Archival annotations from the ledger — disbarments, restorations, transfers, and other remarks.</div>
        </div>
        <div class="field-item">
            <div class="field-name">Source</div>
            <div class="field-desc">Which ledger book the record was transcribed from (Book 4 or Book 5).</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ── SIDEBAR FILTERS ───────────────────────────────────────────────────────────

with st.sidebar:
    st.markdown("### Search & Filter")
    st.markdown("---")

    st.markdown('<div class="sidebar-label">Name</div>', unsafe_allow_html=True)
    name_query = st.text_input(
        "Name", label_visibility="collapsed",
        placeholder="e.g. Anderson, Charles..."
    )

    st.markdown("")
    st.markdown('<div class="sidebar-label">City / Residence</div>', unsafe_allow_html=True)
    city_options = ["— Any city —"] + all_cities
    city_select = st.selectbox("City", city_options, label_visibility="collapsed")

    st.markdown("")
    st.markdown('<div class="sidebar-label">Year of Admission</div>', unsafe_allow_html=True)
    use_year_filter = st.checkbox("Filter by year range", value=False)
    if use_year_filter:
        year_range = st.slider(
            "Year range", YEAR_MIN, YEAR_MAX,
            (YEAR_MIN, YEAR_MAX), step=1,
            label_visibility="collapsed"
        )
    else:
        year_range = (YEAR_MIN, YEAR_MAX)

    st.markdown("")
    st.markdown('<div class="sidebar-label">Source</div>', unsafe_allow_html=True)
    source_select = st.selectbox(
        "Source", ["Both books", "Book 4 only", "Book 5 only"],
        label_visibility="collapsed"
    )

    st.markdown("")
    notes_only = st.checkbox("Only records with notes", value=False)

    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.78rem;color:#4a4a4a;font-style:italic;">'
        + str(len(df)) + ' total records &middot; Book 4 &amp; Book 5'
        + '</div>',
        unsafe_allow_html=True
    )

# ── FILTERING ─────────────────────────────────────────────────────────────────

results = df.copy()

if name_query.strip():
    q = name_query.strip().lower()
    results = results[results["Name"].str.lower().str.contains(q, na=False)]

if city_select != "— Any city —":
    results = results[results["Residence"] == city_select]

if use_year_filter:
    results = results[
        (results["Year_int"] >= year_range[0]) &
        (results["Year_int"] <= year_range[1])
    ]

if source_select == "Book 4 only":
    results = results[results["Source"] == "Book 4"]
elif source_select == "Book 5 only":
    results = results[results["Source"] == "Book 5"]

if notes_only:
    results = results[results["Notes"] != ""]

# ── RESULTS HEADER + EXPORT ───────────────────────────────────────────────────

count = len(results)
col_results, col_export = st.columns([6, 1])

with col_results:
    any_filter = name_query or city_select != "— Any city —" or use_year_filter or notes_only
    if any_filter:
        plural = "s" if count != 1 else ""
        result_text = "No records found" if count == 0 else str(count) + " record" + plural + " found"
    else:
        result_text = "Showing all " + str(count) + " records — use the filters to search."
    st.markdown('<div class="result-meta">' + result_text + '</div>', unsafe_allow_html=True)

with col_export:
    if count > 0:
        export_cols = ["Name", "Date of Admission", "Year", "Residence",
                       "Residence_Original", "Notes", "Source"]
        csv_bytes = results[export_cols].to_csv(index=False).encode("utf-8")
        st.download_button(
            label="Export CSV",
            data=csv_bytes,
            file_name="attorneys_results.csv",
            mime="text/csv",
        )

# ── RECORD DISPLAY ────────────────────────────────────────────────────────────

MAX_DISPLAY = 500

if count == 0:
    st.markdown(
        '<div class="no-results">'
        '<div class="icon">&#9878;</div>'
        '<div>No records match your search.</div>'
        '<div style="font-size:0.8rem;margin-top:0.3rem;">'
        'Try broadening the name search or adjusting the filters.'
        '</div></div>',
        unsafe_allow_html=True
    )
else:
    if count > MAX_DISPLAY:
        st.info(
            "Showing the first " + str(MAX_DISPLAY) + " of " + str(count) + " results. "
            "Refine your search or use Export CSV to get the full set."
        )

    for _, row in results.head(MAX_DISPLAY).iterrows():
        name      = row["Name"]              or "—"
        date      = row["Date of Admission"] or "—"
        city      = row["Residence"]         or row["Residence_Original"] or "—"
        city_orig = row["Residence_Original"]
        notes     = row["Notes"]
        source    = row["Source"]

        if city_orig and city_orig != city and city_orig.lower() not in city.lower():
            city_display = city + ' <span class="orig-label">(as written: ' + city_orig + ')</span>'
        else:
            city_display = city

        note_block = ""
        if notes:
            note_block = '<div class="record-note">&#128221; ' + notes + '</div>'

        card = (
            '<div class="record-card">'
              '<div class="record-name">' + name + '</div>'
              '<div class="record-meta">'
                '<span class="field"><span class="label">Admitted</span>' + date + '</span>'
                '<span class="field"><span class="label">Residence</span>' + city_display + '</span>'
              '</div>'
              + note_block +
              '<div><span class="record-source">' + source + '</span></div>'
            '</div>'
        )

        st.markdown(card, unsafe_allow_html=True)
