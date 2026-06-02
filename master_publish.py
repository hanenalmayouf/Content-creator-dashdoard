
import os
import re
import shutil

# List of all files to process
slides_files = [
    'Ultralytics_Foundations_1_Tasks_Inference.qmd',
    'Ultralytics_Foundations_2_Real_World_Use_Cases.qmd',
    'Ultralytics_Foundations_3_Custom_Data_Training.qmd',
    'Ultralytics_Foundations_4_Evaluation_Deployment.qmd',
    'HuggingFace_CV_Part5.qmd',
    'Image_Foundations.qmd'
]

BASE_DIR = '/Users/halmayyof/Test3/test3/ذد/cv-for-developers-ultralytics/slides'
DOCS_DIR = '/Users/halmayyof/Test3/test3/ذد/cv-for-developers-ultralytics/docs'

SILENT_PATCH = r"""
```{python}
#| echo: false
#| output: false
import matplotlib.pyplot as plt
try:
    import matplotlib_inline.backend_inline
    matplotlib_inline.backend_inline.set_matplotlib_formats('svg')
except:
    pass
plt.rcParams['svg.fonttype'] = 'none'

def fix_ar(text):
    return text
```
"""

def process_files():
    for filename in slides_files:
        filepath = os.path.join(BASE_DIR, filename)
        if not os.path.exists(filepath):
            print(f"Skipping {filename} - not found.")
            continue
            
        with open(filepath, 'r') as f:
            content = f.read()
            
        # 1. Remove any old patches or technical printouts
        content = re.sub(r'print\("SVG-Native.*?\)\n', '', content)
        content = re.sub(r'print\("Arabic SVG support.*?\)\n', '', content)
        
        # 2. Inject Silent Patch after YAML
        if "---" in content:
            parts = content.split("---", 2)
            if len(parts) >= 3:
                if "matplotlib_inline.backend_inline" not in parts[2]:
                    content = "---" + parts[1] + "---" + SILENT_PATCH + parts[2]
        
        with open(filepath, 'w') as f:
            f.write(content)
        print(f"Patched {filename}")

def deploy_assets():
    docs_slides_dir = os.path.join(DOCS_DIR, 'slides')
    if not os.path.exists(docs_slides_dir):
        os.makedirs(docs_slides_dir)
    
    # Copy all .html files and their associated _files directories
    for item in os.listdir(BASE_DIR):
        src_path = os.path.join(BASE_DIR, item)
        dst_path = os.path.join(docs_slides_dir, item)
        
        if item.endswith('.html'):
            shutil.copy2(src_path, dst_path)
            
        if item.endswith('_files'):
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            
        if item in ['assets', 'slides_template', 'outputs']:
            if os.path.exists(dst_path):
                shutil.rmtree(dst_path)
            shutil.copytree(src_path, dst_path)
            
        if item.endswith('.png') or item.endswith('.jpg') or item.endswith('.svg'):
             shutil.copy2(src_path, dst_path)

    print("Fully deployed slides, dependencies, and assets to docs/slides/")

def create_index():
    repo_url = "https://colab.research.google.com/github/hanenalmayouf/Computer_vision_Arabic-/blob/main/labs/"
    
    index_html = f"""
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>منهج الرؤية الحاسوبية - SDAIA</title>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;700;800&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; background: #f0f4f8; margin: 0; padding: 0; color: #1C355E; }}
        header {{ background: linear-gradient(135deg, #1C355E, #00C9A7); color: white; padding: 4rem 1rem; text-align: center; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }}
        .container {{ max-width: 1200px; margin: 2rem auto; padding: 1rem; }}
        h1 {{ margin: 0; font-size: 2.8rem; font-weight: 800; }}
        .section-title {{ margin: 3rem 0 2rem; color: #1C355E; text-align: center; font-size: 2.2rem; font-weight: 800; }}
        .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 2.5rem; }}
        .card {{ background: white; border-radius: 24px; padding: 2.5rem; transition: 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); box-shadow: 0 10px 30px rgba(0,0,0,0.05); border: 1px solid #eef2f7; display: flex; flex-direction: column; }}
        .card:hover {{ transform: translateY(-10px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); border-color: #00C9A7; }}
        .card h3 {{ margin: 0 0 1rem 0; color: #1C355E; font-size: 1.5rem; font-weight: 800; }}
        .card p {{ margin: 0 0 2.5rem 0; font-size: 1rem; color: #546e7a; line-height: 1.6; flex-grow: 1; }}
        .badge {{ display: inline-block; padding: 6px 14px; border-radius: 12px; font-size: 0.8rem; font-weight: 700; margin-bottom: 1.2rem; background: #e0f2f1; color: #00796b; width: fit-content; }}
        .btn-group {{ display: flex; gap: 12px; flex-wrap: wrap; }}
        .btn {{ flex: 1; min-width: 130px; text-align: center; padding: 14px 20px; border-radius: 15px; font-weight: 700; text-decoration: none; font-size: 0.95rem; transition: 0.3s; display: flex; align-items: center; justify-content: center; gap: 8px; }}
        .btn-slides {{ background: #1C355E; color: white; }}
        .btn-slides:hover {{ background: #2c5282; }}
        .btn-lab {{ background: #00C9A7; color: white; }}
        .btn-lab:hover {{ background: #00a88b; }}
        .footer {{ text-align: center; padding: 4rem 2rem; color: #94a3b8; font-size: 0.9rem; border-top: 1px solid #e2e8f0; margin-top: 4rem; }}
        img.logo {{ width: 140px; margin-bottom: 1.5rem; }}
    </style>
</head>
<body>
    <header>
        <img src="slides/slides_template/assets/sdaia.svg" alt="SDAIA" class="logo">
        <h1>منهج الرؤية الحاسوبية الاحترافي</h1>
        <p>مسار تطوير الأنظمة باستخدام YOLO و HuggingFace</p>
    </header>
    
    <div class="container">
        <h2 class="section-title">خارطة الطريق التعليمية 🗺️</h2>
        <div class="grid">
            <!-- Module 0 -->
            <div class="card">
                <span class="badge">الوحدة التمهيدية</span>
                <h3>0. أساسيات الصورة الرقمية</h3>
                <p>تعلم كيف يفهم الكمبيوتر الصور، البكسلات، القنوات اللونية، وأنظمة الإحداثيات.</p>
                <div class="btn-group">
                    <a href="slides/Image_Foundations.html" class="btn btn-slides">🎥 عرض المحاضرة</a>
                    <a href="{repo_url}00_images.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل</a>
                </div>
            </div>

            <!-- Module 1 -->
            <div class="card">
                <span class="badge">الجزء الأول</span>
                <h3>1. المهام والاستدلال</h3>
                <p>اكتشف قدرات YOLO في الاكتشاف، التجزئة، التصنيف، وتقدير الوضعية.</p>
                <div class="btn-group">
                    <a href="slides/Ultralytics_Foundations_1_Tasks_Inference.html" class="btn btn-slides">🎥 عرض المحاضرة</a>
                    <a href="{repo_url}01_tasks_inference_ar.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل</a>
                </div>
            </div>

            <!-- Module 2 -->
            <div class="card">
                <span class="badge">الجزء الثاني</span>
                <h3>2. تطبيقات العالم الحقيقي</h3>
                <p>ما وراء الصناديق: تحليل المناطق، التتبع الحركي، والخرائط الحرارية للفيديو.</p>
                <div class="btn-group">
                    <a href="slides/Ultralytics_Foundations_2_Real_World_Use_Cases.html" class="btn btn-slides">🎥 عرض المحاضرة</a>
                    <a href="{repo_url}02_solutions_expanded.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل A</a>
                    <a href="{repo_url}02b_video_engineering.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل B</a>
                </div>
            </div>

            <!-- Module 3 -->
            <div class="card">
                <span class="badge">الجزء الثالث</span>
                <h3>3. تدريب النماذج المخصصة</h3>
                <p>تجهيز البيانات الخاصة، ضبط المعاملات الفائقة، وبدء دورات التدريب.</p>
                <div class="btn-group">
                    <a href="slides/Ultralytics_Foundations_3_Custom_Data_Training.html" class="btn btn-slides">🎥 عرض المحاضرة</a>
                    <a href="{repo_url}03_custom_training.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل</a>
                </div>
            </div>

            <!-- Module 4 -->
            <div class="card">
                <span class="badge">الجزء الرابع</span>
                <h3>4. التقييم والنشر</h3>
                <p>فهم مصفوفة الارتباك، IoU، الدقة، الاستدعاء، وتصدير النماذج للإنتاج.</p>
                <div class="btn-group">
                    <a href="slides/Ultralytics_Foundations_4_Evaluation_Deployment.html" class="btn btn-slides">🎥 عرض المحاضرة</a>
                    <a href="{repo_url}04a_roi_evaluation.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل A</a>
                    <!-- <a href="{repo_url}04b_evaluation_technical.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل B</a> -->
                </div>
            </div>

            <!-- Module 5 -->
            <!--
            <div class="card">
                <span class="badge">الجزء الخامس</span>
                <h3>5. نظام HuggingFace للرؤية</h3>
                <p>استخدام SAM 3 للتجزئة، والبحث بالصور، ونماذج لغة الرؤية المتعددة.</p>
                <div class="btn-group">
                    <a href="slides/HuggingFace_CV_Part5.html" class="btn btn-slides">🎥 عرض المحاضرة</a>
                    <a href="{repo_url}05_huggingface_cv_ar.ipynb" class="btn btn-lab" target="_blank">🧪 المعمل</a>
                </div>
            </div>
            -->
        </div>
    </div>

    <div class="footer">
        © 2026 جميع الحقوق محفوظة لـ سدايا (SDAIA) <br>
        منهج الرؤية الحاسوبية المطور لتمكين الكوادر الوطنية.
    </div>
</body>
</html>
"""
    if not os.path.exists(DOCS_DIR): os.makedirs(DOCS_DIR)
    
    with open(os.path.join(DOCS_DIR, 'index.html'), 'w') as f:
        f.write(index_html)
    
    # Root index for backup
    root_index = os.path.join('/Users/halmayyof/Test3/test3/ذد/cv-for-developers-ultralytics/', 'index.html')
    with open(root_index, 'w') as f:
        f.write(index_html.replace('href="slides/', 'href="docs/slides/'))

    print("Created card-based index.html in docs/ and root.")

if __name__ == "__main__":
    process_files()
    deploy_assets()
    create_index()
