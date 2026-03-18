#!/usr/bin/env python3
"""
=============================================================
  أداة تحديث Footer لجميع صفحات موقع عبدالله نبيل
  - تحديث/إضافة روابط التواصل الاجتماعي
  - تحديث/إضافة خانة الاشتراك بالإيميل (web3forms)
  - تصحيح الروابط الخاطئة
  
  الاستخدام: python update_footer.py
=============================================================
"""

import os
import re
import shutil
from datetime import datetime
from pathlib import Path


# ============================================================
# الإعدادات - عدّل هذه القيم حسب حاجتك
# ============================================================

# مجلد الموقع (المجلد الحالي افتراضياً)
SITE_DIR = "."

# مفتاح web3forms للنشرة البريدية
WEB3FORMS_ACCESS_KEY = "94b920e4-a574-497a-a553-a3841670258f"

# الروابط الصحيحة
LINKS = {
    "linkedin": "https://linkedin.com/in/abdullah-nabil-n8n",
    "x_twitter": "https://x.com/abdullah_nabil_",
    "whatsapp": "https://wa.me/967718672576",
    "email": "mailto:abdullah0nabil@gmail.com",
    "github": "https://github.com/abdullah-nabil"
}

# هل تريد إنشاء نسخة احتياطية؟
CREATE_BACKUP = True


# ============================================================
# كود التواصل الاجتماعي الصحيح والكامل
# ============================================================

SOCIAL_LINKS_HTML = f'''                    <div>
                    <h4 class="font-bold text-white mb-4">تابعني</h4>
                    <div class="flex gap-3">
                        <!-- LinkedIn -->
                        <a href="{LINKS['linkedin']}" target="_blank" class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-saudi hover:text-white transition-all" title="LinkedIn">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
                        </a>
                        <!-- X (Twitter) -->
                        <a href="{LINKS['x_twitter']}" target="_blank" class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-700 hover:text-white transition-all" title="X (Twitter)">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>
                        </a>
                        <!-- WhatsApp -->
                        <a href="{LINKS['whatsapp']}" target="_blank" class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-green-500 hover:text-white transition-all" title="WhatsApp">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M.057 24l1.687-6.163c-1.041-1.804-1.588-3.849-1.587-5.946.003-6.556 5.338-11.891 11.893-11.891 3.181.001 6.167 1.24 8.413 3.488 2.245 2.248 3.481 5.236 3.48 8.414-.003 6.557-5.338 11.892-11.893 11.892-1.99-.001-3.951-.5-5.688-1.448l-6.305 1.654zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884-.001 2.225.651 3.891 1.746 5.634l-.999 3.648 3.742-.981zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>
                        </a>
                        <!-- Email -->
                        <a href="{LINKS['email']}" class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-red-500 hover:text-white transition-all" title="Email">
                            <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 5.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"></path></svg>
                        </a>
                        <!-- GitHub -->
                        <a href="{LINKS['github']}" target="_blank" class="w-10 h-10 bg-gray-800 rounded-lg flex items-center justify-center text-gray-400 hover:bg-gray-700 hover:text-white transition-all" title="GitHub">
                            <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/></svg>
                        </a>
                    </div>'''


# ============================================================
# كود خانة الاشتراك بالإيميل (النشرة البريدية)
# ============================================================

NEWSLETTER_HTML = f'''
                    <!-- النشرة البريدية -->
                    <div class="mt-6">
                        <h4 class="font-bold text-white mb-2 text-sm">احصل على نصائح أتمتة مجانية</h4>
                        <p class="text-gray-500 text-xs mb-3">انضم لأكثر من 500 متابع.</p>
                        <form action="https://api.web3forms.com/submit" method="POST" class="flex gap-2" id="newsletter-form">
                            <input type="hidden" name="access_key" value="{WEB3FORMS_ACCESS_KEY}">
                            <input type="hidden" name="subject" value="اشتراك جديد في النشرة البريدية">
                            <input type="hidden" name="from_name" value="النشرة البريدية - موقع عبدالله نبيل">
                            <input type="hidden" name="redirect" value="">
                            <input type="email" name="email" placeholder="بريدك الإلكتروني" required class="flex-1 px-3 py-2 bg-gray-800 border border-gray-700 rounded-lg text-sm text-white placeholder-gray-500 focus:border-saudi outline-none" dir="ltr">
                            <button type="submit" class="px-4 py-2 bg-saudi rounded-lg text-white text-sm font-bold hover:bg-saudi-light transition-colors">اشترك</button>
                        </form>
                    </div>'''


# ============================================================
# الكود الكامل للعمود الثالث في Footer (تابعني + النشرة)
# ============================================================

FULL_COLUMN3_HTML = f'''{SOCIAL_LINKS_HTML}
{NEWSLETTER_HTML}
                </div>'''


# ============================================================
# الفئة الرئيسية للمعالجة
# ============================================================

class FooterUpdater:
    """أداة تحديث Footer لجميع صفحات HTML"""

    def __init__(self, site_dir: str):
        self.site_dir = Path(site_dir)
        self.html_files = []
        self.results = {
            "updated": [],
            "skipped": [],
            "errors": [],
            "no_footer": []
        }

    def find_html_files(self):
        """البحث عن جميع ملفات HTML في المجلد والمجلدات الفرعية"""
        self.html_files = list(self.site_dir.rglob("*.html"))
        # استبعاد مجلد النسخ الاحتياطية
        self.html_files = [
            f for f in self.html_files
            if "backup_" not in str(f) and "node_modules" not in str(f)
        ]
        return self.html_files

    def create_backup(self, file_path: Path):
        """إنشاء نسخة احتياطية من الملف"""
        backup_dir = self.site_dir / f"backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        backup_dir.mkdir(exist_ok=True)

        # الحفاظ على هيكل المجلدات
        relative_path = file_path.relative_to(self.site_dir)
        backup_path = backup_dir / relative_path
        backup_path.parent.mkdir(parents=True, exist_ok=True)

        shutil.copy2(file_path, backup_path)
        return backup_path

    def has_footer(self, content: str) -> bool:
        """فحص إذا كان الملف يحتوي على footer"""
        return bool(re.search(r'<footer[\s>]', content, re.IGNORECASE))

    def fix_social_links(self, content: str) -> str:
        """تصحيح روابط التواصل الاجتماعي الخاطئة في كل الصفحة"""

        # تصحيح روابط LinkedIn الخاطئة
        wrong_linkedin_patterns = [
            r'href="https?://linkedin\.com/abdullah[^"]*"',
            r'href="https?://www\.linkedin\.com/abdullah[^"]*"',
            r'href="https?://linkedin\.com/in/[^"]*"',
            r'href="#"([^>]*title="LinkedIn")',
        ]
        for pattern in wrong_linkedin_patterns:
            if 'title="LinkedIn"' in pattern or 'LinkedIn' in content:
                content = re.sub(
                    r'href="[^"]*"(\s*[^>]*title="LinkedIn")',
                    f'href="{LINKS["linkedin"]}"\\1',
                    content
                )

        # تصحيح روابط WhatsApp الخاطئة
        content = re.sub(
            r'href="https?://wa\.me/[^"]*"',
            f'href="{LINKS["whatsapp"]}"',
            content
        )

        # تصحيح روابط X/Twitter الخاطئة
        content = re.sub(
            r'href="[^"]*"(\s*[^>]*title="X[^"]*")',
            f'href="{LINKS["x_twitter"]}"\\1',
            content
        )

        # تصحيح روابط البريد الإلكتروني
        content = re.sub(
            r'href="mailto:[^"]*"',
            f'href="{LINKS["email"]}"',
            content
        )

        return content

    def find_social_section(self, content: str) -> dict:
        """البحث عن قسم التواصل الاجتماعي في Footer"""
        result = {
            "exists": False,
            "has_newsletter": False,
            "start": -1,
            "end": -1
        }

        # البحث عن "تابعني" داخل Footer
        footer_match = re.search(r'<footer[\s>]', content, re.IGNORECASE)
        if not footer_match:
            return result

        footer_start = footer_match.start()
        footer_end_match = re.search(r'</footer>', content[footer_start:], re.IGNORECASE)
        if not footer_end_match:
            return result

        footer_content = content[footer_start:footer_start + footer_end_match.end()]

        # البحث عن قسم "تابعني"
        follow_match = re.search(r'تابعني', footer_content)
        if follow_match:
            result["exists"] = True

        # فحص وجود خانة النشرة البريدية
        newsletter_patterns = [
            r'احصل على نصائح أتمتة',
            r'newsletter',
            r'النشرة البريدية',
            r'بريدك الإلكتروني.*اشترك',
        ]
        for pattern in newsletter_patterns:
            if re.search(pattern, footer_content, re.IGNORECASE):
                result["has_newsletter"] = True
                break

        return result

    def update_footer_column3(self, content: str) -> tuple:
        """تحديث العمود الثالث في Footer (روابط + نشرة)"""
        changes_made = []

        # البحث عن Footer
        footer_match = re.search(r'<footer[\s>]', content, re.IGNORECASE)
        if not footer_match:
            return content, changes_made

        footer_start = footer_match.start()

        # ===== الحالة 1: يوجد قسم "تابعني" - نستبدله بالكامل =====
        # نبحث عن الـ div الذي يحتوي على "تابعني" بالكامل
        tabieni_pattern = re.compile(
            r'(<div[^>]*>\s*'                          # div البداية
            r'<h4[^>]*>تابعني</h4>\s*'                 # عنوان تابعني
            r'<div[^>]*class="flex gap-3"[^>]*>.*?</div>'  # أيقونات التواصل
            r'(?:\s*<!--.*?-->\s*)?'                    # تعليقات اختيارية
            r'(?:\s*<div[^>]*class="mt-6"[^>]*>.*?</div>)?' # النشرة البريدية (اختيارية)
            r'\s*</div>)',                              # إغلاق div الرئيسي
            re.DOTALL
        )

        match = tabieni_pattern.search(content, footer_start)

        if match:
            # استبدال القسم بالكامل
            content = content[:match.start()] + FULL_COLUMN3_HTML + content[match.end():]
            changes_made.append("تم تحديث قسم 'تابعني' والروابط")
            changes_made.append("تم تحديث/إضافة خانة النشرة البريدية")
            return content, changes_made

        # ===== الحالة 2: محاولة بديلة - بحث أبسط =====
        # البحث عن أي div يحتوي على "تابعني"
        simple_pattern = re.compile(
            r'(<h4[^>]*>تابعني</h4>.*?)(</div>\s*</div>)',
            re.DOTALL
        )

        footer_end = content.find('</footer>', footer_start)
        footer_section = content[footer_start:footer_end] if footer_end != -1 else content[footer_start:]

        match2 = simple_pattern.search(footer_section)
        if match2:
            # نحتاج نجد الـ div المحتوي
            # نبحث عن أقرب <div قبل "تابعني"
            tabieni_pos = footer_section.find('تابعني')
            if tabieni_pos != -1:
                # نبحث للخلف عن أقرب <div
                before_tabieni = footer_section[:tabieni_pos]
                last_div_open = before_tabieni.rfind('<div')

                if last_div_open != -1:
                    # نحتاج نجد نهاية هذا الـ div (مع كل محتوياته)
                    remaining = footer_section[last_div_open:]

                    # عدّ الـ div المفتوحة والمغلقة
                    div_count = 0
                    pos = 0
                    end_pos = -1

                    while pos < len(remaining):
                        open_match = re.search(r'<div[\s>]', remaining[pos:])
                        close_match = re.search(r'</div>', remaining[pos:])

                        if open_match and (not close_match or open_match.start() < close_match.start()):
                            div_count += 1
                            pos += open_match.start() + 4
                        elif close_match:
                            div_count -= 1
                            pos += close_match.start() + 6
                            if div_count == 0:
                                end_pos = pos
                                break
                        else:
                            break

                    if end_pos != -1:
                        absolute_start = footer_start + last_div_open
                        absolute_end = footer_start + last_div_open + end_pos

                        content = (
                            content[:absolute_start]
                            + FULL_COLUMN3_HTML
                            + content[absolute_end:]
                        )
                        changes_made.append("تم تحديث قسم 'تابعني' (طريقة بديلة)")
                        changes_made.append("تم تحديث/إضافة خانة النشرة البريدية")
                        return content, changes_made

        # ===== الحالة 3: لا يوجد قسم "تابعني" - نضيفه =====
        # نبحث عن آخر </div> قبل خط الفاصل في Footer
        divider_pattern = re.compile(
            r'(<!-- Divider -->|<div[^>]*class="border-t border-gray-800)',
            re.IGNORECASE
        )
        divider_match = divider_pattern.search(content, footer_start)

        if divider_match:
            # نضيف القسم قبل الفاصل
            insert_pos = divider_match.start()

            # نتأكد من إغلاق الـ grid الرئيسي
            content = (
                content[:insert_pos]
                + "\n                <!-- Column 3: Social Media -->\n"
                + FULL_COLUMN3_HTML
                + "\n            </div>\n\n            "
                + content[insert_pos:]
            )
            changes_made.append("تم إضافة قسم 'تابعني' جديد")
            changes_made.append("تم إضافة خانة النشرة البريدية")
        else:
            # نبحث عن </footer> ونضيف قبله
            footer_close = content.find('</footer>', footer_start)
            if footer_close != -1:
                insert_pos = footer_close

                content = (
                    content[:insert_pos]
                    + "\n        <!-- Social & Newsletter Section -->\n"
                    + "        <div class='container mx-auto px-4'>\n"
                    + FULL_COLUMN3_HTML
                    + "\n        </div>\n"
                    + content[insert_pos:]
                )
                changes_made.append("تم إضافة قسم 'تابعني' قبل إغلاق Footer")
                changes_made.append("تم إضافة خانة النشرة البريدية")

        return content, changes_made

    def add_newsletter_js(self, content: str) -> str:
        """إضافة JavaScript للنشرة البريدية إذا لم يكن موجوداً"""

        newsletter_js = '''
    <!-- Newsletter Form Handler -->
    <script>
    (function() {
        const nlForm = document.getElementById('newsletter-form');
        if (nlForm) {
            nlForm.addEventListener('submit', async function(e) {
                e.preventDefault();
                const btn = this.querySelector('button[type="submit"]');
                const emailInput = this.querySelector('input[name="email"]');
                const originalText = btn.textContent;
                
                btn.disabled = true;
                btn.textContent = 'جاري...';
                
                try {
                    const formData = new FormData(this);
                    // إضافة اسم تلقائي للمشترك
                    formData.append('name', 'مشترك نشرة بريدية');
                    formData.append('message', 'اشتراك جديد في النشرة البريدية من: ' + emailInput.value);
                    
                    const response = await fetch(this.action, {
                        method: 'POST',
                        body: formData,
                        headers: { 'Accept': 'application/json' }
                    });
                    
                    if (response.ok) {
                        btn.textContent = '✓ تم!';
                        btn.classList.remove('bg-saudi');
                        btn.classList.add('bg-green-600');
                        emailInput.value = '';
                        setTimeout(() => {
                            btn.textContent = originalText;
                            btn.classList.remove('bg-green-600');
                            btn.classList.add('bg-saudi');
                            btn.disabled = false;
                        }, 3000);
                    } else {
                        throw new Error('فشل الإرسال');
                    }
                } catch (error) {
                    btn.textContent = 'خطأ!';
                    btn.classList.remove('bg-saudi');
                    btn.classList.add('bg-red-500');
                    setTimeout(() => {
                        btn.textContent = originalText;
                        btn.classList.remove('bg-red-500');
                        btn.classList.add('bg-saudi');
                        btn.disabled = false;
                    }, 3000);
                }
            });
        }
    })();
    </script>'''

        # فحص إذا كان السكربت موجود مسبقاً
        if 'newsletter-form' in content and "nlForm.addEventListener" in content:
            return content

        # إضافة قبل </body>
        if '</body>' in content:
            content = content.replace('</body>', newsletter_js + '\n</body>')

        return content

    def process_file(self, file_path: Path) -> dict:
        """معالجة ملف HTML واحد"""
        result = {
            "file": str(file_path.relative_to(self.site_dir)),
            "changes": [],
            "status": "skipped"
        }

        try:
            # قراءة الملف
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                original_content = content

            # فحص وجود Footer
            if not self.has_footer(content):
                result["status"] = "no_footer"
                result["changes"].append("لا يحتوي على footer")
                return result

            # الخطوة 1: تصحيح جميع الروابط الخاطئة
            content = self.fix_social_links(content)
            if content != original_content:
                result["changes"].append("تم تصحيح الروابط الخاطئة")

            # الخطوة 2: تحديث/إضافة قسم التواصل والنشرة
            content, column_changes = self.update_footer_column3(content)
            result["changes"].extend(column_changes)

            # الخطوة 3: إضافة JavaScript للنشرة البريدية
            content_before_js = content
            content = self.add_newsletter_js(content)
            if content != content_before_js:
                result["changes"].append("تم إضافة JavaScript للنشرة البريدية")

            # حفظ التغييرات إذا وجدت
            if content != original_content:
                # إنشاء نسخة احتياطية
                if CREATE_BACKUP:
                    self.create_backup(file_path)

                # كتابة الملف المحدث
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(content)

                result["status"] = "updated"
            else:
                result["status"] = "no_changes"
                result["changes"].append("لا توجد تغييرات مطلوبة")

        except Exception as e:
            result["status"] = "error"
            result["changes"].append(f"خطأ: {str(e)}")

        return result

    def run(self):
        """تشغيل الأداة على جميع الملفات"""
        print("=" * 60)
        print("   أداة تحديث Footer - موقع عبدالله نبيل")
        print("=" * 60)
        print()

        # البحث عن ملفات HTML
        files = self.find_html_files()
        print(f"📂 تم العثور على {len(files)} ملف HTML")
        print(f"📁 المجلد: {self.site_dir.absolute()}")
        print()

        if not files:
            print("⚠️  لم يتم العثور على أي ملفات HTML!")
            return

        # معالجة كل ملف
        all_results = []
        for i, file_path in enumerate(files, 1):
            relative_path = file_path.relative_to(self.site_dir)
            print(f"[{i}/{len(files)}] معالجة: {relative_path}")

            result = self.process_file(file_path)
            all_results.append(result)

            # عرض النتيجة
            status_icons = {
                "updated": "✅",
                "no_changes": "⏭️",
                "no_footer": "⚠️",
                "error": "❌",
                "skipped": "⏭️"
            }
            icon = status_icons.get(result["status"], "❓")
            print(f"   {icon} {', '.join(result['changes'])}")
            print()

        # ===== التقرير النهائي =====
        print()
        print("=" * 60)
        print("   📊 التقرير النهائي")
        print("=" * 60)

        updated = [r for r in all_results if r["status"] == "updated"]
        no_changes = [r for r in all_results if r["status"] == "no_changes"]
        no_footer = [r for r in all_results if r["status"] == "no_footer"]
        errors = [r for r in all_results if r["status"] == "error"]

        print(f"\n   ✅ تم تحديثها: {len(updated)} ملف")
        for r in updated:
            print(f"      • {r['file']}")
            for change in r["changes"]:
                print(f"        → {change}")

        if no_changes:
            print(f"\n   ⏭️  بدون تغييرات: {len(no_changes)} ملف")
            for r in no_changes:
                print(f"      • {r['file']}")

        if no_footer:
            print(f"\n   ⚠️  بدون Footer: {len(no_footer)} ملف")
            for r in no_footer:
                print(f"      • {r['file']}")

        if errors:
            print(f"\n   ❌ أخطاء: {len(errors)} ملف")
            for r in errors:
                print(f"      • {r['file']}: {r['changes']}")

        if CREATE_BACKUP and updated:
            print(f"\n   💾 تم إنشاء نسخ احتياطية في مجلد backup_*")

        print()
        print("=" * 60)
        print("   ✨ اكتملت العملية بنجاح!")
        print("=" * 60)


# ============================================================
# التشغيل
# ============================================================

if __name__ == "__main__":
    updater = FooterUpdater(SITE_DIR)
    updater.run()