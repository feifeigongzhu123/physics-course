import re, glob, xml.etree.ElementTree as ET
for f in sorted(glob.glob(r'D:\AI\ZCode\physics\_build\scenes\ps-8[2-6].svg')):
    s = open(f, encoding='utf-8').read()
    try:
        ET.fromstring(s)
        xmlok = 'XML OK'
    except Exception as e:
        xmlok = 'XML FAIL: ' + str(e)
    zones = re.findall(r'data-zone="([123])"', s)
    title = re.findall(r'<text x="450" y="(4[0-9])"', s)
    sizes = [float(x) for x in re.findall(r'font-size="([0-9.]+)"', s)]
    bad = [ln for ln in s.splitlines() if (m := re.search(r'font-size="([0-9.]+)"', ln)) and float(m.group(1)) < 11]
    scene = re.search(r'\[data-scene="(ps-8[2-6])"\]', s)
    prefixed = len(re.findall(r'class="[^"]*\bs8[2-6]-', s))
    vb = re.search(r'viewBox="([^"]+)"', s)
    print(f'{f.split(chr(92))[-1]}: {xmlok}; viewBox={vb.group(1) if vb else None}; zones={zones}; titleY={title}; minFont={min(sizes) if sizes else None}; scene={scene.group(1) if scene else None}; prefixed={prefixed}; bytes={len(s)}; badFontLines={len(bad)}')
    for ln in bad:
        print('   BAD:', ln.strip())
