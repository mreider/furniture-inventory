#!/usr/bin/env python3
"""Single source for both pages. Edit ITEMS below (or the HTML directly),
then run:  python3 generate.py   -> rebuilds index.html + mover.html in place.
Images live in images/ and are not touched by this script."""
import os, html
SITE = os.path.dirname(os.path.abspath(__file__))

ITEMS = [
 # room, name, owner, decision, [seqs], slug
 ("Entrance", "Closets", "Matt / Alison", "michael", [0], "entrance-closets"),
 ("Entrance", "Cabinets", "Matt / Alison", "michael", [1], "entrance-cabinets"),
 ("Entrance", "Shoe Rack", "Matt / Alison", "matt_removes", [2], "entrance-shoe-rack"),
 ("Kitchen / Dining Area", "Shelf", "Matt / Alison", "july28", [3], "kitchen-shelf"),
 ("Kitchen / Dining Area", "Table", "Matt / Alison", "july28", [4], "kitchen-table"),
 ("Living Room", "Gray IKEA Sofa", "Matt / Alison", "july10", [5], "living-gray-sofa"),
 ("Living Room", "Red IKEA Sofa", "Matt / Alison", "july10", [6], "living-red-sofa"),
 ("Living Room", "Blue Chair and Stool", "Matt / Alison", "july10", [7], "living-chair-stool"),
 ("Living Room", "TV Stand and Shelves", "Matt / Alison", "july10", [8], "living-tv-stand"),
 ("Living Room", "Shelves", "Matt / Alison", "july10", [9], "living-shelves"),
 ("Downstairs Front Bedroom", "Chest of Drawers", "Leo Grillberger", "leo", [10], "df-chest-drawers"),
 ("Downstairs Front Bedroom", "Motorized Desk and Chair", "Matt / Alison", "sell", [11], "df-desk-chair"),
 ("Downstairs Front Bedroom", "Mattress and Bed Frame", "Matt / Alison", "july10", [12], "df-bed"),
 ("Downstairs Rear Bedroom", "Chest of Drawers", "Leo Grillberger", "leo", [13], "dr-chest-drawers"),
 ("Downstairs Rear Bedroom", "Bed Frame and Mattress", "Matt / Alison", "july28", [14], "dr-bed"),
 ("Downstairs Rear Bedroom", "Bed Side Tables", "Matt / Alison", "july28", [15], "dr-bedside-tables"),
 ("Back Utility Room", "Desk", "Matt / Alison", "matt_removes", [16], "utility-desk"),
 ("Back Utility Room", "Washer + 2 Dryers", "Matt / Alison", "sell", [17, 18], "utility-washer-dryers"),
 ("Garage Storage", "Bed Frame", "Matt / Alison", "matt_removes", [19], "garage-bed-frame"),
 ("Downstairs Bathroom", "Shelves", "Matt / Alison", "matt_removes", [20], "db-shelves"),
 ("Upstairs Front Bedroom", "Mirror", "Matt / Alison", "matt_removes", [21], "uf-mirror"),
 ("Upstairs Front Bedroom", "Wardrobe Unit", "Matt / Alison", "july10", [22], "uf-wardrobe"),
 ("Upstairs Front Bedroom", "Chest of Drawers", "Matt / Alison", "july10", [23], "uf-chest-drawers"),
 ("Upstairs Front Bedroom", "Desk", "Matt / Alison", "july10", [24], "uf-desk"),
 ("Upstairs Front Bedroom", "Shelves", "Matt / Alison", "matt_removes", [25], "uf-shelves"),
 ("Upstairs Front Bedroom", "Bed", "Leo Grillberger", "leo", [26], "uf-bed"),
 ("Upstairs Hallway", "Mattress", "Matt / Alison", "july10", [27], "uh-mattress"),
 ("Upstairs Hallway", "Bedside Table", "Leo Grillberger", "leo", [28], "uh-bedside-table"),
 ("Upstairs Rear Bedroom", "Chest of Drawers", "Matt / Alison", "michael", [29], "ur-chest-drawers"),
 ("Upstairs Rear Bedroom", "Bed Frame and Mattress", "Matt / Alison", "july28", [30], "ur-bed"),
 ("Upstairs Rear Bedroom", "Bedside Tables", "Leo Grillberger", "leo", [31], "ur-bedside-tables"),
 ("Upstairs Rear Bedroom", "Desk", "Matt / Alison", "july28", [32], "ur-desk"),
 ("Upstairs Rear Bedroom", "Shelves", "Matt / Alison", "july28", [33], "ur-shelves"),
 ("Upstairs Rear Bedroom", "Cabinets", "Matt / Alison", "july10", [34], "ur-cabinets"),
]

# decision label + css class (label already reflects July 9 -> July 10 change)
DECISION = {
 "michael":      ("Michael wants",       "d-michael"),
 "matt_removes": ("Matt Removes",        "d-mattrem"),
 "july28":       ("Remove July 28th",    "d-july28"),
 "july10":       ("Remove July 10",      "d-july10"),
 "sell":         ("Matt / Alison Sell",  "d-sell"),
 "leo":          ("Needs decision",      "d-leo"),
}


# items reserved for a specific person (slug -> name); shown as its own pill
RESERVED = {
 "dr-bedside-tables": "Timur",
 "db-shelves":        "Timur",
 "entrance-shoe-rack":"Timur",
 "living-chair-stool":"Timur",
 "living-tv-stand":   "Timur",
 "df-desk-chair":     "Vika",
 "kitchen-table":     "James",
 "kitchen-shelf":     "Korbinian",
}


def imgnames(slug, seqs):
    if len(seqs)==1: return [f"{slug}.jpg"]
    return [f"{slug}-{n+1}.jpg" for n in range(len(seqs))]


#!/usr/bin/env python3
import os, html, shutil

def esc(s): return html.escape(s, quote=True)

# stable, shared item numbers (document order) — same number on every page
NUM = {it[5]: i for i, it in enumerate(ITEMS, 1)}

# display order + labels/classes for decision tags
DEC_ORDER = ["michael", "leo", "july10", "july28", "sell", "matt_removes"]
DEC_LABEL = {
 "michael":      "Michael wants",
 "leo":          "Leo to decide",
 "july10":       "Remove July 10",
 "july28":       "Remove July 28th",
 "sell":         "Sell",
 "matt_removes": "Matt removes",
}
DEC_CLASS = {
 "michael":"d-michael","leo":"d-leo","july10":"d-july10",
 "july28":"d-july28","sell":"d-sell","matt_removes":"d-mattrem",
}

STYLE = """
*{box-sizing:border-box}
body{margin:0;font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  color:#1f2328;background:#f6f7f9;-webkit-text-size-adjust:100%}
header.site{background:#111827;color:#fff;padding:26px 20px}
header.site .wrap{max-width:1100px;margin:0 auto}
header.site h1{margin:0 0 6px;font-size:23px;font-weight:700}
header.site p{margin:0;color:#c7cbd1;font-size:15px}
header.site nav{margin-top:12px;font-size:14px}
header.site nav a{color:#a5b4fc;text-decoration:none;font-weight:600;margin-right:16px}
.wrap{max-width:1100px;margin:0 auto;padding:0 20px}
.filterbar{position:sticky;top:0;z-index:5;background:#fffffff2;backdrop-filter:blur(6px);
  border-bottom:1px solid #e4e7eb;padding:12px 0}
.filterbar .wrap{display:flex;flex-wrap:wrap;gap:8px;align-items:center}
.flabel{font-size:13px;color:#6b7280;font-weight:600;margin-right:2px}
.chip{border:1px solid #d1d5db;background:#fff;border-radius:20px;padding:5px 13px;font-size:13px;
  font-weight:600;cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:6px;line-height:1}
.chip .n{font-weight:600;opacity:.7;font-size:12px}
.chip.active{box-shadow:0 0 0 2px #111827 inset;border-color:#111827}
.chip.michael.active{box-shadow:0 0 0 2px #1e40af inset;border-color:#1e40af}
.chip.d-michael{background:#dbeafe;color:#1e40af;border-color:#bfdbfe}
.chip.d-leo{background:#fef3c7;color:#b45309;border-color:#fde68a}
.chip.d-july10{background:#d1fae5;color:#047857;border-color:#a7f3d0}
.chip.d-july28{background:#ede9fe;color:#6d28d9;border-color:#ddd6fe}
.chip.d-sell{background:#f3e8ff;color:#7e22ce;border-color:#e9d5ff}
.chip.d-mattrem{background:#fee2e2;color:#b91c1c;border-color:#fecaca}
.chip.active{filter:saturate(1.1)}
.chip.on{outline:3px solid rgba(17,24,39,.85);outline-offset:1px}
#allchip{background:#111827;color:#fff;border-color:#111827}
#allchip.dim{background:#fff;color:#374151}
main{padding:22px 0 60px}
.block{margin-bottom:8px}
h2.room{font-size:14px;text-transform:uppercase;letter-spacing:.04em;color:#6b7280;
  margin:26px 0 12px;padding-bottom:6px;border-bottom:1px solid #e4e7eb}
.count{color:#9ca3af;font-weight:500}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:16px}
.card{background:#fff;border:1px solid #e4e7eb;border-radius:10px;overflow:hidden;display:flex;flex-direction:column}
.photos{display:flex;background:#eef0f2;position:relative}
.idnum{position:absolute;top:8px;left:8px;z-index:1;background:#111827e6;color:#fff;
  font-size:13px;font-weight:700;padding:3px 9px;border-radius:20px;letter-spacing:.02em}
.photos a{flex:1;display:block;line-height:0}
.photos img{width:100%;height:190px;object-fit:cover;display:block}
.body{padding:12px 14px;flex:1;display:flex;flex-direction:column;gap:8px}
.name{font-weight:650;font-size:16px}
.meta{font-size:13px;color:#6b7280}
.badges{display:flex;flex-wrap:wrap;gap:6px;margin-top:2px}
.badge{font-size:12px;font-weight:600;padding:3px 9px;border-radius:20px;white-space:nowrap}
.d-michael{background:#dbeafe;color:#1e40af}
.d-mattrem{background:#fee2e2;color:#b91c1c}
.d-july28{background:#ede9fe;color:#6d28d9}
.d-july10{background:#d1fae5;color:#047857}
.d-sell{background:#f3e8ff;color:#7e22ce}
.d-leo{background:#fef3c7;color:#b45309}
.d-reserved{background:#cffafe;color:#0e7490}
.owner{background:#f3f4f6;color:#374151}
.dl{margin-top:auto;font-size:13px}
.dl a{color:#4338ca;text-decoration:none;font-weight:600}
.dl a:hover{text-decoration:underline}
.empty{display:none;color:#6b7280;padding:30px 0;font-size:15px}
footer{padding:30px 20px;text-align:center;color:#9ca3af;font-size:13px}
@media (max-width:520px){ .photos img{height:220px} }
"""

FILTER_JS = """
<script>
const state=new Set();
function apply(){
  document.querySelectorAll('.card').forEach(c=>{
    const d=c.dataset.dec;
    c.style.display=(state.size===0||state.has(d))?'':'none';
  });
  let anyVisible=false;
  document.querySelectorAll('.block').forEach(b=>{
    let n=0;b.querySelectorAll('.card').forEach(c=>{if(c.style.display!=='none')n++;});
    b.style.display=n?'':'none';
    if(n)anyVisible=true;
    const cnt=b.querySelector('.count');if(cnt)cnt.textContent='· '+n;
  });
  document.querySelectorAll('.chip[data-dec]').forEach(ch=>ch.classList.toggle('on',state.has(ch.dataset.dec)));
  const all=document.getElementById('allchip');if(all)all.classList.toggle('dim',state.size!==0);
  const e=document.getElementById('empty');if(e)e.style.display=anyVisible?'none':'block';
}
function toggle(d){state.has(d)?state.delete(d):state.add(d);apply();}
function clearAll(){state.clear();apply();}
document.addEventListener('DOMContentLoaded',apply);
</script>
"""

def page_head(title, nav=""):
    return f"""<!doctype html><html lang="en"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<meta name="robots" content="noindex,nofollow">
<title>{esc(title)}</title><style>{STYLE}</style></head><body>
<header class="site"><div class="wrap"><h1>{esc(title)}</h1>{nav}</div></header>"""

PAGE_FOOT = FILTER_JS + "</body></html>"

def filterbar(decisions_present, counts):
    chips = ['<button id="allchip" class="chip" onclick="clearAll()">Show all</button>']
    for d in DEC_ORDER:
        if d in decisions_present:
            chips.append(
              f'<button class="chip {DEC_CLASS[d]}" data-dec="{d}" onclick="toggle(\'{d}\')">'
              f'{esc(DEC_LABEL[d])} <span class="n">{counts[d]}</span></button>')
    return ('<div class="filterbar"><div class="wrap">'
            '<span class="flabel">Filter:</span>' + "".join(chips) + '</div></div>')

def card(item, show_owner=True, show_location_as_meta=None, show_reserved=True):
    room,name,owner,dec,seqs,slug = item
    imgs = imgnames(slug, seqs)
    photos = "".join(
        f'<a href="images/{im}" target="_blank" rel="noopener"><img loading="lazy" src="images/{im}" alt="{esc(name)}"></a>'
        for im in imgs)
    meta = f'<div class="meta">{esc(show_location_as_meta if show_location_as_meta else room)}</div>'
    badges = ""
    resv = RESERVED.get(slug) if show_reserved else None
    if resv:
        badges += f'<span class="badge d-reserved">Reserved · {esc(resv)}</span>'
    if show_owner:
        badges += f'<span class="badge owner">{esc(owner)}</span>'
    badges += f'<span class="badge {DEC_CLASS[dec]}">{esc(DEC_LABEL[dec])}</span>'
    num = NUM[slug]
    return f"""<div class="card" data-dec="{dec}">
<div class="photos"><span class="idnum">#{num}</span>{photos}</div>
<div class="body"><div class="name">{esc(name)}</div>{meta}
<div class="badges">{badges}</div></div></div>"""

def by_key(items, keyfn):
    order, groups = [], {}
    for it in items:
        k = keyfn(it)
        if k not in groups: groups[k]=[]; order.append(k)
        groups[k].append(it)
    return [(k, groups[k]) for k in order]

def write(fn, content):
    with open(os.path.join(SITE, fn), "w") as f: f.write(content)
    print("wrote", fn)

# ---------- Combined page (everyone): full inventory, filter by tag ----------
def build_index():
    present = [d for d in DEC_ORDER if any(it[3]==d for it in ITEMS)]
    counts = {d: sum(1 for it in ITEMS if it[3]==d) for d in present}
    nav = '<nav><a href="index.html">Full inventory</a><a href="mover.html">Mover schedule →</a></nav>'
    h = page_head("Furniture Inventory", nav)
    h += filterbar(present, counts)
    h += '<main><div class="wrap">'
    for room, items in by_key(ITEMS, lambda it: it[0]):
        h += f'<div class="block"><h2 class="room">{esc(room)} <span class="count">· {len(items)}</span></h2>'
        h += '<div class="grid">' + "".join(card(it) for it in items) + '</div></div>'
    h += '<div id="empty" class="empty">No items match that filter.</div>'
    h += '</div></main>' + PAGE_FOOT
    write("index.html", h)

# ---------- Mover page: the two trips, filter by trip tag ----------
def build_mover():
    trip_items = [it for it in ITEMS if it[3] in ("july10","july28")]
    present = [d for d in ["july10","july28"]]
    counts = {d: sum(1 for it in trip_items if it[3]==d) for d in present}
    nav = '<nav><a href="index.html">← Full inventory</a><a href="mover.html">Mover schedule</a></nav>'
    h = page_head("Mover Schedule — Two Trips", nav)
    h += filterbar(present, counts)
    h += '<main><div class="wrap">'
    sections = [
        ("Trip 1 — Thursday 10 July", [it for it in trip_items if it[3]=="july10"]),
        ("Trip 2 — Tuesday 29 July",  [it for it in trip_items if it[3]=="july28"]),
    ]
    for title, items in sections:
        h += f'<div class="block"><h2 class="room">{esc(title)} <span class="count">· {len(items)}</span></h2>'
        h += '<div class="grid">' + "".join(
                card(it, show_owner=False, show_reserved=False, show_location_as_meta=f"Location: {it[0]}") for it in items) + '</div></div>'
    h += '<div id="empty" class="empty">No items match that filter.</div>'
    h += '</div></main>' + PAGE_FOOT
    write("mover.html", h)


if __name__ == "__main__":
    build_index()
    build_mover()
    with open(os.path.join(SITE, "CNAME"), "w") as f: f.write("leo.mreider.com\n")
    print("regenerated index.html + mover.html")
