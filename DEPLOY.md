# دليل نشر نقيب المثاني على Vercel

## هيكل الملفات
```
naqeeb/
├── api/
│   └── query.py
├── vercel.json
└── requirements.txt
```

## خطوات النشر

### ١. إنشاء حساب Vercel (مجاناً بدون بطاقة)
https://vercel.com/signup
سجّل دخولك بحساب GitHub أو Google

### ٢. تثبيت Vercel CLI
في PowerShell أو CMD:
```
npm install -g vercel
```

### ٣. تسجيل الدخول
```
vercel login
```

### ٤. النشر
انتقل لمجلد naqeeb ثم:
```
vercel --prod
```

### ٥. إضافة متغيرات البيئة
بعد النشر افتح:
https://vercel.com/dashboard
اختر المشروع ← Settings ← Environment Variables
أضف:
- SUPABASE_URL = https://zalovdghegcipvsqxocl.supabase.co
- SUPABASE_KEY = (مفتاح anon من Supabase)

### ٦. إعادة النشر بعد إضافة المتغيرات
```
vercel --prod
```

### ٧. اختبار الرابط
```
curl -X POST https://YOUR-PROJECT.vercel.app/api/query \
  -H "Content-Type: application/json" \
  -d "{\"query\": \"أقيموا الصلاة وآتوا الزكاة\"}"
```

## رابط الـ API النهائي
```
https://YOUR-PROJECT.vercel.app/api/query
```
هذا الرابط ستستخدمه في تطبيق الأندرويد.
