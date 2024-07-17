import streamlit as st
from openai import OpenAI

# key = st.secrets["OPENAI_API_KEY"]


# client = OpenAI(api_key=key)
client = OpenAI()

# Load product data from products.txt
def load_product_data():
    with open("products.txt", "r", errors="ignore") as file:
        return file.read()

# Load product data
product_data = load_product_data()

# Load images as bytes
def load_image(image_path):
    with open(image_path, "rb") as image_file:
        return image_file.read()

# Streamlit app setup
hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Custom CSS for st.chat_input
custom_css = """
<style>
.stChatInputContainer > div {
    background-color: rgba(0, 0, 0, 0.8) !important;
    color: #ffffff !important;
    border: 1px solid #ccc !important;
    border-radius: 5px !important;
    padding: 10px !important;
}
.stChatInputContainer > div input {
    color: #ffffff !important;
}
</style>
"""
st.markdown(custom_css, unsafe_allow_html=True)

assistant_avatar = load_image('athletic_logo.png')
user_avatar = load_image('person_athletic.png')

# st.title("Tea Product Explorer")

# Initialize chat history and check if it's the first run
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_prompt = (
        "You are performing an interview to find the best product for a user from the following list of products: \n"
        + product_data +
        "\nPlease start by asking the user about their situation to narrow down the choices. Don't list products until you've asked at least 2 questions."
        "When you indentify which product the user wants, please output the product description (decapitalize everything that is in all caps please) complete with the hyperlink and image. Don't print out the additional information section ever. Do not ever recommend a product that isn't directly relevant to the user's request. If the product doesn't exist, then just say so and suggest something similar."
    )
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    initial_response = "**Hello, I'm AltheticSpaAI!** I'm here to help you boost your health.\n\nWould you like to enhance your sleep, athletic performance, diet, gut health, detoxing, general well-being, or something else?"
    st.session_state.initialized = False
else:
    st.session_state.initialized = True

# Display chat messages from history on app rerun, skipping the system message
for message in st.session_state.messages:
    if message["role"] != "system":
        avatar = assistant_avatar if message["role"] == "assistant" else user_avatar
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# If it's the first time around, display the initial assistant message only once
if not st.session_state.initialized:
    with st.chat_message("assistant", avatar=assistant_avatar):
        st.markdown(initial_response)
    st.session_state.messages.append({"role": "assistant", "content": initial_response})
    st.session_state.initialized = True

# Accept user input
if prompt := st.chat_input("Ask AthleticSpaAI anything!"):
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    with st.chat_message("user", avatar=user_avatar):
        st.markdown(prompt)

    # Display thinking loader with spinner
    with st.chat_message("assistant", avatar=assistant_avatar):
        message_placeholder = st.empty()
        with st.spinner(''):
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages
            )

    assistant_message = response.choices[0].message.content

    # Update assistant response in chat message container
    message_placeholder.markdown(assistant_message)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})
