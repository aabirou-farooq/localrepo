import streamlit as st
import pandas as pd
import re
from datetime import date

# --------------------------------------------------
# CROP MANAGEMENT REGISTRATION SYSTEM
# Streamlit + Regular Expressions + Pandas
# --------------------------------------------------

st.set_page_config(
    page_title="Crop Management Registration",
    page_icon="🌱",
    layout="wide"
)

# Store registered records during the current Streamlit session
if "registrations" not in st.session_state:
    st.session_state.registrations = []


# --------------------------------------------------
# REGEX VALIDATION FUNCTIONS
# --------------------------------------------------

def validate_farmer_name(name):
    pattern = r"^[A-Za-z ]{3,40}$"
    return bool(re.fullmatch(pattern, name.strip()))


def validate_phone(phone):
    pattern = r"^[6-9]\d{9}$"
    return bool(re.fullmatch(pattern, phone.strip()))


def validate_email(email):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return bool(re.fullmatch(pattern, email.strip()))


def validate_crop_name(crop):
    pattern = r"^[A-Za-z ]{2,30}$"
    return bool(re.fullmatch(pattern, crop.strip()))


def validate_crop_id(crop_id):
    pattern = r"^CRP\d{4}$"
    return bool(re.fullmatch(pattern, crop_id.strip().upper()))


def validate_pin(pin):
    pattern = r"^\d{6}$"
    return bool(re.fullmatch(pattern, pin.strip()))


def validate_land_area(area):
    return area > 0


def validate_production(production):
    return production > 0


# --------------------------------------------------
# TITLE
# --------------------------------------------------

st.title("🌱 Crop Management Registration System")
st.write(
    "Register farmer and crop information using Streamlit. "
    "Important fields are validated using Regular Expressions."
)

st.divider()


# --------------------------------------------------
# REGISTRATION FORM
# --------------------------------------------------

with st.form("crop_registration_form"):

    st.subheader("Farmer Registration Details")

    col1, col2 = st.columns(2)

    with col1:
        farmer_name = st.text_input(
            "Farmer Name *",
            placeholder="Example: Aabir Farooq"
        )

        phone = st.text_input(
            "Phone Number *",
            placeholder="Example: 9876543210"
        )

        email = st.text_input(
            "Email Address *",
            placeholder="Example: farmer@gmail.com"
        )

        pin = st.text_input(
            "PIN Code *",
            placeholder="Example: 190001"
        )

    with col2:
        crop_id = st.text_input(
            "Crop ID *",
            placeholder="Example: CRP1234"
        )

        crop_name = st.text_input(
            "Crop Name *",
            placeholder="Example: Rice"
        )

        crop_type = st.selectbox(
            "Crop Type *",
            ["Food Crop", "Cash Crop", "Cereal", "Vegetable", "Fruit"]
        )

        season = st.radio(
            "Growing Season *",
            ["Kharif", "Rabi", "Zaid"]
        )

    st.subheader("Crop Details")

    col3, col4 = st.columns(2)

    with col3:
        land_area = st.number_input(
            "Land Area (acres) *",
            min_value=0.0,
            step=0.5,
            format="%.2f"
        )

        expected_production = st.number_input(
            "Expected Production (kg) *",
            min_value=0.0,
            step=100.0
        )

    with col4:
        registration_date = st.date_input(
            "Registration Date *",
            value=date.today()
        )

        irrigation = st.multiselect(
            "Irrigation Methods",
            ["Canal", "Tube Well", "Rainwater", "Drip Irrigation", "Sprinkler"]
        )

        organic_farming = st.checkbox(
            "Organic Farming"
        )

    notes = st.text_area(
        "Additional Notes",
        placeholder="Enter any additional crop information..."
    )

    register = st.form_submit_button(
        "🌱 Register Crop"
    )


# --------------------------------------------------
# VALIDATION AND REGISTRATION
# --------------------------------------------------

if register:

    # Check required fields first
    required_fields = [
        farmer_name,
        phone,
        email,
        pin,
        crop_id,
        crop_name
    ]

    if any(field.strip() == "" for field in required_fields):
        st.warning("Please fill in all required fields.")

    else:
        errors = []

        # Regex validations
        if not validate_farmer_name(farmer_name):
            errors.append("Please enter a valid farmer name.")

        if not validate_phone(phone):
            errors.append("Please enter a valid 10-digit Indian phone number.")

        if not validate_email(email):
            errors.append("Please enter a valid email address.")

        if not validate_pin(pin):
            errors.append("Please enter a valid 6-digit PIN code.")

        if not validate_crop_id(crop_id):
            errors.append("Crop ID must follow the format CRP1234.")

        if not validate_crop_name(crop_name):
            errors.append("Please enter a valid crop name.")

        # Other validation rules
        if not validate_land_area(land_area):
            errors.append("Land area must be greater than 0.")

        if not validate_production(expected_production):
            errors.append("Expected production must be greater than 0.")

        # Check duplicate Crop ID
        existing_ids = [
            record["Crop ID"]
            for record in st.session_state.registrations
        ]

        if crop_id.upper() in existing_ids:
            errors.append("This Crop ID is already registered.")

        # Display errors
        if errors:
            for error in errors:
                st.error(error)

            st.info("Registration was not completed. Please correct the invalid information.")

        else:
            # Create registration record using dictionary
            registration = {
                "Farmer Name": farmer_name.strip(),
                "Phone": phone.strip(),
                "Email": email.strip(),
                "PIN": pin.strip(),
                "Crop ID": crop_id.strip().upper(),
                "Crop Name": crop_name.strip(),
                "Crop Type": crop_type,
                "Season": season,
                "Land Area (acres)": land_area,
                "Expected Production (kg)": expected_production,
                "Registration Date": registration_date,
                "Irrigation": ", ".join(irrigation) if irrigation else "None",
                "Organic Farming": "Yes" if organic_farming else "No",
                "Notes": notes.strip()
            }

            # Store dictionary in list
            st.session_state.registrations.append(registration)

            st.success("Registration completed successfully!")


# --------------------------------------------------
# DISPLAY REGISTERED RECORDS USING PANDAS
# --------------------------------------------------

st.divider()
st.subheader("📋 Registered Crop Records")

if st.session_state.registrations:

    df = pd.DataFrame(st.session_state.registrations)

    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )

    # Additional feature: summary statistics
    st.subheader("📊 Crop Summary")

    total_records = len(df)
    total_land = df["Land Area (acres)"].sum()
    total_production = df["Expected Production (kg)"].sum()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registered Crops", total_records)

    with col2:
        st.metric("Total Land", f"{total_land:.2f} acres")

    with col3:
        st.metric("Expected Production", f"{total_production:.0f} kg")

    # Additional feature: filter records
    st.subheader("🔎 Filter Records")

    selected_type = st.selectbox(
        "Filter by Crop Type",
        ["All"] + sorted(df["Crop Type"].unique().tolist())
    )

    if selected_type == "All":
        filtered_df = df
    else:
        filtered_df = df[df["Crop Type"] == selected_type]

    st.dataframe(
        filtered_df,
        use_container_width=True,
        hide_index=True
    )

else:
    st.info("No crop registrations yet. Submit the form above to add a record.")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.caption(
    "Crop Management System | Streamlit + Python Regex + Pandas"
)
