import os
import shutil
import json
import subprocess
from typing import List, Dict, Any
import google.generativeai as genai
from pydantic import BaseModel, Field
import nbformat as nbf
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
api_key = os.getenv("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key, transport='rest')

# Manual OpenAPI schema for Syllabus (Structured Output) to prevent Pydantic V2 translation failures in Gemini API
MANUAL_SYLLABUS_SCHEMA = {
    "type": "OBJECT",
    "properties": {
        "title": {
            "type": "STRING", 
            "description": "عنوان الدورة التدريبية باللغة العربية"
        },
        "description": {
            "type": "STRING", 
            "description": "وصف عام وموجز للدورة باللغة العربية"
        },
        "weeks": {
            "type": "ARRAY",
            "description": "الأسابيع التدريبية للدورة",
            "items": {
                "type": "OBJECT",
                "properties": {
                    "week_number": {
                        "type": "INTEGER", 
                        "description": "رقم الأسبوع (مثال: 1، 2...)"
                    },
                    "title": {
                        "type": "STRING", 
                        "description": "عنوان الأسبوع باللغة العربية"
                    },
                    "days": {
                        "type": "ARRAY",
                        "description": "قائمة الأيام التدريبية داخل الأسبوع",
                        "items": {
                            "type": "OBJECT",
                            "properties": {
                                "day_number": {
                                    "type": "INTEGER", 
                                    "description": "رقم اليوم التدريبي (1، 2، 3...)"
                                },
                                "title": {
                                    "type": "STRING", 
                                    "description": "عنوان درس اليوم باللغة العربية"
                                },
                                "description": {
                                    "type": "STRING", 
                                    "description": "وصف مختصر وشامل لمحتوى الدرس باللغة العربية"
                                },
                                "objectives": {
                                    "type": "ARRAY",
                                    "description": "قائمة الأهداف التعليمية لدرس اليوم باللغة العربية",
                                    "items": {"type": "STRING"}
                                },
                                "strategies": {
                                    "type": "ARRAY",
                                    "description": "قائمة بالاستراتيجيات التعليمية المطبقة في هذا الدرس",
                                    "items": {"type": "STRING"}
                                },
                                "strategy_application": {
                                    "type": "STRING", 
                                    "description": "شرح مفصل لكيفية تطبيق وتفعيل الاستراتيجية في الأنشطة التعليمية"
                                },
                                "lesson_id": {
                                    "type": "STRING", 
                                    "description": "معرف فريد للدرس (مثال: w1d1, w1d2...)"
                                }
                            },
                            "required": ["day_number", "title", "description", "objectives", "strategies", "strategy_application", "lesson_id"]
                        }
                    }
                },
                "required": ["week_number", "title", "days"]
            }
        }
    },
    "required": ["title", "description", "weeks"]
}

# Default template paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(BASE_DIR, "templates")
GENERATED_DIR = os.path.join(BASE_DIR, "generated_lessons")

def get_quarto_path() -> str:
    local_path = "/Users/halmayyof/Test3/test3/ذد/quarto-bin/bin/quarto"
    if os.path.exists(local_path):
        return local_path
    return "quarto"

# ----------------- Syllabus Generation -----------------

def generate_syllabus_ai(topic: str, hours_per_day: int, days_per_week: int, weeks_count: int, strategies: str, target_audience: str) -> Dict[str, Any]:
    """
    Generates a structured syllabus using Gemini API with Structured Outputs, tailored to the target audience.
    """
    if not api_key:
        # Return a mock syllabus if no API key is provided
        return get_mock_syllabus(topic, weeks_count, days_per_week)
        
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    model = genai.GenerativeModel(model_name)
    
    prompt = f"""
    أنت مصمم مناهج تعليمية محترف وخبير في الذكاء الاصطناعي والتعليم الحديث.
    قم بتصميم منهج تدريبي كامل باللغة العربية حول الموضوع التالي:
    - الموضوع: {topic}
    - الفئة المستهدفة: {target_audience}
    - المدة التدريبية: {hours_per_day} ساعات في اليوم، {days_per_week} أيام في الأسبوع، لإجمالي {weeks_count} أسابيع.
    - استراتيجيات التعلم المفضلة: {strategies}
    
    شروط هامة لتكييف المنهج حسب الفئة المستهدفة ({target_audience}):
    1. لغة الشرح والمفاهيم: يجب أن تتناسب لغة وعمق وتفاصيل المنهج تماماً مع الفئة المستهدفة:
       - إذا كانت الفئة (صفوف أولية أو عليا): ركز على الألعاب، الصور والتمثيل البصري، المفاهيم البسيطة بدون كود معقد أو رياضيات.
       - إذا كانت الفئة (غير تقنية): تجنب التعقيد الرياضي والبرمجي العميق وركز على الاستخدام والتطبيقات العملية والواجهات البسيطة.
       - إذا كانت الفئة (متخصصين أو خبراء ذكاء اصطناعي): استخدم لغة تقنية عالية، وتطرق للتفاصيل الرياضية والخوارزميات البرمجية المتقدمة والمشاريع العميقة.
    2. يجب أن يتناسب المنهج تماماً مع المدة الزمنية المحددة ويغطي المفاهيم بالتدرج المناسب.
    3. قم بتوزيع الدروس بالتفصيل على كل يوم تدريبي في الأسابيع المحددة.
    4. يجب عليك توظيف استراتيجيات التعلم المفضلة المحددة ({strategies}) في تصميم كل درس يومي.
    5. املأ حقل 'strategies' بقائمة الاستراتيجيات المطبقة في هذا الدرس بالتحديد، وحقل 'strategy_application' بشرح مفصل وملموس لكيفية تطبيق وتفعيل هذه الاستراتيجيات في الأنشطة التعليمية والعملية خلال هذا الدرس اليومي بما يناسب فئة الجمهور المستهدف.
    
    أرجع النتيجة بصيغة JSON متوافقة تماماً مع المخطط (Schema) المطلوب.
    """
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            response_schema=MANUAL_SYLLABUS_SCHEMA
        )
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        return get_mock_syllabus(topic, weeks_count, days_per_week)


# ----------------- Slides Generation -----------------

def generate_slides_content(lesson_title: str, lesson_desc: str, objectives: List[str], course_title: str, strategies: List[str] = None, strategy_application: str = "") -> str:
    """
    Calls Gemini to generate Quarto Reveal.js presentation slides (.qmd content).
    """
    if not api_key:
        return get_mock_qmd(lesson_title, lesson_desc, objectives)
        
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-pro")
    model = genai.GenerativeModel(model_name)
    
    strategies_text = ", ".join(strategies) if strategies else "التعلم التفاعلي"
    
    prompt = f"""
    أنت مصمم مناهج محترف ومطور عروض تقديمية تفاعلية.
    قم بكتابة محتوى شرائح عرض تقديمي (Quarto Reveal.js Markdown) لدرس بعنوان "{lesson_title}".
    وصف الدرس: {lesson_desc}
    الأهداف التعليمية: {', '.join(objectives)}
    اسم الدورة: {course_title}
    الاستراتيجيات التعليمية المطبقة: {strategies_text}
    كيفية تفعيل النشاط: {strategy_application}
    
    مواصفات كتابة ملف الـ .qmd:
    1. ترويسة YAML: لا تضف أي ترويسة YAML إطلاقاً! سأقوم أنا بإضافتها تلقائياً. ابدأ كتابة المحتوى مباشرة.
    2. لا تضف رقعة Matplotlib البرمجية، سأقوم بحقنها تلقائياً.
    3. التنسيق والشرائح:
       - ابدأ بشريحة عنوان ترحيبية للدرس باستخدام الفئة المظلمة:
         `# [عنوان الدرس] {{.sdaia-dark data-background-gradient="linear-gradient(135deg, #1C355E, #00C9A7)"}}`
       - أضف شريحة للأهداف التعليمية للدرس.
       - قسّم الدرس إلى أقسام فرعية تبدأ بشريحة عنوان مظلمة:
         `# القسم الأول: [عنوان القسم الأول] {{.sdaia-dark}}`
       - استخدم نظام الأعمدة في بعض الشرائح لتوضيح المقارنات أو الهياكل بوضوح:
         ```markdown
         :::: {{.columns}}
         ::: {{.column width="50%"}}
         [محتوى العمود الأيمن]
         :::
         ::: {{.column width="50%"}}
         [محتوى العمود الأيسر]
         :::
         ::::
         ```
    
    شروط هامة وإلزامية جداً من العميل للمحتوى والتنسيق:
    - لا يقبل أي درس يقل عن 30 شريحة (سلايد). قم بتقسيم المحتوى بتفصيل شديد وتوزيع المعلومات على شرائح عديدة ومريحة للنظر.
    - الهيكلة الرباعية الإجبارية: يجب أن تقسم الدرس برمجياً إلى 4 مراحل (تهيئة، مفاهيم، تطبيق، خلاصة). شريحة عنوان كل مرحلة يجب أن تكون مظلمة ومميزة بإضافة الكلاس الخاص بها هكذا:
      `# المرحلة الأولى: التهيئة والجذب {.sdaia-dark}`
    - تنويع القوالب: لا تكرر تصميم الشريحة، استخدم شرائح نصية، ثم شريحة أعمدة مزدوجة، ثم شريحة مسابقة، وهكذا.
    - ملاحظات المحاضر (Speaker Notes): أضف ملاحظات مساعدة للمحاضر أسفل كل شريحة باستخدام الكود التالي:
      `::: {{.notes}}`
      `[أضف نصيحة أو معلومة إضافية للمحاضر هنا]`
      `:::`
    - لا تقم بكتابة عبارات مثل (شريحة 1 من 30) في العناوين، بل استخدم عناوين حقيقية ومفيدة.
    - احذر من ترك أي شريحة فارغة. تأكد أن كل شريحة (تبدأ بـ #) تحتوي على شرح وافٍ، جدول، صورة، أو مسابقة. لا تستخدم الفواصل --- إلا إذا كان هناك محتوى فعلي.
    - التنسيق النقطي: لا تقم بجمع النقاط في جملة واحدة أبداً. يجب أن تكتب كل نقطة في سطر مستقل كقائمة نقطية (باستخدام الشارطة - ). اترك سطر فارغ قبل القوائم.
    - إبراز المصطلحات: أي مصطلح جديد أو تعريف يجب أن يكون بالخط العريض (Bold)، مثال: **الذكاء الاصطناعي**: هو كذا وكذا.
    - الإكثار من الجداول (Tables): العميل يطلب جداول! ضع جدولاً واحداً على الأقل كل 4 أو 5 شرائح لتلخيص ومقارنة المفاهيم. استخدم صيغة Markdown للجداول.
    - صور حقيقية في يسار الشاشة (Images): **يجب وضع أي صورة دائماً في يسار الشاشة** باستخدام الأعمدة كالتالي:
      :::: {{.columns}}
      ::: {{.column width="60%"}}
      [الشرح هنا]
      :::
      ::: {{.column width="40%"}}
      ![اكتب هنا وصفاً بالعربية للصورة](https://image.pollinations.ai/prompt/exact_meaningful_english_keyword?width=600&height=600&nologo=true)
      :::
      ::::
      استخدم كلمة إنجليزية واحدة فقط (One Single Word) تصف الصورة بدون أي مسافات أو رموز لضمان عمل الرابط (مثال: استبدل `exact_meaningful_english_keyword` بكلمة `data` أو `robot` أو `network`). الروابط تنكسر إذا استخدمت أكثر من كلمة واحدة! لا تضع الصور عشوائياً خارج هذا القالب!
    - قالب المسابقة الإجباري (Quiz Template): لا تقم بحرق الإجابة على الطلاب. استخدم هذا القالب الإجباري لتظهر الإجابة فقط عند النقر:
      # اختبر معلوماتك! 🧠
      [السؤال هنا]
      - أ) خيار أول
      - ب) خيار ثاني
      - ج) خيار ثالث
      
      ::: {{.fragment}}
      **الإجابة الصحيحة:** [الإجابة مع التفسير]
      :::
    - الشروحات يجب أن تكون سهلة وبسيطة جداً ومناسبة للطلاب.
    - يجب إضافة تفاصيل كافية وعميقة تغطي الأهداف التعليمية بالكامل وتضمن فهم الطلاب. استرسل في الشرح واستخدم أمثلة واقعية.
    
    لا تقم بإرجاع أي شيء سوى كود الـ Markdown بصيغة نصية واضحة.
    """
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            max_output_tokens=8192
        )
    )
    return response.text

# ----------------- Lab Notebook Generation (.ipynb) -----------------

def generate_notebook_cells(lesson_title: str, lesson_desc: str, objectives: List[str], strategies: List[str] = None, strategy_application: str = "") -> List[Dict[str, Any]]:
    """
    Calls Gemini to generate the structures and cells of a Jupyter Notebook.
    """
    if not api_key:
        return get_mock_notebook_data(lesson_title, lesson_desc, objectives)
        
    model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    model = genai.GenerativeModel(model_name)
    
    strategies_text = ", ".join(strategies) if strategies else "التعلم التفاعلي"
    
    prompt = f"""
    أنت خبير تقني ومطور بايثون محترف. قم بتصميم معمل برمجي تفاعلي (Jupyter Lab Notebook) حول درس: "{lesson_title}".
    وصف الدرس: {lesson_desc}
    الأهداف: {', '.join(objectives)}
    الاستراتيجيات التعليمية المطبقة: {strategies_text}
    تفاصيل تطبيق النشاط العملي: {strategy_application}
    
    أريدك أن تنشئ هيكل خلايا الدفتر (Notebook Cells) كقائمة JSON مهيكلة.
    يجب أن تحتوي كل خلية في القائمة على:
    - type: إما "markdown" أو "code"
    - source: النص البرمجي أو الشرح النصي باللغة العربية.
    
    شروط هامة:
    1. جميع خلايا الشرح النصي (markdown) يجب أن تبدأ وتنتهي بوسم HTML لتعديل الاتجاه: `<div dir="rtl"> [النص العربي والشرح هنا] </div>` لضمان قراءته بشكل سليم في Colab و Jupyter من اليمين لليسار.
    2. الخلايا البرمجية (code) يجب أن تحتوي على كود بايثون متكامل متعلق بالدرس مع تعليقات تفصيلية باللغة العربية.
    3. وفر خلية برمجية واحدة على الأقل تحتوي على تمرين ناقص للتعلم العملي يحمل التعليق `# TODO` ليقوم الطالب بحله وكتابة الكود الناقص، تليها خلية برمجية بالحل النموذجي الكامل.
    4. أضف قسماً للمشروع التطبيقي للدرس (Project Challenge) في النهاية.
    5. أرجع الناتج بصيغة JSON فقط كقائمة من الخلايا بالبنية المذكورة. لا تضع أي مقدمات أو علامات markdown خارج كود الـ JSON. مثال للهيكل المطلوب:
    [
      {{"type": "markdown", "source": "<div dir=\\"rtl\\\"># معمل أساسيات بايثون\\nأهلاً بكم في المعمل...</div>"}},
      {{"type": "code", "source": "# تثبيت المكتبات إذا لزم الأمر\\nprint(\\"تهيئة بيئة العمل\\")"}}
    ]
    """
    
    response = model.generate_content(
        prompt,
        generation_config=genai.GenerationConfig(
            response_mime_type="application/json",
            temperature=0.2
        )
    )
    
    try:
        return json.loads(response.text)
    except Exception as e:
        print(f"Error parsing Notebook JSON: {e}")
        return get_mock_notebook_data(lesson_title, lesson_desc, objectives)

# ----------------- Lesson Orchestrator -----------------

def sync_with_github(lesson_id: str, lesson_dir: str, ipynb_filename: str):
    """
    Copies the generated lab to the local github_sync repo and pushes it to GitHub.
    """
    github_sync_dir = os.path.join(BASE_DIR, "github_sync")
    if not os.path.exists(github_sync_dir):
        print("GitHub sync dir not found. Skipping auto-push.")
        return False
        
    try:
        # Create target directory in repo
        target_dir = os.path.join(github_sync_dir, "lessons", lesson_id)
        os.makedirs(target_dir, exist_ok=True)
        
        # Copy notebook
        src_notebook = os.path.join(lesson_dir, ipynb_filename)
        dst_notebook = os.path.join(target_dir, ipynb_filename)
        shutil.copy2(src_notebook, dst_notebook)
        
        # Git commands
        subprocess.run(["git", "pull", "origin", "main"], cwd=github_sync_dir) # Just in case
        subprocess.run(["git", "add", "."], cwd=github_sync_dir, check=True)
        
        # Check if there are changes to commit
        status = subprocess.run(["git", "status", "--porcelain"], cwd=github_sync_dir, capture_output=True, text=True)
        if status.stdout.strip():
            subprocess.run(["git", "commit", "-m", f"Auto-sync lab for {lesson_id}"], cwd=github_sync_dir, check=True)
            subprocess.run(["git", "push", "origin", "main"], cwd=github_sync_dir, check=True)
            print(f"Successfully pushed {lesson_id} to GitHub.")
        return True
    except Exception as e:
        print(f"Failed to sync with GitHub: {e}")
        return False

def build_lesson(lesson_id: str, lesson_title: str, lesson_desc: str, objectives: List[str], course_title: str, strategies: List[str] = None, strategy_application: str = "") -> Dict[str, str]:
    """
    Orchestrates the generation of slides (.qmd -> .html), notebook (.ipynb), and zips everything.
    """
    lesson_dir = os.path.join(GENERATED_DIR, lesson_id)
    os.makedirs(lesson_dir, exist_ok=True)
    
    # 1. Copy slides_template to lesson directory
    src_template = os.path.join(TEMPLATES_DIR, "slides_template")
    dst_template = os.path.join(lesson_dir, "slides_template")
    if os.path.exists(dst_template):
        shutil.rmtree(dst_template)
    shutil.copytree(src_template, dst_template)
    
    # Also copy _quarto.yml
    shutil.copy2(os.path.join(TEMPLATES_DIR, "_quarto.yml"), os.path.join(lesson_dir, "_quarto.yml"))
    
    # 2. Generate Slides Content
    slides_body = generate_slides_content(lesson_title, lesson_desc, objectives, course_title, strategies, strategy_application)
    
    # Prepend YAML Header and Matplotlib Silent Patch
    yaml_header = f"""---
title: "{lesson_title}"
subtitle: "{lesson_desc}"
lang: ar
dir: rtl
format:
  revealjs:
    theme: [default, slides_template/assets/sdaia.scss]
    logo: slides_template/assets/sdaia.svg
    transition: convex
    background-transition: fade
    title-slide-attributes:
      data-background-image: "slides_template/assets/anim.svg"
      data-background-opacity: "0.15"
    chalkboard: true
    progress: true
    center: false
    incremental: true
    code-copy: true
    code-line-numbers: true
    filters:
      - slides_template/assets/splash.lua
---
"""
    
    matplotlib_patch = """
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
    
    qmd_content = yaml_header + matplotlib_patch + "\n" + slides_body
    
    # Write lesson.qmd
    qmd_path = os.path.join(lesson_dir, "lesson.qmd")
    with open(qmd_path, "w", encoding="utf-8") as f:
        f.write(qmd_content)
        
    # 3. Render Slides via Quarto CLI
    html_url = ""
    try:
        # Check if quarto CLI is available
        quarto_bin = get_quarto_path()
        result = subprocess.run([quarto_bin, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Quarto is available. Compiling slides...")
            # Set QUARTO_PYTHON to use the virtual environment's python interpreter
            env = os.environ.copy()
            venv_python = os.path.join(BASE_DIR, ".venv", "bin", "python")
            if os.path.exists(venv_python):
                env["QUARTO_PYTHON"] = venv_python
            
            # Run quarto render lesson.qmd --to revealjs inside the lesson directory
            subprocess.run([quarto_bin, "render", "lesson.qmd", "--to", "revealjs"], cwd=lesson_dir, env=env, check=True)
            html_url = f"/lessons/{lesson_id}/docs/lesson.html"
        else:
            print("Quarto is not installed. Will skip HTML rendering, but QMD is generated.")
    except Exception as e:
        print(f"Quarto rendering failed: {e}. (Is Quarto installed?)")

        
    # 4. Generate Jupyter Notebook (.ipynb)
    notebook_cells_data = generate_notebook_cells(lesson_title, lesson_desc, objectives, strategies, strategy_application)
    
    # Build notebook using nbformat
    nb = nbf.v4.new_notebook()
    
    # Add Google Colab badge at the start
    colab_badge = f"""<div dir="rtl">

[![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/hanenalmayouf/Content-creator-dashdoard/blob/main/lessons/{lesson_id}/{lesson_id}_lab.ipynb)

# {lesson_title}
### {lesson_desc}
</div>"""
    nb['cells'].append(nbf.v4.new_markdown_cell(colab_badge))
    
    # Add generated cells
    for cell in notebook_cells_data:
        cell_type = cell.get("type", "markdown")
        source_content = cell.get("source", "")
        
        if cell_type == "markdown":
            nb['cells'].append(nbf.v4.new_markdown_cell(source_content))
        elif cell_type == "code":
            nb['cells'].append(nbf.v4.new_code_cell(source_content))
            
    # Write .ipynb file
    ipynb_filename = f"{lesson_id}_lab.ipynb"
    ipynb_path = os.path.join(lesson_dir, ipynb_filename)
    with open(ipynb_path, "w", encoding="utf-8") as f:
        nbf.write(nb, f)
        
    # 5. Create a ZIP package
    # We will zip: lesson.qmd, lesson.html (if compiled), lesson_files/ (if compiled), slides_template/, and the ipynb file.
    zip_filename = f"{lesson_id}_package"
    zip_path = os.path.join(lesson_dir, zip_filename)
    
    # We can use shutil.make_archive
    shutil.make_archive(zip_path, 'zip', lesson_dir)
    
    # 6. Auto-sync to GitHub
    sync_with_github(lesson_id, lesson_dir, ipynb_filename)
    
    return {
        "lesson_id": lesson_id,
        "qmd_file": f"/lessons/{lesson_id}/lesson.qmd",
        "html_file": html_url if html_url else "",
        "notebook_file": f"/lessons/{lesson_id}/{ipynb_filename}",
        "zip_package": f"/lessons/{lesson_id}/{zip_filename}.zip"
    }

# ----------------- Mock Data Generators -----------------

def get_mock_syllabus(topic: str, weeks: int, days: int) -> Dict[str, Any]:
    syllabus = {
        "title": f"دورة تدريبية متكاملة في {topic}",
        "description": f"منهج مكثف ومصمم لتمكين الكوادر الوطنية من مفاهيم {topic} عبر التطبيقات العملية.",
        "weeks": []
    }
    
    for w in range(1, weeks + 1):
        week = {
            "week_number": w,
            "title": f"الأسبوع {w}: التأسيس والمهام الأساسية في {topic}",
            "days": []
        }
        for d in range(1, days + 1):
            lesson_id = f"w{w}d{d}"
            week["days"].append({
                "day_number": d,
                "title": f"الدرس {d}: مقدمة عملية في {topic} - المستوى {w}",
                "description": f"شرح المبادئ الأساسية وتطبيق أول معمل برمجي للمفاهيم الخاصة بـ {topic}.",
                "objectives": [
                    f"التعرف على المكونات الأساسية لـ {topic}",
                    "تثبيت المكتبات والتحقق من بيئة العمل",
                    "كتابة وتطبيق كود برمجي بسيط لحل المشكلة"
                ],
                "strategies": ["التعلم القائم على المشاريع", "التلعيب والمسابقات"],
                "strategy_application": "يتم تطبيق المبادئ النظرية عبر كتابة برنامج عملي مصغر (مشروع صغير) في نهاية اليوم، وتليها مسابقة سريعة لاختبار الفهم البصري.",
                "lesson_id": lesson_id
            })
        syllabus["weeks"].append(week)
        
    return syllabus

def get_mock_qmd(title: str, desc: str, objectives: List[str]) -> str:
    objectives_list = "\n".join([f"- {obj}" for obj in objectives])
    return f"""# {title} {{.sdaia-dark data-background-gradient="linear-gradient(135deg, #1C355E, #00C9A7)"}}

## مقدمة وأهداف الدرس
**مرحبًا بكم في هذا الدرس التفاعلي**

{desc}

### أهداف الدرس التعليمية:
{objectives_list}

---

# القسم الأول: الأساسيات والمفاهيم {{.sdaia-dark data-background-gradient="linear-gradient(135deg, #1C355E, #00C9A7)"}}

## مقارنة المفاهيم الهامة
**تفصيل للأعمدة المزدوجة**

:::: {{.columns}}
::: {{.column width="50%"}}
### المفهوم الأول
- شرح المفهوم الأول بالتفصيل.
- كيفية استخدامه في بايثون.
:::

::: {{.column width="50%"}}
### المفهوم الثاني
- شرح المفهوم الثاني بالتفصيل.
- مميزات وعيوب كل طريقة.
:::
::::

---

## مسابقة سريعة
**اختبر معلوماتك**

أي من التالي يعد أفضل ممارسة لحفظ النصوص العربية في الرسوم البيانية؟

<div style="display: flex; justify-content: center; gap: 15px; margin: 30px 0;">
  <button class="quiz-btn" onclick="checkQ1('wrong1')">استخدام خط افتراضي</button>
  <button class="quiz-btn" onclick="checkQ1('correct')">تعديل matplotlib لإخراج SVG</button>
  <button class="quiz-btn" onclick="checkQ1('wrong2')">تحويل النصوص لصور</button>
</div>
<p id="feedback1" style="font-weight: bold; font-size: 1.1em; min-height: 40px; text-align: center; color: #00C9A7;"></p>

<script>
function checkQ1(ans) {{
  var fb = document.getElementById("feedback1");
  if(ans === 'correct') {{
    fb.style.color = "#00C9A7";
    fb.innerHTML = "✅ إجابة صحيحة! تصدير الرسوم بصيغة SVG بدون تضمين خطوط يضمن بقاء النص قابلاً للقراءة والعرض الصحيح.";
  }} else {{
    fb.style.color = "#FF6666";
    fb.innerHTML = "❌ إجابة خاطئة. الخيار الآخر غير صحيح تقنياً للغات ذات الحروف المتصلة.";
  }}
}}
</script>

<style>
  .reveal .slide {{ text-align: right; direction: rtl; }}
  .quiz-btn {{ background-color: #1C355E; color: white; border: 2px solid #1C355E; padding: 10px 20px; border-radius: 8px; cursor: pointer; transition: 0.3s; font-family: 'Helvetica Neue Arabic', sans-serif; }}
  .quiz-btn:hover {{ background-color: transparent; color: #1C355E; }}
</style>
"""


def get_mock_notebook_data(title: str, desc: str, objectives: List[str]) -> List[Dict[str, Any]]:
    return [
        {
            "type": "markdown",
            "source": f'<div dir="rtl">\n# معمل: {title}\n{desc}\n\n### أهداف المعمل:\n' + "\n".join([f"- {obj}" for obj in objectives]) + "\n</div>"
        },
        {
            "type": "markdown",
            "source": '<div dir="rtl">\n## 1. تهيئة بيئة العمل وتثبيت المكتبات\nنقوم أولاً بالتحقق من المكتبات الأساسية.\n</div>'
        },
        {
            "type": "code",
            "source": "# TODO: أكمل الكود لتثبيت matplotlib و numpy\n# !pip install matplotlib numpy\nimport numpy as np\nimport matplotlib.pyplot as plt\nprint('تم استيراد المكتبات بنجاح!')"
        },
        {
            "type": "markdown",
            "source": '<div dir="rtl">\n## 2. الحل النموذجي للتحدي البرمجي\nالكود أدناه يمثل الحل النموذجي لتهيئة المخططات وحل مشكلة النصوص العربية.\n</div>'
        },
        {
            "type": "code",
            "source": "# إعدادات Matplotlib لإخراج SVG\nimport matplotlib_inline.backend_inline\nmatplotlib_inline.backend_inline.set_matplotlib_formats('svg')\nplt.rcParams['svg.fonttype'] = 'none'\n\n# رسم مخطط بسيط\nx = np.linspace(0, 10, 100)\ny = np.sin(x)\nplt.plot(x, y)\nplt.title('Sin Wave Chart')\nplt.show()"
        },
        {
            "type": "markdown",
            "source": '<div dir="rtl">\n## 3. المشروع التطبيقي للدرس (Project Challenge)\n**المطلوب:** تطبيق المفاهيم التي تم دراستها وبناء خوارزمية كاملة لحل المشكلة.\n</div>'
        },
        {
            "type": "code",
            "source": "# اكتب الكود الخاص بك هنا لحل التحدي التطبيقي\n# def custom_solution():\n#     pass"
        }
    ]


def recompile_lesson_slides(lesson_id: str, new_content: str) -> Dict[str, str]:
    """
    Saves the new QMD content to lesson.qmd, re-renders the slides using Quarto, and updates the ZIP package.
    """
    lesson_dir = os.path.join(GENERATED_DIR, lesson_id)
    if not os.path.exists(lesson_dir):
        raise FileNotFoundError(f"Lesson directory not found for ID: {lesson_id}")
        
    qmd_path = os.path.join(lesson_dir, "lesson.qmd")
    with open(qmd_path, "w", encoding="utf-8") as f:
        f.write(new_content)
        
    html_url = ""
    try:
        # Run quarto render
        quarto_bin = get_quarto_path()
        result = subprocess.run([quarto_bin, "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print("Quarto is available. Re-compiling slides...")
            env = os.environ.copy()
            venv_python = os.path.join(BASE_DIR, ".venv", "bin", "python")
            if os.path.exists(venv_python):
                env["QUARTO_PYTHON"] = venv_python
            
            subprocess.run([quarto_bin, "render", "lesson.qmd", "--to", "revealjs"], cwd=lesson_dir, env=env, check=True)
            html_url = f"/lessons/{lesson_id}/docs/lesson.html"
    except Exception as e:
        print(f"Quarto rendering failed on recompile: {e}")
        
    # Re-zip the package
    zip_filename = f"{lesson_id}_package"
    zip_path = os.path.join(lesson_dir, zip_filename)
    
    # Remove old zip if it exists
    if os.path.exists(zip_path + ".zip"):
        os.remove(zip_path + ".zip")
        
    shutil.make_archive(zip_path, 'zip', lesson_dir)
    
    # Determine the ipynb filename
    ipynb_filename = f"{lesson_id}_lab.ipynb"
    
    return {
        "lesson_id": lesson_id,
        "qmd_file": f"/lessons/{lesson_id}/lesson.qmd",
        "html_file": html_url if html_url else "",
        "notebook_file": f"/lessons/{lesson_id}/{ipynb_filename}",
        "zip_package": f"/lessons/{lesson_id}/{zip_filename}.zip"
    }
