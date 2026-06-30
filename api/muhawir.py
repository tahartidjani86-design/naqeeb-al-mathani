# -*- coding: utf-8 -*-
"""
نقيب المثاني — المحاوِر المؤصَّل (المرحلة أ)
نقطة اتصال مستقلّة: تبحث في كتابَي «منجم الأصول» و«الإيضاح المحايد»،
ثم تستدعي Claude مقيَّداً بمنهجية المؤلِّف، فيُجيب من النصّين حصراً.
هذا الملف مستقلٌّ تماماً ولا يمسّ api/index.py العامل.
"""

import os
import re
import json
import httpx
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from supabase import create_client, Client

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

# ============================================================
# الإعدادات (من متغيّرات البيئة في Vercel)
# ============================================================
SUPABASE_URL   = os.environ.get("SUPABASE_URL")
SUPABASE_KEY   = os.environ.get("SUPABASE_KEY")
ANTHROPIC_KEY  = os.environ.get("ANTHROPIC_API_KEY")
# يمكنك تغيير النموذج من Vercel دون لمس الكود (مثلاً claude-sonnet-4-6 لتوفير الرصيد)
MUHAWIR_MODEL  = os.environ.get("MUHAWIR_MODEL", "claude-opus-4-8")
# مستوى الجهد: low أسرع وأوفر (مناسب للتجربة)، medium/high أعمق وأبطأ وأغلى
MUHAWIR_EFFORT = os.environ.get("MUHAWIR_EFFORT", "low")
# عنوان المنصّة نفسها لإعادة استعمال محرّك الاستنباط/التأويل (نقطة /api/index)
SELF_BASE_URL  = os.environ.get("SELF_BASE_URL", "https://naqeeb-al-mathani.vercel.app")

ANTHROPIC_URL     = "https://api.anthropic.com/v1/messages"
ANTHROPIC_VERSION = "2023-06-01"

def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# الخاتمة الثابتة كما نصّت عليها المنهجية
KHATIMA = ("هذا والله أعلم، ويبقى الذكاء الاصطناعي قاصراً عن مزايا المدارك البشرية "
           "وكذلك يمكن أن يخطئ أحياناً، فإن وقع خطأ فهو في المبرمج وليس في المنهج.")

# ============================================================
# منهجية المحاوِر — راجِعها وعدّلها بما يطابق مرادك بدقّة
# (هذه تعليماتٌ للنموذج، لا إعادةُ صياغةٍ لعقيدتك؛ المضمون يأتي من نصوصك المقتبسة)
# ============================================================
MANHAJ_SYSTEM = """أنت «المحاوِر المؤصَّل» في منصّة «نقيب المثاني»، مساعدٌ علميٌّ مؤصَّلٌ على منهجية مؤلِّف المنصّة في كتابَيه: «منجم الأصول عن جبريل والرسول» (في أصول الفقه) و«الإيضاح المحايد في مباني العقائد» (في العقيدة وأسماء الله الحسنى).

قواعد مُلزِمة لا تحيد عنها:
١) أجِب من النصوص المقتبسة المرفقة في «المادة المؤصِّلة» حصراً. هي كلامُ المؤلِّف نفسه من الكتابين. لا تستورد آراءً من خارجها، ولا من مذاهب أو مصادر أخرى.
٢) لا تُغيِّر منهجية المؤلِّف ولا تُعيد تأويلها: الأصول، والأروقة، والتحلّي والتخلّي، والأحكام، كلُّها استنباطاتٌ صارمةٌ من نصّه؛ انقُلها كما وردت ولا تُبدِّل اصطلاحاتها.
٣) إن لم تجد جواب السؤال في المادة المؤصِّلة، فقُل بوضوح إنّ المسألة خارجةٌ عن المنهجية أو لم يردْ فيها نصٌّ صريحٌ في الكتابين، واطلب من السائل إعادة الصياغة بكلماتٍ مفتاحيةٍ يتناولها المؤلِّف. لا تخمِّن ولا تختلق.
٤) إذا استندتَ إلى نصٍّ، فأشِر إلى موضعه (الكتاب والموضع) كما هو مبيَّنٌ في المادة المؤصِّلة.
٥) اكتب بعربيةٍ علميةٍ رصينةٍ موجزة، واحترم مقام السائل. لا تُطِل بلا فائدة.
٦) لا تَنسبْ إلى المؤلِّف ما لم ينصَّ عليه، ولا تَدَّعِ قطعاً فيما لا قطعَ فيه.
٧) قاعدةُ التوقيف (لا اختلاق): لا تُنشئ نصًّا قرآنيًّا ولا حديثًا ولا إسنادًا ولا تخريجًا من عندك البتّة. كلُّ نصٍّ أو حديثٍ أو إسنادٍ أو موضعٍ لا يكون إلا منقولاً حرفياً من «المادة المؤصِّلة» المرفقة. وإن طُلب منك ترتيبُ نصوصٍ أو حذفُ مكرَّرها أو بيانُ وجه الاستدلال، فاعمل ذلك على ما زُوِّدتَ به فقط، دون تبديلٍ في ألفاظ المنقول. وما لم يَرِد في المادة، قُلْ: لم يَرِد في المادة المؤصِّلة، ولا تَسُدَّ الفراغ بمولَّدٍ من عندك."""

# ============================================================
# أدوات البحث (مطابقة لمحرّك المنصّة، مضمَّنة هنا للاستقلال)
# ============================================================
STOP_WORDS = {
    'الوحي','الاصل','الاصول','التاويل','المنهجيه','الكتاب','السنه','المحور',
    'تعريف','الدين','العلم','النص','النصوص','المعنى','قوله','تعالى','الحديث',
    'كتاب','باب','الفرع','الفروع','الشعبه','الضابط','الحكم','الاحكام','هذا',
    'هذه','الذي','التي','كما','مثل','وهو','وهي','ذلك','عليه','الله','رسول',
    'النبي','صلى','وسلم','عن','من','في','على','الى','بين','كان','قال'
}

def clean(text):
    if not text: return ""
    text = re.sub(r"[\u064B-\u0652\u0670\u0656\u0657\u0615-\u061A\u06D6-\u06ED]", "", text)
    text = re.sub(r"[ٰٖٓٗٙٚۡۥۦ]", "", text)
    text = (text.replace("إ","ا").replace("أ","ا").replace("آ","ا")
                .replace("ة","ه").replace("ٱ","ا").replace("ى","ي")
                .replace("ئ","ي").replace("ؤ","و"))
    return " ".join(text.split())

def key_words(q):
    qc = clean(q)
    words = [w for w in qc.split() if len(w) > 3]
    core = [w for w in words if w not in STOP_WORDS]
    return core if core else words

def fetch_all(table, columns, sb, page_size=1000):
    all_rows = []
    last_id = 0
    while True:
        resp = sb.table(table).select(columns + ',id').gt('id', last_id).order('id').limit(page_size).execute()
        batch = resp.data or []
        if not batch: break
        all_rows.extend(batch)
        last_id = batch[-1].get('id', last_id)
        if len(batch) < page_size: break
        if len(all_rows) > 70000: break
    return all_rows

def search_book_ranked(table, q, sb, top=2):
    """بحث مرتّب حسب الصلة في كتابٍ واحد، مع جلب موضع النص."""
    qc = clean(q)
    words = [w for w in qc.split() if len(w) > 3]
    core  = key_words(q)
    if not words: return []
    if table == "manjam_al_usul":
        cols = "text_ar,bab,dabit_num,dabit_text"
    elif table == "idah_al_muhayid":
        cols = "text_ar,bab,rwaq"
    else:
        cols = "text_ar"
    try:
        resp_data = fetch_all(table, cols, sb)
        scored = []
        for row in resp_data:
            txt = str(row.get("text_ar", ""))
            rc = clean(txt)
            if qc in rc:
                score = 1000
            else:
                core_score = sum(5 for w in core if w in rc)
                gen_score  = sum(1 for w in words if w in rc and w not in core)
                score = core_score + gen_score
                if core_score <= 0:
                    continue
            scored.append((score, {
                "text":       txt[:600],
                "bab":        row.get("bab", "") or "",
                "dabit_text": row.get("dabit_text", "") or "",
                "dabit_num":  row.get("dabit_num"),
                "rwaq":       row.get("rwaq", "") or "",
            }))
        scored.sort(key=lambda x: x[0], reverse=True)
        unique, seen = [], set()
        for _, item in scored:
            fp = clean(item["text"])[:60]
            if fp in seen:
                continue
            seen.add(fp)
            unique.append(item)
            if len(unique) >= top:
                break
        return unique
    except Exception:
        return []

def fmt_index_label(item):
    parts = []
    if item.get("bab"):        parts.append(item["bab"])
    if item.get("dabit_text"): parts.append(f"الضابط: {item['dabit_text']}")
    if item.get("rwaq"):       parts.append(item["rwaq"])
    return " · ".join(parts)

def gather_sources(query, sb):
    """يجمع أفضل النصوص من الكتابين لتكون المادة المؤصِّلة."""
    sources = []
    for tbl, name in [("manjam_al_usul", "كتاب منجم الأصول"),
                      ("idah_al_muhayid", "كتاب الإيضاح المحايد")]:
        for item in search_book_ranked(tbl, query, sb, top=2):
            sources.append({
                "المصدر": name,
                "الموضع": fmt_index_label(item),
                "النص":   item["text"],
            })
    return sources

def build_grounding(sources):
    """يصوغ المادة المؤصِّلة نصّاً يُحقَن في تعليمات النظام."""
    if not sources:
        return ("لم يُعثر على نصٍّ مطابقٍ في كتابَي المؤلِّف لهذا السؤال. "
                "التزِم بالقاعدة الثالثة: بيِّن أنّ المسألة خارجةٌ عن المنهجية أو لا نصَّ فيها، "
                "واطلب إعادة الصياغة.")
    blocks = []
    for i, s in enumerate(sources, 1):
        loc = f" — الموضع: {s['الموضع']}" if s.get("الموضع") else ""
        blocks.append(f"[{i}] {s['المصدر']}{loc}\n{s['النص']}")
    return "المادة المؤصِّلة (نصوص المؤلِّف من الكتابين):\n\n" + "\n\n".join(blocks)

# ============================================================
# الربط بمحرّكي الاستنباط والتأويل (المرحلة الثانية)
# ============================================================
# ألفاظٌ تدلّ على أنّ السؤال حكميٌّ، فتُستدعى عندها آلةُ الأحكام
RULING_KEYWORDS = {
    "حكم","الحكم","يجوز","جائز","الجواز","واجب","الوجوب","يجب","فرض","الفرض",
    "حرام","التحريم","يحرم","مكروه","الكراهة","مباح","الاباحه","مندوب","الندب",
    "مستحب","سنه","امر","الامر","نهي","النهي","تحل","يحل","عزيمه","رخصه","يكفر",
}

def looks_like_ruling(q):
    """بوّابةٌ خفيفةٌ حتميّة: هل السؤال حكميٌّ يستدعي آلةَ الأحكام؟"""
    qc = clean(q)
    words = set(qc.split())
    return bool(words & RULING_KEYWORDS)

async def fetch_analysis(text):
    """يُعيد استعمال محرّك الاستنباط/التأويل عبر نقطة /api/index — غير حاسم.
    يُجري التحليل على النصّ الممرَّر، ويُعيد حصيلة الاستنباط والتأويل أو None."""
    try:
        async with httpx.AsyncClient(timeout=20.0) as client:
            r = await client.post(f"{SELF_BASE_URL}/api/index", json={"query": text})
        if r.status_code != 200:
            return None
        data = r.json()
        return {
            "استنباط": data.get("استنباط", {}),
            "تأويل":   data.get("تأويل", {}),
        }
    except Exception:
        return None

def build_analysis_card(analysis):
    """يُجهّز بطاقةَ التحليل في صورتَين: نصٍّ موجزٍ للنموذج، وبنيةٍ مرتّبةٍ للعرض."""
    if not analysis:
        return None
    ist = analysis.get("استنباط", {}) or {}
    taw = analysis.get("تأويل", {}) or {}

    fields = []
    def add(label, val):
        if val and str(val).strip() and str(val).strip() != "—":
            fields.append((label, str(val).strip()))

    # نأخذ السطر الأوّل من الأصول (العنوان) دون النصّ الكامل تفادياً للإطالة
    usul = (ist.get("الأصول") or "").split("\n")[0]
    add("الأصل", ist.get("الأصل"))
    add("الأصول", usul)
    furoo = ist.get("الفروع")
    if isinstance(furoo, list): furoo = "، ".join(furoo)
    add("الفروع", furoo)
    add("الشعبة", ist.get("الشعبة"))
    dabit = ist.get("الضابط")
    if isinstance(dabit, list): dabit = "، ".join(dabit)
    add("الضابط", dabit)
    add("الحكم النظري", ist.get("الحكم_النظري"))
    add("الحكم الضروري", ist.get("الحكم_الضروري"))

    # الأروقة (إن كُشف اسمٌ من الأسماء الحسنى في النصّ المحلَّل)
    names = taw.get("الأسماء_المكتشفة") or []
    interp = taw.get("التأويل")
    arwiqa = []
    if names and isinstance(interp, list):
        for n in interp:
            arwiqa.append({
                "الاسم":  n.get("الاسم", ""),
                "الرواق": n.get("الرواق", ""),
                "الباب":  n.get("الباب", ""),
                "الركن":  n.get("الركن", ""),
                "حكم_التحلي_التخلي": n.get("حكم_التحلي_التخلي", ""),
            })

    if not fields and not arwiqa:
        return None

    # نصٌّ موجزٌ للنموذج
    lines = ["بطاقةُ التحليل المؤصَّل (أنتجها محرّكا الاستنباط والتأويل حتمياً من النصّ الأوثق صلةً؛ "
             "استأنِسْ بها في تحرير الحكم ووفّق بينها وبين النصوص، فإن بدت غير ذات صلةٍ بالسؤال فأهمِلها):"]
    for label, val in fields:
        lines.append(f"- {label}: {val}")
    for a in arwiqa:
        seg = "، ".join(v for v in [a['الاسم'], a['الرواق'], a['الباب'], a['الركن']] if v)
        if seg:
            lines.append(f"- من الأروقة: {seg}")
            if a["حكم_التحلي_التخلي"]:
                lines.append(f"  · حكم التحلي/التخلي: {a['حكم_التحلي_التخلي']}")
    card_text = "\n".join(lines)

    # بنيةٌ مرتّبةٌ للعرض المطويّ
    card_struct = {"حقول": [{"label": l, "value": v} for l, v in fields], "أروقة": arwiqa}
    return {"text": card_text, "struct": card_struct}

# ============================================================
# استدعاء Claude
# ============================================================
async def call_claude(messages, grounding):
    system_text = MANHAJ_SYSTEM + "\n\n" + grounding
    payload = {
        "model": MUHAWIR_MODEL,
        "max_tokens": 1500,
        "system": system_text,
        "messages": messages,
        # مستوى الجهد — low للسرعة والتوفير. احذف هذا السطر لو أردت السلوك الافتراضي.
        "output_config": {"effort": MUHAWIR_EFFORT},
    }
    headers = {
        "x-api-key": ANTHROPIC_KEY,
        "anthropic-version": ANTHROPIC_VERSION,
        "content-type": "application/json",
    }
    async with httpx.AsyncClient(timeout=55.0) as client:
        r = await client.post(ANTHROPIC_URL, headers=headers, json=payload)
    if r.status_code != 200:
        # نُعيد رسالة الخطأ كما هي ليسهل تشخيصها أثناء التجربة
        raise RuntimeError(f"Anthropic {r.status_code}: {r.text[:500]}")
    data = r.json()
    parts = [b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"]
    return "\n".join(p for p in parts if p).strip()

# ============================================================
# الدالة الرئيسية للمحاوِر
# ============================================================
@app.post("/api/muhawir")
@app.post("/")
async def muhawir(request: Request):
    try:
        body = await request.json()
        raw = body.get("messages", [])
        # تنظيف وتقييد السجلّ إلى آخر ٨ رسائل لضبط الكلفة
        cleaned = [
            {"role": m.get("role"), "content": str(m.get("content", "")).strip()}
            for m in raw
            if m.get("role") in ("user", "assistant") and str(m.get("content", "")).strip()
        ][-8:]
        # إسقاط أيّ رسائل مساعِدٍ في المقدّمة (يجب أن يبدأ السجلّ بالمستخدم)
        while cleaned and cleaned[0]["role"] == "assistant":
            cleaned.pop(0)
        # دمج الرسائل المتتالية لنفس الدور لضمان تعاقب الأدوار
        messages = []
        for m in cleaned:
            if messages and messages[-1]["role"] == m["role"]:
                messages[-1]["content"] += "\n" + m["content"]
            else:
                messages.append(dict(m))
        if not messages or messages[-1]["role"] != "user":
            return JSONResponse({"error": "يجب أن ينتهي السجلّ برسالة مستخدم"}, status_code=400)
        if not SUPABASE_URL or not SUPABASE_KEY:
            return JSONResponse({"error": "متغيّرات Supabase غير مضبوطة"}, status_code=500)
        if not ANTHROPIC_KEY:
            return JSONResponse({"error": "المفتاح ANTHROPIC_API_KEY غير مضبوط في Vercel"}, status_code=500)

        # السؤال الحالي = آخر رسالة مستخدم
        query = messages[-1]["content"]
        sb = get_supabase()
        sources   = gather_sources(query, sb)
        grounding = build_grounding(sources)

        # بطاقةُ التحليل: تُستدعى آلةُ الأحكام عند المسائل الحكميّة فقط (غير حاسمة)
        card = None
        if sources and looks_like_ruling(query):
            analysis = await fetch_analysis(sources[0]["النص"])
            card = build_analysis_card(analysis)
            if card:
                grounding += "\n\n" + card["text"]

        reply = await call_claude(messages, grounding)

        out = {
            "reply":   reply,
            "المصادر": sources,
            "خاتمة":   KHATIMA,
        }
        if card:
            out["بطاقة_التحليل"] = card["struct"]
        return JSONResponse(out)
    except Exception as e:
        return JSONResponse({"error": str(e)}, status_code=500)
