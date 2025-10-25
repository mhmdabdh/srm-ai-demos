import os
import re
import subprocess
from typing import List, Dict
from google import genai


# Function 1: Initialize Gemini AI Client
def initialize_genai_client(api_key: str):
    try:
        #configuration = Configuration(api_key=api_key)
        client = genai.Client(api_key=api_key)
        return client
    except ImportError as e:
        raise ImportError("Failed to import Gemini AI Client. Ensure the library is installed.") from e


# Function 2: Read Go Files in Specific Directory
def read_go_files(directory: str) -> List[str]:
    go_files = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".go"):
                go_files.append(os.path.join(root, file))
    return go_files


# Function 3: Static Analysis of Go Code
def analyze_go_file(file_path: str) -> Dict[str, any]:
    with open(file_path, "r") as f:
        lines = f.readlines()

    code_lines = sum(1 for line in lines if line.strip() and not line.strip().startswith("//"))
    comment_lines = sum(1 for line in lines if line.strip().startswith("//"))
    total_lines = len(lines)

    # Basic regex to find function definitions
    function_definitions = re.findall(r"func\s+\w+\(", "".join(lines))
    function_count = len(function_definitions)

    # Example shallow complexity (counts 'if', 'for', 'switch')
    complexity = sum(line.count("if") + line.count("for") + line.count("switch") for line in lines)

    return {
        "file_name": os.path.basename(file_path),
        "total_lines": total_lines,
        "code_lines": code_lines,
        "comment_lines": comment_lines,
        "function_count": function_count,
        "complexity": complexity,
    }


# Function 4: Run gofmt to Analyze Formatting
def run_gofmt(file_path: str):
    try:
        result = subprocess.run(["gofmt", "-l", file_path], capture_output=True, text=True)
        return result.stdout.strip()
    except FileNotFoundError:
        return "gofmt tool not found. Make sure Go is installed and available in PATH."


# Function 5: Use Gemini AI for Advanced Feedback
def analyze_with_genai(client, file_name: str, analysis_data: Dict[str, any], file_content: str) -> str:
    try:
        # Build meaningful prompt for AI analysis
        prompt = (
            f"Analyze the following Go code from the file '{file_name}'. "
            f"Here are some basic metrics for the file:\n"
            f"- Total lines: {analysis_data['total_lines']}\n"
            f"- Code lines: {analysis_data['code_lines']}\n"
            f"- Comment lines: {analysis_data['comment_lines']}\n"
            f"- Number of functions: {analysis_data['function_count']}\n"
            f"- Estimated complexity: {analysis_data['complexity']}\n\n"
            "Now, analyze the code and provide:"
            " 1. Any issues, improvements, or readability concerns.\n"
            " 2. Suggestions to improve maintainability, modularity, and clarity.\n"
            " 3. Insights on logic and performance optimizations.\n\n"
            f"CODE:\n```go\n{file_content}\n```"
        )
        # Call Gemini AI for an analysis
        response = client.models.generate_content( model="gemini-2.0-flash", contents=prompt)
        #return response.result_dict['text']  # Handle based on API response structure
        return response.text
    except Exception as e:
        return f"Error with Gemini AI analysis: {str(e)}"
def compute_score(static_analysis: Dict, ai_insights: str) -> float:
    """
       Combines static metrics and AI insights into a raw score:
       - More code lines, quality comments, functions = higher score
       - Lower complexity = better score
       Adjust weights as needed for your use case.
       """
    # Static scoring
    score = (
            static_analysis["code_lines"] * 1.5 +  # More code lines
            static_analysis["comment_lines"] * 2.0 +  # Well-commented code
            static_analysis["function_count"] * 3.0  # More modularity
            - static_analysis["complexity"] * 1.5  # Lower complexity is better
    )

    # AI-based adjustments: simple heuristic
    if "excellent" in ai_insights.lower():
        score += 10  # Bonus points for exceptional feedback
    if "needs improvement" in ai_insights.lower():
        score -= 5  # Deduction for improvement areas
    if "security issue" in ai_insights.lower() or "bug" in ai_insights.lower():
        score -= 10  # Penalize for security or bug issues

    return max(score, 0)  # Ensure the score doesn't drop below zero


# Function 6: Generate Consolidated Report
def generate_report(go_analysis_results: List[Dict], ai_insights: List[str], scores: List[float]):
    print("\n=== Go Code Quality Report ===\n")
    ranked_results = sorted(
        zip(go_analysis_results, ai_insights, scores),
        key=lambda x: x[2],  # Sort by score
        reverse=True
    )
    for idx, (result, insight, score) in enumerate(ranked_results):
        print(f"Rank #{idx + 1}: {result['file_name']} (Score: {score:.2f})")
        print(f"- Total Lines: {result['total_lines']}")
        print(f"- Code Lines (Excluding Comments): {result['code_lines']}")
        print(f"- Comment Lines: {result['comment_lines']}")
        print(f"- Number of Functions: {result['function_count']}")
        print(f"- Estimated Complexity: {result['complexity']}")

        print("\n--- AI Insights ---")
        print(insight)
        print("=" * 40)

        # Highlight the top-ranked assignment
    top_file = ranked_results[0][0]["file_name"]
    print(f"\n>>> The top-rated assignment is: {top_file}")


# Main Function
def main():
    # Directory containing Go files (Updated based on your request)
    target_directory = "/Users/mohammed.abdullah/Documents/05_go_assignments"

    # API Key for Gemini AI
    #api key = to be entered here   # Replace this with your actual API Key
    client = initialize_genai_client(api_key)

    # Gather Go files
    go_files = read_go_files(target_directory)
    if not go_files:
        print("No Go files found in the target directory.")
        return

    # Analyze each Go file
    go_analysis_results = []
    ai_insights = []
    scores = []

    for file_path in go_files:
        # Static analysis
        analysis_result = analyze_go_file(file_path)
        go_analysis_results.append(analysis_result)

        # Advanced analysis using Gemini AI
        with open(file_path, "r") as f:
            file_content = f.read()
            insight = analyze_with_genai(client, analysis_result['file_name'], analysis_result, file_content)
            ai_insights.append(insight)

        # Compute score for ranking
        score = compute_score(analysis_result, insight)
        scores.append(score)

        # Print consolidated report and rank assignments
    generate_report(go_analysis_results, ai_insights, scores)


if __name__ == "__main__":
    main()
