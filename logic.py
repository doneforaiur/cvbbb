from guidance_prompts import extract_info

def generate_pdf(user_input):
    user_info_json = extract_info(user_input)
    
    