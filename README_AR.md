# تشغيل بوت Discord على استضافة 24/7

## مهم جدًا
التوكن القديم ظهر داخل الملف، لذلك ألغِه من Discord Developer Portal وأنشئ توكنًا جديدًا.

## تشغيل محلي
1. ثبّت Python وFFmpeg.
2. افتح الطرفية داخل المجلد.
3. نفّذ:
   pip install -r requirements.txt
4. أنشئ متغير البيئة DISCORD_TOKEN.
5. شغّل:
   python bot.py

## Railway
1. أنشئ مشروعًا جديدًا.
2. ارفع هذا المجلد إلى GitHub ثم اربطه بالمشروع.
3. أضف متغيرًا باسم:
   DISCORD_TOKEN
4. ضع فيه التوكن الجديد.
5. سيستخدم Railway ملف Dockerfile تلقائيًا.

## VPS / Docker
ابنِ الصورة:
   docker build -t discord-music-bot .

ثم شغّلها:
   docker run -d --restart unless-stopped \
     -e DISCORD_TOKEN="ضع_التوكن_الجديد_هنا" \
     --name discord-music-bot \
     discord-music-bot

بهذا سيعود البوت للعمل تلقائيًا بعد إعادة تشغيل السيرفر.
