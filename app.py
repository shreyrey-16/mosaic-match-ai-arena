
"""MOSAIC MATCH // CYBERPUNK AI ARENA
Run with: streamlit run app.py
"""

import pandas as pd
import streamlit as st
import altair as alt
from PIL import Image, ImageOps

from game import list_images, make_round
from ai_player import AIPlayer


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MOSAIC MATCH // AI ARENA",
    page_icon="🧩",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# CYBERPUNK STYLING
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;500;600;700;800;900&family=Rajdhani:wght@400;500;600;700&display=swap');

:root {
    --cyan:#00f5ff;
    --purple:#a855f7;
    --pink:#ff3cac;
    --green:#39ff88;
    --red:#ff4569;
    --muted:#9aa8c7;
}

.stApp {
    background:
      radial-gradient(ellipse at 8% 0%,rgba(0,245,255,.08),transparent 32%),
      radial-gradient(ellipse at 92% 8%,rgba(168,85,247,.12),transparent 34%),
      linear-gradient(145deg,#070914,#0b1020 55%,#080914);
    color:#edf8ff;
    font-family:'Rajdhani',sans-serif;
}

[data-testid="stHeader"] {
    background:rgba(7,9,20,.75);
}

[data-testid="stSidebar"] {
    background:linear-gradient(180deg,#101426,#090c19);
    border-right:1px solid rgba(0,245,255,.25);
}

[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
h1,h2,h3 {
    font-family:'Orbitron',sans-serif !important;
    color:#edf8ff;
}

.block-container {
    max-width:1500px;
    padding-top:1rem;
    padding-bottom:2rem;
}

p,label,li {
    font-family:'Rajdhani',sans-serif;
}

hr {
    border-color:rgba(0,245,255,.18) !important;
}

[data-testid="stAppViewContainer"]:before {
    content:"";
    position:fixed;
    inset:0;
    pointer-events:none;
    z-index:0;
    opacity:.08;
    background-image:
      linear-gradient(rgba(0,245,255,.13) 1px,transparent 1px),
      linear-gradient(90deg,rgba(0,245,255,.13) 1px,transparent 1px);
    background-size:42px 42px;
    animation:gridDrift 18s linear infinite;
}

@keyframes gridDrift {
    from {background-position:0 0}
    to {background-position:42px 42px}
}

@keyframes neonGlow {
    0%,100% {
        text-shadow:0 0 9px rgba(0,245,255,.35);
    }
    50% {
        text-shadow:0 0 22px rgba(0,245,255,.75),
                    0 0 32px rgba(168,85,247,.35);
    }
}

@keyframes fadeIn {
    from {opacity:0;transform:translateY(8px)}
    to {opacity:1;transform:translateY(0)}
}

.mm-hero {
    padding:1.15rem 1.5rem;
    margin-bottom:1rem;
    border:1px solid rgba(0,245,255,.34);
    border-radius:16px;
    background:linear-gradient(110deg,
      rgba(0,245,255,.06),
      rgba(168,85,247,.12),
      rgba(255,60,172,.03));
    animation:fadeIn .5s ease-out;
}

.mm-kicker {
    color:var(--cyan);
    font-family:'Orbitron',sans-serif;
    font-size:.64rem;
    font-weight:700;
    letter-spacing:.18em;
    margin-bottom:.4rem;
}

.mm-title {
    font-family:'Orbitron',sans-serif;
    font-size:clamp(1.8rem,4vw,3.1rem);
    font-weight:900;
    line-height:1.1;
    letter-spacing:-.035em;
    animation:neonGlow 4s ease-in-out infinite;
}

.mm-title span {
    color:var(--cyan);
}

.mm-subtitle {
    margin-top:.5rem;
    color:#b8c7e4;
    font-size:1rem;
}

.mm-status {
    display:inline-flex;
    align-items:center;
    gap:7px;
    margin-top:.65rem;
    padding:5px 10px;
    border:1px solid rgba(57,255,136,.3);
    border-radius:30px;
    color:var(--green);
    font-family:'Orbitron',sans-serif;
    font-size:.59rem;
}

.mm-dot {
    width:7px;
    height:7px;
    border-radius:50%;
    background:var(--green);
    box-shadow:0 0 9px var(--green);
}

.mm-panel {
    padding:.8rem;
    border:1px solid rgba(0,245,255,.22);
    border-radius:13px;
    background:linear-gradient(145deg,#11172b,#0a0e1d);
}

.mm-panel-title {
    color:var(--cyan);
    font-family:'Orbitron',sans-serif;
    font-size:.75rem;
    letter-spacing:.08em;
    margin-bottom:.5rem;
}

.mm-target {
    padding:.7rem;
    border:1px solid rgba(168,85,247,.65);
    border-radius:14px;
    background:rgba(168,85,247,.07);
    box-shadow:0 0 18px rgba(168,85,247,.09);
}

.mm-target-label {
    margin-bottom:.55rem;
    color:#d6a7ff;
    font-family:'Orbitron',sans-serif;
    font-size:.7rem;
    letter-spacing:.08em;
}

.mm-muted {
    color:var(--muted);
    font-size:.85rem;
}

[data-testid="stMetric"] {
    padding:10px 13px;
    border:1px solid rgba(0,245,255,.2);
    border-radius:12px;
    background:rgba(16,23,43,.92);
}

[data-testid="stMetricLabel"] {
    color:#a7badb !important;
    font-family:'Orbitron',sans-serif !important;
    font-size:.62rem !important;
}

[data-testid="stMetricValue"] {
    color:var(--cyan) !important;
    font-family:'Orbitron',sans-serif !important;
}

.stButton>button {
    width:100%;
    min-height:2.35rem;
    border:1px solid rgba(0,245,255,.38);
    border-radius:9px;
    background:linear-gradient(105deg,
      rgba(0,245,255,.06),rgba(168,85,247,.1));
    color:#eafaff;
    font-family:'Orbitron',sans-serif;
    font-size:.64rem;
    font-weight:700;
    transition:all .2s ease;
}

.stButton>button:hover {
    border-color:var(--cyan);
    background:rgba(0,245,255,.13);
    box-shadow:0 0 14px rgba(0,245,255,.2);
    transform:translateY(-1px);
}

.stProgress>div>div {
    background:rgba(0,245,255,.1);
    border:1px solid rgba(0,245,255,.2);
    border-radius:20px;
}

.stProgress>div>div>div {
    background:linear-gradient(90deg,#00bcd4,#00f5ff,#a855f7);
}

[data-testid="stImage"] img {
    border-radius:9px;
}

[data-testid="stDataFrame"] {
    border:1px solid rgba(0,245,255,.2);
    border-radius:10px;
    overflow:hidden;
}

[data-testid="stExpander"] {
    border:1px solid rgba(0,245,255,.3);
    border-radius:12px;
    background:rgba(12,17,33,.85);
}

.mm-footer {
    padding:1.2rem 0;
    color:#71809f;
    text-align:center;
    font-family:'Orbitron',sans-serif;
    font-size:.6rem;
    letter-spacing:.12em;
}

@media(prefers-reduced-motion:reduce) {
    *,*:before,*:after {
        animation:none !important;
        transition:none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# IMAGE UTILITIES
# =========================================================

def framed_image(img, color, width=5):
    """Add a coloured border to a candidate image."""
    if not isinstance(img, Image.Image):
        img = Image.open(img)

    img = img.convert("RGB")
    return ImageOps.expand(img, border=width, fill=color)


def neon_similarity_chart(scores, correct_idx, ai_idx):
    """Draw a custom SVG cosine-similarity chart."""
    if scores is None or len(scores) == 0:
        return

    scores = [float(s) for s in scores]

    chart_width = 760
    left = 100
    right = 70
    top = 24
    row_height = 43
    bar_height = 19
    bar_max = chart_width - left - right
    chart_height = top + len(scores) * row_height + 18

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {chart_width} {chart_height}" '
        f'width="100%" role="img" aria-label="Similarity ranking">',
        '<defs>',
        '<linearGradient id="neonBar" x1="0" y1="0" x2="1" y2="0">',
        '<stop offset="0%" stop-color="#00bcd4"/>',
        '<stop offset="65%" stop-color="#00f5ff"/>',
        '<stop offset="100%" stop-color="#a855f7"/>',
        '</linearGradient>',
        '</defs>',
    ]

    for tick in range(5):
        value = tick / 4
        x = left + value * bar_max

        parts.append(
            f'<line x1="{x:.1f}" y1="10" x2="{x:.1f}" '
            f'y2="{chart_height-12}" stroke="#26324c" stroke-width="1"/>'
        )

        parts.append(
            f'<text x="{x:.1f}" y="{chart_height-1}" '
            f'fill="#91a4c7" font-size="11" text-anchor="middle">'
            f'{value:.2f}</text>'
        )

    ranking = sorted(
        range(len(scores)),
        key=lambda i: scores[i],
        reverse=True,
    )

    for rank, idx in enumerate(ranking):
        y = top + rank * row_height
        score = scores[idx]

        # The feature similarity values are normally between -1 and 1.
        # Clamp only the displayed bar width, not the original score.
        bar_width = max(0, min(score, 1)) * bar_max

        if idx == correct_idx:
            label_color = "#39ff88"
            marker = "CORRECT"
        elif idx == ai_idx:
            label_color = "#00f5ff"
            marker = "AI PICK"
        else:
            label_color = "#c4d2ec"
            marker = ""

        parts.append(
            f'<text x="8" y="{y+15}" fill="{label_color}" '
            f'font-family="Arial,sans-serif" font-size="12">'
            f'Option {idx+1}</text>'
        )

        parts.append(
            f'<rect x="{left}" y="{y}" width="{bar_max}" '
            f'height="{bar_height}" rx="5" fill="#121a2e"/>'
        )

        parts.append(
            f'<rect x="{left}" y="{y}" width="{bar_width:.2f}" '
            f'height="{bar_height}" rx="5" fill="url(#neonBar)"/>'
        )

        parts.append(
            f'<text x="{left+bar_max+7}" y="{y+14}" '
            f'fill="{label_color}" font-family="Arial,sans-serif" '
            f'font-size="11">{score:.3f}</text>'
        )

        if marker:
            parts.append(
                f'<text x="{left-7}" y="{y+15}" fill="{label_color}" '
                f'font-size="8" text-anchor="end">{marker}</text>'
            )

    parts.append("</svg>")

    st.markdown(
        '<div style="border:1px solid rgba(0,245,255,.2);'
        'border-radius:12px;padding:12px;'
        'background:rgba(5,10,23,.8);overflow:hidden;">'
        + "".join(parts)
        + "</div>",
        unsafe_allow_html=True,
    )


# =========================================================
# AI MODEL
# =========================================================

@st.cache_resource
def get_ai():
    return AIPlayer()


# =========================================================
# SESSION STATE
# =========================================================

def init_state():
    defaults = {
        "history": [],
        "round": None,
        "round_id": 0,
        "session_complete": False,
        "streak": 0,
        "best_streak": 0,
        "last_settings": None,
        "pending_settings": None,
    }

    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def reset_challenge():
    st.session_state.history = []
    st.session_state.round = None
    st.session_state.round_id = 0
    st.session_state.session_complete = False
    st.session_state.streak = 0
    st.session_state.best_streak = 0
    st.session_state.last_settings = None
    st.session_state.pending_settings = None


def start_round(paths, choices_count, level):
    r = make_round(paths, choices_count, level)
    st.session_state.round_id += 1

    r.update({
        "picked": None,
        "ai_pick": None,
        "sims": None,
        "id": st.session_state.round_id,
    })

    st.session_state.round = r
    st.session_state.last_settings = (level, choices_count)
    st.session_state.pending_settings = None


def answer_round(index, round_limit):
    r = st.session_state.round

    if r is None or r["picked"] is not None:
        return

    try:
        with st.spinner("NEURAL ENGINE // ANALYSING IMAGES..."):
            ai_pick, sims = get_ai().guess(
                r["target"],
                r["choices"],
            )

        r["picked"] = index
        r["ai_pick"] = ai_pick
        r["sims"] = sims

        human_ok = int(index == r["answer"])
        ai_ok = int(ai_pick == r["answer"])

        st.session_state.history.append({
            "round": len(st.session_state.history) + 1,
            "level": r["level"],
            "choices": len(r["choices"]),
            "you": human_ok,
            "ai": ai_ok,
            "human_pick": index,
            "ai_pick": ai_pick,
            "answer": r["answer"],
        })

        if human_ok:
            st.session_state.streak += 1
            st.session_state.best_streak = max(
                st.session_state.best_streak,
                st.session_state.streak,
            )
        else:
            st.session_state.streak = 0

        if len(st.session_state.history) >= round_limit:
            st.session_state.session_complete = True

    except Exception as exc:
        st.error(
            "AI inference failed. Check PyTorch, torchvision "
            "and pretrained model weights."
        )
        st.code(str(exc))


init_state()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="mm-kicker">CONTROL CENTER // 01</div>'
        '<h2>ARENA SETUP</h2>',
        unsafe_allow_html=True,
    )

    st.caption("Configure your visual challenge.")

    level = st.slider("⚡ Distortion level", 1, 5, 3)

    choices_count = st.selectbox(
        "▦ Mosaic size",
        [4, 6, 9],
        index=2,
        format_func=lambda n: f"{n} OPTIONS",
    )

    round_limit = st.selectbox(
        "◉ Challenge length",
        [5, 10],
        index=0,
        format_func=lambda n: f"{n} ROUNDS",
    )

    folder = st.text_input("Image directory", "images")

    st.markdown("---")

    st.markdown("""
    <div class="mm-panel">
      <div class="mm-panel-title">MISSION BRIEFING</div>
      <p>01 // Study the distorted target.</p>
      <p>02 // Find its original in the mosaic.</p>
      <p>03 // Compete against the AI.</p>
      <p>04 // Analyse similarity rankings.</p>
      <p style="color:#00f5ff">OBJECTIVE // MAXIMUM ACCURACY</p>
    </div>
    """, unsafe_allow_html=True)

    st.write("")

    if st.button("↻ RESET ARENA", use_container_width=True):
        reset_challenge()
        st.rerun()


# =========================================================
# HEADER
# =========================================================

st.markdown("""
<div class="mm-hero">
  <div class="mm-kicker">SYSTEM ONLINE // COMPUTER VISION EXPERIMENT</div>
  <div class="mm-title">MOSAIC <span>MATCH</span></div>
  <div class="mm-subtitle">
    HUMAN INSTINCT VS MACHINE INTELLIGENCE.
    One target. Multiple possibilities. One correct match.
  </div>
  <div class="mm-status">
    <span class="mm-dot"></span> NEURAL ENGINE READY
  </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# IMAGE LOADING AND ROUND MANAGEMENT
# =========================================================

paths = list_images(folder)

if len(paths) < choices_count:
    st.error(
        f"Add at least {choices_count} images to '{folder}'. "
        f"Found {len(paths)}."
    )
    st.stop()

settings = (level, choices_count)

if not st.session_state.session_complete:
    current = st.session_state.round

    if current is None:
        start_round(paths, choices_count, level)

    elif current["picked"] is None:
        if st.session_state.last_settings != settings:
            start_round(paths, choices_count, level)

    elif st.session_state.last_settings != settings:
        st.session_state.pending_settings = settings


# =========================================================
# SCOREBOARD
# =========================================================

history = st.session_state.history
played = len(history)

human_total = sum(item["you"] for item in history)
ai_total = sum(item["ai"] for item in history)

st.progress(
    min(played / round_limit, 1.0),
    text=f"MISSION PROGRESS // {played:02d} OF {round_limit:02d} ROUNDS",
)

m1, m2, m3, m4 = st.columns(4)

m1.metric("HUMAN SCORE", f"{human_total}/{played}")
m2.metric("AI SCORE", f"{ai_total}/{played}")
m3.metric("CURRENT STREAK", f"🔥 {st.session_state.streak}")
m4.metric("BEST STREAK", f"⚡ {st.session_state.best_streak}")


# =========================================================
# FINAL RESULTS
# =========================================================

if st.session_state.session_complete:
    st.balloons()

    human_acc = 100 * human_total / played if played else 0
    ai_acc = 100 * ai_total / played if played else 0

    st.markdown("""
    <div class="mm-hero">
      <div class="mm-kicker">MISSION COMPLETE // FINAL REPORT</div>
      <div class="mm-title">ARENA <span>RESULTS</span></div>
      <div class="mm-subtitle">
        Every round analysed. Every prediction counted.
      </div>
    </div>
    """, unsafe_allow_html=True)

    if human_acc > ai_acc:
        st.success("🏆 HUMAN VICTORY // You outscored the AI.")
    elif ai_acc > human_acc:
        st.info("🤖 MACHINE VICTORY // The AI scored higher.")
    else:
        st.info("⚔️ DRAW // Both achieved the same accuracy.")

    c1, c2 = st.columns(2)
    c1.metric("HUMAN ACCURACY", f"{human_acc:.1f}%")
    c2.metric("AI ACCURACY", f"{ai_acc:.1f}%")

    df = pd.DataFrame(history)

    # -----------------------------------------
    # Accuracy by difficulty level
    # -----------------------------------------

    summary = (
        df.groupby("level")
        .agg(
            Rounds=("you", "count"),
            Human_accuracy=("you", "mean"),
            AI_accuracy=("ai", "mean"),
        )
        .reset_index()
        .rename(columns={"level": "Distortion level"})
    )

    summary["Human_accuracy"] = (
        summary["Human_accuracy"] * 100
    ).round(1)

    summary["AI_accuracy"] = (
        summary["AI_accuracy"] * 100
    ).round(1)

    st.markdown("### PERFORMANCE BY DISTORTION LEVEL")

    st.dataframe(
        summary.rename(columns={
            "Human_accuracy": "Human accuracy (%)",
            "AI_accuracy": "AI accuracy (%)",
        }),
        hide_index=True,
        use_container_width=True,
    )

    # -----------------------------------------
    # Corrected side-by-side accuracy chart
    # -----------------------------------------

    performance = (
        df.groupby("level")[["you", "ai"]]
        .mean()
        .reset_index()
        .rename(columns={
            "level": "Distortion Level",
            "you": "Human",
            "ai": "AI",
        })
        .melt(
            id_vars="Distortion Level",
            var_name="Player",
            value_name="Accuracy",
        )
    )

    performance["Accuracy"] *= 100

    chart = (
        alt.Chart(performance)
        .mark_bar(
            cornerRadiusTopLeft=5,
            cornerRadiusTopRight=5,
            size=24,
        )
        .encode(
            x=alt.X(
                "Distortion Level:O",
                title="Distortion Level",
                axis=alt.Axis(
                    labelColor="#b8c7e4",
                    titleColor="#00f5ff",
                ),
            ),
            xOffset=alt.XOffset("Player:N"),
            y=alt.Y(
                "Accuracy:Q",
                title="Accuracy (%)",
                scale=alt.Scale(domain=[0, 100], nice=False),
                axis=alt.Axis(
                    values=[0, 20, 40, 60, 80, 100],
                    labelColor="#b8c7e4",
                    titleColor="#00f5ff",
                    gridColor="#26324c",
                ),
            ),
            color=alt.Color(
                "Player:N",
                scale=alt.Scale(
                    domain=["Human", "AI"],
                    range=["#00f5ff", "#a855f7"],
                ),
                legend=alt.Legend(
                    title="PLAYER",
                    labelColor="#eafaff",
                    titleColor="#00f5ff",
                ),
            ),
            tooltip=[
                alt.Tooltip("Distortion Level:O"),
                alt.Tooltip("Player:N"),
                alt.Tooltip("Accuracy:Q", format=".1f"),
            ],
        )
        .properties(
            height=300,
            background="#0b1020",
            title=alt.TitleParams(
                text="HUMAN VS AI // ACCURACY BY DIFFICULTY",
                color="#00f5ff",
                font="Orbitron",
                fontSize=14,
            ),
        )
        .configure_view(stroke="#26324c")
        .configure_axis(
            domainColor="#26324c",
            tickColor="#26324c",
        )
    )

    st.altair_chart(chart, use_container_width=True)

    # -----------------------------------------
    # Round-by-round report
    # -----------------------------------------

    with st.expander("VIEW ROUND-BY-ROUND REPORT"):
        report = df.copy()

        report["Human result"] = report["you"].map({
            1: "CORRECT",
            0: "INCORRECT",
        })

        report["AI result"] = report["ai"].map({
            1: "CORRECT",
            0: "INCORRECT",
        })

        report["Human option"] = report["human_pick"] + 1
        report["AI option"] = report["ai_pick"] + 1
        report["Correct option"] = report["answer"] + 1

        st.dataframe(
            report[[
                "round",
                "level",
                "Human option",
                "AI option",
                "Correct option",
                "Human result",
                "AI result",
            ]],
            hide_index=True,
            use_container_width=True,
        )

    if st.button(
        "🚀 PLAY AGAIN",
        type="primary",
        use_container_width=True,
    ):
        reset_challenge()
        st.rerun()

    st.markdown(
        '<div class="mm-footer">MOSAIC MATCH // VISION ARENA</div>',
        unsafe_allow_html=True,
    )

    st.stop()


# =========================================================
# GAME BOARD
# =========================================================

r = st.session_state.round
answered = r["picked"] is not None

if st.session_state.pending_settings:
    st.info(
        "Settings changed. Your completed round is preserved; "
        "the new settings apply to the next round."
    )

target_col, board_col = st.columns([0.92, 2.8], gap="large")


# TARGET PANEL

with target_col:
    st.markdown(
        '<div class="mm-panel-title">◈ TARGET ACQUISITION</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="mm-target-label">IDENTIFY THIS OBJECT</div>',
        unsafe_allow_html=True,
    )

    st.markdown('<div class="mm-target">', unsafe_allow_html=True)
    st.image(r["target"], use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown(f"""
    <div class="mm-panel" style="margin-top:10px">
      <div class="mm-muted">DISTORTION LEVEL</div>
      <div style="font-family:Orbitron;color:#d6a7ff;font-size:1.1rem">
        {r["level"]} / 5
      </div>
      <div class="mm-muted" style="margin-top:7px">
        ROUND {played+1:02d} / {round_limit:02d}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Look past rotation, colour shifts, blur and noise.")


# MOSAIC CANDIDATES

with board_col:
    st.markdown(
        '<div class="mm-panel-title">▦ MOSAIC GRID // SELECT YOUR MATCH</div>',
        unsafe_allow_html=True,
    )

    st.caption(
        "Choose one candidate. The AI independently ranks "
        "all options after your answer."
    )

    per_row = 3 if choices_count in (6, 9) else 2

    for row_start in range(0, choices_count, per_row):
        cols = st.columns(per_row, gap="medium")

        for offset, col in enumerate(cols):
            i = row_start + offset

            if i >= choices_count:
                break

            with col:
                st.markdown(
                    f'<div style="font-family:Orbitron;font-size:.62rem;'
                    f'letter-spacing:.09em;color:#00f5ff;margin-bottom:4px">'
                    f'CANDIDATE // {i+1:02d}</div>',
                    unsafe_allow_html=True,
                )

                # Correct answer gets green priority if it is also
                # the AI's choice or the human's choice.
                if answered and i == r["answer"]:
                    border_color = "#39ff88"
                    border_width = 5
                elif answered and i == r["picked"]:
                    border_color = "#ff3cac"
                    border_width = 5
                elif answered and i == r["ai_pick"]:
                    border_color = "#00f5ff"
                    border_width = 5
                else:
                    border_color = "#26324c"
                    border_width = 2

                image_to_show = framed_image(
                    r["choices"][i],
                    border_color,
                    border_width,
                )

                st.image(
                    image_to_show,
                    use_container_width=True,
                )

                if not answered:
                    if st.button(
                        f"LOCK IN #{i+1:02d}",
                        key=f"pick_{r['id']}_{i}",
                        use_container_width=True,
                    ):
                        answer_round(i, round_limit)
                        st.rerun()

                else:
                    labels = []

                    if i == r["answer"]:
                        labels.append(
                            '<span style="color:#39ff88;font-weight:700">'
                            '✓ CORRECT</span>'
                        )

                    if i == r["picked"]:
                        labels.append(
                            '<span style="color:#ff3cac;font-weight:700">'
                            'YOU</span>'
                        )

                    if i == r["ai_pick"]:
                        labels.append(
                            '<span style="color:#00f5ff;font-weight:700">'
                            'AI</span>'
                        )

                    if labels:
                        st.markdown(
                            '<div style="font-size:.76rem;'
                            'padding:5px 2px;line-height:1.6">'
                            + " &nbsp;|&nbsp; ".join(labels)
                            + "</div>",
                            unsafe_allow_html=True,
                        )

                    st.caption(
                        f"Similarity: {r['sims'][i]:.3f}"
                    )


# =========================================================
# ROUND FEEDBACK AND AI LAB
# =========================================================

if answered:
    human_won = r["picked"] == r["answer"]
    ai_won = r["ai_pick"] == r["answer"]

    st.divider()

    if human_won and not ai_won:
        st.success("HUMAN ADVANTAGE // You found the match; the AI did not.")
    elif ai_won and not human_won:
        st.warning("AI ADVANTAGE // The model found the correct match.")
    elif human_won and ai_won:
        st.success("DUAL SUCCESS // Both identified the correct candidate.")
    else:
        st.error("NO MATCH // Neither selected the correct candidate.")

    with st.expander(
        "🧠 OPEN AI LAB // Similarity ranking and model reasoning",
        expanded=False,
    ):
        st.write(
            "ResNet18 extracts visual feature vectors. Cosine similarity "
            "compares the target with each candidate. The AI selects "
            "the candidate with the highest similarity score."
        )

        sims = r["sims"]

        ranking = sorted(
            range(len(sims)),
            key=lambda i: sims[i],
            reverse=True,
        )

        best = ranking[0]
        correct_rank = ranking.index(r["answer"]) + 1

        a, b, c = st.columns(3)

        a.metric("AI TOP CANDIDATE", f"OPTION {best+1}")
        b.metric("TOP SIMILARITY", f"{sims[best]:.3f}")
        c.metric(
            "CORRECT ANSWER RANK",
            f"#{correct_rank} / {choices_count}",
        )

        score_df = pd.DataFrame({
            "Candidate": [
                f"Option {i+1}" for i in range(choices_count)
            ],
            "Cosine similarity": sims,
            "AI rank": [
                ranking.index(i) + 1
                for i in range(choices_count)
            ],
            "Correct answer": [
                "YES" if i == r["answer"] else ""
                for i in range(choices_count)
            ],
        }).sort_values("AI rank")

        st.dataframe(
            score_df,
            hide_index=True,
            use_container_width=True,
        )

        st.markdown("#### NEURAL SIMILARITY SCAN")

        neon_similarity_chart(
            sims,
            correct_idx=r["answer"],
            ai_idx=r["ai_pick"],
        )

        st.caption(
            "Similarity is not a probability. A higher score means "
            "the feature vectors are more similar; it does not "
            "guarantee a correct prediction."
        )

    if played < round_limit:
        if st.button(
            "▶ NEXT ROUND // CONTINUE MISSION",
            type="primary",
            use_container_width=True,
        ):
            next_level, next_choices = (
                st.session_state.pending_settings
                or (level, choices_count)
            )

            start_round(paths, next_choices, next_level)
            st.rerun()


# =========================================================
# FOOTER
# =========================================================

st.markdown("""
<div class="mm-footer">
 MOSAIC MATCH // VISION ARENA<br>
 IMAGE AUGMENTATION · RESNET18 · COSINE SIMILARITY
</div>
""", unsafe_allow_html=True)
