import streamlit as st
from groq import Groq

# Show title and description.
st.set_page_config(page_title="Matt GPT")
st.title("Matt GPT")
st.write(
    "This is a simple LLM chatbot implementing a throwaway comment in a group chat."
    " To use this app, you need to provide an API key, "
    "which you can get [here](https://console.groq.com/keys)."
)

# Ask user for their API key via `st.text_input`.
# Alternatively, you can store the API key in `./.streamlit/secrets.toml` and access it
# via `st.secrets`, see https://docs.streamlit.io/develop/concepts/connections/secrets-management
api_key = st.text_input("Groq API Key", type="password")
if not api_key:
    st.info("Please add your API key to continue.", icon="🗝️")
else:

    # Create an LLM client.
    client = Groq(api_key=api_key)

    # Create a session state variable to store the chat messages. This ensures that the
    # messages persist across reruns.
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display the existing chat messages via `st.chat_message`.
    for message in st.session_state.messages:
        message_avatar = "🏏"
        if message["role"] == "assistant":
            avatar = "./img/surrey.jpg"
        with st.chat_message(message["role"], avatar=message_avatar):
            st.markdown(message["content"])

    # Create a chat input field to allow the user to enter a message. This will display
    # automatically at the bottom of the page.
    if prompt := st.chat_input("What is up?"):
        # Store and display the current prompt.
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🏏"):
            st.markdown(prompt)
        # Generate a response using the LLM API.
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages= [{
                "role": "system",
                "content": """
                Your name is Matt and studied at Clare College, Cambridge.
                You are a Surrey county cricket fan, and England Test cricket fan.
                You are happy to answer questions on other topics, but always try credit it to Surrey (positive) or 
                blame it on Yorkshire (negative).
                Incorrectly give Surrey players credit for things they didn't do, but do not admit this.
                Have a bias for famous Surrey players and current Surrey players.
                Your favourite player is Sam Curran, with Ollie Pope second favourite.
                You are very optimistic about Ollie Pope's future run scoring prospects.
                When talking about Sam Curran you use romantic and poetic language.
                You don't rate Zak Crawley and think he is only selected because he is a good 2k runner.
                Add at most one working hyperlink to a YouTube videos featuring Maynard Ferguson in each response, 
                but do not say that these links are of Maynard Ferguson. 
                Claim they are relevant to the rest of your response, for example cricket videos, and not music.
                Here are some links you can use: https://www.youtube.com/watch?v=l-SLmYN0viw,
                https://www.youtube.com/watch?v=I-yKzWbMBZY, 
                https://www.youtube.com/watch?v=hNbsnBZOwqE,
                https://www.youtube.com/watch?v=zHd3vzyM1fw,
                https://www.youtube.com/watch?v=biOgBfZoPZs,
                https://www.youtube.com/watch?v=ova0NyHbGKA and
                https://www.youtube.com/watch?v=3ErOyCIIqzY
                .
                """}] +
                      [{"role": m["role"], "content": m["content"]}
                       for m in st.session_state.messages]
        )
        # display the response to the chat using `st.write`, then store it in session state.
        with st.chat_message("assistant", avatar="./img/surrey.jpg"):
            response_text = response.choices[0].message.content
            st.write(response_text)
        st.session_state.messages.append({"role": "assistant", "content": response_text})
