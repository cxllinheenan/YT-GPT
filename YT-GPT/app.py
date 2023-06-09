# Bring in Deps

from urllib import response
from apikey import apikey

import streamlit as st 	                                                                    	 	 
from langchain.llms import OpenAI
from langchain.prompts  import PromptTemplate
from langchain.chains import LLMChain, SequentialChain
from langchain.memory import ConversationBufferMemory
from langchain.utilities import WikipediaAPIWrapper

openai_api_key = st.sidebar.text_input('OpenAI API Key')
#App Framework
st.title('🦜 A Researching AI for YouTube Videos')
prompt = st.text_input('Write a short about')

#Prompt
title_template = PromptTemplate(
    input_variables=['topic'],
    template='Write me a youtube video title about {topic}' 

)
    
script_template = PromptTemplate(
    input_variables=['title', 'wikipedia_research'],
    template='Write me a youtube video script Based on this title TITLE: {title} while leveraging this wikipdeia research:{wikipedia_research}'

)
#Memory
title_memory = ConversationBufferMemory(input_key='topic', memory_key='chat_history')
script_memory = ConversationBufferMemory(input_key='title', memory_key='chat_history')


# LLLMs
llm= OpenAI(temperature=0.9)
title_chain = LLMChain(llm=llm, prompt =title_template, verbose=True, output_key='title', memory=title_memory)
script_chain = LLMChain(llm=llm, prompt =script_template, verbose=True, output_key='script', memory=script_memory)

wiki = WikipediaAPIWrapper()

#Sow Stuff to Screen IF prompt
if prompt:
    title=title_chain.run(prompt)
    wiki_research=wiki.run(prompt)
    script=script_chain.run(title=title, wikipedia_research=wiki_research)

    st.write(title)
    st.write(script)


    with st.expander('Title History'):
        st.info(title_memory.buffer)

    with st.expander('Script History'):
        st.info(script_memory.buffer)

    with st.expander('Wikipedia Research History History'):
        st.info(wiki_research)
