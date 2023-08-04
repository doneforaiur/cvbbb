from guidance_prompts import extract_info
from latex_templates import info_to_pdf


def generate_pdf(user_input):
    user_info_json = extract_info(user_input)
    
    print(user_info_json)
    
    pdf_path =  info_to_pdf(user_info_json)
    
    return pdf_path

