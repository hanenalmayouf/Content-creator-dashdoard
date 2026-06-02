import pypdf
import os

pdf_path = "/Users/halmayyof/Desktop/مراجع الوثيقه/مراجع البحوث/R10.pdf"
keywords = ["strategy", "strategies"]

if os.path.exists(pdf_path):
    with open(pdf_path, 'rb') as f:
        reader = pypdf.PdfReader(f)
        matches = []
        for page_num in range(len(reader.pages)):
            text = reader.pages[page_num].extract_text()
            if text:
                lines = text.split("\n")
                for line in lines:
                    if any(kw in line.lower() for kw in keywords):
                        matches.append((page_num + 1, line))
        
        print(f"Found {len(matches)} matches in R10.pdf:")
        for page, line in matches[:40]:
            print(f"[Page {page}] {line.strip()}")
else:
    print("R10.pdf does not exist")
