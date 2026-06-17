# -*- coding: utf-8 -*-
"""
نقيب المثاني - Vercel Serverless Function
دالة واحدة شاملة: استنباط + تأويل + استفسار
"""

import re
import os
import json
from collections import Counter
from http.server import BaseHTTPRequestHandler
from supabase import create_client, Client

# ======================== الاتصال بـ Supabase ========================
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# ======================== قاموس التحلي/التخلي ========================
TAHALLI_RULES = {
    "الله": {"hukm": "لا يجوز", "say": "لا يقال إله"},
    "الرب": {"hukm": "يجوز", "say": "يقال رباني"},
    "الرحمن": {"hukm": "يجوز", "say": "لا يقال رحمن"},
    "الرحيم": {"hukm": "يجب", "say": "يقال رحيم"},
    "مالك الملك": {"hukm": "يجوز", "say": "يقال مالك"},
    "الملك": {"hukm": "يجوز", "say": "يقال ملك"},
    "ذو الجلال والإكرام": {"hukm": "يجوز", "say": "يقال جليل كريم"},
    "الجليل": {"hukm": "يجوز", "say": "يقال جليل"},
    "المجيد": {"hukm": "يجوز", "say": "يقال مجيد"},
    "الماجد": {"hukm": "يجوز", "say": "يقال ماجد"},
    "العزيز": {"hukm": "يجوز", "say": "يقال عزيز"},
    "العظيم": {"hukm": "يجوز", "say": "يقال عظيم"},
    "الكبير": {"hukm": "يجوز", "say": "يقال كبير"},
    "الواسع": {"hukm": "يجوز", "say": "يقال واسع"},
    "الغني": {"hukm": "يجوز", "say": "يقال غني"},
    "العلي": {"hukm": "يجوز", "say": "يقال علي"},
    "الأول": {"hukm": "يجوز", "say": "يقال أول"},
    "الأخر": {"hukm": "يجوز", "say": "يقال آخر"},
    "الظاهر": {"hukm": "يجوز", "say": "يقال ظاهر"},
    "الباطن": {"hukm": "يجوز", "say": "يقال باطن"},
    "النور": {"hukm": "يجوز", "say": "يقال نور"},
    "الحي": {"hukm": "يجب", "say": "يقال حي"},
    "الباقي": {"hukm": "يجوز", "say": "يقال باقي"},
    "الواحد": {"hukm": "يجوز", "say": "يقال واحد"},
    "الصمد": {"hukm": "لا يجوز", "say": "لا يقال صمد"},
    "القدوس": {"hukm": "يجوز", "say": "يقال قدوس"},
    "السلام": {"hukm": "يجب", "say": "يقال سلام"},
    "العليم": {"hukm": "يجوز", "say": "يقال عليم"},
    "الحكيم": {"hukm": "يجوز", "say": "يقال حكيم"},
    "الرقيب": {"hukm": "يجوز", "say": "يقال رقيب"},
    "الشهيد": {"hukm": "يجوز", "say": "يقال شهيد"},
    "السميع": {"hukm": "يجوز", "say": "يقال سميع"},
    "البصير": {"hukm": "يجوز", "say": "يقال بصير"},
    "المحصي": {"hukm": "يجوز", "say": "يقال محصي"},
    "الخبير": {"hukm": "يجوز", "say": "يقال خبير"},
    "الصبور": {"hukm": "يجب", "say": "يقال صبور"},
    "الرشيد": {"hukm": "يجب", "say": "يقال رشيد"},
    "العدل": {"hukm": "يجب", "say": "يقال عدل"},
    "الحكم": {"hukm": "يجوز", "say": "يقال حكم"},
    "الحق": {"hukm": "يجب", "say": "يقال حق"},
    "المقسط": {"hukm": "يجوز", "say": "يقال مقسط"},
    "المتعال": {"hukm": "لا يجوز", "say": "لا يقال متعال"},
    "الخالق": {"hukm": "يجوز", "say": "يقال خالق"},
    "البارئ": {"hukm": "يجوز", "say": "يقال بارئ"},
    "المصور": {"hukm": "يجوز", "say": "يقال مصور"},
    "الواجد": {"hukm": "يجوز", "say": "يقال واجد"},
    "البديع": {"hukm": "يجوز", "say": "يقال بديع"},
    "المبدئ": {"hukm": "يجوز", "say": "يقال مبدئ"},
    "المعيد": {"hukm": "يجوز", "say": "يقال معيد"},
    "المحيي": {"hukm": "يجوز", "say": "يقال محيي"},
    "المميت": {"hukm": "لا يجوز", "say": "لا يقال مميت"},
    "الباعث": {"hukm": "لا يجوز", "say": "لا يقال باعث"},
    "الوارث": {"hukm": "يجوز", "say": "يقال وارث"},
    "القادر": {"hukm": "يجوز", "say": "يقال قادر"},
    "المقتدر": {"hukm": "يجوز", "say": "يقال مقتدر"},
    "الضار": {"hukm": "يجوز", "say": "يقال ضار"},
    "المانع": {"hukm": "يجوز", "say": "يقال مانع"},
    "الجامع": {"hukm": "يجوز", "say": "يقال جامع"},
    "المنتقم": {"hukm": "يجوز", "say": "يقال منتقم"},
    "القابض": {"hukm": "يجوز", "say": "يقال قابض"},
    "الخافض": {"hukm": "يجوز", "say": "يقال خافض"},
    "المؤخر": {"hukm": "يجوز", "say": "يقال مؤخر"},
    "المقيت": {"hukm": "يجوز", "say": "يقال مقيت"},
    "المذل": {"hukm": "يجوز", "say": "يقال مذل"},
    "الجبار": {"hukm": "يجوز", "say": "يقال جبار"},
    "القهار": {"hukm": "يجوز", "say": "يقال قهار"},
    "المهيمن": {"hukm": "يجوز", "say": "يقال مهيمن"},
    "المتكبر": {"hukm": "لا يجوز", "say": "لا يقال متكبر"},
    "القوي": {"hukm": "يجوز", "say": "يقال قوي"},
    "المتين": {"hukm": "يجوز", "say": "يقال متين"},
    "الكريم": {"hukm": "يجب", "say": "يقال كريم"},
    "الفتاح": {"hukm": "يجوز", "say": "يقال فتاح"},
    "المغني": {"hukm": "يجوز", "say": "يقال مغني"},
    "الرزاق": {"hukm": "يجوز", "say": "يقال رزاق"},
    "الوهاب": {"hukm": "يجوز", "say": "يقال وهاب"},
    "الباسط": {"hukm": "يجوز", "say": "يقال باسط"},
    "القيوم": {"hukm": "يجوز", "say": "يقال قيوم"},
    "البر": {"hukm": "يجب", "say": "يقال بر"},
    "المجيب": {"hukm": "يجوز", "say": "يقال مجيب"},
    "النافع": {"hukm": "يجوز", "say": "يقال نافع"},
    "الحفيظ": {"hukm": "يجب", "say": "يقال حفيظ"},
    "العفو": {"hukm": "يجوز", "say": "يقال عفو"},
    "اللطيف": {"hukm": "يجوز", "say": "يقال لطيف"},
    "الرؤوف": {"hukm": "يجب", "say": "يقال رؤوف"},
    "الحليم": {"hukm": "يجب", "say": "يقال حليم"},
    "المعز": {"hukm": "يجوز", "say": "يقال معز"},
    "الرافع": {"hukm": "يجوز", "say": "يقال رافع"},
    "المقدم": {"hukm": "يجوز", "say": "يقال مقدم"},
    "الوال": {"hukm": "يجب", "say": "يقال وال"},
    "الغفار": {"hukm": "يجوز", "say": "يقال غفار"},
    "الغفور": {"hukm": "يجوز", "say": "يقال غفور"},
    "التواب": {"hukm": "يجوز", "say": "يقال تواب"},
    "الودود": {"hukm": "يجب", "say": "يقال ودود"},
    "الشكور": {"hukm": "يجب", "say": "يقال شكور"},
    "الحميد": {"hukm": "يجب", "say": "يقال حميد"},
    "الحسيب": {"hukm": "يجوز", "say": "يقال حسيب"},
    "الولي": {"hukm": "يجوز", "say": "يقال ولي"},
    "الوكيل": {"hukm": "يجوز", "say": "يقال وكيل"},
    "الهادي": {"hukm": "يجوز", "say": "يقال هادي"},
    "المؤمن": {"hukm": "يجب", "say": "يقال مؤمن"},
}

# ======================== الدوال المساعدة ========================
def clean_arabic_text(text):
    if not text: return ""
    text = re.sub(r"[\u064B-\u0652\u0670\u0656\u0657\u0615-\u061A\u06D6-\u06ED]", "", text)
    text = re.sub(r"[ٰٖٓٗٙٚۡۥۦ]", "", text)
    text = (text.replace("إ","ا").replace("أ","ا").replace("آ","ا")
                .replace("ة","ه").replace("ٱ","ا").replace("ى","ي")
                .replace("ئ","ي").replace("ؤ","و"))
    return " ".join(text.split())

def get_tahalli_rule(name):
    name_clean = clean_arabic_text(name)
    for key, rule in TAHALLI_RULES.items():
        if clean_arabic_text(key) == name_clean:
            return f"{rule['hukm']} التحلي به ({rule['say']})"
    return "لا يوجد حكم محدد"

def get_special_attribute(name):
    name_clean = clean_arabic_text(name)
    for w in ['الله','الٰه','اله','اللهم']:
        if w in name_clean: return "مشيئة الألوهية"
    for w in ['الرب','ربنا','ربكم','ربك','ربي','رب']:
        if w in name_clean: return "شؤون الربوبية"
    return None

def extract_keywords(text, top_n=10):
    stop_words = {'في','على','إلى','عن','من','إن','أن','و','ف','ب','ل','ك','ما',
                  'لا','هل','قد','ثم','حتى','إذا','لم','لن','هذا','هذه','ذلك',
                  'تلك','الذي','التي','يكون','كان','ليس','إلا','بل','لكن','عند','مع','بين'}
    words = text.split()
    filtered = [w for w in words if w not in stop_words and len(w) > 2]
    return [word for word, _ in Counter(filtered).most_common(top_n)]

# ======================== استعلامات Supabase ========================
def search_quran(q_clean, sb):
    try:
        resp = sb.table("quran_verses").select("surah,ayah,text").execute()
        for row in resp.data:
            if clean_arabic_text(str(row.get("text",""))).replace("ٱ","ا") == q_clean.replace("ٱ","ا"):
                return {
                    "is_wahy": True,
                    "source": "القرآن",
                    "reference": f"سورة {row['surah']} آية {row['ayah']}",
                    "details": str(row.get("text",""))[:150]
                }
    except: pass
    return None

def search_manjam(q_clean, sb):
    try:
        resp = sb.table("manjam_usul").select("content").execute()
        for row in resp.data:
            if q_clean in clean_arabic_text(str(row.get("content",""))):
                return {
                    "is_wahy": False,
                    "source": "منجم الأصول",
                    "reference": "منجم الأصول",
                    "details": str(row.get("content",""))[:150]
                }
    except: pass
    return None

def search_idah(q_clean, sb):
    try:
        resp = sb.table("idah_muhayid").select("content").execute()
        for row in resp.data:
            if q_clean in clean_arabic_text(str(row.get("content",""))):
                return {
                    "is_wahy": False,
                    "source": "الإيضاح المحايد",
                    "reference": "الإيضاح المحايد",
                    "details": str(row.get("content",""))[:150]
                }
    except: pass
    return None

def search_in_sources(q_clean, sb):
    result = search_quran(q_clean, sb)
    if result: return result
    result = search_manjam(q_clean, sb)
    if result: return result
    result = search_idah(q_clean, sb)
    if result: return result
    return {
        "is_wahy": False,
        "source": "غير وحي",
        "reference": "منجم الأصول",
        "details": "لم يوجد نص مباشر"
    }

def read_author_rules(q_clean, sb):
    context = ""
    for table, label in [("manjam_usul","المنجم"), ("idah_muhayid","الإيضاح")]:
        try:
            resp = sb.table(table).select("content").execute()
            for row in resp.data:
                if q_clean in clean_arabic_text(str(row.get("content",""))):
                    context += f"• في {label}: {str(row.get('content',''))[:120]}\n"
        except: pass
    return context

# ======================== محرك الاستنباط ========================
def classify_branch(text):
    text_clean = clean_arabic_text(text)
    branches = []
    if any(kw in text_clean for kw in ['الصلاة','الزكاة','الصوم','الحج','الطهارة','الوضوء','الغسل','التيمم']):
        branches.append("تشريعي (فرع الإسلام)")
    if any(kw in text_clean for kw in ['الإيمان','المؤمنون','آمنوا','التوحيد','الله','الرسل','كفر','شرك']):
        branches.append("عقائدي (فرع الإيمان)")
    if any(kw in text_clean for kw in ['البيع','الشراء','التجارة','الربا','الطلاق','النكاح','الزواج','الأخلاق','بر','إحسان','معروف','منكر']):
        branches.append("معاملاتي (فرع الإحسان)")
    if not branches:
        branches.append("تشريعي (فرع الإسلام)")
    return branches

def classify_dabit(text):
    text_clean = clean_arabic_text(text)
    dabits = []
    asma_pattern = r'(الله|الرب|الرحمن|الرحيم|الملك|القدوس|السلام|المؤمن|المهيمن|العزيز|الجبار|المتكبر|الخالق|البارئ|المصور|الغفور|القهار|الوهاب|الرزاق|الفتاح|العليم|القابض|الباسط|الخافض|الرافع|المعز|المذل|السميع|البصير|الحكم|العدل|اللطيف|الخبير|الحليم|العظيم|الشكور|العلي|الكبير|الحفيظ|المقيت|الحسيب|الجليل|الكريم|الرقيب|المجيب|الواسع|الحكيم|الودود|المجيد|الباعث|الشهيد|الحق|الوكيل|القوي|المتين|الولي|الحميد|المحصي|المبدئ|المعيد|المحيي|المميت|الواجد|الماجد|الواحد|الصمد|القادر|المقتدر|المقدم|المؤخر|الأول|الآخر|الظاهر|الباطن|الوال|المتعال|البر|التواب|المنتقم|العفو|الرؤوف|مالك الملك|ذو الجلال والإكرام|المقسط|الجامع|الغني|المغني|المانع|الضار|النافع|النور|الهادي|البديع|الباقي|الوارث|الرشيد|الصبور)'
    if re.search(asma_pattern, text_clean): dabits.append("لفظ محكم")
    if any(k in text_clean for k in ['قياس','علة','شبه']): dabits.append("القياس")
    if any(k in text_clean for k in ['أجمع','إجماع','اتفق']): dabits.append("الإجماع")
    if any(k in text_clean for k in ['نسخ','ناسخ','منسوخ']): dabits.append("النسخ")
    if any(k in text_clean for k in ['فعل','عمل','صنع']): dabits.append("الفعل")
    if any(k in text_clean for k in ['أقر','إقرار','اعترف']): dabits.append("الإقرار")
    if any(k in text_clean for k in ['سبب','سببية']): dabits.append("السبب")
    if any(k in text_clean for k in ['مجمل','مبهم','احتمال']): dabits.append("لفظ مجمل")
    if not dabits: dabits.append("لفظ متفاوت")
    return dabits

def get_dabit_details(text, asl_source, dabit_rule):
    command_kw = ['افعلوا','اقيموا','اتوا','اطيعوا','تفسحوا','انشزوا','افسحوا','أمر','كتب','فرض','أوجب','لابد','يجب','يلزم','حق','على']
    prohibition_kw = ['نهي','حرم','لا تفعل','لا يجوز','لا يحل','لا تقربوا']
    has_command = any(kw in text for kw in command_kw)
    has_prohibition = any(kw in text for kw in prohibition_kw)
    dabit_str = " ".join(dabit_rule) if isinstance(dabit_rule, list) else dabit_rule
    if "قياس" in dabit_str: dab_type = "قياس"
    elif "إجماع" in dabit_str: dab_type = "إجماع"
    elif "نسخ" in dabit_str: dab_type = "نسخ"
    elif "فعل" in dabit_str: dab_type = "فعل"
    elif "إقرار" in dabit_str: dab_type = "إقرار"
    elif "سبب" in dabit_str: dab_type = "سبب"
    elif "محكم" in dabit_str: dab_type = "لفظ محكم"
    elif "مجمل" in dabit_str: dab_type = "لفظ مجمل"
    else: dab_type = "لفظ متفاوت"
    return {
        "type": dab_type,
        "source": asl_source if asl_source in ['الكتاب','السنة'] else 'لا ينتمي لوحي',
        "has_command": has_command,
        "has_prohibition": has_prohibition
    }

def extract_hukm_nazari(text, dabit, branch, asl_source):
    ruling_indicators = ['وجب','فرض','لابد','يجب','يلزم','حق','على','نهي','حرم','لا تفعل',
                         'لا يجوز','لا يحل','ندب','مندوب','استحب','سنة','مكروه','يكره',
                         'مباح','حلال','يجوز','آداء','قضاء','إعادة','رخصة','عزيمة',
                         'افعلوا','اقيموا','اتوا','اطيعوا','تفسحوا','انشزوا','افسحوا']
    if not any(kw in text for kw in ruling_indicators): return "النص لا يحمل حكماً"
    details = get_dabit_details(text, asl_source, dabit)
    if details["type"] == "إقرار": return "جائز"
    if "عقائدي" in str(branch) and details["type"] == "لفظ محكم" and details["source"] == 'الكتاب': return "واجب"
    if details["type"] == "لفظ محكم" and details["source"] == 'الكتاب':
        if details["has_command"]: return "واجب"
        elif details["has_prohibition"]: return "مستحيل"
        else: return "جائز"
    return "جائز"

def extract_hukm_darori(text, nazari, dabit, branch, asl_source):
    if nazari == "النص لا يحمل حكماً": return "النص لا يحمل حكماً"
    details = get_dabit_details(text, asl_source, dabit)
    if "عقائدي" in str(branch) and nazari == "واجب": return "فرض عين"
    if details["type"] == "لفظ محكم" and details["source"] == 'الكتاب':
        if nazari == "واجب": return "فرض عين"
        elif nazari == "مستحيل": return "حرام"
        else: return "جائز"
    if details["type"] == "قياس" and 'علة' in text:
        text_clean = clean_arabic_text(text)
        if 'آداء' in text_clean or 'اداء' in text_clean: return "الآداء"
        elif 'قضاء' in text_clean: return "القضاء"
        elif 'إعادة' in text_clean or 'اعادة' in text_clean: return "الإعادة"
        elif 'رخصة' in text_clean or 'رخصه' in text_clean: return "الرخصة"
        else: return "العزيمة"
    return "مباح"

def istinbat_engine(user_query, sb):
    q_clean = clean_arabic_text(user_query)
    origin = search_in_sources(q_clean, sb)
    asl_source = ('الكتاب' if origin['source'] == 'القرآن'
                  else 'السنة' if origin['source'] not in ['غير وحي','منجم الأصول','الإيضاح المحايد']
                  else 'لا ينتمي لوحي')
    asl_type = (f"{origin['source']} - {origin['reference']}" if origin['is_wahy']
                else f"{origin['source']} (ليس وحياً)")
    branch     = classify_branch(q_clean)
    dabit_rule = classify_dabit(q_clean)
    nazari     = extract_hukm_nazari(q_clean, dabit_rule, branch, asl_source)
    darori     = extract_hukm_darori(q_clean, nazari, dabit_rule, branch, asl_source)
    author_notes = read_author_rules(q_clean, sb)
    match_seerah = f"• التخريج: {origin['details']}\n"
    if author_notes:
        match_seerah += f"• مطابقات المؤلف:\n{author_notes}"
    return {
        "asl_type": asl_type,
        "asl_source": asl_source,
        "branch_context": branch,
        "dabit_rule": dabit_rule,
        "hukm_nazari": nazari,
        "hukm_darori_illa": darori,
        "sunnah_seerah_match": match_seerah
    }

# ======================== محرك التأويل ========================
def tawil_engine(user_query, sb):
    q_clean = clean_arabic_text(user_query)
    try:
        resp = sb.table("AlArwiqa_Author_Rules").select(
            "asm_name,martaba_text,rwaq_text,bab_text,rkn_text"
        ).execute()
        rows = resp.data
    except:
        rows = []

    detected, interpretations = [], []

    def add_name(name):
        if name in detected: return
        detected.append(name)
        for r in rows:
            if clean_arabic_text(r['asm_name']) == clean_arabic_text(name):
                interpretations.append({
                    "asm_name":     r['asm_name'],
                    "martaba":      r['martaba_text'],
                    "rwaq":         r['rwaq_text'],
                    "bab":          r['bab_text'],
                    "rkn":          r['rkn_text'],
                    "special_note": get_special_attribute(r['asm_name']) or "",
                    "tahalli":      get_tahalli_rule(r['asm_name'])
                })
                break

    for w in q_clean.split():
        if w.startswith('ال') and len(w) > 2:
            for r in rows:
                if clean_arabic_text(r['asm_name']) == clean_arabic_text(w):
                    add_name(r['asm_name']); break
        if 'الله' in w or 'اله' in w: add_name('الله')
        if 'رب' in w: add_name('الرب')

    return {"names_found": detected, "interpretation": interpretations}

# ======================== محرك الاستفسار ========================
def istifsar_engine(user_query, sb):
    q_clean = clean_arabic_text(user_query)
    results = []
    for table, label in [("idah_muhayid","كتاب الإيضاح"), ("manjam_usul","كتاب منجم الأصول"), ("quran_verses","القرآن")]:
        try:
            field = "text" if table == "quran_verses" else "content"
            resp = sb.table(table).select(field).execute()
            for row in resp.data:
                if q_clean in clean_arabic_text(str(row.get(field,""))):
                    results.append({"source": label, "text": str(row.get(field,""))[:300]})
                    break
        except: pass
    return {"answers": results}

# ======================== Vercel Handler ========================
class handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_POST(self):
        try:
            length = int(self.headers.get('Content-Length', 0))
            body = json.loads(self.rfile.read(length) or b'{}')
            user_query = body.get("query", "").strip()

            if not user_query:
                self._respond(400, {"error": "الحقل query مطلوب"})
                return

            if not SUPABASE_URL or not SUPABASE_KEY:
                self._respond(500, {"error": "متغيرات البيئة غير مضبوطة"})
                return

            sb = get_supabase()
            result = {
                "query":    user_query,
                "istinbat": istinbat_engine(user_query, sb),
                "tawil":    tawil_engine(user_query, sb),
                "istifsar": istifsar_engine(user_query, sb)
            }
            self._respond(200, result)

        except Exception as e:
            self._respond(500, {"error": str(e)})

    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def _respond(self, code, data):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(code)
        self._send_cors_headers()
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
