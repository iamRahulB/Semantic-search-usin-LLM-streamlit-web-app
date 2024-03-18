from langchain_community.vectorstores import FAISS
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import datetime


class PineConeIndex:

    def __init__(self) -> None:
        self.now = datetime.datetime.now(datetime.timezone(datetime.timedelta(hours=5, minutes=30)))
        self.formatted_time=self.now.strftime("%Y-%m-%d %H:%M:%S")

        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

        self.index_name = "chathistory"



    def add_to_pinecone(self,user_input,response):
        
        vectorstore = PineconeVectorStore(index_name=self.index_name, embedding=self.embeddings)

        response_formatted=f"'time : {self.formatted_time}', 'user question : {user_input}\n ', 'AI response : {response}'"

        vectorstore.add_texts(response_formatted)

        print("added to pinecone--------------------------response_formatted",response_formatted)


    
    def get_from_pinecone(self,user_input):

        docsearch_query = PineconeVectorStore.from_existing_index( index_name=self.index_name,embedding=self.embeddings,)

        docs = docsearch_query.max_marginal_relevance_search(user_input,k=1,fetch_k=3)

        print("semantic docs------------------",docs)

        user_input_semantic_search=[]

        try :
        
            for i, doc in enumerate(docs):
                user_input_semantic_search.append(f"{self.formatted_time} :{doc.page_content}")
                print(f"{i + 1}.", doc.page_content, "\n")

            print("best of best------------------",user_input_semantic_search)

        except:
            pass
        
            # except :
            #    docsearch_except = PineconeVectorStore.from_texts(texts=["this is first test message of pinecone. Ai dont include this in chat "], embedding=embeddings, index_name=index_name,ids=["rahulb"])
            #    docsearch_except = PineconeVectorStore.from_texts(texts=["this is first test message of pinecone. Ai dont include this in chat "], embedding=embeddings, index_name=index_name,ids=["rahulb"])
            #    docs_except = docsearch_query.similarity_search(user_input,k=1)
            #    user_input_semantic_search=[docs_except[0].page_content]
            # print("user input semantic search----------------------",user_input_semantic_search)

            # user_input_semantic_search=[docs[0].page_content,docs[1].page_content]
        
        print("got from pinecone")

        return user_input_semantic_search
