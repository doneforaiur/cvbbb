from pylatex.base_classes import Environment, CommandBase, Arguments
from pylatex.package import Package
from pylatex import Document, Section, Subsection, Command, UnsafeCommand
from pylatex.utils import NoEscape, italic

def info_to_cv(user_info):

    # ? Import packages, set rules
    doc = Document(documentclass = 'scrartcl' , document_options = ["paper=a4","fontsize=11pt"], fontenc=None, inputenc=None)
    doc.preamble.append(Command("usepackage", "babel","english"))
    doc.preamble.append(Command("usepackage", "inputenc", "utf8x"))
    doc.preamble.append(Command("usepackage","microtype", ["protrusion=true" , "expansion=true"]))
    doc.preamble.append(Command("usepackage", "amsmath"))
    doc.preamble.append(Command("usepackage", "amsfonts"))
    doc.preamble.append(Command("usepackage", "hyperref"))
    doc.preamble.append(Command("usepackage", "amsthm"))
    doc.preamble.append(Command("usepackage", "graphicx"))
    doc.preamble.append(Command("usepackage", "xcolor", "svgnames"))
    doc.preamble.append(Command("usepackage", "geometry"))
    doc.preamble.append(Command("usepackage", "url"))
    doc.preamble.append(Command("usepackage", "sectsty"))
    doc.preamble.append(Command("usepackage", "mdframed"))
    doc.append(Command('frenchspacing'))
    doc.append(Command('pagestyle', 'empty'))
    doc.append(Command("textheight=700px"))
    doc.append(Command("sectionfont", NoEscape(r"""\usefont{OT1}{phv}{b}{n} \sectionrule{0pt}{0pt}{-5pt}{3pt}""")))
    doc.append(Command("newlength",Command("spacebox")))
    doc.append(Command("settowidth",[Command("spacebox"), "8888888888"]))


    # ? Custom commands for entries
    sepspace = UnsafeCommand('newcommand', r'\sepspace',
                             extra_arguments=r"""
                             \vspace*{1em}""")

    MyName = UnsafeCommand('newcommand', r'\MyName', options=1,
                             extra_arguments=r"""
                            \Huge \usefont{OT1}{phv}{b}{n} \hfill #1
                            \par \normalsize \normalfont""")

    NewPart = UnsafeCommand('newcommand', r'\NewPart', options=1,
                             extra_arguments=r"""\section*{\uppercase{#1}}""")

    PersonalEntry = UnsafeCommand('newcommand', r'\PersonalEntry', options=2,
                             extra_arguments=r"""
                            \noindent\hangindent=2em\hangafter=0 % Indentation
                            \parbox{\spacebox}{        % Box to align text
                            \textit{#1}}               % Entry name (birth, address, etc.)
                            \hspace{1.5em} #2 
                            \par
                            """)

    SkillsEntry = UnsafeCommand('newcommand', r'\SkillsEntry', options=2,
                             extra_arguments=r"""
                            \noindent\hangindent=2em\hangafter=0 % Indentation
                            \parbox{\spacebox}{        % Box to align text
                            \textit{#1}}			   % Entry name (birth, address, etc.)
                            \hspace{1.5em} #2 \par    % Entry value 
                            """)

    EducationEntry = UnsafeCommand('newcommand', r'\EducationEntry', options=4,
                             extra_arguments=r"""
                                \noindent \textbf{#1} \hfill      % Study
                                \colorbox{Black}{%
                                    \parbox{6em}{%
                                    \hfill\color{White}#2}} \par  % Duration
                                \noindent \textit{#3} \par        % School
                                \noindent\hangindent=2em\hangafter=0 \small #4 % Description
                                \normalsize \par
                                """)

    WorkEntry = UnsafeCommand('newcommand', r'\WorkEntry', options=4,
                             extra_arguments=r"""
                            % Same as \EducationEntry
                            \noindent \textbf{#1} \hfill      % Jobname
                            \colorbox{Black}{\color{White}#2} \par  % Duration
                            \noindent \textit{#3} \par              % Company
                            \noindent\hangindent=2em\hangafter=0 \small #4 % Description
                            \normalsize \par 
                            """)


    doc.append(sepspace)
    doc.append(MyName)
    doc.append(NewPart)
    doc.append(PersonalEntry)
    doc.append(SkillsEntry)
    doc.append(EducationEntry)
    doc.append(WorkEntry)
    
    
    # Actual content
    doc.append(Command("MyName", user_info["first_name"] + " " + user_info["last_name"]))
    doc.append(Command('sepspace'))

    doc.append(Command('NewPart', ["Personal details", NoEscape("")]))

    if user_info["address"] != "":    
        doc.append(Command('PersonalEntry' , ["Address", user_info["address"]]))

    if user_info["phone"] != "":
        doc.append(Command('PersonalEntry', ["Phone", user_info["phone"]]))
    
    if user_info["personal_website"] != "":
        doc.append(Command('PersonalEntry', ["Website", NoEscape("\href{" + user_info["personal_website"] + "}{" + user_info["personal_website"] +"}")]))
    
    if user_info["github_link"] != "":
        doc.append(Command('PersonalEntry', ["Github", NoEscape("\href{" + user_info["github_link"] + "}{" + user_info["github_link"] +"}")]))
    
    if user_info["linkedin_link"] != "":
        doc.append(Command('PersonalEntry', ["LinkedIn", NoEscape("\href{" + user_info["linkedin_link"] + "}{" + user_info["linkedin_link"] +"}")]))
        
    
    
    if user_info["email"] != "":
        doc.append(Command('PersonalEntry', ["Mail", NoEscape("\href{mailto:" + user_info["email"] + "}{" + user_info["email"] +"}")]))

    if len(user_info["previous_workplace_info"]) > 0:
        doc.append(Command('NewPart', ["Work details", NoEscape("")]))

        for work_info in user_info["previous_workplace_info"]:
            doc.append(Command("WorkEntry",[work_info["position"], NoEscape(work_info["start_date"] + " - " + work_info["end_date"]),
                                            work_info["company_name"], work_info["description"]]))
            doc.append(Command('sepspace'))

    if len(user_info["previous_education_info"]) > 0:
        doc.append(Command('NewPart', ["Education details", NoEscape("")]))
    
        for education_info in user_info["previous_education_info"]:
            doc.append(Command("EducationEntry", [education_info["degree"], NoEscape(education_info["start_date"] + " - " + education_info["end_date"]),
                                                education_info["school_name"], education_info["description"]]))
            doc.append(Command('sepspace'))
    
    prev_lang = user_info["previously_used_programming_languages"]
    prev_frameworks = user_info["previously_used_frameworks"]
    prev_databases = user_info["previously_used_databases"]
    human_languages = user_info["human_languages"]
    
    if len(prev_lang) > 0 or len(prev_frameworks) > 0 or len(prev_databases) > 0 or len(human_languages) > 0:
        doc.append(Command('NewPart', ["Skills", NoEscape("")]))
    
    if len(prev_lang) > 0:
        doc.append(Command("SkillsEntry", ["Programming Languages", ", ".join(prev_lang)]))
        
    if len(prev_frameworks) > 0:
        doc.append(Command("SkillsEntry", ["Frameworks", ", ".join(prev_frameworks)]))
        
    if len(prev_databases) > 0:
        doc.append(Command("SkillsEntry", ["Databases", ", ".join(prev_databases)]))


    if len(human_languages) > 0:
        doc.append(Command("SkillsEntry", [ "Human Languages", "English (fluent)"]))
        for index ,lang in enumerate(human_languages):
            if index == 0:
                continue
            doc.append(Command("SkillsEntry", [ NoEscape(""), "Portuguese (fluent)"]))
    
    tex = doc.dumps()
    
    doc.generate_tex("./resume")
    doc.generate_pdf("./resume")
    
    return "./resume.pdf"


def info_to_cover_letter(user_info):
    doc = Document(documentclass = 'moderncv' , document_options = ["11pt","a4paper","roman"], fontenc=None, inputenc=None)
    
    doc.preamble.append(Command("usepackage", "babel","english"))
    doc.preamble.append(Command("usepackage", "inputenc", "utf8"))
    # \usepackage[scale=0.75]{geometry}
    doc.preamble.append(Command("usepackage", "geometry", "scale=0.75"))
    
    doc.append(Command("name", user_info["first_name"] + " " + user_info["last_name"]))
    if user_info["address"] != "":
        doc.append(Command("address", user_info["address"]))
    
    if user_info["phone"] != "":
        doc.append(Command("phone", user_info["phone"]))
    
    if user_info["email"] != "":
        doc.append(Command("email", user_info["email"]))
    
    doc.append(Command("begin", "document"))
    doc.append(Command("recipient", user_info["recipient"]))
    doc.append(Command("date", NoEscape(r"\today")))
    doc.append(Command("opening", user_info["opening"]))
    doc.append(Command("closing", user_info["closing"]))

    doc.append(Command("makelettertitle"))
    
    doc.append(user_info["letter_text"])
    
    doc.append(Command("vspace", "1cm"))
    
    doc.append(Command("makeletterclosing"))
    
    doc.append(Command("end", "document"))
    
    doc.generate_tex("./cover_letter")
    doc.generate_pdf("./cover_letter")
    
    return "./cover_letter.pdf"