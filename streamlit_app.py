import base64
import streamlit as st
from guidance_prompts import extract_info, suggest_improvements, improve_cv
from latex_templates import info_to_pdf

st.set_page_config(layout="wide")
user_input_area, pdf_area = st.columns(2, gap="medium")

if "pdf_path" not in st.session_state:
    st.session_state["pdf_path"] = "./place_holder.pdf"

if "generated_cv" not in st.session_state:
    st.session_state["generated_cv"] = False
    
if "user_info_json" not in st.session_state:
    st.session_state["user_info_json"] = {}

print(st.session_state)

with user_input_area:
    improvement_suggestions = st.empty()
    user_input_area_text = st.empty()
    user_input_area_button = st.empty()


    if st.session_state.generated_cv == False:
        user_info = user_input_area_text.text_area('Talk about yourself!', 'I am ...')
        if user_input_area_button.button('Generate CV!'):
            
            # user_info_json = extract_info(user_info)
            
            # ! don't burn money :^)
            user_info_json = {'first_name': 'John', 'last_name': 'Silver', 'email': 'me@johnsilver.com', 'phone': '', 'address': 'Palo Alto', 'personal_website': 'https://www.johnsilver.com', 'linkedin_link': 'https://www.linkedin.com/in/johnsilver', 'github_link': '', 'previous_education_info': [{'school_name': 'UCLA', 'degree': "Bachelor's Degree in Computer Science", 'start_date': '09/06', 'end_date': '06/10', 'description': 'Developed some Java aplications for the school.'}], 'previous_workplace_info': [{'company_name': 'Apple', 'position': 'Team Lead', 'start_date': '10/16', 'end_date': '', 'description': 'Working on a product that lets users generate a CV from their LinkedIn profile.'}, {'company_name': 'Google', 'position': 'Software Engineer', 'start_date': '10/11', 'end_date': '10/16', 'description': 'Worked on numerous projects including Speech to Text, Text to Speech, Large Language Models, and many more. Developed a special algorithm that can generate a song from a given picture.'}], 'previously_used_programming_languages': ['Python', 'C++', 'JavaScript'], 'previously_used_frameworks': ['React', 'Flutter'], 'previously_used_databases': ['MySQL', 'NoSQL'], 'human_languages': []}
            
            st.session_state["user_info_json"] = user_info_json
            
            suggested_improvements = [{'importancy': 'medium', 'type': 'workplace', 'description': 'Add more details to your work experience at Apple. For example, you can add bullet points like; Led a team of 5 developers to complete a project within a tight deadline. Collaborated with the design team to create a user-friendly interface.'}, {'importancy': 'high', 'type': 'programming_languages', 'description': 'Add more programming languages and frameworks to your list. Having experience with more than 3 programming languages and frameworks will make you a more versatile developer.'}, {'importancy': 'medium', 'type': 'education', 'description': 'Add more details to your education experience at UCLA. For example, you can add bullet points like; Participated in a hackathon and developed a web application that helps people find the nearest recycling center. Completed a research project on machine learning and presented it at a conference.'}, {'importancy': 'low', 'type': 'phone', 'description': 'Consider adding your phone number to your CV. This will make it easier for potential employers to contact you.'}, {'importancy': 'low', 'type': 'github_link', 'description': 'Consider adding your GitHub link to your CV. This will showcase your coding skills and projects to potential employers.'}, {'importancy': 'low', 'type': 'human_languages', 'description': 'Consider adding the languages you speak to your CV. This will show potential employers that you have good communication skills and can work with people from different backgrounds.'}]
            # suggested_improvements = suggest_improvements(user_info_json)
            print(suggested_improvements)
            
            st.write("Suggested improvements:")
            # generate multiple streamlit.info()
            for i in suggested_improvements:
                if i["importancy"] == "high":
                    st.error(i["description"])
                elif i["importancy"] == "medium":
                    st.warning(i["description"])
                elif i["importancy"] == "low":
                    st.info(i["description"])
                else:
                    st.success(i["description"])            
            
            # info_to_pdf(user_info_json)
            
            st.session_state["pdf_path"] =  "./resume.pdf"
            st.session_state["generated_cv"] = True

            user_input_area_button.empty()
            user_input_area_text.empty()


    if st.session_state.generated_cv == True:

        wanted_improvements = user_input_area_text.text_area('Dont like your output? Give some feedback', 'Make the ...')
        if user_input_area_button.button('Make some changes!'):
            st.session_state["user_info_json"]
            
            improved_user_info_json = improve_cv(st.session_state["user_info_json"], wanted_improvements)
            
            st.session_state["user_info_json"] = improved_user_info_json
            
            
            print(improved_user_info_json)
            # suggested_improvements = suggest_improvements(improved_user_info_json)
            
            # st.write("Suggested improvements:")
            # # generate multiple streamlit.info()
            # for i in suggested_improvements:
            #     if i["importancy"] == "high":
            #         st.error(i["description"])
            #     elif i["importancy"] == "medium":
            #         st.warning(i["description"])
            #     elif i["importancy"] == "low":
            #         st.info(i["description"])
            #     else:
            #         st.success(i["description"])
                    
            info_to_pdf(improved_user_info_json)
            
            st.write("Improving CV with your feedback...")

    if st.session_state["pdf_path"] == None:
        st.write("No PDF generated yet.")

with pdf_area:
    pdf_area = st.empty()
    with open(st.session_state["pdf_path"], "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    pdf_display = F'<iframe src="data:application/pdf;base64,{base64_pdf}" width="100%" height="1000" type="application/pdf"></iframe>'
    pdf_area.markdown(pdf_display, unsafe_allow_html=True)
