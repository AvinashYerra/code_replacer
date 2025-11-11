import streamlit as st

# --- Define environment-specific replacements ---
ENV_CONFIG = {
    "dev": {
        "$DI_DB$": "PHIHUB_DEALINSIGHTSD_DB",
        "$CCDM_DB$": "COMM_US_PUB_PROD_DB",
        "$CI_DB$": "PHIHUB_CID_DB",
    },
    "stage": {
        "$DI_DB$": "PHIHUB_DEALINSIGHTSS_DB",
        "$CCDM_DB$": "COMM_US_PUB_PROD_DB",
        "$CI_DB$": "PHIHUB_CISTG_DB",
    },
    "prod": {
        "$DI_DB$": "PHIHUB_DEALINSIGHTSP_DB",
        "$CCDM_DB$": "COMM_US_PUB_PROD_DB",
        "$CI_DB$": "PHIHUB_CIPRD_DB",
    },
}

# --- Streamlit UI ---
st.title("🔧 Environment Variable Replacer")

st.markdown("""
Paste your code or configuration below, choose an environment,
and the app will replace the relevant variables.
""")


# Input area for code
code_input = st.text_area("Paste your code here:", height=250)

# Dropdown for environment selection
env = st.selectbox("Select Environment", ["dev", "stage", "prod"])

# Replace button
if st.button("Replace Variables"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        replaced_code = code_input
        for var, value in ENV_CONFIG[env].items():
            replaced_code = replaced_code.replace(f"${{{var}}}", value)
            replaced_code = replaced_code.replace(f"{var}", value)

        st.success(f"Variables replaced for **{env.upper()}** environment:")
        st.code(replaced_code, language="python")

        # Optional: download button
        st.download_button(
            label="💾 Download Updated Code",
            data=replaced_code,
            file_name=f"updated_{env}.txt",
            mime="text/plain"
        )