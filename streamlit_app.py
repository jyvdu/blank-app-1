import streamlit as st

st.set_page_config(page_title="Marikina Jeepney Finder")

# --- Data: jeepney -> stops it passes. Edit freely. ---
JEEPNEYS = {
    "Parang":      ["Parang", "Concepcion"],
    "SSS Village": ["SSS Village", "Concepcion"],
    "Kalumpang":   ["Kalumpang"],
}

LOCS = ["Parang", "Concepcion", "SSS Village", "Kalumpang"]

st.title("Marikina Jeepney Finder")
cur = st.selectbox("Current location", LOCS, index=0)
dst = st.selectbox("Destination", LOCS, index=3)

def serving(loc):
    return [j for j, stops in JEEPNEYS.items() if loc in stops]

if cur == dst:
    st.info("Pick two different locations.")
else:
    direct = [j for j in JEEPNEYS if cur in JEEPNEYS[j] and dst in JEEPNEYS[j]]
    if direct:
        st.success(f"Ride the **{' or '.join(direct)}** jeepney from {cur} to {dst}.")
    else:
        from_cur, to_dst = serving(cur), serving(dst)
        if not from_cur or not to_dst:
            missing = cur if not from_cur else dst
            st.error(f"No jeepney in the list serves {missing}. Edit the JEEPNEYS dict to add it.")
        else:
            st.warning(f"No direct jeepney. Transfer at **Bayan (Marikina Town Center)**:")
            st.markdown(f"1. Ride the **{' or '.join(from_cur)}** jeepney from {cur} to Bayan.")
            st.markdown(f"2. Transfer to the **{' or '.join(to_dst)}** jeepney to {dst}.")