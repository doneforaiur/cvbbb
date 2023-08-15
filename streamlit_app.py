import base64
import time
import streamlit as st
from guidance_prompts import extract_info, suggest_improvements, improve_cv
from latex_templates import info_to_pdf

st.set_page_config(
    page_title="CV Builder but Better!",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': 'https://github.com/doneforaiur/cvbbb',
        'Report a bug': "https://github.com/doneforaiur/cvbbb/issues",
        'About': "# Want a CV but don't know how? You're in the right place!"
    }
)

user_input_area, pdf_area = st.columns(2, gap="medium")

if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = "./place_holder.pdf"

if "generated_cv" not in st.session_state:
    st.session_state["generated_cv"] = False
    
if "user_info_json" not in st.session_state:
    st.session_state["user_info_json"] = {}
    
if "generate_cover_letter" not in st.session_state:
    st.session_state["generate_cover_letter"] = False
    
if "job_listing" not in st.session_state:
    st.session_state["job_listing"] = ""


with user_input_area:
    improvement_suggestions = st.empty()
    user_input_area_text = st.empty()
    user_input_area_button = st.empty()

    if st.session_state.generated_cv == False:
        generate_cover_letter = st.checkbox('Generate a cover letter?', value=st.session_state["generate_cover_letter"], disabled=st.session_state["generate_cover_letter"])
        if generate_cover_letter:
            st.session_state["generate_cover_letter"] = True
        
        job_listing = user_input_area_text.text_area('Job listing', 'We are looking for ...')
        if user_input_area_button.button('Generate CV!', use_container_width=True):
            st.session_state["job_listing"] = job_listing


        user_info = user_input_area_text.text_area('Talk about yourself!', 'I am ...')
        if user_input_area_button.button('Generate CV!', use_container_width=True):
            
            with st.spinner('Extracting information from text...'):
                user_info_json = extract_info(user_info)
                st.session_state["user_info_json"] = user_info_json
                
            with st.spinner('Generating CV...'):
                info_to_pdf(user_info_json)
            
            st.session_state["pdf_path"] =  "./resume.pdf"
            st.session_state["generated_cv"] = True

            user_input_area_button.empty()
            user_input_area_text.empty()

    if st.session_state.generated_cv == True:
        wanted_improvements = user_input_area_text.text_area('Dont like your output? Give some feedback', 'Make the ...')
        if user_input_area_button.button('Make some changes!', use_container_width=True):
            with st.spinner('Improving CV with your feedback...'):
                improved_user_info_json = improve_cv(st.session_state["user_info_json"], wanted_improvements)
                st.session_state["user_info_json"] = improved_user_info_json
            
            with st.spinner('Regenerating CV...'):
                info_to_pdf(improved_user_info_json)

with pdf_area:
    with open(st.session_state["pdf_path"], "rb") as f:
        if st.session_state["pdf_path"] == "./place_holder.pdf":
            disabled = True
        else:
            disabled = False
        pdf_area.download_button(
            label="Download my CV!",
            data=f,
            file_name="resume.pdf",
            mime="application/pdf",
            use_container_width=True,
            disabled=disabled
        )
        
    with open(st.session_state["pdf_path"], "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="800" type="application/pdf"></iframe>'
    pdf_area.markdown(pdf_display, unsafe_allow_html=True)


# Get suggestions after the CV has been generated
# ? TODO: spinner appears on the very bottom, fix this
if st.session_state["generated_cv"] == True:
    with st.spinner('Generating suggestions...'):
        suggested_improvements = suggest_improvements(st.session_state["user_info_json"])
        time.sleep(1)
    
    user_input_area.write("Suggested improvements:")
    for i in suggested_improvements:
        if i["importancy"] == "high":
            user_input_area.error(i["description"])
        elif i["importancy"] == "medium":
            user_input_area.warning(i["description"])
        elif i["importancy"] == "low":
            user_input_area.info(i["description"])
        else:
            user_input_area.success(i["description"])
