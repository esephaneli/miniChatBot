import re
import ast
import operator as op
from datetime import datetime

# ---------- Yardımcılar ----------
STOPWORDS = {"ve","ile","da","de","mi","mı","mu","mü","bir","ya","ki","the","a","an"}
PUNCT_RE  = re.compile(r"[^\w\sçğıöşü.-]", flags=re.I)

def normalize(text: str) -> str:
    text = text.lower().strip()
    text = PUNCT_RE.sub("", text)
    return " ".join(w for w in text.split() if w not in STOPWORDS)

def contains_any(text: str, keywords: set) -> bool:
    return any(k in text for k in keywords)

# Basit durum: yapılacaklar listesi (bellekte)
todos = []

# ---------- Güvenli hesap makinesi ----------
OPS = {
    ast.Add: op.add, ast.Sub: op.sub, ast.Mult: op.mul, ast.Div: op.truediv,
    ast.Pow: op.pow, ast.USub: op.neg, ast.UAdd: op.pos, ast.Mod: op.mod
}

def _eval_expr(node):
    if isinstance(node, ast.Constant):
        return node.value
    if isinstance(node, ast.UnaryOp):
        return OPS[type(node.op)](_eval_expr(node.operand))
    if isinstance(node, ast.BinOp):
        if type(node.op) not in OPS:
            raise ValueError("İzin verilmeyen işlem")
        return OPS[type(node.op)](_eval_expr(node.left), _eval_expr(node.right))
    raise ValueError("İfade desteklenmiyor")

def safe_calc(expr: str):
    tree = ast.parse(expr, mode="eval")
    return _eval_expr(tree.body)

# ---------- Intent tanımları ----------
INTENTS = [
    {
        "name": "selam",
        "keywords": {"selam","merhaba","hey","slm","selamlar","naber","nasılsın"},
        "handler": lambda _: "Selam! Ben mini chatbot 'yardım' yazabilirsin."
    },
    {
        "name": "zaman",
        "keywords": {"saat","tarih","zaman","günlerden"},
        "handler": lambda _: f"Şu an: {datetime.now().strftime('%d.%m.%Y %H:%M')}"
    },
    {
        "name": "yardim",
        "keywords": {"yardım","komutlar","help","?"},
        "handler": lambda _: (
            "Komutlar:\n"
            "- 'hesapla 2+2*3'\n"
            "- 'todo ekle <metin>' / 'todo liste' / 'hepsini sil'\n"
            "- 'kimsin', 'selam', 'zaman', 'fıkra'\n"
            "- Çıkış: 'q', 'çık', 'exit'"
        )
    },
    {
        "name": "kimlik",
        "keywords": {"kimsin","nesin","adın ne","adın"},
        "handler": lambda _: "Ben kural tabanlı mini bir sohbet botuyum. Basit görevlerde yardımcı olurum!"
    },
    {
        "name": "fikra",
        "keywords": {"fıkra","şaka","espiri"},
        "handler": lambda _: "Bilgisayar neden üşümez? Çünkü içinde fan(atik) var "
    },
    # Hesap makinesi (safe_calc ile)
    {
        "name": "hesap",
        "keywords": {"hesapla"},
        "handler": lambda text: (
            (lambda expr: f"Sonuç: {safe_calc(expr)}")
            (text.split("hesapla",1)[1].strip() or "0")
        )
    },
    # TODO komutları (önce ekle, sonra liste/temizle)
    {
        "name": "todo_ekle",
        "keywords": {"todo ekle","yapılacak ekle","yapilacak ekle"},
        "handler": lambda text: (
            (lambda item: (todos.append(item), f"Eklendi : {item}"))(
                text.split("ekle",1)[1].strip() if "ekle" in text else ""
            )[1]
            if ("ekle" in text and text.split("ekle",1)[1].strip())
            else "Ne ekleyeyim? Örn: 'todo ekle sunum hazırla'"
        )
    },
    {
        "name": "todo_liste",
        "keywords": {"todo liste","yapılacaklar","yapilacaklar","todo"},
        "handler": lambda _: "Yapılacaklar boş." if not todos else (
            "Yapılacaklar:\n" + "\n".join(f"- {i+1}. {t}" for i,t in enumerate(todos))
        )
    },
    {
        "name": "todo_temizle",
        "keywords": {"hepsini sil","todo sıfırla","todo sifirla"},
        "handler": lambda _: (todos.clear(), "Tümü silindi ")[1]
    },
]

# ---------- Ana yönlendirici ----------
def handle(text_raw: str) -> str:
    text = normalize(text_raw)

    # Intent eşleştirme
    for intent in INTENTS:
        if contains_any(text, intent["keywords"]):
            try:
                return intent["handler"](text)
            except Exception as e:
                return f"Bu komutta bir hata oluştu: {e}"

    # Basit duygu ipucu
    if contains_any(text, {"uzgun","moralim bozuk","kotu hissediyorum","kotu hissediyorum"}):
        return "Üzgün hissetmene üzüldüm. Küçük bir yürüyüş molası iyi gelebilir. Bugün 15 dk mini hedef koymayı dene. "

    # Mini FAQ
    faq_map = {
        "python nedir": "Python; okunabilirliği yüksek, çok amaçlı bir programlama dilidir.",
        "pandas nedir": "Pandas; tablo tipi veriler için güçlü bir Python kütüphanesidir.",
        "hava": "Hava durumunu şu an bilemiyorum, ama pencereden bakmak en düşük gecikmeli API ",
    }
    for k, v in faq_map.items():
        if k in text:
            return v

    # Fallback
    return "Bunu anlamadım 'yardım' yazarak komutları görebilirsin."

# ---------- Ana döngü ----------
def main():
    print("Mini Chatbot 🤖 | çıkış: q / çık / exit")
    while True:
        try:
            user = input("Sen: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBot: Görüşürüz ")
            break

        if user.lower() in {"q","çık","cik","exit"}:
            print("Bot: Görüşürüz ")
            break

        # Sadece matematiksel ifade gibi görünüyorsa (kestirme)
        if re.fullmatch(r"[0-9\.\s\+\-\*\/\%\(\)\^]+", user.replace("**","^")):
            expr = user.replace("^","**")
            try:
                print(f"Bot: Sonuç: {safe_calc(expr)}")
                continue
            except Exception:
                pass  # normal akışa düşsün

        resp = handle(user)
        print(f"Bot: {resp}")

if __name__ == "__main__":
    main()
