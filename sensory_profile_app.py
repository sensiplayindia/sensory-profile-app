import streamlit as st

st.set_page_config(page_title="CHILD Sensory Profile 2 Assessment", layout="wide")

# --- PARENT MOBILE NUMBER DATABASE ---
# Keep phone numbers inside quotes "" so Python treats them as text.
# This prevents errors if a number starts with 0 or has a country code.
MOBILE_DATABASE = {
    "9820012345": "Kiaan Gada",
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
        # Clean up input by removing any spaces or dashes parents might type
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

# --- THE APP UNLOCKS HERE ---
verified_child = st.session_state["authorized_child"]
st.title("🧩 CHILD Sensory Profile 2™ Online Assessment Portal")
st.success(f"🔓 Welcome! Secure session active for: **{verified_child}**")

# The sidebar profile form fields auto-fill the child's name instantly!
st.sidebar.header("📋 Child & Caregiver Information")
child_name = st.sidebar.text_input("Child's First & Last Name", value=verified_child)
# ... [The remaining 86 assessment grid rows stay identical below]
