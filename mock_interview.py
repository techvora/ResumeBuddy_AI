import PyPDF2
import docx
import streamlit as st
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import PromptTemplate
import os
from dotenv import load_dotenv
import chromadb
from chromadb.config import Settings

favicon_path = "images/Yellow_Favicon.png"
st.set_page_config(page_title="Resume Flex AI", page_icon=favicon_path, layout="wide", menu_items=None, )


load_dotenv()


genai.configure(api_key="Your_API_Key")


llm = ChatGoogleGenerativeAI(
    model="gemini-1.5-pro",
    temperature=0.7,
    top_k=40,
    top_p=0.8,
    max_output_tokens=2048
)


embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")


PERSIST_DIRECTORY = "chroma_db"
if not os.path.exists(PERSIST_DIRECTORY):
    os.makedirs(PERSIST_DIRECTORY)


# Initialize Chroma client with specific settings
chroma_client = chromadb.PersistentClient(
    path=PERSIST_DIRECTORY,
    settings=Settings(
        anonymized_telemetry=False,
        is_persistent=True
    )
)


interview_question_template = PromptTemplate(
    input_variables=["resume", "previous_questions", "previous_answer"],
    template="""
    Role: You are an expert technical interviewer.

    Context:
    - Candidate's Resume: {resume}
    - Previous Questions Asked: {previous_questions}
    - Last Answer Received: {previous_answer}

    Task: Generate a relevant technical interview question that:
    1. Aligns with the candidate's background and experience
    2. Builds upon previous questions and answers
    3. Tests both theoretical knowledge and practical application
    4. Is clear and specific
    5. i want my initial question is always "Can you please tell me a bit about yourself?", also don't give any other information's with the question.
    6. make sure don't try to ask big question like two to three things at a time in the question don't do that.

    Generate the next interview question:
    """
)

evaluation_template = PromptTemplate(
    input_variables=["qa_pairs"],
    template="""
    Role: You are an expert interview evaluator.

    Interview Questions and Answers:
    {qa_pairs}

    Task: Evaluate the candidate's performance considering:
    1. Technical accuracy (30%)
    2. Problem-solving approach (25%)
    3. Communication clarity (20%)
    4. Depth of knowledge (15%)
    5. Overall coherence (10%)

    Provide:
    1. A score out of 10
    2. Detailed feedback for each aspect
    3. Areas of improvement
    4. Notable strengths

    Your evaluation:
    """
)


def create_rag_pipeline(resume_text):
    try:
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_text(resume_text)

        vectorstore = Chroma.from_texts(
            texts=texts,
            embedding=embeddings,
            persist_directory=PERSIST_DIRECTORY,
            client=chroma_client,
            collection_name="interview_collection"
        )

        qa = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever(search_kwargs={"k": 3})
        )
        return qa
    except Exception as e:
        st.error(f"Error creating RAG pipeline: {str(e)}")
        raise


class InterviewCoordinator:
    def __init__(self, resume_text):
        self.rag_pipeline = create_rag_pipeline(resume_text)
        self.questions_and_answers = []
        self.memory = ConversationBufferMemory()

    def generate_question(self, previous_questions, previous_answer):
        try:
            prompt = interview_question_template.format(
                resume=self.rag_pipeline.run("Summarize the candidate's background"),
                previous_questions=previous_questions,
                previous_answer=previous_answer
            )
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            st.error(f"Error generating question: {str(e)}")
            return "Could not generate question. Please try again."


    def evaluate_interview(self):
        try:
            prompt = evaluation_template.format(
                qa_pairs=self.questions_and_answers
            )
            response = llm.invoke(prompt)
            return response.content
        except Exception as e:
            st.error(f"Error during evaluation: {str(e)}")
            return "Could not complete evaluation. Please try again."



st.title("Mock Interview System")

if 'coordinator' not in st.session_state:
    st.session_state.coordinator = None
if 'current_question' not in st.session_state:
    st.session_state.current_question = None
if 'interview_active' not in st.session_state:
    st.session_state.interview_active = False

# GET RESUME AS PDF FROM USER INPUTS AND STORE IN VARIABLES
resume = st.file_uploader("Upload your resume here", type=['pdf', 'docx', 'doc'], label_visibility="collapsed",
                          help="Upload your resume here. Max size: 200MB")


def resume_text_from_pdf(pdf_file):
    if pdf_file != None:
        try:
            if pdf_file.type == 'application/pdf':

                # EXTRACT TEXT FROM PDF
                pdf_reader = PyPDF2.PdfReader(pdf_file)
                text = ""
                for page in pdf_reader.pages:
                    text += page.extract_text()
                return text

            elif pdf_file.type.startswith('application/vnd.openxmlformats-officedocument.wordprocessingml'):

                # # EXTRACT TEXT FROM DOC, DOCX
                doc = docx.Document(pdf_file)
                text = ""
                for paragraph in doc.paragraphs:
                    text += paragraph.text + "\n"
                return text

            else:
                print(f"Error: Unsupported file type: {pdf_file}")
                return None

        except Exception as e:
            print(f"An error occurred while extracting text: {e}")
            return None


resume_text = resume_text_from_pdf(resume)

if st.button("Start Interview"):
    if resume_text:
        try:
            st.session_state.coordinator = InterviewCoordinator(resume_text)
            st.session_state.interview_active = True
            st.session_state.current_question = st.session_state.coordinator.generate_question([], "")
        except Exception as e:
            st.error(f"Error starting interview: {str(e)}")
    else:
        st.warning("Please paste your resume before starting the interview.")

if st.session_state.interview_active:
    st.write(f"Question: {st.session_state.current_question}")
    answer = st.text_input("Your answer:")

    col1, col2 = st.columns(2)
    with col1:
        if st.button("Submit Answer"):
            if answer:
                st.session_state.coordinator.questions_and_answers.append(
                    (st.session_state.current_question, answer)
                )
                st.session_state.current_question = st.session_state.coordinator.generate_question(
                    [qa[0] for qa in st.session_state.coordinator.questions_and_answers],
                    answer
                )
                st.rerun()
            else:
                st.warning("Please provide an answer before submitting.")

    with col2:
        endqa = st.button("End Interview")

    if endqa:
        evaluation = st.session_state.coordinator.evaluate_interview()
        st.write("Evaluation Results:")
        st.write(evaluation)
        st.session_state.interview_active = False
        st.session_state.coordinator = None
        st.session_state.current_question = None