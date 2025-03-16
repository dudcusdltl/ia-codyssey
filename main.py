print('Hello Mars')


def read_logs(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()

def parse_logs(logs):
    parsed_logs = []
    for log in logs:
        if '[' in log and ']' in log:
            start = log.index('[') + 1
            end = log.index(']')
            level = log[start:end]
            message = log[end + 2:].strip()
            if level in ('ERROR', 'INFO', 'WARN'):
                parsed_logs.append((level, message))
    return parsed_logs

def analyze_logs(parsed_logs):
    total_logs = len(parsed_logs)
    total_errors = sum(1 for log in parsed_logs if log[0] == 'ERROR')

    error_count = {}
    for log in parsed_logs:
        if log[0] == 'ERROR':
            error_count[log[1]] = error_count.get(log[1], 0) + 1

    most_common_errors = sorted(error_count.items(), key=lambda x: x[1], reverse=True)[:5]

    summary = {
        'total_logs': total_logs,
        'total_errors': total_errors,
        'most_common_errors': most_common_errors
    }
    return summary

def generate_markdown_report(summary, output_path):
    md_content = f'''\
# Log Analysis Report

## Summary
- Total Logs: {summary['total_logs']}
- Total Errors: {summary['total_errors']}

## Top 5 Errors
'''

    for error, count in summary['most_common_errors']:
        md_content += f'- **{error}**: {count} times\n'

    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(md_content)

    print(f'Report saved to {output_path}')

def main():
    file_path = r'C:\Users\min99\Downloads\mission_computer_main.log'
    output_path = 'log_analysis.md'

    print('Reading logs...')
    logs = read_logs(file_path)

    print('Parsing logs...')
    parsed_logs = parse_logs(logs)

    print('Analyzing logs...')
    summary = analyze_logs(parsed_logs)

    print('Generating report...')
    generate_markdown_report(summary, output_path)

    print('Log analysis complete!')

if __name__ == '__main__':
    main()
