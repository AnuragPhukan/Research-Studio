from datetime import datetime
from langchain.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun, WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

search_tool = DuckDuckGoSearchRun()
wiki_api = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=1000)
wiki_tool = WikipediaQueryRun(api_wrapper=wiki_api)


@tool
def save_to_txt(data: str, filename: str = "research_output.txt") -> str:
    """Save text data to a local .txt file with a timestamp header."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = (
        f"--- Research Output ---\n"
        f"Timestamp: {timestamp}\n\n"
        f"{data}\n\n"
    )
    with open(filename, "a", encoding="utf-8") as file:
        file.write(formatted_text)
    return f"Data successfully saved to {filename}"

def save_to_file(filename: str, content: str) -> None:
    """Saves the given content to a file with the specified filename."""
    with open(filename, 'w') as file:
        file.write(content) 
