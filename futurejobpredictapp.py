import streamlit as st
import json, os, urllib.parse
from datetime import datetime

USER_FILE = "users.json"

# Load or create users
def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f, indent=2)

def authenticate(username, password):
    users = load_users()
    return username in users and users[username]["password"] == password

def register_user(username, password):
    users = load_users()
    if username in users:
        return False
    users[username] = {
        "password": password,
        "goal_job": None,
        "goal_history": [],
        "progress": {},
        "timeline": []
    }
    save_users(users)
    return True

def get_current_user():
    users = load_users()
    return users.get(st.session_state.username, {})

def update_current_user(data):
    users = load_users()
    users[st.session_state.username].update(data)
    save_users(users)

st.set_page_config("Future Job Tracker App", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = ""

def login_ui():
    st.title("🔐 Login or Register")

    login_tab, register_tab = st.tabs(["🔑 Login", "📝 Register"])

    with login_tab:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if authenticate(username, password):
                st.success("Logged in!")
                st.session_state.logged_in = True
                st.session_state.username = username
                st.rerun()
            else:
                st.error("Invalid login.")

    with register_tab:
        new_user = st.text_input("New Username")
        new_pass = st.text_input("New Password", type="password")
        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("Registered! Now login.")
            else:
                st.warning("Username already exists.")

def show_quiz():
    st.title(f"Welcome, {st.session_state.username} 👋")
    user = get_current_user()
    goal = user.get("goal_job")

    if goal:
        st.info(f"🎯 Your Goal Career: **{goal}**")
        st.markdown("""
        **Suggested Steps:**
        - 📚 Learn required skills
        - 🧪 Do mini projects
        - 📜 Earn certifications
        - 💼 Apply for internships
        - 📈 Track your learning
        """)

        # 📈 Progress Tracker
        st.subheader("📈 Your Progress")
        progress_items = ["Completed course", "Built a project", "Updated resume", "Mock interview"]
        progress_state = user.get("progress", {})

        for item in progress_items:
            checked = st.checkbox(item, value=progress_state.get(item, False))
            progress_state[item] = checked

        update_current_user({"progress": progress_state})

        # 📅 Timeline
        st.subheader("📅 Your Timeline")
        new_event = st.text_input("Add timeline entry")
        if st.button("Add to Timeline") and new_event:
            timeline = user.get("timeline", [])
            timeline.append(f"{datetime.now().strftime('%Y-%m-%d')}: {new_event}")
            update_current_user({"timeline": timeline})
            st.rerun()

        for event in reversed(user.get("timeline", [])):
            st.markdown(f"- {event}")

        if st.button("❌ Clear My Goal"):
            update_current_user({"goal_job": None})
            st.rerun()

    # Quiz
    st.subheader("🔮 Take the Career Quiz")
    questions = [
        ("Do you enjoy solving technical problems?", "technical"),
        ("Do you enjoy analyzing data and numbers?", "analytical"),
        ("Are you interested in designing visual content?", "creative"),
        ("Do you enjoy helping people and giving advice?", "social"),
        ("Are you interested in working with software and computers?", "software"),
        ("Do you enjoy teaching or mentoring others?", "teaching"),
        ("Are you good at understanding human behavior and emotions?", "psychology"),
        ("Do you like working with machines or infrastructure?", "engineering"),
        ("Would you enjoy a job that involves travel and storytelling?", "travel"),
        ("Do you like understanding how the human body works?", "science"),
        ("Do you like performing on stage or screen?", "performance"),
        ("Do you enjoy cooking and experimenting with food?", "cooking"),
        ("Are you interested in fashion and trends?", "fashion"),
        ("Do you have strong writing or editing skills?", "writing"),
        ("Are you a good planner or organizer?", "planning"),
        ("Do you like sports and physical activity?", "sports"),
        ("Are you interested in law and justice?", "law"),
        ("Do you prefer freelancing or remote work flexibility?", "freelance")
    ]

    job_database = {
    "Software Engineer": {
        "tags": ["technical", "software", "analytical"],
        "description": "Designs and develops software applications and systems.",
        "salary": "₹8-30 LPA",
        "qualification": "B.Tech in Computer Science or related field"
    },
    "Data Scientist": {
        "tags": ["analytical", "software"],
        "description": "Analyzes large sets of data to find patterns and insights.",
        "salary": "₹10-35 LPA",
        "qualification": "B.Sc/M.Sc in Data Science, Statistics or related field"
    },
    "Graphic Designer": {
        "tags": ["creative"],
        "description": "Creates visual content for branding, ads, and websites.",
        "salary": "₹3-10 LPA",
        "qualification": "Bachelor’s in Design, Fine Arts or related field"
    },
    "Teacher": {
        "tags": ["teaching", "social"],
        "description": "Educates students and helps them learn subjects effectively.",
        "salary": "₹2-8 LPA",
        "qualification": "B.Ed + subject-specific degree"
    },
    "Doctor": {
        "tags": ["science", "social", "teaching"],
        "description": "Diagnoses and treats illnesses, promotes health and wellness.",
        "salary": "₹6-25 LPA",
        "qualification": "MBBS, MD/MS"
    },
    "Psychologist": {
        "tags": ["psychology", "teaching"],
        "description": "Studies mental processes and supports mental health.",
        "salary": "₹4-15 LPA",
        "qualification": "M.A/M.Sc in Psychology + license"
    },
    "Engineer": {
        "tags": ["technical", "engineering"],
        "description": "Designs, builds, and maintains machines, structures or systems.",
        "salary": "₹4-15 LPA",
        "qualification": "B.Tech in Mechanical/Civil/Electrical, etc."
    },
    "Travel Blogger": {
        "tags": ["creative", "travel"],
        "description": "Travels to new places and shares stories, photos, and tips.",
        "salary": "₹1-10 LPA (varies)",
        "qualification": "No fixed degree; skills in writing, photography, social media"
    },
    "Actor": {
        "tags": ["performance", "creative"],
        "description": "Performs in plays, films, or shows to entertain and inspire.",
        "salary": "₹3-50 LPA",
        "qualification": "Training in Drama/Theatre, Portfolio"
    },
    "Artist": {
        "tags": ["creative"],
        "description": "Creates artwork in various mediums like painting, digital art, or sculpture.",
        "salary": "₹2-20 LPA",
            "qualification": "BFA or equivalent experience"
    },
    "Athlete": {
        "tags": ["sports", "performance"],
        "description": "Competes in sports and maintains peak physical condition.",
        "salary": "₹1-50 LPA",
        "qualification": "Training, Sports Academy, National Trials"
    },
    "Author": {
        "tags": ["writing", "creative"],
        "description": "Writes books, novels, articles, or content for various media.",
        "salary": "₹2-15 LPA",
        "qualification": "No fixed degree; Literature or Journalism preferred"
    },
    "Lawyer": {
        "tags": ["law", "analytical", "social"],
        "description": "Represents clients in legal matters and interprets laws.",
        "salary": "₹4-20 LPA",
        "qualification": "LLB + Bar Council Registration"
    },
    "Editor": {
        "tags": ["writing", "analytical"],
        "description": "Reviews and edits content for clarity, grammar, and style.",
        "salary": "₹3-12 LPA",
        "qualification": "Degree in English, Journalism, or Communication"
    },
    "Pharmacist": {
        "tags": ["science", "analytical"],
        "description": "Prepares and dispenses medication, advises on drug use.",
        "salary": "₹3-10 LPA",
        "qualification": "B.Pharm / M.Pharm + License"
    },
    "Chef": {
        "tags": ["cooking", "creative"],
        "description": "Prepares food and manages kitchen operations.",
        "salary": "₹2-15 LPA",
        "qualification": "Hotel Management or Culinary Arts Diploma"
    },
    "Event Planner": {
        "tags": ["planning", "creative", "social"],
        "description": "Plans and coordinates events like weddings, parties, and conferences.",
        "salary": "₹3-10 LPA",
        "qualification": "Bachelor’s in Event Management or PR"
    },
    "Fashion Designer": {
        "tags": ["fashion", "creative"],
        "description": "Designs clothing, accessories, and fashion collections.",
        "salary": "₹3-20 LPA",
        "qualification": "Bachelor’s in Fashion Design"
    },
    "Electrician": {
        "tags": ["technical", "engineering"],
        "description": "Installs and repairs electrical systems in buildings and homes.",
        "salary": "₹1.5-8 LPA",
        "qualification": "ITI/Diploma in Electrical"
    },
    "Nurse": {
        "tags": ["science", "social"],
        "description": "Provides medical care, support, and compassion to patients.",
        "salary": "₹2-8 LPA",
        "qualification": "GNM / B.Sc Nursing + Registration"
    },
    "Freelancer": {
        "tags": ["freelance", "creative", "technical"],
        "description": "Self-employed worker offering skills like writing, coding, or design.",
        "salary": "Varies widely",
        "qualification": "No fixed degree; Skill-based"
    }
}

    job_icons = {
    "Software Engineer": "💻",
    "Data Scientist": "📊",
    "Graphic Designer": "🎨",
    "Teacher": "👩‍🏫",
    "Doctor": "🩺",
    "Psychologist": "🧠",
    "Engineer": "🛠️",
    "Travel Blogger": "🌍",
    "Historical Researcher": "📜",
    "Chemical Engineer": "⚗️",
    "Physics Engineer": "🔬",
    "Content Creator": "📸",
    "Architect": "🏛️",
    "Chartered Accountant": "📈",
    "Actor": "🎭",
    "Artist": "🖌️",
    "Athlete": "🏃",
    "Author": "✍️",
    "Lawyer": "⚖️",
    "Editor": "📝",
    "Pharmacist": "💊",
    "Chef": "👨‍🍳",
    "Event Planner": "🎉",
    "Fashion Designer": "👗",
    "Electrician": "🔌",
    "Nurse": "👩‍⚕️",
    "Freelancer": "🌐"
}

    scores = {}
    for q, tag in questions:
        ans = st.radio(q, ["Yes", "No"], key=tag)
        if ans == "Yes":
            scores[tag] = scores.get(tag, 0) + 1

    if st.button("🔎 Predict Careers"):
        job_scores = {job: sum(scores.get(t, 0) for t in data["tags"]) for job, data in job_database.items()}
        top_jobs = sorted(job_scores.items(), key=lambda x: x[1], reverse=True)[:5]

        st.subheader("✨ Suggested Careers")
        for job, score in top_jobs:
            icon = job_icons.get(job, "💼")
            st.markdown(f"### {icon} {job} — {score} match(es)")
            st.markdown(f"**Description**: {job_database[job]['description']}")
            st.markdown(f"💰 **Salary**: {job_database[job]['salary']}")
            st.markdown(f"🎓 **Qualification**: {job_database[job]['qualification']}")
            st.markdown(f"[🔍 Search {job} on LinkedIn](https://www.linkedin.com/jobs/search/?keywords={urllib.parse.quote(job)})")
            st.markdown(f"[▶️ Watch {job} Videos](https://www.youtube.com/results?search_query={urllib.parse.quote(job + ' career')})")



if not st.session_state.logged_in:
    login_ui()
else:
    show_quiz()
