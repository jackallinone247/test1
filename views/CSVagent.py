import streamlit as st
from langchain_community.utilities import SQLDatabase
from sqlalchemy import create_engine
import pandas as pd
import os
from langchain.chat_models import init_chat_model
from langchain_community.agent_toolkits import create_sql_agent
import re
import time

from langchain.callbacks.base import BaseCallbackHandler




def clean_ansi(text):
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)


class StreamlitCallbackHandler(BaseCallbackHandler):
    def __init__(self, container):
        self.container = container
        self.logs = []
        self.log_area = container.empty()

    def _add_log(self, message):
        self.logs.append(message)
        self.log_area.markdown(message)
        time.sleep(0.5)  # Slow down here

    def on_tool_start(self, serialized, input_str, **kwargs):
        self._add_log(f"🛠️ **Invoking** `{serialized['name']}` with `{input_str}`")

    def on_tool_end(self, output, **kwargs):
        self._add_log(f"📦 **Tool Output**: `{output}`")

    def on_text(self, text, **kwargs):
        self._add_log(f"🧠 {text}")

    def on_agent_action(self, action, **kwargs):
        self._add_log(f"🤔 **Agent Action**: {action.log}")

    # def on_chain_start(self, serialized, inputs, **kwargs):
    #     self._add_log("🚀 **Chain Started**")

    # def on_chain_end(self, outputs, **kwargs):
    #     self._add_log("✅ **Chain Finished**")





# Setup API keys
os.environ["OPENAI_API_KEY"] = st.secrets["OPENAI_API_KEY"]
# os.environ["MISTRAL_API_KEY"] = st.secrets["MISTRAL_API_KEY"]  # Uncomment if using Mistral


# Page config
st.set_page_config(page_title="CSV Chatbot", page_icon="🧠", layout="wide")
st.title("📊 CSV Chatbot Assistant")

# Sidebar: File uploader
with st.sidebar:
    st.header("Upload CSV")
    csv_file = st.file_uploader("Choose a CSV file", type="csv")

# Session state to store chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if csv_file is not None:
    df = pd.read_csv(csv_file)
    engine = create_engine("sqlite:///data.db")
    df.to_sql("data", engine, index=False, if_exists="replace")

    db = SQLDatabase(engine=engine)

    # Choose LLM
    llm = init_chat_model("gpt-4.1-mini", model_provider="openai")
    # llm = init_chat_model("mistral-large-latest", model_provider="mistralai")

    agent_executor = create_sql_agent(llm, db=db, agent_type="openai-functions", verbose=True)

    # Display current chat history
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

    # Chat input
    user_query = st.chat_input("Ask a question about your CSV file...")

    if user_query:
        # Display user message
        st.session_state.chat_history.append({"role": "user", "content": user_query})
        with st.chat_message("user"):
            st.markdown(user_query)

        # Process with agent
        # with st.chat_message("assistant"):
        #     with st.spinner("Thinking..."):
        #         response = agent_executor.invoke({"input": user_query})
        #         answer = response["output"]
        #         st.markdown(answer)
        #         st.session_state.chat_history.append({"role": "assistant", "content": answer})
        with st.chat_message("assistant"):

            thought_placeholder = st.empty()
            callback_handler = StreamlitCallbackHandler(thought_placeholder)
            with st.spinner("Thinking..."):
                
                from io import StringIO
                import sys

                old_stdout = sys.stdout
                sys.stdout = mystdout = StringIO()

                try:
                    response = agent_executor.invoke(
                    {"input": user_query},
                    config={"callbacks": [callback_handler]}
                )
                finally:
                    sys.stdout = old_stdout

                reasoning_trace = clean_ansi(mystdout.getvalue())

                # Optional: Format steps a bit
                reasoning_trace = reasoning_trace.replace("> Entering new SQL Agent Executor chain...", "### 🤖 Agent Started")
                reasoning_trace = reasoning_trace.replace("> Finished chain.", "### ✅ Agent Finished")

                
                # Final response
                st.markdown(response["output"])

                st.session_state.chat_history.append({"role": "assistant", "content": response["output"]})
                
                with st.expander("🔍 See thought process"):
                    st.markdown(reasoning_trace)
                    # st.markdown("\n\n".join(callback_handler.logs))d

               
                



            
            

            # with st.spinner("Thinking..."):
            #     # Capture verbose output
            #     from io import StringIO
            #     import sys

            #     old_stdout = sys.stdout
            #     sys.stdout = mystdout = StringIO()

            #     try:
            #         response = agent_executor.invoke({"input": user_query})
            #     finally:
            #         sys.stdout = old_stdout

            #     answer = response["output"]
                

            #     # Show final answer
            #     st.markdown(answer)

            #     # Expandable reasoning trace
            #     # reasoning_trace = mystdout.getvalue()
            #     reasoning_trace = clean_ansi(mystdout.getvalue())

            #     # Optional: Format steps a bit
            #     reasoning_trace = reasoning_trace.replace("> Entering new SQL Agent Executor chain...", "### 🤖 Agent Started")
            #     reasoning_trace = reasoning_trace.replace("> Finished chain.", "### ✅ Agent Finished")

            #     with st.expander("🔍 See thought process"):
            #         st.markdown(reasoning_trace)


            #     # Store in history
            #     st.session_state.chat_history.append({"role": "assistant", "content": answer})

