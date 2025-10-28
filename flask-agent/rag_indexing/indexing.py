import bs4
import sys, os, json
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_qdrant import QdrantVectorStore

def read_configs(config_file):
    with open(config_file) as f:
        return json.load(f)

def from_web(url):
    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
    )
    return loader.load()

def retriever_from_docs(docs):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    vectorstore = QdrantVectorStore.from_documents(
        documents=splits,
        embedding=OpenAIEmbeddings(),
        collection_name="my_documents",
        url="http://localhost:6333",  # Qdrant server endpoint
    )
    print("Embeddings are added to Qdrant server.")

if __name__ == "__main__":
    configs = read_configs("../../config.json")
    os.environ["OPENAI_API_KEY"] = configs["chatbot"]["OPENAI_API_KEY"]
    os.environ["GOOGLE_API_KEY"] = configs["chatbot"]["GOOGLE_API_KEY"]
    retriever_from_docs(from_web(sys.argv[1]))