
import streamlit as st
from Bio.Seq import Seq

st.title("CRISPR gRNA Design Tool")

st.write("Enter a DNA sequence to find possible gRNA candidates.")

def find_grnas(sequence):
    sequence = str(Seq(sequence.upper().replace(" ", "")))
    results = []

    for i in range(len(sequence) - 2):
        pam = sequence[i:i+3]

        if pam[1:] == "GG" and i >= 20:
            guide = sequence[i-20:i]

            results.append({
                "gRNA": guide,
                "PAM": pam,
                "Position": i + 1
            })

    return results

dna = st.text_area("Enter DNA sequence:")

if st.button("Find gRNAs"):
    if dna:
        results = find_grnas(dna)

        if results:
            st.success("Possible gRNA candidates found!")

            for number, result in enumerate(results, 1):
                st.subheader(f"Candidate {number}")
                st.write("gRNA:", result["gRNA"])
                st.write("PAM:", result["PAM"])
                st.write("Position:", result["Position"])
        else:
            st.warning("No suitable NGG PAM sites found.")
    else:
        st.warning("Please enter a DNA sequence.")
