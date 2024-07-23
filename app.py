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

assistant_avatar = load_image('athletic_logo.png')
user_avatar = load_image('person_athletic.png')

st.set_page_config(
    page_title="Rapha",
    page_icon="🤖",
)

hide_streamlit_style = """
            <style>
            #root > div:nth-child(1) > div > div > div > div > section > div {padding-top: 0rem;}
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_streamlit_style, unsafe_allow_html=True)

# Add custom CSS
st.markdown("""
    <style>
    .chat-input-container {
        position: fixed;
        top: 0;
        width: 100%;
        z-index: 999;
        background-color: white;
        padding: 10px 0;
        box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    }
    .chat-messages {
        margin-top: 100px;  /* Adjust based on your input container height */
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize chat history and check if it's the first run
if "messages" not in st.session_state:
    st.session_state.messages = []
    initial_prompt = (
        "You are performing an interview to find the best product for a user from the following list of products: \n"
        + product_data +
        "\nPlease start by asking the user about their situation to narrow down the choices. Don't list products until you've asked at least 2 questions."
        "When you identify which product the user wants, please output the product description (decapitalize everything that is in all caps please) complete with the hyperlink and image. Don't print out the additional information section ever. Do not ever recommend a product that isn't directly relevant to the user's request. If the product doesn't exist, then just say so and suggest something similar."
    )
    st.session_state.messages.append({"role": "system", "content": initial_prompt})
    initial_response = "**Hello, I'm Rapha!** I'm here to help you boost your health.\n\nWould you like to enhance your sleep, athletic performance, diet, gut health, general well-being, or something else?"
    st.session_state.initialized = False
else:
    st.session_state.initialized = True

# Accept user input at the top
with st.container():
    st.markdown('<div class="chat-input-container">', unsafe_allow_html=True)
    prompt = st.chat_input("Ask Rapha anything!")
    st.markdown('</div>', unsafe_allow_html=True)

if prompt:
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    # Display user message in chat message container
    # with st.chat_message("user", avatar=user_avatar):
    #     st.markdown(prompt)

    # Display thinking loader with spinner
    with st.spinner(''):
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages
        )

    assistant_message = response.choices[0].message.content

    # # Update assistant response in chat message container
    # message_placeholder.markdown(assistant_message)

    # Add assistant response to chat history
    st.session_state.messages.append({"role": "assistant", "content": assistant_message})

# # Display chat messages from history on app rerun, including the initial message if it's the first run
# st.markdown('<div class="chat-messages">', unsafe_allow_html=True)

for message in reversed(st.session_state.messages):
    if message["role"] != "system":
        avatar = assistant_avatar if message["role"] == "assistant" else user_avatar
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

# if not st.session_state.initialized:
#     with st.chat_message("assistant", avatar=assistant_avatar):
#         st.markdown(initial_response)
#     st.session_state.messages.append({"role": "assistant", "content": initial_response})
#     st.session_state.initialized = True

st.markdown('</div>', unsafe_allow_html=True)
