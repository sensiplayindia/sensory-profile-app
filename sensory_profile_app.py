import streamlit as st
import pandas as pd
import os
import io
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

st.set_page_config(page_title="CHILD Sensory Profile 2 Assessment", layout="wide")

# Local storage configuration 
DATA_FILE = "saved_parent_results.csv"

# --- PARENT MOBILE NUMBER DATABASE ---
MOBILE_DATABASE = {
    "9820012345": "Kiaan Gada",
    "9819987654": "Aarav Mehta",
    "9112345678": "Ananya Sharma"
}

user_responses = {}

def load_saved_results(mobile_number):
    if os.path.exists(DATA_FILE):
        try:
            df = pd.read_csv(DATA_FILE)
            df["Mobile Number"] = df["Mobile Number"].astype(str).str.strip()
            user_data = df[df["Mobile Number"] == str(mobile_number)]
            if not user_data.empty:
                return user_data.iloc[-1]
        except:
            pass
    return None

def check_mobile_login():
    if "authorized_child" in st.session_state:
        return True

    st.subheader("📲 Parent Login Portal")
    st.markdown("Please log in with your registered mobile number to access your child's sensory profile questionnaire.")
    
    parent_input = st.text_input("Enter Registered Mobile Number:", placeholder="e.g., 9820012345")
    
    if st.button("Log In"):
        clean_number = parent_input.replace(" ", "").replace("-", "").strip()
        
        if clean_number in MOBILE_DATABASE:
            st.session_state["authorized_child"] = MOBILE_DATABASE[clean_number]
            st.session_state["parent_mobile"] = clean_number
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
parent_input = st.session_state["parent_mobile"]

st.title("🧩 CHILD Sensory Profile 2™ Online Assessment Portal")
st.success(f"🔓 Welcome! Secure session active for: **{verified_child}**")

# Check historical records
saved_record = load_saved_results(parent_input)

# --- PDF GENERATION ENGINE ---
def generate_report_pdf(child_name, date_str, sec_list, quad_list):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter, rightMargin=40, leftMargin=40, topMargin=40, bottomMargin=40)
    story = []
    
    styles = getSampleStyleSheet()
    title_style = ParagraphStyle(
        'DocTitle', parent=styles['Heading1'], fontName='Helvetica-Bold', fontSize=18, textColor=colors.HexColor('#2F855A'), spaceAfter=15
    )
    section_style = ParagraphStyle(
        'SectionHeader', parent=styles['Heading2'], fontName='Helvetica-Bold', fontSize=13, textColor=colors.HexColor('#2D3748'), spaceBefore=15, spaceAfter=10
    )
    body_style = ParagraphStyle(
        'Body', parent=styles['Normal'], fontName='Helvetica', fontSize=10, textColor=colors.HexColor('#4A5568')
    )
    bold_body = ParagraphStyle(
        'BoldBody', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, textColor=colors.HexColor('#2D3748')
    )
    
    # Header Information
    story.append(Paragraph("🧩 CHILD Sensory Profile 2™ Assessment Report", title_style))
    story.append(Paragraph(f"<b>Child's Name:</b> {child_name}", body_style))
    story.append(Paragraph(f"<b>Assessment Date:</b> {date_str}", body_style))
    story.append(Spacer(1, 15))
    
    # 1. Section Scores Table
    story.append(Paragraph("1. Sensory & Behavioral Section Breakdown", section_style))
    sec_table_data = [[Paragraph("<b>Sensory / Behavioral Category</b>", bold_body), Paragraph("<b>Raw Score</b>", bold_body), Paragraph("<b>Max</b>", bold_body)]]
    for row in sec_list:
        sec_table_data.append([
            Paragraph(str(row.get("Sensory / Behavioral Section Category")), body_style),
            Paragraph(str(row.get("Child's Raw Score Total")), body_style),
            Paragraph(str(row.get("Maximum Possible Score")), body_style)
        ])
    
    t1 = Table(sec_table_data, colWidths=[280, 120, 100])
    t1.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#F7FAFC')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#E2E8F0')),
    ]))
    story.append(t1)
    story.append(Spacer(1, 20))
    
    # 2. Quadrant Table
    story.append(Paragraph("2. Sensory Pattern Quadrant Grid Placement", section_style))
    quad_table_data = [[
        Paragraph("<b>Sensory Quadrant Profile</b>", bold_body), 
        Paragraph("<b>Total Score</b>", bold_body), 
        Paragraph("<b>Normative Range</b>", bold_body), 
        Paragraph("<b>Placement Status</b>", bold_body)
    ]]
    for row in quad_list:
        quad_table_data.append([
            Paragraph(str(row.get("Sensory Quadrant Profile Pattern")), body_style),
            Paragraph(str(row.get("Total Score")), body_style),
            Paragraph(str(row.get("Normative Range Benchmark")), body_style),
            Paragraph(f"<b>{str(row.get('Clinical Placement Status'))}</b>", body_style)
        ])
        
    t2 = Table(quad_table_data, colWidths=[180, 80, 110, 130])
    t2.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#E6FFFA')),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor('#CBD5E0')),
    ]))
    story.append(t2)
    
    doc.build(story)
    buffer.seek(0)
    return buffer

# --- VIEW RENDER LOGIC ---
if saved_record is not None:
    st.markdown("### 📋 Previously Saved History Found")
    st.info(f"Last assessment submitted on: **{saved_record['Timestamp']}**")
    
    history_sec = [
        {"Sensory / Behavioral Section Category": "Auditory Processing", "Child's Raw Score Total": saved_record["Auditory Total"], "Maximum Possible Score": "/ 40"},
        {"Sensory / Behavioral Section Category": "Visual Processing", "Child's Raw Score Total": saved_record["Visual Total"], "Maximum Possible Score": "/ 30"},
        {"Sensory / Behavioral Section Category": "Touch Processing", "Child's Raw Score Total": saved_record["Touch Total"], "Maximum Possible Score": "/ 55"},
        {"Sensory / Behavioral Section Category": "Movement Processing", "Child's Raw Score Total": saved_record["Movement Total"], "Maximum Possible Score": "/ 40"},
        {"Sensory / Behavioral Section Category": "Body Position Processing", "Child's Raw Score Total": saved_record["Body Position Total"], "Maximum Possible Score": "/ 40"},
        {"Sensory / Behavioral Section Category": "Oral Sensory Processing", "Child's Raw Score Total": saved_record["Oral Total"], "Maximum Possible Score": "/ 50"},
        {"Sensory / Behavioral Section Category": "Conduct Associated with SP", "Child's Raw Score Total": saved_record["Conduct Total"], "Maximum Possible Score": "/ 45"},
        {"Sensory / Behavioral Section Category": "Social Emotional Responses", "Child's Raw Score Total": saved_record["Social Total"], "Maximum Possible Score": "/ 70"},
        {"Sensory / Behavioral Section Category": "Attentional Responses", "Child's Raw Score Total": saved_record["Attentional Total"], "Maximum Possible Score": "/ 50"},
    ]
    
    history_quad = [
        {"Sensory Quadrant Profile Pattern": "Seeking / Seeker", "Total Score": saved_record["Seeking Score"], "Normative Range Benchmark": "20 - 47", "Clinical Placement Status": saved_record["Seeking Status"]},
        {"Sensory Quadrant Profile Pattern": "Avoiding / Avoider", "Total Score": saved_record["Avoiding Score"], "Normative Range Benchmark": "21 - 46", "Clinical Placement Status": saved_record["Avoiding Status"]},
        {"Sensory Quadrant Profile Pattern": "Sensitivity / Sensor", "Total Score": saved_record["Sensitivity Score"], "Normative Range Benchmark": "18 - 42", "Clinical Placement Status": saved_record["Sensitivity Status"]},
        {"Sensory Quadrant Profile Pattern": "Registration / Bystander", "Total Score": saved_record["Registration Score"], "Normative Range Benchmark": "19 - 43", "Clinical Placement Status": saved_record["Registration Status"]},
    ]
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("1️⃣ Sensory & Behavioral Section Breakdown")
        st.table(pd.DataFrame(history_sec))
    with col2:
        st.subheader("2️⃣ Sensory Pattern Quadrant Grid Placement")
        st.dataframe(pd.DataFrame(history_quad), use_container_width=True)
    
    # PDF download button with dynamic custom styles
    pdf_bytes = generate_report_pdf(verified_child, str(saved_record['Timestamp']), history_sec, history_quad)
    st.download_button(
        label="📥 Download Clinical Report PDF",
        data=pdf_bytes,
        file_name=f"{verified_child.replace(' ', '_')}_Sensory_Profile_Report.pdf",
        mime="application/pdf"
    )
        
    st.markdown("---")
    show_form = st.checkbox("🔄 Need to re-take the assessment or overwrite these scores? Check this box to load a blank form.")
else:
    show_form = True

if show_form:
    st.sidebar.header("📋 Child & Caregiver Information")
    child_name = st.sidebar.text_input("Child's First & Last Name", value=verified_child)
    child_id = st.sidebar.text_input("ID / Case Number", placeholder="Optional")
    birth_date = st.sidebar.date_input("Child's Birth Date")
    test_date = st.sidebar.date_input("Test Date")
    gender = st.sidebar.selectbox("Gender", ["Male", "Female", "Other"])
    caregiver_name = st.sidebar.text_input("Completed By (Caregiver Name)")
    relationship = st.sidebar.text_input("Relationship to Child", placeholder="e.g., Parent")

    options = ["Almost Always (5)", "Frequently (4)", "Half the Time (3)", "Occasionally (2)", "Almost Never (1)", "Does Not Apply (0)"]
    score_map = {"Almost Always (5)": 5, "Frequently (4)": 4, "Half the Time (3)": 3, "Occasionally (2)": 2, "Almost Never (1)": 1, "Does Not Apply (0)": 0}

    items_db = [
        {"num": 1, "section": "Auditory Processing", "quad": "AV", "text": "reacts strongly to unexpected or loud noises (for example, sirens, dog barking, hair dryer)."},
        {"num": 2, "section": "Auditory Processing", "quad": "AV", "text": "holds hands over ears to protect them from sound."},
        {"num": 3, "section": "Auditory Processing", "quad": "SN", "text": "struggles to complete tasks when music or TV is on."},
        {"num": 4, "section": "Auditory Processing", "quad": "SN", "text": "is distracted when there is a lot of noise around."},
        {"num": 5, "section": "Auditory Processing", "quad": "AV", "text": "becomes unproductive with background noise (for example, fan, refrigerator)."},
        {"num": 6, "section": "Auditory Processing", "quad": "SN", "text": "tunes me out or seems to ignore me."},
        {"num": 7, "section": "Auditory Processing", "quad": "SN", "text": "seems not to hear when I call his or her name (even though hearing is OK)."},
        {"num": 8, "section": "Auditory Processing", "quad": "RG", "text": "enjoys strange noises or makes noise(s) for fun."},
        {"num": 9, "section": "Visual Processing", "quad": "SN", "text": "prefers to play or work in low lighting."},
        {"num": 10, "section": "Visual Processing", "quad": "None", "text": "prefers bright colors or patterns for clothing."},
        {"num": 11, "section": "Visual Processing", "quad": "None", "text": "enjoys looking at visual details in objects."},
        {"num": 12, "section": "Visual Processing", "quad": "RG", "text": "needs help to find objects that are obvious to others."},
        {"num": 13, "section": "Visual Processing", "quad": "SN", "text": "is more bothered by bright lights than other same-aged children."},
        {"num": 14, "section": "Visual Processing", "quad": "SK", "text": "watches people as they move around the room."},
        {"num": 15, "section": "Visual Processing", "quad": "AV", "text": "is bothered by bright lights (for example, hides from sunlight through car window).* Omitted from Visual Total Score."},
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
        {"num": 27, "section": "Movement Processing", "quad": "None", "text": "pursues movement to the point it interferes with daily routines (for example, can't sit still, fidgets)."},
        {"num": 28, "section": "Movement Processing", "quad": "SK", "text": "rocks in chair, on floor, or while standing."},
        {"num": 29, "section": "Movement Processing", "quad": "None", "text": "hesitates going up or down curbs or steps (for example, is cautious, stops before moving)."},
        {"num": 30, "section": "Movement Processing", "quad": "SK", "text": "becomes excited during movement tasks."},
        {"num": 31, "section": "Movement Processing", "quad": "SK", "text": "takes movement or climbing risks that are unsafe."},
        {"num": 32, "section": "Movement Processing", "quad": "SK", "text": "looks for opportunities to fall with no regard for own safety (for example, falls down on purpose)."},
        {"num": 33, "section": "Movement Processing", "quad": "RG", "text": "loses balance unexpectedly when walking on an uneven surface."},
        {"num": 34, "section": "Movement Processing", "quad": "RG", "text": "bumps into things, failing to notice objects or people in the way."},
        {"num": 35, "section": "Body Position Processing", "quad": "RG", "text": "moves stiffly."},
        {"num": 36, "section": "Body Position Processing", "quad": "RG", "text": "becomes tired easily, especially when standing or holding the body in one position."},
        {"num": 37, "section": "Body Position Processing", "quad": "RG", "text": "seems to have weak muscles."},
        {"num": 38, "section": "Body Position Processing", "quad": "RG", "text": "props to support self (for example, holds head in hands, leans against a wall)."},
        {"num": 39, "section": "Body Position Processing", "quad": "RG", "text": "clings to objects, walls, or banisters more than same-aged children."},
        {"num": 40, "section": "Body Position Processing", "quad": "RG", "text": "walks loudly as if feet are heavy."},
        {"num": 41, "section": "Body Position Processing", "quad": "SK", "text": "drapes self over furniture or on other people."},
        {"num": 42, "section": "Body Position Processing", "quad": "None", "text": "needs heavy blankets to sleep."},
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
        {"num": 53, "section": "Conduct Associated with SP", "quad": "RG", "text": "seems accident-prone."},
        {"num": 54, "section": "Conduct Associated with SP", "quad": "RG", "text": "rushes through coloring, writing, or drawing."},
        {"num": 55, "section": "Conduct Associated with SP", "quad": "SK", "text": "takes excessive risks (for example, climbs high into a tree, jumps off tall furniture) that compromise own safety."},
        {"num": 56, "section": "Conduct Associated with SP", "quad": "SK", "text": "seems more active than same-aged children."},
        {"num": 57, "section": "Conduct Associated with SP", "quad": "RG", "text": "does things in a harder way than is needed (for example, wastes time, moves slowly)."},
        {"num": 58, "section": "Conduct Associated with SP", "quad": "AV", "text": "can be stubborn and uncooperative."},
        {"num": 59, "section": "Conduct Associated with SP", "quad": "AV", "text": "has temper tantrums."},
        {"num": 60, "section": "Conduct Associated with SP", "quad": "SK", "text": "appears to enjoy falling."},
        {"num": 61, "section": "Conduct Associated with SP", "quad": "AV", "text": "resists eye contact from me or others."},
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

    unique_sections = list(dict.fromkeys([item["section"] for item in items_db]))
    tabs = st.tabs(unique_sections)

    for index, sec_name in enumerate(unique_sections):
        with tabs[index]:
            st.subheader(f"📍 {sec_name} Items")
            sec_items = [i for i in items_db if i["section"] == sec_name]
            for item in sec_items:
                choice = st.radio(f"**Item {item['num']}:** {item['text']}", options, index=5, key=f"item_{item['num']}", horizontal=True)
                user_responses[item['num']] = score_map[choice]

    if st.button("📊 Calculate & Save Results", type="primary"):
        st.markdown("---")
        st.header("🏁 Summary & Quadrant Results")
        
        sec_totals = {sec: 0 for sec in unique_sections}
        quad_totals = {"SK": 0, "AV": 0, "SN": 0, "RG": 0}
        max_scores = {
            "Auditory Processing": 40, "Visual Processing": 30, "Touch Processing": 55,
            "Movement Processing": 40, "Body Position Processing": 40, "Oral Sensory Processing": 50,
            "Conduct Associated with SP": 45, "Social Emotional Responses": 70, "Attentional Responses": 50
        }
        
        for item in items_db:
            score = user_responses[item["num"]]
            if item["num"] not in [15, 86]:
                sec_totals[item["section"]] += score
            if item["quad"] in quad_totals:
                quad_totals[item["quad"]] += score

        st.subheader("1️⃣ Sensory & Behavioral Section Breakdown")
        sec_summary_data = [{"Sensory / Behavioral Section Category": sec, "Child's Raw Score Total": str(score), "Maximum Possible Score": f"/ {max_scores.get(sec, 0)}"} for sec, score in sec_totals.items()]
        st.table(pd.DataFrame(sec_summary_data))

        st.subheader("2️⃣ Sensory Pattern Quadrant Grid Placement")
        def get_cutoff_status(quad, val):
            cutoffs = {
                "SK": [(0, 19, "Less Than Others"), (20, 47, "Just Like the Majority"), (48, 60, "More Than Others"), (61, 95, "Much More Than Others")],
                "AV": [(0, 20, "Less Than Others"), (21, 46, "Just Like the Majority"), (47, 59, "More Than Others"), (60, 100, "Much More Than Others")],
                "SN": [(0, 17, "Less Than Others"), (18, 42, "Just Like the Majority"), (43, 53, "More Than Others"), (54, 95, "Much More Than Others")],
                "RG": [(0, 18, "Less Than Others"), (19, 43, "Just Like the Majority"), (44, 55, "More Than Others"), (56, 110, "Much More Than Others")]
            }
            for low, high, msg in cutoffs[quad]:
                if low <= val <= high: return msg
            return "Out of Bounds"

        quad_summary_data = []
        quad_names = {"SK": "Seeking / Seeker", "AV": "Avoiding / Avoider", "SN": "Sensitivity / Sensor", "RG": "Registration / Bystander"}
        quad_norms = {"SK": "20 - 47", "AV": "21 - 46", "SN": "18 - 42", "RG": "19 - 43"}

        for quad, score in quad_totals.items():
            status = get_cutoff_status(quad, score)
            quad_summary_data.append({"Sensory Quadrant Profile Pattern": quad_names[quad], "Total Score": str(score), "Normative Range Benchmark": quad_norms[quad], "Clinical Placement Status": status})
        
        st.dataframe(pd.DataFrame(quad_summary_data), use_container_width=True)
        st.success(f"🎉 Scoring completely finalized for {child_name}!")

        # --- LOCAL FILE STORAGE ENGINE WITH INDIA CLOCK CONFIG ---
        timestamp_ist = (pd.Timestamp.now(tz='UTC').tz_convert('Asia/Kolkata')).strftime("%Y-%m-%d %H:%M:%S")
        new_record = {
            "Timestamp": timestamp_ist,
            "Mobile Number": str(parent_input),
            "Child Name": str(child_name),
            "Auditory Total": int(sec_totals["Auditory Processing"]),
            "Visual Total": int(sec_totals["Visual Processing"]),
            "Touch Total": int(sec_totals["Touch Processing"]),
            "Movement Total": int(sec_totals["Movement Processing"]),
            "Body Position Total": int(sec_totals["Body Position Processing"]),
            "Oral Total": int(sec_totals["Oral Sensory Processing"]),
            "Conduct Total": int(sec_totals["Conduct Associated with SP"]),
            "Social Total": int(sec_totals["Social Emotional Responses"]),
            "Attentional Total": int(sec_totals["Attentional Responses"]),
            "Seeking Score": int(quad_totals["SK"]),
            "Seeking Status": str(get_cutoff_status("SK", quad_totals["SK"])),
            "Avoiding Score": int(quad_totals["AV"]),
            "Avoiding Status": str(get_cutoff_status("AV", quad_totals["AV"])),
            "Sensitivity Score": int(quad_totals["SN"]),
            "Sensitivity Status": str(get_cutoff_status("SN", quad_totals["SN"])),
            "Registration Score": int(quad_totals["RG"]),
            "Registration Status": str(get_cutoff_status("RG", quad_totals["RG"]))
        }
        
        if os.path.exists(DATA_FILE):
            try:
                db_df = pd.read_csv(DATA_FILE)
                db_df = pd.concat([db_df, pd.DataFrame([new_record])], ignore_index=True)
            except:
                db_df = pd.DataFrame([new_record])
        else:
            db_df = pd.DataFrame([new_record])
            
        db_df.to_csv(DATA_FILE, index=False)
        st.toast("💾 Assessment saved successfully!", icon="✅")
        st.rerun()
