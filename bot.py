

أمس 6:27 م

message.txt
مستند

اليوم 6:37 ص
ممتاز! بما أن لديك


أنا لا أستطيع توليد صورة الآن، لكن


الصورة التي تم إنشاؤها: واجهة بوت موسيقى داكنة نيون


تحرير


الصورة التي تم إنشاؤها: Musikbot UI i futuristisk stil


تحرير

Tänkte i 57s

الصورة التي تم إنشاؤها: لوحة تحكم بوت الموسيقى النيوني


تحرير


الصورة التي تم إنشاؤها: لوحة تحكم الموسيقى في ديسكورد


تحرير


الصورة التي تم إنشاؤها: Musikbot kontrollpanel med arabisk UI


تحرير


الصورة التي تم إنشاؤها: Musikbot kontrollpanel i neonstil


تحرير


الصورة التي تم إنشاؤها: Discord dashboard guide med färgexempel


تحرير


تخيل فتاة


انت قلت ليس هناك اخطاء


كود ملصق واحد. py
ملف



كود ملصق واحد(1). py
ملف
اعيد هذا  في الكود الخاص بي ولا اريد اخطاء

لماذا

تم


كود ملصق واحد(2). py
ملف
قوم بفعلها وارجو ان يعمل بشكل ممتاز ومن دون اخطاء وسرعه استجابه 


.env.example
ملف
 هل هذا

هل هذا هو


تم


كود ملصق واحد(3). py
ملف




اين ارفع 



ثم 

والان 






 متصل ولاكن لايشغل اغاني لماذا




هنا ام لا









تقصد هكذا 




هل هذا صحيح اخر الكود 







 احمر

هل هذا يبقى هكذا 






حل 



github

اغلقت vs  ولكن يوجد اشاره للبوت ولايطلع صوت 



كود ملصق واحد(4). py
ملف

























لن تجده لأن كودك لا يستخدم متغيرًا باسم FFMPEG_OPTIONS.

عندك السطر داخل play_next() بهذا الشكل تقريبًا:

ffmpeg_source = discord.FFmpegPCMAudio(
    audio_url,
    before_options=FFMPEG_BEFORE_OPTIONS,
    options=f'-vn -af "{audio_filter}"'
)
عدّل فقط قيمة options إلى:

ffmpeg_source = discord.FFmpegPCMAudio(
    audio_url,
    before_options=FFMPEG_BEFORE_OPTIONS,
    options=(
        '-vn '
        '-headers "User-Agent: Mozilla/5.0\\r\\n" '
        f'-af "{audio_filter}"'
    )
)
وابحث داخل YDL_OPTIONS عن:

"format": "bestaudio[ext=m4a]/bestaudio/best",
وغيّره إلى:

"format": "bestaudio/best",
ثم احفظ bot.py، ارفعه إلى GitHub، وبعدها اعمل Redeploy في Railway.

مهم: -user_agent ليس خيارًا صحيحًا داخل جزء options بهذه الطريقة، لذلك استخدم -headers كما في الكود أعلاه. ومع ذلك، إذا استمر خطأ 403 بعد هذا التعديل، فغالبًا رابط Google Video مرتبط بعنوان IP أو جلسة مختلفة، وستكون المشكلة من Railway/YouTube وليست من FFmpeg نفسه.


سوف ارسل لك الكود واضف هذا الذي تقوله 

ممتاز، أرسل ملف bot.py كاملًا هنا (ارفعه كملف وليس على شكل صور).

بعد أن ترسله سأقوم بـ:

إضافة التعديلات الخاصة بـ FFmpeg.

تعديل YDL_OPTIONS.

التأكد من أن YOUTUBE_COOKIES_BASE64 يعمل بشكل صحيح.

مراجعة إعدادات yt-dlp.

التأكد من توافق الكود مع Railway وDockerfile وrequirements.txt.

عدم حذف أي أوامر أو ميزات موجودة في البوت إلا إذا كانت تسبب المشكلة.

ثم سأعيد لك الملف bot.py جاهزًا للرفع إلى GitHub بحيث يكفي أن تستبدل الملف القديم وتعمل Redeploy على Railway.



نص واحد ملصق .txt
مستند

تم تعديل الكود لمعالجة خطأ 403 Forbidden عبر تمرير ترويسات User-Agent وReferer وOrigin التي يوفرها yt-dlp إلى FFmpeg. كما تم فحص الكود نحويًا بنجاح. 


تحميل النسخة الجاهزة للرفع

فك الضغط ثم استبدل هذه الملفات في GitHub:

bot.py
requirements.txt
Dockerfile
railway.json
.gitignore
بعدها افتح Railway واضغط Redeploy. لا تغيّر متغيري:

DISCORD_TOKEN
YOUTUBE_COOKIES_BASE64
إذا استمر 403 بعد هذه النسخة، فسيكون الرفض من خوادم YouTube لعنوان IP الخاص بـRailway، وليس خطأً نحويًا في الكود. 


import asyncio
import base64
import os
from pathlib import Path

import discord
import yt_dlp
from discord.ext import commands

try:
from dotenv import load_dotenv
except ImportError:
load_dotenv = None

BASE_DIR = Path(file).resolve().parent

if load_dotenv is not None:
load_dotenv(BASE_DIR / ".env")

TOKEN = os.getenv("DISCORD_TOKEN")
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(
command_prefix="$",
intents=intents,
help_command=None
)

FFMPEG_BEFORE_OPTIONS = (
"-reconnect 1 "
"-reconnect_streamed 1 "
"-reconnect_delay_max 5"
)

def prepare_youtube_cookies():
"""إنشاء ملف Cookies مؤقت من YOUTUBE_COOKIES_BASE64."""
encoded_cookies = os.getenv(
"YOUTUBE_COOKIES_BASE64",
""
).strip()

if not encoded_cookies:
    print("ℹ️ YOUTUBE_COOKIES_BASE64 غير موجود.")
    return None

cookies_path = Path("/tmp/youtube_cookies.txt")

try:
    decoded = base64.b64decode(
        encoded_cookies,
        validate=True
    )

    if not decoded:
        raise ValueError("ملف Cookies الناتج فارغ.")

    cookies_path.write_bytes(decoded)

    print("✅ تم تجهيز Cookies الخاصة بـ YouTube.")
    return str(cookies_path)

except Exception as error:
    print(f"❌ تعذر تجهيز YouTube Cookies: {error}")
    return None
YOUTUBE_COOKIES_FILE = prepare_youtube_cookies()

YDL_OPTIONS = {
"format": "bestaudio/best",
"quiet": True,
"no_warnings": False,
"noplaylist": True,
"default_search": "ytsearch",
"socket_timeout": 20,
"retries": 3,
"fragment_retries": 3,
"remote_components": ["ejs"],
"js_runtimes": {
"deno": {}
},
}

if YOUTUBE_COOKIES_FILE:
YDL_OPTIONS["cookiefile"] = YOUTUBE_COOKIES_FILE

قائمة الانتظار
queue = []

تكرار الأغنية الحالية
LOOP = False

مستوى الصوت الافتراضي: 50%
VOLUME = 0.5

الأغنية الحالية
current_song = None

وضع الباس الحالي
BASS_MODE = "normal"

المؤثر الصوتي الحالي
AUDIO_EFFECT = "off"

التشغيل التلقائي
AUTOPLAY = False

آخر أغنية تم تشغيلها لاستخدامها في الاقتراحات
last_song = None

يمنع التشغيل التلقائي بعد الإيقاف اليدوي
MANUAL_STOP = False

إعدادات الباس
BASS_PRESETS = {
"off": "anull",
"normal": "bass=g=4=110=0.6,alimiter=limit=0.95",
"strong": "bass=g=10=105=0.7,alimiter=limit=0.90",
"extreme": "bass=g=16=95=0.8,alimiter=limit=0.85",
}

BASS_NAMES = {
"off": "متوقف",
"normal": "عادي",
"strong": "قوي",
"extreme": "قوي جدًا",
}

المؤثرات والفلاتر الصوتية
AUDIO_EFFECTS = {
"off": "anull",

"echo": (
    "aecho=0.8:0.7:60:0.35,"
    "alimiter=limit=0.92"
),

"reverb": (
    "aecho=0.8:0.75:40|80:0.30|0.18,"
    "alimiter=limit=0.90"
),

"chorus": (
    "chorus=0.7:0.9:55:0.4:0.25:2,"
    "alimiter=limit=0.92"
),

"flanger": (
    "flanger=delay=5:depth=2:"
    "regen=0:width=71:speed=0.5:"
    "shape=sinusoidal:phase=25:"
    "interp=linear,"
    "alimiter=limit=0.92"
),

"phaser": (
    "aphaser=in_gain=0.4:"
    "out_gain=0.74:"
    "delay=3:"
    "decay=0.4:"
    "speed=0.5:"
    "type=triangular,"
    "alimiter=limit=0.92"
),

"haas": (
    "haas=left_delay=2.05:"
    "right_delay=2.12:"
    "side_gain=1:"
    "middle_source=mid:"
    "middle_phase=false,"
    "alimiter=limit=0.92"
),

"surround": (
    "surround=chl_out=stereo:"
    "level_in=1:"
    "level_out=1:"
    "lfe=0,"
    "alimiter=limit=0.92"
),

"eightd": (
    "apulsator=hz=0.10:amount=0.85,"
    "alimiter=limit=0.92"
),

"nightcore": (
    "asetrate=48000*1.18,"
    "aresample=48000,"
    "atempo=1/1.18,"
    "alimiter=limit=0.92"
),

"vaporwave": (
    "asetrate=48000*0.80,"
    "aresample=48000,"
    "atempo=1/0.80,"
    "aecho=0.8:0.7:45:0.20,"
    "alimiter=limit=0.90"
),

"deepvoice": (
    "asetrate=48000*0.85,"
    "aresample=48000,"
    "atempo=1/0.85,"
    "alimiter=limit=0.92"
),

"slow": (
    "atempo=0.85,"
    "alimiter=limit=0.95"
),

"fast": (
    "atempo=1.25,"
    "alimiter=limit=0.95"
),

"tremolo": (
    "tremolo=f=5:d=0.6,"
    "alimiter=limit=0.94"
),

"vibrato": (
    "vibrato=f=5:d=0.4,"
    "alimiter=limit=0.94"
),

"crystal": (
    "crystalizer=i=2.0:c=1,"
    "alimiter=limit=0.91"
),

"radio": (
    "highpass=f=300,"
    "lowpass=f=3400,"
    "acompressor=threshold=0.15:ratio=4,"
    "volume=1.2,"
    "alimiter=limit=0.88"
),

"telephone": (
    "highpass=f=400,"
    "lowpass=f=3000,"
    "equalizer=f=1500:t=q:w=1:g=4,"
    "alimiter=limit=0.92"
),

"cinema": (
    "highpass=f=25,"
    "bass=g=8:f=60:w=0.8,"
    "equalizer=f=120:t=q:w=1:g=4,"
    "equalizer=f=300:t=q:w=1:g=2,"
    "acompressor=threshold=0.14:"
    "ratio=2.5:attack=20:release=220,"
    "alimiter=limit=0.89"
),

"car": (
    "highpass=f=28,"
    "bass=g=10:f=65:w=0.8,"
    "equalizer=f=110:t=q:w=1:g=5,"
    "equalizer=f=250:t=q:w=1:g=-2,"
    "equalizer=f=8000:t=q:w=1:g=2,"
    "acompressor=threshold=0.12:"
    "ratio=3:attack=15:release=160,"
    "alimiter=limit=0.86"
),

"vocal": (
    "highpass=f=80,"
    "equalizer=f=250:t=q:w=1:g=-2,"
    "equalizer=f=2500:t=q:w=1:g=4,"
    "equalizer=f=6000:t=q:w=1:g=2,"
    "acompressor=threshold=0.15:ratio=2.5,"
    "alimiter=limit=0.92"
),

"karaoke": (
    "pan=stereo|c0=c0-c1|c1=c1-c0,"
    "highpass=f=120,"
    "lowpass=f=12000,"
    "alimiter=limit=0.92"
),

"wide": (
    "extrastereo=m=1.8,"
    "alimiter=limit=0.92"
),

"mono": (
    "pan=mono|c0=0.5*c0+0.5*c1"
),

"clean": (
    "highpass=f=30,"
    "lowpass=f=18000,"
    "dynaudnorm,"
    "alimiter=limit=0.94"
),
}

AUDIO_EFFECT_NAMES = {
"off": "بدون فلتر",
"echo": "صدى",
"reverb": "ريفيرب",
"chorus": "كورَس",
"flanger": "فلانجر",
"phaser": "فايزر",
"haas": "توسيع Haas",
"surround": "صوت محيطي",
"eightd": "صوت 8D",
"nightcore": "نايتكور",
"vaporwave": "فايبرويف",
"deepvoice": "صوت عميق",
"slow": "بطيء",
"fast": "سريع",
"tremolo": "تريمولو",
"vibrato": "فيبراتو",
"crystal": "كريستال",
"radio": "راديو",
"telephone": "هاتف",
"cinema": "سينمائي",
"car": "سيارة",
"vocal": "تعزيز الغناء",
"karaoke": "كاريوكي",
"wide": "ستيريو واسع",
"mono": "مونو",
"clean": "تنظيف الصوت",
}

def build_audio_filter():
"""بناء سلسلة فلاتر FFmpeg من الباس والمؤثر الحالي."""
filters = []

bass_filter = BASS_PRESETS.get(
    BASS_MODE,
    BASS_PRESETS["normal"]
)

effect_filter = AUDIO_EFFECTS.get(
    AUDIO_EFFECT,
    AUDIO_EFFECTS["off"]
)

if bass_filter != "anull":
    filters.append(bass_filter)

if effect_filter != "anull":
    filters.append(effect_filter)

if not filters:
    return "anull"

return ",".join(filters)
async def set_music_presence(title="Music"):
"""إبقاء البوت في حالة عدم الإزعاج."""
await bot.change_presence(
status=discord.Status.dnd,
activity=discord.Game(name=title)
)

def extract_song_info(query):
"""استخراج معلومات الأغنية بالرابط أو البحث بالاسم."""
with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
info = ydl.extract_info(
query,
download=False
)

    if info and "entries" in info:
        entries = info.get("entries") or []

        if not entries:
            raise ValueError("لم يتم العثور على نتائج.")

        info = entries[0]

    if not info:
        raise ValueError("تعذر استخراج معلومات الأغنية.")

    return info
def build_song_from_info(info):
"""تحويل نتيجة yt-dlp إلى بيانات أغنية."""
title = info.get("title", "أغنية غير معروفة")

webpage_url = (
    info.get("webpage_url")
    or info.get("original_url")
)

if not webpage_url:
    video_id = info.get("id")

    if video_id:
        webpage_url = (
            f"https://www.youtube.com/watch?v={video_id}"
        )

if not webpage_url:
    raise ValueError("لم يتم العثور على رابط الأغنية.")

return {
    "title": title,
    "url": webpage_url
}
def find_autoplay_song(seed_song):
"""البحث عن اقتراح قريب من آخر أغنية."""
seed_title = seed_song.get("title", "").strip()

if not seed_title:
    raise ValueError("عنوان آخر أغنية غير صالح.")

search_query = (
    f"ytsearch5:{seed_title} similar songs official audio"
)

with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
    result = ydl.extract_info(
        search_query,
        download=False
    )

entries = (result or {}).get("entries") or []

for info in entries:
    if not info:
        continue

    candidate = build_song_from_info(info)

    if candidate["url"] == seed_song.get("url"):
        continue

    return candidate

raise ValueError("لم يتم العثور على اقتراح مناسب.")
def create_music_embed(song):
"""إنشاء Embed للأغنية الحالية."""
embed = discord.Embed(
title="🎵 يتم التشغيل الآن",
description=f"{song['title']}",
color=discord.Color.gold()
)

embed.add_field(
    name="🔊 مستوى الصوت",
    value=f"**{int(VOLUME * 100)}%**",
    inline=True
)

embed.add_field(
    name="🎚️ الباس",
    value=f"**{BASS_NAMES[BASS_MODE]}**",
    inline=True
)

embed.add_field(
    name="🎛️ الفلتر",
    value=f"**{AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}**",
    inline=True
)

embed.add_field(
    name="🔁 التكرار",
    value="**مفعّل**" if LOOP else "**متوقف**",
    inline=True
)

embed.add_field(
    name="📋 الأغاني المنتظرة",
    value=f"**{len(queue)}**",
    inline=True
)

embed.add_field(
    name="♾️ التشغيل التلقائي",
    value="**مفعّل**" if AUTOPLAY else "**متوقف**",
    inline=True
)

embed.set_footer(
    text="🟨 استخدم الأزرار والقوائم للتحكم — الفلاتر تطبق على الأغنية التالية"
)

return embed


class BassSelect(discord.ui.Select):
"""قائمة اختيار الباس داخل لوحة التشغيل."""

def __init__(self):
    descriptions = {
        "off": "إيقاف تعزيز الباس",
        "normal": "باس متوازن",
        "strong": "باس قوي",
        "extreme": "باس قوي جدًا",
    }

    emojis = {
        "off": "🔇",
        "normal": "🎚️",
        "strong": "🔊",
        "extreme": "💥",
    }

    options = [
        discord.SelectOption(
            label=BASS_NAMES[key],
            value=key,
            description=descriptions[key],
            emoji=emojis[key],
            default=(key == BASS_MODE)
        )
        for key in BASS_PRESETS
    ]

    super().__init__(
        placeholder=f"🟨 الباس الحالي: {BASS_NAMES[BASS_MODE]}",
        min_values=1,
        max_values=1,
        options=options,
        row=1
    )

async def callback(self, interaction: discord.Interaction):
    global BASS_MODE

    view = self.view

    if view is None or not await view.check_user(interaction):
        return

    BASS_MODE = self.values[0]

    for option in self.options:
        option.default = option.value == BASS_MODE

    self.placeholder = (
        f"🟨 الباس الحالي: {BASS_NAMES[BASS_MODE]}"
    )

    embed = (
        create_music_embed(current_song)
        if current_song
        else None
    )

    await interaction.response.edit_message(
        embed=embed,
        view=view
    )
class FilterSelect(discord.ui.Select):
"""قائمة اختيار مجموعة من الفلاتر داخل لوحة التشغيل."""

def __init__(self, filter_keys, placeholder, row):
    options = [
        discord.SelectOption(
            label=AUDIO_EFFECT_NAMES[key],
            value=key,
            description=f"تفعيل فلتر {AUDIO_EFFECT_NAMES[key]}",
            default=(key == AUDIO_EFFECT)
        )
        for key in filter_keys
    ]

    super().__init__(
        placeholder=placeholder,
        min_values=1,
        max_values=1,
        options=options,
        row=row
    )

async def callback(self, interaction: discord.Interaction):
    global AUDIO_EFFECT

    view = self.view

    if view is None or not await view.check_user(interaction):
        return

    AUDIO_EFFECT = self.values[0]

    for item in view.children:
        if isinstance(item, FilterSelect):
            for option in item.options:
                option.default = (
                    option.value == AUDIO_EFFECT
                )

    embed = (
        create_music_embed(current_song)
        if current_song
        else None
    )

    await interaction.response.edit_message(
        embed=embed,
        view=view
    )
class MusicControls(discord.ui.View):
def init(self, ctx):
super().init(timeout=600)
self.ctx = ctx

    filter_keys = list(AUDIO_EFFECTS.keys())

    # Discord يسمح بحد أقصى 25 خيارًا في القائمة الواحدة.
    first_filters = filter_keys[:13]
    second_filters = filter_keys[13:]

    self.add_item(BassSelect())

    self.add_item(
        FilterSelect(
            first_filters,
            "🟨 الفلاتر الأساسية",
            row=2
        )
    )

    self.add_item(
        FilterSelect(
            second_filters,
            "🟨 الفلاتر الإضافية",
            row=3
        )
    )

async def check_user(self, interaction):
    """التأكد من أن المستخدم داخل روم البوت."""
    if not interaction.user.voice:
        await interaction.response.send_message(
            "❌ ادخل إلى روم صوتي أولًا.",
            ephemeral=True
        )
        return False

    voice = interaction.guild.voice_client

    if not voice:
        await interaction.response.send_message(
            "❌ البوت غير موجود داخل روم صوتي.",
            ephemeral=True
        )
        return False

    if interaction.user.voice.channel != voice.channel:
        await interaction.response.send_message(
            "❌ يجب أن تكون في نفس روم البوت.",
            ephemeral=True
        )
        return False

    return True

@discord.ui.button(
    label=None,
    emoji="⏸️",
    style=discord.ButtonStyle.secondary
)
async def pause_resume(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    if not await self.check_user(interaction):
        return

    voice = interaction.guild.voice_client

    if voice.is_playing():
        voice.pause()

        button.emoji = "▶️"

        await interaction.response.edit_message(
            view=self
        )

    elif voice.is_paused():
        voice.resume()

        button.emoji = "⏸️"

        await interaction.response.edit_message(
            view=self
        )

    else:
        await interaction.response.send_message(
            "❌ لا توجد أغنية تعمل حاليًا.",
            ephemeral=True
        )

@discord.ui.button(
    label=None,
    emoji="⏭️",
    style=discord.ButtonStyle.secondary
)
async def skip_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global current_song

    if not await self.check_user(interaction):
        return

    voice = interaction.guild.voice_client

    if voice.is_playing() or voice.is_paused():
        current_song = None

        await interaction.response.send_message(
            "⏭️ تم تخطي الأغنية."
        )

        voice.stop()

    else:
        await interaction.response.send_message(
            "❌ لا توجد أغنية تعمل.",
            ephemeral=True
        )

@discord.ui.button(
    label=None,
    emoji="🔁",
    style=discord.ButtonStyle.secondary
)
async def loop_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global LOOP

    if not await self.check_user(interaction):
        return

    if current_song is None:
        await interaction.response.send_message(
            "❌ لا توجد أغنية حالية لتكرارها.",
            ephemeral=True
        )
        return

    LOOP = not LOOP

    if LOOP:
        button.emoji = "🔂"
    else:
        button.emoji = "🔁"

    embed = create_music_embed(current_song)

    await interaction.response.edit_message(
        embed=embed,
        view=self
    )

@discord.ui.button(
    label=None,
    emoji="🧹",
    style=discord.ButtonStyle.secondary
)
async def clear_filter_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global AUDIO_EFFECT

    if not await self.check_user(interaction):
        return

    AUDIO_EFFECT = "off"

    for item in self.children:
        if isinstance(item, FilterSelect):
            for option in item.options:
                option.default = (
                    option.value == AUDIO_EFFECT
                )

    embed = (
        create_music_embed(current_song)
        if current_song
        else None
    )

    await interaction.response.edit_message(
        embed=embed,
        view=self
    )

@discord.ui.button(
    label=None,
    emoji="⏹️",
    style=discord.ButtonStyle.secondary
)
async def stop_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global current_song, LOOP, MANUAL_STOP

    if not await self.check_user(interaction):
        return

    voice = interaction.guild.voice_client

    queue.clear()
    current_song = None
    LOOP = False
    MANUAL_STOP = True

    for item in self.children:
        item.disabled = True

    await interaction.response.edit_message(
        content="⏹️ تم إيقاف التشغيل ومسح قائمة الانتظار.",
        embed=None,
        view=self
    )

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    await set_music_presence()
@bot.event
async def on_ready():
await set_music_presence()
print(f"✅ Logged in as {bot.user}")

@bot.command(name="vjoin123")
async def join_voice(ctx):
if not ctx.author.voice:
await ctx.send("❌ ادخل إلى روم صوتي أولًا.")
return

channel = ctx.author.voice.channel

try:
    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()

    await set_music_presence()

    await ctx.send(
        f"✅ دخلت إلى: **{channel.name}**"
    )

except Exception as error:
    print(f"Voice connection error: {error}")
    await ctx.send(
        "❌ تعذر الدخول إلى الروم الصوتي."
    )
@bot.command(name="leave123")
async def leave_voice(ctx):
global current_song, LOOP, MANUAL_STOP

voice = ctx.voice_client

if not voice:
    await ctx.send("❌ لست داخل أي روم.")
    return

queue.clear()
current_song = None
LOOP = False
MANUAL_STOP = True

if voice.is_playing() or voice.is_paused():
    voice.stop()

await voice.disconnect()
await set_music_presence()

await ctx.send(
    "👋 تم الخروج من الروم ومسح قائمة الانتظار."
)
async def play_next(ctx):
global current_song, last_song, MANUAL_STOP

voice = ctx.voice_client

if voice is None or not voice.is_connected():
    current_song = None
    await set_music_presence()
    return

if voice.is_playing() or voice.is_paused():
    return

if MANUAL_STOP:
    current_song = None
    await set_music_presence()
    return

if LOOP and current_song:
    song = current_song

elif queue:
    song = queue.pop(0)
    current_song = song

elif AUTOPLAY and last_song:
    try:
        await ctx.send(
            "♾️ انتهت قائمة الانتظار، جارٍ البحث عن اقتراح..."
        )

        song = await asyncio.to_thread(
            find_autoplay_song,
            last_song
        )

        current_song = song

        await ctx.send(
            f"✨ التشغيل التلقائي اختار: **{song['title']}**"
        )

    except Exception as autoplay_error:
        print(f"Autoplay error: {autoplay_error}")
        current_song = None
        await set_music_presence()

        await ctx.send(
            "⚠️ لم أتمكن من العثور على أغنية مقترحة."
        )
        return

else:
    current_song = None
    await set_music_presence()
    return

try:
    info = await asyncio.to_thread(
        extract_song_info,
        song["url"]
    )

    audio_url = info.get("url")

    if not audio_url:
        raise ValueError(
            "لم يتم العثور على رابط الصوت."
        )

    audio_filter = build_audio_filter()

    ffmpeg_source = discord.FFmpegPCMAudio(
        audio_url,
        before_options=FFMPEG_BEFORE_OPTIONS,
        options=f'-vn -af "{audio_filter}"'
    )

    source = discord.PCMVolumeTransformer(
        ffmpeg_source,
        volume=VOLUME
    )

    last_song = song

    def finished(error):
        if error:
            print(f"Playback error: {error}")

        future = asyncio.run_coroutine_threadsafe(
            play_next(ctx),
            bot.loop
        )

        def check_result(task):
            try:
                task.result()
            except Exception as task_error:
                print(
                    f"Next song error: {task_error}"
                )

        future.add_done_callback(check_result)

    voice.play(
        source,
        after=finished
    )

    await set_music_presence(
        song["title"]
    )

    embed = create_music_embed(song)
    controls = MusicControls(ctx)

    await ctx.send(
        embed=embed,
        view=controls
    )

except Exception as error:
    print(f"Music error: {error}")

    await ctx.send(
        f"❌ تعذر تشغيل: **{song['title']}**"
    )

    current_song = None
    await play_next(ctx)
@bot.command(name="play")
async def play(ctx, *, query: str):
"""تشغيل أغنية بالرابط أو البحث عنها بالاسم."""
global MANUAL_STOP

MANUAL_STOP = False
if not ctx.author.voice:
    await ctx.send("❌ ادخل إلى روم صوتي أولًا.")
    return

loading_message = None

try:
    if ctx.voice_client is None:
        await ctx.author.voice.channel.connect()

    voice = ctx.voice_client

    if voice.channel != ctx.author.voice.channel:
        await voice.move_to(
            ctx.author.voice.channel
        )

    loading_message = await ctx.send(
        "🔎 جارٍ البحث عن الأغنية..."
    )

    if query.startswith(("http://", "https://")):
        search_query = query
    else:
        search_query = f"ytsearch1:{query}"

    info = await asyncio.to_thread(
        extract_song_info,
        search_query
    )

    song = build_song_from_info(info)
    title = song["title"]

    queue.append(song)

    if loading_message:
        try:
            await loading_message.delete()
        except discord.HTTPException:
            pass

    if voice.is_playing() or voice.is_paused():
        embed = discord.Embed(
            title="✅ تمت إضافة أغنية",
            description=f"**{title}**",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📍 ترتيبها",
            value=f"**{len(queue)}**",
            inline=True
        )

        embed.add_field(
            name="🎚️ وضع الباس",
            value=f"**{BASS_NAMES[BASS_MODE]}**",
            inline=True
        )

        embed.add_field(
            name="🎛️ الفلتر",
            value=f"**{AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}**",
            inline=True
        )

        await ctx.send(embed=embed)

    else:
        await play_next(ctx)

except Exception as error:
    print(f"Play command error: {error}")

    if loading_message:
        try:
            await loading_message.delete()
        except discord.HTTPException:
            pass

    error_text = str(error)

    if "Sign in to confirm" in error_text:
        await ctx.send(
            "❌ YouTube طلب التحقق. "
            "تأكد من إعداد YOUTUBE_COOKIES_BASE64 في Railway."
        )
    else:
        await ctx.send(
            "❌ لم أتمكن من العثور على الأغنية أو تشغيلها."
        )
@play.error
async def play_error(ctx, error):
if isinstance(
error,
commands.MissingRequiredArgument
):
await ctx.send(
"❌ اكتب اسم الأغنية أو رابطها.\n"
"مثال: $play Believer\n"
"أو: $play رابط_الأغنية"
)
else:
print(f"Play error: {error}")

@bot.command(name="bass")
async def change_bass(ctx, mode: str = None):
"""عرض أو تغيير وضع الباس."""
global BASS_MODE

if mode is None:
    embed = discord.Embed(
        title="🎚️ قائمة الباس",
        description=(
            "`$bass off` — إيقاف الباس\n"
            "`$bass normal` — باس عادي\n"
            "`$bass strong` — باس قوي\n"
            "`$bass extreme` — باس قوي جدًا"
        ),
        color=discord.Color.orange()
    )

    embed.add_field(
        name="الوضع الحالي",
        value=f"**{BASS_NAMES[BASS_MODE]}**",
        inline=False
    )

    embed.set_footer(
        text="يتم تطبيق التغيير على الأغنية التالية"
    )

    await ctx.send(embed=embed)
    return

mode = mode.lower()

aliases = {
    "off": "off",
    "normal": "normal",
    "strong": "strong",
    "extreme": "extreme",
    "ايقاف": "off",
    "إيقاف": "off",
    "عادي": "normal",
    "قوي": "strong",
    "اقوى": "extreme",
    "أقوى": "extreme",
}

selected_mode = aliases.get(mode)

if selected_mode is None:
    await ctx.send(
        "❌ اختر أحد الأوضاع التالية:\n"
        "`off` أو `normal` أو `strong` أو `extreme`"
    )
    return

BASS_MODE = selected_mode

await ctx.send(
    f"🎚️ تم تغيير الباس إلى: "
    f"**{BASS_NAMES[BASS_MODE]}**\n"
    "ℹ️ سيتم تطبيقه على الأغنية التالية."
)
@bot.command(
name="filter",
aliases=["فلتر", "effect", "مؤثر", "تأثير"]
)
async def change_audio_effect(ctx, effect: str = None):
"""عرض أو تغيير الفلتر الصوتي."""
global AUDIO_EFFECT

if effect is None:
    filter_descriptions = {
        "off": "إيقاف جميع الفلاتر",
        "echo": "إضافة صدى واضح",
        "reverb": "صدى واسع يشبه القاعات",
        "chorus": "مضاعفة واتساع الصوت",
        "flanger": "موجات صوتية متحركة",
        "phaser": "تأثير فايزر متحرك",
        "haas": "توسيع الستيريو",
        "surround": "مجال صوتي محيطي",
        "eightd": "تحريك الصوت بين القناتين",
        "nightcore": "نغمة أعلى وإحساس أسرع",
        "vaporwave": "نغمة منخفضة مع صدى",
        "deepvoice": "خفض طبقة الصوت",
        "slow": "إبطاء التشغيل",
        "fast": "تسريع التشغيل",
        "tremolo": "تذبذب مستوى الصوت",
        "vibrato": "تذبذب طبقة الصوت",
        "crystal": "إبراز حدة وتفاصيل الصوت",
        "radio": "محاكاة صوت الراديو",
        "telephone": "محاكاة صوت الهاتف",
        "cinema": "صوت سينمائي عميق",
        "car": "تأثير سماعات السيارة",
        "vocal": "إبراز صوت المغني",
        "karaoke": "تقليل الصوت الموجود في المنتصف",
        "wide": "ستيريو أوسع",
        "mono": "تحويل الصوت إلى مونو",
        "clean": "تنظيف وتوحيد مستوى الصوت",
    }

    lines = []

    for filter_key in AUDIO_EFFECTS:
        lines.append(
            f"`$filter {filter_key}` — "
            f"**{AUDIO_EFFECT_NAMES[filter_key]}**: "
            f"{filter_descriptions[filter_key]}"
        )

    embed = discord.Embed(
        title="🎛️ قائمة الفلاتر الصوتية",
        description="\n".join(lines),
        color=discord.Color.purple()
    )

    embed.add_field(
        name="الفلتر الحالي",
        value=f"**{AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}**",
        inline=False
    )

    embed.set_footer(
        text="يتم تطبيق الفلتر على الأغنية التالية"
    )

    await ctx.send(embed=embed)
    return

effect = effect.lower().strip()

aliases = {
    "off": "off",
    "none": "off",
    "echo": "echo",
    "reverb": "reverb",
    "chorus": "chorus",
    "flanger": "flanger",
    "phaser": "phaser",
    "aphaser": "phaser",
    "haas": "haas",
    "surround": "surround",
    "8d": "eightd",
    "eightd": "eightd",
    "nightcore": "nightcore",
    "vaporwave": "vaporwave",
    "deepvoice": "deepvoice",
    "slow": "slow",
    "fast": "fast",
    "tremolo": "tremolo",
    "vibrato": "vibrato",
    "crystal": "crystal",
    "radio": "radio",
    "telephone": "telephone",
    "cinema": "cinema",
    "car": "car",
    "vocal": "vocal",
    "karaoke": "karaoke",
    "wide": "wide",
    "mono": "mono",
    "clean": "clean",

    "ايقاف": "off",
    "إيقاف": "off",
    "بدون": "off",
    "صدى": "echo",
    "ريفيرب": "reverb",
    "كورس": "chorus",
    "فلانجر": "flanger",
    "فايزر": "phaser",
    "توسيع": "haas",
    "محيطي": "surround",
    "ثماني": "eightd",
    "نايتكور": "nightcore",
    "فايبرويف": "vaporwave",
    "عميق": "deepvoice",
    "بطيء": "slow",
    "سريع": "fast",
    "تريمولو": "tremolo",
    "فيبراتو": "vibrato",
    "كريستال": "crystal",
    "راديو": "radio",
    "هاتف": "telephone",
    "تلفون": "telephone",
    "سينمائي": "cinema",
    "سيارة": "car",
    "غناء": "vocal",
    "كاريوكي": "karaoke",
    "واسع": "wide",
    "مونو": "mono",
    "نظيف": "clean",
    "تنظيف": "clean",
}

selected_effect = aliases.get(effect)

if selected_effect is None:
    available = "، ".join(
        f"`{name}`"
        for name in AUDIO_EFFECTS
    )

    await ctx.send(
        "❌ الفلتر غير معروف.\n\n"
        f"الفلاتر المتاحة:\n{available}\n\n"
        "اكتب `$filter` لعرض التفاصيل."
    )
    return

AUDIO_EFFECT = selected_effect

await ctx.send(
    "🎛️ تم تغيير الفلتر إلى: "
    f"**{AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}**\n"
    "ℹ️ سيتم تطبيقه على الأغنية التالية."
)
@bot.command(name="loop")
async def loop_song(ctx):
global LOOP

if not ctx.voice_client:
    await ctx.send(
        "❌ البوت غير موجود في روم صوتي."
    )
    return

if current_song is None:
    await ctx.send(
        "❌ لا توجد أغنية حالية لتكرارها."
    )
    return

LOOP = not LOOP

if LOOP:
    await ctx.send(
        f"🔁 تم تفعيل تكرار: "
        f"**{current_song['title']}**"
    )
else:
    await ctx.send(
        "⏹️ تم إيقاف تكرار الأغنية."
    )
@bot.command(name="volume")
async def change_volume(ctx, volume: int):
global VOLUME

if volume < 0 or volume > 100:
    await ctx.send(
        "❌ اختر مستوى صوت من 0 إلى 100."
    )
    return

VOLUME = volume / 100

voice = ctx.voice_client

if voice and isinstance(
    voice.source,
    discord.PCMVolumeTransformer
):
    voice.source.volume = VOLUME

await ctx.send(
    f"🔊 تم تغيير مستوى الصوت إلى "
    f"**{volume}%**."
)
@change_volume.error
async def volume_error(ctx, error):
if isinstance(
error,
commands.MissingRequiredArgument
):
await ctx.send(
"❌ اكتب مستوى الصوت.\n"
"مثال: $volume 50"
)

elif isinstance(error, commands.BadArgument):
    await ctx.send(
        "❌ مستوى الصوت يجب أن يكون "
        "رقمًا من 0 إلى 100."
    )

else:
    print(f"Volume error: {error}")
@bot.command(name="تخطي", aliases=["skip"])
async def skip(ctx):
global current_song

voice = ctx.voice_client

if voice and (
    voice.is_playing() or voice.is_paused()
):
    current_song = None
    voice.stop()

    await ctx.send(
        "⏭️ تم تخطي الأغنية."
    )
else:
    await ctx.send(
        "❌ لا توجد أغنية تعمل."
    )
@bot.command(name="pause")
async def pause(ctx):
voice = ctx.voice_client

if voice and voice.is_playing():
    voice.pause()

    await ctx.send(
        "⏸️ تم إيقاف الأغنية مؤقتًا."
    )
else:
    await ctx.send(
        "❌ لا توجد أغنية تعمل."
    )
@bot.command(name="resume")
async def resume(ctx):
voice = ctx.voice_client

if voice and voice.is_paused():
    voice.resume()

    await ctx.send(
        "▶️ تم استكمال الأغنية."
    )
else:
    await ctx.send(
        "❌ لا توجد أغنية متوقفة مؤقتًا."
    )
@bot.command(name="stop")
async def stop(ctx):
global current_song, LOOP, MANUAL_STOP

voice = ctx.voice_client

queue.clear()
current_song = None
LOOP = False
MANUAL_STOP = True

if voice and (
    voice.is_playing() or voice.is_paused()
):
    voice.stop()

await set_music_presence()

await ctx.send(
    "⏹️ تم إيقاف التشغيل ومسح قائمة الانتظار."
)
@bot.command(
name="autoplay",
aliases=["تلقائي", "تشغيل_تلقائي"]
)
async def autoplay_command(ctx, mode: str = None):
"""عرض أو تغيير حالة التشغيل التلقائي."""
global AUTOPLAY, MANUAL_STOP

if mode is None:
    status = "مفعّل" if AUTOPLAY else "متوقف"

    await ctx.send(
        f"♾️ التشغيل التلقائي حاليًا: **{status}**\n"
        "استخدم `$autoplay on` أو `$autoplay off`."
    )
    return

aliases = {
    "on": True,
    "enable": True,
    "تشغيل": True,
    "تفعيل": True,
    "مفعل": True,
    "مفعّل": True,
    "off": False,
    "disable": False,
    "ايقاف": False,
    "إيقاف": False,
    "تعطيل": False,
    "متوقف": False,
}

selected = aliases.get(mode.lower().strip())

if selected is None:
    await ctx.send(
        "❌ استخدم `$autoplay on` أو `$autoplay off`."
    )
    return

AUTOPLAY = selected

if AUTOPLAY:
    MANUAL_STOP = False
    await ctx.send("♾️ تم تفعيل التشغيل التلقائي.")
else:
    await ctx.send("⏹️ تم إيقاف التشغيل التلقائي.")
@bot.command(name="queue")
async def show_queue(ctx):
if not queue:
await ctx.send(
"📋 قائمة الانتظار فارغة."
)
return

description = ""

for index, song in enumerate(
    queue,
    start=1
):
    line = (
        f"**{index}.** "
        f"{song['title']}\n"
    )

    if len(description) + len(line) > 3900:
        description += "\n… توجد أغاني أخرى."
        break

    description += line

embed = discord.Embed(
    title=(
        f"📋 قائمة الانتظار "
        f"— {len(queue)} أغنية"
    ),
    description=description,
    color=discord.Color.blue()
)

embed.add_field(
    name="🎚️ الباس الحالي",
    value=f"**{BASS_NAMES[BASS_MODE]}**",
    inline=True
)

embed.add_field(
    name="🎛️ الفلتر الحالي",
    value=f"**{AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}**",
    inline=True
)

await ctx.send(embed=embed)
@bot.command(name="مسح")
async def clear_queue(ctx):
queue.clear()

await ctx.send(
    "🗑️ تم مسح قائمة الانتظار بالكامل."
)
@bot.command(name="حذف")
async def remove_from_queue(
ctx,
position: int
):
if not queue:
await ctx.send(
"📋 قائمة الانتظار فارغة."
)
return

if position < 1 or position > len(queue):
    await ctx.send(
        f"❌ اختر رقمًا من 1 إلى "
        f"{len(queue)}."
    )
    return

removed_song = queue.pop(
    position - 1
)

await ctx.send(
    f"🗑️ تم حذف "
    f"**{removed_song['title']}** "
    f"من قائمة الانتظار."
)
@remove_from_queue.error
async def remove_error(ctx, error):
if isinstance(
error,
commands.MissingRequiredArgument
):
await ctx.send(
"❌ اكتب رقم الأغنية.\n"
"مثال: $حذف 2"
)

elif isinstance(error, commands.BadArgument):
    await ctx.send(
        "❌ يجب كتابة رقم صحيح."
    )

else:
    print(f"Remove error: {error}")
============================================================
لوحة التحكم التفاعلية
============================================================
MENU_COLOR = discord.Color.from_rgb(126, 70, 255)

def create_dashboard_embed(user):
"""إنشاء الصفحة الرئيسية للوحة التحكم."""
song_title = (
current_song["title"]
if current_song
else "لا توجد أغنية تعمل حاليًا"
)

loop_status = "مفعّل" if LOOP else "متوقف"

embed = discord.Embed(
    title="🎵 لوحة تحكم بوت الموسيقى",
    description=(
        "مرحبًا بك في لوحة التحكم التفاعلية.\n"
        "اختر قسمًا من القائمة أو استخدم أزرار التحكم السريع."
    ),
    color=MENU_COLOR
)

embed.add_field(
    name="🎶 الأغنية الحالية",
    value=f"**{song_title}**",
    inline=False
)

embed.add_field(
    name="🔊 مستوى الصوت",
    value=f"**{int(VOLUME * 100)}%**",
    inline=True
)

embed.add_field(
    name="🎚️ الباس",
    value=f"**{BASS_NAMES[BASS_MODE]}**",
    inline=True
)

embed.add_field(
    name="🎛️ الفلتر",
    value=f"**{AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}**",
    inline=True
)

embed.add_field(
    name="🔁 التكرار",
    value=f"**{loop_status}**",
    inline=True
)

embed.add_field(
    name="📋 قائمة الانتظار",
    value=f"**{len(queue)} أغنية**",
    inline=True
)

embed.add_field(
    name="♾️ التشغيل التلقائي",
    value="**مفعّل**" if AUTOPLAY else "**متوقف**",
    inline=True
)

embed.add_field(
    name="🟣 حالة البوت",
    value="**جاهز للتحكم**",
    inline=True
)

embed.set_thumbnail(url=user.display_avatar.url)

embed.set_footer(
    text="✨ اختر قسمًا من القائمة الموجودة بالأسفل"
)

return embed
def create_section_embed(section, user):
"""إنشاء صفحات أقسام لوحة التحكم."""
section_data = {
"playback": {
"title": "🎵 أوامر التشغيل",
"color": discord.Color.from_rgb(184, 80, 255),
"description": (
"$play اسم الأغنية — تشغيل أغنية أو إضافتها للقائمة\n"
"$pause — إيقاف مؤقت\n"
"$resume — استكمال التشغيل\n"
"$skip — تخطي الأغنية الحالية\n"
"$stop — إيقاف التشغيل ومسح القائمة\n"
"$loop — تشغيل أو إيقاف التكرار\n"
"$autoplay on/off — تشغيل أو إيقاف Autoplay"
)
},
"queue": {
"title": "📋 قائمة الانتظار",
"color": discord.Color.from_rgb(45, 155, 255),
"description": (
"$queue — عرض قائمة الانتظار\n"
"$حذف 2 — حذف الأغنية رقم 2\n"
"$مسح — مسح جميع الأغاني المنتظرة"
)
},
"audio": {
"title": "🔊 الصوت والباس",
"color": discord.Color.from_rgb(62, 214, 116),
"description": (
"$volume 50 — تغيير الصوت من 0 إلى 100\n"
"$bass off — إيقاف الباس\n"
"$bass normal — باس عادي\n"
"$bass strong — باس قوي\n"
"$bass extreme — باس قوي جدًا"
)
},
"filters": {
"title": "🎛️ الفلاتر والمؤثرات",
"color": discord.Color.from_rgb(255, 165, 40),
"description": (
"$filter — عرض جميع الفلاتر\n"
"$filter echo — صدى\n"
"$filter reverb — ريفيرب\n"
"$filter eightd — صوت 8D\n"
"$filter nightcore — نايتكور\n"
"$filter cinema — صوت سينمائي\n"
"$filter clean — تنظيف الصوت\n"
"$filter off — إيقاف الفلتر"
)
},
"voice": {
"title": "🎙️ الاتصال الصوتي",
"color": discord.Color.from_rgb(255, 75, 153),
"description": (
"$vjoin123 — دخول البوت إلى رومك\n"
"$leave123 — خروج البوت ومسح القائمة"
)
},
"info": {
"title": "ℹ️ معلومات البوت",
"color": discord.Color.from_rgb(60, 220, 220),
"description": (
f"الصوت الحالي: {int(VOLUME * 100)}%\n"
f"الباس الحالي: {BASS_NAMES[BASS_MODE]}\n"
f"الفلتر الحالي: {AUDIO_EFFECT_NAMES[AUDIO_EFFECT]}\n"
f"الأغاني المنتظرة: {len(queue)}\n"
f"التكرار: {'مفعّل' if LOOP else 'متوقف'}\n"
f"التشغيل التلقائي: "
f"{'مفعّل' if AUTOPLAY else 'متوقف'}"
)
}
}

data = section_data[section]

embed = discord.Embed(
    title=data["title"],
    description=data["description"],
    color=data["color"]
)

embed.set_thumbnail(url=user.display_avatar.url)
embed.set_footer(text="🏠 استخدم زر الرئيسية للعودة")

return embed
class DashboardSelect(discord.ui.Select):
"""قائمة أقسام لوحة التحكم."""

def __init__(self):
    options = [
        discord.SelectOption(
            label="التشغيل",
            value="playback",
            description="تشغيل وإيقاف وتخطي الأغاني",
            emoji="🎵"
        ),
        discord.SelectOption(
            label="قائمة الانتظار",
            value="queue",
            description="عرض وحذف الأغاني المنتظرة",
            emoji="📋"
        ),
        discord.SelectOption(
            label="الصوت والباس",
            value="audio",
            description="التحكم بمستوى الصوت والباس",
            emoji="🔊"
        ),
        discord.SelectOption(
            label="الفلاتر والمؤثرات",
            value="filters",
            description="عرض الفلاتر الصوتية",
            emoji="🎛️"
        ),
        discord.SelectOption(
            label="الاتصال الصوتي",
            value="voice",
            description="دخول وخروج البوت",
            emoji="🎙️"
        ),
        discord.SelectOption(
            label="معلومات البوت",
            value="info",
            description="عرض الحالة والإعدادات الحالية",
            emoji="ℹ️"
        ),
    ]

    super().__init__(
        placeholder="✨ اختر قسمًا من لوحة التحكم",
        min_values=1,
        max_values=1,
        options=options,
        row=0
    )

async def callback(self, interaction: discord.Interaction):
    view = self.view

    if view is None:
        return

    embed = create_section_embed(
        self.values[0],
        interaction.user
    )

    await interaction.response.edit_message(
        embed=embed,
        view=view
    )
class DashboardView(discord.ui.View):
"""لوحة التحكم الرئيسية."""

def __init__(self, author_id):
    super().__init__(timeout=300)
    self.author_id = author_id
    self.message = None
    self.add_item(DashboardSelect())

async def interaction_check(self, interaction):
    if interaction.user.id != self.author_id:
        await interaction.response.send_message(
            "❌ هذه اللوحة تخص الشخص الذي فتحها.",
            ephemeral=True
        )
        return False

    return True

def get_voice(self, interaction):
    if interaction.guild is None:
        return None

    return interaction.guild.voice_client

async def require_same_voice(self, interaction):
    if not interaction.user.voice:
        await interaction.response.send_message(
            "❌ ادخل إلى روم صوتي أولًا.",
            ephemeral=True
        )
        return None

    voice = self.get_voice(interaction)

    if voice is None:
        await interaction.response.send_message(
            "❌ البوت غير موجود داخل روم صوتي.",
            ephemeral=True
        )
        return None

    if interaction.user.voice.channel != voice.channel:
        await interaction.response.send_message(
            "❌ يجب أن تكون في نفس روم البوت.",
            ephemeral=True
        )
        return None

    return voice

@discord.ui.button(
    label="تشغيل/إيقاف",
    emoji="⏯️",
    style=discord.ButtonStyle.primary,
    row=1
)
async def pause_resume_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    voice = await self.require_same_voice(interaction)

    if voice is None:
        return

    if voice.is_playing():
        voice.pause()
    elif voice.is_paused():
        voice.resume()
    else:
        await interaction.response.send_message(
            "❌ لا توجد أغنية تعمل حاليًا.",
            ephemeral=True
        )
        return

    await interaction.response.edit_message(
        embed=create_dashboard_embed(interaction.user),
        view=self
    )

@discord.ui.button(
    label="تخطي",
    emoji="⏭️",
    style=discord.ButtonStyle.secondary,
    row=1
)
async def skip_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global current_song

    voice = await self.require_same_voice(interaction)

    if voice is None:
        return

    if not (voice.is_playing() or voice.is_paused()):
        await interaction.response.send_message(
            "❌ لا توجد أغنية تعمل.",
            ephemeral=True
        )
        return

    current_song = None
    voice.stop()

    await interaction.response.send_message(
        "⏭️ تم تخطي الأغنية.",
        ephemeral=True
    )

@discord.ui.button(
    label="تكرار",
    emoji="🔁",
    style=discord.ButtonStyle.success,
    row=1
)
async def loop_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global LOOP

    voice = await self.require_same_voice(interaction)

    if voice is None:
        return

    if current_song is None:
        await interaction.response.send_message(
            "❌ لا توجد أغنية حالية لتكرارها.",
            ephemeral=True
        )
        return

    LOOP = not LOOP

    await interaction.response.edit_message(
        embed=create_dashboard_embed(interaction.user),
        view=self
    )

@discord.ui.button(
    label="إيقاف",
    emoji="⏹️",
    style=discord.ButtonStyle.danger,
    row=1
)
async def stop_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global current_song, LOOP, MANUAL_STOP

    voice = await self.require_same_voice(interaction)

    if voice is None:
        return

    queue.clear()
    current_song = None
    LOOP = False
    MANUAL_STOP = True

    if voice.is_playing() or voice.is_paused():
        voice.stop()

    await set_music_presence()

    await interaction.response.edit_message(
        embed=create_dashboard_embed(interaction.user),
        view=self
    )

@discord.ui.button(
    label="الرئيسية",
    emoji="🏠",
    style=discord.ButtonStyle.secondary,
    row=1
)
async def home_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    await interaction.response.edit_message(
        embed=create_dashboard_embed(interaction.user),
        view=self
    )

@discord.ui.button(
    label="تشغيل تلقائي",
    emoji="♾️",
    style=discord.ButtonStyle.primary,
    row=2
)
async def autoplay_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    global AUTOPLAY, MANUAL_STOP

    AUTOPLAY = not AUTOPLAY

    if AUTOPLAY:
        MANUAL_STOP = False
        button.style = discord.ButtonStyle.success
    else:
        button.style = discord.ButtonStyle.secondary

    await interaction.response.edit_message(
        embed=create_dashboard_embed(interaction.user),
        view=self
    )

@discord.ui.button(
    label="تحديث",
    emoji="🔄",
    style=discord.ButtonStyle.secondary,
    row=2
)
async def refresh_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    await interaction.response.edit_message(
        embed=create_dashboard_embed(interaction.user),
        view=self
    )

@discord.ui.button(
    label="إغلاق",
    emoji="✖️",
    style=discord.ButtonStyle.danger,
    row=2
)
async def close_dashboard_button(
    self,
    interaction: discord.Interaction,
    button: discord.ui.Button
):
    for item in self.children:
        item.disabled = True

    await interaction.response.edit_message(
        content="🔒 تم إغلاق لوحة التحكم.",
        embed=None,
        view=self
    )

async def on_timeout(self):
    for item in self.children:
        item.disabled = True

    if self.message is not None:
        try:
            await self.message.edit(view=self)
        except discord.HTTPException:
            pass
@bot.command(
name="menu",
aliases=["قائمة", "اوامر", "أوامر", "help", "مساعدة"]
)
async def dashboard_command(ctx):
"""فتح لوحة التحكم التفاعلية."""
view = DashboardView(ctx.author.id)

message = await ctx.send(
    embed=create_dashboard_embed(ctx.author),
    view=view
)

view.message = message
@bot.event
async def on_command_error(ctx, error):
"""إظهار أخطاء الأوامر بوضوح."""
if isinstance(error, commands.CommandNotFound):
return

if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("❌ يوجد جزء ناقص في الأمر.")
    return

print(f"Command error: {type(error).__name__}: {error}")

await ctx.send(
    f"❌ حدث خطأ: `{type(error).__name__}`"
)
if not TOKEN:
raise RuntimeError(
"لم يتم العثور على DISCORD_TOKEN. "
"أضف توكن البوت إلى متغيرات البيئة."
)

bot.run(TOKEN)


إغلاق
