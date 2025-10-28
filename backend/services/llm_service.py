import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client()

def analyze_text_with_ai(text: str) -> dict:
    prompt = f"""
    A következő szövegből gyűjtsd ki ezeket az adatokat:
    -*Allergének*: Glutén, Tojás, Rák, Hal, Földimogyoró, Szója, Tej, Diófélék, Zeller, Mustár
    (Ha egyik sem található, üres listát adj vissza.)
    -*Tápérték jellemzők*: Energia, Zsír, Szénhidrát, Cukor, Fehérje, Só, Nátrium
    Ha a tápértékben csak 'só' szerepel, számítsd át nátriummá is (1 g só = 0.393 g nátrium, a nátriumot mg-ban add meg).

    FONTOS: A kulcsokban NE legyen egység (pl. "g", "kcal"), csak a név! Az értékek legyenek számok (float vagy null).

    Válasz kizárólag érvényes JSON formátumban:

    {{
      "Allergének": ["Glutén", "Tej"],
      "Tápanyagok": {{
        "Energia": 450.0,
        "Zsír": 12.5,
        "Szénhidrát": 60.0,
        "Cukor": 5.0,
        "Fehérje": 8.0,
        "Só": 1.2,
        "Nátrium": 471.6
      }}
    }}

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