import streamlit as st
from main import run_journeygo
st.set_page_config(
    page_title="JourneyGo",
    page_icon="✈️",
    layout="wide"
)
st.title("JourneyGo")
st.caption("AI Travel Planner powered by LangChain + Groq")
if "traveler_name" not in st.session_state:
    st.session_state.traveler_name = ""
if not st.session_state.traveler_name:
    st.subheader("Welcome to JourneyGo")
    name = st.text_input(
        "What is your name?",
        placeholder="Enter your name..."
    )
    if st.button("Start Journey", type="primary"):
        if name.strip():
            st.session_state.traveler_name = name.strip()
            st.rerun()
        else:
            st.warning("Please enter your name.")
else:
    st.write(
        f"Welcome, {st.session_state.traveler_name}! "
        "Where would you like to travel?"
    )
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