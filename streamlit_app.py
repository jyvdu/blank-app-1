# app.py
import streamlit as st

st.set_page_config(page_title="Marikina Jeepney Finder", page_icon="🚌", layout="wide")

# ============================================================
# DATA — edit freely. Locations are limited to Marikina only.
# ============================================================
# corridors/street tags that locations and routes share for matching
LOCATIONS = {
    # Barangay Poblacion
    "Marikina Town Center (Poblacion)": {"brgy": "Poblacion", "tags": ["J.P. Rizal"]},
    # Concepcion
    "Concepcion Chapel":                {"brgy": "Concepcion", "tags": ["J.P. Rizal", "Concepcion Road"]},
    "SSS Village":                      {"brgy": "Concepcion", "tags": ["Concepcion Road"]},
    "Marikina Sports Center":           {"brgy": "Concepcion", "tags": ["Concepcion Road"]},
    "Marikina Industrial Area (Marcos Hwy)": {"brgy": "Concepcion", "tags": ["Marcos Highway"]},
    # Sto. Niño
    "Shoe Avenue":                      {"brgy": "Sto. Niño", "tags": ["Shoe Avenue"]},
    "Riverbanks Center":                {"brgy": "Sto. Niño", "tags": ["Shoe Avenue", "J.P. Rizal"]},
    # Marikina Heights
    "Marikina Heights – Bayan-Bayan":   {"brgy": "Marikina Heights", "tags": ["Bayan-Bayan Road"]},
    "Kalayaan Avenue (Marikina Heights)": {"brgy": "Marikina Heights", "tags": ["Kalayaan Avenue"]},
    "Sumulong Highway (Marikina Heights)": {"brgy": "Marikina Heights", "tags": ["Sumulong Highway"]},
    # Others
    "Parang Chapel":                    {"brgy": "Parang", "tags": ["Shoe Avenue", "Parang Road"]},
    "Nangka Elementary School":         {"brgy": "Nangka", "tags": ["Nangka Road"]},
    "Bagong Silang Chapel":             {"brgy": "Bagong Silang", "tags": ["F. Manalo Street"]},
    "San Roque Chapel":                 {"brgy": "San Roque", "tags": ["Marcos Highway", "San Roque Road"]},
    "Sta. Elena Chapel":                {"brgy": "Sta. Elena", "tags": ["J.P. Rizal"]},
    "Jesús de la Peña Church":          {"brgy": "Jesús de la Peña", "tags": ["J.P. Rizal"]},
    "Carlos P. Garcia Ave (C-5)":       {"brgy": "Marikina Heights", "tags": ["Carlos P. Garcia Avenue"]},
}

ROUTES = {
    "Town Center – Concepcion": {
        "path": "Marikina Town Center → Concepcion",
        "serves": ["Marikina Town Center (Poblacion)", "Concepcion Chapel", "SSS Village",
                   "Marikina Sports Center"],
        "corridors": ["J.P. Rizal", "Concepcion Road"],
        "color": "Green",
        "notes": "Via J.P. Rizal; passes SSS Village and the Sports Center.",
    },
    "Town Center – Shoe Avenue": {
        "path": "Marikina Town Center → Shoe Avenue (Sto. Niño)",
        "serves": ["Marikina Town Center (Poblacion)", "Riverbanks Center", "Shoe Avenue"],
        "corridors": ["J.P. Rizal", "Shoe Avenue"],
        "color": "—",
        "notes": "Runs along Shoe Avenue through Sto. Niño.",
    },
    "Town Center – Marikina Heights": {
        "path": "Marikina Town Center → Marikina Heights",
        "serves": ["Marikina Town Center (Poblacion)", "Marikina Heights – Bayan-Bayan"],
        "corridors": ["J.P. Rizal", "Bayan-Bayan Road"],
        "color": "Green",
        "notes": "Via Bayan-Bayan Road up to Marikina Heights proper.",
    },
    "Town Center – Parang": {
        "path": "Marikina Town Center → Parang",
        "serves": ["Marikina Town Center (Poblacion)", "Parang Chapel"],
        "corridors": ["J.P. Rizal", "Shoe Avenue", "Parang Road"],
        "color": "—",
        "notes": "Via Shoe Avenue / Nangka Road into Parang.",
    },
    "Town Center – Nangka": {
        "path": "Marikina Town Center → Nangka",
        "serves": ["Marikina Town Center (Poblacion)", "Nangka Elementary School"],
        "corridors": ["J.P. Rizal", "Nangka Road"],
        "color": "—",
        "notes": "Serves Nangka proper and the school area.",
    },
    "Town Center – Bagong Silang": {
        "path": "Marikina Town Center → Bagong Silang",
        "serves": ["Marikina Town Center (Poblacion)", "Bagong Silang Chapel"],
        "corridors": ["J.P. Rizal", "F. Manalo Street"],
        "color": "—",
        "notes": "Via F. Manalo Street toward the QC boundary.",
    },
    "Town Center – San Roque": {
        "path": "Marikina Town Center → San Roque",
        "serves": ["Marikina Town Center (Poblacion)", "San Roque Chapel"],
        "corridors": ["J.P. Rizal", "Marcos Highway", "San Roque Road"],
        "color": "—",
        "notes": "Serves the San Roque / Bukid area near the city boundary.",
    },
    "Town Center – Sta. Elena / Jesús de la Peña": {
        "path": "Marikina Town Center → Sta. Elena → Jesús de la Peña",
        "serves": ["Marikina Town Center (Poblacion)", "Sta. Elena Chapel", "Jesús de la Peña Church"],
        "corridors": ["J.P. Rizal"],
        "color": "—",
        "notes": "Along J.P. Rizal through the old town area.",
    },
    "SSS Village – Town Center": {
        "path": "SSS Village → Marikina Town Center",
        "serves": ["SSS Village", "Concepcion Chapel", "Marikina Town Center (Poblacion)"],
        "corridors": ["Concepcion Road", "J.P. Rizal"],
        "color": "—",
        "notes": "Direct from SSS Village to the Town Center.",
    },
    "Marcos Highway – Town Center (Industrial Area)": {
        "path": "Marikina Industrial Area (Marcos Hwy) → Marikina Town Center",
        "serves": ["Marikina Industrial Area (Marcos Hwy)", "Marikina Town Center (Poblacion)"],
        "corridors": ["Marcos Highway", "J.P. Rizal"],
        "color": "—",
        "notes": "Serves factories along the Marcos Highway / Industrial strip.",
    },
    "Marikina Heights – Kalayaan Ave (to QC)": {
        "path": "Marikina Heights → Kalayaan Avenue (Quezon City side)",
        "serves": ["Marikina Heights – Bayan-Bayan", "Kalayaan Avenue (Marikina Heights)"],
        "corridors": ["Bayan-Bayan Road", "Kalayaan Avenue"],
        "color": "—",
        "notes": "Exits Marikina via Kalayaan Avenue toward Quezon City.",
    },
    "Marikina Heights – Sumulong Highway": {
        "path": "Marikina Heights → Sumulong Highway (Antipolo side)",
        "serves": ["Marikina Heights – Bayan-Bayan", "Sumulong Highway (Marikina Heights)"],
        "corridors": ["Bayan-Bayan Road", "Sumulong Highway"],
        "color": "—",
        "notes": "Serves the Sumulong Highway stretch in Marikina Heights.",
    },
    "C-5 / C.P. Garcia – Marikina Heights": {
        "path": "Carlos P. Garcia Ave (C-5) → Marikina Heights",
        "serves": ["Carlos P. Garcia Ave (C-5)", "Marikina Heights – Bayan-Bayan"],
        "corridors": ["Carlos P. Garcia Avenue", "Bayan-Bayan Road"],
        "color": "—",
        "notes": "Along C.P. Garcia Avenue connecting to Marikina Heights.",
    },
}

TRANSFER_HUB_PRIORITY = [
    "Marikina Town Center (Poblacion)",
    "Shoe Avenue",
    "Riverbanks Center",
    "Concepcion Chapel",
    "Marikina Heights – Bayan-Bayan",
]

# ============================================================
# LOGIC
# ============================================================
def score_route(route: dict, loc: str) -> int:
    """How well a route serves a location: stops = 6, shared corridor tags = 2 each."""
    s = 6 if loc in route["serves"] else 0
    s += 2 * len(set(LOCATIONS[loc]["tags"]) & set(route["corridors"]))
    return s


def find_transfer(origin: str, dest: str):
    """Best (route-from, hub, route-to) pair when no single route serves both."""
    from_routes = {n: r for n, r in ROUTES.items() if score_route(r, origin) > 0}
    to_routes = {n: r for n, r in ROUTES.items() if score_route(r, dest) > 0}

    best = None
    for n1, r1 in from_routes.items():
        for n2, r2 in to_routes.items():
            if n1 == n2:
                continue
            shared = set(r1["serves"]) & set(r2["serves"])
            for hub in TRANSFER_HUB_PRIORITY:
                if hub in shared:
                    score = (score_route(r1, origin) + score_route(r2, dest), -TRANSFER_HUB_PRIORITY.index(hub))
                    if best is None or score > best[0]:
                        best = (score, n1, hub, n2)
                    break  # prefer the highest-priority hub for this pair
    if best is None:
        return None
    _, n1, hub, n2 = best
    return n1, hub, n2


def render_route(name: str, route: dict, caption: str | None = None):
    with st.expander(f"🚌 **{name}** — {route['path']}"):
        st.write(f"**Corridors:** {', '.join(route['corridors'])}")
        st.write(f"**Stops / areas:** {', '.join(route['serves'])}")
        if route["color"] != "—":
            st.write(f"**Route color:** {route['color']}")
        st.caption(route["notes"])
        if caption:
            st.caption(caption)


# ============================================================
# UI
# ============================================================
st.title("🚌 Marikina Jeepney Finder")
st.caption("Find jeepney routes near your current location and destination — within Marikina City only.")

options = sorted(LOCATIONS.keys(), key=lambda k: (LOCATIONS[k]["brgy"], k))

if "cur" not in st.session_state:
    st.session_state.cur = "Marikina Town Center (Poblacion)"
if "dst" not in st.session_state:
    st.session_state.dst = "Concepcion Chapel"


def swap():
    st.session_state.cur, st.session_state.dst = st.session_state.dst, st.session_state.cur


c1, c2, c3 = st.columns([5, 1, 5])
with c1:
    cur = st.selectbox(
        "📍 Current location", options, key="cur",
        format_func=lambda k: f"{k} — {LOCATIONS[k]['brgy']}")
with c2:
    st.write("")
    st.write("")
    st.button("⇄ Swap", on_click=swap, use_container_width=True)
with c3:
    dst = st.selectbox(
        "🎯 Destination", options, key="dst",
        format_func=lambda k: f"{k} — {LOCATIONS[k]['brgy']}")

st.divider()

if cur == dst:
    st.info("You're already at your destination — pick two different locations.")
    st.stop()

direct = sorted(
    [(n, r, score_route(r, cur) + score_route(r, dst))
     for n, r in ROUTES.items()
     if score_route(r, cur) > 0 and score_route(r, dst) > 0],
    key=lambda x: -x[2])

if direct:
    st.success(f"✅ **{len(direct)} jeepney route(s)** go near both **{cur}** and **{dst}**.")
    near_both = len({cur, dst} & set(direct[0][1]["serves"])) == 2
    if near_both:
        st.caption("Top pick stops at both locations.")
    for name, route, score in direct:
        render_route(name, route, caption=f"Match score: {score}")
else:
    st.warning(
        f"😕 No single jeepney serves both **{cur}** and **{dst}**. "
        "Here's the best two-ride option:")

    transfer = find_transfer(cur, dst)
    if transfer:
        n1, hub, n2 = transfer
        st.subheader("🔁 Suggested transfer")
        st.markdown(f"""
1. Ride **{n1}** — *{ROUTES[n1]['path']}*
2. Get off / transfer at **{hub}**
3. Ride **{n2}** — *{ROUTES[n2]['path']}*
        """)
        render_route(n1, ROUTES[n1], caption=f"Leg 1 — pick-up near {cur}")
        render_route(n2, ROUTES[n2], caption=f"Leg 2 — alight near {dst}")
    else:
        st.info("No transfer pair found in the data — try different locations.")

    # Nearest routes to each endpoint as backup
    st.subheader("📍 Routes near your current location")
    for name, route in sorted(ROUTES.items(), key=lambda kv: -score_route(kv[1], cur))[:3]:
        if score_route(route, cur) > 0:
            render_route(name, route, caption=f"Score near {cur}: {score_route(route, cur)}")

    st.subheader("🎯 Routes near your destination")
    for name, route in sorted(ROUTES.items(), key=lambda kv: -score_route(kv[1], dst))[:3]:
        if score_route(route, dst) > 0:
            render_route(name, route, caption=f"Score near {dst}: {score_route(route, dst)}")

st.divider()
st.caption(
    "⚠️ Routes, colors, and corridors are approximate and for convenience only — "
    "verify with local signage or the driver before riding. "
    "To add/correct a route, edit the `ROUTES` and `LOCATIONS` dicts at the top of this file."
)