"""Principales materias primas / productos de exportación por país (top 3–4)."""

MATERIAS = {
    # ================== AMÉRICA ==================
    "AM-01AR": "Soja, maíz, carne vacuna, trigo",
    "AM-02BO": "Gas natural, zinc, estaño, plata",
    "AM-03BR": "Soja, mineral de hierro, petróleo, café",
    "AM-04CA": "Petróleo, oro, madera, trigo",
    "AM-05CL": "Cobre, litio, frutas, salmón",
    "AM-06CO": "Petróleo, café, carbón, flores",
    "AM-07CR": "Dispositivos médicos, banano, piña, café",
    "AM-08CU": "Níquel, tabaco, azúcar, ron",
    "AM-09EC": "Petróleo, banano, camarón, cacao",
    "AM-10US": "Petróleo, aviones, maíz, soja",
    "AM-11GT": "Café, azúcar, banano, cardamomo",
    "AM-12MX": "Vehículos, petróleo, electrónica, aguacate",
    "AM-13PA": "Cobre, banano, azúcar, café",
    "AM-14PE": "Cobre, oro, zinc, harina de pescado",
    "AM-15PY": "Soja, carne vacuna, maíz, energía eléctrica",
    "AM-16UY": "Carne vacuna, soja, celulosa, lácteos",

    # ================== EUROPA ==================
    "EU-01DE": "Automóviles, maquinaria, química, productos farmacéuticos",
    "EU-02ES": "Vehículos, aceite de oliva, vino, frutas y hortalizas",
    "EU-03FR": "Aviones, vino, cosméticos, productos de lujo",
    "EU-04IT": "Maquinaria, vehículos, vino, moda y textiles",
    "EU-05GR": "Aceite de oliva, petróleo refinado, pescado, aluminio",
    "EU-06PT": "Vehículos, vino, corcho, calzado",
    "EU-07GB": "Petróleo, whisky, maquinaria, productos farmacéuticos",
    "EU-08NL": "Petróleo refinado, gas natural, flores, quesos",
    "EU-09CH": "Relojes, química, oro, productos farmacéuticos",
    "EU-10SE": "Maquinaria, mineral de hierro, madera, vehículos",
    "EU-11NO": "Petróleo, gas natural, pescado (salmón), aluminio",
    "EU-12PL": "Vehículos, maquinaria, muebles, carbón",

    # ================== ASIA ==================
    "AS-01CN": "Electrónica, maquinaria, textiles, acero",
    "AS-02JP": "Vehículos, electrónica, maquinaria, acero",
    "AS-03IN": "Productos refinados de petróleo, diamantes, arroz, textiles",
    "AS-04KR": "Semiconductores, vehículos, barcos, electrónica",
    "AS-05TR": "Vehículos, textiles, oro, maquinaria",
    "AS-06TH": "Electrónica, vehículos, caucho, arroz",
    "AS-07IL": "Diamantes, tecnología, productos farmacéuticos, química",
    "AS-08VN": "Electrónica, textiles, calzado, café",

    # ================== ÁFRICA ==================
    "AF-01EG": "Petróleo, gas natural, oro, textiles",
    "AF-02ZA": "Oro, platino, carbón, mineral de hierro",
    "AF-03MA": "Fosfato, automóviles, textiles, cítricos",
    "AF-04NG": "Petróleo, gas natural, cacao, sésamo",
    "AF-05KE": "Té, café, flores cortadas, horticultura",
    "AF-06SN": "Oro, fosfatos, pescado, maní",

    # ================== OCEANÍA ==================
    "OC-01AU": "Hierro, carbón, oro, gas natural, trigo, lana",
    "OC-02NZ": "Leche en polvo, mantequilla, carne de cordero, kiwi, vino",
    "OC-03PG": "Oro, cobre, gas natural, petróleo, café, aceite de palma",
    "OC-04FJ": "Caña de azúcar, agua embotellada, pescado, coco, oro",
}

if __name__ == "__main__":
    assert len(MATERIAS) == 46
    print(f"✓ {len(MATERIAS)} países con materias primas")
