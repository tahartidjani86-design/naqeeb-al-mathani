# -*- coding: utf-8 -*-
"""
نقيب المثاني - Vercel Serverless Function (FastAPI)
المنهجية الكاملة: استنباط + تأويل + استفسار
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

KHATIMA = "\n\nهذا والله أعلم، ويبقى الذكاء الاصطناعي قاصراً عن مزايا مدارك البشر وقد يخطئ."

# ============================================================
# قاموس الأروقة الثمانية — مثبّت في الكود كاملاً
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
# قاموس التحلي والتخلي
# ============================================================
TAHALLI_RULES = {
    "الله":               {"hukm": "لا يجوز", "say": "لا يقال إله"},
    "الرب":               {"hukm": "يجوز",    "say": "يقال رباني"},
    "الرحمن":             {"hukm": "يجوز",    "say": "لا يقال رحمن"},
    "الرحيم":             {"hukm": "يجب",     "say": "يقال رحيم"},
    "مالك الملك":         {"hukm": "يجوز",    "say": "يقال مالك"},
    "الملك":              {"hukm": "يجوز",    "say": "يقال ملك"},
    "ذو الجلال والإكرام": {"hukm": "يجوز",    "say": "يقال جليل كريم"},
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
    "القدوس":             {"hukm": "يجوز",    "say": "يقال قدوس"},
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
    nc = clean(name)
    if any(w in nc for w in ['الله','اله','اللهم']): return "مشيئة الألوهية"
    if any(w in nc for w in ['الرب','ربنا','ربكم','ربي','رب']): return "شؤون الربوبية"
    return None

# ============================================================
# البحث في Supabase
# ============================================================
def search_quran(q, sb):
    """بحث جزئي في القرآن الكريم"""
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
            return {"found": True, "source": "القرآن الكريم",
                    "reference": f"سورة {b['sura_name']} ({b['sura_num']}) — الآية {b['aya_num']}",
                    "text": b["text"]}
    except: pass
    return {"found": False}

def search_hadith(q, sb):
    """البحث في أحاديث الجداول المتاحة"""
    hadith_tables = ["hadith", "seerah_halabiyya", "seerah_ibn_hish", "seerah_tashrii"]
    qc = clean(q)
    words = [w for w in qc.split() if len(w) > 3][:5]
    results = []
    for table in hadith_tables:
        try:
            resp = sb.table(table).selresp = sb.table(table).select("text_ar,source").limit(300).execute()ect("text,source").limit(300).execute()
            for row in resp.data:
                rc = clean(str(row.get("text","")))
                score = sum(1 for w in words if w in rc)
                if score >= 2:
                    results.append({"source": row.get("source", table),
                                    "text": str(row.get("text",""))[:200], "score": score})
        except: pass
    results.sort(key=lambda x: x["score"], reverse=True)
    return results[:3]

def search_manjam(q, sb):
    try:
        resp = sb.table("manjam_al_usul").select("text_ar").execute()
        qc = clean(q)
        for row in resp.data:
            if qc in clean(str(row.get("text_ar",""))):
                return str(row.get("text_ar",""))[:300]
    except: pass
    return ""

def search_idah(q, sb):
    try:
        resp = sb.table("idah_al_muhayid").select("text_ar").execute()
        qc = clean(q)
        for row in resp.data:
            if qc in clean(str(row.get("text_ar",""))):
                return str(row.get("text_ar",""))[:300]
    except: pass
    return ""

# ============================================================
# محرك الاستنباط
# ============================================================
def classify_branch(text):
    t = clean(text)
    branches = []
    tashrii  = ['الصلاة','الزكاة','الصوم','الحج','الطهارة','الوضوء','الغسل','التيمم',
                'الجهاد','النكاح','الطلاق','القصاص','المواريث','الاسلام','المسلمون',
                'صلوا','اقيموا','ويقيمون','الجمعه','الحج']
    aqadi    = ['الإيمان','المؤمنون','آمنوا','يؤمنون','التوحيد','الله','الرسل','الأنبياء',
                'الملائكة','الجنه','النار','القضاء','القدر','كفر','شرك','الغيب',
                'يشاء','المشيئه','الرب','ربكم','ربنا','ربي']
    muamalati= ['الإحسان','المحسن','التقوى','البر','السخاء','الإنفاق','النصيحه',
                'الصدق','الأخلاق','معروف','منكر','ينفقون','رزقناهم']
    if any(k in t for k in tashrii):    branches.append("فرع تشريعي — فرع الإسلام")
    if any(k in t for k in aqadi):      branches.append("فرع عقائدي — فرع الإيمان")
    if any(k in t for k in muamalati):  branches.append("فرع معاملاتي — فرع الإحسان")
    return branches or ["فرع تشريعي — فرع الإسلام"]

def extract_shuba(text, branches):
    t = clean(text)
    shuba_map = {'الصلاة':'الصلاة وأحكامها','الزكاة':'الزكاة والصدقات',
                 'الصوم':'الصوم وأحكامه','الحج':'الحج والعمرة',
                 'الطهارة':'الطهارة والوضوء','الجهاد':'الجهاد والرباط',
                 'النكاح':'النكاح وأحكامه','الطلاق':'الطلاق والفرقة',
                 'الإيمان':'الإيمان وأصوله','التوحيد':'التوحيد ونفي الشرك',
                 'الغيب':'الإيمان بالغيب','الإنفاق':'الإنفاق في سبيل الله',
                 'التقوى':'التقوى والإحسان','الأخلاق':'الأخلاق والآداب'}
    for k, v in shuba_map.items():
        if k in t: return v
    if 'عقائدي' in str(branches): return 'العقيدة والتوحيد'
    if 'تشريعي' in str(branches): return 'الأحكام التشريعية'
    return 'المحور العام'

def classify_dabit(text, asl_source):
    t = clean(text)
    dabits = []
    cmd = ['افعلوا','اقيموا','اتوا','اطيعوا','أمر','كتب','فرض','أوجب','لابد',
           'يجب','يلزم','صلوا','آتوا','ارجعوا','انشزوا','تفسحوا']
    prh = ['نهي','حرم','لا تقربوا','لا تفعلوا','لا يحل','لا تقتلوا']
    mujmal   = ['لا يكلف','الا وسعها','مجمل','مبهم']
    mutafawit= ['أولي الأمر','يرجح','متفاوت']
    asma = list(ARWIQA.keys())
    has_asma = any(clean(a) in t for a in asma)
    has_cmd  = any(k in t for k in cmd)
    has_prh  = any(k in t for k in prh)
    if has_asma or has_cmd or has_prh:
        if any(k in t for k in mujmal): dabits.append("لفظ مجمل")
        elif any(k in t for k in mutafawit): dabits.append("لفظ متفاوت")
        else: dabits.append("لفظ محكم")
    if any(k in t for k in ['قياس','علة','شبه']): dabits.append("القياس")
    if any(k in t for k in ['أجمع','إجماع','اتفق','السلف','الصحابه']): dabits.append("الإجماع")
    if any(k in t for k in ['نسخ','ناسخ','منسوخ']): dabits.append("النسخ")
    if any(k in t for k in ['فعل النبي','تحنيك','رفع اليدين']): dabits.append("الفعل")
    if any(k in t for k in ['أقر','إقرار','سكت عن']): dabits.append("الإقرار")
    if any(k in t for k in ['سبب','سببيه','بسبب']): dabits.append("السبب")
    return dabits or ["لفظ متفاوت"]

def extract_hukm_nazari(text, dabits, branches, asl_source):
    t = clean(text)
    ds = " ".join(dabits)
    cmd = ['افعلوا','اقيموا','اتوا','اطيعوا','أمر','كتب','فرض','أوجب','يجب','صلوا','آتوا']
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
        return "واجب" if nazari == "واجب" else "مستحب"
    if "لفظ محكم" in ds:
        if nazari == "واجب":
            return "فرض عين" if "عقائدي" in str(branches) else "فرض عين"
        if nazari == "مستحيل": return "حرام"
        if nazari == "مندوب":  return "مندوب عيني"
        if nazari == "يُجتنب": return "مكروه"
    if "لفظ مجمل" in ds or "لفظ متفاوت" in ds: return "مباح"
    if "الإجماع" in ds: return "فرض كفاية"
    if "النسخ" in ds or "السبب" in ds: return "فرض عين"
    return "مباح"

def istinbat_engine(q, sb):
    quran = search_quran(q, sb)
    hadith = search_hadith(q, sb)
    if quran["found"]:
        asl = f"وحي — {quran['source']} | {quran['reference']}"
        asl_source = "الكتاب"
        usul = ["الكتاب"]
        if hadith: usul.append("السنة")
    elif hadith:
        asl = f"وحي — السنة النبوية | {hadith[0]['source']}"
        asl_source = "السنة"
        usul = ["السنة"]
    else:
        asl = "ليس وحياً مباشراً في قاعدة البيانات"
        asl_source = "غير وحي"
        usul = ["—"]
    branches = classify_branch(q)
    shuba    = extract_shuba(q, branches)
    dabits   = classify_dabit(q, asl_source)
    nazari   = extract_hukm_nazari(q, dabits, branches, asl_source)
    darori   = extract_hukm_darori(q, nazari, dabits, branches, asl_source)
    hadith_txt = ""
    if hadith:
        hadith_txt = "أحاديث متصلة:\n" + "\n".join(f"• {h['source']}: {h['text'][:120]}..." for h in hadith)
    return {
        "الأصل":              asl,
        "الأصول":             " و ".join(usul),
        "الفروع":             branches,
        "الشعبة":             shuba,
        "الضابط":             dabits,
        "الحكم_النظري":       nazari,
        "الحكم_الضروري":      darori,
        "الأحاديث_المتصلة":   hadith_txt or "لم توجد أحاديث مرتبطة في قاعدة البيانات",
        "خاتمة":              KHATIMA
    }

# ============================================================
# محرك التأويل
# ============================================================
def tawil_engine(q, sb):
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
    # الله والرب بأشكالهما
    if any(x in qc for x in ['الله','اله','اللهم']): add('الله')
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
    manjam = search_manjam(q, sb)
    idah   = search_idah(q, sb)
    answers = []
    if manjam: answers.append({"المصدر": "كتاب منجم الأصول",    "النص": manjam})
    if idah:   answers.append({"المصدر": "كتاب الإيضاح المحايد", "النص": idah})
    if not answers:
        answers.append({"المصدر": "منهجية نقيب المثاني", "النص": (
            "نقيب المثاني نظام للاستنباط والتأويل مبني على منهجية كتابَي «منجم الأصول» "
            "و«الإيضاح المحايد» للعلامة محمد الطاهر المدني التجاني. "
            "يتكون من ثلاثة محركات: الاستنباط (الأصل والأصول والفروع والشعبة والضابط والأحكام)، "
            "والتأويل (الأسماء الحسنى والأروقة الثمانية وأحكام التحلي والتخلي)، "
            "والاستفسار (الإجابة من المصادر المعتمدة فقط). "
            "إذا كان سؤالك خارجاً عن هذه المنهجية فالإجابة: السؤال خارج عن منهجيتي."
        )})
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
