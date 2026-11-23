(function(){
  'use strict';

  var APP_VERSION = 'v1.2.0';
  var APP_BUILD = '2026-11-21';
  document.documentElement.setAttribute('data-version', APP_VERSION);
  document.documentElement.setAttribute('data-build', APP_BUILD);

  var errs = [];
  document.documentElement.setAttribute('data-js-errors', '0');
  function noteErr(msg){
    errs.push(String(msg || 'error'));
    document.documentElement.setAttribute('data-js-errors', String(errs.length));
    var bar = document.getElementById('errorBar');
    if(bar){ bar.textContent = '脚本错误：' + errs[errs.length - 1]; bar.classList.add('show'); }
  }
  window.addEventListener('error', function(e){ noteErr(e.message || 'script error'); });
  window.addEventListener('unhandledrejection', function(e){
    noteErr((e.reason && e.reason.message) || 'promise rejection');
  });

  var DATA = [];
  try{
    DATA = JSON.parse(document.getElementById('physics-data').textContent);
  }catch(e){
    noteErr('课程数据解析失败');
  }

  var POINT_MAP = {};
  DATA.forEach(function(p){ POINT_MAP[p.id] = p; });

  var KEY = 'physics_progress_v1';
  var store = { learned: {}, answers: {}, wrong: {} };
  try{
    var raw = localStorage.getItem(KEY);
    if(raw){
      var o = JSON.parse(raw);
      store.learned = o.learned || {};
      store.answers = o.answers || {};
      store.wrong = o.wrong || {};
    }
  }catch(e){}
  function save(){
    try{ localStorage.setItem(KEY, JSON.stringify(store)); }catch(e){}
  }

  var current = {
    point: null, index: -1, step: 0, playing: false, paused: false,
    soundOn: true, audio: null, timers: [], speechBtn: null,
    from: 0, downloading: false, realOpen: false
  };

  var CACHE_NAME = 'physics-audio-v1';
  var isFile = location.protocol === 'file:';
  var canCache = (typeof caches !== 'undefined') && !isFile && window.isSecureContext !== false;
  var blobUrls = {};
  var audioPool = [];

  function el(id){ return document.getElementById(id); }
  function esc(s){
    return String(s == null ? '' : s)
      .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
      .replace(/"/g, '&quot;');
  }
  function letter(i){ return 'ABCD'.charAt(i); }
  function clearTimers(){
    for(var i = 0; i < current.timers.length; i++) clearTimeout(current.timers[i]);
    current.timers = [];
  }
  function setBar(pct){
    var bar = el('audioBar');
    if(!bar) return;
    pct = Math.max(0, Math.min(100, Number(pct) || 0));
    bar.style.transition = 'none';
    bar.style.width = pct + '%';
  }
  function resetBar(){ setBar(0); }
  function setPlayText(t){
    var b = el('play');
    if(b) b.textContent = t;
  }
  function showPause(show, label){
    var p = el('pause');
    if(!p) return;
    p.hidden = !show;
    if(!show) p.textContent = '⏸ 暂停';
    else if(label) p.textContent = label;
  }
  function detachAudio(){
    if(!current.audio) return;
    var a = current.audio;
    current.audio = null;
    a.onended = null;
    a.ontimeupdate = null;
    a.onplaying = null;
    a.onerror = null;
    a.onloadedmetadata = null;
    try{ a.pause(); a.currentTime = 0; }catch(e){}
  }
  function stopAudio(){
    clearTimers();
    detachAudio();
  }
  function stopPlayback(){
    stopAudio();
    current.playing = false;
    current.paused = false;
    current.from = 0;
    resetBar();
    setPlayText('▶ 播放讲解');
    var b = el('play');
    if(b) b.disabled = false;
    showPause(false);
  }

  /* ---------- 语音缓存 / 整学段下载 ---------- */
  function cacheOpen(){
    return caches.open(CACHE_NAME);
  }
  function rememberBlob(src, cache){
    if(blobUrls[src]) return Promise.resolve(blobUrls[src]);
    return cache.match(src).then(function(r){
      if(!r) return null;
      return r.blob().then(function(b){
        if(blobUrls[src]) return blobUrls[src];
        blobUrls[src] = URL.createObjectURL(b);
        return blobUrls[src];
      });
    }).catch(function(){ return null; });
  }
  function hydrate(src){
    if(!canCache || blobUrls[src]) return Promise.resolve();
    return cacheOpen().then(function(c){ return rememberBlob(src, c); }).catch(function(){});
  }
  function hydratePoint(p){
    if(!canCache) return;
    cacheOpen().then(function(c){
      p.steps.forEach(function(s){ rememberBlob(s.audio, c); });
    }).catch(function(){});
  }
  function warm(src){
    if(!canCache) return Promise.resolve();
    return cacheOpen().then(function(c){
      return c.match(src).then(function(hit){
        if(hit) return rememberBlob(src, c);
        return fetch(src, { cache: 'no-store' }).then(function(r){
          if(!r.ok) throw new Error('HTTP ' + r.status);
          return c.put(src, r.clone()).then(function(){ return rememberBlob(src, c); });
        });
      });
    }).catch(function(){});
  }
  function playableSrc(src){ return blobUrls[src] || src; }
  function allAudio(){
    var list = [];
    DATA.forEach(function(p){ p.steps.forEach(function(s){ list.push(s); }); });
    return list;
  }
  function downloadAllAudio(){
    if(!canCache){
      window.alert(isFile
        ? '当前是本地文件打开，语音已经在本机，无需下载。'
        : '当前地址不是 HTTPS 或 localhost，浏览器不允许整学段缓存；直接播放仍会按需加载。');
      return;
    }
    if(current.downloading) return;
    var list = allAudio();
    var totalDur = 0;
    list.forEach(function(s){ totalDur += (s.dur || 0); });
    var perSec = /\.mp3$/i.test(list[0].audio) ? 6000 : 32000;
    var estMb = Math.max(1, Math.round(totalDur * perSec / 1048576));
    if(estMb >= 20 && !window.confirm('将下载本学段全部 ' + list.length + ' 段语音，约 ' + estMb + ' MB，继续吗？')) return;

    var btn = el('downloadAll');
    var done = 0, fail = 0, bytes = 0, index = 0;
    current.downloading = true;
    if(btn){ btn.disabled = true; btn.textContent = '准备下载…'; }

    function update(){
      if(btn) btn.textContent = '下载中 ' + done + '/' + list.length +
        (bytes ? ' · ' + (bytes / 1048576).toFixed(1) + ' MB' : '');
    }
    function worker(){
      if(index >= list.length) return Promise.resolve();
      var src = list[index++].audio;
      return cacheOpen().then(function(c){
        return c.match(src).then(function(hit){
          if(hit){ done++; update(); return; }
          return fetch(src, { cache: 'no-store' }).then(function(r){
            if(!r.ok) throw new Error('HTTP ' + r.status);
            bytes += Number(r.headers.get('content-length') || 0);
            return c.put(src, r.clone()).then(function(){ done++; update(); });
          });
        }).catch(function(){ fail++; update(); });
      }).then(function(){ return worker(); });
    }

    var jobs = [];
    for(var k = 0; k < 3; k++) jobs.push(worker());
    Promise.all(jobs).then(function(){
      current.downloading = false;
      if(btn){
        btn.disabled = false;
        btn.textContent = fail ? ('下载完成，失败 ' + fail + ' 段') : ('语音已缓存 ' + done + ' 段 ✓');
      }
      list.forEach(function(s){ hydrate(s.audio); });
    }).catch(function(){
      current.downloading = false;
      if(btn){ btn.disabled = false; btn.textContent = '下载失败，请重试'; }
    });
  }
  function updateDownloadState(){
    var btn = el('downloadAll');
    if(!btn || current.downloading) return;
    if(!canCache){
      btn.textContent = isFile ? '本地文件 · 无需下载' : '需 HTTPS 才能整学段缓存';
      btn.disabled = true;
      return;
    }
    var list = allAudio();
    cacheOpen().then(function(c){
      return Promise.all(list.map(function(s){ return c.match(s.audio); }));
    }).then(function(hits){
      if(current.downloading) return;
      var hit = 0;
      hits.forEach(function(h){ if(h) hit++; });
      btn.disabled = false;
      btn.textContent = hit === list.length
        ? ('语音已缓存 ' + hit + ' 段 ✓')
        : (hit ? ('继续下载语音 ' + hit + '/' + list.length) : '下载本学段语音');
    }).catch(function(){});
  }

  /* ---------- 首页 ---------- */
  function unitList(){
    var order = [], map = {};
    DATA.forEach(function(p){
      if(!map[p.unit]){ map[p.unit] = []; order.push(p.unit); }
      map[p.unit].push(p);
    });
    return order.map(function(u){ return { unit: u, points: map[u] }; });
  }

  function answeredCount(){
    var n = 0;
    for(var k in store.answers){ if(Object.prototype.hasOwnProperty.call(store.answers, k)) n++; }
    return n;
  }
  function wrongCount(){
    var n = 0;
    for(var k in store.wrong){ if(Object.prototype.hasOwnProperty.call(store.wrong, k)) n++; }
    return n;
  }
  function learnedCount(){
    var n = 0;
    for(var k in store.learned){ if(store.learned[k]) n++; }
    return n;
  }

  function updateStats(){
    var a = el('statLearned'), b = el('statAnswered'), c = el('statWrong');
    if(a) a.textContent = learnedCount();
    if(b) b.textContent = answeredCount();
    if(c) c.textContent = wrongCount();
  }

  function pointAnswered(p){
    var n = 0;
    p.questions.forEach(function(q){
      if(Object.prototype.hasOwnProperty.call(store.answers, q.id)) n++;
    });
    return n;
  }

  function renderHome(){
    var wrap = el('units');
    if(!wrap) return;
    var totalSteps = 0, totalQs = 0;
    DATA.forEach(function(p){ totalSteps += p.steps.length; totalQs += p.questions.length; });
    if(el('homeTitle')) el('homeTitle').textContent = DATA.length + ' 个知识点，每个 3 步看懂';
    var examLabel = (DATA[0] && DATA[0].grade === 'senior') ? '高考真题改编' : '中考真题改编';
    if(el('homeSub')) el('homeSub').textContent = totalSteps + ' 段动画 · ' + totalQs + ' 道' + examLabel + ' · 每题逐项解析';
    wrap.innerHTML = '';
    var idx = 0;
    unitList().forEach(function(group){
      var unit = document.createElement('div');
      unit.className = 'unit';
      var head = document.createElement('button');
      head.type = 'button';
      head.className = 'unit-head';
      head.setAttribute('aria-expanded', 'true');
      head.innerHTML =
        '<span class="unit-title">' + esc(group.unit) + '</span>' +
        '<span class="unit-meta">' + group.points.length + ' 个知识点</span>' +
        '<span class="chev">⌄</span>';
      head.addEventListener('click', function(){
        var closed = unit.classList.toggle('closed');
        head.setAttribute('aria-expanded', closed ? 'false' : 'true');
      });

      var body = document.createElement('div');
      body.className = 'unit-body';
      group.points.forEach(function(p){
        idx++;
        var n = pointAnswered(p);
        var learned = !!store.learned[p.id];
        var row = document.createElement('button');
        row.type = 'button';
        row.className = 'point-row' + (learned ? ' done' : '');
        row.setAttribute('data-point', p.id);
        var badge, badgeCls = 'badge';
        if(learned){ badge = '已学'; badgeCls += ' done'; }
        else if(n > 0){ badge = '已答 ' + n + '/5'; }
        else { badge = '动画'; }
        row.innerHTML =
          '<span class="pnum">' + (idx < 10 ? '0' + idx : idx) + '</span>' +
          '<span class="pinfo"><b>' + esc(p.name) + '</b><em>' + esc(p.subtitle) + '</em></span>' +
          '<span class="' + badgeCls + '">' + badge + '</span>';
        row.addEventListener('click', function(){ openPoint(p.id, 0); });
        body.appendChild(row);
      });

      unit.appendChild(head);
      unit.appendChild(body);
      wrap.appendChild(unit);
    });
    updateStats();
    updateDownloadState();
    var v = el('appVersion');
    if(v){
      v.innerHTML = '版本 <b>v' + APP_VERSION + '</b> · ' + APP_BUILD + ' · 本学段 ' + DATA.length +
        ' 点 / ' + totalSteps + ' 步 / ' + totalQs + ' 题';
    }
  }

  /* ---------- 课程页 ---------- */
  function renderChips(p){
    var box = el('stepChips');
    box.innerHTML = '';
    p.steps.forEach(function(s, i){
      var b = document.createElement('button');
      b.type = 'button';
      b.className = 'step';
      b.textContent = (i + 1) + ' · ' + s.label;
      b.addEventListener('click', function(){
        stopPlayback();
        startPlayback(i);
      });
      box.appendChild(b);
    });
  }

  function updateChips(i){
    var chips = el('stepChips').querySelectorAll('.step');
    for(var k = 0; k < chips.length; k++){
      chips[k].classList.toggle('on', k === i);
    }
  }

  function updateLearnedTag(){
    var tag = el('learnedTag');
    if(!tag || !current.point) return;
    if(store.learned[current.point.id]){
      tag.textContent = '已学';
      tag.classList.add('learned');
    }else{
      tag.textContent = '3 步动画';
      tag.classList.remove('learned');
    }
  }

  function markLearned(){
    if(!current.point) return;
    if(!store.learned[current.point.id]){
      store.learned[current.point.id] = 1;
      save();
      updateStats();
      updateLearnedTag();
    }
  }

  function centerZone(i){
    var wrap = el('stageBox');
    if(!wrap || !current.point) return;
    if(wrap.scrollWidth <= wrap.clientWidth + 4) return;
    var sc = document.getElementById('scene-' + current.point.id);
    if(!sc) return;
    var svg = sc.querySelector('svg');
    if(!svg) return;
    var groups = [];
    for(var k = 0; k < svg.children.length; k++){
      var node = svg.children[k];
      if(node.tagName && node.tagName.toLowerCase() === 'g') groups.push(node);
    }
    var g = groups[i] || groups[0];
    var zoned = svg.querySelector('[data-zone="' + (i + 1) + '"]');
    if(zoned) g = zoned;
    if(!g) return;
    var wr = wrap.getBoundingClientRect();
    var gr = g.getBoundingClientRect();
    var center = gr.left - wr.left + wrap.scrollLeft + gr.width / 2;
    var target = center - wrap.clientWidth / 2;
    var max = wrap.scrollWidth - wrap.clientWidth;
    target = Math.max(0, Math.min(max, target));
    if(Math.abs(wrap.scrollLeft - target) < 4) return;
    var reduce = window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    if(wrap.scrollTo){
      wrap.scrollTo({ left: target, behavior: reduce ? 'auto' : 'smooth' });
    }else{
      wrap.scrollLeft = target;
    }
  }

  function setStep(i){
    var p = current.point;
    if(!p) return;
    i = Math.max(0, Math.min(2, i));
    current.step = i;

    var scenes = document.querySelectorAll('.scene');
    for(var k = 0; k < scenes.length; k++) scenes[k].classList.remove('on');
    var sc = document.getElementById('scene-' + p.id);
    if(sc){
      sc.classList.add('on');
      sc.className = 'scene on s' + (i + 1);
    }
    updateChips(i);

    var s = p.steps[i];
    el('caption').innerHTML = '<b>第 ' + (i + 1) + ' 步：</b>' + s.caption;

    var eq = el('equation');
    if(s.eq){
      eq.innerHTML = esc(s.eq) + (s.eqSub ? '<span>' + esc(s.eqSub) + '</span>' : '');
      eq.classList.add('show');
    }else{
      eq.classList.remove('show');
      eq.innerHTML = '';
    }

    var ro = el('readouts');
    ro.innerHTML = '';
    p.readoutLabels.forEach(function(label, k){
      var d = document.createElement('div');
      d.className = 'readout';
      d.innerHTML = '<span>' + esc(label) + '</span><b>' + esc(s.reads[k] || '—') + '</b>';
      ro.appendChild(d);
    });

    if(i === 2) markLearned();

    var scrollToZone = function(){ centerZone(i); };
    if(window.requestAnimationFrame) window.requestAnimationFrame(scrollToZone);
    else setTimeout(scrollToZone, 30);
  }

  function startPlayback(from){
    if(!current.point) return;
    stopAudio();
    current.playing = true;
    current.paused = false;
    current.from = (typeof from === 'number' && from >= 0 && from < 3) ? from : 0;
    var btn = el('play');
    if(btn) btn.disabled = true;
    setPlayText('加载语音…');
    showPause(false);
    playStep(current.from);
  }

  function preloadStep(i){
    if(!current.point || i >= 3) return;
    warm(current.point.steps[i].audio);
  }

  function failStep(i){
    detachAudio();
    current.playing = false;
    current.paused = false;
    current.from = i;
    resetBar();
    var b = el('play');
    if(b){ b.disabled = false; b.textContent = '↻ 重试'; }
    showPause(false);
  }

  function playStep(i){
    if(!current.playing || !current.point) return;
    if(i >= 3){
      current.playing = false;
      current.paused = false;
      current.from = 0;
      setPlayText('↻ 重播');
      var b = el('play');
      if(b) b.disabled = false;
      showPause(false);
      setBar(100);
      markLearned();
      return;
    }

    detachAudio();
    current.step = i;
    current.from = i;
    current.paused = false;
    setStep(i);
    resetBar();
    setPlayText('加载语音…');

    var s = current.point.steps[i];

    var a;
    try{
      a = new Audio(playableSrc(s.audio));
    }catch(e){
      failStep(i);
      return;
    }
    current.audio = a;
    a.preload = 'auto';
    a.muted = !current.soundOn;
    audioPool.push(a);
    if(audioPool.length > 120) audioPool.shift();

    a.onloadedmetadata = function(){
      if(current.audio !== a) return;
      setBar(0);
    };
    a.ontimeupdate = function(){
      if(current.audio !== a) return;
      var d = a.duration;
      if(!isFinite(d) || d <= 0) d = s.dur || 0;
      setBar(d > 0 ? (a.currentTime / d) * 100 : 0);
    };
    a.onplaying = function(){
      if(current.audio !== a) return;
      setPlayText('播放中…');
      showPause(true, '⏸ 暂停');
      preloadStep(i + 1);
    };
    a.onended = function(){
      if(current.audio !== a) return;
      a.onended = null;
      current.audio = null;
      playStep(i + 1);
    };
    a.onerror = function(){
      if(current.audio !== a) return;
      failStep(i);
    };

    var pr;
    try{
      pr = a.play();
    }catch(e){
      failStep(i);
      return;
    }
    if(pr && pr.catch){
      pr.catch(function(err){
        if(current.audio !== a) return;
        if(err && err.name === 'NotAllowedError'){
          current.paused = true;
          setPlayText('点击继续');
          showPause(true, '▶ 继续');
        }else{
          failStep(i);
        }
      });
    }
  }

  function togglePause(){
    if(!current.audio || !current.playing) return;
    var a = current.audio;
    var p = el('pause');
    if(current.paused){
      current.paused = false;
      if(p) p.textContent = '⏸ 暂停';
      setPlayText('播放中…');
      var pr = a.play();
      if(pr && pr.catch){
        pr.catch(function(){ current.paused = true; if(p) p.textContent = '▶ 继续'; });
      }
    }else{
      current.paused = true;
      try{ a.pause(); }catch(e){}
      if(p) p.textContent = '▶ 继续';
      setPlayText('已暂停');
    }
  }

  /* ---------- 题库 ---------- */
  function correctIdxs(q){
    if(q.answerIndexes && q.answerIndexes.length) return q.answerIndexes.slice();
    return [q.answerIndex];
  }
  function isMulti(q){ return correctIdxs(q).length > 1; }
  function sameSet(a, b){
    if(!Array.isArray(a) || !Array.isArray(b) || a.length !== b.length) return false;
    var x = a.slice().sort(), y = b.slice().sort();
    for(var i = 0; i < x.length; i++){ if(x[i] !== y[i]) return false; }
    return true;
  }
  function isCorrect(q, chosen){
    if(Array.isArray(chosen)) return sameSet(chosen, correctIdxs(q));
    return chosen === correctIdxs(q)[0];
  }
  function answerLetters(q){
    return correctIdxs(q).map(function(i){ return letter(i); }).join('、');
  }

  function buildFeedback(q, chosen){
    var idxs = correctIdxs(q);
    var ok = isCorrect(q, chosen);
    var notes = q.optionNotes.map(function(n, i){
      return '<p class="' + (idxs.indexOf(i) >= 0 ? 'ok' : '') + '">' + esc(n) + '</p>';
    }).join('');
    return '<div class="verdict ' + (ok ? 'ok' : 'no') + '">' +
      (ok ? '✓ 回答正确' : '✗ 正确答案是 ' + answerLetters(q)) +
      '</div><div class="notes">' + notes + '</div>' +
      '<div class="explain"><b>解析</b> ' + esc(q.explanation) + '</div>' +
      '<div class="q-actions"><button class="speak" type="button">🔊 听讲解</button>' +
      '<button class="redo" type="button">↻ 重做本题</button></div>';
  }

  function revealQuestion(card, q, chosen, qi){
    var idxs = correctIdxs(q);
    var opts = card.querySelectorAll('.opt');
    for(var i = 0; i < opts.length; i++){
      opts[i].disabled = true;
      if(idxs.indexOf(i) >= 0) opts[i].classList.add('correct');
      var picked = Array.isArray(chosen) ? chosen.indexOf(i) >= 0 : i === chosen;
      if(picked && idxs.indexOf(i) < 0) opts[i].classList.add('wrong');
    }
    var sub = card.querySelector('.submit-answer');
    if(sub){ sub.disabled = true; sub.textContent = '已提交'; }
    var fb = card.querySelector('.q-feedback');
    fb.innerHTML = buildFeedback(q, chosen);
    fb.classList.remove('hidden');
    var btn = fb.querySelector('.speak');
    if(btn) btn.addEventListener('click', function(){ speakQuestion(q, qi, btn); });
    var redo = fb.querySelector('.redo');
    if(redo) redo.addEventListener('click', function(){ redoQuestion(q); });
  }

  function questionCard(q, qi, container, tag, after){
    var multi = isMulti(q);
    var card = document.createElement('div');
    card.className = 'q card';
    card.setAttribute('data-q', q.id);
    var opts = q.options.map(function(o, i){
      return '<button class="opt" type="button" data-i="' + i + '">' +
        '<span class="letter">' + letter(i) + '</span><span>' + esc(o) + '</span></button>';
    }).join('');
    var realTag = q.real ? '<span class="real-tag">真题</span>' : '';
    card.innerHTML =
      '<div class="q-top"><span class="q-idx">' + esc(tag) + '</span>' + realTag +
      (q.angle ? '<span class="angle">' + esc(q.angle) + '</span>' : '') +
      '<span class="source">' + esc(q.source) + '</span></div>' +
      '<p class="stem">' + esc(q.stem) + '</p>' +
      (q.image ? '<img class="q-image" src="' + esc(q.image) + '" alt="原题配图">' : '') +
      (multi ? '<div class="multi-tip">多选题：选出所有正确项，再点“提交答案”</div>' : '') +
      '<div class="opts">' + opts + '</div>' +
      (multi ? '<button class="submit-answer" type="button">提交答案</button>' : '') +
      '<div class="q-feedback hidden"></div>';

    var btns = card.querySelectorAll('.opt');
    var answered = Object.prototype.hasOwnProperty.call(store.answers, q.id);
    var sel = Array.isArray(store.answers[q.id]) ? store.answers[q.id].slice() : [];
    function markSel(){
      for(var k = 0; k < btns.length; k++){
        btns[k].classList.toggle('selected', sel.indexOf(k) >= 0);
      }
    }
    for(var i = 0; i < btns.length; i++){
      (function(idx){
        btns[idx].addEventListener('click', function(){
          if(Object.prototype.hasOwnProperty.call(store.answers, q.id)) return;
          if(multi){
            var at = sel.indexOf(idx);
            if(at >= 0) sel.splice(at, 1); else sel.push(idx);
            markSel();
            return;
          }
          store.answers[q.id] = idx;
          if(idx === correctIdxs(q)[0]){ delete store.wrong[q.id]; }
          else { store.wrong[q.id] = 1; }
          save();
          revealQuestion(card, q, idx, qi);
          after();
        });
      })(i);
    }
    var sub = card.querySelector('.submit-answer');
    if(sub){
      sub.addEventListener('click', function(){
        if(Object.prototype.hasOwnProperty.call(store.answers, q.id) || !sel.length) return;
        store.answers[q.id] = sel.slice().sort();
        if(sameSet(store.answers[q.id], correctIdxs(q))){ delete store.wrong[q.id]; }
        else { store.wrong[q.id] = 1; }
        save();
        revealQuestion(card, q, store.answers[q.id], qi);
        after();
      });
    }
    if(answered){
      if(multi) markSel();
      revealQuestion(card, q, store.answers[q.id], qi);
    }
    container.appendChild(card);
  }

  function updateRedoAll(){
    var b = el('redoAll');
    if(!b || !current.point) return;
    var n = pointAnswered(current.point);
    b.disabled = n === 0;
    b.style.opacity = n === 0 ? '.45' : '1';
  }

  function renderQuestions(){
    var p = current.point;
    var wrap = el('questions');
    wrap.innerHTML = '';
    p.questions.forEach(function(q, qi){
      questionCard(q, qi, wrap, 'Q' + (qi + 1), function(){
        updateStats();
        updateQProgress();
        updateRedoAll();
      });
    });
    updateQProgress();
    updateRedoAll();
  }

  function updateQProgress(){
    var p = current.point;
    if(!p) return;
    var n = pointAnswered(p);
    var right = 0;
    p.questions.forEach(function(q){
      if(Object.prototype.hasOwnProperty.call(store.answers, q.id) && isCorrect(q, store.answers[q.id])) right++;
    });
    el('qProgress').textContent = '已答 ' + n + '/5 · 答对 ' + right;
  }

  function redoQuestion(q){
    delete store.answers[q.id];
    delete store.wrong[q.id];
    save();
    updateStats();
    if(q.real) renderReal();
    else renderQuestions();
  }

  function redoAllBase(){
    var p = current.point;
    if(!p) return;
    p.questions.forEach(function(q){ delete store.answers[q.id]; delete store.wrong[q.id]; });
    save();
    renderQuestions();
    updateStats();
  }

  function redoAllReal(){
    var p = current.point;
    if(!p) return;
    (p.realQuestions || []).forEach(function(q){ delete store.answers[q.id]; delete store.wrong[q.id]; });
    save();
    renderReal();
    updateStats();
  }

  function updateRealProgress(){
    var p = current.point;
    if(!p || !p.realQuestions) return;
    var n = 0, right = 0;
    p.realQuestions.forEach(function(q){
      if(Object.prototype.hasOwnProperty.call(store.answers, q.id)){
        n++;
        if(isCorrect(q, store.answers[q.id])) right++;
      }
    });
    var elx = el('realProgress');
    if(elx) elx.textContent = '已答 ' + n + '/' + p.realQuestions.length + ' · 答对 ' + right;
  }

  function renderReal(){
    var p = current.point;
    var wrap = el('realBank');
    if(!wrap) return;
    wrap.innerHTML = '';
    var list = (p && p.realQuestions) || [];
    if(!list.length) return;
    if(!current.realOpen){
      wrap.innerHTML = '<div class="card real-teaser">' +
        '<div><b>高考真题加练</b><span>本知识点还有 ' + list.length + ' 道真题，含逐项错因解析</span></div>' +
        '<button id="openReal" type="button">继续做真题</button></div>';
      var open = el('openReal');
      if(open) open.addEventListener('click', function(){
        current.realOpen = true;
        renderReal();
      });
      return;
    }
    wrap.innerHTML = '<div class="q-head real-head"><h2>高考真题 · 加练</h2>' +
      '<span id="realProgress"></span>' +
      '<button id="closeReal" type="button" class="redo-all">收起真题</button>' +
      '<button id="redoReal" type="button" class="redo-all">↻ 重做全部真题</button></div>' +
      '<div id="realQuestions"></div>';
    var qbox = el('realQuestions');
    list.forEach(function(q, qi){
      questionCard(q, qi, qbox, 'R' + (qi + 1), function(){
        updateStats();
        updateRealProgress();
      });
    });
    var close = el('closeReal');
    if(close) close.addEventListener('click', function(){ current.realOpen = false; renderReal(); });
    var redo = el('redoReal');
    if(redo) redo.addEventListener('click', redoAllReal);
    updateRealProgress();
  }

  /* ---------- 语音朗读 ---------- */
  function pickVoice(){
    if(!('speechSynthesis' in window)) return null;
    var vs = window.speechSynthesis.getVoices() || [];
    for(var i = 0; i < vs.length; i++){
      if(/zh[-_]CN/i.test(vs[i].lang) || /Huihui|Chinese|中文|普通话/i.test(vs[i].name)) return vs[i];
    }
    return null;
  }

  function stopSpeech(){
    if('speechSynthesis' in window) window.speechSynthesis.cancel();
    if(current.speechBtn){
      current.speechBtn.textContent = '🔊 听讲解';
      current.speechBtn = null;
    }
  }

  function speakQuestion(q, qi, btn){
    if(!('speechSynthesis' in window)){ btn.textContent = '此设备不支持语音'; return; }
    if(current.speechBtn === btn){
      stopSpeech();
      return;
    }
    stopSpeech();
    var text = '第' + (qi + 1) + '题，正确答案是' + answerLetters(q) + '。' + q.explanation;
    var u = new SpeechSynthesisUtterance(text);
    u.lang = 'zh-CN';
    u.rate = 0.95;
    u.pitch = 1;
    var v = pickVoice();
    if(v) u.voice = v;
    var self = btn;
    u.onend = function(){ if(current.speechBtn === self){ self.textContent = '🔊 听讲解'; current.speechBtn = null; } };
    u.onerror = function(){ if(current.speechBtn === self){ self.textContent = '🔊 听讲解'; current.speechBtn = null; } };
    current.speechBtn = btn;
    btn.textContent = '■ 停止';
    window.speechSynthesis.speak(u);
  }

  /* ---------- 打开知识点 ---------- */
  function updateHash(){
    if(!current.point) return;
    try{ history.replaceState(null, '', '#' + current.point.id + '/' + current.step); }catch(e){}
  }

  function openPoint(id, stepIdx, viaRow){
    var p = POINT_MAP[id];
    if(!p) return;
    stopPlayback();
    stopSpeech();
    current.point = p;
    current.index = DATA.indexOf(p);
    current.step = 0;
    current.realOpen = false;

    el('home').classList.add('hidden');
    el('lesson').classList.remove('hidden');
    el('lessonKicker').textContent = p.unit;
    el('lessonTitle').textContent = p.title;
    el('lessonSub').textContent = p.subtitle;
    el('crumb').textContent = p.unit + ' · ' + p.name;

    renderChips(p);
    renderQuestions();
    renderReal();
    setStep(typeof stepIdx === 'number' ? stepIdx : 0);
    updateLearnedTag();
    var lv = el('lessonVersion');
    if(lv) lv.textContent = '版本 v' + APP_VERSION + ' · ' + APP_BUILD + ' · ' + p.unit;
    current.from = 0;
    hydratePoint(p);

    var prev = el('prevPoint'), next = el('nextPoint');
    prev.disabled = current.index <= 0;
    next.disabled = current.index >= DATA.length - 1;
    prev.style.opacity = prev.disabled ? '.45' : '1';
    next.style.opacity = next.disabled ? '.45' : '1';

    var b = el('play');
    b.disabled = false;
    b.textContent = '▶ 播放讲解';

    updateHash();
    try{ window.scrollTo(0, 0); }catch(e){}
    if(viaRow){ /* 由用户点击进入，保持静音待播 */ }
  }

  function goHome(){
    stopPlayback();
    stopSpeech();
    current.point = null;
    el('lesson').classList.add('hidden');
    el('home').classList.remove('hidden');
    renderHome();
    try{ history.replaceState(null, '', location.pathname + location.search); }catch(e){}
    try{ window.scrollTo(0, 0); }catch(e){}
  }

  /* ---------- 事件绑定 ---------- */
  el('back').addEventListener('click', goHome);
  el('play').addEventListener('click', function(){
    if(!current.point) return;
    if(current.playing) return;
    startPlayback(current.from || 0);
  });
  el('pause').addEventListener('click', togglePause);
  el('downloadAll').addEventListener('click', downloadAllAudio);
  el('sound').addEventListener('click', function(){
    current.soundOn = !current.soundOn;
    el('sound').textContent = current.soundOn ? '🔊 讲解' : '🔇 静音';
    if(current.audio) current.audio.muted = !current.soundOn;
  });
  el('prevPoint').addEventListener('click', function(){
    if(current.index > 0) openPoint(DATA[current.index - 1].id, 0);
  });
  el('nextPoint').addEventListener('click', function(){
    if(current.index < DATA.length - 1) openPoint(DATA[current.index + 1].id, 0);
  });
  var redoAllBtn = el('redoAll');
  if(redoAllBtn) redoAllBtn.addEventListener('click', redoAllBase);
  el('reset').addEventListener('click', function(){
    if(!window.confirm('确定清空已学知识点、答题记录和错题吗？')) return;
    store = { learned: {}, answers: {}, wrong: {} };
    save();
    renderHome();
    if(current.point) goHome();
  });

  var resizeTimer = null;
  window.addEventListener('resize', function(){
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(function(){
      if(current.point) centerZone(current.step);
    }, 150);
  });

  if('speechSynthesis' in window){
    window.speechSynthesis.onvoiceschanged = function(){ /* 触发一次语音列表加载 */ };
  }

  /* ---------- 初始化 ---------- */
  renderHome();

  var m = (location.hash || '').match(/^#((?:pj|ps)-[1-9][0-9]?)(?:\/([0-2]))?$/);
  if(m && POINT_MAP[m[1]]){
    openPoint(m[1], m[2] ? Number(m[2]) : 0);
  }

  document.documentElement.setAttribute('data-ready', '1');
  document.documentElement.setAttribute('data-points', String(DATA.length));

  if(location.search.indexOf('debug=1') >= 0){
    setTimeout(function(){
      var w = function(id){ var e = el(id); return e ? e.offsetWidth : 0; };
      var vals = [w('stageBox'), w('caption'), w('readouts'), w('questions'), w('lesson'), document.body.scrollWidth];
      document.documentElement.setAttribute('data-debug', vals.join('/'));
    }, 600);
  }

  window.__PH = {
    data: DATA,
    open: openPoint,
    home: goHome,
    get errors(){ return errs.slice(); },
    get current(){
      return {
        playing: current.playing,
        paused: current.paused,
        step: current.step,
        soundOn: current.soundOn,
        audioTime: current.audio ? current.audio.currentTime : 0,
        audioDur: current.audio ? current.audio.duration : 0,
        audioSrc: current.audio ? current.audio.src : '',
        bar: el('audioBar') ? el('audioBar').style.width : ''
      };
    },
    activeAudios: function(){
      return audioPool.filter(function(a){ return !a.paused && !a.ended; }).length;
    },
    seek: function(sec){
      if(!current.audio) return;
      var d = current.audio.duration;
      if(!isFinite(d) || d <= 0) return;
      current.audio.currentTime = Math.max(0, Math.min(d - 0.25, sec));
    },
    downloadAll: downloadAllAudio,
    canCache: canCache,
    store: store
  };
})();
