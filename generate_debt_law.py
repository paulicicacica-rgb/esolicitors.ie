import os, json, time, urllib.request, urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"
SARAH_IMG = "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face"

SYSTEM = "You write plain English content for eSolicitors.ie. Accurate Irish law only. No markdown. No bullet points. No headings. Output plain text paragraphs only. Never invent facts."

PAGES = [
    {
        "path": "./debt-law/index.html",
        "title": "Debt Law Ireland — Get Legal Help With Money Problems",
        "meta": "Struggling with debt in Ireland? Bailiff at the door, being sued, mortgage arrears or repossession? Get free legal advice matched to your situation.",
        "h1": "Debt problems\nin Ireland.\n<em>There are more options than you think.</em>",
        "intro": "Debt problems in Ireland can feel overwhelming — but the law protects you more than most people realise. Whether you are being chased by creditors, facing a court summons, worried about your home, or dealing with a bailiff at the door, an Irish solicitor can help you understand your options and protect your rights.",
        "law": "Civil Liability Acts, Enforcement of Court Orders Acts, Land and Conveyancing Law Reform Act 2009 — Irish law provides significant protections for debtors at every stage of the process.",
        "topics": [
            {"url": "/debt-law/bailiff-at-door-ireland/", "title": "Bailiff at the Door", "desc": "Know exactly what a sheriff or bailiff can and cannot do at your home."},
            {"url": "/debt-law/being-sued-for-money-ireland/", "title": "Being Sued for Money", "desc": "Received a court summons for debt in Ireland? Find out what happens next."},
            {"url": "/debt-law/cant-pay-mortgage-ireland/", "title": "Can't Pay Mortgage", "desc": "In mortgage arrears in Ireland? There are legal protections you may not know about."},
            {"url": "/debt-law/car-repossession-ireland/", "title": "Car Repossession", "desc": "Finance company threatening to repossess your car? Know your rights first."},
        ],
        "prompt": "Write 3 paragraphs about debt law in Ireland for eSolicitors.ie. Cover: what types of debt problems Irish solicitors help with, what protections Irish law gives debtors, and why getting legal advice early makes a difference. Plain English, accurate Irish law, no markdown, no bullet points."
    },
    {
        "path": "./debt-law/bailiff-at-door-ireland/index.html",
        "title": "Bailiff at the Door in Ireland — Your Rights",
        "meta": "A bailiff or sheriff came to your door in Ireland? They have strict legal limits. Find out exactly what they can and cannot do and how to protect yourself.",
        "h1": "A bailiff came\nto your door.\n<em>Here is what they can and cannot do.</em>",
        "intro": "In Ireland, the term 'bailiff' usually refers to a court-appointed sheriff or county registrar enforcing a civil court judgment. They have significant powers — but also strict legal limits. Many people do not realise that a bailiff cannot force entry into your home, and that you have rights throughout the process.",
        "law": "Enforcement of Court Orders Acts — court sheriffs enforce civil debt judgments. They must have a valid court order and follow strict procedures. Forcing entry to a private dwelling is not permitted.",
        "topics": None,
        "prompt": "Write 3 paragraphs for eSolicitors.ie about what happens when a bailiff or sheriff comes to the door in Ireland. Cover: what a sheriff is and what legal authority they have, what they cannot do (force entry, take certain items), and what a person should do if a bailiff arrives. Accurate Irish law, plain English, no markdown."
    },
    {
        "path": "./debt-law/being-sued-for-money-ireland/index.html",
        "title": "Being Sued for Money in Ireland — What Happens Next",
        "meta": "Received a court summons or civil bill for debt in Ireland? Find out exactly what the process is and what your options are.",
        "h1": "You've been sued\nfor money in Ireland.\n<em>Here is what the process looks like.</em>",
        "intro": "Being served with a court summons or civil bill for money owed in Ireland is serious — but it is not the end of the road. The Irish court system has a clear process, and you have the right to respond, defend the claim, or negotiate a settlement. Ignoring it is the worst thing you can do.",
        "law": "Civil Liability Acts — civil debt claims in Ireland are heard in the District Court (up to €15,000), Circuit Court (up to €75,000), or High Court. A judgment against you can lead to attachment of earnings or enforcement against property.",
        "topics": None,
        "prompt": "Write 3 paragraphs for eSolicitors.ie about being sued for money in Ireland. Cover: how the Irish civil courts work for debt claims, what happens if you ignore a summons (default judgment), and what options a person has when they receive a court summons for debt. Accurate Irish law only, plain English, no markdown."
    },
    {
        "path": "./debt-law/cant-pay-mortgage-ireland/index.html",
        "title": "Can't Pay Mortgage in Ireland — Legal Protections and Options",
        "meta": "In mortgage arrears in Ireland? Irish law gives you significant protections. Find out what your lender must do before repossession and what options you have.",
        "h1": "You can't pay\nyour mortgage in Ireland.\n<em>Irish law protects you more than you know.</em>",
        "intro": "If you are falling behind on your mortgage in Ireland, your lender cannot simply take your home. Irish law — particularly the Code of Conduct on Mortgage Arrears — requires lenders to follow a strict process before they can begin repossession proceedings. There are options available that many homeowners do not know about.",
        "law": "Land and Conveyancing Law Reform Act 2009, Code of Conduct on Mortgage Arrears (CCMA) — lenders must engage with the Mortgage Arrears Resolution Process (MARP) before any legal action. Courts can adjourn repossession proceedings to allow this process to complete.",
        "topics": None,
        "prompt": "Write 3 paragraphs for eSolicitors.ie about mortgage arrears in Ireland. Cover: what protections the Code of Conduct on Mortgage Arrears gives homeowners, what the Mortgage Arrears Resolution Process is and what a lender must do before they can repossess, and what options a homeowner in arrears has including Personal Insolvency Arrangements. Accurate Irish law, plain English, no markdown."
    },
    {
        "path": "./debt-law/car-repossession-ireland/index.html",
        "title": "Car Repossession in Ireland — Know Your Rights",
        "meta": "Finance company threatening to repossess your car in Ireland? You have rights. Find out what they can and cannot do and what your options are.",
        "h1": "Your car is being\nthreatened with repossession.\n<em>You have more rights than you think.</em>",
        "intro": "If you have a car on finance in Ireland and you have fallen behind on payments, the finance company may threaten repossession. But the process is not as straightforward as many people think. The law requires certain procedures to be followed — and in some cases a court order is needed before the car can be taken.",
        "law": "Consumer Credit Act 1995 — for hire purchase agreements in Ireland, once you have paid one third of the total price, the finance company cannot repossess the vehicle without a court order. This is known as the 'one third rule'.",
        "topics": None,
        "prompt": "Write 3 paragraphs for eSolicitors.ie about car repossession in Ireland. Cover: how hire purchase agreements work and what rights a consumer has, the one third rule under the Consumer Credit Act 1995 (cannot repossess without court order once one third is paid), and what someone should do if threatened with repossession. Accurate Irish law, plain English, no markdown."
    },
]

SARAH_CSS = "<style>.sarah-widget{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.22);max-width:480px;margin:0 auto}.sarah-header{background:#0c1f3d;padding:14px 18px;display:flex;align-items:center;gap:12px;position:relative;border-bottom:1px solid rgba(200,146,42,.2)}.sarah-av{width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid #c8922a;flex-shrink:0}.sarah-av img{width:100%;height:100%;object-fit:cover}.sarah-header-text strong{display:block;font-size:.88rem;font-weight:600;color:#fff}.sarah-header-text span{font-size:.72rem;color:rgba(255,255,255,.4)}.sarah-online{width:8px;height:8px;background:#4ade80;border-radius:50%;position:absolute;right:16px;top:50%;transform:translateY(-50%)}.sarah-messages{height:260px;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:#f7f3ee}.smsg{display:flex;align-items:flex-end;gap:7px}.smsg.user{flex-direction:row-reverse}.smsg-av{width:26px;height:26px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1.5px solid #c8922a}.smsg-av img{width:100%;height:100%;object-fit:cover}.smsg-bubble{max-width:78%;padding:9px 12px;border-radius:12px;font-size:.83rem;line-height:1.65}.smsg.ai .smsg-bubble{background:#fff;color:#0c1f3d;border-bottom-left-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.06)}.smsg.user .smsg-bubble{background:#0c1f3d;color:#fff;border-bottom-right-radius:3px}.sarah-typing{display:flex;align-items:flex-end;gap:7px}.sarah-typing-bubble{background:#fff;border-radius:12px;border-bottom-left-radius:3px;padding:9px 12px;display:flex;gap:3px;align-items:center}.sdot{width:5px;height:5px;background:#bbb;border-radius:50%;animation:sdotB 1.2s infinite}.sdot:nth-child(2){animation-delay:.2s}.sdot:nth-child(3){animation-delay:.4s}@keyframes sdotB{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}.sarah-input-area{border-top:1px solid #e2ddd6;padding:10px 12px;background:#fff}.sarah-input-row{display:flex;align-items:center;gap:8px;background:#f7f3ee;border:1.5px solid #e2ddd6;border-radius:10px;padding:8px 12px;transition:border-color .2s}.sarah-input-row:focus-within{border-color:#c8922a}.sarah-input-row textarea{flex:1;border:none;background:transparent;font-family:inherit;font-size:.83rem;color:#0c1f3d;resize:none;outline:none;line-height:1.5;max-height:70px;overflow-y:auto}.sarah-input-row textarea::placeholder{color:#bbb}.sarah-send{width:32px;height:32px;border-radius:7px;background:#0c1f3d;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0}.sarah-send:hover{background:#162d52}.sarah-note{text-align:center;font-size:.7rem;color:#bbb;margin-top:6px}</style>"

SARAH_JS = """<script>
(function(){
var img="https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face";
var history=[],stage="story",collected={},loading=false;
var system="You are Sarah, a warm intake assistant for eSolicitors.ie. Be human and warm. Ask about situation, then name, then phone. No legal advice. Respond ONLY JSON: {\\"message\\":\\"...\\",\\"next_stage\\":\\"details|name|phone|done\\"}";
var msgs=document.getElementById("sarahMsgs");
var input=document.getElementById("sarahInput");
function addMsg(isUser){var row=document.createElement("div");row.className="smsg"+(isUser?" user":"");if(!isUser){var av=document.createElement("div");av.className="smsg-av";av.innerHTML="<img src=\\""+img+"\\" alt=\\"Sarah\\"/>";row.appendChild(av);}var b=document.createElement("div");b.className="smsg-bubble";row.appendChild(b);msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;return b;}
function type(el,text,cb){var w=text.split(" ");var i=0;el.textContent="";function n(){if(i<w.length){el.textContent+=(i===0?"": " ")+w[i];i++;setTimeout(n,40+Math.random()*15);}else{if(cb)cb();}}n();}
function showTyping(){var r=document.createElement("div");r.className="sarah-typing";r.id="sarahTyping";r.innerHTML="<div class=\\"smsg-av\\"><img src=\\""+img+"\\"/></div><div class=\\"sarah-typing-bubble\\"><div class=\\"sdot\\"></div><div class=\\"sdot\\"></div><div class=\\"sdot\\"></div></div>";msgs.appendChild(r);msgs.scrollTop=msgs.scrollHeight;}
function removeTyping(){var t=document.getElementById("sarahTyping");if(t)t.remove();}
function send(){if(!input)return;var text=input.value.trim();if(!text||loading)return;input.value="";input.style.height="auto";loading=true;addMsg(true).textContent=text;history.push({role:"user",content:text});if(stage==="name")collected.name=text;if(stage==="phone")collected.phone=text;setTimeout(function(){showTyping();setTimeout(function(){fetch("/api/chat",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({system:system+"\\nStage: "+stage,messages:history})}).then(function(r){removeTyping();if(!r.ok){addMsg(false).textContent="Something went wrong.";loading=false;return;}return r.json();}).then(function(d){if(!d)return;var raw=(d.content&&d.content[0]&&d.content[0].text)||"";var p;try{var m=raw.replace(/```json|```/g,"").trim().match(/\\{[\\s\\S]*\\}/);p=m?JSON.parse(m[0]):null;if(!p||!p.message)throw 0;}catch(e){p={message:raw||"Something went wrong.",next_stage:stage};}var b=addMsg(false);type(b,p.message,function(){msgs.scrollTop=msgs.scrollHeight;});history.push({role:"assistant",content:p.message});if(p.next_stage)stage=p.next_stage;if(stage==="done"&&collected.phone){var tr=history.map(function(m){return(m.role==="user"?"Visitor: ":"Sarah: ")+m.content;}).join("\\n");fetch("/api/leads",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({name:collected.name||"",phone:collected.phone||"",issue:history[0]&&history[0].content?history[0].content.substring(0,120):"",transcript:tr,source:window.location.pathname})});}loading=false;}).catch(function(){removeTyping();addMsg(false).textContent="Network error.";loading=false;});},Math.min(text.length*12,1000));},400);};
if(input){input.addEventListener("input",function(){this.style.height="auto";this.style.height=Math.min(this.scrollHeight,70)+"px";});input.addEventListener("keydown",function(e){if(e.key==="Enter"&&!e.shiftKey){e.preventDefault();send();}});}
window.sarahDebtSend=send;
setTimeout(function(){var b=addMsg(false);type(b,"Hi, I'm Sarah from eSolicitors.ie. Tell me about your situation — what's happened and what you need help with.",function(){msgs.scrollTop=msgs.scrollHeight;});},700);
})();
</script>"""

def call_api(prompt):
    payload = json.dumps({"model":MODEL,"max_tokens":800,"system":SYSTEM,"messages":[{"role":"user","content":prompt}]}).encode()
    req = urllib.request.Request("https://api.anthropic.com/v1/messages", data=payload,
        headers={"Content-Type":"application/json","x-api-key":API_KEY,"anthropic-version":"2023-06-01"}, method="POST")
    try:
        with urllib.request.urlopen(req) as r:
            return json.loads(r.read())["content"][0]["text"].strip()
    except Exception as e:
        print(f"  API error: {e}")
        return None

def nav():
    return '''<nav style="position:sticky;top:0;z-index:100;background:#0c1f3d;border-bottom:1px solid rgba(200,146,42,.2);padding:0 5%;height:62px;display:flex;align-items:center;justify-content:space-between">
  <a href="/" style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:#c8922a">Solicitors</span>.ie</a>
  <ul style="display:flex;gap:20px;list-style:none;align-items:center">
    <li><a href="/personal-injury/" style="color:rgba(255,255,255,.6);text-decoration:none;font-size:.85rem">Personal Injury</a></li>
    <li><a href="/employment-law/" style="color:rgba(255,255,255,.6);text-decoration:none;font-size:.85rem">Employment</a></li>
    <li><a href="/debt-law/" style="color:rgba(255,255,255,.6);text-decoration:none;font-size:.85rem">Debt</a></li>
    <li><a href="/chat.html" style="background:#c8922a;color:#0c1f3d;padding:8px 18px;border-radius:6px;font-weight:600;text-decoration:none;font-size:.85rem">Get Help Free</a></li>
  </ul>
</nav>'''

def footer():
    return '''<footer style="background:#080f1e;padding:36px 5%">
  <div style="max-width:1100px;margin:0 auto;display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;margin-bottom:24px">
    <a href="/" style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:#c8922a">Solicitors</span>.ie</a>
    <div style="display:flex;gap:40px;flex-wrap:wrap">
      <div><h4 style="font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-bottom:12px">Debt Law</h4>
        <ul style="list-style:none;display:flex;flex-direction:column;gap:8px">
          <li><a href="/debt-law/bailiff-at-door-ireland/" style="color:rgba(255,255,255,.3);text-decoration:none;font-size:.83rem">Bailiff at the Door</a></li>
          <li><a href="/debt-law/being-sued-for-money-ireland/" style="color:rgba(255,255,255,.3);text-decoration:none;font-size:.83rem">Being Sued for Money</a></li>
          <li><a href="/debt-law/cant-pay-mortgage-ireland/" style="color:rgba(255,255,255,.3);text-decoration:none;font-size:.83rem">Can't Pay Mortgage</a></li>
          <li><a href="/debt-law/car-repossession-ireland/" style="color:rgba(255,255,255,.3);text-decoration:none;font-size:.83rem">Car Repossession</a></li>
        </ul>
      </div>
    </div>
  </div>
  <div style="border-top:1px solid rgba(255,255,255,.07);padding-top:16px">
    <span style="font-size:.72rem;color:rgba(255,255,255,.22)">© 2026 eSolicitors.ie Ltd. eSolicitors.ie is a referral service, not a law firm.</span>
  </div>
</footer>'''

def sarah_widget():
    return f'''{SARAH_CSS}
<div class="sarah-widget">
  <div class="sarah-header">
    <div class="sarah-av"><img src="{SARAH_IMG}" alt="Sarah"/></div>
    <div class="sarah-header-text"><strong>Sarah — eSolicitors.ie</strong><span>Legal intake · Free · Confidential</span></div>
    <div class="sarah-online"></div>
  </div>
  <div class="sarah-messages" id="sarahMsgs"></div>
  <div class="sarah-input-area">
    <div class="sarah-input-row">
      <textarea id="sarahInput" rows="1" placeholder="Tell me about your situation..."></textarea>
      <button class="sarah-send" onclick="sarahDebtSend()"><svg width="14" height="14" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg></button>
    </div>
    <div class="sarah-note">Confidential · Free · No obligation</div>
  </div>
</div>
{SARAH_JS}'''

def build_page(page, content):
    topics_html = ""
    if page.get("topics"):
        topics_html = '<div style="display:flex;flex-direction:column;gap:12px;margin-top:24px">'
        for t in page["topics"]:
            topics_html += f'<a href="{t["url"]}" style="background:#fff;border:1px solid #e8e2d9;border-left:3px solid #c8922a;border-radius:0 10px 10px 0;padding:18px;text-decoration:none;display:block;transition:box-shadow .2s"><div style="font-size:.9rem;font-weight:700;color:#0c1f3d;margin-bottom:5px">{t["title"]}</div><div style="font-size:.82rem;color:#4a5568;line-height:1.6">{t["desc"]}</div><div style="font-size:.75rem;color:#c8922a;font-weight:600;margin-top:8px">Find out more →</div></a>'
        topics_html += '</div>'

    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page["title"]} | eSolicitors.ie</title>
<meta name="description" content="{page["meta"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0c1f3d;--navy-mid:#162d52;--gold:#c8922a;--gold-light:#e8b04a;--cream:#f7f3ee;--border:#e8e2d9;--white:#fff;--text-mid:#4a5568}}
body{{font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--navy);overflow-x:hidden}}
</style>
</head>
<body>
{nav()}
<section style="background:var(--navy);padding:56px 5% 64px;position:relative;overflow:hidden">
  <div style="position:absolute;top:-100px;right:-100px;width:500px;height:500px;background:radial-gradient(circle,rgba(200,146,42,.08) 0%,transparent 70%);pointer-events:none"></div>
  <div style="max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 400px;gap:56px;align-items:start;position:relative;z-index:1">
    <div>
      <div style="display:inline-flex;align-items:center;background:rgba(200,146,42,.12);border:1px solid rgba(200,146,42,.3);color:#e8b04a;padding:5px 13px;border-radius:100px;font-size:.72rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:22px">⚖️ Debt Law Ireland</div>
      <h1 style="font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;color:#fff;line-height:1.1;letter-spacing:-.02em;margin-bottom:18px;white-space:pre-line">{page["h1"].replace("<em>","<em style='font-style:italic;color:#c8922a'>")}</h1>
      <p style="font-size:.97rem;color:rgba(255,255,255,.6);line-height:1.85;font-weight:300;margin-bottom:28px">{page["intro"]}</p>
    </div>
    <div>{sarah_widget()}</div>
  </div>
</section>
<div style="max-width:1100px;margin:0 auto;padding:0 5%">
  <div style="padding:52px 0;border-bottom:1px solid var(--border)">
    <div style="font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:10px">Irish Law</div>
    <h2 style="font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;color:var(--navy);margin-bottom:14px">What the law says</h2>
    <div style="font-size:.95rem;color:var(--text-mid);line-height:1.9;font-weight:300;max-width:720px">{content.replace(chr(10), '<br><br>')}</div>
    <div style="background:#fff;border:1.5px solid var(--border);border-left:4px solid var(--navy);border-radius:0 10px 10px 0;padding:18px 22px;margin-top:20px;max-width:720px">
      <div style="font-size:.72rem;font-weight:700;color:var(--navy);text-transform:uppercase;letter-spacing:.06em;margin-bottom:7px">Legal Framework</div>
      <p style="font-size:.86rem;color:var(--text-mid);line-height:1.75">{page["law"]}</p>
    </div>
  </div>
  {f'<div style="padding:52px 0"><div style="font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:10px">Situations We Cover</div><h2 style="font-family:\'Playfair Display\',serif;font-size:1.7rem;font-weight:700;color:var(--navy);margin-bottom:6px">What brought you here?</h2><p style="font-size:.9rem;color:var(--text-mid);margin-bottom:0">{topics_html}</p></div>' if topics_html else ''}
</div>
<div style="background:var(--navy);padding:60px 5%;text-align:center">
  <div style="max-width:600px;margin:0 auto 28px">
    <div style="font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:12px">Free Solicitor Matching</div>
    <h2 style="font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:12px;line-height:1.2">Sound familiar?<br>Get matched with a specialist.</h2>
    <p style="color:rgba(255,255,255,.55);font-size:.92rem;margin-bottom:0;line-height:1.7">Tell Sarah what happened. Free, confidential, no obligation.</p>
  </div>
</div>
{footer()}
</body>
</html>'''

for page in PAGES:
    if os.path.exists(page["path"]):
        print(f"Skip: {page['path']}")
        continue
    print(f"Generating: {page['path']}")
    content = call_api(page["prompt"])
    if not content:
        print(f"  FAILED")
        continue
    html = build_page(page, content)
    os.makedirs(os.path.dirname(page["path"]), exist_ok=True)
    with open(page["path"], "w", encoding="utf-8") as f:
        f.write(html)
    print(f"  Saved: {page['path']}")
    time.sleep(0.5)

print("Done.")
