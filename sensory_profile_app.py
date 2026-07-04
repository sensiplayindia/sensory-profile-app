import streamlit as st

st.set_page_config(page_title="CHILD Sensory Profile 2 Assessment", layout="wide")

# --- PARENT MOBILE NUMBER DATABASE ---
# Update this dictionary to add or change parents. 
# Keep numbers in quotes "" to prevent formatting bugs.
MOBILE_DATABASE = {
    "9920892121": "Kiaan Gada",
    "9819987654": "Aarav Mehta",
    "9112345678": "Ananya Sharma"
}

def check_mobile_login():
    """Returns True if the parent enters a registered mobile number."""
    if "authorized_child" in st.session_state:
        return True

    st.subheader("📲 Parent Login Portal")
    st.markdown("Please log in with your registered mobile number to access your child's sensory profile questionnaire.")
    
    parent_input = st.text_input("Enter Registered Mobile Number:", placeholder="e.g., 9820012345")
    
    if st.button("Log In"):
        # Clean up input by removing any spaces or dashes parents might accidentally type
        clean_number = parent_input.replace(" ", "").replace("-", "").strip()
        
        if clean_number in MOBILE_DATABASE:
            st.session_state["authorized_child"] = MOBILE_DATABASE[clean_number]
            st.rerun()
        elif clean_number == "":
            st.warning("Please enter your mobile number.")
        else:
            st.error("❌ This mobile number is not registered in our system. Please check with your provider.")
            return False
    return False

if not check_mobile_login():
    st.stop()

# --- THE APP UNLOCKS HERE AFTER VALID LOGIN ---
verified_child = st.session_state["authorized_child"]
st.title("🧩 CHILD Sensory Profile 2™ Online Assessment Portal")
st.success(f"🔓 Welcome! Secure session active for: **{verified_child}**")

# Sidebar profile form fields
st.sidebar.header("📋 Child & Caregiver Information")
child_name = st.sidebar.text_input("Child's First & Last Name", value=verified_child)
child_id = st.sidebar.text_input("ID / Case Number", placeholder="Optional")
birth_date = st.sidebar.date_input("Child's Birth Date")
test_date = st.sidebar.date_input("Test Date")
gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
caregiver_name = st.sidebar.text_input("Completed By (Caregiver Name)")
relationship = st.sidebar.text_input("Relationship to Child", placeholder="e.g., Parent")

# Score Options
options = ["Almost Always (5)", "Frequently (4)", "Half the Time (3)", "Occasionally (2)", "Almost Never (1)", "Does Not Apply (0)"]
score_map = {"Almost Always (5)": 5, "Frequently (4)": 4, "Half the Time (3)": 3, "Occasionally (2)": 2, "Almost Never (1)": 1, "Does Not Apply (0)": 0}

# Complete Item Database Mapped with Sections & Quadrants
items_db = [
    # Auditory
    {"num": 1, "section": "Auditory Processing", "quad": "AV", "text": "reacts strongly to unexpected or loud noises (for example, sirens, dog barking, hair dryer)."},
    {"num": 2, "section": "Auditory Processing", "quad": "AV", "text": "holds hands over ears to protect them from sound."},
    {"num": 3, "section": "Auditory Processing", "quad": "SN", "text": "struggles to complete tasks when music or TV is on."},
    {"num": 4, "section": "Auditory Processing", "quad": "SN", "text": "is distracted when there is a lot of noise around."},
    {"num": 5, "section": "Auditory Processing", "quad": "AV", "text": "becomes unproductive with background noise (for example, fan, refrigerator)."},
    {"num": 6, "section": "Auditory Processing", "quad": "SN", "text": "tunes me out or seems to ignore me."},
    {"num": 7, "section": "Auditory Processing", "quad": "SN", "text": "seems not to hear when I call his or her name (even though hearing is OK)."},
    {"num": 8, "section": "Auditory Processing", "quad": "RG", "text": "enjoys strange noises or makes noise(s) for fun."},
    # Visual
    {"num": 9, "section": "Visual Processing", "quad": "SN", "text": "prefers to play or work in low lighting."},
    {"num": 10, "section": "Visual Processing", "quad": "None", "text": "prefers bright colors or patterns for clothing."},
    {"num": 11, "section": "Visual Processing", "quad": "None", "text": "enjoys looking at visual details in objects."},
    {"num": 12, "section": "Visual Processing", "quad": "RG", "text": "needs help to find objects that are obvious to others."},
    {"num": 13, "section": "Visual Processing", "quad": "SN", "text": "is more bothered by bright lights than other same-aged children."},
    {"num": 14, "section": "Visual Processing", "quad": "SK", "text": "watches people as they move around the room."},
    {"num": 15, "section": "Visual Processing", "quad": "AV", "text": "is bothered by bright lights (for example, hides from sunlight through car window).* Omitted from Visual Total Score."},
    # Touch
    {"num": 16, "section": "Touch Processing", "quad": "SN", "text": "shows distress during grooming (for example, fights or cries during haircutting, face washing, fingernail cutting)."},
    {"num": 17, "section": "Touch Processing", "quad": "None", "text": "becomes irritated by wearing shoes or socks."},
    {"num": 18, "section": "Touch Processing", "quad": "AV", "text": "shows an emotional or aggressive response to being touched."},
    {"num": 19, "section": "Touch Processing", "quad": "SN", "text": "becomes anxious when standing close to others (for example, in a line)."},
    {"num": 20, "section": "Touch Processing", "quad": "SN", "text": "rubs or scratches a part of the body that has been touched."},
    {"num": 21, "section": "Touch Processing", "quad": "SK", "text": "touches people or objects to the point of annoying others."},
    {"num": 22, "section": "Touch Processing", "quad": "SK", "text": "displays need to touch toys, surfaces, or textures (for example, wants to get the feeling of everything)."},
    {"num": 23, "section": "Touch Processing", "quad": "RG", "text": "seems unaware of pain."},
    {"num": 24, "section": "Touch Processing", "quad": "RG", "text": "seems unaware of temperature changes."},
    {"num": 25, "section": "Touch Processing", "quad": "SK", "text": "touches people and objects more than same-aged children."},
    {"num": 26, "section": "Touch Processing", "quad": "RG", "text": "seems oblivious to messy hands or face."},
    # Movement
    {"num": 27, "section": "Movement Processing", "quad": "None", "text": "pursues movement to the point it interferes with daily routines (for example, can't sit still, fidgets)."},
    {"num": 28, "section": "Movement Processing", "quad": "SK", "text": "rocks in chair, on floor, or while standing."},
    {"num": 29, "section": "Movement Processing", "quad": "None", "text": "hesitates going up or down curbs or steps (for example, is cautious, stops before moving)."},
    {"num": 30, "section": "Movement Processing", "quad": "SK", "text": "becomes excited during movement tasks."},
    {"num": 31, "section": "Movement Processing", "quad": "SK", "text": "takes movement or climbing risks that are unsafe."},
    {"num": 32, "section": "Movement Processing", "quad": "SK", "text": "looks for opportunities to fall with no regard for own safety (for example, falls down on purpose)."},
    {"num": 33, "section": "Movement Processing", "quad": "RG", "text": "loses balance unexpectedly when walking on an uneven surface."},
    {"num": 34, "section": "Movement Processing", "quad": "RG", "text": "bumps into things, failing to notice objects or people in the way."},
    # Body Position
    {"num": 35, "section": "Body Position Processing", "quad": "RG", "text": "moves stiffly."},
    {"num": 36, "section": "Body Position Processing", "quad": "RG", "text": "becomes tired easily, especially when standing or holding the body in one position."},
    {"num": 37, "section": "Body Position Processing", "quad": "RG", "text": "seems to have weak muscles."},
    {"num": 38, "section": "Body Position Processing", "quad": "RG", "text": "props to support self (for example, holds head in hands, leans against a wall)."},
    {"num": 39, "section": "Body Position Processing", "quad": "RG", "text": "clings to objects, walls, or banisters more than same-aged children."},
    {"num": 40, "section": "Body Position Processing", "quad": "RG", "text": "walks loudly as if feet are heavy."},
    {"num": 41, "section": "Body Position Processing", "quad": "SK", "text": "drapes self over furniture or on other people."},
    {"num": 42, "section": "Body Position Processing", "quad": "None", "text": "needs heavy blankets to sleep."},
    # Oral Sensory
    {"num": 43, "section": "Oral Sensory Processing", "quad": "None", "text": "gags easily from certain food textures or food utensils in mouth."},
    {"num": 44, "section": "Oral Sensory Processing", "quad": "SN", "text": "rejects certain tastes or food smells that are typically part of children's diets."},
    {"num": 45, "section": "Oral Sensory Processing", "quad": "SN", "text": "eats only certain tastes (for example, sweet, salty)."},
    {"num": 46, "section": "Oral Sensory Processing", "quad": "SN", "text": "limits self to certain food textures."},
    {"num": 47, "section": "Oral Sensory Processing", "quad": "SN", "text": "is a picky eater, especially about food textures."},
    {"num": 48, "section": "Oral Sensory Processing", "quad": "SK", "text": "smells nonfood objects."},
    {"num": 49, "section": "Oral Sensory Processing", "quad": "SK", "text": "shows a strong preference for certain tastes."},
    {"num": 50, "section": "Oral Sensory Processing", "quad": "SK", "text": "craves certain foods, tastes, or smells."},
    {"num": 51, "section": "Oral Sensory Processing", "quad": "SK", "text": "puts objects in mouth (for example, pencil, hands)."},
    {"num": 52, "section": "Oral Sensory Processing", "quad": "SN", "text": "bites tongue or lips more than same-aged children."},
    # Conduct
    {"num": 53, "section": "Conduct Associated with SP", "quad": "RG", "text": "seems accident-prone."},
    {"num": 54, "section": "Conduct Associated with SP", "quad": "RG", "text": "rushes through coloring, writing, or drawing."},
    {"num": 55, "section": "Conduct Associated with SP", "quad": "SK", "text": "takes excessive risks (for example, climbs high into a tree, jumps off tall furniture) that compromise own safety."},
    {"num": 56, "section": "Conduct Associated with SP", "quad": "SK", "text": "seems more active than same-aged children."},
    {"num": 57, "section": "Conduct Associated with SP", "quad": "RG", "text": "does things in a harder way than is needed (for example, wastes time, moves slowly)."},
    {"num": 58, "section": "Conduct Associated with SP", "quad": "AV", "text": "can be stubborn and uncooperative."},
    {"num": 59, "section": "Conduct Associated with SP", "quad": "AV", "text": "has temper tantrums."},
    {"num": 60, "section": "Conduct Associated with SP", "quad": "SK", "text": "appears to enjoy falling."},
    {"num": 61, "section": "Conduct Associated with SP", "quad": "AV", "text": "resists eye contact from me or others."},
    # Social Emotional
    {"num": 62, "section": "Social Emotional Responses", "quad": "RG", "text": "seems to have low self-esteem (for example, difficulty liking self)."},
    {"num": 63, "section": "Social Emotional Responses", "quad": "AV", "text": "needs positive support to return to challenging situations."},
    {"num": 64, "section": "Social Emotional Responses", "quad": "AV", "text": "is sensitive to criticisms."},
    {"num": 65, "section": "Social Emotional Responses", "quad": "AV", "text": "has definite, predictable fears."},
    {"num": 66, "section": "Social Emotional Responses", "quad": "AV", "text": "expresses feeling like a failure."},
    {"num": 67, "section": "Social Emotional Responses", "quad": "AV", "text": "is too serious."},
    {"num": 68, "section": "Social Emotional Responses", "quad": "AV", "text": "has strong emotional outbursts when unable to complete a task."},
    {"num": 69, "section": "Social Emotional Responses", "quad": "SN", "text": "struggles to interpret body language or facial expression."},
    {"num": 70, "section": "Social Emotional Responses", "quad": "AV", "text": "gets frustrated easily."},
    {"num": 71, "section": "Social Emotional Responses", "quad": "AV", "text": "has fears that interfere with daily routines."},
    {"num": 72, "section": "Social Emotional Responses", "quad": "AV", "text": "is distressed by changes in plans, routines, or expectations."},
    {"num": 73, "section": "Social Emotional Responses", "quad": "SN", "text": "needs more protection from life than same-aged children."},
    {"num": 74, "section": "Social Emotional Responses", "quad": "AV", "text": "interacts or participates in groups less than same-aged children."},
    {"num": 75, "section": "Social Emotional Responses", "quad": "AV", "text": "has difficulty with friendships (for example, making or keeping friends)."},
    # Attentional
    {"num": 76, "section": "Attentional Responses", "quad": "RG", "text": "misses eye contact with me during everyday interactions."},
    {"num": 77, "section": "Attentional Responses", "quad": "SN", "text": "struggles to pay attention."},
    {"num": 78, "section": "Attentional Responses", "quad": "SN", "text": "looks away from tasks to notice all actions in the room."},
    {"num": 79, "section": "Attentional Responses", "quad": "RG", "text": "seems oblivious within an active environment (for example, unaware of activity)."},
    {"num": 80, "section": "Attentional Responses", "quad": "RG", "text": "stares intensively at objects."},
    {"num": 81, "section": "Attentional Responses", "quad": "AV", "text": "stares intensively at people."},
    {"num": 82, "section": "Attentional Responses", "quad": "SK", "text": "watches everyone when they move around the room."},
    {"num": 83, "section": "Attentional Responses", "quad": "SK", "text": "jumps from one thing to another so that it interferes with activities."},
    {"num": 84, "section": "Attentional Responses", "quad": "SN", "text": "gets lost easily."},
    {"num": 85, "section": "Attentional Responses", "quad": "RG", "text": "has a hard time finding objects in competing backgrounds."},
    {"num": 86, "section": "Attentional Responses", "quad": "RG", "text": "seems unaware when people come into the room.* Omitted from Attentional Total Score."}
]

# Set up form view split by section name
unique_sections = list(dict.fromkeys([item["section"] for item in items_db]))
tabs = st.tabs(unique_sections)

user_responses = {}

for index, sec_name in enumerate(unique_sections):
    with tabs[index]:
        st.subheader(f"📍 {sec_name} Items")
        st.caption("When presented with the opportunity, my child...")
        sec_items = [i for i in items_db if i["section"] == sec_name]
        
        for item in sec_items:
            key = f"item_{item['num']}"
            choice = st.radio(
                f"**Item {item['num']}:** {item['text']}", 
                options, 
                index=5, # Default picker points to 'Does Not Apply'
                key=key, 
                horizontal=True
            )
            user_responses[item['num']] = score_map[choice]

if st.button("📊 Calculate & Generate Diagnostic Profile Report", type="primary"):
    st.header("🏁 Child Profile Diagnostic Summary Results")
    
    sec_totals = {sec: 0 for sec in unique_sections}
    quad_totals = {"SK": 0, "AV": 0, "SN": 0, "RG": 0}
    
    for item in items_db:
        score = user_responses[item["num"]]
        if item["num"] not in [15, 86]:
            sec_totals[item["section"]] += score
            
        if item["quad"] in quad_totals:
            quad_totals[item["quad"]] += score

    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Section Raw Score Breakdown")
        for sec, score in sec_totals.items():
            st.metric(label=sec, value=f"{score}")

    with col2:
        st.subheader("🎯 Quadrant Profile Diagnostic Patterns")
        
        def get_cutoff_status(quad, val):
            cutoffs = {
                "SK": [(0, 19, "Less Than Others"), (20, 47, "Just Like the Majority"), (48, 60, "More Than Others"), (61, 95, "Much More Than Others")],
                "AV": [(0, 20, "Less Than Others"), (21, 46, "Just Like the Majority"), (47, 59, "More Than Others"), (60, 100, "Much More Than Others")],
                "SN": [(0, 17, "Less Than Others"), (18, 42, "Just Like the Majority"), (43, 53, "More Than Others"), (54, 95, "Much More Than Others")],
                "RG": [(0, 18, "Less Than Others"), (19, 43, "Just Like the Majority"), (44, 55, "More Than Others"), (56, 110, "Much More Than Others")]
            }
            for low, high, msg in cutoffs[quad]:
                if low <= val <= high:
                    return msg
            return "Out of Bounds"

        for quad, score in quad_totals.items():
            quad_name = {"SK": "Seeking / Seeker", "AV": "Avoiding / Avoider", "SN": "Sensitivity / Sensor", "RG": "Registration / Bystander"}[quad]
            status = get_cutoff_status(quad, score)
            st.markdown(f"**{quad_name}:** `{score}` points → **{status}**")

    st.success("Assessment Complete.")
