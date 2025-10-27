import os
from google import genai
#import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def analyze_text_with_ai(text: str) -> dict:
    prompt = f"""
    A következő szövegből gyűjtsd ki ezeket az adatokat:
    -*Allergének*: Glutén, Tojás, Rák, Hal, Földimogyoró, Szója, Tej, Diófélék, Zeller, Mustár
    (Ha egyik sem található, üres listát adj vissza.)
    -*Tápérték jellemzők*: Energia (kcal), Zsír (g), Szénhidrát (g), Cukor (g), Fehérje (g), Só (g), Nátrium (mg)
    Ha a tápértékben csak 'só' szerepel, számítsd át nátriummá is (1 g só = 0.393 g nátrium, a nátriumot mg-ban add meg)

    Válasz kizárólag érvényes JSON formátumban.

  "Allergének": [string, ...],    ha nincs allergén, legyen [] (üres lista)
  "Tápanyagok":
     "Energia (kcal)": float | null,
     "Zsír (g)": float | null,
     "Szénhidrát (g)": float | null,
     "Cukor (g)": float | null,
     "Fehérje (g)": float | null,
     "Só (g): float | null,
     "Nátrium (mg)": float | null

    A szöveg:
    {text}
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt,
        config={
            "response_mime_type": "application/json"
        }
    )
    return response.text