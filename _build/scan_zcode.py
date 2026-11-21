# -*- coding: utf-8 -*-
import json, sqlite3, sys, io
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
base = Path(r'C:\Users\萱萱\.zcode')
needles = ['英词通', '517ac708', '03:30', 'english-daily']

def walk(o, path=''):
    if isinstance(o, dict):
        for k, v in o.items():
            walk(v, path + '/' + str(k))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            walk(v, path + f'[{i}]')
    else:
        s = str(o)
        if any(n in s for n in needles):
            print('JSON', path, '=', s[:300])

for name in ['v2/bot-state.v3.json', 'v2/bot-config.v3.json', 'v2/setting.json', 'cli/db/db.sqlite']:
    p = base / name
    if not p.exists():
        continue
    if p.suffix == '.json':
        try:
            walk(json.loads(p.read_text(encoding='utf-8')))
        except Exception as e:
            print('ERR json', p, e)

for db in base.rglob('*.sqlite'):
    try:
        con = sqlite3.connect(str(db))
        tabs = [r[0] for r in con.execute("select name from sqlite_master where type='table'")]
        hit = False
        for t in tabs:
            try:
                rows = con.execute(f'select * from "{t}"').fetchall()
            except Exception:
                continue
            for r in rows:
                s = str(r)
                if any(n in s for n in needles):
                    if not hit:
                        print('DB', db)
                        hit = True
                    print(' ', t, s[:500])
        con.close()
    except Exception:
        pass
