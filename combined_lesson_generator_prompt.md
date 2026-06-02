# 🚀 البرومبت الشامل والمنهجي لبناء منصة توليد الدروس التفاعلية الذكية
# Unified System Prompt & Technical Blueprint for Interactive Lesson Generation Platform

مرحباً بك! هذا الملف يدمج **المتطلبات الوظيفية للمنصة** مع **المواصفات التقنية الدقيقة وقوالب التنسيق وحلول التعريب** المستوحاة من مشروع `cv-for-developers-ultralytics`. 
يمكنك تقديم هذا الملف بالكامل كـ (Prompt/Context) للمساعد الذكي في بيئة عمل جديدة ليقوم ببناء المنصة من الصفر بشكل احترافي ومتناسق.

---

# 📝 نص البرومبت الشامل للمطور الذكي (System Prompt)

أريد بناء منصة ويب كاملة (Full-Stack Web Platform) لتخطيط الورش التدريبية وتوليد المناهج والدروس التعليمية التفاعلية تلقائياً باستخدام الذكاء الاصطناعي (Gemini API)، بحيث تتطابق مخرجاتها من عروض تقديمية تفاعلية (Quarto Reveal.js) ومعامل برمجية (Jupyter Notebooks) مع الهوية البصرية ومواصفات التنسيق وحلول التعريب المعتمدة في مشروع `cv-for-developers-ultralytics`.

---

## 🎯 الجزء الأول: وظيفة المنصة وفكرتها الأساسية

يقوم المستخدم بالدخول إلى المنصة وتحديد تفاصيل ورشة العمل:
1. **موضوع ورشة العمل** (مثال: الرؤية الحاسوبية للمطورين، أو أساسيات لغة بايثون).
2. **الخطة الزمنية لورشة العمل**:
   - عدد الساعات التدريبية في اليوم (مثال: 4 ساعات).
   - عدد أيام التدريب في الأسبوع (مثال: 3 أيام).
   - إجمالي مدة الورشة بالأيام أو الأسابيع.
3. **استراتيجيات التعلم المطلوبة** (مثل: التعلم القائم على المشاريع، التلعيب والمسابقات، الاستقصاء العلمي، التعلم البصري، إلخ).

بناءً على هذه المدخلات، تقوم المنصة بالخطوات التالية تلقائياً:
* **المرحلة الأولى: تقسيم وتوزيع المنهج (Syllabus Roadmap)**:
  - توليد خطة دراسية متكاملة مقسمة إلى وحدات ودروس تناسب الساعات والأيام المحددة وإعادة الناتج كجدول زمني مهيكل (JSON).
  - عرض الخطة كخريطة طريق (Roadmap) تفاعلية للمستخدم على الواجهة مع أزرار لتوليد كل درس على حدة.
* **المرحلة الثانية: توليد محتوى كل درس (Content Generation)**:
  - لكل درس، يتم توليد:
    1. **عرض تقديمي تفاعلي (Slides)** بصيغة Quarto Markdown (`.qmd`) باللغة العربية (RTL) متوافق مع نظام Reveal.js، ويحتوي على مسابقات برمجية تفاعلية.
    2. **معمل برمجي عملي (Lab)** بصيغة Jupyter Notebook (`.ipynb`) يحتوي على شرح نظري مبسط، خلايا برمجية جاهزة للتشغيل، وتمارين عملية يكملها الطالب مع حلولها.
    3. **مشروع تطبيقي للدرس (Project)** مدمج في نهاية المعمل لترسيخ المفاهيم.

---

## 🛠️ الجزء الثاني: التقنيات المقترحة للهيكل (Tech Stack)

1. **واجهة المستخدم (Frontend)**:
   - إطار العمل: React (باستخدام Vite).
   - التصميم: Vanilla CSS مخصص بتصميم زجاجي (Glassmorphism) يدعم الوضعين المظلم والمضيء (Dark/Light)، ودعم كامل للغة العربية (RTL)، وميكرو-أنيميشن سلس.
   - الميزات: لوحة تحكم تفاعلية، مستعرض العروض التقديمية في `iframe` ملء الشاشة، وأزرار تنزيل للملفات الفردية أو كحزمة مضغوطة ZIP.
2. **الخلفية البرمجية (Backend)**:
   - إطار العمل: Python (FastAPI).
   - محرك التوليد: Gemini API (حزمة `google-generativeai`) مع استخدام ميزة Structured Outputs لضمان توليد الخطة كـ JSON.
   - محركات التجميع: مكتبة `nbformat` لبناء ملفات `.ipynb` برمجياً، و Quarto CLI لتجميع العروض التقديمية وتوليد الـ HTML.

---

## 📐 الجزء الثالث: المواصفات التقنية الدقيقة للمخرجات (The Technical Blueprint)

يجب تزويد الخلفية البرمجية والمولّد بالبيانات والقوالب التالية لضمان تطابق المخرجات:

### 1. إعدادات Quarto المعتمدة (`_quarto.yml`)
يجب على الخلفية نسخ هذا الملف وحفظه بجانب ملفات الـ `.qmd` قبل بدء التجميع:
```yaml
quarto-required: ">= 1.4"
project:
  output-dir: docs
  execute-dir: project
  render:
    - "**/*.qmd"
    - "!slides/slides_template/*.qmd"
execute:
  echo: false
  warning: false
  message: false
format:
  revealjs:
    slide-number: c/t
    show-slide-number: all
    embed-resources: false
    preview-links: false
    theme: [default, slides_template/assets/sdaia.scss]  # السمة المخصصة
    logo: slides_template/assets/sdaia.svg
    transition: slide
    background-transition: fade
    title-slide-attributes:
      data-background-image: "slides_template/assets/anim.svg"
      data-background-opacity: "0.15"
      data-background-size: "cover"
    chalkboard: 
      buttons: true
    progress: true
    history: true
    hide-inactive-cursor: true
    strip-comments: true
    center: false
    incremental: false
    code-copy: true
    code-line-numbers: true
    filters:
      - slides_template/assets/splash.lua
```

### 2. فلتر Lua المخصص (`splash.lua`)
يُنسخ في المجلد `slides_template/assets/`:
```lua
function Header(h)
  if h.classes:includes("splash") then
    h.attributes["background-image"] = "{{< brand logo anim >}}"
    h.attributes["background-opacity"] = "0.1"
  end
  return h
end
```

### 3. سمات التنسيق المخصص (`sdaia.scss`)
يتم نسخه في مجلد الأصول `assets/` ويحتوي على الهوية البصرية لـ SDAIA:
* **الألوان**:Navy `#1C355E` (للعناوين)، Orange `#E96852` (لإبراز الكلمات الهامة)، Teal `#00AE8D` (للملاحظات والروابط)، Purple `#625D9C` (للتنبيهات).
* **الخطوط**: `"DiodrumArabic"` أو `"Noto Sans Arabic"` للعناوين، و `"Helvetica Neue Arabic"` للمتن.
* **إعدادات RTL**: ضبط `direction: rtl; text-align: right;` لجميع العناصر والنصوص عدا كود البرمجة.
* **فئات التصميم**:
  * `.sdaia-dark`: توليد شريحة بـ Gradient خلفية أزرق داكن إلى تركواز.
  * `.qbox`: صندوق لتغليف التمارين والأسئلة.
  * `.bilingual`: شريحة مقسمة لعمودين (عربي وإنجليزي للمقارنات).

### 4. رقعة الرسوم البيانية الصامتة (Matplotlib Silent Patch)
لمنع تلف وتداخل الحروف العربية في الرسوم البيانية التي يولدها بايثون داخل الشرائح، يجب على المولد حقن الكود التالي في ملف الـ `.qmd` فوراً بعد ترويسة YAML:
```python
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
```

### 5. هيكل الشرائح التفاعلية وسيناريو المسابقات
* شريحة العنوان والفاصل تأخذ الفئة المظلمة:
  `# اسم الوحدة {.sdaia-dark data-background-gradient="linear-gradient(135deg, #1C355E, #00C9A7)"}`
* الشرح يستخدم نظام الأعمدة لسهولة الفهم البصري (`:::: {.columns}`).
* المسابقة التفاعلية تحتوي على أزرار HTML مدمجة مع JavaScript للتحقق وعرض الإجابة التوضيحية فوراً:
  ```html
  ## مسابقة سريعة
  
  **اختبر معلوماتك**
  
  السؤال هنا؟
  
  <div style="display: flex; justify-content: center; gap: 15px; margin: 30px 0;">
    <button class="quiz-btn" onclick="checkQ1('wrong')">إجابة 1</button>
    <button class="quiz-btn" onclick="checkQ1('correct')">إجابة 2</button>
  </div>
  
  <p id="feedback1" style="font-weight: bold; font-size: 1.1em; min-height: 40px; text-align: center; color: #00C9A7;"></p>
  
  <script>
  function checkQ1(ans) {
    var fb = document.getElementById("feedback1");
    if(ans === 'correct') {
      fb.style.color = "#00C9A7";
      fb.innerHTML = "✅ إجابة صحيحة! التفسير العلمي هنا.";
    } else {
      fb.style.color = "#FF6666";
      fb.innerHTML = "❌ إجابة خاطئة. التوجيه التعليمي هنا.";
    }
  }
  </script>
  ```
* تذييل الشرائح يغلف بتنسيقات CSS مخصصة:
  ```html
  <style>
    .reveal .slide { text-align: right; direction: rtl; }
    .quiz-btn { background-color: var(--r-main-color); color: var(--r-background-color); border: 2px solid var(--r-main-color); padding: 10px 20px; border-radius: 8px; cursor: pointer; transition: 0.3s; }
    .quiz-btn:hover { background-color: transparent; color: var(--r-main-color); }
  </style>
  ```

### 6. هيكل المعمل البرمجي (`.ipynb`)
عند بناء ملف Jupyter Notebook برمجياً باستخدام بايثون، يجب اتباع القواعد التالية:
* **خلايا الـ Markdown**: يجب تغليف محتوى كل خلية نصية بـ `<div dir="rtl">` لضمان محاذاة النص العربي بشكل صحيح في بيئات Jupyter و Google Colab.
* **خلية البداية**: تحتوي على شارة الفتح السريع في كولاب:
  ```markdown
  [![Open In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/...)
  ```
* **خلايا الأكواد (Code Cells)**: تحتوي على الكود مع تعليقات تفصيلية باللغة العربية، وتدريبات ناقصة تحمل وسم `# TODO` ليقوم الطالب بحلها، تليها خلايا الحل النموذجي.

---

## 🗺️ الجزء الرابع: خطوات البناء المفصلة (Roadmap)

### الخطوة 1: تهيئة بيئة العمل والملفات الثابتة
* إعداد مجلد المشروع وهيكله كما هو موضح بالأسفل.
* وضع ملفات القوالب الثابتة لشرائح العرض (`sdaia.scss`, `sdaia.svg`, `anim.svg`, `favicon.html`, `splash.lua`) في مجلد الموارد الثابتة بالخلفية لنسخها تلقائياً عند توليد كل درس.
* تهيئة المتغيرات البيئية لاستلام مفتاح Gemini API.

### الخطوة 2: لوحة التحكم والواجهة الأمامية
* بناء واجهة متطابقة بجماليات عصرية (Glassmorphism، ألوان متباينة، ميكرو-أنيميشن).
* دعم كامل للغة العربية (RTL).
* نموذج إدخال المعايير (موضوع الورشة، ساعات التدريب، عدد الأيام، استراتيجيات التعلم).
* **عرض المنهج المقترح (Syllabus Roadmap View)**: جدول تفاعلي يعرض أسابيع وأيام التدريب ومحتويات كل درس، مع زر "توليد محتوى الدرس" بجانب كل درس.
* واجهة المكتبة (Library): بطاقات الدروس المنجزة بنجاح مع خيارات: (عرض الشرائح في iframe، تنزيل المعمل، فتح بكولاب، وتنزيل حزمة ZIP كاملة).

### الخطوة 3: هندسة البرومبت للتوليد الذكي (Prompt Engineering)
1. **برومبت توليد المنهج (Curriculum Prompt)**: يطلب من Gemini تقسيم الموضوع العام إلى خطة مفصلة بصيغة JSON مهيكلة تحتوي على: الأسابيع، الأيام، عنوان الدرس، الوصف، والأهداف التدريبية.
2. **برومبت توليد الشرائح (`.qmd`)**: يوجه النموذج لكتابة ملف Quarto متوافق تماماً مع مواصفات *الجزء الثالث* (يدعم RTL، مسابقة تفاعلية، تقسيم أعمدة، رقعة Matplotlib). **شروط إلزامية جديدة**: يجب ألا يقل الدرس عن 30 شريحة، ويجب أن يحتوي على جداول، وصور توضيحية (أو روابط وهمية معبرة)، مع تقديم شروحات سهلة ومبسطة وتفصيلية تناسب الطلاب.
3. **برومبت توليد المعمل والمشروع (`.ipynb`)**: يوجه النموذج لتوليد خلايا Markdown مغلفة بـ `<div dir="rtl">` وخلايا Code تحتوي على تدريبات `# TODO` ومشاريع تطبيقية نموذجية.

### الخطوة 4: الخلفية ومعالج توليد المخرجات (Backend Generation Manager)
* استقبال الطلبات ومعالجة المدخلات.
* استدعاء Gemini API وتمرير النصوص.
* عند طلب توليد درس محدد:
  1. إنشاء مجلد مؤقت للدرس.
  2. نسخ مجلد القوالب الافتراضية `slides_template` بجواره مباشرة.
  3. كتابة ملف الـ `.qmd` المحقون برقعة Matplotlib.
  4. تشغيل أمر النظام برمجياً:
     `quarto render lesson.qmd --to revealjs`
  5. استخدام مكتبة `nbformat` في بايثون لتركيب خلايا المعمل والمشروع البرمجي وحفظها كملف `.ipynb`.
  6. نقل الـ HTML النهائي وكافة الملحقات ومستندات المعمل إلى المجلد العام للمنصة ليسهل الوصول إليها.
  7. ضغط المخرجات وإتاحتها للتنزيل كحزمة ZIP.

---

## 📁 هيكل المجلدات المقترح للمشروع الجديد

```text
interactive-course-generator/
├── backend/
│   ├── app.py                 # نقطة الدخول الرئيسية لـ FastAPI
│   ├── requirements.txt       # المكتبات البرمجية المطلوبة (FastAPI, nbformat, Jinja2, etc.)
│   ├── generator.py           # مدير التوليد الذكي وهندسة البرومبتات لـ Gemini
│   ├── templates/             
│   │   └── slides_template/   # مجلد القوالب الثابتة المنسوخ من المشروع القديم
│   │       ├── _metadata.yml
│   │       ├── template.qmd
│   │       └── assets/
│   │           ├── sdaia.scss
│   │           ├── sdaia.svg
│   │           ├── anim.svg
│   │           ├── favicon.html
│   │           └── splash.lua
│   └── generated_lessons/     # مخرجات التوليد الذكي (HTML, ipynb, zip)
├── frontend/
│   ├── index.html
│   ├── src/
│   │   ├── main.jsx
│   │   ├── App.jsx            # لوحة التحكم والمستعرض التفاعلي
│   │   └── components/        # بطاقات الدروس وخارطة الطريق
│   └── package.json
└── README.md
```

ابتدئ بالخطوة الأولى مباشرة وابنِ لنا منصة رائعة متناسقة!
