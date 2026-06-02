import zipfile
import xml.etree.ElementTree as ET
import os

def extract_text_from_docx(docx_path):
    try:
        with zipfile.ZipFile(docx_path) as docx:
            xml_content = docx.read('word/document.xml')
            root = ET.fromstring(xml_content)
            ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
            
            paragraphs = []
            for para in root.findall('.//w:p', ns):
                text_runs = []
                for run in para.findall('.//w:t', ns):
                    if run.text:
                        text_runs.append(run.text)
                text = "".join(text_runs).strip()
                if text:
                    paragraphs.append(text)
            return paragraphs
    except Exception as e:
        return [f"Error: {e}"]

desktop_dir = "/Users/halmayyof/Desktop"
docx_path = "/Users/halmayyof/Desktop/١١وثيقة الدراسة والتخطيط لمشروع تفعيل حاﻻت استخدام الذكاء اﻹصطناعي في التعليم.docx"

paragraphs = extract_text_from_docx(docx_path)

print("Searching for Use Cases (حالات استخدام) or educational categories...")
for i, para in enumerate(paragraphs):
    if "حالة" in para or "حالات" in para or "استخدام" in para:
        if i > 250: # focus on chapter 2 or late chapter 1
            print(f"[{i}] {para}")
            print("-" * 30)
