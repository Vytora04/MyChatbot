import streamlit as st
from langchain.chat_models import ChatOllama
from langchain.schema import HumanMessage, AIMessage
from langchain.memory import ConversationBufferMemory
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# ---- Streamlit Setup ---- #
st.set_page_config(layout="wide")
st.title("Vytora Local ChatAI")

# ---- Sidebar Inputs ---- #
st.sidebar.header("Settings")

model_options = ["mistral", "phi3.5"]
MODEL = st.sidebar.selectbox("Choose a Model", model_options, index=0)

# Inputs for max history and context size
MAX_HISTORY = st.sidebar.number_input("Max History", min_value=1, max_value=10, value=2, step=1)
CONTEXT_SIZE = st.sidebar.number_input("Context Size", min_value=1024, max_value=16384, value=8192, step=1024)

# Dropdown for thought process
thought_options = ["Show Thought Process", "Direct Answer Only"]
THOUGHT_MODE = st.sidebar.selectbox("Response Style", thought_options, index=0)

# Advanced settings in an expander (dropdown)
with st.sidebar.expander("Advanced Settings"):
    TEMPERATURE = st.slider("Temperature", min_value=0.0, max_value=2.0, value=0.7, step=0.01)
    TOP_P = st.slider("Top-P", min_value=0.0, max_value=1.0, value=0.9, step=0.01)
    TOP_K = st.slider("Top-K", min_value=1, max_value=100, value=40, step=1)
    MAX_TOKENS = st.number_input("Max Tokens", min_value=128, max_value=4096, value=512, step=1)

# Clear Chat button above Summarize Chat
clear_btn = st.sidebar.button("Clear Chat")
# Summarize button
summarize_btn = st.sidebar.button("Summarize Chat")

# ---- Function to Clear Memory When Settings Change ---- #
def clear_memory():
    st.session_state.chat_history = []
    st.session_state.memory = ConversationBufferMemory(return_messages=True)  # Reset memory

# Clear memory if settings are changed
if "prev_context_size" not in st.session_state or st.session_state.prev_context_size != CONTEXT_SIZE:
    clear_memory()
    st.session_state.prev_context_size = CONTEXT_SIZE

# ---- Initialize Chat Memory ---- #
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "memory" not in st.session_state:
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ---- LangChain LLM Setup ---- #
model_map = {
    "mistral": "mistral",
    "phi3.5": "phi3.5"
}
llm_args = {
    "model": model_map.get(MODEL, MODEL),
    "streaming": True,
    "temperature": TEMPERATURE,
    "top_p": TOP_P,
    "top_k": TOP_K,
    "max_tokens": MAX_TOKENS,
}
llm = ChatOllama(**llm_args)

# ---- Prompt Template ---- #

# Set prompt template based on thought process selection
if THOUGHT_MODE == "Show Thought Process":
    prompt_text = "{history}\nUser: {human_input}\nAssistant:"
else:
    prompt_text = (
        "{history}\nUser: {human_input}\nAssistant: "
        "Answer directly and concisely. Do NOT show your thinking, reasoning, or any chain-of-thought. "
    "Do not use <think> or any explanation."
    )

prompt_template = PromptTemplate(
    input_variables=["history", "human_input"],
    template=prompt_text
)

chain = LLMChain(llm=llm, prompt=prompt_template, memory=st.session_state.memory)

# ---- Display Chat History ---- #
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---- Trim Function (Removes Oldest Messages) ---- #
def trim_memory():
    while len(st.session_state.chat_history) > MAX_HISTORY * 2:  # Each cycle has 2 messages (User + AI)
        st.session_state.chat_history.pop(0)  # Remove oldest User message
        if st.session_state.chat_history:
            st.session_state.chat_history.pop(0)  # Remove oldest AI response

# ---- Handle User Input ---- #
if prompt := st.chat_input("Say something"):
    # Show User Input Immediately
    with st.chat_message("user"):
        st.markdown(prompt)

    st.session_state.chat_history.append({"role": "user", "content": prompt})  # Store user input

    # Trim chat history before generating response
    trim_memory()

    # ---- Get AI Response (Streaming) ---- #
    with st.chat_message("assistant"):
        response_container = st.empty()
        full_response = ""

        for chunk in chain.stream({"human_input": prompt}):
            if isinstance(chunk, dict) and "text" in chunk:
                text_chunk = chunk["text"]
                full_response += text_chunk
                response_container.markdown(full_response)

    # Store response in session_state
    st.session_state.chat_history.append({"role": "assistant", "content": full_response})

    # Trim history after storing the response
    trim_memory()

# ---- Clear Chat ---- #
if clear_btn:
    st.session_state.chat_history = []
    st.session_state.memory = ConversationBufferMemory(return_messages=True)

# ---- Summarize Chat History ---- #
if summarize_btn and st.session_state.chat_history:
    history_text = "\n".join([
        f"{msg['role'].capitalize()}: {msg['content']}" for msg in st.session_state.chat_history
    ])
    summary_prompt = f"Summarize the following conversation between a user and an assistant:\n\n{history_text}\n\nSummary:"
    summary_chain = LLMChain(
        llm=ChatOllama(**llm_args),
        prompt=PromptTemplate(input_variables=["human_input"], template="{human_input}"),
        memory=None
    )
    with st.sidebar:
        st.subheader("Conversation Summary")
        summary_response = ""
        for chunk in summary_chain.stream({"human_input": summary_prompt}):
            if isinstance(chunk, dict) and "text" in chunk:
                summary_response += chunk["text"]
                st.markdown(summary_response)