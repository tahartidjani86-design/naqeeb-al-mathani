# -*- coding: utf-8 -*-
"""
نقيب المثاني - Vercel Serverless Function (FastAPI)
النسخة النهائية المراجعة — استنباط + تأويل + استفسار
"""

import re
import os
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# الخاتمة الثابتة كما نصّت عليها المنهجية
KHATIMA = "هذا والله أعلم، ويبقى الذكاء الاصطناعي قاصراً عن مزايا المدارك البشرية وكذلك يمكن أن يخطئ أحياناً، فإن وقع خطأ فهو في المبرمج وليس في المنهج."

# ============================================================
# قاموس الأروقة الثمانية — مثبّت كاملاً
# ============================================================
ARWIQA = {
    "الله":               {"martaba": "مرتبة ذات الاسم الجامع لاستواء اسم الذات واسماء الصفات واسماء الفعال", "rwaq": "رواق المنفردات", "bab": "أزلي أبدي", "rkn": "الحضرة العلية"},
    "الرحمن":             {"martaba": "منزلة صفات الاسم الجامع لاستواء اسماء الصفات", "rwaq": "رواق المنفردات", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الرحيم":             {"martaba": "وظيف فعال الاسم الجامع لاستواء اسماء الفعال", "rwaq": "رواق المنفردات", "bab": "قضاء وأقدار", "rkn": "الإحاطة والتكوين والعدل والإمداد الخاص والعام"},
    "مالك الملك":         {"martaba": "منزلة صفات الاسم الجامع لاستواء اسماء الأركان", "rwaq": "رواق المنفردات", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الملك":              {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "ذو الجلال والإكرام": {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الجليل":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "المجيد":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي", "rkn": "الملكية"},
    "الماجد":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أبدي", "rkn": "الملكية"},
    "العزيز":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "العظيم":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الكبير":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الواسع":             {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الغني":              {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "العلي":              {"martaba": "منزلة صفات", "rwaq": "رواق الكرسي", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الأول":              {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي", "rkn": "الملكية"},
    "الآخر":              {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أبدي", "rkn": "الملكية"},
    "الظاهر":             {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أبدي", "rkn": "الملكية"},
    "الباطن":             {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي", "rkn": "الملكية"},
    "النور":              {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الحي":               {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي", "rkn": "الملكية"},
    "الباقي":             {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أبدي", "rkn": "الملكية"},
    "الواحد":             {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "الصمد":              {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "القدوس":             {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "السلام":             {"martaba": "منزلة صفات", "rwaq": "رواق العرش", "bab": "أزلي أبدي", "rkn": "الملكية"},
    "العليم":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الحكيم":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الرقيب":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الشهيد":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "السميع":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "البصير":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "المحصي":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الخبير":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الصبور":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الرشيد":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "العدل":              {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الحكم":              {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الحق":               {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "المقسط":             {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "المتعال":            {"martaba": "وظيف فعال", "rwaq": "رواق المواثيق", "bab": "قضاء", "rkn": "الإحاطة"},
    "الخالق":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "البارئ":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المصور":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "الواجد":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "البديع":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المبدئ":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المعيد":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المحيي":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المميت":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "الباعث":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "الوارث":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "القادر":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المقتدر":            {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "الضار":              {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "المانع":             {"martaba": "وظيف فعال", "rwaq": "رواق النشأ", "bab": "قضاء", "rkn": "التكوين"},
    "الجامع":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المنتقم":            {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "القابض":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "الخافض":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المؤخر":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المقيت":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المذل":              {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "الجبار":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "القهار":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المهيمن":            {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المتكبر":            {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "القوي":              {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "المتين":             {"martaba": "وظيف فعال", "rwaq": "رواق النشر", "bab": "قضاء", "rkn": "العدل"},
    "الكريم":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الفتاح":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "المغني":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الرزاق":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الوهاب":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الباسط":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "القيوم":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "البر":               {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "المجيب":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "النافع":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الحفيظ":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "العفو":              {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "اللطيف":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الرؤوف":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "الحليم":             {"martaba": "وظيف فعال", "rwaq": "رواق التعميم", "bab": "أقدار", "rkn": "إمداد"},
    "المعز":              {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الرافع":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "المقدم":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الوال":              {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الغفار":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الغفور":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "التواب":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الودود":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الشكور":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الحميد":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الحسيب":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الولي":              {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الوكيل":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "الهادي":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
    "المؤمن":             {"martaba": "وظيف فعال", "rwaq": "رواق التخصيص", "bab": "أقدار", "rkn": "إمداد"},
}

# ============================================================
# قاموس التحلي والتخلي — كما نصّت عليه المنهجية
# ============================================================
TAHALLI_RULES = {
    "الله":               {"hukm": "لا يجوز", "say": "لا يقال إله"},
    "الرب":               {"hukm": "يجوز",    "say": "يقال رباني"},
    "الرحمن":             {"hukm": "يجوز",    "say": "ولا يقال رحمن"},
    "الرحيم":             {"hukm": "يجب",     "say": "يقال رحيم"},
    "مالك الملك":         {"hukm": "يجوز",    "say": "يقال مالك"},
    "الملك":              {"hukm": "يجوز",    "say": "يقال ملك"},
    "ذو الجلال والإكرام": {"hukm": "يجوز",    "say": "يقال جليل مكرم"},
    "الجليل":             {"hukm": "يجوز",    "say": "يقال جليل"},
    "المجيد":             {"hukm": "يجوز",    "say": "يقال مجيد"},
    "الماجد":             {"hukm": "يجوز",    "say": "يقال ماجد"},
    "العزيز":             {"hukm": "يجوز",    "say": "يقال عزيز"},
    "العظيم":             {"hukm": "يجوز",    "say": "يقال عظيم"},
    "الكبير":             {"hukm": "يجوز",    "say": "يقال كبير"},
    "الواسع":             {"hukm": "يجوز",    "say": "يقال واسع"},
    "الغني":              {"hukm": "يجوز",    "say": "يقال غني"},
    "العلي":              {"hukm": "يجوز",    "say": "يقال علي"},
    "الأول":              {"hukm": "يجوز",    "say": "يقال أول"},
    "الآخر":              {"hukm": "يجوز",    "say": "يقال آخر"},
    "الظاهر":             {"hukm": "يجوز",    "say": "يقال ظاهر"},
    "الباطن":             {"hukm": "يجوز",    "say": "يقال باطن"},
    "النور":              {"hukm": "يجوز",    "say": "يقال نور"},
    "الحي":               {"hukm": "يجب",     "say": "يقال حي"},
    "الباقي":             {"hukm": "يجوز",    "say": "يقال باقي"},
    "الواحد":             {"hukm": "يجوز",    "say": "يقال واحد"},
    "الصمد":              {"hukm": "لا يجوز", "say": "لا يقال صمد"},
    "القدوس":             {"hukm": "يجوز",    "say": "يقال مقدس"},
    "السلام":             {"hukm": "يجب",     "say": "يقال سلام"},
    "العليم":             {"hukm": "يجوز",    "say": "يقال عليم"},
    "الحكيم":             {"hukm": "يجوز",    "say": "يقال حكيم"},
    "الرقيب":             {"hukm": "يجوز",    "say": "يقال رقيب"},
    "الشهيد":             {"hukm": "يجوز",    "say": "يقال شهيد"},
    "السميع":             {"hukm": "يجوز",    "say": "يقال سميع"},
    "البصير":             {"hukm": "يجوز",    "say": "يقال بصير"},
    "المحصي":             {"hukm": "يجوز",    "say": "يقال محصي"},
    "الخبير":             {"hukm": "يجوز",    "say": "يقال خبير"},
    "الصبور":             {"hukm": "يجب",     "say": "يقال صبور"},
    "الرشيد":             {"hukm": "يجب",     "say": "يقال رشيد"},
    "العدل":              {"hukm": "يجب",     "say": "يقال عدل"},
    "الحكم":              {"hukm": "يجوز",    "say": "يقال حكم"},
    "الحق":               {"hukm": "يجب",     "say": "يقال حق"},
    "المقسط":             {"hukm": "يجوز",    "say": "يقال مقسط"},
    "المتعال":            {"hukm": "لا يجوز", "say": "لا يقال متعال"},
    "الخالق":             {"hukm": "يجوز",    "say": "يقال خالق"},
    "البارئ":             {"hukm": "يجوز",    "say": "يقال بارئ"},
    "المصور":             {"hukm": "يجوز",    "say": "يقال مصور"},
    "الواجد":             {"hukm": "يجوز",    "say": "يقال واجد"},
    "البديع":             {"hukm": "يجوز",    "say": "يقال بديع"},
    "المبدئ":             {"hukm": "يجوز",    "say": "يقال مبدئ"},
    "المعيد":             {"hukm": "يجوز",    "say": "يقال معيد"},
    "المحيي":             {"hukm": "يجوز",    "say": "يقال محيي"},
    "المميت":             {"hukm": "لا يجوز", "say": "لا يقال مميت"},
    "الباعث":             {"hukm": "لا يجوز", "say": "لا يقال باعث"},
    "الوارث":             {"hukm": "يجوز",    "say": "يقال وارث"},
    "القادر":             {"hukm": "يجوز",    "say": "يقال قادر"},
    "المقتدر":            {"hukm": "يجوز",    "say": "يقال مقتدر"},
    "الضار":              {"hukm": "يجوز",    "say": "يقال ضار"},
    "المانع":             {"hukm": "يجوز",    "say": "يقال مانع"},
    "الجامع":             {"hukm": "يجوز",    "say": "يقال جامع"},
    "المنتقم":            {"hukm": "يجوز",    "say": "يقال منتقم"},
    "القابض":             {"hukm": "يجوز",    "say": "يقال قابض"},
    "الخافض":             {"hukm": "يجوز",    "say": "يقال خافض"},
    "المؤخر":             {"hukm": "يجوز",    "say": "يقال مؤخر"},
    "المقيت":             {"hukm": "يجوز",    "say": "يقال مقيت"},
    "المذل":              {"hukm": "يجوز",    "say": "يقال مذل"},
    "الجبار":             {"hukm": "يجوز",    "say": "يقال جبار"},
    "القهار":             {"hukm": "يجوز",    "say": "يقال قهار"},
    "المهيمن":            {"hukm": "يجوز",    "say": "يقال مهيمن"},
    "المتكبر":            {"hukm": "لا يجوز", "say": "لا يقال متكبر"},
    "القوي":              {"hukm": "يجوز",    "say": "يقال قوي"},
    "المتين":             {"hukm": "يجوز",    "say": "يقال متين"},
    "الكريم":             {"hukm": "يجب",     "say": "يقال كريم"},
    "الفتاح":             {"hukm": "يجوز",    "say": "يقال فتاح"},
    "المغني":             {"hukm": "يجوز",    "say": "يقال مغني"},
    "الرزاق":             {"hukm": "يجوز",    "say": "يقال رزاق"},
    "الوهاب":             {"hukm": "يجوز",    "say": "يقال وهاب"},
    "الباسط":             {"hukm": "يجوز",    "say": "يقال باسط"},
    "القيوم":             {"hukm": "يجوز",    "say": "يقال قيوم"},
    "البر":               {"hukm": "يجب",     "say": "يقال بر"},
    "المجيب":             {"hukm": "يجوز",    "say": "يقال مجيب"},
    "النافع":             {"hukm": "يجوز",    "say": "يقال نافع"},
    "الحفيظ":             {"hukm": "يجب",     "say": "يقال حفيظ"},
    "العفو":              {"hukm": "يجوز",    "say": "يقال عفو"},
    "اللطيف":             {"hukm": "يجوز",    "say": "يقال لطيف"},
    "الرؤوف":             {"hukm": "يجب",     "say": "يقال رؤوف"},
    "الحليم":             {"hukm": "يجب",     "say": "يقال حليم"},
    "المعز":              {"hukm": "يجوز",    "say": "يقال معز"},
    "الرافع":             {"hukm": "يجوز",    "say": "يقال رافع"},
    "المقدم":             {"hukm": "يجوز",    "say": "يقال مقدم"},
    "الوال":              {"hukm": "يجب",     "say": "يقال وال"},
    "الغفار":             {"hukm": "يجوز",    "say": "يقال غفار"},
    "الغفور":             {"hukm": "يجوز",    "say": "يقال غفور"},
    "التواب":             {"hukm": "يجوز",    "say": "يقال تواب"},
    "الودود":             {"hukm": "يجب",     "say": "يقال ودود"},
    "الشكور":             {"hukm": "يجب",     "say": "يقال شكور"},
    "الحميد":             {"hukm": "يجب",     "say": "يقال حميد"},
    "الحسيب":             {"hukm": "يجوز",    "say": "يقال حسيب"},
    "الولي":              {"hukm": "يجوز",    "say": "يقال ولي"},
    "الوكيل":             {"hukm": "يجوز",    "say": "يقال وكيل"},
    "الهادي":             {"hukm": "يجوز",    "say": "يقال هادي"},
    "المؤمن":             {"hukm": "يجب",     "say": "يقال مؤمن"},
}

# ============================================================
# دوال مساعدة
# ============================================================
def clean(text):
    if not text: return ""
    text = re.sub(r"[\u064B-\u0652\u0670\u0656\u0657\u0615-\u061A\u06D6-\u06ED]", "", text)
    text = re.sub(r"[ٰٖٓٗٙٚۡۥۦ]", "", text)
    text = (text.replace("إ","ا").replace("أ","ا").replace("آ","ا")
                .replace("ة","ه").replace("ٱ","ا").replace("ى","ي")
                .replace("ئ","ي").replace("ؤ","و"))
    return " ".join(text.split())

def get_tahalli(name):
    nc = clean(name)
    for k, v in TAHALLI_RULES.items():
        if clean(k) == nc:
            return f"{v['hukm']} التحلي به — {v['say']}"
    return "لا يوجد حكم محدد"

def get_rwaq_info(name):
    nc = clean(name)
    for k, v in ARWIQA.items():
        if clean(k) == nc:
            return v
    return None

def get_special(name):
    """تمييز مشيئة الألوهية وشؤون الربوبية"""
    nc = clean(name)
    if any(w in nc for w in ['الله','اله','اللهم','الاهكم','لله']):
        return "مشيئة الألوهية"
    if any(w in nc for w in ['الرب','ربنا','ربكم','ربك','ربي','رب ']):
        return "شؤون الربوبية"
    return None

# ============================================================
# البحث في Supabase
# ============================================================
def search_quran(q, sb):
    """بحث في القرآن الكريم مع إظهار نص الآية"""
    try:
        resp = sb.table("quran").select("sura_num,aya_num,sura_name,text_uthmani").execute()
        qc = clean(q)
        words = [w for w in qc.split() if len(w) > 3]
        matches = []
        for row in resp.data:
            rc = clean(str(row.get("text_uthmani","")))
            score = sum(1 for w in words if w in rc)
            if score >= 1 or qc in rc:
                matches.append({
                    "sura_num":  row.get("sura_num",""),
                    "aya_num":   row.get("aya_num",""),
                    "sura_name": row.get("sura_name",""),
                    "text":      row.get("text_uthmani",""),
                    "score":     score
                })
        if matches:
            matches.sort(key=lambda x: x["score"], reverse=True)
            b = matches[0]
            return {
                "found":     True,
                "source":    "القرآن الكريم",
                "reference": f"سورة {b['sura_name']} ({b['sura_num']}) — الآية {b['aya_num']}",
                "text":      b["text"]
            }
    except: pass
    return {"found": False}

def clean_matn(text):
    """تنظيف المتن من سلسلة الإسناد وإبقاء نص الحديث"""
    if not text: return ""
    # حذف رقم الحديث في البداية
    text = re.sub(r'^["\d\s,]+', '', text).strip()
    # البحث عن بداية المتن بعد الإسناد
    markers = ['قال رسول الله', 'قال النبي', 'أن رسول الله', 'أن النبي',
               'عن النبي', 'سمعت رسول الله', 'سمعت النبي', 'يقول',
               'قال صلى الله عليه وسلم', 'قال:']
    best_pos = -1
    for m in markers:
        pos = text.find(m)
        if pos != -1 and (best_pos == -1 or pos < best_pos):
            best_pos = pos
    if best_pos > 0:
        return text[best_pos:].strip()
    return text.strip()

def search_hadith(q, sb):
    """البحث في الحديث مع ترتيب حسب الصلة وتنظيف المتن"""
    qc = clean(q)
    words = [w for w in qc.split() if len(w) > 3][:5]
    if not words:
        return []
    candidates = {}
    for word in words:
        try:
            resp = sb.table("hadith").select("text_ar,source")\
                .ilike("text_ar", f"%{word}%")\
                .limit(15).execute()
            for row in resp.data:
                txt = row.get("text_ar","")
                if not txt: continue
                key = txt[:80]
                if key not in candidates:
                    rc = clean(str(txt))
                    score = sum(1 for w in words if w in rc)
                    candidates[key] = {
                        "source": row.get("source", "حديث"),
                        "text":   clean_matn(str(txt))[:300],
                        "score":  score
                    }
        except: pass
    # ترتيب حسب أعلى صلة
    ranked = sorted(candidates.values(), key=lambda x: x["score"], reverse=True)
    return ranked[:3]

def search_book_ranked(table, q, sb, top=1):
    """بحث دقيق مرتّب حسب الصلة في كتاب معيّن"""
    qc = clean(q)
    words = [w for w in qc.split() if len(w) > 3]
    if not words: return []
    try:
        resp = sb.table(table).select("text_ar").execute()
        scored = []
        for row in resp.data:
            txt = str(row.get("text_ar",""))
            rc = clean(txt)
            # تطابق تام للجملة كاملة = أولوية قصوى
            if qc in rc:
                scored.append((100, txt))
                continue
            # عدد الكلمات المطابقة
            score = sum(1 for w in words if w in rc)
            if score >= 1:
                scored.append((score, txt))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [t[1][:450] for t in scored[:top]]
    except: pass
    return []

def search_manjam(q, sb):
    """التخريج من كتاب منجم الأصول حصراً"""
    res = search_book_ranked("manjam_al_usul", q, sb, top=1)
    return res[0] if res else ""

def search_idah(q, sb):
    """التخريج من كتاب الإيضاح المحايد حصراً"""
    res = search_book_ranked("idah_al_muhayid", q, sb, top=1)
    return res[0] if res else ""

# ============================================================
# محرك الاستنباط
# ============================================================
def classify_branch(text):
    t = clean(text)
    branches = []
    tashrii  = ['الصلاة','الزكاة','الصوم','الحج','الطهارة','الوضوء','الغسل','التيمم',
                'الجهاد','النكاح','الطلاق','القصاص','المواريث','الاسلام','المسلمون',
                'صلوا','اقيموا','ويقيمون','وآتوا','الزكاه']
    aqadi    = ['الإيمان','المؤمنون','آمنوا','يؤمنون','التوحيد','الله','الرسل','الأنبياء',
                'الملائكه','الجنه','النار','القضاء','القدر','كفر','شرك','الغيب',
                'يشاء','المشيئه','الرب','ربكم','ربنا','ربي','امنوا']
    muamalati= ['الإحسان','المحسن','التقوى','البر','السخاء','الإنفاق','النصيحه',
                'الصدق','الاخلاق','معروف','منكر','ينفقون','رزقناهم','والانفاق']
    if any(k in t for k in tashrii):    branches.append("فرع تشريعي — فرع الإسلام")
    if any(k in t for k in aqadi):      branches.append("فرع عقائدي — فرع الإيمان")
    if any(k in t for k in muamalati):  branches.append("فرع معاملاتي — فرع الإحسان")
    return branches or ["فرع تشريعي — فرع الإسلام"]

def extract_shuba(text, branches):
    t = clean(text)
    shuba_map = {
        'الصلاة':'الصلاة وأحكامها','الزكاة':'الزكاة والصدقات',
        'الصوم':'الصوم وأحكامه','الحج':'الحج والعمرة',
        'الطهارة':'الطهارة والوضوء','الجهاد':'الجهاد والرباط',
        'النكاح':'النكاح وأحكامه','الطلاق':'الطلاق والفرقة',
        'الإيمان':'الإيمان وأصوله','التوحيد':'التوحيد ونفي الشرك',
        'الغيب':'الإيمان بالغيب','الإنفاق':'الإنفاق في سبيل الله',
        'التقوى':'التقوى والإحسان','الأخلاق':'الأخلاق والآداب',
        'الجهاد':'الجهاد والرباط','القصاص':'القصاص والحدود',
        'المواريث':'المواريث والفرائض'
    }
    for k, v in shuba_map.items():
        if k in t: return v
    if 'عقائدي' in str(branches): return 'العقيدة والتوحيد'
    if 'تشريعي' in str(branches): return 'الأحكام التشريعية'
    return 'المحور العام'

def classify_dabit(text, asl_source):
    """تعيين الضابط مع التعليل — لماذا اختاره النظام"""
    t = clean(text)
    dabits = []
    reasons = []
    cmd = ['افعلوا','اقيموا','اتوا','اطيعوا','أمر','كتب','فرض','أوجب','يجب','صلوا','آتوا','ارجعوا']
    prh = ['نهي','حرم','لا تقربوا','لا تفعلوا','لا يحل','لا تقتلوا']
    mujmal   = ['لا يكلف','الا وسعها','مجمل','مبهم','لا يكلف الله']
    mutafawit= ['أولي الأمر','يرجح','متفاوت','اطيعوا']
    asma_list = list(ARWIQA.keys())
    has_asma  = any(clean(a) in t for a in asma_list)
    has_cmd   = any(k in t for k in cmd)
    has_prh   = any(k in t for k in prh)

    # كشف الكلمة المسببة لتضمينها في التعليل
    def found_kw(kws):
        for k in kws:
            if k in t: return k
        return ""

    if found_kw(mujmal):
        dabits.append("لفظ مجمل")
        reasons.append(f"الضابط «لفظ مجمل»: لاحتواء النص على صيغة إجمال (مثل «{found_kw(mujmal)}»)، والمجمل حكمه الجواز كما في المنهجية.")
    elif found_kw(mutafawit) and not has_cmd:
        dabits.append("لفظ متفاوت")
        reasons.append(f"الضابط «لفظ متفاوت»: لورود صيغة تحتمل أكثر من معنى (مثل «{found_kw(mutafawit)}»)، فيُرجَّح المعنى الأنسب وحكمه الجواز.")
    elif has_asma or has_cmd or has_prh:
        dabits.append("لفظ محكم")
        if has_cmd:
            reasons.append(f"الضابط «لفظ محكم»: لاحتواء النص على أمر صريح (مثل «{found_kw(cmd)}»). والمحكم من الكتاب أمره واجب، ومن السنة أمره مندوب.")
        elif has_prh:
            reasons.append(f"الضابط «لفظ محكم»: لاحتواء النص على نهي صريح (مثل «{found_kw(prh)}»). والمحكم من الكتاب نهيه واجب الاجتناب، ومن السنة يُجتنب.")
        else:
            reasons.append("الضابط «لفظ محكم»: لورود اسم من أسماء الله الحسنى المحكمة في الدلالة، وإن لم يكن فيه أمر ولا نهي فالنص لا يحمل حكماً.")

    if found_kw(['قياس','علة','شبه']):
        dabits.append("القياس")
        reasons.append("الضابط «القياس»: لاحتواء النص على إشارة للقياس. فإن كان قياس شبه فحكمه واجب أو جائز أو مستحيل، وإن كان قياس علة فحكمه الآداء أو القضاء أو الإعادة أو الرخصة أو العزيمة.")
    if found_kw(['أجمع','إجماع','اتفق','السلف','الصحابه']):
        dabits.append("الإجماع")
        reasons.append("الضابط «الإجماع»: لورود ما يدل على اتفاق. وحكمه الوجوب سواء كان إجماعاً من نصوص الكتاب أو عن السلف من الصحابة.")
    if found_kw(['نسخ','ناسخ','منسوخ']):
        dabits.append("النسخ")
        reasons.append("الضابط «النسخ»: لورود ما يدل على نسخ حكم سابق. وحكمه واجب كما في المنهجية.")
    if found_kw(['فعل النبي','تحنيك','رفع اليدين','قلب العبائه']):
        dabits.append("الفعل")
        reasons.append("الضابط «الفعل»: لاحتواء النص على فعل نبوي. فالفعل المستقل حكمه الاستحباب، والمجمل بواجب حكمه واجب، والمجمل بمندوب حكمه المندوب.")
    if found_kw(['أقر','إقرار','سكت عن']):
        dabits.append("الإقرار")
        reasons.append("الضابط «الإقرار»: لورود ما يدل على إقرار النبي ﷺ. وحكمه الجواز سواء كان من الكتاب أو من السنة.")
    if found_kw(['سبب','سببيه','بسبب']):
        dabits.append("السبب")
        reasons.append("الضابط «السبب»: لورود ما يدل على سبب. وحكمه واجب كما في المنهجية.")

    if not dabits:
        dabits = ["لفظ متفاوت"]
        reasons.append("الضابط «لفظ متفاوت»: لعدم ورود صيغة محكمة أو مجملة صريحة، فيُرجَّح المعنى الأنسب وحكمه الجواز.")

    return dabits, reasons

def extract_hukm_nazari(text, dabits, branches, asl_source):
    t = clean(text)
    ds = " ".join(dabits)
    cmd = ['افعلوا','اقيموا','اتوا','اطيعوا','أمر','كتب','فرض','أوجب','يجب','صلوا','آتوا','ارجعوا']
    prh = ['نهي','حرم','لا تقربوا','لا تفعلوا','لا يحل']
    has_cmd = any(k in t for k in cmd)
    has_prh = any(k in t for k in prh)

    if "الإقرار" in ds: return "جائز"
    if "لفظ محكم" in ds:
        if asl_source == "الكتاب":
            if has_cmd: return "واجب"
            if has_prh: return "مستحيل"
            return "النص لا يحمل حكماً"
        if asl_source == "السنة":
            if has_cmd: return "مندوب"
            if has_prh: return "يُجتنب"
            return "النص لا يحمل حكماً"
    if "لفظ مجمل" in ds: return "جائز"
    if "لفظ متفاوت" in ds: return "جائز"
    if "القياس" in ds and "عله" not in t and "علة" not in t:
        if has_cmd: return "واجب"
        if has_prh: return "مستحيل"
        return "جائز"
    if "الإجماع" in ds: return "واجب"
    if "النسخ" in ds: return "واجب"
    if "السبب" in ds: return "واجب"
    return "النص لا يحمل حكماً"

def extract_hukm_darori(text, nazari, dabits, branches, asl_source):
    t = clean(text)
    ds = " ".join(dabits)
    if nazari == "النص لا يحمل حكماً": return "النص لا يحمل حكماً"
    if "القياس" in ds and ("عله" in t or "علة" in t):
        if any(k in t for k in ['آداء','اداء','أداء']): return "الآداء"
        if 'قضاء' in t: return "القضاء"
        if 'إعاده' in t or 'اعاده' in t: return "الإعادة"
        if any(k in t for k in ['رخصه','رخصة']): return "الرخصة"
        return "العزيمة"
    if "الفعل" in ds:
        if nazari == "واجب": return "واجب"
        if nazari == "مندوب": return "مندوب عيني"
        return "مستحب"
    if "لفظ محكم" in ds:
        if nazari == "واجب":
            return "فرض عين" if "عقائدي" in str(branches) or "تشريعي" in str(branches) else "فرض كفاية"
        if nazari == "مستحيل": return "حرام"
        if nazari == "مندوب":  return "مندوب عيني"
        if nazari == "يُجتنب": return "مكروه"
    if "لفظ مجمل" in ds or "لفظ متفاوت" in ds: return "مباح"
    if "الإجماع" in ds: return "فرض كفاية"
    if "النسخ" in ds or "السبب" in ds: return "فرض عين"
    return "مباح"

def istinbat_engine(q, sb):
    """محرك الاستنباط — المنهجية الكاملة"""
    quran  = search_quran(q, sb)
    hadith = search_hadith(q, sb)

    # ١. الأصل
    if quran["found"]:
        asl        = "وحي"
        asl_source = "الكتاب"
        usul       = ["الكتاب"]
        nass       = quran["text"]
        ref        = quran["reference"]
        if hadith: usul.append("السنة")
    elif hadith:
        asl        = "وحي"
        asl_source = "السنة"
        usul       = ["السنة"]
        nass       = hadith[0]["text"]
        ref        = hadith[0]["source"]
    else:
        asl        = "ليس وحياً مباشراً في قاعدة البيانات"
        asl_source = "غير وحي"
        usul       = ["—"]
        nass       = ""
        ref        = "—"

    # ٢. الأصول — إظهار نص الآية أو راوي الحديث
    usul_text = " و ".join(usul)
    nass_display = f"\n{nass[:200]}" if nass else ""

    # ٣. الفروع والشعبة
    branches = classify_branch(q)
    shuba    = extract_shuba(q, branches)

    # ٤. الضابط والأحكام (مع التعليل)
    dabits, dabit_reasons = classify_dabit(q, asl_source)
    nazari  = extract_hukm_nazari(q, dabits, branches, asl_source)
    darori  = extract_hukm_darori(q, nazari, dabits, branches, asl_source)

    # تعليل الأحكام
    hukm_reason = ""
    if nazari == "واجب":
        hukm_reason = "الحكم النظري «واجب» لأن النص محكم من الكتاب فيه أمر صريح."
    elif nazari == "مندوب":
        hukm_reason = "الحكم النظري «مندوب» لأن النص محكم من السنة فيه أمر."
    elif nazari == "مستحيل":
        hukm_reason = "الحكم النظري «مستحيل» (أي نهي) لورود النهي الصريح في النص."
    elif nazari == "جائز":
        hukm_reason = "الحكم النظري «جائز» لأن الضابط مجمل أو متفاوت يحتمل المعاني."
    elif nazari == "النص لا يحمل حكماً":
        hukm_reason = "النص محكم لكن ليس فيه أمر ولا نهي ولا جواز، فلا يحمل حكماً."

    # ٥. الأحاديث المتصلة
    hadith_display = ""
    if hadith:
        hadith_display = "أحاديث متصلة:\n"
        for h in hadith:
            hadith_display += f"• {h['source']}: {h['text'][:150]}...\n"

    # ٦. التخريج — من المنجم والإيضاح حصراً
    takhreej_manjam = search_manjam(q, sb)
    takhreej_idah   = search_idah(q, sb)
    takhreej = ""
    if takhreej_manjam:
        takhreej += f"• من كتاب منجم الأصول:\n{takhreej_manjam}\n\n"
    if takhreej_idah:
        takhreej += f"• من كتاب الإيضاح المحايد:\n{takhreej_idah}\n"
    if not takhreej:
        takhreej = "لم توجد مطابقات في المصدرين المعتمدَين (منجم الأصول / الإيضاح المحايد)"

    return {
        "الأصل":              asl,
        "الأصول":             f"{usul_text}{nass_display}\nالمرجع: {ref}",
        "الفروع":             branches,
        "الشعبة":             shuba,
        "الضابط":             dabits,
        "تعليل_الضابط":       dabit_reasons,
        "الحكم_النظري":       nazari,
        "تعليل_الحكم":        hukm_reason,
        "الحكم_الضروري":      darori,
        "الأحاديث_المتصلة":   hadith_display or "لم توجد أحاديث مرتبطة في قاعدة البيانات",
        "التخريج":            takhreej,
        "خاتمة":              KHATIMA
    }

# ============================================================
# محرك التأويل
# ============================================================
def tawil_engine(q, sb):
    """محرك التأويل — الأروقة الثمانية + التحلي/التخلي"""
    qc = clean(q)
    all_names = {clean(k): k for k in ARWIQA.keys()}
    detected = []
    seen = set()

    def add(name_orig):
        nc = clean(name_orig)
        if nc in seen: return
        seen.add(nc)
        rwaq = get_rwaq_info(name_orig)
        if rwaq:
            entry = {
                "الاسم":              name_orig,
                "المرتبة":            rwaq["martaba"],
                "الرواق":             rwaq["rwaq"],
                "الباب":              rwaq["bab"],
                "الركن":              rwaq["rkn"],
                "حكم_التحلي_التخلي": get_tahalli(name_orig),
            }
            sp = get_special(name_orig)
            if sp: entry["ملاحظة_خاصة"] = sp
            detected.append(entry)

    # بحث في كل كلمة
    for word in qc.split():
        if word in all_names: add(all_names[word])
    # بحث في النص كاملاً
    for nc, orig in all_names.items():
        if nc in qc: add(orig)
    # الله والرب بأشكالهما المختلفة
    if any(x in qc for x in ['الله','اله','اللهم','لله','الاهكم']): add('الله')
    if any(x in qc for x in ['الرب','ربنا','ربكم','ربي','رب ']): add('الرب')

    if not detected:
        return {
            "الأسماء_المكتشفة": [],
            "التأويل": "لم يُكتشف اسم من أسماء الله الحسنى في النص المدخل",
            "خاتمة": KHATIMA
        }
    return {
        "الأسماء_المكتشفة": [d["الاسم"] for d in detected],
        "التأويل": detected,
        "خاتمة": KHATIMA
    }

# ============================================================
# محرك الاستفسار
# ============================================================
def istifsar_engine(q, sb):
    """محرك الاستفسار — الإجابة من المنجم والإيضاح حصراً، مرتّبة حسب الصلة"""
    answers = []

    # أفضل نتيجتين من منجم الأصول
    manjam_results = search_book_ranked("manjam_al_usul", q, sb, top=2)
    for txt in manjam_results:
        answers.append({"المصدر": "كتاب منجم الأصول", "النص": txt})

    # أفضل نتيجتين من الإيضاح المحايد
    idah_results = search_book_ranked("idah_al_muhayid", q, sb, top=2)
    for txt in idah_results:
        answers.append({"المصدر": "كتاب الإيضاح المحايد", "النص": txt})

    if not answers:
        answers.append({
            "المصدر": "تنبيه",
            "النص": (
                "السؤال خارج عن منهجيتي، أو لم توجد إجابة مباشرة في "
                "كتاب منجم الأصول أو كتاب الإيضاح المحايد.\n"
                "يمكنك إعادة صياغة سؤالك بكلمات مفتاحية يتناولها المؤلف في الكتابين."
            )
        })
    return {"الإجابات": answers, "خاتمة": KHATIMA}

# ============================================================
# الدالة الرئيسية
# ============================================================
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
            "query":    user_query,
            "استنباط": istinbat_engine(user_query, sb),
            "تأويل":   tawil_engine(user_query, sb),
            "استفسار": istifsar_engine(user_query, sb)
        })
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
