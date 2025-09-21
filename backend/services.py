import shutil
from langchain_huggingface import HuggingFaceEmbeddings
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from youtube_transcript_api.formatters import JSONFormatter
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain.schema.runnable import RunnableParallel, RunnableLambda, RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
import os, re

load_dotenv()

embedding_model = HuggingFaceEmbeddings(model_name='sentence-transformers/all-MiniLM-L6-v2')
llm = ChatGoogleGenerativeAI(model='gemini-2.0-flash')
DB_PATH = "vectorstore"

def get_video_id(url: str) -> str:
    """Extract YouTube video ID from URL."""
    match = re.search(r"(?:v=|youtu\.be/)([a-zA-Z0-9_-]{11})", url)
    return match.group(1) if match else None

def format_result(docs):
    result = ''
    for doc in docs:
        result += doc.page_content
    return result

def load_transcript(url: str):
    """Fetch transcript and build FAISS index."""
    video_id = get_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL")

    transcript_list = YouTubeTranscriptApi().fetch(video_id, languages=["en"])
    transcript = " ".join(chunk.text for chunk in transcript_list)

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunk = splitter.create_documents([transcript])

    # Clear old vectorstore
    if os.path.exists(DB_PATH):
        shutil.rmtree(DB_PATH)
    os.makedirs(DB_PATH, exist_ok=True)

    vectordb = FAISS.from_documents(
        embedding = embedding_model,
        documents = chunk
    )
    vectordb.save_local(DB_PATH)

    return len(chunk)

def query_rag(question: str):
    """Query FAISS index."""
    vectordb = FAISS.load_local(DB_PATH, embedding_model, allow_dangerous_deserialization=True)
    retriever = vectordb.as_retriever(
        search_type = "similarity",
        search_kwargs = {'k': 4}
    )
    
    prompt = PromptTemplate(
        template = 'You are a helpful assistant. Answer the question ONLY based on the context with a detailed overview. If there is no information, simply answer \"I don\'t know.\". The context and question is given below. /n/n Context -> {context} /n/n Question -> {question}',
        input_variables = ['context', 'question']
    )

    parallel_chain = RunnableParallel({
        'context': retriever | RunnableLambda(format_result),
        'question': RunnablePassthrough()
    })

    parser = StrOutputParser()
    sequence_chain = prompt | llm | parser

    chain = parallel_chain | sequence_chain

    answer = chain.invoke(question)

    return answer
