"""
Generador de cartas "Banderas del Mundo" a PNG.

Descarga los SVG oficiales de flagcdn.com, los embebe en la plantilla
plantilla_carta.html y exporta un PNG en alta resolución (≈300 DPI,
tamaño póker 63×88 mm).

Uso:
    python3 generar_cartas.py              # genera todas las cartas del catálogo
    python3 generar_cartas.py AM-01        # genera sólo esa carta
"""
import sys
import re
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent
PLANTILLA = (BASE / "plantilla_carta.html").read_text(encoding="utf-8")
SALIDA_PNG = BASE / "cartas_png"
CACHE_SVG = BASE / "banderas_svg"
SALIDA_PNG.mkdir(exist_ok=True)
CACHE_SVG.mkdir(exist_ok=True)

DEVICE_SCALE = 4  # 4x ≈ 300 DPI

# =====================================================================
# Catálogo: ID de carta → código ISO 3166-1 alpha-2 (flagcdn)
# =====================================================================
CATALOGO = {
    # América
    "AM-01": "ar",  # Argentina
    "AM-02": "bo",  # Bolivia
    "AM-03": "br",  # Brasil
    "AM-04": "ca",  # Canadá
    "AM-05": "cl",  # Chile
    "AM-06": "co",  # Colombia
    "AM-07": "cr",  # Costa Rica
    "AM-08": "cu",  # Cuba
    "AM-09": "ec",  # Ecuador
    "AM-10": "us",  # EE. UU.
    "AM-11": "gt",  # Guatemala
    "AM-12": "mx",  # México
    "AM-13": "pa",  # Panamá
    "AM-14": "pe",  # Perú
    "AM-15": "py",  # Paraguay
    "AM-16": "uy",  # Uruguay
    "AM-17": "ve",  # Venezuela
    "AM-18": "do",  # Rep. Dominicana
    "AM-19": "hn",  # Honduras
    # Europa
    "EU-01": "de",  # Alemania
    "EU-02": "es",  # España
    "EU-03": "fr",  # Francia
    "EU-04": "it",  # Italia
    "EU-05": "gr",  # Grecia
    "EU-06": "pt",  # Portugal
    "EU-07": "gb",  # Reino Unido
    "EU-08": "nl",  # Países Bajos
    "EU-09": "ch",  # Suiza
    "EU-10": "se",  # Suecia
    "EU-11": "no",  # Noruega
    "EU-12": "pl",  # Polonia
    "EU-13": "be",  # Bélgica
    "EU-14": "at",  # Austria
    "EU-15": "ie",  # Irlanda
    # Asia
    "AS-01": "cn",  # China
    "AS-02": "jp",  # Japón
    "AS-03": "in",  # India
    "AS-04": "kr",  # Corea del Sur
    "AS-05": "tr",  # Turquía
    "AS-06": "th",  # Tailandia
    "AS-07": "il",  # Israel
    "AS-08": "vn",  # Vietnam
    # África
    "AF-01": "eg",  # Egipto
    "AF-02": "za",  # Sudáfrica
    "AF-03": "ma",  # Marruecos
    "AF-04": "ng",  # Nigeria
    "AF-05": "ke",  # Kenia
    "AF-06": "sn",  # Senegal
    # Oceanía
    "OC-01": "au",  # Australia
    "OC-02": "nz",  # Nueva Zelanda
    "OC-03": "pg",  # Papúa Nueva Guinea
    "OC-04": "fj",  # Fiji
}


def obtener_svg(iso: str, page) -> str:
    """Devuelve el SVG de la bandera (descarga con Playwright si no está en cache)."""
    ruta = CACHE_SVG / f"{iso}.svg"
    if not ruta.exists():
        url = f"https://flagcdn.com/{iso}.svg"
        print(f"  [↓] {url}")
        resp = page.request.get(url)
        if not resp.ok:
            raise RuntimeError(f"No se pudo descargar {url}: {resp.status}")
        ruta.write_text(resp.text(), encoding="utf-8")
    svg = ruta.read_text(encoding="utf-8")
    if "preserveAspectRatio" not in svg:
        svg = re.sub(r"<svg", '<svg preserveAspectRatio="xMidYMid meet"', svg, count=1)
    return svg


def render_carta(id_carta: str, svg: str, page) -> Path:
    html = PLANTILLA.replace("{{ID}}", id_carta).replace("{{BANDERA_SVG}}", svg)
    page.set_content(html, wait_until="networkidle")
    page.wait_for_timeout(600)
    destino = SALIDA_PNG / f"{id_carta}.png"
    page.locator(".carta").screenshot(path=str(destino), omit_background=True)
    return destino


def main():
    args = sys.argv[1:]
    forzar = "--force" in args
    args = [a for a in args if a != "--force"]
    ids = args if args else list(CATALOGO.keys())
    if not forzar:
        ids = [i for i in ids if not (SALIDA_PNG / f"{i}.png").exists()]
        if not ids:
            print("Todas las cartas ya existen. Usa --force para regenerar.")
            return

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 300, "height": 400},
            device_scale_factor=DEVICE_SCALE,
        )
        page = ctx.new_page()

        total = len(ids)
        for idx, id_carta in enumerate(ids, 1):
            if id_carta not in CATALOGO:
                print(f"[!] {id_carta} no está en el catálogo")
                continue
            iso = CATALOGO[id_carta]
            print(f"[{idx}/{total}] {id_carta} ({iso})")
            svg = obtener_svg(iso, page)
            ruta = render_carta(id_carta, svg, page)
            print(f"       → {ruta.name}")

        browser.close()

    print(f"\n✓ Listo. {total} PNG(s) en {SALIDA_PNG}")


if __name__ == "__main__":
    main()
