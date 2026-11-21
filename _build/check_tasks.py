# -*- coding: utf-8 -*-
import sqlite3, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
con = sqlite3.connect(r'C:\Users\萱萱\.zcode\v2\tasks-index.sqlite')
for t in ('automations', 'automation_runs', 'tasks'):
    cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
    print('==', t, cols)
    rows = con.execute(f"select * from {t}").fetchall()
    print('rows', len(rows))
    for r in rows[:20]:
        d = dict(zip(cols, r))
        s = json.dumps(d, ensure_ascii=False, default=str)
        if any(k in s for k in ('英词通', '音频', '03:30', 'audio')):
            print(s[:1200])
