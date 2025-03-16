import re
from collections import Counter
import sys

# 출력 인코딩 설정
sys.stdout.reconfigure(encoding='utf-8')

# 파일 경로 설정
file_path = r"C:\Users\min99\Downloads\mission_computer_main.log"
output_path = "log_analysis.md"

def read_logs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def parse_logs(logs):
    pattern = r'\[(ERROR|INFO|WARN)\]\s+(.*)'
    parsed_logs = [re.findall(pattern, log)[0] for log in logs if re.search(pattern, log)]
    return parsed_logs

def analyze_logs(parsed_logs):
    error_messages = [log[1] for log in parsed_logs if log[0] == 'ERROR']
    most_common_errors = Counter(error_messages).most_common(5)
    
    summary = {
        'total_logs': len(parsed_logs),
        'total_errors': len(error_messages),
        'most_common_errors': most_common_errors
    }
    return summary

def generate_markdown_report(summary, output_path):
    md_content = f"""
# Log Analysis Report

## Summary
- Total Logs: {summary['total_logs']}
- Total Errors: {summary['total_errors']}

## Top 5 Errors
"""
    for error, count in summary['most_common_errors']:
        md_content += f"- **{error}**: {count} times\n"

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(md_content)

    print(f"Report saved to {output_path}")

def main():
    print("📂 Reading logs...")  # 이모지 출력 가능
    logs = read_logs(file_path)
    
    print("🛠️ Parsing logs...")
    parsed_logs = parse_logs(logs)
    
    print("📊 Analyzing logs...")
    summary = analyze_logs(parsed_logs)
    
    print("📝 Generating report...")
    generate_markdown_report(summary, output_path)
    
    print("✅ Log analysis complete!")

if __name__ == "__main__":
    main()
