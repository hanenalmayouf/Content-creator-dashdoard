أريد بناء منصة ويب كاملة (Full-Stack Web Platform) لتخطيط الورش التدريبية وتوليد المناهج والدروس التعليمية التفاعلية تلقائياً باستخدام الذكاء الاصطناعي (Gemini API).

يجب أن تتطابق مخرجات المنصة (عروض Quarto Reveal.js ومعامل Jupyter Notebook) مع الهوية البصرية لـ SDAIA وحلول التعريب المعتمدة في مشروعنا السابق.

---

### 🎯 المتطلبات الوظيفية الأساسية للمنصة:

1. **مدخلات المستخدم**:
   - موضوع ورشة العمل (مثال: أساسيات بايثون).
   - المدة (عدد الساعات باليوم، عدد الأيام بالأسبوع، إجمالي عدد الأسابيع).
   - استراتيجيات التعلم المفضلة (التعلم القائم على المشاريع، التلعيب والمسابقات، إلخ).

2. **توليد المنهج (Syllabus)**:
   - يقوم الذكاء الاصطناعي بتقسيم الموضوع إلى خطة متكاملة (JSON مهيكل) يتم عرضها للمستخدم على الواجهة كخريطة طريق (Roadmap).

3. **توليد محتوى الدرس فردياً**:
   - عند النقر على درس معين، يقوم النظام بتوليد:
     - **عرض تقديمي تفاعلي (Slides)** بصيغة Quarto (`.qmd`).
     - **معمل برمجي وتدريب (Lab & Project)** بصيغة Jupyter Notebook (`.ipynb`).

---

### 📏 المواصفات التقنية الدقيقة للمخرجات (يجب برمجتها في المولد الذكي):

#### أولاً: العروض التقديمية التفاعلية (`.qmd`):
- **ترويسة الـ YAML**: يجب أن تحتوي دائماً على الإعدادات التالية لدعم العربية والسمة البصرية المخصصة:
```yaml
title: "[عنوان الدرس]"
subtitle: "[العنوان الفرعي]"
lang: ar
dir: rtl
format:
  revealjs:
    theme: [default, slides_template/assets/sdaia.scss]
    logo: slides_template/assets/sdaia.svg
    transition: slide
    background-transition: fade
    title-slide-attributes:
      data-background-image: "slides_template/assets/anim.svg"
      data-background-opacity: "0.15"
    chalkboard: true
    progress: true
    center: false
    incremental: false
    code-copy: true
    code-line-numbers: true
    filters:
      - slides_template/assets/splash.lua
```

- **رقعة الرسوم البيانية الصامتة (Matplotlib Patch)**: يجب حقن هذا الكود البرمجي بعد ترويسة YAML مباشرة في كل ملف `.qmd` لضمان إخراج رسوم بيانية بصيغة SVG وحفظ النصوص العربية بشكل سليم دون تلف:
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
```
```

- **تنسيق الشرائح**:
  - شريحة العنوان والفاصل: `# العنوان {.sdaia-dark data-background-gradient="linear-gradient(135deg, #1C355E, #00C9A7)"}`
  - تقسيم المحتوى لعمودين: استخدام نظام الأعمدة (`:::: {.columns}` و `::: {.column width="50%"}`).
  - أسئلة تفاعلية (Interactive Quiz): كتابة أزرار HTML تفاعلية مع كود JavaScript مدمج لعرض الإجابات والتقييم الفوري كما يلي:
```html
## مسابقة سريعة
**اختبر معلوماتك**
[السؤال هنا]

<div style="display: flex; justify-content: center; gap: 15px; margin: 30px 0;">
  <button class="quiz-btn" onclick="checkQ(true)">الإجابة الصحيحة</button>
  <button class="quiz-btn" onclick="checkQ(false)">الإجابة الخاطئة</button>
</div>
<p id="feedback" style="font-weight: bold; font-size: 1.1em; min-height: 40px; text-align: center; color: #00C9A7;"></p>

<script>
function checkQ(isCorrect) {
  var fb = document.getElementById("feedback");
  if(isCorrect) {
    fb.style.color = "#00C9A7";
    fb.innerHTML = "✅ إجابة صحيحة! [التوضيح العلمي]";
  } else {
    fb.style.color = "#FF6666";
    fb.innerHTML = "❌ إجابة خاطئة. [التصحيح]";
  }
}
</script>
```

#### ثانياً: المعامل البرمجية (`.ipynb`):
- **تغليف النصوص**: عند توليد ملف Jupyter Notebook، يجب تغليف محتوى كل خلية نصية (Markdown Cell) بوسم `<div dir="rtl">...</div>` لضمان قراءة اللغة العربية من اليمين لليسار في بيئات Jupyter و Google Colab.
- **تثبيت المكتبات والتحقق**: توفير خلايا برمجية في البداية لتثبيت المكتبات اللازمة تلقائياً وشارة الفتح السريع في كولاب.
- **التمارين والتحديات**: تحتوي الخلايا البرمجية على تعليقات عربية، وتدريبات ناقصة تحمل وسم `# TODO` ليقوم الطالب بحلها، تليها خلايا الحل النموذجي والمشروع التطبيقي.

---

### 🛠️ خطة العمل المطلوبة للبناء:

1. **الخلفية البرمجية (Backend - FastAPI)**:
   - استقبال طلبات التوليد، تقسيم المنهج عبر استدعاء Gemini API (باستخدام Structured Outputs للحصول على JSON).
   - عند توليد درس محدد: إنشاء مجلد مؤقت، نسخ مجلد السمات الافتراضي `slides_template` بجوار الملف، كتابة الـ `.qmd` المحقن بالرقعة، تجميع العرض التقديمي برمجياً باستخدام `quarto render` للمجلد العام، وبناء ملف `.ipynb` باستخدام مكتبة `nbformat`.
   - توفير ميزة تنزيل الملفات أو الحزمة كاملة كملف مضغوط ZIP.

2. **الواجهة الأمامية (Frontend - React)**:
   - تصميم واجهة متكاملة عصرية بلغة عربية (RTL)، تعتمد على الوضع الداكن (Dark Mode) بجماليات زجاجية (Glassmorphism).
   - عرض خريطة الطريق (Roadmap) وإتاحة توليد الدروس الفردية بشكل مستقل لتسريع تجربة الاستخدام.
   - تضمين مستعرض شرائح تفاعلي عبر `iframe` مدمج بشكل أنيق وملء الشاشة لمراجعة الدروس داخل المنصة.

3. **الأصول وملفات التنسيق**:
   - استخدم مجلد القوالب الجاهز `slides_template` المتاح في مشروعنا (والذي يحتوي على ملفات التنسيق والشعارات `sdaia.scss` و `sdaia.svg` و `anim.svg` وفلتر `splash.lua`).
