import os
import time

import streamlit as st

from settings import DATA_DIR
from src.data_loader import DrugFilter

st.set_page_config(layout="wide")


@st.cache(suppress_st_warning=True)
def load_df():
    drug_filter = DrugFilter.from_df(DATA_DIR / "preprocessed.csv")
    return drug_filter


def numerals(num):
    if num == 1:
        return "st"
    elif num == 2:
        return "nd"
    elif num == 3:
        return "rd"
    else:
        return "th"


drug_filter = load_df()
dosage_types = drug_filter.dosage_types.copy()
dosage_types.sort()
dosage_types.insert(0, None)
substances = drug_filter.substance_list.copy()
substances.sort()
substances.insert(0, None)

st.title("Clinical development search engine")
substance = st.selectbox("What substance are you interested in?", substances)
if substance:
    filtered = drug_filter.filter_by_substance(substance)
    dosages_available = drug_filter.available_dosages(filtered).copy()
    dosages_available.sort()
    dosage = st.selectbox(
        "What type of dosage are you interested in?", dosages_available
    )

    df = drug_filter.filter_drugs(substance.upper(), dosage)

    with st.spinner("### Searching..."):
        gif_runner = st.image(os.path.join(DATA_DIR, "search_crop.gif"))
        time.sleep(3)
        gif_runner.empty()
    st.success("Done!")

    if df.empty:
        st.write("## No such drug. Please change search criteria.")
    else:
        st.markdown(f"## SUBSTANCE: {df['ActiveIngredient'].iloc[0]}")
        st.markdown(
            "-------------------------------------------------------------------------------"
        )
        st.markdown(f"### DRUG NAME: {df['DrugName'].iloc[0]}")
        st.markdown(f"### DOSAGE: {df['Dosage'].iloc[0]}")
        st.markdown(
            "-------------------------------------------------------------------------------"
        )
        st.write("**INDICATION**: ", df["Indication"].iloc[0])
        st.markdown(
            "-------------------------------------------------------------------------------"
        )
        st.write("**BIOAVAILABILITY**: ", df["bioavailability"].iloc[0])
        st.write("**BIOAVAILABILITY CONTEXT**: ", df["bioavailability_context"].iloc[0])
        st.markdown(
            "-------------------------------------------------------------------------------"
        )
        st.write("**PROTEIN BINDING**: ", df["ProteinBinding"].iloc[0])
        st.write("**PROTEIN BINDING CONTEXT**: ", df["ProteinBindingContext"].iloc[0])
        st.write(
            f'<a href="{df["ApplicationDocsURL"].iloc[0]}">Reference</a></td>',
            unsafe_allow_html=True,
        )
        st.markdown(
            "-------------------------------------------------------------------------------"
        )

        st.write("**RECOMMENDED STUDIES**: ", len(df["RecommendedStudies"].iloc[0]))

        for i, (study_num, study) in enumerate(
            df["RecommendedStudies"].iloc[0].items()
        ):
            if not study:
                st.write("No recommended studies")
            st.write(f"### {i+1}{numerals(i+1)} study")
            st.write("**Study type**: ", study["Type"])
            st.write("**Design**: ", study["Design"])
            st.write("**Strength**: ", study["Strength"])
            st.write("**Subjects**: ", study["Subjects"])

        st.write(
            f'<a href="{df["URL"].iloc[0]}">Reference</a></td>', unsafe_allow_html=True
        )
