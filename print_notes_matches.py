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

docx_path = "/Users/halmayyof/Desktop/مراجع الوثيقه/مرافق الكراسه/١١وثيقة الدراسة والتخطيط لمشروع تفعيل حاﻻت استخدام الذكاء اﻹصطناعي في التعليم[1] ملاحظات الفصل الاول.docx"
paragraphs = extract_text_from_docx(docx_path)

print("Printing Paragraphs 35 to 135:")
for i in range(35, 135):
    if i < len(paragraphs):
        print(f"[{i}] {paragraphs[i]}")
        print("-" * 30)
