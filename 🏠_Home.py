# -*- coding: utf-8 -*-
"""home.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1pHuQqNc9ymXBdpBCL0K7Dhe58k94ZETW
"""

import streamlit as st


def home():
    st.set_page_config(
        page_title="FitSphere- Home",
        page_icon="👨‍⚕️",
    )
    st.sidebar.info(
        "**About**: This project is made using publicly available data and comes with no guarantee. We do not store any of the patient's personal information."
    )
    col1, col2, col3 = st.columns([1, 6, 1])

    with col1:
        st.write("")

    with col2:
        st.image("logos/fitsphere-logo.png")

    with col3:
        st.write("")

    st.markdown("---")

    st.markdown(
        f"<h2 style='text-align: center; color: white; background-color: orange;'>About </h2>",
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown(
        f"<p style='text-align: center; color: black; font-size: 20px'> We are virtual Health Consultant, and use state-of-the-art machine learning & deep learning technologies to provide healthcare solutions, help common people and health organizations power their care experience with advanced analytics</p>",
        unsafe_allow_html=True,
    )

    st.markdown("---")

    st.markdown(
        f"<h2 style='text-align: center; color: white; background-color: orange;'>Our Services</h2>",
        unsafe_allow_html=True,
    )
    st.write("")

    st.markdown(
        f"⚕️ **Early Diabetes Detection** - Enter the patient's attributes from the test report and check whether he/she has chances of diabetes or not"
    )

    st.markdown(
        f"⚕️ **Pneumonia Detection** - Enter the patient's attributes from the test report and check whether he/she has chances of any type of pneumonia or not"
    )

    st.markdown("---")

    st.warning(
        "**Disclaimer**: The information on this site is not intended or implied to be a substitute for professional medical advice, diagnosis, or treatment. All content, including text, graphics, images, and information, contained on or available through this website is for general information purposes only. This website makes no representation and assumes no responsibility for the accuracy of information contained on or available through this website, and such information is subject to change without notice. You are encouraged to confirm any information obtained from or through this website with other sources, and review all information regarding any medical condition or treatment with your physician. NEVER DISREGARD PROFESSIONAL MEDICAL ADVICE OR DELAY SEEKING MEDICAL TREATMENT BECAUSE OF SOMETHING YOU HAVE READ ON OR ACCESSED THROUGH THIS WEBSITE. We do not recommend, endorse, or make any representation about the efficacy, appropriateness, or suitability of any specific tests, products, procedures, treatments, services, opinions, health care providers, or other information that may be contained on or available through this website. WE ARE NOT RESPONSIBLE NOR LIABLE FOR ANY ADVICE, COURSE OF TREATMENT, DIAGNOSIS, OR ANY OTHER INFORMATION, SERVICES, OR PRODUCTS THAT YOU OBTAIN THROUGH THIS WEBSITE."
    )


if __name__ == "__main__":
    home()

