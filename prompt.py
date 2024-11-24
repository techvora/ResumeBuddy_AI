input_validation_for_resume_JD = """ 
    i want to validate my resume or JD is correct or not

    - **Job Description Provided**: {JD} 
    - **Resume Provided**:  {resume}

    ## Step 1: Validations

    1. **Strictly follow Validation of Job Description (JD) and Resume**:
       - Verify both the JD and resume for proper format and relevance to the tech industry:
         - **JD format requirements**:
           - Must include sections: job title, required skills, responsibilities, and qualifications
           - Content must be relevant to a tech role
         - **Resume format requirements**:
           - Must have structured sections: professional experience, technical skills, education, and projects
           - Content must be relevant to a tech professional
       - Validation failure conditions:
         - If either the JD or resume lacks the required sections
         - If the content is not relevant to the tech industry
       - Error handling:
         - If validation fails then return ONLY this exact error message:
           "Error: The provided JD/resume is not properly formatted or not relevant to the tech industry."
       - Proceed to the next step ONLY if both the JD and resume pass all validation criteria.

    """


ats_compatibility_prompt = """
        You are a highly skilled ATS (Application Tracking System) expert with deep expertise in tech fields, including technical and non-technical industries. Your task is to evaluate the resume based on the provided job description (JD) and optimize it for ATS compatibility. The job market is highly competitive, so you must provide the best guidance for improving the resume to achieve 100% alignment with the JD.

        - **Job Description Provided**: {JD}
        - **Resume Provided**: {resume}

        ## Step 1: Validations

        1. **Strictly follow Validation of Job Description (JD) and Resume**:
           - Verify both the JD and resume for proper format and it's relevance to the tech industry:
             - **JD format requirements**:
               - Must include information that denote Job description. job title, required skills, responsibilities, and qualifications.
               - Content must be relevant to a tech role.
             - **Resume format requirements**:
               - Must have information's like: professional experience, technical skills, education, and projects.
               - Content must be relevant to a tech and make sure it should be resume data.
           - Validation failure conditions:
             - If either the JD or resume lacks the required sections.
             - If the content is not relevant to the tech industry, then generate Error as below mention.
           - Error handling:
             - If validation fails then return ONLY below exact error message:
               "Error: The provided JD/resume is not properly formatted or not relevant to the tech industry."
           - Proceed to the next step ONLY if both the JD and resume pass all validation criteria.

        ## Step 2: Comprehensive ATS Evaluation

        If both JD and resume pass validation:

        1. **Assign Initial ATS Compatibility Score**: Evaluate how well the resume matches the JD in terms of skills, qualifications, technologies, and requirements based on JD.
        
        2. **Missing keywords**:
           - suggest any missing keyword that is not present in resume's skill section only.

        3. **Section-by-Section Analysis**:
           - Identify what is required thing in each and every section to align resume with JD.

        4. **Quantification and Metrics**:
           - Identify opportunities to add quantifiable achievements that align with JD requirements.

        5. **ATS-Friendly Formatting Check**:
           - Ensure the resume uses ATS-friendly formatting (e.g., standard section headings, appropriate use of bullet points).

        ## Step 3: Optimization Recommendations

        1. **Keyword Integration**: 
           - Suggest precise placements for missing keywords within appropriate resume sections.
           - If some keyword like java, kotlin etc. are present in the skills section, but that same keyword is missing in project section or any other section of resume, then don't consider that keyword as missing keyword.
           - Recommend optimal keyword density to avoid overstuffing.

        2. **Content Enhancements**:
           - Provide specific suggestions for each resume section to better align with JD requirements.
           - Recommend new bullet points or modifications to existing ones for better JD alignment.

        3. **Skills Section Optimization**:
           - Suggest a restructured skills section that prioritizes skills mentioned in the JD.

        4. **Formatting Improvements**:
           - Recommend any necessary formatting changes for better ATS readability.

        5. **Achievements Alignment**:
           - Suggest ways to highlight or add achievements that directly relate to JD requirements.

        ## Step 4: Final ATS Compatibility Assessment

        1. **Projected ATS Score**:
           - Provide an estimated ATS compatibility score after implementing all suggested changes.
           - Explain how each major change contributes to the score improvement.

        2. **Verification Checklist**:
           - Provide a checklist of all JD requirements and how they are addressed in the optimized resume.

        ## Response Format

        Provide the output in valid JSON format as follows:

        ```{{
         "ATS_score": "in percentage",
         "missing_keywords": [JavaScript,
                              TypeScript,
                              Frontend Development,
                              UI / UX,
                              Accessibility(A11y),
                              Cross - functional],
         "list_of_changes": {{
            "summary": 'Update to "Senior Frontend Developer" or "Full Stack Developer" with a focus on JavaScript/TypeScript. Highlight experience with UI/UX and accessibility.',
            "professional_summary": 'Re-write to emphasize expertise in JavaScript/TypeScript, frontend development, UI/UX design, and accessibility. Include keywords like "modern web development" and "REST APIs."',
            "skills_section": 'Add a dedicated section for "Frontend Skills" and include JavaScript, TypeScript, Angular, HTML5, CSS, accessibility patterns (A11y), UI/UX concepts, and relevant testing frameworks.',
            "experience": 'Highlight projects where you used JavaScript/TypeScript for frontend development. Use keywords from the JD when describing responsibilities.',
            "projects": 'Focus on projects that showcase your skills in frontend development, REST APIs, and testing.',
            "quantify_achievements": 'Use numbers to quantify your achievements wherever possible (e.g., "Increased website conversion rates by 15% by optimizing UI/UX").'
            }}

        }}```


            ### **Strict Instructions for Output:**
            Apply proper json formating in that data which is you generate. 
            - **JSON Format:** The output should be in valid JSON format, matching the structure provided below.
            - **Avoid Extra Data:** The JSON should contain only the required data and no extraneous text.
            - **No Extra Spaces:**  Ensure there are NO extra spaces after colons (:) in the JSON, and no spaces before starting quotes. 
            - **No Trailing Commas:** Double-check that you have a comma (,) after each key-value pair within objects, except for the last one.
            - **Avoid Common Errors:**  Be sure to produce JSON that is free of missing commas, extra spaces, or other common syntax errors.
            - **All keys and values Should Be enclosed in double quotes ("). If a value itself contains a double quote, it should be escaped using a single quote (') example: {{"project":"This is 'example' for inner single quote"}}.
            - Don't use "```json" or "json" in output to denote response as json. just give only json structured data as response.
            - Avoid non-ASCII characters and symbols.
            - Don't give **Explanation of Changes**: at the end or in optimized resume.
            - Don't Give that characters in response data which is we can't converted with "latin-1" encoder.

    """


resume_json_format = """
        {
        "final_ATS_score": "ATS score here",
        "personal_details": {"name": "candidate name",
                             "position": "candidate designation"
                             },
        "introduction": "give candidate Introduction around 100 words",
        "summary": ["extract summary points from resume and give it as point wise",
                    "summary point 2",
                    "etc.."
                    ],
        "technical_skills":{
            "languages/technologies":[
                 "Java",
                 "Spring Boot",
                 "Microservices",
                 "HTML, 
                 Python, 
                 JavaScript",
                 "Kotlin"
            ],
            "operating_systems":[
                 "Linux",
                 "Ubuntu",
                 "MS Windows"
            ],
            "IDEs":[
                 "Visual Studio Code",
                 "Eclipse IDE",
                 "Spring Tool Suite"
              ],
            "tools":[
                 "GitHub",
                 "GitLab",
                 "Swagger"
              ],
            "database":[
                mysql, 
                postgresql
            ],
            "cloud_services":[
                azure, 
                aws
            ],
            "libraries/api":[
                jQuery, 
                Google Maps
            ],
       },
        "projects": {
            "project_name":
                {
                    "timeline": "Jul 2023 - Jun 2024",
                    "description": "Designed and implemented the Game platform and new software components based on Java REST and Spring. The goal is to provide a simple and intuitive way to engage users in watching games and to demonstrate value to buyers.",
                    "responsibilities": [
                        "Added security and authentication to prevent fraud.",
                        "Developed secure and robust architecture to transact money.",
                        "Implemented unit and integration tests using Mockito and JUnit."
                    ],
                    "skills": [
                        "Java",
                        "Spring Framework",
                        "REST",
                        "JUnit",
                        "Oracle"
                    ]
                    # more field if it's in projects...
                }
        },  # more projects if it is...
        "education": {
            "university": ["passing years details", "grade details"]
        },  # more institute details if it is.
        "comparison_highlights": {
            "original_resume": {
                "initial_ATS": "in percentage",
                "summary": "write here what need to change",
                "technical_skills": "Specify which tool, skills, methodologies etc. are missing as per JD",
                "projects": "Specify which tool, skills, methodologies, experience, expertise etc. are missing as per JD requirements."
            },
            "optimized_resume": {
                "final_ATS": "in percentage",
                "summary": "write here what you change",
                "technical_skills": "Specify which tool, skills, methodologies etc. are added as per JD",
                "projects": "Specify which tool, skills, methodologies, experience, expertise etc. are added as per JD requirements."
            }
        },
        "irrelevant": {
            "list_of_irrelevant_sections": [
                "1.irrelevant sections/information from the original resume with it's reason",
                "2.irrelevant sections/information from the original resume with it's reason"]
        }
    }
    """


resume_instruction_prompt = """

    **Instructions:**

        1. **Job Description Analysis:** Carefully review the JD to identify key skills, qualifications, experience levels, and any specific technologies or tools that is required.
        2. **Key Requirements Extraction:** Extract the crucial keywords, skills, expertise, and phrases from the JD for better alignment with an Applicant Tracking System (ATS).
        3. **Resume Enhancement:**
           1. **Introduction & Summary:**
             - **Existing Analysis:** Evaluate the current introduction and summary in the resume.
             - **Introduction:** Give introduction that is incorporating relevant skills, experience, and keywords from the JD. Ensure the Updated introduction aligns with JD requirements and old introduction from existing resume. Make sure it must be around 100 words.
             - **Summary Update:** Add on summary points that is incorporating relevant skills, experience, and keywords from the JD. Ensure the new summary aligns with JD requirements and old summary from existing resume. Make sure it must be at least top most relevant 12 points. Each points must contains 30-40 words.
                 - Don't remove all data points from summary. keep most important summary point's that is most important to align it with JD.
                 - Make sure if you already add incorporating relevant skills, experience, and keywords from the JD, in Introduction then don't repeat it in summary.
             - **Update experience:** update experience year based on JD and updated experience should be mention in updated Introduction.
             - **Missing Information:** If any important skills or experiences are absent in the resume but essential in the JD, add them in relevant skill section without removing existing skills.
            2. **Technical Skill Analysis & Relevance Check:
              - **Instruction:** "Do not repeat skills. Place each skill in the category where it is most commonly or primarily used. If a skill is both a technology and a language (like HTML or JavaScript etc.), categorize it under "Languages/Scripting."
              - "Extract the skills from JD and organized into categories, ensure each skill is accurately placed under the correct section. if some skills are not relevant to given list then make new section for it and give the list as needed according to these guidelines:
              - "Make sure don't give as it is given example list, give updated skills data as per JD & resume" 
                - Languages/Scripting & Technologies: Include all architectural patterns, markup, scripting languages and technology-specific skills related to application development  (e.g., Java, Spring Boot, JavaScript, HTML, XML etc.).
                - Libraries/APIs: Include all Libraries & api (e.g., DBC, jQuery, Google Maps, EJB, JNDI, JAI etc.).
                - Frameworks: Include all Frameworks (e.g., Spring Boot, Spring, Struts, Junit, Django, Kotlin etc.).
                - Operating Systems: Include all operating system skills (e.g., Linux, Ubuntu, MS Windows).
                - Cloud Services: Include all Cloud Services skills (e.g., AWS, Azure etc.).
                - IDEs: Include all integrated development environments (e.g., Visual Studio Code, Eclipse IDE etc.).
                - Tools: Include all tools used for version control, API documentation, and project management (e.g., GitHub, GitLab, Swagger etc.).
            3.Project Analysis & Relevance Check:               
                - Existing Projects: Review all projects in the resume and list them.
                - Relevance Evaluation: Strictly evaluate whether each project is relevant to the Job Description (JD) based on required skills, technologies, and functionality.
                - Relevance Criteria: If the existing project is based on Java (or any relevant technology in the JD), and there are matching key points like relevant skills, tools, or technologies, then update the project.
                - If an existing project is in a different tech stack (e.g., deep learning, machine learning, UI/UX) and the JD focuses on Java or other unrelated skills, do not attempt to forcefully update the project. Instead, proceed to create a new projects.
                
                - **Project Updates & New Project Creation:**
                - Update Projects: For relevant existing projects, update them by adding missing skills, keywords, functionality, and software from the JD, ensuring that the project reflects the required expertise.
                - New Project Creation: If no existing projects are relevant to the JD,then generate a new project. 
                - The new project must as real world projects. also give project name based on it's description or functionality.
                - Don't use project name or title like project1,project2 etc.. don't do that. use real word name that should be a realistic name or title for new project.
                - Maintain the original structure of existing projects, including sections such as Title, Timeline, Description, Responsibilities, and Skills.
                
                - **Grammar & Formatting:**
                - Ensure that the output has correct grammar, no typos, and professional formatting.
                - Maintain the original formatting and structure of the resume as closely as possible.
            4.Give all project's including new project and all Existing projects should be there.
        4. **Side-by-Side Comparison:** Highlight changes made to the resume by providing a side-by-side comparison between the original and enhanced versions. Indicate what new information was added and its relevance to the JD.
        5. **Irrelevant Information:** Identify and list any irrelevant sections from the original resume, explaining why they are not relevant to the JD.
        6. **ATS Compatibility Assessment:** Provide an estimated ATS compatibility score (in percentage) for the enhanced resume based on its alignment with the JD's requirements. Explain why the score has improved.
            - While calculating ATS remember below instructions:
                - Provide an estimated ATS compatibility score after implementing all suggested changes.
                - Explain how each major change contributes to the score improvement.
                - Always review ATS scores before and after changes

        ###**Important Considerations:**

        - **Accuracy:** Ensure the resume enhancements are accurate and consistent with the original content.
        - **Relevance:** Prioritize information that directly aligns with the JD and ATS systems.
        - **Conciseness:** Keep explanations brief and to the point.
        - **Encoding:** Use only standard ASCII characters to avoid encoding issues.
        - **No Unnecessary Sections:** Avoid adding sections like awards or certificates if not present in the original resume.
        - **Data not Available** If Data is not Available in any section of project then give only "Not Specified" message in that section.

    ### **Strict Instructions for Output:**
    - **Make sure all curly braces of main dictionary and nested dictionary are properly enclosed.
    - **Give all data in single dictionary as above mention format, Don't give separately dictionary data like resume data in single dictionary and another one for Comparison & Irrelevant data.
    - **JSON Format:** The output should be in valid JSON format, matching the structure provided below.
    - **Avoid Extra Data:** The JSON should contain only the required data and no extraneous text.
    - **No Extra Spaces:**  Ensure there are NO extra spaces after colons (:) in the JSON, and no spaces before starting quotes. 
    - **No Trailing Commas:** Double-check that you have a comma (,) after each key-value pair within objects, except for the last one.
    - **Avoid Common Errors:**  Be sure to produce JSON that is free of missing commas, extra spaces, or other common syntax errors.
    - **All keys and values Should Be enclosed in double quotes ("). If a value itself contains a double quote, it should be escaped using a single quote (') example: {{"project":"This is 'example' for inner single quote"}}.
    - Don't use "```json" or "json" in output to denote response as json. just give only json structured data as response.
    - Avoid non-ASCII characters and symbols.
    - Don't give **Explanation of Changes**: at the end or in optimized resume.
    - Don't Give that characters in response data which is we can't converted with "latin-1" encoder.

    **JSON Structure:**

    {json_format}

"""


first_resume_prompt = """
        **Resume Enhancement & ATS Optimization**

            **Input:**

        - **Job Description (JD):** {JD}
        - **Resume:** {resume_txt}

        {instruction}

"""


new_resume_json_format = """
    {
       "personal_details":{
          "name":"candidate name",
          "position":"candidate designation"
       },
       "introduction":"give candidate Introduction around 100 words",
       "summary":[
          "extract summary points from resume and give it as point wise",
          "summary point 2",
          "etc.."
       ],
       "technical_skills":{
          "languages/technologies":[],
          "operating_systems":[],
          "IDEs":[],
          "tools":[],
          "database":[],
          "cloud_services":[],
          "libraries/api":[],
       },
       "projects":{
          "project_name":{
             "timeline":"Jul 2023 - Jun 2024",
             "description":"Designed and implemented the Game platform and new software components based on Java REST and Spring. The goal is to provide a simple and intuitive way to engage users in watching games and to demonstrate value to buyers.",
             "responsibilities":[
                "Added security and authentication to prevent fraud.",
                "Developed secure and robust architecture to transact money.",
                "Implemented unit and integration tests using Mockito and JUnit."
             ],
             "skills":[
                "Java",
                "Spring Framework",
                "REST",
                "JUnit",
                "Oracle"
             ]
          }
       }
    }
"""


only_jd_through_resume_prompt = """
        **Build a New Resume based on JD**

        **Input:**

        - **Job Description:** {JD}

        1. **Job Description Analysis:** Carefully review the JD to identify key skills, qualifications, experience levels, and any specific technologies or tools that is required.
        2. **Key Requirements Extraction:** Extract the crucial keywords, skills and expertise from the JD for better alignment with an Applicant Tracking System (ATS).
        3. **Resume Builder:**
           1. **Introduction & Summary:**
             - **Introduction:** Give introduction that is incorporating relevant skills, experience, and keywords from the JD. Ensure the Updated introduction aligns with JD requirements. Make sure it must be around 150 words.
             - **Summary Update:** Add on summary points that is incorporating relevant skills, experience, and keywords from the JD. Ensure the new summary aligns with JD requirements and old summary from existing resume. Make sure it must be at least top most relevant 12 points. Each points must contains 30-40 words.
                 - Make sure if you already add incorporating relevant skills, experience, and keywords from the JD in Introduction part, then don't repeat it in summary.
             - **Update experience:** update experience year based on JD and updated experience should be mention in updated Introduction.
           2. **Technical Skill Analysis & Relevance Check:
             - **Instruction:** "Do not repeat skills. Place each skill in the category where it is most commonly or primarily used. If a skill is both a technology and a language (like HTML or JavaScript etc.), categorize it under "Languages/Scripting."
             - "Extract the skills from JD and organized into categories, ensure each skill is accurately placed under the correct section. if some skills are not relevant to given list then make new section for it and update the list as needed according to these guidelines:
             - "Make sure don't give as it is given example list, give updated skills data as per JD"
                - Languages/Scripting & Technologies: Include all architectural patterns, markup, scripting languages and technology-specific skills related to application development.
                - Libraries/APIs: Include all Libraries & api.
                - Frameworks: Include all Frameworks.
                - Operating Systems: Include all operating system skills.
                - Cloud Services: Include all Cloud Services skills.
                - IDEs: Include all integrated development environments.
                - Tools: Include all tools used for version control, API documentation, and project management.
             - "Give all the skills section as per JD, if that section doesn't have any skill from JD then update it according the JD and give it."
           3.Projects:      
             - Generate a minimum six project ideas from JD for a developer with over two years of experience.       
             - New Project Creation: Generate a new project based on jd requirements, The new project is must real world projects and also give that project name based on it's description or functionality.
             - Make sure project description is must with brief info at least around 150 words.
             - Don't use new project name or title like project1, project_name etc... don't do that.
             - Also don't use project1 or project_name in starting of new project title/name. Give only project name.
             - Maintain the original structure of projects as mentioned in below json format, including sections such as Title, Timeline, Description, Responsibilities, and Skills.
             - **Grammar & Formatting:**
             - Ensure that the output has correct grammar, professional formatting and no typos.
                
        ###**Important Considerations:**
        - **Relevance:** Prioritize information that directly aligns with the JD and ATS systems.
        - **Don't give static Data:** Don't give static data as mentioned in below json structure as it is. Perform above instructions and give new resume data in mentioned json structure.
        - **Conciseness:** Keep explanations brief and to the point.
        - **Data not Available** If Data is not Available in any section of project then give only "Not Specified" message in that section.

    ### **Strict Instructions for Output:**
    - **Make sure all curly braces of main dictionary and nested dictionary are properly enclosed.
    - **Give all data in single dictionary as below mention format, Don't give separately dictionary data like resume data in single dictionary and another one for Comparison & Irrelevant data.
    - **Avoid Extra Data:** The JSON should contain only the required data and no extraneous text.
    - **No Extra Spaces:** Ensure there are NO extra spaces after colons (:) in the JSON, and no spaces before starting quotes. 
    - **No Trailing Commas:** Double-check that you have a comma (,) after each key-value pair within objects, except for the last one.
    - **Avoid Common Errors:**  Be sure to produce JSON that is free of missing commas, extra spaces, or other common syntax errors.
    - **All keys and values Should Be enclosed in double quotes ("). If a value itself contains a double quote, it should be escaped using a single quote (') example: {{"project":"This is 'example' for inner single quote"}}.
    - Don't use "```json" or "json" in output to denote response as json. just give only json structured data as response.
    - Avoid non-ASCII characters and symbols.
    - Don't try to give not specified or no data etc.. as value if there's data not available 

    **JSON Structure:**
    
    {json_format}
    follow this json structure to give proper json formatting resume.
"""


revalidate_resume_prompt = """

    Hey, I want to validate if my resume follows the given instructions. If not, please regenerate the resume based on the provided instructions.

    **Important Notes:**
    1. Provide the output **only in JSON format** without any additional information like titles or headers.
    2. Focus on the following sections for validation and generation.

    **Job Description (JD):** 
    {jd}

    **Resume:** 
    {first_resume}

    **Instructions:** 
    {instruction}

    - Check if the resume adheres to the instructions provided. If it does not, regenerate the resume strictly in JSON format based on the instructions.

"""


interview_question_json_format = """
    {
        "interview_questions": ["Question1", "Questions2"]
    }
    """


interview_question_prompt = """ 

    Hey, expert Interview Questions Builder! Your task is to suggest highly recommended **technical interview questions** based on the provided resume, specifically focusing on **MNC** interview standards.

    Based on the Resume**:

    **Resume:**
    {resume}

    **Task:**
    1. **Generate Tailored Technical Interview Questions:** Based on the job description or resume to identify the key technical skills and responsibilities.
    2. ** Create a set of insightful and relevant **technical** interview questions that are frequently asked in MNC company interviews and align with the candidate's resume.
    3. **Prioritize Key Topics:** Focus on the most commonly asked topics in the industry and specific technologies mentioned in the JD/resume also give some Programming practicals questions also.
    4. Give at least 20 Questions as per resume, make sure that questions is mostly asked in MNC companies.

    **Don't follow questions like below:**
    - make sure you don't have rights to ask questions like below
        - what's your salary expectations.
        - related to personal information.

    **Important Considerations:**
    - Don't give numbers to Interview questions like 1,2 etc...
    - Make sure don't show extracted key skills or requirements it's only for your perspective to generate a interview questions.
    - Prioritize clarity and conciseness in the interview questions.
    - Ensure the questions are technically challenging and relevant to the candidate's experience.
    - Do not show any of the steps you have performed. Only show Interview Questions
    - Give only json data as given format only. Don't give extra data or information's before and after JSON data like "```json" or "json" & other info.
    - Adaptable to different formats and free from grammatical errors or typos.

    **Strictly Follow Instructions for Output & Guidelines:**
    - **JSON Format:** The output should be in valid JSON format, matching the structure provided below.
    - **Avoid Extra Data:** The JSON should contain only the required data and no extraneous text.
    - **No Extra Spaces:**  Ensure there are NO extra spaces after colons (:) in the JSON, and no spaces before starting quotes. 
    - **No Trailing Commas:** Ensure there are no trailing commas (commas after the last item in an object) in the JSON.
    - **Avoid Common Errors:**  Be sure to produce JSON that is free of missing commas, extra spaces, or other common syntax errors.
    - Use double quotes (") for all keys and values.
    - Don't give extra information like ("I'll generate technical interview questions based on the provided resume. Since the resume is not provided in a readable format, I'll assume the skills and technologies mentioned in the job description. Please find the generated questions in JSON format:```") or other info before JSON data structure of Interview questions.
    - Don't Give that characters in response data which is we can't converted with "latin-1" encoder.
    
    **JSON Structure:**

    {qa_json_format}


"""



mock_interview_qa_prompt = """
    You are an expert technical interviewer. Your task is to conduct a realistic, in-depth technical interview based on the given resume and previous answers.

    **Resume Context:**
    {resume}

    **Previous Answer:**
    {previous_answer}

    **Previously Asked Questions:**
    {previous_questions}


    Instructions:
    
    1. If this is the first question (no previous answer) or if the previous answer was "skip":
       - Generate a technical question based on the most advanced or recent skills/projects mentioned in the resume.
       - Focus on the candidate's strongest areas to start the interview positively.

    2. If the previous answer contains random characters or is irrelevant:
       - Respond with: "I'm sorry, but I didn't understand your answer. Could you please provide a relevant response to the question?"
       - Then, repeat the last asked question.

    3. For subsequent questions:
       - Analyze the previous answer carefully.
       - If the answer demonstrates knowledge, ask a follow-up question that delves deeper into that topic.
       - If the answer is vague or shows uncertainty, ask a related but different question on the same topic to give the candidate another chance.
       - If the answer is strong, move on to a new topic from the resume.

    4. Throughout the interview:
       - Ask technical questions that require problem-solving, not just factual recall.
       - Include questions about system design, coding practices, and real-world scenarios related to the candidate's experience.
       - Occasionally ask about how the candidate handled challenges or collaborated in their projects.

    5. Avoid:
       - Repeating questions that have already been asked.
       - Asking basic questions like age, years of experience, or project timelines.
       - Focusing too much on a single project; draw from the entire resume.

    6. Response Format:
       - Provide only the next question, without any additional text, numbering, or explanation.
       - Start the question directly, without any prefix like "Question:".

    Generate the next appropriate question based on these instructions.
    """

