import streamlit as st

st.set_page_config(page_title="Marikina Jeepney Finder")

# --- Data: jeepney -> list of stops. Edit freely. ---
JEEPNEYS = {
    "Parang – Bayan":      ["Parang"],
    "SSS Village – Bayan": ["SSS Village", "Concepcion"],
    "NGI – Bayan":         ["NGI"],
    "Kalumpang – Bayan":   ["Kalumpang"],
}

LOCS = ["Parang", "NGI", "Concepcion", "SSS Village", "Kalumpang"]

# --- UI ---
st.title("Marikina Jeepney Finder")
cur = st.selectbox("Current location", LOCS, index=0)
dst = st.selectbox("Destination", LOCS, index=3)

def serving(loc):
    return [j for j, stops in JEEPNEYS.items() if loc in stops]

if cur == dst:
    st.info("Pick two different locations.")
else:
    direct = [j for j, stops in JEEPNEYS.items() if cur in stops and dst in stops]
    if direct:
        st.success(f"Ride: **{' / '.join(direct)}**")
    else:
        st.warning("No direct jeepney. Take one from each side and transfer at **Bayan (Marikina Town Center)**:")
        st.markdown(f"**From {cur}:** {', '.join(serving(cur)) or 'none in list'}")
        st.markdown(f"**To {dst}:** {', '.join(serving(dst)) or 'none in list'}")