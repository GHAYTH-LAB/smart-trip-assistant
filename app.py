import streamlit as st
from main import run_journeygo

APP_CSS = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap');
    :root { --ink: #14232e; --teal: #087b7f; --coral: #ef7655; }
    .stApp { background: radial-gradient(circle at 8% 0%, #dff4f0 0, transparent 29%), radial-gradient(circle at 96% 14%, #fff0e7 0, transparent 26%), #f8fbfa; color: var(--ink); font-family: 'DM Sans', sans-serif; }
    .block-container { max-width: 1040px; padding-top: 2.8rem; padding-bottom: 3rem; }
    #MainMenu, footer, header { visibility: hidden; }
    .journey-hero { animation: float-in .6s ease-out both; margin-bottom: 2rem; }
    .journey-hero .eyebrow { color: var(--teal); font-size: .76rem; font-weight: 700; letter-spacing: .13em; text-transform: uppercase; }
    .journey-hero h1 { font-family: 'Playfair Display', serif; font-size: clamp(2.7rem, 7vw, 5rem); line-height: 1; margin: .35rem 0 .65rem; }
    .journey-hero p { color: #657681; font-size: 1.08rem; max-width: 540px; margin: 0; }
    [data-testid="stVerticalBlockBorderWrapper"] { border-radius: 20px; border-color: rgba(20,35,46,.09); background: rgba(255,255,255,.7); box-shadow: 0 14px 36px rgba(20,55,62,.07); }
    .stTextInput input { border-radius: 10px; border-color: #c7d9d6; }
    .stTextInput input:focus { border-color: var(--teal); box-shadow: 0 0 0 1px var(--teal); }
    div.stButton > button { background: var(--teal); border: 0; border-radius: 10px; color: white; font-weight: 700; padding: .62rem 1.1rem; transition: transform .18s ease, box-shadow .18s ease; }
    div.stButton > button:hover { background: #006b70; transform: translateY(-2px); box-shadow: 0 8px 18px rgba(8,123,127,.22); }
    [data-testid="stChatMessage"] { border-radius: 16px; animation: float-in .38s ease-out both; }
    [data-testid="stChatMessageContent"], [data-testid="stChatMessageContent"] * { color: #14232e !important; }
    [data-testid="stChatMessageContent"] { background: rgba(255,255,255,.92); border: 1px solid #d9e6e3; padding: .15rem .7rem; }
    [data-testid="stChatInput"] { animation: float-in .55s ease-out both; }
    [data-testid="stChatInput"] textarea { background: #ffffff !important; color: #14232e !important; border: 1px solid #9bbdb8 !important; border-radius: 12px !important; }
    [data-testid="stChatInput"] textarea::placeholder { color: #56706e !important; opacity: 1; }
    [data-testid="stChatInput"] textarea:focus { border-color: #087b7f !important; box-shadow: 0 0 0 3px rgba(8,123,127,.14) !important; }
    [data-testid="stBottom"] { background: linear-gradient(180deg, rgba(248,251,250,0), #f8fbfa 35%) !important; }
    h3 { font-family: 'Playfair Display', serif; }
    @keyframes float-in { from { opacity: 0; transform: translateY(14px); } to { opacity: 1; transform: translateY(0); } }
    @media (prefers-reduced-motion: reduce) { *, *::before, *::after { animation: none !important; transition: none !important; } }
</style>
"""

st.set_page_config(
    page_title="JourneyGo",
    page_icon="✈️",
    layout="wide"
)
st.markdown(APP_CSS, unsafe_allow_html=True)
st.markdown("""
<div class="journey-hero">
    <div class="eyebrow">Your thoughtful travel companion</div>
    <h1>JourneyGo</h1>
    <p>From the first idea to a day-by-day itinerary, your next escape starts here.</p>
</div>
""", unsafe_allow_html=True)
if "traveler_name" not in st.session_state:
    st.session_state.traveler_name = ""
if not st.session_state.traveler_name:
    with st.container(border=True):
        st.subheader("Let’s begin your next escape")
        st.caption("Tell us your name, then describe the trip you have in mind.")
        name = st.text_input("Your name", placeholder="Enter your name...")
        if st.button("Start planning →", type="primary"):
            if name.strip():
                st.session_state.traveler_name = name.strip()
                st.rerun()
            else:
                st.warning("Please enter your name.")
        st.caption("1. Introduce yourself  •  2. Describe your trip  •  3. Receive your plan")
else:
    st.markdown(f"Welcome back, **{st.session_state.traveler_name}**. Where would you like to travel?")
    prompt = st.chat_input(
        "Describe your trip..."
    )
    if prompt:
        with st.chat_message("user"):
            st.write(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Planning your trip..."):
                response = run_journeygo(prompt)
            st.markdown(
                f"### {response.departure_city} → "
                f"{response.destination_city}"
            )
            st.write(
                f"Flight: {response.flight_info}"
            )
            st.write("Hotels:")
            for hotel in response.hotel_infos:
                st.write(hotel)
            st.write(
               f"Visa: {response.visa_info}"
            )
            st.write("Itinerary:")
            for day in response.days:
                st.write(
                    f"Day {day.day_number}:"
                )
                for activity in day.activities:
                    st.write(
                        f"- {activity}"
                    )
