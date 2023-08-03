import guidance
import os


if os.environ["OPENAI_API_KEY"] is None:
    print("OPENAI_API_KEY environment variable not set")
    os.exit(1)

guidance.llm = guidance.llms.OpenAI("gpt-3.5-turbo-0301", api_key=os.environ["OPENAI_API_KEY"])



def extract_info(user_input):
    
    # ? Example input
    # user_input = """Hello, my name is John Silver and I am 25 years old. I graduated UCLA in 2010 and I have started my professional 
    # career in October of 2011. I have worked as a software engineer at Google. I worked on numerous projects including Speech to Text, 
    # Text to Speech, Large Language Models, and many more. We developed a special algorithm that can generate a song from a given picture. 
    # After working at Google for 5 years, I switched to Apple as a Team Lead. I have been working at Apple for 3 years now. I'm currently 
    # working on a product that lets users generate a CV from their LinkedIn profile. I have a personal websitehttps://www.johnsilver.com 
    # and my LinkedIn profile is https://www.linkedin.com/in/johnsilver. My email is me@johnsilver.com.I've used Python, Java, C++, 
    # and JavaScript. I have a dog named Rex. I love to play tennis and I'm a big fan of the Lakers."""
    
    
    generate_one_json = guidance("""
    {{#system}} You extract and parse important information from given plain text to JSON format. 
    Place "" if the information is not provided or already in a list. Current year is 2023, convert relative dates to 03/2008 format.
    Template for the JSON output;
    {
        "first_name": "",
        "last_name": "",
        "age": "",  
        "email": "",
        "phone": "",
        "personal_website": "",
        "linkedin_link": "",
        "previous_education_info": [
            {
                "school_name": "",
                "degree": "",
                "start_date": "",
                "end_date": "",
                "description": ""
            }]
        "previous_workplace_info": [
            {
                "company_name": "",
                "position": "",
                "start_date": "",
                "end_date": "",
                "description": ""
            }]
    }
    {{/system}}
    {{#user}}
    Text to parse:
    "{{user_info}}"
    {{/user}}
    {{#assistant}}{{gen 'extracted_information' stop="\n\n"}}{{/assistant}}
    """)

    cv_information = generate_one_json(
        user_info=user_input
    )

    # ! TODO: Validate the JSON output
    json_data = eval(cv_information["extracted_information"])

    return json_data

def info_to_json_completion_based(user_input):
    generate_multiple_fields = guidance("""
    Extract and parse important information from given plain text to JSON format. Place "" if the information is not 
        provided or already in a list. Convert relative dates to 03/2008 format. Currently it's 2023.           
    User information: "{{user_info}}"
    JSON format:
    ```json
    {
        "first_name": "{{gen 'name' stop='"'}}",
        "last_name": "{{gen 'last_name' stop='"'}}",
        "age": "{{gen 'age' stop='"'}}",  
        "email": "{{gen 'email' stop='"'}}",
        "phone": "{{gen 'phone' stop='"'}}",
        "personal_website": "{{gen 'personal_website' stop='"'}}",
        "linkedin_link": "{{gen 'linkedin_link' stop='"'}}",
        "number_of_work_history_entries": {{gen 'number_of_work_history_entries' stop=','}},
        "number_of_education_entries": {{gen 'number_of_education_entries' stop=','}},
        
        "previous_workplace_company_name": [{{gen 'previous_workplace_company_name' num_iterations=3 stop=']'}}]
        "previous_workplace_position": [{{gen 'previous_workplace_position' num_iterations=3 stop=']'}}]
        "previous_workplace_start_date": [{{gen 'previous_workplace_start_date' num_iterations=3 stop=']'}}]
        "previous_workplace_end_date": [{{gen 'previous_workplace_end_date' num_iterations=3 stop=']'}}]
        "previous_workplace_description": [{{gen 'previous_workplace_description' num_iterations=3 stop=']'}}]
    }
    ```
    """)

    cv_information = generate_multiple_fields(
        user_info=user_input,
    )
    
    
    # ? The reason for multiple lists; guidance function does not support nested lists.
    json_data = {
        "first_name": cv_information["name"],
        "last_name": cv_information["last_name"],
        "age": cv_information["age"],
        "email": cv_information["email"],
        "phone": cv_information["phone"],
        "personal_website": cv_information["personal_website"],
        "linkedin_link": cv_information["linkedin_link"],
        "number_of_work_history_entries": cv_information["number_of_work_history_entries"],
        "number_of_education_entries": cv_information["number_of_education_entries"],
        "previous_workplace_company_name": cv_information["previous_workplace_company_name"],
        "previous_workplace_position": cv_information["previous_workplace_position"],
        "previous_workplace_start_date": cv_information["previous_workplace_start_date"],
        "previous_workplace_end_date": cv_information["previous_workplace_end_date"],
        "previous_workplace_description": cv_information["previous_workplace_description"],
    }
    
    return json_data