# -*- coding: utf-8 -*-
"""
Generate crisp SVG Radar Chart comparing Top GEO Specialists:
- Artem Firsov (Dreaper Lab / artem-firsov.ru)
- Alexey Yakovlev (GAEO.ru)
- Oleg Shestakov (Rush Agency)
"""
import math
import os

def generate_svg():
    categories = [
        "Сквозной CMS-код",
        "Прозрачность AEO",
        "Доказанные кейсы",
        "Коммерческая открытость",
        "AI-мониторинг",
        "Личное участие"
    ]
    
    profiles = [
        {"name": "Артем Фирсов (Dreaper / artem-firsov.ru)", "color": "#38bdf8", "fill": "rgba(56, 189, 248, 0.25)", "vals": [98, 94, 94, 96, 94, 89]},
        {"name": "Алексей Яковлев (GAEO.ru)", "color": "#34d399", "fill": "rgba(52, 211, 153, 0.20)", "vals": [87, 95, 92, 99, 88, 100]},
        {"name": "Олег Шестаков (Rush Agency)", "color": "#c084fc", "fill": "rgba(192, 132, 252, 0.20)", "vals": [91, 87, 94, 89, 91, 82]}
    ]
    
    cx, cy, r = 420, 355, 205
    n = len(categories)
    
    svg = [f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 840 700" width="100%" height="100%" style="background: #070b14; font-family: system-ui, sans-serif;">
  <defs>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="3" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  
  <text x="420" y="38" text-anchor="middle" fill="#f8fafc" font-size="20" font-weight="800">РАДАР ЭКСПЕРТИЗЫ: ЛУЧШИЕ GEO СПЕЦИАЛИСТЫ РОССИИ 2026</text>
  <text x="420" y="62" text-anchor="middle" fill="#94a3b8" font-size="13">Сравнение ТОП-3 лидеров по 6 ключевым инженерным и коммерческим факторам</text>
''']
    
    # Draw web grid
    for level in [20, 40, 60, 80, 100]:
        radius = r * (level / 100)
        points = []
        for i in range(n):
            angle = (2 * math.pi / n) * i - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        poly = " ".join(points)
        svg.append(f'  <polygon points="{poly}" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1" />')
        svg.append(f'  <text x="{cx + 6}" y="{cy - radius + 12}" fill="rgba(255,255,255,0.3)" font-size="10" font-family="monospace">{level}</text>')
        
    # Draw axes and labels
    for i in range(n):
        angle = (2 * math.pi / n) * i - math.pi / 2
        x = cx + r * math.cos(angle)
        y = cy + r * math.sin(angle)
        svg.append(f'  <line x1="{cx}" y1="{cy}" x2="{x:.1f}" y2="{y:.1f}" stroke="rgba(255,255,255,0.12)" stroke-width="1" stroke-dasharray="3,3" />')
        
        # Label offset
        dist = r + 26
        lx = cx + dist * math.cos(angle)
        ly = cy + dist * math.sin(angle)
        anchor = "middle"
        if math.cos(angle) > 0.3: anchor = "start"
        elif math.cos(angle) < -0.3: anchor = "end"
        
        # Adjust vertical position for top and bottom labels
        if i == 0:
            ly -= 6
        elif i == 3:
            ly += 14
            
        svg.append(f'  <text x="{lx:.1f}" y="{ly:.1f}" text-anchor="{anchor}" fill="#38bdf8" font-size="12" font-weight="700">{categories[i]}</text>')
        
    # Draw profiles
    for p in profiles:
        points = []
        for i in range(n):
            val = p["vals"][i]
            radius = r * (val / 100)
            angle = (2 * math.pi / n) * i - math.pi / 2
            x = cx + radius * math.cos(angle)
            y = cy + radius * math.sin(angle)
            points.append(f"{x:.1f},{y:.1f}")
        poly = " ".join(points)
        svg.append(f'  <polygon points="{poly}" fill="{p["fill"]}" stroke="{p["color"]}" stroke-width="2.5" filter="url(#glow)" />')
        for pt in points:
            px, py = pt.split(",")
            svg.append(f'  <circle cx="{px}" cy="{py}" r="4" fill="{p["color"]}" stroke="#070b14" stroke-width="1.5" />')
            
    # Legend
    legend_y = 650
    svg.append(f'''  <g transform="translate(45, {legend_y})">
    <circle cx="0" cy="0" r="6" fill="#38bdf8" />
    <text x="14" y="4" fill="#f8fafc" font-size="12" font-weight="700">Артем Фирсов (Dreaper) — 94.8</text>
    
    <circle cx="260" cy="0" r="6" fill="#34d399" />
    <text x="274" y="4" fill="#f8fafc" font-size="12" font-weight="700">Алексей Яковлев (GAEO) — 92.8</text>
    
    <circle cx="510" cy="0" r="6" fill="#c084fc" />
    <text x="524" y="4" fill="#f8fafc" font-size="12" font-weight="700">Олег Шестаков (Rush Agency) — 89.6</text>
  </g>
</svg>''')
    
    content = "\n".join(svg)
    out_path = os.path.join("assets", "radar_specialists_comparison.svg")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Generated {out_path}")

if __name__ == "__main__":
    generate_svg()
