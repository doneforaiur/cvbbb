import guidance
import os


if os.environ["OPENAI_API_KEY"] is None:
    print("OPENAI_API_KEY environment variable not set")
    os.exit(1)

guidance.llm = guidance.llms.OpenAI("text-ada-001", api_key=os.environ["OPENAI_API_KEY"])
# guidance.llm = guidance.llms.Transformers("stabilityai/stablelm-base-alpha-3b", device=0)

# define a guidance program that adapts proverbs
program = guidance("""
Extract important information from given plain text to JSON format. Leave blank if the information is not provided.
                   
User information: "{{user_info}}"

JSON format:
```json
{
    
    # PERSONAL INFORMATION
    
    "first_name": "{{gen 'name' stop='"'}}",
    "last_name": "{{gen 'last_name' stop='"'}}",
    "age": "{{gen 'age' stop='"'}}",  
    "email": "{{gen 'email' stop='"'}}",
    "phone": "{{gen 'phone' stop='"'}}",
    "personal_website": "{{gen 'personal_website' stop='"'}}",
    
    "number_of_work_history_entries": {{gen 'number_of_work_history_entries' pattern='[0-9]+' stop=','}},
    "number_of_education_entries": {{gen 'number_of_education_entries' pattern='[0-9]+' stop=','}},
    
    "all_used_softwares_and_frameworks": [{{gen 'all_used_softwares_and_frameworks' stop=']'}}],
    
    # WORK EXPERIENCE
    
    # ! TODO: loops doesnt work
    "work_experience": [{{#geneach 'items' num_iterations=2 join=', '}}
    {
        "company_name": "{{gen 'this' stop='"'}}",
        "position": "{{gen 'this' stop='"'}}",
        "start_date": "{{gen 'this' stop='"'}}",
        "end_date": "{{gen 'this' stop='"'}}",
        "description": "{{gen 'this' stop='"'}}",
        "location": "{{gen 'this' stop='"'}}"
    }
    {{/geneach}}]
    
}
```
""")

# execute the program on a specific proverb
executed_program = program(
    user_info="Hello, my name is John Silver and I am 25 years old. I have worked for Intel in Santa Cruz for 5 years starting in 2011 and then quit when I found a job at Apple. Now, I'm a Team Lead. I worked on developing Android projects and selling them.",
)

print(executed_program)
