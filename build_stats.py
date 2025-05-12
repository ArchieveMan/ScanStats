from pathlib import Path
import re, json, sys
from config import BASE_DIR 

def extract_flat_number(fn): 
    return int(m.group(1) or m.group(2)) if (m := re.search(r'(\d{1,3})кв|кв(\d{1,3})', fn.lower())) else None

def extract_house_number(name: str) -> tuple:
    match = re.search(r'\b(\d+)([А-Яа-я]|\\/\d+)?\b', name)
    if match:
        return (int(match.group(1)), match.group(2) or '')
    return (float('inf'), name)

def process_district(path: Path, name: str):
    if not path.is_dir(): return print("❌ Указанная папка не найдена.")
    data = []
    for house in sorted(filter(Path.is_dir, path.iterdir()), key=lambda x: extract_house_number(x.name)):
        flats = sorted(set(filter(None, (extract_flat_number(f.name) for f in house.glob("*.pdf")))))
        if not flats: print(f"⚠️ Нет корректных файлов в доме: {house.name}"); continue
        maxf, allf = flats[-1], set(range(1, flats[-1] + 1))
        data.append({
            "house": house.name,
            "total_flats": maxf,
            "scanned": {"count": len(flats), "list": flats},
            "not_scanned": {"count": len(ns := sorted(allf - set(flats))), "list": ns}
        })
        
    if not data: return print("❌ Не найдено ни одного дома с корректными PDF-файлами.")
    out = BASE_DIR / "data" / (name if name.endswith("_stats.json") else name + "_stats.json")
    out.parent.mkdir(exist_ok=True)

    text = json.dumps({"district": path.name, "houses": data}, ensure_ascii=False, indent=2)
    out.write_text(re.sub(r'\[\s+([^][]*?)\s+\]', lambda m: '[' + ' '.join(m.group(1).split()) + ']', text), encoding="utf-8")
    print(f"✅ JSON сохранён: {out}")

# process_district(Path(input("Введите путь к папке микрорайона: ").strip()), input("Введите имя JSON-файла (без _stats.json): ").strip())