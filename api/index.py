
# -*- coding: utf-8 -*-
"""
نقيب المثاني - Vercel Serverless Function (FastAPI)
"""

import re
import os
import json
from collections import Counter
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

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

def search_quran(q_clean, sb):
    try:
        resp = sb.table("quran_verses").select("surah,ayah,text").execute()
        for row in resp.data:
            if clean_arabic_text(str(row.get("text",""))).replace("ٱ","ا") == q_clean.replace("ٱ","ا"):
                return {"is_wahy": True, "source": "القرآن",
                        "reference": f"سورة {row['surah']} آية {row['ayah']}",
                        "details": str(row.get("text",""))[:150]}
    except: pass
    return None

def search_manjam(q_clean, sb):
    try:
        resp = sb.table("manjam_usul").select("content").execute()
        for row in resp.data:
            if q_clean in clean_arabic_text(str(row.get("content",""))):
                return {"is_wahy": False, "source": "منجم الأصول",
                        "reference": "منجم الأصول", "details": str(row.get("content",""))[:150]}
    except: pass
    return None

def search_idah(q_clean, sb):
    try:
        resp = sb.table("idah_muhayid").select("content").execute()
        for row in resp.data:
            if q_clean in clean_arabic_text(str(row.get("content",""))):
                return {"is_wahy": False, "source": "الإيضاح المحايد",
                        "reference": "الإيضاح المحايد", "details": str(row.get("content",""))[:150]}
    except: pass
    return None

def search_in_sources(q_clean, sb):
    return (search_quran(q_clean, sb) or search_manjam(q_clean, sb) or
            search_idah(q_clean, sb) or
            {"is_wahy": False, "source": "غير وحي", "reference": "منجم الأصول", "details": "لم يوجد نص مباشر"})

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

def classify_branch(text):
    t = clean_arabic_text(text)
    branches = []
    if any(k in t for k in ['الصلاة','الزكاة','الصوم','الحج','الطهارة','الوضوء','الغسل','التيمم']):
        branches.append("تشريعي (فرع الإسلام)")
    if any(k in t for k in ['الإيمان','المؤمنون','آمنوا','التوحيد','الله','الرسل','كفر','شرك']):
        branches.append("عقائدي (فرع الإيمان)")
    if any(k in t for k in ['البيع','الشراء','التجارة','الربا','الطلاق','النكاح','الزواج','الأخلاق','بر','إحسان','معروف','منكر']):
        branches.append("معاملاتي (فرع الإحسان)")
    return branches or ["تشريعي (فرع الإسلام)"]

def classify_dabit(text):
    t = clean_arabic_text(text)
    dabits = []
    asma = r'(الله|الرب|الرحمن|الرحيم|الملك|القدوس|السلام|المؤمن|المهيمن|العزيز|الجبار|المتكبر|الخالق|البارئ|المصور|الغفور|القهار|الوهاب|الرزاق|الفتاح|العليم|القابض|الباسط|السميع|البصير|الحكم|العدل|اللطيف|الخبير|الحليم|العظيم|الشكور|العلي|الكبير|الحفيظ|الجليل|الكريم|الرقيب|المجيب|الواسع|الحكيم|الودود|المجيد|الشهيد|الحق|الوكيل|القوي|المتين|الولي|الحميد|المحصي|المبدئ|المعيد|المحيي|المميت|الواجد|الماجد|الواحد|الصمد|القادر|المقتدر|المقدم|المؤخر|الأول|الآخر|الظاهر|الباطن|الوال|المتعال|البر|التواب|المنتقم|العفو|الرؤوف|المقسط|الجامع|الغني|المغني|المانع|الضار|النافع|النور|الهادي|البديع|الباقي|الوارث|الرشيد|الصبور)'
    if re.search(asma, t): dabits.append("لفظ محكم")
    if any(k in t for k in ['قياس','علة','شبه']): dabits.append("القياس")
    if any(k in t for k in ['أجمع','إجماع','اتفق']): dabits.append("الإجماع")
    if any(k in t for k in ['نسخ','ناسخ','منسوخ']): dabits.append("النسخ")
    if any(k in t for k in ['فعل','عمل','صنع']): dabits.append("الفعل")
    if any(k in t for k in ['أقر','إقرار','اعترف']): dabits.append("الإقرار")
    if any(k in t for k in ['سبب','سببية']): dabits.append("السبب")
    if any(k in t for k in ['مجمل','مبهم','احتمال']): dabits.append("لفظ مجمل")
    return dabits or ["لفظ متفاوت"]

def get_dabit_details(text, asl_source, dabit_rule):
    cmd = ['افعلوا','اقيموا','اتوا','اطيعوا','أمر','كتب','فرض','أوجب','لابد','يجب','يلزم']
    prh = ['نهي','حرم','لا تفعل','لا يجوز','لا يحل','لا تقربوا']
    ds = " ".join(dabit_rule) if isinstance(dabit_rule, list) else dabit_rule
    tp = ("قياس" if "قياس" in ds else "إجماع" if "إجماع" in ds else "نسخ" if "نسخ" in ds else
          "فعل" if "فعل" in ds else "إقرار" if "إقرار" in ds else "سبب" if "سبب" in ds else
          "لفظ محكم" if "محكم" in ds else "لفظ مجمل" if "مجمل" in ds else "لفظ متفاوت")
    return {"type": tp,
            "source": asl_source if asl_source in ['الكتاب','السنة'] else 'لا ينتمي لوحي',
            "has_command": any(k in text for k in cmd),
            "has_prohibition": any(k in text for k in prh)}

def extract_hukm_nazari(text, dabit, branch, asl_source):
    ri = ['وجب','فرض','لابد','يجب','يلزم','نهي','حرم','لا تفعل','لا يجوز','ندب','مندوب',
          'استحب','سنة','مكروه','يكره','مباح','حلال','يجوز','افعلوا','اقيموا','اتوا']
    if not any(k in text for k in ri): return "النص لا يحمل حكماً"
    d = get_dabit_details(text, asl_source, dabit)
    if d["type"] == "إقرار": return "جائز"
    if "عقائدي" in str(branch) and d["type"] == "لفظ محكم" and d["source"] == 'الكتاب': return "واجب"
    if d["type"] == "لفظ محكم" and d["source"] == 'الكتاب':
        return "واجب" if d["has_command"] else "مستحيل" if d["has_prohibition"] else "جائز"
    return "جائز"

def extract_hukm_darori(text, nazari, dabit, branch, asl_source):
    if nazari == "النص لا يحمل حكماً": return "النص لا يحمل حكماً"
    d = get_dabit_details(text, asl_source, dabit)
    if "عقائدي" in str(branch) and nazari == "واجب": return "فرض عين"
    if d["type"] == "لفظ محكم" and d["source"] == 'الكتاب':
        return "فرض عين" if nazari == "واجب" else "حرام" if nazari == "مستحيل" else "جائز"
    if d["type"] == "قياس" and 'علة' in text:
        tc = clean_arabic_text(text)
        if 'آداء' in tc or 'اداء' in tc: return "الآداء"
        if 'قضاء' in tc: return "القضاء"
        if 'إعادة' in tc: return "الإعادة"
        if 'رخصة' in tc: return "الرخصة"
        return "العزيمة"
    return "مباح"

def istinbat_engine(user_query, sb):
    q = clean_arabic_text(user_query)
    origin = search_in_sources(q, sb)
    asl_source = ('الكتاب' if origin['source'] == 'القرآن' else
                  'السنة' if origin['source'] not in ['غير وحي','منجم الأصول','الإيضاح المحايد'] else
                  'لا ينتمي لوحي')
    branch = classify_branch(q)
    dabit  = classify_dabit(q)
    nazari = extract_hukm_nazari(q, dabit, branch, asl_source)
    darori = extract_hukm_darori(q, nazari, dabit, branch, asl_source)
    notes  = read_author_rules(q, sb)
    match  = f"• التخريج: {origin['details']}\n"
    if notes: match += f"• مطابقات المؤلف:\n{notes}"
    return {"asl_type": f"{origin['source']} - {origin['reference']}" if origin['is_wahy'] else f"{origin['source']} (ليس وحياً)",
            "asl_source": asl_source, "branch_context": branch, "dabit_rule": dabit,
            "hukm_nazari": nazari, "hukm_darori_illa": darori, "sunnah_seerah_match": match}

def tawil_engine(user_query, sb):
    q = clean_arabic_text(user_query)
    try:
        rows = sb.table("AlArwiqa_Author_Rules").select("asm_name,martaba_text,rwaq_text,bab_text,rkn_text").execute().data
    except: rows = []
    detected, interpretations = [], []
    def add_name(name):
        if name in detected: return
        detected.append(name)
        for r in rows:
            if clean_arabic_text(r['asm_name']) == clean_arabic_text(name):
                interpretations.append({
                    "asm_name": r['asm_name'], "martaba": r['martaba_text'],
                    "rwaq": r['rwaq_text'], "bab": r['bab_text'], "rkn": r['rkn_text'],
                    "special_note": get_special_attribute(r['asm_name']) or "",
                    "tahalli": get_tahalli_rule(r['asm_name'])})
                break
    for w in q.split():
        if w.startswith('ال') and len(w) > 2:
            for r in rows:
                if clean_arabic_text(r['asm_name']) == clean_arabic_text(w): add_name(r['asm_name']); break
        if 'الله' in w or 'اله' in w: add_name('الله')
        if 'رب' in w: add_name('الرب')
    return {"names_found": detected, "interpretation": interpretations}

def istifsar_engine(user_query, sb):
    q = clean_arabic_text(user_query)
    results = []
    for table, label in [("idah_muhayid","كتاب الإيضاح"), ("manjam_usul","كتاب منجم الأصول"), ("quran_verses","القرآن")]:
        try:
            field = "text" if table == "quran_verses" else "content"
            for row in sb.table(table).select(field).execute().data:
                if q in clean_arabic_text(str(row.get(field,""))):
                    results.append({"source": label, "text": str(row.get(field,""))[:300]}); break
        except: pass
    return {"answers": results}

@app.post("/api/index")
@app.post("/")
async def salsal_grand_query(request: Request):
    try:
        body = await request.json()
        user_query = body.get("query", "").strip()
        if not user_query:
            return JSONResponse({"error": "الحقل query مطلوب"}, status_code=400)
        if not SUPABASE_URL or not SUPABASE_KEY:
            return JSONResponse({"error": "متغيرات البيئة غير مضبوطة"}, status_code=500)
        sb = get_supabase()
        return JSONResponse({
            "query": user_query,
            "istinbat": istinbat_engine(user_query, sb),
            "tawil":    tawil_engine(user_query, sb),
            "istifsar": istifsar_engine(user_query, sb)
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
