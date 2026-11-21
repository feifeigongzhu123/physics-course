# -*- coding: utf-8 -*-
import sqlite3, sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
con = sqlite3.connect(r'C:\Users\萱萱\.zcode\cli\db\db.sqlite')
sid = 'session_44ec4a1d907c8dcb23598674837fb847'
row = con.execute("select title, directory, datetime(time_updated,'unixepoch','localtime'), summary_files from session where id=?", (sid,)).fetchone()
print('SESSION', row)
for t in ['session_target', 'todo']:
    try:
        rows = con.execute(f"select * from {t} where session_id=?", (sid,)).fetchall()
        print(t, rows)
    except Exception as e:
        print(t, 'ERR', e)
msgs = con.execute("select id, datetime(time_created,'unixepoch','localtime'), data from message where session_id=? order by time_created desc limit 8", (sid,)).fetchall()
for mid, ts, data in msgs:
    try:
        o = json.loads(data)
        role = o.get('role')
        txt = ''
        if isinstance(o.get('content'), str):
            txt = o['content']
        elif isinstance(o.get('content'), list):
            txt = ' '.join(str(c.get('text','')) for c in o['content'] if isinstance(c, dict))
        print('MSG', ts, role, txt[:300].replace('\n',' '))
    except Exception as e:
        print('MSG raw', ts, str(data)[:200])
