import streamlit as st
import google.generativeai as genai

# Function to get response from Gemini
def get_gemini_response(prompt, api_key):
    default_prompt = "Please provide a detailed job description summary, separating key points and main content clearly. Keep the output concise and informative."
    full_prompt = f"{default_prompt}\n\n{prompt}"
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        response = model.generate_content(full_prompt)
        return response.text.strip()
    except Exception as e:
        st.error(f"Error with Gemini service: {str(e)}")
        return "Sorry, I couldn't process your request."

# Streamlit app layout
st.set_page_config(page_title="ProJob Summarizer", layout="wide")

# Sidebar for API key input
with st.sidebar:
    st.header("Login")
    api_key = st.text_input("Enter your Gemini API Key:", type="password")
    login_button = st.button("Login")

# Check if user is logged in
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if login_button and api_key:
    st.session_state.logged_in = True
    st.success("Successfully logged in!")

# Display logout button if logged in
if st.session_state.logged_in:
    st.title("ProJob Summarizer")
    st.markdown("A professional tool to summarize job descriptions and provide key insights.")

    # Logout button
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    # Chat interface layout
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat history
    chat_container = st.container()
    with chat_container:
        for message in st.session_state.messages:
            if message["role"] == "assistant":
                st.markdown(f"**JobSum Agent:** {message['content']}")
            elif message["role"] == "user":
                st.markdown(f"**You:** {message['content']}")

        # User input
        user_input = st.text_input("Type your message here...")

        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.markdown(f"**You:** {user_input}")

            # Get response from the agent
            response = get_gemini_response(user_input, api_key)
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.markdown(f"**JobSum Agent:** {response}")
else:
    st.error("Please login to continue.")
