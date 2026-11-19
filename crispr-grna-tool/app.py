
import streamlit as st
from Bio.Seq import Seq

st.set_page_config(
    page_title="CRISPR gRNA Design Tool",
    page_icon="🧬",
    layout="centered"
)

# Pink aesthetic styling
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #fff0f7, #ffe0ef);
    color: #4a2638;
}

.block-container {
    max-width: 900px;
    padding-top: 3rem;
}

h1 {
    color: #d63384 !important;
    text-align: center;
    font-size: 42px !important;
}

h2, h3 {
    color: #d63384 !important;
}

.subtitle {
    text-align: center;
    color: #8f5b73;
    font-size: 17px;
    margin-bottom: 30px;
}

.card {
    background: rgba(255,255,255,0.92);
    border-radius: 24px;
    padding: 30px;
    margin-bottom: 25px;
    box-shadow: 0 10px 30px rgba(214,51,132,0.12);
    border: 1px solid #ffd1e5;
}

label {
    color: #b52b6f !important;
}

textarea {
    background: #fffafd !important;
    border: 2px solid #f3b6d2 !important;
    border-radius: 14px !important;
}

.stButton button {
    width: 100%;
    background: linear-gradient(135deg, #d63384, #ec6aa8);
    color: white;
    border: none;
    border-radius: 14px;
    padding: 12px;
    font-weight: bold;
}

.stButton button:hover {
    color: white;
    border: 1px solid #d63384;
}

.pam-box {
    display: inline-block;
    padding: 10px 16px;
    background: #ffe4f0;
    border-radius: 12px;
    color: #b52b6f;
    font-weight: bold;
    margin-bottom: 15px;
}

table {
    width: 100%;
    border-collapse: collapse;
    background: white;
    border-radius: 14px;
    overflow: hidden;
}

th {
    background: #d63384;
    color: white;
    padding: 14px;
    text-align: left;
}

td {
    padding: 13px;
    border-bottom: 1px solid #f8d4e4;
    color: #4a2638;
}

tr:nth-child(even) {
    background: #fff4f9;
}

.footer {
    text-align: center;
    color: #a66d86;
    font-size: 13px;
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)



def find_grnas(dna_sequence):
    sequence = dna_sequence.upper().replace(" ", "").replace("\n", "")

    
    if not sequence:
        return []

    if any(base not in "ATGC" for base in sequence):
        raise ValueError("Please enter a valid DNA sequence containing A, T, G and C only.")

    sequence = str(Seq(sequence))
    results = []


    for i in range(len(sequence) - 2):
        pam = sequence[i:i+3]

        if pam[1:] == "GG" and i >= 20:
            guide = sequence[i-20:i]

            results.append({
                "position": i + 1,
                "guide": guide,
                "pam": pam
            })

    return results


# Header
st.markdown("""
<div style="text-align:center; margin-bottom:25px;">
    <div style="font-size:55px;">🧬🎀</div>
</div>
""", unsafe_allow_html=True)

st.title("CRISPR gRNA Design Tool")

st.markdown("""
<p class="subtitle">
Find potential guide RNA candidates from your DNA sequence.
</p>
""", unsafe_allow_html=True)


# Input card
st.markdown('<div class="card">', unsafe_allow_html=True)

st.markdown("### 🧬 DNA Sequence")

dna = st.text_area(
    "Enter DNA sequence",
    placeholder="Paste your DNA sequence here...",
    height=150,
    label_visibility="collapsed"
)

st.markdown(
    '<div class="pam-box">✨ PAM: NGG</div>',
    unsafe_allow_html=True
)

search = st.button("🔍 Find gRNAs", use_container_width=True)

st.markdown('</div>', unsafe_allow_html=True)


# Results
if search:

    if not dna.strip():
        st.warning("Please enter a DNA sequence.")

    else:
        try:
            results = find_grnas(dna)

            if results:
                st.markdown("""
                <div class="card">
                    <h2>🎀 Potential gRNA Candidates</h2>
                </div>
                """, unsafe_allow_html=True)

                table = """
                <table>
                <tr>
                    <th>📍 Position</th>
                    <th>🧬 gRNA Sequence</th>
                    <th>✨ PAM</th>
                </tr>
                """

                for result in results:
                    table += f"""
                    <tr>
                        <td>{result['position']}</td>
                        <td><strong>{result['guide']}</strong></td>
                        <td>{result['pam']}</td>
                    </tr>
                    """

                table += "</table>"

                st.markdown(table, unsafe_allow_html=True)

            else:
                st.info("💗 No potential gRNA candidates were found.")

        except ValueError as error:
            st.error(str(error))


# Footer
st.markdown("""
<div class="footer">
CRISPR gRNA Design Tool • Bioinformatics Project 🧬🎀
</div>
""", unsafe_allow_html=True)
