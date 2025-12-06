# import os
# import requests
# import json
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# serpapi_key = os.getenv("SERPAPI_KEY")
# site_url = os.getenv("YOUR_SITE_URL", "")
# site_name = os.getenv("YOUR_SITE_NAME", "")

# def call_mistral(prompt):
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {openrouter_api_key}",
#         "Content-Type": "application/json",
#     }
#     if site_url:
#         headers["HTTP-Referer"] = site_url
#     if site_name:
#         headers["X-Title"] = site_name

#     data = {
#         "model": "mistralai/mistral-7b-instruct:free",
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     response_json = response.json()
#     print(f"API Response for prompt '{prompt[:100]}...'response json: {response_json}")  

#     if "choices" not in response_json or not response_json["choices"]:
#         raise ValueError(f"Unexpected API response: {response_json}")

#     message_content = response_json["choices"][0]["message"].get("content", "").strip()

#     # Remove placeholder text like "[OUT]"
#     if "[OUT]" in message_content:
#         message_content = message_content.replace("[OUT]", "").strip()

#     if not message_content:
#         raise ValueError("Empty response from Mistral API")

#     return message_content

# def generate_search_query(topic):
#     prompt = f"Generate a concise search query for the topic: '{topic}'. Do not include '[OUT]' in your response."
#     try:
#         query = call_mistral(prompt)
#         return query
#     except Exception as e:
#         print(f"Error generating query: {e}")
#         return topic  # Fallback: Use the original topic as the query

# def search_web(query):
#     url = f"https://serpapi.com/search.json?q={query}&api_key={serpapi_key}"
#     response = requests.get(url)
#     # print(f"SerpAPI Response for query '{query}' response text: {response.text} response json: {response.json()}")  
#     data = response.json()

#     # Extract snippets from the top search results
#     results = []
#     if "organic_results" in data:
#         for result in data["organic_results"][:3]:  # Get top 3 results
#             if "snippet" in result:
#                 results.append(result["snippet"])
#     else:
#         return "No search results found."

#     return "\n".join(results)

# def summarize(results):
#     prompt = f"""
#     Summarize the following text in detail. Do not include '[OUT]' in your response.
#     Provide a comprehensive summary that captures all key points and relevant details:

#     {results}
#     """
#     try:
#         summary = call_mistral(prompt)
#         return summary
#     except Exception as e:
#         print(f"Error generating summary: {e}")
#         return f"Summary could not be generated. Here are the key details:\n{results[:1000]}..."

# def save_summary(summary, filename="outputs/research_summary.txt"):
#     # Create the outputs directory if it doesn't exist
#     os.makedirs("outputs", exist_ok=True)

#     # Save the summary to a file
#     with open(filename, "w") as file:
#         file.write(summary)

#     print(f"Summary saved to '{filename}'.")

# def main():
#     try:
#         topic = input("Enter your research topic: ")
#         query = generate_search_query(topic)
#         print(f"\nGenerated query: {query}")

#         results = search_web(query)
#         print(f"\nSearch results:\n{results}")

#         summary = summarize(results)
#         print(f"\nSummary:\n{summary}")

#         # Save the summary to a file
#         save_summary(summary)

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()















# old code without serpapi integration

# import os
# import requests
# import json
# from dotenv import load_dotenv

# # Load API keys
# load_dotenv()
# openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# site_url = os.getenv("YOUR_SITE_URL", "")
# site_name = os.getenv("YOUR_SITE_NAME", "")

# def call_mistral(prompt):
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {openrouter_api_key}",
#         "Content-Type": "application/json",
#     }
#     if site_url:
#         headers["HTTP-Referer"] = site_url
#     if site_name:
#         headers["X-Title"] = site_name

#     data = {
#         "model": "mistralai/mistral-7b-instruct:free",
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }

#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     response_json = response.json()
#     print(f"API Response for prompt '{prompt[:50]}...': {response_json}")  # Debug: Print the response

#     if "choices" not in response_json or not response_json["choices"]:
#         raise ValueError(f"Unexpected API response: {response_json}")

#     message_content = response_json["choices"][0]["message"].get("content", "").strip()

#     # Remove placeholder text like "[OUT]"
#     if "[OUT]" in message_content:
#         message_content = message_content.replace("[OUT]", "").strip()

#     if not message_content:
#         raise ValueError("Empty response from Mistral API")

#     return message_content

# def generate_search_query(topic):
#     prompt = f"Generate a concise search query for the topic: '{topic}'. Do not include '[OUT]' in your response."
#     try:
#         query = call_mistral(prompt)
#         return query
#     except Exception as e:
#         print(f"Error generating query: {e}")
#         return topic  # Fallback: Use the original topic as the query

# def summarize(results):
#     prompt = f"""
#     Summarize the following text in 3 clear bullet points. Do not include '[OUT]' in your response.
#     Focus on the key information and be concise:

#     {results}
#     """
#     try:
#         summary = call_mistral(prompt)
#         return summary
#     except Exception as e:
#         print(f"Error generating summary: {e}")
#         return f"Summary could not be generated. Here are the key details:\n{results[:200]}..."

# def main():
#     try:
#         topic = input("Enter your research topic: ")
#         query = generate_search_query(topic)
#         print(f"\nGenerated query: {query}")

#         # Simulate search results (since SerpAPI is not being used)
#         results = f"Search results for '{query}':\n\nLarge Language Models (LLMs) are advanced AI systems trained on vast amounts of text data. They can generate human-like text and are used in a variety of applications, including chatbots, content creation, and code generation. LLMs are important because they enable machines to understand and generate human language, making AI more accessible and useful."
#         print(f"\nSearch results:\n{results}")

#         summary = summarize(results)
#         print(f"\nSummary:\n{summary}")

#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()











































# old version with Mistral 7B Instruct model


# # Load API keys
# load_dotenv()
# openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
# serpapi_key = os.getenv("SERPAPI_KEY")
# site_url = os.getenv("YOUR_SITE_URL", "")
# site_name = os.getenv("YOUR_SITE_NAME", "")

# def call_mistral(prompt):
#     url = "https://openrouter.ai/api/v1/chat/completions"
#     headers = {
#         "Authorization": f"Bearer {openrouter_api_key}",
#         "Content-Type": "application/json",
#     }
#     if site_url:
#         headers["HTTP-Referer"] = site_url
#     if site_name:
#         headers["X-Title"] = site_name

#     data = {
#         "model": "mistralai/mistral-7b-instruct:free",
#         "messages": [
#             {"role": "user", "content": prompt}
#         ]
#     }
#     response = requests.post(url, headers=headers, data=json.dumps(data))
#     response_json = response.json()
#     print("Full API response:", response_json)  # Debug: Print full response

#     if "choices" not in response_json or not response_json["choices"]:
#         raise ValueError(f"Unexpected API response: {response_json}")

#     message_content = response_json["choices"][0]["message"].get("content", "").strip()
#     print("Extracted message content:", message_content) 

#     # Remove placeholder text like ">> [OUT]"
#     if message_content.startswith(">> [OUT]"):
#         message_content = message_content[8:].strip()

#     if not message_content:
#         raise ValueError("Empty response from Mistral API")

#     return message_content

# # Step 1: Generate search query using Mistral 7B Instruct
# def generate_search_query(topic):
#     prompt = f"Generate a concise search query for the topic: '{topic}'."
#     return call_mistral(prompt)

# # Step 2: Perform web search (using SerpAPI)
# def search_web(query):
#     url = f"https://serpapi.com/search.json?q={query}&api_key={serpapi_key}"
#     response = requests.get(url)
#     data = response.json()
#     results = [result["snippet"] for result in data.get("organic_results", [])[:3]]
#     return "\n".join(results)

# # Step 3: Summarize results using Mistral 7B Instruct
# def summarize(results):
#     prompt = f"""
#     Please summarize the following text in 3 clear bullet points.
#     Focus on the key information and be concise:

#     {results}
#     """
#     try:
#         summary = call_mistral(prompt)
#         if not summary:
#             # Fallback: Use a simpler prompt
#             prompt = f"Summarize this in 3 points: {results}"
#             summary = call_mistral(prompt)
#         return summary
#     except Exception as e:
#         print(f"Error generating summary: {e}")
#         return "Summary could not be generated."
    

# # Step 4: Save summary
# def save_summary(summary, filename="outputs/research_summary.txt"):
#     os.makedirs("outputs", exist_ok=True)
#     with open(filename, "w") as f:
#         f.write(summary)

# # Main workflow
# def main():
#     try:
#         topic = input("Enter your research topic: ")
#         query = generate_search_query(topic)
#         print(f"Generated query: {query}")
#         results = search_web(query)
#         print("Search results:\n", results)
#         summary = summarize(results)
#         print("Initial summary attempt:", summary)  # Debug
#         if summary:
#             save_summary(summary)
#             print("Summary saved to 'outputs/research_summary.txt'.")
#         else:
#             print("Summary is empty. Check the API response.")
#     except Exception as e:
#         print(f"An error occurred: {e}")

# if __name__ == "__main__":
#     main()











