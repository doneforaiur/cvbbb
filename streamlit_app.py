import base64
import streamlit as st
from guidance_prompts import extract_info
from latex_templates import info_to_pdf

st.set_page_config(layout="wide")
user_input_area, pdf_area = st.columns(2, gap="medium")

st.session_state.cv_generated = False
st.session_state.generate_cv = False
st.session_state.pdf_path = None

with user_input_area:
    user_info = st.text_area('Talk about yourself!', 'I graduated from ...')
    if st.button('Generate CV!'):
        with st.spinner('Wait for it...'):
            st.session_state.generate_cv = True
            
            user_info_json = extract_info(user_info)
            
            # ! don't burn money :^)
            # user_info_json = {'first_name': 'John', 'last_name': 'Silver', 'email': 'me@johnsilver.com', 'phone': '', 'address': 'Palo Alto', 'personal_website': 'https://www.johnsilver.com', 'linkedin_link': 'https://www.linkedin.com/in/johnsilver', 'github_link': '', 'previous_education_info': [{'school_name': 'UCLA', 'degree': "Bachelor's Degree in Computer Science", 'start_date': '09/06', 'end_date': '06/10', 'description': 'Developed some Java aplications for the school.'}], 'previous_workplace_info': [{'company_name': 'Apple', 'position': 'Team Lead', 'start_date': '10/16', 'end_date': '', 'description': 'Working on a product that lets users generate a CV from their LinkedIn profile.'}, {'company_name': 'Google', 'position': 'Software Engineer', 'start_date': '10/11', 'end_date': '10/16', 'description': 'Worked on numerous projects including Speech to Text, Text to Speech, Large Language Models, and many more. Developed a special algorithm that can generate a song from a given picture.'}], 'previously_used_programming_languages': ['Python', 'C++', 'JavaScript'], 'previously_used_frameworks': ['React', 'Flutter'], 'previously_used_databases': ['MySQL', 'NoSQL'], 'human_languages': []}
            
            st.write("Information extracted. Generating PDF...")
            
            pdf_path =  info_to_pdf(user_info_json)
                        
            st.session_state.pdf_path = pdf_path
            st.session_state.cv_generated = True

with pdf_area:
    if st.session_state.cv_generated:
        with open("resume.pdf", "rb") as f:
            base64_pdf = base64.b64encode(f.read()).decode('utf-8')

        pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
        st.markdown(pdf_display, unsafe_allow_html=True)