import os
from datetime import datetime
from research_agent import ResearchResponse, run_research, save_report_docx


query = input("Enter your research query: ")
structured_response = run_research(query)

print(structured_response)
if isinstance(structured_response, ResearchResponse):
    print(structured_response.model_dump())

try:
    print("Do you want to save this as a file? (Yes/No): ", end="", flush=True)
    save_choice = input().strip().lower()
except EOFError:
    save_choice = "no"

if save_choice in {"yes", "y"}:
    reports_dir = os.path.join(os.path.dirname(__file__), "reports")
    os.makedirs(reports_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"report_{timestamp}.docx"
    filepath = os.path.join(reports_dir, filename)
    save_report_docx(structured_response, filepath)
    print(f"Saved report to {filepath}")
