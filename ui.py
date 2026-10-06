import streamlit as st
from backend import (
    create_tables,
    add_registration,
    get_registrations,
    get_leaderboard,
    add_team,
    add_event,
    get_events
)
create_tables()
# Page configuration
st.set_page_config(
    page_title="MRECW - College Events",
    page_icon="🚀",
    layout="wide"
)
def go_to_registration():
    st.session_state.navigation = "📝 Registration"
# Title
st.title("🚀 MRECW")
st.subheader("College Events & Hackathon Portal")

st.write("Discover events, join hackathons, build teams and showcase your ideas!")

# Sidebar navigation
st.sidebar.title("📌 Navigation")

pages = [
    "🏠 Home",
    "🚀 Hackathons",
    "📝 Registration",
    "🏆 Leaderboard"
]

if "navigation" not in st.session_state:
    st.session_state.navigation = "🏠 Home"

page = st.sidebar.radio(
    "Go to",
    pages,
    key="navigation"
)
# ---------------- HOME ----------------
# ---------------- HOME ----------------
if page == "🏠 Home":

    st.header("Welcome to MRECW 👋")

    st.info(
        "Your one-stop platform for college events, hackathons, "
        "workshops and competitions."
    )

    st.subheader("🔥 Featured Hackathon")

    events = get_events()

    hackathons = [
        event for event in events
        if event[1] == "Hackathon"
    ]

    if hackathons:

        featured = hackathons[0]

        event_name = featured[2]
        description = featured[3]
        event_date = featured[4]
        venue = featured[5]
        team_size = featured[6]
        prize = featured[7]

        st.markdown(f"### 🚀 {event_name}")

        st.write(description)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "🏆 Prize Pool",
                prize if prize else "Not specified"
            )

        with col2:
            st.metric(
                "👥 Team Size",
                team_size if team_size else "Not specified"
            )

        with col3:
            st.metric(
                "📅 Event Date",
                event_date
            )

        st.write(f"📍 **Venue:** {venue}")

    else:

        st.info("No hackathon has been added yet.")

    st.divider()

    # ---------------- UPCOMING EVENTS ----------------

    st.subheader("📅 Upcoming Events")

    events = get_events()

    if events:

        col1, col2 = st.columns(2)

        for index, event in enumerate(events):

            event_id = event[0]
            event_type = event[1]
            event_name = event[2]
            description = event[3]
            event_date = event[4]
            venue = event[5]
            team_size = event[6]
            prize = event[7]
            rules = event[8]

            if index % 2 == 0:
                current_col = col1
            else:
                current_col = col2

            with current_col:

                if event_type == "Hackathon":
                    st.markdown(f"### 🚀 {event_name}")
                else:
                    st.markdown(f"### 💻 {event_name}")

                st.write(description)

                st.write(f"📅 **Date:** {event_date}")

                st.write(f"📍 **Venue:** {venue}")

                if team_size:
                    st.write(f"👥 **Team Size:** {team_size}")

                if prize:
                    st.write(f"🏆 **Prize:** {prize}")

                with st.expander("📋 View Rules"):
                    st.write(rules)

                st.divider()

    else:

        st.info("No upcoming events available.")

    # ---------------- ADMIN ADD EVENT ----------------

    st.subheader("➕ Add New Event")

    with st.expander("🔐 Admin: Add Hackathon / Workshop"):

        event_type = st.selectbox(
            "📌 Event Type",
            ["Hackathon", "Workshop"]
        )

        event_name = st.text_input(
            "🏆 Event Name"
        )

        description = st.text_area(
            "📝 Description"
        )

        event_date = st.text_input(
            "📅 Event Date"
        )

        venue = st.text_input(
            "📍 Venue"
        )

        team_size = st.text_input(
            "👥 Team Size",
            placeholder="Example: 2-4 members"
        )

        prize = st.text_input(
            "💰 Prize",
            placeholder="Example: ₹50,000"
        )

        rules = st.text_area(
            "📋 Rules"
        )

        if st.button("➕ Add Event", key="add_event_button"):

            if event_name and event_date:

                add_event(
                    event_type,
                    event_name,
                    description,
                    event_date,
                    venue,
                    team_size,
                    prize,
                    rules
                )

                st.success(
                    f"✅ {event_type} added successfully!"
                )

                st.rerun()

            else:

                st.warning(
                    "⚠️ Event name and event date are required."
                )
    
# ---------------- HACKATHONS ----------------
elif page == "🚀 Hackathons":

    st.header("🚀 Upcoming Hackathons")

    events = get_events()

    hackathons = [
        event for event in events
        if event[1] == "Hackathon"
    ]

    if hackathons:

        for event in hackathons:

            event_id = event[0]
            event_type = event[1]
            event_name = event[2]
            description = event[3]
            event_date = event[4]
            venue = event[5]
            team_size = event[6]
            prize = event[7]
            rules = event[8]

            st.subheader(f"🚀 {event_name}")

            st.write(description)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.write(f"📅 **Date:** {event_date}")

            with col2:
                st.write(f"👥 **Team:** {team_size}")

            with col3:
                st.write(f"🏆 **Prize:** {prize}")

            st.write(f"📍 **Venue:** {venue}")

            st.divider()

            st.subheader("📋 Rules")

            st.write(rules)

            st.success("🎯 Registration is open!")

            st.button(
                "📝 Register Now",
                key=f"register_{event_id}",
                on_click=go_to_registration
            )

            st.divider()

    else:

        st.info("No hackathons available currently.")
    


# ---------------- REGISTRATION ----------------
elif page == "📝 Registration":

    st.header("📝 Hackathon Registration")

    name = st.text_input("👤 Student Name")

    roll = st.text_input("🎓 Roll Number")

    branch = st.selectbox(
        "📚 Branch",
        ["AIML", "CSE", "ECE", "EEE", "IT", "Other"]
    )

    year = st.selectbox(
        "📅 Year",
        ["1st Year", "2nd Year", "3rd Year", "4th Year"]
    )

    email = st.text_input("📧 Email")

    team = st.text_input("👥 Team Name")

    skills = st.multiselect(
        "💻 Skills",
        [
            "Python",
            "Java",
            "C",
            "HTML/CSS",
            "JavaScript",
            "AI/ML",
            "Cloud"
        ]
    )

    idea = st.text_area(
        "💡 Project Idea",
        placeholder="Describe your project idea..."
    )

    if st.button("🚀 Submit Registration"):

        if name and roll and email and team:

            skills_text = ", ".join(skills)

            success, message = add_registration(
                name,
                roll,
                branch,
                year,
                email,
                team,
                skills_text,
                idea
            )

            if success:

                st.success(message)
                st.balloons()

            else:

                st.error(message)

        else:

            st.warning(
                "⚠️ Please fill in all required fields."
            )


# ---------------- LEADERBOARD ----------------
elif page == "🏆 Leaderboard":

    st.header("🏆 Hackathon Leaderboard")

    # Add team and score
    st.subheader("➕ Add Team Score")

    team = st.text_input("👥 Team Name")

    project = st.text_input("💡 Project Name")

    score = st.number_input(
        "🏆 Score",
        min_value=0,
        max_value=100,
        value=0
    )

    if st.button("Add to Leaderboard"):

        if team and project:

            add_team(team, project, score)

            st.success("✅ Team added successfully!")

        else:

            st.warning("⚠️ Enter team name and project name.")

    st.divider()

    # Display leaderboard
    st.subheader("🏆 Current Rankings")

    data = get_leaderboard()

    if data:

        leaderboard_data = []

        for rank, row in enumerate(data, start=1):

            leaderboard_data.append({
                "Rank": rank,
                "Team": row[0],
                "Project": row[1],
                "Score": row[2]
            })

        st.dataframe(
            leaderboard_data,
            use_container_width=True,
            hide_index=True
        )

    else:

        st.info("No leaderboard data available yet.")