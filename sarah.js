(function () {
  var SARAH_IMG = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face";
  var TYPING_SPEED = 40;

  var SARAH_SYSTEM = "You are Sarah, a warm and human intake assistant for eSolicitors.ie — an Irish solicitor matching service.\n\nYour job is to understand the person's situation and collect their contact details so a solicitor can call them back. You are not a lawyer. Never give legal advice.\n\nCONVERSATION STAGES:\n\nSTAGE story: The person just arrived. Ask them to describe what happened — where, when, what occurred. Warm and brief. 2 sentences.\nExample: \"Hi, I'm Sarah from eSolicitors.ie. Tell me what happened — where you were, what occurred, and roughly when.\"\n\nSTAGE details: They described the situation. Acknowledge briefly with warmth (1 sentence). Ask ONE natural follow-up question based on what they said. Examples: Was anyone else involved? Did you receive any official documents? How long ago did this happen? Have you spoken to anyone about it yet?\nnext_stage: name\n\nSTAGE name: Acknowledge their follow-up answer briefly. Ask for their first name naturally.\nExample: \"That gives me a clearer picture. Can I ask your first name?\"\nnext_stage: phone\n\nSTAGE phone: Use their name. Ask for phone number.\nExample: \"Thanks [name]. What's the best number for a solicitor to reach you on?\"\nnext_stage: done\n\nSTAGE done: Warm confirmation. Solicitor will call within a few hours.\nExample: \"Perfect [name], you're all set. One of our solicitors will be in touch within a few hours.\"\n\nRULES: Max 2-3 short sentences. No legal advice. No fees. No emojis. No bullet points. Sound like a real warm person.\n\nRespond ONLY with valid JSON: {\"message\":\"...\",\"next_stage\":\"story|details|name|phone|done\",\"show_solicitors\":false}";

  function typeMessage(el, text, cb) {
    var words = text.split(' ');
    var i = 0;
    el.textContent = '';
    function next() {
      if (i < words.length) {
        el.textContent += (i === 0 ? '' : ' ') + words[i];
        i++;
        setTimeout(next, TYPING_SPEED + Math.random() * 20);
      } else {
        if (cb) cb();
      }
    }
    next();
  }

  if (!document.getElementById('sarah-css')) {
    var style = document.createElement('style');
    style.id = 'sarah-css';
    style.textContent = '.sarah-widget{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.25);max-width:480px;margin:0 auto}.sarah-header{background:#0c1f3d;padding:14px 18px;display:flex;align-items:center;gap:12px;position:relative;border-bottom:1px solid rgba(200,146,42,.2)}.sarah-av{width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid #c8922a;flex-shrink:0}.sarah-av img{width:100%;height:100%;object-fit:cover}.sarah-header-text strong{display:block;font-size:.88rem;font-weight:600;color:#fff}.sarah-header-text span{font-size:.75rem;color:rgba(255,255,255,.45)}.sarah-online{width:8px;height:8px;background:#4ade80;border-radius:50%;position:absolute;right:16px;top:50%;transform:translateY(-50%);animation:sarahPulse 2s infinite}@keyframes sarahPulse{0%,100%{box-shadow:0 0 0 2px rgba(74,222,128,.25)}50%{box-shadow:0 0 0 6px rgba(74,222,128,.08)}}.sarah-messages{height:280px;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth;background:#f7f3ee}.sarah-messages::-webkit-scrollbar{width:3px}.sarah-messages::-webkit-scrollbar-thumb{background:#e2ddd6;border-radius:2px}.smsg{display:flex;align-items:flex-end;gap:7px}.smsg.user{flex-direction:row-reverse}.smsg-av{width:26px;height:26px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1.5px solid #c8922a}.smsg-av img{width:100%;height:100%;object-fit:cover}.smsg-bubble{max-width:78%;padding:9px 12px;border-radius:12px;font-size:.83rem;line-height:1.65}.smsg.ai .smsg-bubble{background:#fff;color:#0c1f3d;border-bottom-left-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.06)}.smsg.user .smsg-bubble{background:#0c1f3d;color:#fff;border-bottom-right-radius:3px}.sarah-typing{display:flex;align-items:flex-end;gap:7px}.sarah-typing-bubble{background:#fff;border-radius:12px;border-bottom-left-radius:3px;padding:9px 12px;display:flex;gap:3px;align-items:center}.sdot{width:5px;height:5px;background:#bbb;border-radius:50%;animation:sdotBounce 1.2s infinite}.sdot:nth-child(2){animation-delay:.2s}.sdot:nth-child(3){animation-delay:.4s}@keyframes sdotBounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}.sarah-input-area{border-top:1px solid #e2ddd6;padding:10px 12px;background:#fff}.sarah-input-row{display:flex;align-items:center;gap:8px;background:#f7f3ee;border:1.5px solid #e2ddd6;border-radius:10px;padding:8px 12px;transition:border-color .2s}.sarah-input-row:focus-within{border-color:#c8922a}.sarah-input-row textarea{flex:1;border:none;background:transparent;font-family:inherit;font-size:.83rem;color:#0c1f3d;resize:none;outline:none;line-height:1.5;max-height:70px;overflow-y:auto}.sarah-input-row textarea::placeholder{color:#bbb}.sarah-send{width:32px;height:32px;border-radius:7px;background:#0c1f3d;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0}.sarah-send:hover{background:#162d52}.sarah-note{text-align:center;font-size:.7rem;color:#bbb;margin-top:6px}.sol-cards-wrap{display:flex;flex-direction:column;gap:7px;margin-top:4px}.sol-card{background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:9px 11px;display:flex;align-items:center;gap:9px;box-shadow:0 2px 8px rgba(15,30,53,.06)}.sol-av{width:36px;height:36px;border-radius:50%;background:#0c1f3d;display:flex;align-items:center;justify-content:center;font-size:.78rem;font-weight:700;color:#c8922a;flex-shrink:0}.sol-info{flex:1}.sol-name{font-size:12.5px;font-weight:600;color:#0c1f3d}.sol-area{font-size:10.5px;color:#8896a8;margin-top:1px}.sol-stars{color:#f5a623;font-size:10px;margin-top:2px}.sol-badge{background:#0c1f3d;color:#fff;font-size:8.5px;font-weight:600;border-radius:4px;padding:2px 6px}';
    document.head.appendChild(style);
  }

  function createInstance(messagesId, inputId) {
    var history = [], stage = 'story', collected = {}, isLoading = false;
    var msgs = document.getElementById(messagesId);
    var input = document.getElementById(inputId);

    function addMsg(isUser) {
      var row = document.createElement('div');
      row.className = 'smsg' + (isUser ? ' user' : '');
      if (!isUser) {
        var av = document.createElement('div');
        av.className = 'smsg-av';
        av.innerHTML = '<img src="' + SARAH_IMG + '" alt="Sarah"/>';
        row.appendChild(av);
      }
      var b = document.createElement('div');
      b.className = 'smsg-bubble';
      row.appendChild(b);
      msgs.appendChild(row);
      msgs.scrollTop = msgs.scrollHeight;
      return b;
    }

    function showTyping() {
      var row = document.createElement('div');
      row.className = 'sarah-typing';
      row.id = messagesId + '-typing';
      row.innerHTML = '<div class="smsg-av"><img src="' + SARAH_IMG + '"/></div><div class="sarah-typing-bubble"><div class="sdot"></div><div class="sdot"></div><div class="sdot"></div></div>';
      msgs.appendChild(row);
      msgs.scrollTop = msgs.scrollHeight;
    }

    function removeTyping() {
      var t = document.getElementById(messagesId + '-typing');
      if (t) t.remove();
    }

    function showSolicitors() {
      var sols = window.SARAH_SOLICITORS || [
        {initials:'CO', name:"Ciara O'Brien", area:'Criminal & Road Traffic', county:'Dublin', stars:'5.0', reviews:47},
        {initials:'MF', name:'Michael Fitzgerald', area:'Personal Injury', county:'Cork', stars:'4.9', reviews:31},
        {initials:'SG', name:'Sinead Gallagher', area:'Employment Law', county:'Galway', stars:'5.0', reviews:28}
      ];
      var row = document.createElement('div');
      row.className = 'smsg';
      var av = document.createElement('div');
      av.className = 'smsg-av';
      av.innerHTML = '<img src="' + SARAH_IMG + '"/>';
      row.appendChild(av);
      var wrap = document.createElement('div');
      wrap.className = 'sol-cards-wrap';
      sols.forEach(function(sol) {
        var card = document.createElement('div');
        card.className = 'sol-card';
        card.innerHTML = '<div class="sol-av">' + sol.initials + '</div><div class="sol-info"><div class="sol-name">' + sol.name + '</div><div class="sol-area">' + sol.area + ' · ' + sol.county + '</div><div class="sol-stars">★★★★★ <span style="color:#999;font-size:9px">' + sol.stars + ' (' + sol.reviews + ')</span></div></div><div class="sol-badge">Verified</div>';
        wrap.appendChild(card);
      });
      row.appendChild(wrap);
      msgs.appendChild(row);
      msgs.scrollTop = msgs.scrollHeight;
    }

    function send() {
      if (!input) return;
      var text = input.value.trim();
      if (!text || isLoading) return;
      input.value = '';
      input.style.height = 'auto';
      isLoading = true;
      var b = addMsg(true);
      b.textContent = text;
      history.push({role:'user', content:text});
      if (stage === 'name') collected.name = text;
      if (stage === 'phone') collected.phone = text;

      // Human delay before typing indicator
      setTimeout(function() {
        showTyping();
        // Extra read delay based on message length
        var readDelay = Math.min(text.length * 12, 1200);
        setTimeout(function() {
          fetch('/api/chat', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({system: SARAH_SYSTEM + '\n\nCurrent stage: ' + stage, messages: history})
          }).then(function(res) {
            removeTyping();
            if (!res.ok) {
              var eb = addMsg(false);
              eb.textContent = 'Something went wrong. Please try again.';
              isLoading = false;
              return;
            }
            return res.json();
          }).then(function(data) {
            if (!data) return;
            var raw = (data.content && data.content[0] && data.content[0].text) || '';
            var parsed;
            try {
              var m = raw.replace(/```json|```/g,'').trim().match(/\{[\s\S]*\}/);
              parsed = m ? JSON.parse(m[0]) : null;
              if (!parsed || !parsed.message) throw 0;
            } catch(e) {
              parsed = {message: raw || 'Something went wrong.', next_stage: stage, show_solicitors: false};
            }
            var bubble = addMsg(false);
            typeMessage(bubble, parsed.message, function() {
              msgs.scrollTop = msgs.scrollHeight;
              if (parsed.show_solicitors) setTimeout(showSolicitors, 600);
            });
            history.push({role:'assistant', content:parsed.message});
            if (parsed.next_stage) stage = parsed.next_stage;
            if (stage === 'done' && collected.phone) {
              var transcript = history.map(function(m) { return (m.role==='user'?'Visitor: ':'Sarah: ') + m.content; }).join('\n');
              var issue = '';
              for (var i=0; i<history.length; i++) { if (history[i].role==='user') { issue=history[i].content.substring(0,120); break; } }
              fetch('/api/leads', {
                method:'POST',
                headers:{'Content-Type':'application/json'},
                body:JSON.stringify({name:collected.name||'',phone:collected.phone||'',issue:issue,transcript:transcript,source:window.location.pathname})
              });
            }
            isLoading = false;
          }).catch(function() {
            removeTyping();
            var eb = addMsg(false);
            eb.textContent = 'Network error. Please try again.';
            isLoading = false;
          });
        }, readDelay);
      }, 400 + Math.random() * 300);
    }

    if (input) {
      input.addEventListener('input', function() { this.style.height='auto'; this.style.height=Math.min(this.scrollHeight,70)+'px'; });
      input.addEventListener('keydown', function(e) { if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();send();} });
    }

    // Greeting with typing effect after short delay
    setTimeout(function() {
      var b = addMsg(false);
      typeMessage(b, "Hi, I'm Sarah from eSolicitors.ie. Tell me what happened — where you were, what occurred, and roughly when.", function() {
        msgs.scrollTop = msgs.scrollHeight;
      });
    }, 700);

    return {send: send};
  }

  function mountInline(container) {
    var uid = 'sw' + Math.random().toString(36).slice(2,6);
    container.innerHTML = '<div class="sarah-widget"><div class="sarah-header"><div class="sarah-av"><img src="' + SARAH_IMG + '" alt="Sarah"/></div><div class="sarah-header-text"><strong>Sarah — eSolicitors.ie</strong><span>Legal intake assistant · Here to help</span></div><div class="sarah-online"></div></div><div class="sarah-messages" id="' + uid + '-msgs"></div><div class="sarah-input-area"><div class="sarah-input-row"><textarea id="' + uid + '-input" rows="1" placeholder="Tell me what happened..."></textarea><button class="sarah-send" onclick="window.' + uid + '_send()"><svg width="14" height="14" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button></div><div class="sarah-note">Confidential · Free · No obligation</div></div></div>';
    var inst = createInstance(uid + '-msgs', uid + '-input');
    window[uid + '_send'] = function() { inst.send(); };
  }

  // Mount on all script tags
  var scripts = document.querySelectorAll('script[src*="sarah.js"]');
  scripts.forEach(function(script) {
    var container = document.createElement('div');
    script.parentNode.insertBefore(container, script);
    mountInline(container);
  });

})();
