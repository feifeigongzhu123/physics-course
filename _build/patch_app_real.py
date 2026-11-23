# -*- coding: utf-8 -*-
from pathlib import Path

p = Path(r"D:\AI\ZCode\physics\_build\app.js")
s = p.read_text(encoding="utf-8")

start = s.index("  /* ---------- 题库 ---------- */")
end = s.index("  /* ---------- 语音朗读 ---------- */")
new_block = r'''  /* ---------- 题库 ---------- */
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
    card.innerHTML =
      '<div class="q-top"><span class="q-idx">' + esc(tag) + '</span>' +
      (q.angle ? '<span class="angle">' + esc(q.angle) + '</span>' : '') +
      '<span class="source">' + esc(q.source) + '</span></div>' +
      '<p class="stem">' + esc(q.stem) + '</p>' +
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

'''
s = s[:start] + new_block + s[end:]

# speakQuestion: multi answers
s = s.replace(
  "var text = '第' + (qi + 1) + '题，正确答案是' + letter(q.answerIndex) + '。' + q.explanation;",
  "var text = '第' + (qi + 1) + '题，正确答案是' + answerLetters(q) + '。' + q.explanation;"
)

# current state: realOpen
s = s.replace(
  "soundOn: true, audio: null, timers: [], speechBtn: null,\n    from: 0, downloading: false",
  "soundOn: true, audio: null, timers: [], speechBtn: null,\n    from: 0, downloading: false, realOpen: false"
)

# openPoint reset/render real
s = s.replace(
  "current.point = p;\n    current.index = DATA.indexOf(p);\n    current.step = 0;",
  "current.point = p;\n    current.index = DATA.indexOf(p);\n    current.step = 0;\n    current.realOpen = false;"
)
s = s.replace(
  "renderChips(p);\n    renderQuestions();\n    setStep",
  "renderChips(p);\n    renderQuestions();\n    renderReal();\n    setStep"
)

# bind redoAll near reset binding
s = s.replace(
  "el('reset').addEventListener('click', function(){",
  "var redoAllBtn = el('redoAll');\n  if(redoAllBtn) redoAllBtn.addEventListener('click', redoAllBase);\n  el('reset').addEventListener('click', function(){"
)

p.write_text(s, encoding="utf-8")
print("patched app.js", len(s))
