import { useState, useEffect } from 'react';
import sdaiaLogo from './assets/sdaia.svg';
import sdaiaIcon from './assets/icon.svg';
import {
  BookOpen,

  Calendar,
  Clock,
  Settings,
  Sparkles,
  Download,
  ExternalLink,
  Play,
  Maximize2,
  ChevronDown,
  ChevronUp,
  RefreshCw,
  AlertCircle,
  FolderArchive,
  FlaskConical,
  BookOpenCheck,
  CheckCircle2,
  X,
  Plus
} from 'lucide-react';
import './App.css';

const API_BASE_URL = 'http://localhost:8000';

const DEFAULT_STRATEGIES = [
  { id: 'adaptive', label: 'التعلم المخصّص والتكيّفي (Personalized & Adaptive)' },
  { id: 'gamification', label: 'التعلم التفاعلي والتلعيب والألعاب التعليمية (Gamified)' },
  { id: 'collaborative', label: 'التعلم التشاركي والتعاوني وحل المشكلات (Collaborative)' },
  { id: 'affective', label: 'النمذجة العاطفية والاجتماعية لتعديل التدريس (Affective)' },
  { id: 'formative', label: 'التقييم التكويني المستمر والتحليلات التعليمية (Formative)' },
  { id: 'critical', label: 'تطوير التفكير النقدي والمهارات العليا (Critical Thinking)' }
];

const TARGET_AUDIENCES = [
  { id: 'specialists', label: 'المتخصصون (علوم حاسب أو ذكاء اصطناعي)' },
  { id: 'early_school', label: 'طلاب المدارس - الصفوف الأولية (أول، ثاني، ثالث ابتدائي)' },
  { id: 'upper_school', label: 'طلاب المدارس - الصفوف العليا (رابع، خامس، سادس ابتدائي)' },
  { id: 'middle_school', label: 'طلاب المدارس - المرحلة المتوسطة' },
  { id: 'high_school', label: 'طلاب المدارس - المرحلة الثانوية' },
  { id: 'non_tech_uni', label: 'طلاب الجامعة غير التقنيين' },
  { id: 'ai_experts', label: 'خبراء الذكاء الاصطناعي (ذوي خبرة كبيرة)' }
];

function App() {
  // 1. Saved Courses history state
  const [savedCourses, setSavedCourses] = useState(() => {
    try {
      const parsed = JSON.parse(localStorage.getItem('saved_courses'));
      return Array.isArray(parsed) ? parsed : [];
    } catch {
      return [];
    }
  });

  // 2. Active Course ID state
  const [activeCourseId, setActiveCourseId] = useState(() => {
    return localStorage.getItem('active_course_id') || null;
  });

  // Helper function to read from active course if loaded
  const getInitialValue = (key, defaultValue) => {
    try {
      const parsed = JSON.parse(localStorage.getItem('saved_courses'));
      const courses = Array.isArray(parsed) ? parsed : [];
      const activeId = localStorage.getItem('active_course_id');
      const activeCourse = courses.find(c => c && c.id === activeId);
      if (activeCourse && activeCourse[key] !== undefined && activeCourse[key] !== null) {
        // Additional type safety to prevent crashes from legacy local storage values
        if (key === 'selectedStrategies' && !Array.isArray(activeCourse[key])) {
          return defaultValue;
        }
        if (key === 'lessonResults' && (typeof activeCourse[key] !== 'object' || Array.isArray(activeCourse[key]))) {
          return defaultValue;
        }
        return activeCourse[key];
      }
    } catch (e) {
      console.error(e);
    }
    return defaultValue;
  };

  // Input parameters
  const [topic, setTopic] = useState(() => getInitialValue('topic', ''));
  const [hoursPerDay, setHoursPerDay] = useState(() => getInitialValue('hoursPerDay', 4));
  const [daysPerWeek, setDaysPerWeek] = useState(() => getInitialValue('daysPerWeek', 3));
  const [weeksCount, setWeeksCount] = useState(() => getInitialValue('weeksCount', 2));
  const [selectedStrategies, setSelectedStrategies] = useState(() => getInitialValue('selectedStrategies', ['adaptive', 'gamification', 'formative']));
  const [customStrategy, setCustomStrategy] = useState(() => getInitialValue('customStrategy', ''));
  const [targetAudience, setTargetAudience] = useState(() => getInitialValue('targetAudience', 'specialists'));

  // App states
  const [loading, setLoading] = useState(false);
  const [syllabus, setSyllabus] = useState(() => getInitialValue('syllabus', null));
  const [error, setError] = useState(null);
  const [expandedWeeks, setExpandedWeeks] = useState({ 1: true });

  // Lesson generation states
  const [generatingLessons, setGeneratingLessons] = useState({});
  const [lessonResults, setLessonResults] = useState(() => getInitialValue('lessonResults', {}));
  const [activePreview, setActivePreview] = useState(null); // { url, title }

  // Auto-save useEffect hook
  useEffect(() => {
    if (!syllabus) return;

    const currentId = activeCourseId || 'course_' + Date.now();
    if (!activeCourseId) {
      setActiveCourseId(currentId);
      localStorage.setItem('active_course_id', currentId);
    }

    const courseData = {
      id: currentId,
      title: syllabus.title || topic || 'منهج دراسي جديد',
      topic,
      targetAudience,
      hoursPerDay,
      daysPerWeek,
      weeksCount,
      selectedStrategies,
      customStrategy,
      syllabus,
      lessonResults,
      updatedAt: new Date().toISOString()
    };

    setSavedCourses(prev => {
      const arrayPrev = Array.isArray(prev) ? prev : [];
      const filtered = arrayPrev.filter(c => c && c.id !== currentId);
      const updated = [courseData, ...filtered];
      localStorage.setItem('saved_courses', JSON.stringify(updated));
      return updated;
    });
  }, [syllabus, lessonResults, topic, targetAudience, hoursPerDay, daysPerWeek, weeksCount, selectedStrategies, customStrategy, activeCourseId]);

  // Navigation & history handlers
  const handleLoadCourse = (course) => {
    setActiveCourseId(course.id);
    localStorage.setItem('active_course_id', course.id);

    setTopic(course.topic || '');
    setHoursPerDay(course.hoursPerDay || 4);
    setDaysPerWeek(course.daysPerWeek || 3);
    setWeeksCount(course.weeksCount || 2);
    setSelectedStrategies(course.selectedStrategies || ['adaptive', 'gamification', 'formative']);
    setCustomStrategy(course.customStrategy || '');
    setTargetAudience(course.targetAudience || 'specialists');
    setSyllabus(course.syllabus || null);
    setLessonResults(course.lessonResults || {});
    setError(null);
  };

  const handleNewCourse = () => {
    setActiveCourseId(null);
    localStorage.removeItem('active_course_id');

    setTopic('');
    setHoursPerDay(4);
    setDaysPerWeek(3);
    setWeeksCount(2);
    setSelectedStrategies(['adaptive', 'gamification', 'formative']);
    setCustomStrategy('');
    setTargetAudience('specialists');
    setSyllabus(null);
    setLessonResults({});
    setError(null);
  };

  const handleDeleteCourse = (courseId) => {
    setSavedCourses(prev => {
      const arrayPrev = Array.isArray(prev) ? prev : [];
      const updated = arrayPrev.filter(c => c && c.id !== courseId);
      localStorage.setItem('saved_courses', JSON.stringify(updated));
      return updated;
    });
    
    if (activeCourseId === courseId) {
      handleNewCourse();
    }
  };

  // Pre-generation editing states
  const [editingDayId, setEditingDayId] = useState(null);
  const [editForm, setEditForm] = useState({ title: '', description: '', objectives: '', strategies: '', strategy_application: '' });

  // Post-generation code editor states
  const [editingCodeDay, setEditingCodeDay] = useState(null); // { lesson_id, title }
  const [qmdContent, setQmdContent] = useState('');
  const [loadingCode, setLoadingCode] = useState(false);
  const [recompiling, setRecompiling] = useState(false);

  // Helper functions for inline editing
  const startEditing = (day) => {
    setEditingDayId(day.lesson_id);
    setEditForm({
      title: day.title || '',
      description: day.description || '',
      objectives: day.objectives ? day.objectives.join('\n') : '',
      strategies: day.strategies ? day.strategies.join('\n') : '',
      strategy_application: day.strategy_application || ''
    });
  };

  const saveEditing = (weekNumber, lessonId) => {
    setSyllabus(prevSyllabus => {
      if (!prevSyllabus || !Array.isArray(prevSyllabus.weeks)) return prevSyllabus;

      const updatedWeeks = prevSyllabus.weeks.map(week => {
        if (week.week_number !== weekNumber) return week;
        if (!Array.isArray(week.days)) return week;

        const updatedDays = week.days.map(day => {
          if (day.lesson_id !== lessonId) return day;

          return {
            ...day,
            title: editForm.title,
            description: editForm.description,
            objectives: editForm.objectives.split('\n').map(o => o.trim()).filter(Boolean),
            strategies: editForm.strategies.split('\n').map(s => s.trim()).filter(Boolean),
            strategy_application: editForm.strategy_application
          };
        });

        return { ...week, days: updatedDays };
      });

      return { ...prevSyllabus, weeks: updatedWeeks };
    });
    setEditingDayId(null);
  };

  const handleOpenCodeEditor = async (day) => {
    setEditingCodeDay(day);
    setLoadingCode(true);
    setQmdContent('');
    try {
      const response = await fetch(`${API_BASE_URL}/api/load-lesson-file?lesson_id=${day.lesson_id}&file_type=qmd`);
      if (!response.ok) {
        throw new Error('فشل تحميل كود الشرائح من السيرفر.');
      }
      const data = await response.json();
      setQmdContent(data.content);
    } catch (err) {
      alert(err.message);
      setEditingCodeDay(null);
    } finally {
      setLoadingCode(false);
    }
  };

  const handleSaveCode = async () => {
    if (!editingCodeDay) return;
    setRecompiling(true);
    try {
      const response = await fetch(`${API_BASE_URL}/api/save-lesson-file`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lesson_id: editingCodeDay.lesson_id,
          file_type: 'qmd',
          content: qmdContent
        })
      });
      if (!response.ok) {
        throw new Error('فشل حفظ كود الشرائح أو إعادة تجميع العرض.');
      }
      const data = await response.json();
      setLessonResults(prev => ({ ...prev, [editingCodeDay.lesson_id]: data }));
      setEditingCodeDay(null);
      alert('تم تحديث الدرس وإعادة تجميع الشرائح وحزمة ZIP بنجاح! 🎉');
    } catch (err) {
      alert(err.message);
    } finally {
      setRecompiling(false);
    }
  };

  // Handlers
  const handleGenerateSyllabus = async (e) => {
    e.preventDefault();
    if (!topic.trim()) return;

    setLoading(true);
    setError(null);
    setSyllabus(null);
    setLessonResults({});

    // Combine checked strategies and custom strategies
    const activeStrategies = DEFAULT_STRATEGIES
      .filter(s => selectedStrategies.includes(s.id))
      .map(s => s.label);

    if (customStrategy.trim()) {
      activeStrategies.push(customStrategy.trim());
    }

    const strategiesString = activeStrategies.join('، ') || 'عام وتطبيقي';
    const audienceLabel = TARGET_AUDIENCES.find(a => a.id === targetAudience)?.label || targetAudience;

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-syllabus`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          topic,
          hours_per_day: hoursPerDay,
          days_per_week: daysPerWeek,
          weeks_count: weeksCount,
          strategies: strategiesString,
          target_audience: audienceLabel
        })
      });

      if (!response.ok) {
        throw new Error('فشل توليد المنهج الدراسي. يرجى التحقق من اتصال الخادم ومفتاح Gemini.');
      }

      const data = await response.json();
      setSyllabus(data);
      // Auto expand week 1
      setExpandedWeeks({ 1: true });
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  const handleGenerateLesson = async (day, courseTitle) => {
    const lessonId = day.lesson_id;

    setGeneratingLessons(prev => ({ ...prev, [lessonId]: true }));
    setError(null);

    try {
      const response = await fetch(`${API_BASE_URL}/api/generate-lesson`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          lesson_id: lessonId,
          lesson_title: day.title,
          lesson_desc: day.description,
          objectives: day.objectives,
          course_title: courseTitle,
          strategies: day.strategies || [],
          strategy_application: day.strategy_application || ""
        })
      });

      if (!response.ok) {
        throw new Error(`فشل توليد الدرس: ${day.title}`);
      }

      const data = await response.json();
      setLessonResults(prev => ({ ...prev, [lessonId]: data }));
    } catch (err) {
      setError(err.message);
    } finally {
      setGeneratingLessons(prev => ({ ...prev, [lessonId]: false }));
    }
  };

  const toggleWeek = (weekNum) => {
    setExpandedWeeks(prev => ({ ...prev, [weekNum]: !prev[weekNum] }));
  };

  const handleOpenPreview = (result, title) => {
    if (!result.html_file) {
      alert("لم يتم العثور على ملف HTML للشرائح. تأكد من توفر Quarto CLI في خادم الخلفية لتجميع ملفات .qmd");
      return;
    }

    // Fix path if it is missing the docs/ directory (legacy localStorage support)
    let htmlFile = result.html_file;
    if (htmlFile.startsWith('/lessons/') && !htmlFile.includes('/docs/')) {
      const parts = htmlFile.split('/');
      if (parts.length === 4) {
        htmlFile = `/lessons/${parts[2]}/docs/${parts[3]}`;
      }
    }

    setActivePreview({
      url: `${API_BASE_URL}${htmlFile}`,
      title: title
    });
  };

  const handleFullScreen = () => {
    const iframe = document.getElementById('slides-iframe');
    if (iframe) {
      if (iframe.requestFullscreen) {
        iframe.requestFullscreen();
      } else if (iframe.webkitRequestFullscreen) { /* Safari */
        iframe.webkitRequestFullscreen();
      } else if (iframe.msRequestFullscreen) { /* IE11 */
        iframe.msRequestFullscreen();
      }
    }
  };

  return (
    <div className="app-container">
      {/* Top Header */}
      <header className="header glass-container animate-fade-in">
        <div className="header-info">
          <h1>منصة توليد المناهج والدروس التفاعلية </h1>

        </div>
        <div className="logo-section">
          <img src={sdaiaLogo} className="sdaia-logo-img" alt="SDAIA Logo" />
        </div>
      </header>



      {/* Main Grid */}
      <main className="main-content">
        {/* Right side: Parameters Form */}
        <section className="form-panel glass-container animate-fade-in">
          <h2 className="panel-title">
            <Settings className="panel-icon text-teal" />
            معايير الورشة التدريبية
          </h2>

          <form onSubmit={handleGenerateSyllabus} className="params-form">
            <div className="form-group">
              <label htmlFor="topic">موضوع ورشة العمل</label>
              <textarea
                id="topic"
                rows="3"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                placeholder="أدخل موضوع الورشة، مثال: أساسيات الرؤية الحاسوبية ومعالجة الصور"
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="target-audience">الفئة المستهدفة للورشة</label>
              <select
                id="target-audience"
                value={targetAudience}
                onChange={(e) => setTargetAudience(e.target.value)}
              >
                {TARGET_AUDIENCES.map((audience) => (
                  <option key={audience.id} value={audience.id}>
                    {audience.label}
                  </option>
                ))}
              </select>
            </div>

            <div className="form-row">
              <div className="form-group col">
                <label htmlFor="weeks">عدد الأسابيع</label>
                <input
                  type="number"
                  id="weeks"
                  min="1"
                  max="12"
                  value={weeksCount}
                  onChange={(e) => setWeeksCount(parseInt(e.target.value))}
                />
              </div>
              <div className="form-group col">
                <label htmlFor="days">أيام التدريب/أسبوع</label>
                <input
                  type="number"
                  id="days"
                  min="1"
                  max="7"
                  value={daysPerWeek}
                  onChange={(e) => setDaysPerWeek(parseInt(e.target.value))}
                />
              </div>
              <div className="form-group col">
                <label htmlFor="hours">ساعات التدريب/يوم</label>
                <input
                  type="number"
                  id="hours"
                  min="1"
                  max="12"
                  value={hoursPerDay}
                  onChange={(e) => setHoursPerDay(parseInt(e.target.value))}
                />
              </div>
            </div>

            <div className="form-group">
              <label>استراتيجيات التعلم المفضلة (اختياري)</label>
              <div className="checkbox-group">
                {DEFAULT_STRATEGIES.map(strategy => (
                  <label key={strategy.id} className="checkbox-label">
                    <input
                      type="checkbox"
                      checked={selectedStrategies.includes(strategy.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setSelectedStrategies(prev => [...prev, strategy.id]);
                        } else {
                          setSelectedStrategies(prev => prev.filter(id => id !== strategy.id));
                        }
                      }}
                    />
                    {strategy.label}
                  </label>
                ))}
              </div>
            </div>

            <div className="form-group">
              <label htmlFor="custom-strategy">إضافات أخرى للاستراتيجية (اختياري)</label>
              <input
                type="text"
                id="custom-strategy"
                value={customStrategy}
                onChange={(e) => setCustomStrategy(e.target.value)}
                placeholder="أدخل أي استراتيجية أو أسلوب إضافي..."
              />
            </div>


            <button
              type="submit"
              className="btn-submit"
              disabled={loading}
            >
              {loading ? (
                <>
                  <RefreshCw className="spinner-icon" />
                  جاري التخطيط الذكي...
                </>
              ) : (
                <>
                  <Sparkles className="sparkle-icon" />
                  توليد خارطة المنهج (Syllabus)
                </>
              )}
            </button>
          </form>

          {/* Saved Courses History Panel */}
          <div className="saved-courses-section">
            <div className="section-header">
              <h3>المناهج المحفوظة 📚</h3>
              <button type="button" onClick={handleNewCourse} className="btn-new-course" title="بدء منهج جديد">
                <Plus size={14} />
                <span>منهج جديد</span>
              </button>
            </div>
            
            {(!Array.isArray(savedCourses) || savedCourses.length === 0) ? (
              <p className="no-saved-courses">لا توجد مناهج محفوظة حالياً.</p>
            ) : (
              <div className="saved-courses-list">
                {savedCourses.map(course => {
                  if (!course) return null;
                  return (
                    <div 
                      key={course.id} 
                      className={`saved-course-item ${activeCourseId === course.id ? 'active' : ''}`}
                      onClick={() => handleLoadCourse(course)}
                    >
                      <div className="course-item-info">
                        <span className="course-item-title">{course.title}</span>
                        <span className="course-item-meta">
                          {TARGET_AUDIENCES.find(a => a.id === course.targetAudience)?.label || course.targetAudience}
                          {course.syllabus?.weeks && Array.isArray(course.syllabus.weeks) && ` • ${course.syllabus.weeks.length} أسابيع`}
                        </span>
                      </div>
                      <button 
                        type="button"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDeleteCourse(course.id);
                        }}
                        className="btn-delete-course"
                        title="حذف المنهج"
                      >
                        <X size={14} />
                      </button>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </section>

        {/* Left side: Results Panel */}
        <section className="results-panel glass-container animate-fade-in">
          {error && (
            <div className="error-alert">
              <AlertCircle className="error-icon" />
              <span>{error}</span>
            </div>
          )}

          {/* Initial/Welcome state */}
          {!loading && !syllabus && !error && (
            <div className="welcome-state">
              <img src={sdaiaIcon} className="welcome-logo sdaia-icon-img" alt="SDAIA Icon" />
              <h3>ابدأ بتخطيط منهجك التعليمي</h3>

              <p>أدخل موضوع ورشة العمل ومعاييرها في اللوحة الجانبية، وسيقوم المساعد الذكي بتوزيع المنهج وتوفير خريطة طريق تفاعلية لتوليد الشرائح والمعامل برمجياً.</p>

              <div className="features-grid">
                <div className="feature-card">
                  <span className="feature-badge">1</span>
                  <h4>خطة دراسية ذكية</h4>
                  <p>تقسيم المواضيع زمنياً وتحديد الأهداف اليومية بدقة.</p>
                </div>
                <div className="feature-card">
                  <span className="feature-badge">2</span>
                  <h4>شرائح Reveal.js</h4>
                  <p>عروض تقديمية غنية تدعم العربية RTL والمسابقات ومظهر SDAIA.</p>
                </div>
                <div className="feature-card">
                  <span className="feature-badge">3</span>
                  <h4>دفاتر Jupyter</h4>
                  <p>معامل تدريبية برمجية مع شفرات ناقصة TODO للطلاب مع الحل النموذجي.</p>
                </div>
              </div>
            </div>
          )}

          {/* Loading state */}
          {loading && (
            <div className="loading-state">
              <div className="loading-spinner"></div>
              <h3>جاري بناء هيكل المنهج الدراسي عبر Gemini...</h3>
              <p>نقوم الآن بتصميم الأهداف التعليمية وتوزيع الدروس على الأسابيع والأيام التدريبية.</p>
            </div>
          )}

          {/* Syllabus Roadmap view */}
          {syllabus && !loading && (
            <div className="syllabus-view">
              <div className="course-header">
                <span className="badge-category">المنهج المقترح</span>
                <h2>{syllabus.title}</h2>
                <p>{syllabus.description}</p>
              </div>

              <div className="roadmap-title">
                <Calendar className="roadmap-icon text-teal" />
                <h3>خارطة الطريق وتوزيع الدروس</h3>
              </div>

              <div className="weeks-list">
                {syllabus && Array.isArray(syllabus.weeks) && syllabus.weeks.map((week) => (
                  <div key={week.week_number} className="week-item">
                    <button
                       type="button"
                       onClick={() => toggleWeek(week.week_number)}
                       className="week-header"
                    >
                      <div className="week-title-wrapper">
                        <span className="week-badge">الأسبوع {week.week_number}</span>
                        <h4>{week.title}</h4>
                      </div>
                      {expandedWeeks[week.week_number] ? <ChevronUp /> : <ChevronDown />}
                    </button>

                    {expandedWeeks[week.week_number] && (
                      <div className="days-list animate-fade-in">
                        {Array.isArray(week.days) && week.days.map((day) => {
                          const isGenerating = generatingLessons[day.lesson_id];
                          const result = lessonResults[day.lesson_id];
                          const isEditing = editingDayId === day.lesson_id;

                          if (isEditing) {
                            return (
                              <div key={day.lesson_id} className="day-card editing-card animate-fade-in">
                                <div className="day-card-header editing-header">
                                  <span className="day-number-badge">اليوم {day.day_number}</span>
                                  <input
                                    type="text"
                                    value={editForm.title}
                                    onChange={(e) => setEditForm({ ...editForm, title: e.target.value })}
                                    placeholder="عنوان الدرس"
                                    className="edit-input-field title-input"
                                  />
                                </div>

                                <div className="edit-field-group">
                                  <label>وصف الدرس:</label>
                                  <textarea
                                    value={editForm.description}
                                    onChange={(e) => setEditForm({ ...editForm, description: e.target.value })}
                                    placeholder="وصف تفصيلي للدرس"
                                    rows="2"
                                    className="edit-textarea-field"
                                  />
                                </div>

                                <div className="edit-field-group">
                                  <label>الأهداف التعليمية (هدف واحد في كل سطر):</label>
                                  <textarea
                                    value={editForm.objectives}
                                    onChange={(e) => setEditForm({ ...editForm, objectives: e.target.value })}
                                    placeholder="أدخل كل هدف في سطر مستقل..."
                                    rows="3"
                                    className="edit-textarea-field font-mono"
                                  />
                                </div>

                                <div className="edit-field-group">
                                  <label>استراتيجيات التعلم (استراتيجية واحدة في كل سطر):</label>
                                  <textarea
                                    value={editForm.strategies}
                                    onChange={(e) => setEditForm({ ...editForm, strategies: e.target.value })}
                                    placeholder="أدخل كل استراتيجية في سطر مستقل..."
                                    rows="2"
                                    className="edit-textarea-field font-mono"
                                  />
                                </div>

                                <div className="edit-field-group">
                                  <label>كيفية تفعيل واستخدام الاستراتيجية في الأنشطة:</label>
                                  <textarea
                                    value={editForm.strategy_application}
                                    onChange={(e) => setEditForm({ ...editForm, strategy_application: e.target.value })}
                                    placeholder="اشرح كيفية تطبيق الأنشطة والاستراتيجيات..."
                                    rows="2"
                                    className="edit-textarea-field"
                                  />
                                </div>

                                <div className="card-actions edit-actions-row">
                                  <button
                                    onClick={() => saveEditing(week.week_number, day.lesson_id)}
                                    className="btn-save-edit"
                                  >
                                    حفظ التغييرات 💾
                                  </button>
                                  <button
                                    onClick={() => setEditingDayId(null)}
                                    className="btn-cancel-edit"
                                  >
                                    إلغاء ❌
                                  </button>
                                </div>
                              </div>
                            );
                          }

                          return (
                            <div key={day.lesson_id} className="day-card">
                              <div className="day-card-header normal-header">
                                <div className="day-card-title-group">
                                  <span className="day-number-badge">اليوم {day.day_number}</span>
                                  <h5>{day.title}</h5>
                                </div>
                                {!result && !isGenerating && (
                                  <button
                                    onClick={() => startEditing(day)}
                                    className="btn-edit-trigger"
                                    title="تعديل تفاصيل الدرس"
                                  >
                                    تعديل المعايير ⚙️
                                  </button>
                                )}
                              </div>
                              <p className="day-desc">{day.description}</p>

                              {/* Objectives */}
                              {Array.isArray(day.objectives) && day.objectives.length > 0 && (
                                <div className="objectives-wrapper">
                                  <h6>أهداف الدرس:</h6>
                                  <ul>
                                    {day.objectives.map((obj, index) => (
                                      <li key={index}>
                                        <CheckCircle2 className="obj-icon" />
                                        <span>{obj}</span>
                                      </li>
                                    ))}
                                  </ul>
                                </div>
                              )}

                              {/* Learning Strategies */}
                              {Array.isArray(day.strategies) && day.strategies.length > 0 && (
                                <div className="strategies-wrapper">
                                  <h6>الاستراتيجيات المطبقة:</h6>
                                  <div className="strategies-badges">
                                    {day.strategies.map((strat, index) => (
                                      <span key={index} className="strategy-badge-item">
                                        {strat}
                                      </span>
                                    ))}
                                  </div>
                                </div>
                              )}

                              {/* Strategy Application */}
                              {day.strategy_application && (
                                <div className="strategy-app-wrapper">
                                  <h6>كيفية التفعيل والنشاط:</h6>
                                  <p className="strategy-app-text">{day.strategy_application}</p>
                                </div>
                              )}


                              {/* Action Buttons */}
                              <div className="card-actions">
                                {!result ? (
                                  <button
                                    onClick={() => handleGenerateLesson(day, syllabus.title)}
                                    disabled={isGenerating}
                                    className="btn-action-generate"
                                  >
                                    {isGenerating ? (
                                      <>
                                        <RefreshCw className="spinner-icon" />
                                        جاري توليد المحتوى...
                                      </>
                                    ) : (
                                      <>
                                        <Sparkles size={16} />
                                        توليد محتوى الدرس 🪄
                                      </>
                                    )}
                                  </button>
                                ) : (
                                  <div className="generation-results">
                                    <div className="success-tag">
                                      <CheckCircle2 size={16} className="text-teal" />
                                      <span>تم توليد الدرس بنجاح!</span>
                                    </div>
                                    <div className="result-buttons">
                                      {result.html_file && (
                                        <button
                                          onClick={() => handleOpenPreview(result, day.title)}
                                          className="btn-secondary"
                                        >
                                          <Play size={16} />
                                          عرض الشرائح محلياً 🎥
                                        </button>
                                      )}

                                      {result.html_file && (
                                        <a
                                          href={`https://hanenalmayouf.github.io/Content-creator-dashdoard/lessons/${day.lesson_id}/docs/lesson.html`}
                                          target="_blank"
                                          rel="noopener noreferrer"
                                          className="btn-secondary-link"
                                          style={{ backgroundColor: '#28A745', color: '#fff', border: 'none' }}
                                        >
                                          <ExternalLink size={16} />
                                          رابط العرض (.io) 🌐
                                        </a>
                                      )}

                                      <button
                                        onClick={() => handleOpenCodeEditor(day)}
                                        className="btn-secondary edit-code-btn"
                                      >
                                        تعديل كود الشرائح 📝
                                      </button>

                                      <a
                                        href={`https://colab.research.google.com/github/hanenalmayouf/Content-creator-dashdoard/blob/main/lessons/${day.lesson_id}/${day.lesson_id}_lab.ipynb`}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="btn-secondary-link"
                                        style={{ backgroundColor: '#F9AB00', color: '#fff', border: 'none' }}
                                      >
                                        <ExternalLink size={16} />
                                        Colab المعمل في 🚀
                                      </a>

                                      <a
                                        href={`${API_BASE_URL}${result.notebook_file}`}
                                        download
                                        className="btn-secondary-link"
                                      >
                                        <FlaskConical size={16} />
                                        تحميل المعمل 🧪
                                      </a>

                                      <a
                                        href={`${API_BASE_URL}${result.zip_package}`}
                                        download
                                        className="btn-secondary-link zip-btn"
                                      >
                                        <FolderArchive size={16} />
                                        تحميل الحزمة 📦
                                      </a>
                                    </div>
                                  </div>
                                )}
                              </div>
                            </div>
                          );
                        })}
                      </div>
                    )}
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      </main>

      {/* Slide Preview Modal / Overlay */}
      {activePreview && (
        <div className="preview-modal-backdrop">
          <div className="preview-modal glass-container">
            <div className="preview-modal-header">
              <h3>مستعرض الشرائح التفاعلية: {activePreview.title}</h3>
              <div className="preview-header-actions">
                <button onClick={handleFullScreen} className="btn-icon-action" title="ملء الشاشة">
                  <Maximize2 size={18} />
                </button>
                <a
                  href={activePreview.url}
                  target="_blank"
                  rel="noreferrer"
                  className="btn-icon-action-link"
                  title="فتح في نافذة جديدة"
                >
                  <ExternalLink size={18} />
                </a>
                <button onClick={() => setActivePreview(null)} className="btn-icon-action close-btn">
                  <X size={18} />
                </button>
              </div>
            </div>
            <div className="preview-modal-body">
              <iframe
                id="slides-iframe"
                src={activePreview.url}
                title={activePreview.title}
                width="100%"
                height="100%"
                frameBorder="0"
                allowFullScreen
              ></iframe>
            </div>
          </div>
        </div>
      )}

      {/* Slide Markdown Code Editor Modal */}
      {editingCodeDay && (
        <div className="preview-modal-backdrop">
          <div className="preview-modal qmd-editor-modal glass-container">
            <div className="preview-modal-header">
              <h3>محرر كود الشرائح (Quarto Markdown): {editingCodeDay.title}</h3>
              <div className="preview-header-actions">
                <button
                  onClick={() => setEditingCodeDay(null)}
                  className="btn-icon-action close-btn"
                  disabled={recompiling}
                >
                  <X size={18} />
                </button>
              </div>
            </div>
            <div className="preview-modal-body editor-body">
              {loadingCode ? (
                <div className="loading-state">
                  <div className="loading-spinner"></div>
                  <h3>جاري تحميل كود الشرائح...</h3>
                </div>
              ) : (
                <div className="editor-container-inner">
                  <div className="editor-instructions">
                    <p>يمكنك تعديل نصوص الشرائح وصيغتها مباشرة أدناه. بعد الانتهاء، اضغط على <strong>"حفظ وإعادة بناء"</strong> لتحديث ملفات العرض وحزمة التنزيل.</p>
                  </div>
                  <textarea
                    value={qmdContent}
                    onChange={(e) => setQmdContent(e.target.value)}
                    className="qmd-code-textarea"
                    placeholder="كود Quarto Markdown (.qmd)"
                    disabled={recompiling}
                  />
                  <div className="editor-actions">
                    <button
                      onClick={handleSaveCode}
                      className="btn-submit btn-save-code"
                      disabled={recompiling}
                    >
                      {recompiling ? (
                        <>
                          <RefreshCw className="spinner-icon" />
                          جاري حفظ وإعادة بناء الشرائح...
                        </>
                      ) : (
                        <>حفظ وإعادة تجميع 💾</>
                      )}
                    </button>
                    <button
                      onClick={() => setEditingCodeDay(null)}
                      className="btn-secondary"
                      disabled={recompiling}
                    >
                      إلغاء
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
