import os
from datetime import datetime
from flask import Flask, render_template, request, send_from_directory
from research_agent import ResearchResponse, run_research, save_report_docx

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = os.path.join(BASE_DIR, "reports")

app = Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def index():
    data = None
    error = None
    saved = False
    filename = None
    query = ""

    if request.method == "POST":
        query = request.form.get("query", "").strip()
        if not query:
            error = "Please enter a research query."
        else:
            response = run_research(query)
            if isinstance(response, ResearchResponse):
                data = {
                    "topic": response.topic,
                    "report": response.report,
                    "sources": response.sources,
                    "tools_used": response.tools_used,
                }
            else:
                data = {
                    "topic": query,
                    "report": str(response),
                    "sources": [],
                    "tools_used": [],
                }

            os.makedirs(REPORT_DIR, exist_ok=True)
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"report_{timestamp}.docx"
            filepath = os.path.join(REPORT_DIR, filename)
            save_report_docx(response, filepath)
            saved = True

    return render_template(
        "index.html",
        data=data,
        error=error,
        saved=saved,
        filename=filename,
        query=query,
    )


@app.route("/download/<path:filename>", methods=["GET"])
def download(filename):
    filepath = os.path.join(REPORT_DIR, filename)
    if not os.path.exists(filepath):
        return ("Report not found.", 404)
    return send_from_directory(REPORT_DIR, filename, as_attachment=True)


if __name__ == "__main__":
    app.run(debug=True)
