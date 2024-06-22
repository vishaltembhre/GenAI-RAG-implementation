import os,sys
import streamlit as st
from langchain.chat_models import AzureChatOpenAI
from langchain.embeddings import OpenAIEmbeddings
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import FAISS
import pandas as pd
from azure.identity import ClientSecretCredential
from azure.keyvault.secrets import SecretClient
from langchain.agents import create_pandas_dataframe_agentss

def apiDetails():
    #API details - Starts
    TENANT= "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CLIENT_ID = "XXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    CLIENT_SECRET= st.secrets.CLIENT_SECRET
    credential = ClientSecretCredential(TENANT,CLIENT_ID,CLIENT_SECRET)
    VAULT_URL= "https://XXXXXXXXXXXXXXXXXXXXXXXXXXXX.azure.net/"
    client = SecretClient(vault_url=VAULT_URL, credential=credential)
    openai_key = client.get_secret("XXXXXXXXXXXXXXXXXXXXXXXXXXXX")


    os.environ["OPENAI_API_TYPE"] = "azure"
    os.environ["OPENAI_API_BASE"] = "https://biminternalcapability.openai.azure.com/"
    os.environ["OPENAI_API_KEY"] = openai_key.value
    os.environ["OPENAI_API_VERSION"] = "2023-07-01-preview"
    #Api details - Ends

def downloadText(final_output,finalEmail):
    with open(final_output, 'w') as file:
        file.write(finalEmail)
        with open(final_output, "rb") as file:
            btn = st.download_button(
                label="Download File",
                data=file,
                file_name="Email.txt",
                mime="text/plain"
            )

apiDetails()


st.set_page_config(page_title = "Access GPT 4", page_icon="🚀", layout = "wide")#, initial_sidebar_state = "expanded")
st.title("OPEN AI")


conversation_history = []


input = st.text_area("Ask Question",placeholder="Type your question")


llm = AzureChatOpenAI(deployment_name="gpt-4", model_name="gpt-4")


# Prompt
writePrompt = f"""Respond accurately


Question - {{input1}}
"""


prompt = PromptTemplate(template=writePrompt,input_variables=["input1"])
query_llm = LLMChain(llm=llm, prompt=prompt)


# if st.button("Generate Output"):
#     response = query_llm.run({"input1": input})
#     st.write(response)


if input:
    answer = query_llm.run({"input1": input})
    # Save the question and answer to the conversation history
    conversation_history.append((input, answer))
    st.write(f'A: {answer}')


for input, answer in conversation_history:
    st.sidebar.markdown(f'**Q:** {input}')
    st.sidebar.write(f'A: {answer}')


