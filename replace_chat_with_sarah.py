import glob
import re
import os

SARAH_IMG = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face"

SARAH_CSS = """.sarah-widget{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.25)}
.sarah-header{background:var(--navy,#0c1f3d);padding:14px 18px;display:flex;align-items:center;gap:12px;position:relative}
.sarah-av{width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid var(--gold,#c8922a);flex-shrink:0}
.sarah-av img{width:100%;height:100%;object-fit:cover}
.sarah-header-text strong{display:block;font-size:.88rem;font-weight:600;color:#fff}
.sarah-header-text span{font-size:.75rem;color:rgba(255,255,255,0.45)}
.sarah-online{width:8px;height:8px;background:#4ade80;border-radius:50%;position:absolute;right:16px;top:50%;transform:translateY(-50%)}
.sarah-messages{height:300px;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth;background:#f7f3ee}
.sarah-messages::-webkit-scrollbar{width:3px}
.sarah-messages::-webkit-scrollbar-thumb{background:#e2ddd6;border-radius:2px}
.smsg{display:flex;align-items:flex-end;gap:7px}
.smsg.user{flex-direction:row-reverse}
.smsg-av{width:26px;height:26px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1.5px solid var(--gold,#c8922a)}
.smsg-av img{width:100%;height:100%;object-fit:cover}
.smsg-bubble{max-width:78%;padding:9px 12px;border-radius:12px;font-size:.83rem;line-height:1.6}
.smsg.ai .smsg-bubble{background:#fff;color:var(--navy,#0c1f3d);border-bottom-left-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.smsg.user .smsg-bubble{background:var(--navy,#0c1f3d);color:#fff;border-bottom-right-radius:3px}
.sarah-typing{display:flex;align-items:flex-end;gap:7px}
.sarah-typing-bubble{background:#fff;border-radius:12px;border-bottom-left-radius:3px;padding:9px 12px;display:flex;gap:3px;align-items:center}
.sarah-dot{width:5px;height:5px;background:#bbb;border-radius:50%;animation:sbounce 1.2s infinite}
.sarah-dot:nth-child(2){animation-delay:.2s}
.sarah-dot:nth-child(3){animation-delay:.4s}
@keyframes sbounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}}
.sarah-input-area{border-top:1px solid #e2ddd6;padding:10px 12px;background:#fff}
.sarah-input-row{display:flex;align-items:center;gap:8px;background:#f7f3ee;border:1px solid #e2ddd6;border-radius:10px;padding:8px 12px;transition:border-color .2s}
.sarah-input-row:focus-within{border-color:var(--gold,#c8922a)}
.sarah-input-row textarea{flex:1;border:none;background:transparent;font-family:'DM Sans',sans-serif;font-size:.83rem;color:var(--navy,#0c1f3d);resize:none;outline:none;line-height:1.5;max-height:70px;overflow-y:auto}
.sarah-input-row textarea::placeholder{color:#bbb}
.sarah-send{width:32px;height:32px;border-radius:7px;background:var(--navy,#0c1f3d);border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .2s}
.sarah-send:hover{background:#162d52}
.sarah-note{text-align:center;font-size:.7rem;color:#bbb;margin-top:6px}
"""

SARAH_WIDGET_HTML = '''<div class="sarah-widget">
      <div class="sarah-header">
        <div class="sarah-av"><img src="''' + SARAH_IMG + '''" alt="Sarah"/></div>
        <div class="sarah-header-text">
          <strong>Sarah — eSolicitors.ie</strong>
          <span>Legal intake assistant · Here to help</span>
        </div>
        <div class="sarah-online"></div>
      </div>
      <div class="sarah-messages" id="sarahMessages"></div>
      <div class="sarah-input-area">
        <div class="sarah-input-row">
          <textarea id="sarahInput" rows="1" placeholder="Tell me what happened..."></textarea>
          <button class="sarah-send" id="sarahSendBtn" onclick="sarahSend()">
            <svg width="14" height="14" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
        <div class="sarah-note">Confidential · Free · No obligation</div>
      </div>
    </div>'''

SARAH_JS = '''<script>
const SARAH_IMG_URL = "''' + SARAH_IMG + '''";
let sarahHistory = [], sarahStage = "story", sarahCollected = {};
const SARAH_PROMPT = "You are Sarah, a warm intake assistant for eSolicitors.ie. Be kind and human. " +
  "STAGE: story - Respond warmly 2-3 sentences. Ask for first name. next_stage: name. " +
  "STAGE: name - Ask for best phone number. next_stage: phone. " +
  "STAGE: phone - Confirm solicitor in touch within hours. next_stage: done. " +
  "STAGE: done - Brief reassurance. " +
  "RULES: No legal advice. No fees. 2-4 sentences. No emojis. " +
  'Respond ONLY valid JSON: {"message":"...","next_stage":"name|phone|done"}';
function sarahAddMsg(text,isUser){const msgs=document.getElementById('sarahMessages');const row=document.createElement('div');row.className='smsg'+(isUser?' user':'');if(!isUser){const av=document.createElement('div');av.className='smsg-av';av.innerHTML='<img src="'+SARAH_IMG_URL+'" alt="Sarah"/>';row.appendChild(av);}const b=document.createElement('div');b.className='smsg-bubble';b.textContent=text;row.appendChild(b);msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;}
function sarahShowTyping(){const msgs=document.getElementById('sarahMessages');const row=document.createElement('div');row.className='sarah-typing';row.id='sarahTyping';row.innerHTML='<div class="smsg-av"><img src="'+SARAH_IMG_URL+'"/></div><div class="sarah-typing-bubble"><div class="sarah-dot"></div><div class="sarah-dot"></div><div class="sarah-dot"></div></div>';msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;}
function sarahRemoveTyping(){const t=document.getElementById('sarahTyping');if(t)t.remove();}
async function sarahSend(){const input=document.getElementById('sarahInput');const text=input.value.trim();if(!text)return;input.value='';input.style.height='auto';sarahAddMsg(text,true);sarahHistory.push({role:'user',content:text});if(sarahStage==='name')sarahCollected.name=text;if(sarahStage==='phone')sarahCollected.phone=text;sarahShowTyping();try{const res=await fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({system:SARAH_PROMPT+'\\n\\nCurrent stage: '+sarahStage,messages:sarahHistory})});sarahRemoveTyping();if(!res.ok){sarahAddMsg('Something went wrong. Please try again.',false);return;}const data=await res.json();const raw=data.content?.[0]?.text||'';let parsed;try{const m=raw.replace(/```json|```/g,'').trim().match(/\{[\s\S]*\}/);parsed=m?JSON.parse(m[0]):null;if(!parsed||!parsed.message)throw 0;}catch{parsed={message:raw||'Something went wrong.',next_stage:sarahStage};}sarahAddMsg(parsed.message,false);sarahHistory.push({role:'assistant',content:parsed.message});if(parsed.next_stage)sarahStage=parsed.next_stage;if(sarahStage==='done'&&sarahCollected.phone){const transcript=sarahHistory.map(m=>(m.role==='user'?'Visitor: ':'Sarah: ')+m.content).join('\\n');fetch('/api/leads',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({name:sarahCollected.name||'',phone:sarahCollected.phone||'',issue:sarahHistory[0]?.content?.substring(0,120)||'',transcript:transcript,source:window.location.pathname});}}catch(e){sarahRemoveTyping();sarahAddMsg('Network error.',false);}}
const sarahTa=document.getElementById('sarahInput');if(sarahTa){sarahTa.addEventListener('input',function(){this.style.height='auto';this.style.height=Math.min(this.scrollHeight,70)+'px';});sarahTa.addEventListener('keydown',function(e){if(e.key==='Enter'&&!e.shiftKey){e.preventDefault();sarahSend();}});}
sarahAddMsg("Hi, I'm Sarah from eSolicitors.ie. Whatever has brought you here — tell me what happened and I'll make sure you get to the right solicitor.", false);
</script>'''

files = sorted(set(
    glob.glob("./**/*.html", recursive=True) +
    glob.glob("./*.html")
))

fixed = 0

for filepath in files:
    if '.github' in filepath or '/api/' in filepath:
        continue

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
    except:
        continue

    if 'eSolicitors Assistant' not in content or 'chat-widget' not in content:
        continue

    original = content

    # 1. Add Sarah CSS before </style>
    if 'sarah-widget' not in content:
        content = content.replace('</style>', SARAH_CSS + '\n</style>', 1)

    # 2. Replace chat widget HTML
    content = re.sub(
        r'<div class="chat-widget">.*?</div>\s*(?=</div>\s*</section>|</div>\s*\n\s*</section>)',
        SARAH_WIDGET_HTML + '\n    ',
        content,
        flags=re.DOTALL,
        count=1
    )

    # 3. Replace old script block
    script_start = content.find('<script>')
    script_end = content.find('</script>', script_start) + 9
    if script_start != -1 and 'sendMessage' in content[script_start:script_end]:
        content = content[:script_start] + SARAH_JS + content[script_end:]

    # 4. Remove any injected sarah.js
    content = re.sub(r'\s*<script src="/sarah\.js"[^>]*></script>', '', content)

    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"Fixed: {filepath}")
        fixed += 1

print(f"\nDone. Fixed {fixed} files.")
