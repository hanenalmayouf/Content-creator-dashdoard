import json

with open('generator.py', 'r', encoding='utf-8', errors='replace') as f:
    lines = f.readlines()

new_lines = lines[:139] + [
    '            response_mime_type="application/json",\n',
    '            response_schema=MANUAL_SYLLABUS_SCHEMA\n',
    '        )\n',
    '    )\n',
    '    \n',
    '    try:\n',
    '        return json.loads(response.text)\n',
    '    except Exception as e:\n',
    '        print(f"Error parsing JSON: {e}")\n',
    '        return get_mock_syllabus(topic, weeks_count, days_per_week)\n'
] + lines[242:]

with open('generator.py', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
