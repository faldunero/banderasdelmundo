"""
Generador de las 3 cartas especiales (truco) del juego "Banderas del Mundo".

Usa plantilla_carta_especial.html y exporta los PNG a alta resolución
(≈300 DPI, tamaño póker 63×88 mm), con fondo transparente.

Uso:
    python3 generar_cartas_especiales.py              # genera las 3 cartas
    python3 generar_cartas_especiales.py ES-02        # genera solo esa
    python3 generar_cartas_especiales.py --force      # regenera todo
"""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = Path(__file__).parent
PLANTILLA = (BASE / "plantilla_carta_especial.html").read_text(encoding="utf-8")
SALIDA = BASE / "cartas_especiales_png"
SALIDA.mkdir(exist_ok=True)

DEVICE_SCALE = 4  # ≈300 DPI

# -------------------------------------------------------------------
# Íconos (SVG inline). Todos en blanco para contrastar con el medallón.
# -------------------------------------------------------------------
ICONO_RAYO = '''
<svg class="icono-accion" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
    <path d="M14 2 L4 14 L11 14 L10 22 L20 10 L13 10 Z"
          fill="#ffffff" stroke="#ffffff" stroke-width="0.5" stroke-linejoin="round"/>
</svg>
'''

ICONO_RELOJ_PROHIBIDO = '''
<svg class="icono-accion" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
    <circle cx="12" cy="12" r="8.6" stroke="#ffffff" stroke-width="2" fill="none"/>
    <path d="M12 7.2 L12 12 L15.5 14" stroke="#ffffff" stroke-width="2"
          stroke-linecap="round" stroke-linejoin="round" fill="none"/>
    <line x1="5" y1="19" x2="19" y2="5" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round"/>
</svg>
'''

ICONO_CARTA_DESCARTE = '''
<svg class="icono-accion" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg" fill="none">
    <!-- carta -->
    <rect x="5.5" y="2.8" width="13" height="10" rx="1.6"
          stroke="#ffffff" stroke-width="1.9" fill="none"/>
    <circle cx="9" cy="6.2" r="1.2" fill="#ffffff"/>
    <rect x="11.3" y="5.2" width="5.2" height="1.2" rx="0.6" fill="#ffffff"/>
    <rect x="11.3" y="7.7" width="3.8" height="1"   rx="0.5" fill="#ffffff"/>
    <!-- flecha hacia abajo -->
    <line x1="12" y1="14" x2="12" y2="20.2" stroke="#ffffff" stroke-width="2.4" stroke-linecap="round"/>
    <path d="M8.3 16.8 L12 20.8 L15.7 16.8"
          stroke="#ffffff" stroke-width="2.4" fill="none"
          stroke-linecap="round" stroke-linejoin="round"/>
</svg>
'''

# -------------------------------------------------------------------
# Catálogo de cartas especiales
# -------------------------------------------------------------------
CATALOGO = {
    "ES-01": {
        "nombre_archivo": "ES-01_robo_turno.png",
        "nombre_1": "Robo",
        "nombre_2": "de turno",
        "tagline": "Juega otro turno inmediato",
        "icono": ICONO_RAYO,
        "color_primario":    "#f39c12",
        "color_secundario":  "#e67e22",
        "color_brillo":      "#fbc14b",
        "halo1":             "rgba(243,156,18,0.16)",
        "halo2":             "rgba(230,126,34,0.14)",
        "borde_interno":     "rgba(243,156,18,0.22)",
        "sombra_medallon":   "rgba(230,126,34,0.35)",
    },
    "ES-02": {
        "nombre_archivo": "ES-02_pierde_turno.png",
        "nombre_1": "Pierde",
        "nombre_2": "turno",
        "tagline": "El siguiente jugador pierde su turno",
        "icono": ICONO_RELOJ_PROHIBIDO,
        "color_primario":    "#e74c3c",
        "color_secundario":  "#c0392b",
        "color_brillo":      "#ff7b6b",
        "halo1":             "rgba(231,76,60,0.16)",
        "halo2":             "rgba(192,57,43,0.14)",
        "borde_interno":     "rgba(231,76,60,0.22)",
        "sombra_medallon":   "rgba(192,57,43,0.35)",
    },
    "ES-03": {
        "nombre_archivo": "ES-03_descarta_carta.png",
        "nombre_1": "Descarta",
        "nombre_2": "carta",
        "tagline": "Otro jugador manda 1 carta al pozo",
        "icono": ICONO_CARTA_DESCARTE,
        "color_primario":    "#9b59b6",
        "color_secundario":  "#8e44ad",
        "color_brillo":      "#c38ae0",
        "halo1":             "rgba(155,89,182,0.16)",
        "halo2":             "rgba(142,68,173,0.14)",
        "borde_interno":     "rgba(155,89,182,0.22)",
        "sombra_medallon":   "rgba(142,68,173,0.35)",
    },
}


def render_carta(id_carta: str, page) -> Path:
    conf = CATALOGO[id_carta]
    html = (PLANTILLA
            .replace("{{COLOR_PRIMARIO}}",   conf["color_primario"])
            .replace("{{COLOR_SECUNDARIO}}", conf["color_secundario"])
            .replace("{{COLOR_BRILLO}}",     conf["color_brillo"])
            .replace("{{HALO1}}",            conf["halo1"])
            .replace("{{HALO2}}",            conf["halo2"])
            .replace("{{BORDE_INTERNO}}",    conf["borde_interno"])
            .replace("{{SOMBRA_MEDALLON}}",  conf["sombra_medallon"])
            .replace("{{ICONO_SVG}}",        conf["icono"])
            .replace("{{NOMBRE_LINEA_1}}",   conf["nombre_1"])
            .replace("{{NOMBRE_LINEA_2}}",   conf["nombre_2"])
            .replace("{{TAGLINE}}",          conf["tagline"]))
    page.set_content(html, wait_until="networkidle")
    page.wait_for_timeout(600)
    destino = SALIDA / conf["nombre_archivo"]
    page.locator(".carta").screenshot(path=str(destino), omit_background=True)
    return destino


def main():
    args = sys.argv[1:]
    forzar = "--force" in args
    args = [a for a in args if a != "--force"]
    ids = args if args else list(CATALOGO.keys())

    if not forzar:
        ids = [i for i in ids if not (SALIDA / CATALOGO[i]["nombre_archivo"]).exists()]
        if not ids:
            print("Todas las cartas especiales ya existen. Usa --force para regenerar.")
            return

    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx = browser.new_context(
            viewport={"width": 300, "height": 400},
            device_scale_factor=DEVICE_SCALE,
        )
        page = ctx.new_page()
        for idx, id_carta in enumerate(ids, 1):
            if id_carta not in CATALOGO:
                print(f"[!] {id_carta} no está en el catálogo")
                continue
            print(f"[{idx}/{len(ids)}] {id_carta} → {CATALOGO[id_carta]['nombre_archivo']}")
            ruta = render_carta(id_carta, page)
            print(f"       ✓ {ruta.name}")
        browser.close()

    print(f"\n✓ Listo. Cartas en {SALIDA}")


if __name__ == "__main__":
    main()
