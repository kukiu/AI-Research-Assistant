import os
import requests
import json
import streamlit as st
from dotenv import load_dotenv

# Load API keys
load_dotenv()
openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
serpapi_key = os.getenv("SERPAPI_KEY")
site_url = os.getenv("YOUR_SITE_URL", "")
site_name = os.getenv("YOUR_SITE_NAME", "")


def fetch_dynamic_image(keyword="research-paper"):
    url = f"https://api.unsplash.com/photos/random?query={keyword}&client_id={os.getenv('UNSPLASH_API_KEY')}"
    response = requests.get(url)
    data = response.json()
    return data["urls"]["regular"]
 

def call_mistral(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {openrouter_api_key}",
        "Content-Type": "application/json",
    }
    if site_url:
        headers["HTTP-Referer"] = site_url
    if site_name:
        headers["X-Title"] = site_name

    data = {
        "model": "mistralai/mistral-7b-instruct:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))
    response_json = response.json()

    if "choices" not in response_json or not response_json["choices"]:
        raise ValueError(f"Unexpected API response: {response_json}")

    message_content = response_json["choices"][0]["message"].get("content", "").strip()

    if "[OUT]" in message_content:
        message_content = message_content.replace("[OUT]", "").strip()

    if not message_content:
        raise ValueError("Empty response from Mistral API")

    return message_content

def generate_search_query(topic):
    prompt = f"Generate a concise search query for the topic: '{topic}'. Do not include '[OUT]' in your response."
    try:
        query = call_mistral(prompt)
        return query
    except Exception as e:
        st.error(f"Error generating query: {e}")
        return topic

def search_web(query, num_results=5):
    url = f"https://serpapi.com/search.json?q={query}&api_key={serpapi_key}"
    response = requests.get(url)
    data = response.json()

    results = []
    if "organic_results" in data:
        for result in data["organic_results"][:num_results]:
            if "snippet" in result:
                results.append(result["snippet"])
    else:
        return "No search results found."

    return "\n".join(results)

def summarize(results, language="English"):
    language_map = {
        "English": "English",
        "Spanish": "Spanish",
        "French": "French",
        "German": "German",
        "Hindi": "Hindi"
    }
    lang = language_map.get(language, "English")

    prompt = f"""
    Summarize the following text in detail in {lang}. Do not include '[OUT]' in your response.
    Provide a comprehensive summary that captures all key points and relevant details:

    {results}
    """
    try:
        summary = call_mistral(prompt)
        return summary
    except Exception as e:
        st.error(f"Error generating summary: {e}")
        return f"Summary could not be generated. Here are the key details:\n{results[:500]}..."

def save_summary(summary, filename="outputs/research_summary.txt"):
    os.makedirs("outputs", exist_ok=True)
    with open(filename, "w") as file:
        file.write(summary)
    return filename

def main():
    st.title("AI Research Assistant")
    st.markdown("""<style>.big-font {    font-size:20px !important;}</style>""", unsafe_allow_html=True)
    st.markdown('<p class="big-font">Enter a topic to generate a detailed summary.</p>', unsafe_allow_html=True)

    # Fetch and display a dynamic image
    image_keyword = st.session_state.get('image_keyword', 'AI')
    image_url = fetch_dynamic_image(image_keyword)
    st.image(image_url, width=300, caption=f"Image related to '{image_keyword}'")

    # Sidebar for additional options
    st.sidebar.title("Options")
    num_results = st.sidebar.slider("Number of search results:", 1, 10, 5)
    language = st.sidebar.selectbox("Summary Language:",["English", "Spanish", "French", "German", "Hindi"])

    if 'image_keyword' not in st.session_state:
        st.session_state.image_keyword = image_keyword

    st.sidebar.markdown("---")
    st.sidebar.markdown("**About**: This AI Research Assistant fetches real-time search (only text) results and generates detailed summaries.")
    st.sidebar.markdown("---**Example Topics**:")
    st.sidebar.markdown("- Artificial Intelligence")
    st.sidebar.markdown("- Renewable Energy")
    st.sidebar.markdown("- Blockchain Technology")

    topic = st.text_input("Research Topic:")
    if st.button("Generate Summary"):
        if not topic:
            st.warning("Please enter a research topic.")
            return

        with st.spinner("Generating summary..."):
            query = generate_search_query(topic)
            st.subheader(f"Generated Query:")
            st.write(query)

            results = search_web(query, num_results)
            st.subheader("Search Results:")
            st.write(results)

            summary = summarize(results, language)
            st.subheader("Summary:")
            st.markdown(f"**Summary in {language}:**")
            st.write(summary)

            filename = save_summary(summary)
            st.success(f"Summary saved to '{filename}'.")

            with open(filename, "r") as file:
                st.download_button(
                    label="Download Summary",
                    data=file,
                    file_name=filename,
                    mime="text/plain"
                )

if __name__ == "__main__":
    main()

# def main():
#     st.title("AI Research Assistant")
#     st.markdown("""<style>.big-font {    font-size:20px !important;}</style>""", unsafe_allow_html=True)
#     st.markdown('<p class="big-font">Enter a topic to generate a detailed summary.</p>', unsafe_allow_html=True)

#     st.image("https://img.freepik.com/free-vector/artificial-intelligence-concept-illustration_114360-6182.jpg?w=740&t=st=1699299920~exp=1699300520~hmac=89e9f7e3f7b7e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2e2", width=300)

#         # Sidebar for additional options
#     st.sidebar.title("Options")
#     num_results = st.sidebar.slider("Number of search results:", 1, 10, 5)
#     language = st.sidebar.selectbox("Summary Language:",["English", "Spanish", "French", "German", "Hindi"])


    
#     st.sidebar.markdown("**Example Topics**:")
#     st.sidebar.markdown("**About**: This AI Research Assistant fetches real-time search results and generates detailed summaries.")
#     st.sidebar.markdown("- Artificial Intelligence")
#     st.sidebar.markdown("- Renewable Energy")
#     st.sidebar.markdown("- Blockchain Technology")

#     topic = st.text_input("Research Topic:")
#     if st.button("Generate Summary"):
#         if not topic:
#             st.warning("Please enter a research topic.")
#             return

#         with st.spinner("Generating summary..."):
#             query = generate_search_query(topic)
#             st.subheader(f"Generated Query:")
#             st.write(query)

#             results = search_web(query, num_results)
#             st.subheader("Search Results:")
#             st.write(results)

#             summary = summarize(results, language)
#             st.subheader("Summary:")
#             st.markdown(f"**Summary in {language}:**")
#             st.write(summary)

#             filename = save_summary(summary)
#             # st.success(f"Summary saved to '{filename}'.")

#             with open(filename, "r") as file:
#                 st.download_button(
#                     label="Download Summary",
#                     data=file,
#                     file_name=filename,
#                     mime="text/plain"
#                 )






# if you want to remove custom theme, just remove data/text of config.toml

# [theme]
# primaryColor = "#1f77b4"
# backgroundColor = "rgba(92, 159, 160, 1)"
# secondaryBackgroundColor = "#eaefe9ff"
# textColor = "#0f0d0aff"
# font = "sans serif"
