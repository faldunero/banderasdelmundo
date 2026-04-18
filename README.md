# Banderas del Mundo

Juego de cartas educativo + explorador web interactivo de 42 países del mundo, desarrollado por [Ludolab](https://ludolab.cl).

## Contenido

- **`index.html`** — Explorador interactivo: buscador → carta del país → ficha de detalle (nombre, continente, bandera, escudo, mapa, resumen, estadísticas).
- **`cartas_png/`** — Las 42 cartas del juego en formato PNG (tamaño póker, ~300 DPI, fondo transparente).
- **`indice_cartas.html`** — Índice visual con las 42 cartas agrupadas por continente.
- **`plantilla_carta.html`** — Plantilla HTML de la carta, con placeholders `{{ID}}` y `{{BANDERA_SVG}}`.
- **`generar_cartas.py`** — Script Python que embebe cada SVG oficial en la plantilla y exporta el PNG correspondiente usando Playwright.
- **`banderas_svg/`** — Cache local de los SVG oficiales de las banderas (provienen del paquete [`flag-icons`](https://github.com/lipis/flag-icons), licencia MIT).
- **`BD_banderas.xlsx`** — Base de datos original con los 42 países, capitales, continentes, población y colores.

## Países incluidos (42)

- **América (16):** Argentina, Bolivia, Brasil, Canadá, Chile, Colombia, Costa Rica, Cuba, Ecuador, EE. UU., Guatemala, México, Panamá, Perú, Paraguay, Uruguay.
- **Europa (12):** Alemania, España, Francia, Italia, Grecia, Portugal, Reino Unido, Países Bajos, Suiza, Suecia, Noruega, Polonia.
- **Asia (8):** China, Japón, India, Corea del Sur, Turquía, Tailandia, Israel, Vietnam.
- **África (6):** Egipto, Sudáfrica, Marruecos, Nigeria, Kenia, Senegal.

## Identificadores

Cada carta tiene un ID con el formato `XX-NN` (continente + número):

- `AM-01` → Argentina
- `EU-04` → Italia
- `AS-02` → Japón
- `AF-02` → Sudáfrica

## Regenerar las cartas

Requisitos: Python 3.10+, Playwright, Chromium.

```bash
pip install playwright --break-system-packages
python3 -m playwright install chromium
python3 generar_cartas.py             # todas las cartas faltantes
python3 generar_cartas.py AM-05       # una carta específica
python3 generar_cartas.py --force     # regenera todo
```

Las cartas se guardan en `cartas_png/<ID>.png` a 1008×1408 px (listo para impresión).

## Créditos y licencias

- Banderas: [`flag-icons`](https://github.com/lipis/flag-icons) — MIT.
- Mapas: © [OpenStreetMap](https://www.openstreetmap.org/copyright) contributors — ODbL.
- Escudos: [mainfacts.com](https://mainfacts.com/).
- Diseño y juego: [Ludolab.cl](https://ludolab.cl).
