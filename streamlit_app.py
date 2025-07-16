import streamlit as st
import requests

st.set_page_config(page_title="🧠 Smart Local Discovery Chatbot", page_icon="🌍")

st.markdown("""
    <div style='text-align: center;'>
        <img src="https://cdn-icons-png.flaticon.com/512/4712/4712109.png" width="80" />
        <h1>Smart Local Discovery Chatbot</h1>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
Welcome! Ask anything about local services, events, or general topics.  
Try queries like:
- *Find vegetarian restaurants within 2 km of MG Road, Bengaluru*
- *Top-rated dentists in Bengaluru*
- *Trending events in Jaipur this weekend*
""")

query = st.text_input("Enter your query:", key="user_input", help="Example: Top-rated dentists in Bengaluru")

if st.button("🔍 Search"):
    if not query.strip():
        st.warning("❗ Please enter a valid query.")
    else:
        with st.spinner("Processing your request..."):
            response = requests.post("http://localhost:8000/search", json={"query": query})
            if response.status_code == 200:
                data = response.json()
                answer = data.get("response")
                if answer:
                    if "1." in answer and "2." in answer and "3." in answer:
                        st.success("✅ Here are the top 3 results:")
                    else:
                        st.success("✅ Here's what I found:")
                    st.markdown(answer)
                else:
                    st.error("😕 Sorry, no relevant results found.")
            else:
                st.error("🚫 Failed to fetch response from the backend.")

# Custom CSS
st.markdown("""
<style>
/* ✅ Input box style */
input:focus, textarea:focus {
    border: 2px solid #2684FF !important;  /* Blue border */
    box-shadow: 0 0 0 0.2rem rgba(38,132,255,0.25);
    outline: none !important;
}
input, textarea {
    border-radius: 8px !important;
    padding: 10px !important;
    border: 1px solid #ccc;
    font-size: 1rem;
}

/* ✅ Clean and modern button styling (No red) */
button[kind="primary"] {
    border-radius: 8px;
    background-color: #1f77b4; /* Professional blue */
    color: white !important;
    border: none;
    padding: 0.6rem 1.5rem;
    font-weight: 600;
    font-size: 1rem;
    transition: background-color 0.3s ease, transform 0.2s ease;
}

/* ✅ Button hover effect */
button[kind="primary"]:hover {
    background-color: #145a86; /* Darker blue on hover */
    color: white !important;
    transform: translateY(-1px);
}

/* ✅ Remove red or default focus effects */
button:focus {
    outline: none !important;
    box-shadow: none !important;
}
</style>
""", unsafe_allow_html=True)



