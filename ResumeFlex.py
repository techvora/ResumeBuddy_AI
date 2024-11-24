import re
import json
import streamlit as st
from logical_functions import split_list, extract_json_data_from_response, groq_llm_model, google_llm_model
from pdf_format import create_resume_pdf, resume_text_from_pdf
from prompt import (first_resume_prompt, resume_instruction_prompt,
                    interview_question_prompt, ats_compatibility_prompt, resume_json_format,
                    interview_question_json_format, only_jd_through_resume_prompt, new_resume_json_format)



def resume_flex():
    logo_path = "images/logo_dark.png"
    st.logo(logo_path, icon_image=logo_path, link="https://www.inexture.com/")

    # favicon_path = "images/Yellow_Favicon.png"
    # st.set_page_config(page_title="Resume Flex AI", page_icon=favicon_path, layout="wide", menu_items=None, )

    any_action_occurs = False

    # STREAMLIT DESIGN
    col1, col2 = st.columns([2, 2])

    with col1:
        header = st.container()
        header.title("Resume Optimizer")
        header.write("""<div class='fixed-header'/>""", unsafe_allow_html=True)

        # STORE JD AS USER INPUTS IN VARIABLES
        jd = st.text_area("Enter Job Description (JD)", height=200,
                          placeholder="Enter Job Description(JD) in proper formatting")

        # GET RESUME AS PDF FROM USER INPUTS AND STORE IN VARIABLES
        resume = st.file_uploader("Upload your resume", type=['pdf', 'docx', 'doc'], label_visibility="collapsed",
                                  help="Upload your resume here. Max size: 200MB")

        with st.container():
            columns1, columns2 = st.columns([5, 5, ])
            with columns1:
                ats_btn = st.button("Know ATS %", key="ats")
                if ats_btn:
                    any_action_occurs = True
            with columns2:
                questions_btn = st.button("Get Interview Question", key='questions')
                if questions_btn:
                    any_action_occurs = True

            with st.container():
                columns1, columns2 = st.columns([5, 5, ])
                with columns1:
                    resume_optimize_btn = st.button("Optimize Resume", key='resume')
                    if resume_optimize_btn:
                        any_action_occurs = True

                with columns2:
                    new_resume_btn = st.button("Build a new Resume", key='new_resume')
                    if new_resume_btn:
                        any_action_occurs = True

    with col2:
        st.markdown('<div class="custom-col2">', unsafe_allow_html=True)
        st.image("images/illustrations.png")
        st.markdown('</div>', unsafe_allow_html=True)


#===================================================Session_state_initialization===============================================

    # Initialize session state for content input
    if "optimize_resume_data" not in st.session_state:
        st.session_state.optimize_resume_data = None
    if "resume_data" not in st.session_state:
        st.session_state.resume_data = None
    if "ats_data" not in st.session_state:
        st.session_state.ats_data = None
    if "questions_data" not in st.session_state:
        st.session_state.questions_data = None

#===================================================Display_data_functions====================================================

    display_compare = False

    # DISPLAY JSON DATA OF RESUME AS STRUCTURED  FORMAT ON STREAMLIT
    def display_resume(resume_json_response):

        st.write("---")
        with st.container():
            col_1, col_2 = st.columns(2)

            with col_1:
                # Display ATS Score if display_compare is set to True
                if display_compare == "None":
                    st.header(f"Final ATS Score: {resume_json_response.get('final_ATS_score', 'N/A')}")

            with col_2:
                # Generate PDFs and download buttons
                b1, b2 = st.columns(2)
                with b1:

                    freelance_resume_output = create_resume_pdf("freelancer", resume_json_response)

                    # freelance = st.download_button(
                    st.download_button(
                        label="Freelancer Resume",
                        data=freelance_resume_output.encode('latin-1'),
                        file_name="Freelancer_Resume.pdf",
                        key = "freelance",
                        mime="application/pdf"
                    )
                    # if freelance:

                with b2:
                    experience_resume_output = create_resume_pdf("Agency", resume_json_response)
                    # experience = st.download_button(
                    st.download_button(
                        label="Experience Resume",
                        data=experience_resume_output.encode('latin-1'),
                        file_name="Experience_Resume.pdf",
                        key = "experience",
                        mime="application/pdf"
                    )

        # PERSONAL DETAIL
        st.header("Personal Details : ")
        # personal_details = resume_json_response.get("personal_details", {})
        details = st.session_state.resume_data.get("personal_details", {})

        new_name = st.text_input("Want to change your Name enter below:", details.get("name", ""))
        new_position = st.text_input("Want to change Position enter below:", details.get("position", ""))

        st.session_state.resume_data["personal_details"]["name"] = new_name
        st.session_state.resume_data["personal_details"]["position"] = new_position


        # INTRODUCTION
        st.header("Introduction")
        introduction = resume_json_response.get("introduction", "")
        st.write(introduction)

        # SUMMARY
        st.header("Summary")
        for summary_points in resume_json_response.get("summary", []):
            st.write(f"- {summary_points}")

        # TECHNICAL SKILL
        st.write("----")
        st.header(f"Technical Skills")
        technical_skills = resume_json_response.get(f"technical_skills", {})
        for category, skills in technical_skills.items():
            category = category.replace("_", " ")

            if skills:
                category = category if category == "IDEs" else category.capitalize()
                st.subheader(category)
                skill_chunks = split_list(skills, 4)
                columns = st.columns(4)
                for col, chunk in zip(columns, skill_chunks):
                    with col:
                        st.markdown("\n".join([f"- {skill}" for skill in chunk]))

        st.write("---")
        # PROJECTS
        st.header("Projects")
        projects = resume_json_response.get("projects", {})

        for project_name, project_details in projects.items():
            with st.container():
                col_a, col_b = st.columns([1, 1])
                with col_a:
                    st.subheader(project_name)
                st.empty()
                with col_b:
                    st.write("")
                    # st.html(f"<span><strong>Timeline </strong>: {project_details.get('timeline', 'N/A')} </span>")
            st.write(f"**Description**: {project_details.get('description', 'N/A')}")
            if "Not" not in project_details["responsibilities"]:
                st.write("**Responsibilities**:")
                for responsibility in project_details.get("responsibilities", []):
                    st.write(f"- {responsibility}")
            st.write("**Skills**: " + ", ".join(project_details.get("skills", [])))
            st.write("---")
        if "education" in resume_json_response and resume_json_response["education"]:
            st.write("**Education**:")
            for education, details in resume_json_response["education"].items():
                if details:
                    details_str = ', '.join(details)
                    st.write(f"- {education} :- {details_str}")

        if any(key in resume_json_response for key in ["certificate", "certifications"]):
            st.write("**Certifications**:")
            for certificate in resume_json_response.get("certifications", {}).items():
                st.write(f"- {certificate} ")

        if display_compare == True:

            # COMPARISON HIGHLIGHTS
            st.header("Comparison Highlights")
            comparison_highlights = resume_json_response.get("comparison_highlights", {})

            with st.container():
                col_x, col_y = st.columns(2)
                with col_x:
                    st.header("Original Resume")

                    # ats_comparison = comparison_highlights.get("original_resume", {})
                    # st.subheader(f"Initial ATS: {ats_comparison.get('Initial_ATS', 'N/A')}")

                    original_resume = comparison_highlights.get(f"original_resume", {})
                    st.markdown(f"<p><strong>Summary:</strong> {original_resume.get('summary', 'N/A')}</p>",
                                unsafe_allow_html=True)
                    st.markdown(
                        f"<p><strong>Technical Skills:</strong> {original_resume.get('technical_skills', 'N/A')}</p>",
                        unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Projects:</strong> {original_resume.get('projects', 'N/A')}</p>",
                                unsafe_allow_html=True)

                with col_y:
                    st.header("Optimized Resume")

                    # ats_comparison = comparison_highlights.get("Optimized_Resume", {})
                    # st.subheader(f"Final ATS: {ats_comparison.get('Final_ATS', 'N/A')}")

                    optimized_resume = comparison_highlights.get("optimized_resume", {})
                    st.markdown(f"<p><strong>Summary:</strong> {optimized_resume.get('summary', 'N/A')}</p>",
                                unsafe_allow_html=True)
                    st.markdown(
                        f"<p><strong>Technical Skills:</strong> {optimized_resume.get('technical_skills', 'N/A')}</p>",
                        unsafe_allow_html=True)
                    st.markdown(f"<p><strong>Projects:</strong> {optimized_resume.get('projects', 'N/A')}</p>",
                                unsafe_allow_html=True)

            irrelevant_info = resume_json_response.get("Irrelevant", {}).get("list_of_irrelevant_sections", [])

            if irrelevant_info and isinstance(irrelevant_info, list):
                st.header("Irrelevant Information")
                for item in irrelevant_info:
                    st.write(f"- {item}")
                st.write("---")

        # st.rerun()



    # DISPLAY JSON DATA OF ATS COMPATIBILITY AS STRUCTURED FORMAT ON STREAMLIT
    def display_ats_info(ats_json_response):
        st.write("---")
        st.header("ATS Compatibility")

        # ATS SCORE
        ats_score = ats_json_response.get("ATS_score")
        if ats_score:
            st.subheader(f"ATS Score: {ats_score}")
        else:
            st.warning("No ATS score available.")

        # MISSING KEYWORDS
        missing_keywords = ats_json_response.get("missing_keywords", [])
        if missing_keywords:
            st.subheader("Missing Keywords")
            columns = st.columns(4)

            # SPLIT THE LIST INTO CHUNKS
            keyword_chunks = split_list(missing_keywords, 4)

            # DISPLAY EACH CHUNK IN RESPECTIVE COLUMN
            for col, chunk in zip(columns, keyword_chunks):
                with col:
                    st.markdown("\n".join([f"- {kw}" for kw in chunk]))
        else:
            st.write("No missing keywords found.")

        # LIST OF CHANGES
        changes = ats_json_response.get("list_of_changes", {})
        if changes:
            st.header("Suggested Changes")
            for section, suggestions in changes.items():
                if suggestions:
                    st.subheader(f"**{section.capitalize()}**")
                    st.write(suggestions)
                    st.write("---")
        else:
            st.write("No changes suggested.")


    # DISPLAY JSON DATA OF INTERVIEW QUESTIONS AS STRUCTURED FORMAT ON STREAMLIT
    def display_questions(question_json_response):
        st.write("---")
        st.header("Interview Questions")

        # LIST OF QUESTIONS
        qa_response = question_json_response.get("interview_questions", [])

        # ITER THROUGH DISPLAY ALL THE QUESTION
        for index, question in enumerate(qa_response, start=1):
            st.write(f"{index}. {question}")


#===================================================Display_data_functions====================================================


    # STREAMLIT DISPLAYED CONTENTS
    with st.container():

        # TAKE OUT RESUME DATA AS TEXT FROM PDF
        resume_txt = resume_text_from_pdf(resume)


        # BUTTON TO GENERATE RESUME
        if resume_optimize_btn:
            display_compare = True

            st.session_state.questions_data = None
            st.session_state.resume_data = None
            st.session_state.ats_data = None

            if resume and jd:
                with st.spinner('Preparing Resume...'):

                    # FUNCTION CALL TO GET PROMPT FOR BUILD RESUME
                    instruction = resume_instruction_prompt.format(json_format=resume_json_format)
                    resume_prompt = first_resume_prompt.format(JD=jd, resume_txt=resume_txt, instruction=instruction, )

                    # CALL LLM FUNCTION TO GENERATE OPTIMIZED RESUME
                    resume_str_response = google_llm_model(resume_prompt)

                    # # FUNCTION CALL TO REVALIDATE RESUME RESPONSE THROUGH LLM MODEL

                    # validated_resume_prompt = revalidate_resume_prompt.format(JD=JD, resume_txt=resume_str_response, instruction=instruction,)
                    # validated_resume_str_response = llm_model(validated_resume_prompt)


                    llm_resume_str_response = re.sub("[’‘]", "'", resume_str_response)
                    llm_resume_str_response = re.sub("`", "", llm_resume_str_response)

                    only_json_data = extract_json_data_from_response(llm_resume_str_response)
                    print(f"______________only json data after remove extra data____________\n\n{only_json_data}\n\n")

                    try:
                        # LOAD RESPONSE AS JSON
                        st.session_state.resume_data = json.loads(only_json_data)

                    except Exception as e:
                        print(f"error while {e}")
                        st.write(e)
                        st.error("Please try again we can't able to load json...")
            else:
                st.error("JD and Resume field's are required")

        # DISPLAY JSON DATA AS STRUCTURED ON STREAMLIT
        if st.session_state.optimize_resume_data is not None:
            display_resume(st.session_state.optimize_resume_data)


        # BUTTON TO GENERATE INTERVIEW QUESTIONS
        if questions_btn:
            st.session_state.resume_data = None
            st.session_state.ats_data = None
            st.session_state.optimize_resume_data = None

            if resume:
                with st.spinner("Generating Questions..."):

                    # FUNCTION CALL TO GET PROMPT FOR GENERATE INTERVIEW QUESTIONS
                    question_prompt = interview_question_prompt.format(resume=resume_txt, qa_json_format=interview_question_json_format)

                    # CALL LLM FUNCTION TO GENERATE QUESTIONS
                    questions_response = groq_llm_model(question_prompt)
                    llm_questions_response = re.sub("[’‘]", "'", questions_response)
                    llm_questions_response = re.sub("`", "", llm_questions_response)

                    only_json_data = extract_json_data_from_response(llm_questions_response)
                    print(f"______________after remove extra data__________\n{only_json_data}\n\n")

                    try:
                        # LOAD RESPONSE AS JSON
                        st.session_state.questions_data = json.loads(only_json_data)

                    except Exception as e:
                        print(f"Got error while data load into json___________________\n{e}\n\n")
                        st.error("Upload resume if it's already uploaded then re upload it")
            else:
                st.error("Resume field is required")

        # DISPLAY JSON DATA AS STRUCTURED ON STREAMLIT
        if st.session_state.questions_data is not None:
            display_questions(st.session_state.questions_data)


        # BUTTON TO KNOW ATS SCORE & MISSING KEYWORDS
        if new_resume_btn:
            st.session_state.questions_data = None
            st.session_state.ats_data = None
            st.session_state.optimize_resume_data = None

            if jd:
                # DEFAULT LOADER..
                with st.spinner("Preparing a Resume..."):

                    # KNOW ATS SCORE FROM LLM
                    new_resume_prompt = only_jd_through_resume_prompt.format(JD=jd, json_format=new_resume_json_format)

                    # CALL LLM FUNCTION TO GENERATE OPTIMIZED RESUME
                    new_resume_response = groq_llm_model(new_resume_prompt)
                    llm_new_resume_response = re.sub("[’‘]", "'", new_resume_response)
                    llm_new_resume_response = re.sub("`", "", llm_new_resume_response)

                    only_json_data = extract_json_data_from_response(llm_new_resume_response)
                    print(f"______________after remove extra data__________\n{only_json_data}\n\n")

                    try:
                        # LOAD RESPONSE AS JSON
                        st.session_state.resume_data = json.loads(only_json_data)


                    except Exception as e:
                        print(f"\n\n___________________Got error while data load into json{e}\n\n")
                        st.error("Please try again...")
            else:
                st.error("JD is required to build a new resume")

        # DISPLAY JSON DATA AS STRUCTURED ON STREAMLINE
        if st.session_state.resume_data is not None:
            display_resume(st.session_state.resume_data)


        # BUTTON TO KNOW ATS SCORE & MISSING KEYWORDS
        if ats_btn:
            st.session_state.questions_data = None
            st.session_state.resume_data = None
            st.session_state.optimize_resume_data = None

            if resume and jd:
                # DEFAULT LOADER..
                with st.spinner("Checking ATS..."):

                    # KNOW ATS SCORE FROM LLM
                    ats_prompt = ats_compatibility_prompt.format(JD=jd, resume=resume_txt)

                    # CALL LLM FUNCTION TO GENERATE OPTIMIZED RESUME
                    ats_response = groq_llm_model(ats_prompt)
                    llm_ats_response = re.sub("[’‘]", "'", ats_response)
                    llm_ats_response = re.sub("`", "", llm_ats_response)

                    only_json_data = extract_json_data_from_response(llm_ats_response)
                    print(f"______________after remove extra data__________\n{only_json_data}\n\n")

                    try:
                        # LOAD RESPONSE AS JSON
                        st.session_state.ats_data = json.loads(only_json_data)

                    except Exception as e:
                        print(f"\n\n___________________Got error while data load into json{e}\n\n")
                        st.error("Please try again...")
            else:
                st.error("JD and Resume field's are required")

        # DISPLAY JSON DATA AS STRUCTURED ON STREAMLINE
        if st.session_state.ats_data is not None:
            display_ats_info(st.session_state.ats_data)


#======================================================CSS=================================================================


    st.markdown(
        f"""
        <style>
            .st-emotion-cache-9ycgxx::after{{
                content: ' (Resume Only)' !important;
                font-size: 16px;
            }}
            textarea{{
                line-height:1.7 !important;
                letter-spacing : 0.5px ;
                font-size : 18px !important;
            }}
            p {{
                font-size : 22px;
            }}
            label [data-testid="stMarkdownContainer"] p{{
                font-size : 16px;
            }}
            .st-emotion-cache-nok2kl li  {{
                font-size : 20px;
            }}
            .st-emotion-cache-183lzff{{
                font-family : "Source Sans Pro", sans-serif;
                font-size : 16px;
            }}
            .stDownloadButton{{
                display : flex;
                justify-content : end;
                padding : 7px 0px;
            }}
            .stDownloadButton button {{
                background : orange;
                color : white;
                width : 80%;
                padding : 10px;
            }}
            .st-emotion-cache-15hul6a:hover{{
                border-color : orange;
                color : orange;
            }}
            .stDownloadButton button:hover {{
                background-color : orange;
                border-color : orange;  
                color : white;
                padding :10px;
                width : 80%;
            }}
            .stHtml{{
                display : flex;
                justify-content : end;
                font-size : 20px;
            }}
            .st-emotion-cache-15hul6a:active{{
                background-color : orange;
                border-color : orange;
                color : white;
            }}
            .st-emotion-cache-15hul6a:focus:not(:active){{
                border-color : orange;
                color : white;
            }}
            .stButton button {{
                width : 100%;
                background-color : orange;
                color : white;
                padding :10px;
            }}
            .stButton button:hover {{
                width : 100%;
                background-color : orange;
                border-color : orange;  
                color : white;
                padding :10px;
            }}
           .st-emotion-cache-u8hs99{{
                padding : 20px 0px;
           }}
            .st-emotion-cache-12118b6 p {{
                font-weight : 600
            }}

            st-emotion-cache-ocqkz7 [data-testid="stVerticalBlockBorderWrapper"] {{
                padding : 10rem;
            }}
            .stButton{{
                width : auto;
            }}
             .fixed-header {{
                border-bottom: 1.5px solid gray;
            }}
             .stAppViewContainer ::-webkit-scrollbar {{
              display: none;
            }}
            .st-emotion-cache-1jicfl2{{
                padding : 5rem;
               {"height: 100%;" if any_action_occurs == False else ""}
                # display : flex;
                align-items : center;
            }}
            .st-emotion-cache-183lzff{{
                font-size : 28px;
                font-weight : 600;
            }}
            .st-emotion-cache-1rsyhoq li  {{
                font-size : 18px;
            }}
            .st-emotion-cache-17sc1v6{{
                height : 2.2rem;
            }}
            .st-emotion-cache-gi0tri{{
                display : none !important; 
            }}
            h2{{
                color : orange;
            }}
            .st-emotion-cache-1kyxreq{{
                justify-content : center
            }}

            [data-testid="stImageContainer"] img {{
                height : 660px;
            }}
            [data-testid="stVerticalBlockBorderWrapper"]{{
                margin-top : 1%;
            }}
            [data-testid="stVerticalBlockBorderWrapper"]{{
                letter-spacing : 0.5px;
            }}
            [data-testid="stSidebarHeader"] img{{  
                width : 220px;     
                height : 35px; 
            }}
            .st-cc {{
                border-bottom-color : orange;
            }}
            .st-cb {{
                border-top-color : orange;
            }}
            .st-ca {{
                border-right-color : orange;
            }}
            .st-c9 {{
                border-left-color : orange;
            }}
            header [data-testid="stToolbar"]{{
                display : none;
            }}

            @media(max-width : 768px){{
                 [data-testid="stFullScreenFrame"]{{
                    display : none;
                }}
                 div[data-testid="stHorizontalBlock"]:nth-child(2){{
                    display : none;
                }}

                .stHtml{{
                    justify-content : start;
                }}
                button {{
                    width : 100% !important;
                }}
                .st-emotion-cache-keje6w.e1f1d6gn3:nth-of-type(3) {{
                    display: none;
                }}
                 .st-emotion-cache-17sc1v6{{
                    height : 1.75rem;
                }}
                .st-emotion-cache-1jicfl2 {{
                    padding : 4rem 1.2rem 0rem;
                    height : auto;
                    margin-top : 5%;
                }}
                .stButton button {{
                    width : 100% !important;
                    padding : 15px !important;
                    font-size: 16px !important;
                }}
                textarea {{
                    width : 100% !important;
                }}

                p {{
                    font-size : 18px !important;
                }}
                h2 {{
                    font-size : 24px !important;
                }}
                .st-emotion-cache-183lzff{{
                    font-size : 22px;
                }}
                .st-emotion-cache-12118b6 p {{
                    font-size: 14px;
                    line-height: 1.5 !important;
                }}
                .st-emotion-cache-1rsyhoq li {{
                    font-size : 16px !important;
                }}
                 [data-testid="stSidebarCollapsedControl"] img {{
                    width: 180px !important;
                    height: 30px !important;
                    margin-top:5% !important;
                }}
            }}
        </style>
        """,
        unsafe_allow_html=True
    )

# resume_flex()