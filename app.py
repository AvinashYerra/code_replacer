import streamlit as st

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

st.set_page_config(page_title="Environment Variable Replacer", layout="wide")
st.title("🔧 Environment Variable Replacer")

st.markdown("""
Paste your code or configuration below, choose an environment,
and the app will replace the relevant variables efficiently — even for large files.
""")

# --- Helper function: add line numbers for preview only ---
def add_line_numbers(text: str) -> str:
    lines = text.splitlines()
    numbered_lines = [f"{i+1:4d}: {line}" for i, line in enumerate(lines)]
    return "\n".join(numbered_lines)

# --- Input area ---
code_input = st.text_area("Paste your code here:", height=350, key="input_code")

# --- Environment selection ---
env = st.selectbox("Select Environment", ["dev", "stage", "prod"])

# --- Partition settings ---
CHUNK_SIZE = 500

# --- Button click logic ---
if st.button("Replace Variables"):
    if not code_input.strip():
        st.warning("Please paste some code first.")
    else:
        lines = code_input.splitlines()
        chunks = [lines[i:i + CHUNK_SIZE] for i in range(0, len(lines), CHUNK_SIZE)]

        replaced_chunks = []
        for chunk in chunks:
            chunk_text = "\n".join(chunk)
            for var, value in ENV_CONFIG[env].items():
                chunk_text = chunk_text.replace(f"${{{var}}}", value)
                chunk_text = chunk_text.replace(f"{var}", value)
            replaced_chunks.append(chunk_text)

        replaced_code = "\n".join(replaced_chunks)

        st.success(f"✅ Variables replaced for **{env.upper()}** environment")
        st.markdown("### 🧾 Replaced Code")
        st.code(replaced_code, language="python")

        # --- Download clean output (without line numbers) ---
        st.download_button(
            label="💾 Download Updated Code",
            data=replaced_code,
            file_name=f"updated_{env}.txt",
            mime="text/plain"
        )

# --- Optional: show preview of input with line numbers ---
if code_input:
    with st.expander("📋 Preview Input with Line Numbers"):
        st.code(add_line_numbers(code_input), language="python")
