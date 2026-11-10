"""AI phrase generation with permanent no-repeat history."""

from __future__ import annotations

import json
import random
import time
from datetime import datetime

import requests

import config
from config import CATEGORIES, CATEGORIES_NATIVE, HISTORY_DIR, MAX_RECENT_CATEGORIES

PHRASE_HISTORY_FILE = HISTORY_DIR / "all_generated_phrases.json"
RECENT_CATEGORIES_FILE = HISTORY_DIR / "recent_categories.json"

PHRASE_KEY = config.LANGUAGE["history_key"]
LANGUAGE_NAME = config.LANGUAGE["name"]
NATIVE_NAME = config.LANGUAGE["native_name"]

# ==== FALLBACK PHRASES START ====
FALLBACK_PHRASES = [
    {"english": "Stop waiting. Start now.", "native": "Deja de esperar. Comienza ahora.", "transliteration": ""},
    {"english": "This is why you're stuck.", "native": "Por esto estás atascado.", "transliteration": ""},
    {"english": "The secret? Consistency wins.", "native": "¿El secreto? La constancia gana.", "transliteration": ""},
    {"english": "What nobody tells you about success.", "native": "Lo que nadie te dice del éxito.", "transliteration": ""},
    {"english": "Your future self is watching.", "native": "Tu yo futuro te mira.", "transliteration": ""},
    {"english": "Stop saying 'someday'. Say 'today'.", "native": "Deja de decir 'algún día'. Di 'hoy'.", "transliteration": ""},
    {"english": "Stop chasing. Real love finds you.", "native": "Deja de perseguir. El amor real te encuentra.", "transliteration": ""},
    {"english": "This is what real love feels.", "native": "Así se siente el amor verdadero.", "transliteration": ""},
    {"english": "The secret to being deeply loved.", "native": "El secreto para ser amado.", "transliteration": ""},
    {"english": "What nobody tells you about heartbreak.", "native": "Lo que nadie te dice del desamor.", "transliteration": ""},
    {"english": "You deserve this kind of love.", "native": "Mereces este tipo de amor.", "transliteration": ""},
    {"english": "Never settle for less.", "native": "Nunca te conformes con menos.", "transliteration": ""},
    {"english": "Stop this if you want success.", "native": "Deja esto si quieres éxito.", "transliteration": ""},
    {"english": "The one habit that changes everything.", "native": "El hábito que lo cambia todo.", "transliteration": ""},
    {"english": "What successful people do before 8am.", "native": "Lo que hace la gente exitosa temprano.", "transliteration": ""},
    {"english": "This mindset shift changes lives.", "native": "Este cambio mental cambia vidas.", "transliteration": ""},
    {"english": "Why you're not seeing results.", "native": "Por qué no ves resultados.", "transliteration": ""},
    {"english": "The truth about overnight success.", "native": "La verdad sobre el éxito repentino.", "transliteration": ""},
    {"english": "Stop overthinking. Start doing.", "native": "Deja de pensar. Empieza a hacer.", "transliteration": ""},
    {"english": "The lesson life keeps teaching.", "native": "La lección que la vida enseña.", "transliteration": ""},
    {"english": "What I wish I knew at 20.", "native": "Lo que desearía saber a los 20.", "transliteration": ""},
    {"english": "This truth will set you free.", "native": "Esta verdad te liberará.", "transliteration": ""},
    {"english": "The price of staying the same.", "native": "El precio de permanecer igual.", "transliteration": ""},
    {"english": "Why wise people stay quiet.", "native": "Por qué la gente sabia calla.", "transliteration": ""},
    {"english": "Stop looking for happiness there.", "native": "Deja de buscar la felicidad ahí.", "transliteration": ""},
    {"english": "This simple trick boosts joy.", "native": "Este truco simple aumenta la alegría.", "transliteration": ""},
    {"english": "What happy people do differently.", "native": "Lo que hace la gente feliz diferente.", "transliteration": ""},
    {"english": "The real source of lasting happiness.", "native": "La fuente real de felicidad duradera.", "transliteration": ""},
    {"english": "You're one choice away from joy.", "native": "Estás a una elección de la alegría.", "transliteration": ""},
    {"english": "Stop waiting. Choose happiness now.", "native": "Deja de esperar. Elige felicidad ahora.", "transliteration": ""},
    {"english": "This one change transformed me.", "native": "Este único cambio me transformó.", "transliteration": ""},
    {"english": "Stop wasting time on this.", "native": "Deja de perder tiempo en esto.", "transliteration": ""},
    {"english": "The 1% rule that changes lives.", "native": "La regla del 1% cambia vidas.", "transliteration": ""},
    {"english": "What I do every morning.", "native": "Lo que hago cada mañana.", "transliteration": ""},
    {"english": "Your comfort zone is killing you.", "native": "Tu zona de confort te mata.", "transliteration": ""},
    {"english": "Become who you were meant to be.", "native": "Conviértete en quien debías ser.", "transliteration": ""},
    {"english": "This practice changed my life.", "native": "Esta práctica cambió mi vida.", "transliteration": ""},
    {"english": "Stop scrolling. Count your blessings.", "native": "Deja de desplazarte. Cuenta bendiciones.", "transliteration": ""},
    {"english": "What grateful people do daily.", "native": "Lo que hace la gente agradecida diariamente.", "transliteration": ""},
    {"english": "The fastest way to feel abundant.", "native": "La forma más rápida de sentirse abundante.", "transliteration": ""},
    {"english": "Say this every morning for 30 days.", "native": "Di esto cada mañana por 30 días.", "transliteration": ""},
    {"english": "Gratitude turns what we have into enough.", "native": "La gratitud convierte lo tenemos en suficiente.", "transliteration": ""},
    {"english": "Real friends do this without asking.", "native": "Los amigos reales hacen esto sin pedir.", "transliteration": ""},
    {"english": "Stop calling these people friends.", "native": "Deja de llamar amigos a estas personas.", "transliteration": ""},
    {"english": "The test of true friendship.", "native": "La prueba de la verdadera amistad.", "transliteration": ""},
    {"english": "What I learned about loyalty.", "native": "Lo que aprendí sobre la lealtad.", "transliteration": ""},
    {"english": "Keep these people close forever.", "native": "Mantén a estas personas cerca siempre.", "transliteration": ""},
    {"english": "A friend who does this is rare.", "native": "Un amigo que hace esto es raro.", "transliteration": ""},
    {"english": "When everything fails, remember this.", "native": "Cuando todo falla, recuerda esto.", "transliteration": ""},
    {"english": "Stop believing this lie about hope.", "native": "Deja de creer esta mentira sobre esperanza.", "transliteration": ""},
    {"english": "The dawn always comes after darkness.", "native": "El amanecer siempre llega después oscuridad.", "transliteration": ""},
    {"english": "What keeps me going when quitting.", "native": "Lo que me mantiene siguiendo cuando rindo.", "transliteration": ""},
    {"english": "Your breakthrough is closer than think.", "native": "Tu avance está más cerca piensas.", "transliteration": ""},
    {"english": "Never lose faith. This too shall pass.", "native": "Nunca pierdas fe. Esto también pasará.", "transliteration": ""},
    {"english": "Stop waiting for inspiration. Do.", "native": "Deja de esperar inspiración. Haz.", "transliteration": ""},
    {"english": "The secret to endless creative ideas.", "native": "El secreto para ideas creativas infinitas.", "transliteration": ""},
    {"english": "What artists know that others don't.", "native": "Lo que los artistas saben otros no.", "transliteration": ""},
    {"english": "Your creativity is hiding here.", "native": "Tu creatividad se está escondiendo aquí.", "transliteration": ""},
    {"english": "Break these rules to be creative.", "native": "Rompe estas reglas para ser creativo.", "transliteration": ""},
    {"english": "Create first, edit later. Trust.", "native": "Crea primero, edita después. Confía.", "transliteration": ""},
    {"english": "Stop letting them steal your peace.", "native": "Deja de dejarles robar tu paz.", "transliteration": ""},
    {"english": "This breathing trick calms anxiety.", "native": "Este truco respiración calma ansiedad.", "transliteration": ""},
    {"english": "What I do when mind races.", "native": "Lo que hago cuando mente corre.", "transliteration": ""},
    {"english": "The price of inner peace.", "native": "El precio de la paz interior.", "transliteration": ""},
    {"english": "Let go of what you can't control.", "native": "Suelta lo que no puedes controlar.", "transliteration": ""},
    {"english": "Your calm mind is your superpower.", "native": "Tu mente calmada es tu superpoder.", "transliteration": ""},
    {"english": "Stop this if you want confidence.", "native": "Deja esto si quieres confianza.", "transliteration": ""},
    {"english": "Fake confidence until you become it.", "native": "Finge confianza hasta que te conviertas.", "transliteration": ""},
    {"english": "The body language trick that works.", "native": "El truco lenguaje corporal que funciona.", "transliteration": ""},
    {"english": "What confident people never say.", "native": "Lo que la gente confiada nunca dice.", "transliteration": ""},
    {"english": "Your self-talk is shaping you.", "native": "Tu diálogo interno te está formando.", "transliteration": ""},
    {"english": "Stand tall. You're unstoppable.", "native": "Mantente firme. Eres imparable.", "transliteration": ""},
    {"english": "When you want to quit, read.", "native": "Cuando quieras rendirte, lee.", "transliteration": ""},
    {"english": "The pain you feel is growth.", "native": "El dolor que sientes es crecimiento.", "transliteration": ""},
    {"english": "Why most people give up soon.", "native": "Por qué la mayoría se rinde pronto.", "transliteration": ""},
    {"english": "This separates winners from losers.", "native": "Esto separa ganadores de perdedores.", "transliteration": ""},
    {"english": "Keep going. Your moment is coming.", "native": "Sigue yendo. Tu momento está llegando.", "transliteration": ""},
    {"english": "Champions are made in dark.", "native": "Los campeones se hacen oscuridad.", "transliteration": ""},
    {"english": "This message found you for reason.", "native": "Este mensaje te encontró por razón.", "transliteration": ""},
    {"english": "Stop doubting. You were chosen.", "native": "Deja de dudar. Fuiste elegido.", "transliteration": ""},
    {"english": "The world needs your unique gift.", "native": "El mundo necesita tu regalo único.", "transliteration": ""},
    {"english": "What I learned from lowest point.", "native": "Lo que aprendí desde punto más bajo.", "transliteration": ""},
    {"english": "Your comeback will be legendary.", "native": "Tu regreso será legendario.", "transliteration": ""},
    {"english": "Be the person you needed younger.", "native": "Sé persona que necesitabas cuando joven.", "transliteration": ""},
    {"english": "Cut these toxic habits from life.", "native": "Corta estos hábitos tóxicos vida.", "transliteration": ""},
    {"english": "The mindset that attracts good things.", "native": "La mentalidad que atrae cosas buenas.", "transliteration": ""},
    {"english": "Stop consuming. Start creating.", "native": "Deja de consumir. Empieza a crear.", "transliteration": ""},
    {"english": "Your vibe attracts your tribe.", "native": "Tu vibra atrae a tu tribu.", "transliteration": ""},
    {"english": "Choose progress over perfection always.", "native": "Elige progreso sobre perfección siempre.", "transliteration": ""},
    {"english": "Good things happen to those who hustle.", "native": "Cosas buenas pasan a quienes trabajan duro.", "transliteration": ""},
    {"english": "Feel the fear. Do it anyway.", "native": "Siente el miedo. Hazlo todos modos.", "transliteration": ""},
    {"english": "This is what bravery really looks.", "native": "Así es como se ve valentía.", "transliteration": ""},
    {"english": "Stop hiding. The world needs seeing.", "native": "Deja de esconderte. Mundo necesita verte.", "transliteration": ""},
    {"english": "The risk you're avoiding is worth.", "native": "El riesgo que evitas vale pena.", "transliteration": ""},
    {"english": "Courage isn't fearlessness. It's this.", "native": "El coraje no es falta miedo. Es esto.", "transliteration": ""},
    {"english": "Take the leap. The net appears.", "native": "Da el salto. La red aparece.", "transliteration": ""},
    {"english": "This small act changed someone's day.", "native": "Este pequeño acto cambió día alguien.", "transliteration": ""},
    {"english": "Stop underestimating power of kindness.", "native": "Deja de subestimar poder amabilidad.", "transliteration": ""},
    {"english": "What happens when you choose kindness.", "native": "Lo que pasa eliges amabilidad.", "transliteration": ""},
    {"english": "Your kindness is your superpower.", "native": "Tu amabilidad es tu superpoder.", "transliteration": ""},
    {"english": "The ripple effect one kind word.", "native": "El efecto dominó una palabra amable.", "transliteration": ""},
    {"english": "Be the reason someone smiles today.", "native": "Sé razón por la que alguien sonríe.", "transliteration": ""},
    {"english": "Stop rushing. Trust the timing.", "native": "Deja de apresurarte. Confía tiempo.", "transliteration": ""},
    {"english": "This is why patience tested.", "native": "Por esto es paciencia probada.", "transliteration": ""},
    {"english": "The art of waiting without suffering.", "native": "El arte esperar sin sufrir.", "transliteration": ""},
    {"english": "What patient people know you don't.", "native": "Lo que sabe gente paciente tú no.", "transliteration": ""},
    {"english": "Good things come to those who wait.", "native": "Cosas buenas vienen quienes esperan.", "transliteration": ""},
    {"english": "Your seeds growing underground. Be patient.", "native": "Semillas creciendo bajo tierra. Sé paciente.", "transliteration": ""},
    {"english": "Holding grudges poisoning you. Let go.", "native": "Guardar rencores envenena. Suelta.", "transliteration": ""},
    {"english": "This is what forgiveness really means.", "native": "Esto es lo significa perdón.", "transliteration": ""},
    {"english": "Stop waiting apology won't come.", "native": "Deja esperar disculpa no vendrá.", "transliteration": ""},
    {"english": "The freedom feel after forgiving.", "native": "La libertad sientes después perdonar.", "transliteration": ""},
    {"english": "Forgive them not for them, for you.", "native": "Perdona no por ellos, por ti.", "transliteration": ""},
    {"english": "Your healing starts moment you forgive.", "native": "Sanación comienza momento perdonas.", "transliteration": ""},
    {"english": "You're stronger than realize. Here's proof.", "native": "Eres más fuerte das cuenta. Prueba.", "transliteration": ""},
    {"english": "This is how warriors made.", "native": "Así es como hacen guerreros.", "transliteration": ""},
    {"english": "Stop apologizing for being powerful.", "native": "Deja disculparte por ser poderoso.", "transliteration": ""},
    {"english": "The storm didn't break. Refined.", "native": "Tormenta no rompió. Refinó.", "transliteration": ""},
    {"english": "Your scars proof survival. Wear proudly.", "native": "Cicatrices prueba supervivencia. Lleva orgullo.", "transliteration": ""},
    {"english": "Bend but never break. That's resilience.", "native": "Dóblate pero nunca rompas. Resiliencia.", "transliteration": ""},
    {"english": "Stop postponing joy. Celebrate now.", "native": "Deja posponer alegría. Celebra ahora.", "transliteration": ""},
    {"english": "This is what pure joy feels.", "native": "Así es como siente alegría pura.", "transliteration": ""},
    {"english": "Find joy ordinary. It's magic.", "native": "Encuentra alegría ordinario. Mágico.", "transliteration": ""},
    {"english": "What joyful people do you don't.", "native": "Lo que hace gente alegre tú no.", "transliteration": ""},
    {"english": "Your joy is act resistance.", "native": "Alegría es acto resistencia.", "transliteration": ""},
    {"english": "Dance through life nobody's watching.", "native": "Baila vida como si nadie viera.", "transliteration": ""},
    {"english": "Stop burning out. Find rhythm.", "native": "Deja quemarte. Encuentra ritmo.", "transliteration": ""},
    {"english": "This work-life balance really looks.", "native": "Así equilibrio trabajo-vida realmente.", "transliteration": ""},
    {"english": "Secret having all without losing yourself.", "native": "Secreto tenerlo todo sin perderte.", "transliteration": ""},
    {"english": "Can't pour from empty cup. Fill.", "native": "No servir desde taza vacía. Llena.", "transliteration": ""},
    {"english": "Rest productive. Stop feeling guilty.", "native": "Descansar productivo. Deja sentirte culpable.", "transliteration": ""},
    {"english": "Find center. Everything else aligns.", "native": "Encuentra centro. Todo demás alinea.", "transliteration": ""},
    {"english": "This discomfort feel? That's growth.", "native": "¿Incomodidad sientes? Eso crecimiento.", "transliteration": ""},
    {"english": "Stop playing small. Meant more.", "native": "Deja jugar pequeño. Creado más.", "transliteration": ""},
    {"english": "Person becoming worth pain.", "native": "Persona conviertes vale pena.", "transliteration": ""},
    {"english": "What growing pains teach you.", "native": "Dolores crecimiento intentan enseñan.", "transliteration": ""},
    {"english": "Embrace suck. It's temporary.", "native": "Abraza difícil. Temporal.", "transliteration": ""},
    {"english": "Potential unlimited. Start acting.", "native": "Potencial ilimitado. Empieza actuar.", "transliteration": ""},
    {"english": "Stop searching. Purpose already here.", "native": "Deja buscar. Propósito ya aquí.", "transliteration": ""},
    {"english": "This is why feel unfulfilled.", "native": "Por esto es sientes insatisfecho.", "transliteration": ""},
    {"english": "Intersection joy service purpose.", "native": "Intersección alegría servicio propósito.", "transliteration": ""},
    {"english": "What meant do find you.", "native": "Lo destinado hacer encontrará.", "transliteration": ""},
    {"english": "Live intention live regret.", "native": "Vive intención vive arrepentimiento.", "transliteration": ""},
    {"english": "Legacy starts today's choices.", "native": "Legado comienza elecciones hoy.", "transliteration": ""},
    {"english": "Stop living autopilot. Wake now.", "native": "Deja vivir piloto automático. Despierta.", "transliteration": ""},
    {"english": "This moment all truly have.", "native": "Momento todo realmente tienes.", "transliteration": ""},
    {"english": "Present called gift reason.", "native": "Presente llama regalo razón.", "transliteration": ""},
    {"english": "What mindfulness does brain.", "native": "Atención plena hace cerebro.", "transliteration": ""},
    {"english": "Breathe. This only moment exists.", "native": "Respira. Este único momento existe.", "transliteration": ""},
    {"english": "Mind tool. Master it.", "native": "Mente herramienta. Domínala.", "transliteration": ""},
    {"english": "Where is the train station?", "native": "¿Dónde está la estación de tren?", "transliteration": ""},
    {"english": "I would like a coffee, please.", "native": "Quisiera un café, por favor.", "transliteration": ""},
    {"english": "How much does this cost?", "native": "¿Cuánto cuesta esto?", "transliteration": ""},
    {"english": "Can you help me?", "native": "¿Puede ayudarme?", "transliteration": ""},
    {"english": "I don't understand.", "native": "No entiendo.", "transliteration": ""},
    {"english": "Can you speak more slowly?", "native": "¿Puede hablar más despacio?", "transliteration": ""},
    {"english": "The weather is beautiful today.", "native": "Hace muy buen tiempo hoy.", "transliteration": ""},
    {"english": "I am learning Spanish.", "native": "Estoy aprendiendo español.", "transliteration": ""},
    {"english": "See you tomorrow.", "native": "Hasta mañana.", "transliteration": ""},
    {"english": "Thank you very much.", "native": "Muchas gracias.", "transliteration": ""},
]
# ==== FALLBACK PHRASES END ====


def _load_json(path, default):
    if path.exists():
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            pass
    return default


def _save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def load_phrase_history():
    data = _load_json(PHRASE_HISTORY_FILE, {"phrases": [], "last_updated": None})
    data.setdefault("phrases", [])
    return data


def save_phrase_history(data):
    data["last_updated"] = datetime.now().isoformat()
    _save_json(PHRASE_HISTORY_FILE, data)


def is_phrase_used(english):
    english_lower = english.lower().strip()
    for p in load_phrase_history()["phrases"]:
        if p.get("english", "").lower().strip() == english_lower:
            return True
    return False


def _history_native(p):
    for key in (PHRASE_KEY, "vietnamese", "native", "translation", "target"):
        value = p.get(key)
        if value:
            return str(value)
    return ""


def add_phrases_to_history(phrases, category):
    history = load_phrase_history()
    for phrase in phrases:
        history["phrases"].append({
            "english": phrase["english"],
            PHRASE_KEY: phrase["native"],
            "transliteration": phrase.get("transliteration", ""),
            "category": category,
            "generated_at": datetime.now().isoformat(),
        })
    save_phrase_history(history)
    print(f"[content] Saved {len(phrases)} phrases (history total: {len(history['phrases'])})")


def get_available_category():
    data = _load_json(RECENT_CATEGORIES_FILE, {"recent_categories": [], "last_updated": None})
    recent = data.get("recent_categories", [])
    available = [c for c in CATEGORIES if c not in recent]
    if not available:
        recent = recent[-5:]
        available = [c for c in CATEGORIES if c not in recent]
        print("[rotation] Reset recent categories")
    selected = random.choice(available)
    recent.append(selected)
    data["recent_categories"] = recent[-MAX_RECENT_CATEGORIES:]
    data["last_updated"] = datetime.now().isoformat()
    _save_json(RECENT_CATEGORIES_FILE, data)
    print(f"[rotation] Category: {selected} ({len(available)} available)")
    return selected


def _normalize_phrase(item):
    if not isinstance(item, dict):
        return None
    english = str(item.get("english", "")).strip()
    native = str(
        item.get(PHRASE_KEY)
        or item.get("native")
        or item.get("vietnamese")
        or item.get("translation")
        or ""
    ).strip()
    translit = str(item.get("transliteration") or item.get("romanization") or item.get("romaji") or "").strip()
    if not english or not native:
        return None
    if len(english.split()) > 16:
        return None
    if "/" in native or "|" in native:
        native = native.split("/")[0].split("|")[0].strip()
    return {
        "english": english.replace("  ", " ").strip(),
        "native": native.strip(),
        "transliteration": translit.strip().strip("[]"),
    }


def _history_keys(history):
    used_en = set()
    used_nat = set()
    for p in history.get("phrases", []):
        en = str(p.get("english", "")).lower().strip()
        nat = _history_native(p).lower().strip()
        if en:
            used_en.add(en)
        if nat:
            used_nat.add(nat)
    return used_en, used_nat


def generate_phrases(category_english: str, num_phrases: int = 5) -> list:
    category_native = CATEGORIES_NATIVE[category_english]
    history = load_phrase_history()
    used_en, used_nat = _history_keys(history)
    recent_english = [
        p["english"] for p in history["phrases"] if p.get("category") == category_english
    ][-30:]

    models = [config.AI_MODEL]
    if "gemini-fast" not in models:
        models.append("gemini-fast")

    if config.POLLINATIONS_API_KEY:
        for attempt in range(5):
            model = models[0] if attempt < 3 else models[-1]
            try:
                phrases = _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model)
                unique = []
                for item in phrases:
                    p = _normalize_phrase(item)
                    if not p:
                        continue
                    key_en = p["english"].lower().strip()
                    key_nat = p["native"].lower().strip()
                    if key_en in used_en or key_nat in used_nat:
                        continue
                    if any(key_en == u["english"].lower().strip() for u in unique):
                        continue
                    used_en.add(key_en)
                    used_nat.add(key_nat)
                    unique.append(p)
                    if len(unique) >= num_phrases:
                        break
                if len(unique) >= num_phrases:
                    add_phrases_to_history(unique[:num_phrases], category_english)
                    return unique[:num_phrases]
                print(f"[content] Attempt {attempt + 1}: only {len(unique)} fresh phrases (need {num_phrases})")
            except Exception as exc:  # noqa: BLE001 - network boundary
                print(f"[content] Attempt {attempt + 1} failed ({model}): {exc}")
            time.sleep(1.5 * (attempt + 1))
    else:
        print("[content] No POLLINATIONS_API_KEY, using fallback phrases")

    fresh_fallback = []
    for p in FALLBACK_PHRASES:
        if p["english"].lower().strip() in used_en or p["native"].lower().strip() in used_nat:
            continue
        fresh_fallback.append(p)
    if not fresh_fallback:
        raise RuntimeError("Phrase API unavailable and no unused fallback phrases left; refusing to reuse phrases")
    chosen = fresh_fallback[:num_phrases]
    if len(chosen) < num_phrases:
        print(f"[content] Only {len(chosen)} fresh fallback phrases; building a shorter lesson")
    add_phrases_to_history(chosen, category_english)
    return chosen


def _request_phrases(category_english, category_native, recent_english, num_phrases, attempt, model=None):
    avoid = ""
    if recent_english:
        avoid = "\nDo NOT reuse any of these phrases:\n" + "\n".join(f"- {p}" for p in recent_english)

    prompt = f"""Create {num_phrases * 6} unique {category_english} phrases for English speakers learning {LANGUAGE_NAME}.
{avoid}

Rules:
1. Keep every phrase short and natural (4-11 words in English).
2. Use natural commas for TTS breathing pauses.
3. Each phrase must be speakable in 2-4 seconds.
4. Write clean {LANGUAGE_NAME} in {NATIVE_NAME} with correct accents and orthography. One translation only, no slashes.
5. Transliteration is a friendly Roman-script pronunciation guide for English speakers (not IPA).
6. Vary the sentence patterns and emotions. No duplicates.
7. Phrases must feel like real everyday language, not textbook filler.

Return ONLY a JSON array:
[{{"english": "...", "native": "...", "transliteration": "..."}}]"""

    response = requests.post(
        "https://gen.pollinations.ai/v1/chat/completions",
        headers={
            "Authorization": f"Bearer {config.POLLINATIONS_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": model or config.AI_MODEL,
            "messages": [
                {"role": "system", "content": f"You are a {LANGUAGE_NAME} teacher creating short, natural, varied bilingual phrases. Reply with JSON only."},
                {"role": "user", "content": prompt},
            ],
            "temperature": min(0.95 + attempt * 0.02, 1.0),
        },
        timeout=90,
    )
    response.raise_for_status()
    content = response.json()["choices"][0]["message"]["content"].strip()

    if "```json" in content:
        content = content.split("```json", 1)[1].split("```", 1)[0].strip()
    elif "```" in content:
        content = content.split("```", 1)[1].split("```", 1)[0].strip()

    start = content.find("[")
    end = content.rfind("]")
    if start >= 0 and end > start:
        content = content[start:end + 1]

    data = json.loads(content)
    if not isinstance(data, list):
        raise ValueError("AI did not return a JSON array")
    return data
