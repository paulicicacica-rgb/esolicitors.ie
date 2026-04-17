import os, json, re, time, urllib.request, urllib.error, unicodedata

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

# ── LANGUAGE CONFIG ──────────────────────────────────────────────────────────

LANGUAGES = {
    "ro": {
        "name": "Romanian",
        "folder": "ro",
        "assistant": "Mirela",
        "assistant_img": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face",
        "greeting": "Bună, sunt Mirela de la eSolicitors.ie. Spune-mi ce s-a întâmplat și mă asigur că ajungi la avocatul potrivit.",
        "placeholder": "Spune-mi ce s-a întâmplat...",
        "cta_label": "Potrivire gratuită cu avocat",
        "cta_title": "Ești în situația potrivită?<br>Poți avea un caz.",
        "cta_sub": "Spune-i Mirelei ce s-a întâmplat. Ea îți explică opțiunile și te pune în legătură cu avocatul potrivit — gratuit.",
        "confidential": "Confidențial · Gratuit · Fără obligații",
        "back_label": "Înapoi la",
        "nav_home": "Acasă",
        "nav_cta": "Vorbește cu Mirela",
        "footer_disclaimer": "eSolicitors.ie este un serviciu de referire, nu o firmă de avocatură.",
        "solicitors": [
            {"name": "Ioan Popescu", "area": "Drept rutier & penal", "county": "Dublin", "img": "https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=80&h=80&fit=crop&crop=face"},
            {"name": "Maria Constantin", "area": "Infracțiuni de trafic", "county": "Cork", "img": "https://images.unsplash.com/photo-1580489944761-15a19d654956?w=80&h=80&fit=crop&crop=face"},
            {"name": "Alexandru Ionescu", "area": "Apărare penală", "county": "Galway", "img": "https://images.unsplash.com/photo-1560250097-0b93528c311a?w=80&h=80&fit=crop&crop=face"},
        ],
        "system_prompt": "Ești Mirela, o asistentă caldă de la eSolicitors.ie. Vorbești DOAR în română. Ești empatică și umană. ETAPA story: răspunde cu empatie 2-3 propoziții, nu da sfaturi juridice, întreabă prenumele, next_stage: name, show_solicitors: true. ETAPA name: folosește prenumele, întreabă numărul de telefon, next_stage: phone. ETAPA phone: confirmă că un avocat îl contactează în câteva ore, next_stage: done. REGULI: fără sfaturi juridice, max 3 propoziții, fără emoji, română simplă. Răspunde DOAR JSON: {\"message\":\"...\",\"next_stage\":\"name|phone|done\",\"show_solicitors\":false}",
    },
    "pt-br": {
        "name": "Brazilian Portuguese",
        "folder": "pt-br",
        "assistant": "Ana",
        "assistant_img": "https://images.unsplash.com/photo-1544005313-94ddf0286df2?w=80&h=80&fit=crop&crop=face",
        "greeting": "Oi, sou Ana da eSolicitors.ie. Me conta o que aconteceu e vou te conectar com o advogado certo.",
        "placeholder": "Me conta o que aconteceu...",
        "cta_label": "Orientação jurídica gratuita",
        "cta_title": "Passou por algo parecido?<br>Você pode ter um caso.",
        "cta_sub": "Conta para a Ana o que aconteceu. Ela explica suas opções e te conecta com o advogado certo — de graça.",
        "confidential": "Confidencial · Gratuito · Sem compromisso",
        "back_label": "Voltar para",
        "nav_home": "Início",
        "nav_cta": "Falar com Ana",
        "footer_disclaimer": "eSolicitors.ie é um serviço de indicação, não um escritório de advocacia.",
        "solicitors": [
            {"name": "Carlos Silva", "area": "Direito de trânsito & penal", "county": "Dublin", "img": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&h=80&fit=crop&crop=face"},
            {"name": "Ana Rodrigues", "area": "Infrações de trânsito", "county": "Cork", "img": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=80&h=80&fit=crop&crop=face"},
            {"name": "Roberto Santos", "area": "Defesa criminal", "county": "Galway", "img": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop&crop=face"},
        ],
        "system_prompt": "Você é Ana, uma assistente calorosa da eSolicitors.ie. Fala APENAS português brasileiro. É empática e humana. ETAPA story: responda com empatia 2-3 frases, não dê conselhos jurídicos, pergunte o primeiro nome, next_stage: name, show_solicitors: true. ETAPA name: use o nome, pergunte o número de telefone, next_stage: phone. ETAPA phone: confirme que um advogado entrará em contato em algumas horas, next_stage: done. REGRAS: sem conselhos jurídicos, máx 3 frases, sem emoji, português simples. Responda APENAS JSON: {\"message\":\"...\",\"next_stage\":\"name|phone|done\",\"show_solicitors\":false}",
    },
    "pl": {
        "name": "Polish",
        "folder": "pl",
        "assistant": "Kasia",
        "assistant_img": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=80&h=80&fit=crop&crop=face",
        "greeting": "Cześć, jestem Kasia z eSolicitors.ie. Powiedz mi co się stało i znajdę dla ciebie odpowiedniego prawnika.",
        "placeholder": "Powiedz mi co się stało...",
        "cta_label": "Bezpłatne dopasowanie prawnika",
        "cta_title": "Jesteś w podobnej sytuacji?<br>Możesz mieć sprawę.",
        "cta_sub": "Powiedz Kasi co się stało. Wyjaśni twoje opcje i połączy cię z odpowiednim prawnikiem — bezpłatnie.",
        "confidential": "Poufnie · Bezpłatnie · Bez zobowiązań",
        "back_label": "Wróć do",
        "nav_home": "Strona główna",
        "nav_cta": "Porozmawiaj z Kasią",
        "footer_disclaimer": "eSolicitors.ie to serwis pośrednictwa, nie kancelaria prawna.",
        "solicitors": [
            {"name": "Marek Kowalski", "area": "Prawo drogowe & karne", "county": "Dublin", "img": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=80&h=80&fit=crop&crop=face"},
            {"name": "Anna Wiśniewska", "area": "Wykroczenia drogowe", "county": "Cork", "img": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop&crop=face"},
            {"name": "Piotr Nowak", "area": "Obrona karna", "county": "Galway", "img": "https://images.unsplash.com/photo-1463453091185-61582044d556?w=80&h=80&fit=crop&crop=face"},
        ],
        "system_prompt": "Jesteś Kasią, ciepłą asystentką z eSolicitors.ie. Mówisz TYLKO po polsku. Jesteś empatyczna i ludzka. ETAP story: odpowiedz z empatią 2-3 zdania, nie dawaj porad prawnych, zapytaj o imię, next_stage: name, show_solicitors: true. ETAP name: użyj imienia, zapytaj o numer telefonu, next_stage: phone. ETAP phone: potwierdź że prawnik skontaktuje się w ciągu kilku godzin, next_stage: done. ZASADY: bez porad prawnych, maks 3 zdania, bez emoji, prosty polski. Odpowiedz TYLKO JSON: {\"message\":\"...\",\"next_stage\":\"name|phone|done\",\"show_solicitors\":false}",
    },
    "ar": {
        "name": "Arabic",
        "folder": "ar",
        "assistant": "Layla",
        "assistant_img": "https://images.unsplash.com/photo-1551836022-d5d88e9218df?w=80&h=80&fit=crop&crop=face",
        "greeting": "مرحباً، أنا ليلى من eSolicitors.ie. أخبرني بما حدث وسأتأكد من وصولك إلى المحامي المناسب.",
        "placeholder": "أخبرني بما حدث...",
        "cta_label": "مطابقة مجانية مع محامٍ",
        "cta_title": "هل وجدت نفسك في موقف مماثل؟<br>قد يكون لديك قضية.",
        "cta_sub": "أخبر ليلى بما حدث. ستشرح خياراتك وتربطك بالمحامي المناسب في مقاطعتك — مجاناً تماماً.",
        "confidential": "سري · مجاني · بدون التزام",
        "back_label": "العودة إلى",
        "nav_home": "الرئيسية",
        "nav_cta": "تحدث مع ليلى",
        "footer_disclaimer": "eSolicitors.ie خدمة إحالة وليست مكتب محاماة.",
        "solicitors": [
            {"name": "Ahmad Hassan", "area": "قانون المرور والجنائي", "county": "Dublin", "img": "https://images.unsplash.com/photo-1506794778202-cad84cf45f1d?w=80&h=80&fit=crop&crop=face"},
            {"name": "Fatima Al-Rashid", "area": "مخالفات المرور", "county": "Cork", "img": "https://images.unsplash.com/photo-1529626455594-4ff0802cfb7e?w=80&h=80&fit=crop&crop=face"},
            {"name": "Omar Khalil", "area": "الدفاع الجنائي", "county": "Galway", "img": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop&crop=face"},
        ],
        "system_prompt": "أنتِ ليلى، مساعدة دافئة من eSolicitors.ie. تتحدثين باللغة العربية فقط. أنتِ متعاطفة وإنسانية. مرحلة story: أجيبي بتعاطف 2-3 جمل، لا تعطي نصائح قانونية، اسألي عن الاسم الأول، next_stage: name، show_solicitors: true. مرحلة name: استخدمي الاسم، اسألي عن رقم الهاتف، next_stage: phone. مرحلة phone: أكدي أن محامياً سيتواصل خلال ساعات، next_stage: done. القواعد: بدون نصائح قانونية، مقصورة على 3 جمل، بدون إيموجي، عربية بسيطة. أجيبي فقط بـ JSON: {\"message\":\"...\",\"next_stage\":\"name|phone|done\",\"show_solicitors\":false}",
    },
    "es": {
        "name": "Spanish",
        "folder": "es",
        "assistant": "Carmen",
        "assistant_img": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=80&h=80&fit=crop&crop=face",
        "greeting": "Hola, soy Carmen de eSolicitors.ie. Cuéntame qué pasó y me aseguro de que llegues al abogado adecuado.",
        "placeholder": "Cuéntame qué pasó...",
        "cta_label": "Orientación jurídica gratuita",
        "cta_title": "¿Estás en una situación similar?<br>Puede que tengas un caso.",
        "cta_sub": "Cuéntale a Carmen qué pasó. Ella te explicará tus opciones y te conectará con el abogado adecuado — gratis.",
        "confidential": "Confidencial · Gratuito · Sin compromiso",
        "back_label": "Volver a",
        "nav_home": "Inicio",
        "nav_cta": "Hablar con Carmen",
        "footer_disclaimer": "eSolicitors.ie es un servicio de referencia, no un despacho de abogados.",
        "solicitors": [
            {"name": "Carlos García", "area": "Derecho de tráfico & penal", "county": "Dublin", "img": "https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?w=80&h=80&fit=crop&crop=face"},
            {"name": "María López", "area": "Infracciones de tráfico", "county": "Cork", "img": "https://images.unsplash.com/photo-1487412720507-e7ab37603c6f?w=80&h=80&fit=crop&crop=face"},
            {"name": "Javier Martínez", "area": "Defensa penal", "county": "Galway", "img": "https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=80&h=80&fit=crop&crop=face"},
        ],
        "system_prompt": "Eres Carmen, una asistente cálida de eSolicitors.ie. Hablas SOLO en español. Eres empática y humana. ETAPA story: responde con empatía 2-3 frases, no des consejos legales, pregunta el nombre, next_stage: name, show_solicitors: true. ETAPA name: usa el nombre, pregunta el número de teléfono, next_stage: phone. ETAPA phone: confirma que un abogado contactará en horas, next_stage: done. REGLAS: sin consejos legales, máx 3 frases, sin emoji, español sencillo. Responde SOLO JSON: {\"message\":\"...\",\"next_stage\":\"name|phone|done\",\"show_solicitors\":false}",
    },
    "ru": {
        "name": "Russian",
        "folder": "ru",
        "assistant": "Natasha",
        "assistant_img": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop&crop=face",
        "greeting": "Привет, я Наташа из eSolicitors.ie. Расскажи мне что случилось и я подберу тебе нужного адвоката.",
        "placeholder": "Расскажи что случилось...",
        "cta_label": "Бесплатный подбор адвоката",
        "cta_title": "Оказался в похожей ситуации?<br>Возможно, у тебя есть дело.",
        "cta_sub": "Расскажи Наташе что случилось. Она объяснит варианты и подберёт нужного адвоката в твоём округе — бесплатно.",
        "confidential": "Конфиденциально · Бесплатно · Без обязательств",
        "back_label": "Назад к",
        "nav_home": "Главная",
        "nav_cta": "Говорить с Наташей",
        "footer_disclaimer": "eSolicitors.ie — реферальный сервис, не юридическая фирма.",
        "solicitors": [
            {"name": "Alexei Petrov", "area": "Дорожное & уголовное право", "county": "Dublin", "img": "https://images.unsplash.com/photo-1519085360753-af0119f7cbe7?w=80&h=80&fit=crop&crop=face"},
            {"name": "Natalia Sokolova", "area": "Дорожные нарушения", "county": "Cork", "img": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=80&h=80&fit=crop&crop=face"},
            {"name": "Dmitri Volkov", "area": "Уголовная защита", "county": "Galway", "img": "https://images.unsplash.com/photo-1463453091185-61582044d556?w=80&h=80&fit=crop&crop=face"},
        ],
        "system_prompt": "Ты Наташа, тёплый ассистент eSolicitors.ie. Говоришь ТОЛЬКО по-русски. Ты эмпатична и человечна. ЭТАП story: ответь с сочувствием 2-3 предложения, не давай юридических советов, спроси имя, next_stage: name, show_solicitors: true. ЭТАП name: используй имя, спроси номер телефона, next_stage: phone. ЭТАП phone: подтверди что адвокат свяжется в течение часов, next_stage: done. ПРАВИЛА: без юридических советов, макс 3 предложения, без эмодзи, простой русский. Отвечай ТОЛЬКО JSON: {\"message\":\"...\",\"next_stage\":\"name|phone|done\",\"show_solicitors\":false}",
    },
}

# ── TOPICS PER LANGUAGE ──────────────────────────────────────────────────────

TOPICS = {
    "ro": [
        {"slug": "condus-beat", "title": "Prins Băut la Volan în Irlanda", "h1": "Prins <em>băut la volan</em><br>în Irlanda.", "search_query": "prins băut la volan avocat irlanda", "law": "Road Traffic Act 2010 — limita legală este 50mg/100ml sânge", "time_limit": "Acționează imediat după ce ai primit citația", "practice_area": "criminal-law", "stories": [{"slug": "ion-dublin", "name": "Ion", "city": "Dublin", "gender": "m", "situation": "Oprit la un control de rutină cu alcoolemia de 58mg — puțin peste limita de 50mg. Risca pierderea permisului și a locului de muncă.", "outcome": "Acuzație respinsă — permis păstrat"}, {"slug": "maria-cork", "name": "Maria", "city": "Cork", "gender": "f", "situation": "Oprită după un accident minor. Prima abatere. Îngrijorată de efectul asupra carierei în domeniul sănătății.", "outcome": "Suspendare redusă la minimum legal"}, {"slug": "andrei-galway", "name": "Andrei", "city": "Galway", "gender": "m", "situation": "Alcoolemie ridicată. A crezut că nu are nicio șansă. Avocatul a identificat un viciu procedural.", "outcome": "Dosar respins — viciu procedural"}, {"slug": "elena-limerick", "name": "Elena", "city": "Limerick", "gender": "f", "situation": "Asistentă medicală. O condamnare i-ar fi pus în pericol licența profesională.", "outcome": "Licența profesională protejată"}]},
        {"slug": "fara-asigurare", "title": "Prins Fără Asigurare în Irlanda", "h1": "Prins <em>fără asigurare</em><br>în Irlanda.", "search_query": "prins fara asigurare in irlanda ce se intampla", "law": "Road Traffic Act — conducerea fără asigurare este infracțiune penală. Amendă obligatorie și suspendare.", "time_limit": "Contactează un avocat înainte de data judecății", "practice_area": "criminal-law", "stories": [{"slug": "gheorghe-dublin", "name": "Gheorghe", "city": "Dublin", "gender": "m", "situation": "Conducea mașina soției fără să știe că nu era asigurat pentru el. Oprit la control.", "outcome": "Amendă redusă — fără suspendare"}, {"slug": "alina-cork", "name": "Alina", "city": "Cork", "gender": "f", "situation": "Asigurarea expirată cu două zile înainte. Nu primise nicio notificare.", "outcome": "Dosar respins — circumstanțe atenuante"}, {"slug": "mihai-galway", "name": "Mihai", "city": "Galway", "gender": "m", "situation": "Mașina asigurată de angajator. Angajatorul uitase să reînnoiască polița.", "outcome": "Angajatorul a preluat răspunderea"}, {"slug": "cristina-limerick", "name": "Cristina", "city": "Limerick", "gender": "f", "situation": "Prima abatere. Asigurare cumpărată online dar nu activată corect.", "outcome": "Penalitate fixă — fără dosar penal"}]},
        {"slug": "fara-permis", "title": "Prins Fără Permis în Irlanda", "h1": "Prins <em>fără permis</em><br>în Irlanda.", "search_query": "prins fara permis de conducere irlanda", "law": "Road Traffic Act — conducerea fără permis valid este infracțiune. Permisul românesc este valid în Irlanda doar temporar.", "time_limit": "Acționează înainte de data judecății", "practice_area": "criminal-law", "stories": [{"slug": "radu-dublin", "name": "Radu", "city": "Dublin", "gender": "m", "situation": "Permisul românesc expirat. Nu știa că trebuia să-l preschimbe în permis irlandez.", "outcome": "Amendă redusă — circumstanțe atenuante"}, {"slug": "ioana-cork", "name": "Ioana", "city": "Cork", "gender": "f", "situation": "Permis provizoriu. Conducea singură fără instructor — credea că e permis.", "outcome": "Penalitate minimă — prima abatere"}, {"slug": "bogdan-galway", "name": "Bogdan", "city": "Galway", "gender": "m", "situation": "Permisul suspendat dintr-o infracțiune anterioară. Nu știa că suspendarea era încă activă.", "outcome": "Negociere — suspendare redusă"}, {"slug": "laura-limerick", "name": "Laura", "city": "Limerick", "gender": "f", "situation": "Permis din afara UE. Conducea cu permis din Moldova care nu e recunoscut automat.", "outcome": "Dosar retras după regularizare"}]},
        {"slug": "accident-rutier", "title": "Accident Rutier cu Vătămare în Irlanda", "h1": "Accident rutier.<br><em>Ai dreptul la despăgubire.</em>", "search_query": "am avut accident cu masina in irlanda despagubire", "law": "Civil Liability Act — termenul de prescripție este 2 ani de la data accidentului.", "time_limit": "2 ani de la data accidentului — acționează cât mai repede", "practice_area": "personal-injury", "stories": [{"slug": "stefan-dublin", "name": "Ștefan", "city": "Dublin", "gender": "m", "situation": "Lovit din spate pe autostradă. Asigurarea celuilalt șofer a oferit €8,000. Avocatul a obținut mult mai mult.", "outcome": "Despăgubire de €34,000"}, {"slug": "diana-cork", "name": "Diana", "city": "Cork", "gender": "f", "situation": "Pasageră în mașina unui prieten care a cauzat accidentul. Nu știa că poate revendica.", "outcome": "Despăgubire integrală acordată"}, {"slug": "vasile-galway", "name": "Vasile", "city": "Galway", "gender": "m", "situation": "Pietone lovit pe trecere. Șoferul a negat responsabilitatea inițial.", "outcome": "Responsabilitate stabilită — despăgubire acordată"}, {"slug": "ana-limerick", "name": "Ana", "city": "Limerick", "gender": "f", "situation": "Accident la locul de muncă — lovită de o furgonetă în depozit.", "outcome": "Despăgubire include venituri pierdute"}]},
        {"slug": "condus-periculos", "title": "Condus Periculos sau Neglijent în Irlanda", "h1": "Acuzat de <em>condus periculos</em><br>în Irlanda.", "search_query": "acuzat condus periculos irlanda ce fac", "law": "Road Traffic Act — condusul periculos poate duce la închisoare. Condusul neglijent — amendă și suspendare.", "time_limit": "Contactează un avocat imediat după citație", "practice_area": "criminal-law", "stories": [{"slug": "florin-dublin", "name": "Florin", "city": "Dublin", "gender": "m", "situation": "Acuzat de condus neglijent după un accident pe vreme rea. Șofea cu viteză normală.", "outcome": "Acuzație redusă — fără suspendare"}, {"slug": "roxana-cork", "name": "Roxana", "city": "Cork", "gender": "f", "situation": "Schimbare de bandă ce a dus la accident minor. Acuzată de condus periculos.", "outcome": "Reclasificat ca neglijent — penalitate minimă"}, {"slug": "cosmin-galway", "name": "Cosmin", "city": "Galway", "gender": "m", "situation": "Viteza depășită cu 30km/h. Prima abatere cu dosar curat.", "outcome": "Amendă și puncte — fără suspendare"}, {"slug": "simona-limerick", "name": "Simona", "city": "Limerick", "gender": "f", "situation": "Accident în parcare. Cealaltă parte a exagerat amploarea daunelor.", "outcome": "Acuzații reduse — despăgubire minimă"}]},
        {"slug": "concediere-abuziva", "title": "Concediere Abuzivă în Irlanda", "h1": "Concediat<em> fără motiv</em><br>în Irlanda.", "search_query": "concediere abuziva irlanda ce drepturi am", "law": "Unfair Dismissals Act 1977 — ai dreptul să depui plângere la WRC în termen de 6 luni.", "time_limit": "6 luni de la data concedierii — nu rata termenul", "practice_area": "employment-law", "stories": [{"slug": "marius-dublin", "name": "Marius", "city": "Dublin", "gender": "m", "situation": "Concediat după 5 ani fără avertismente sau procedură disciplinară. Angajatorul a spus că e restructurare.", "outcome": "WRC a decis în favoarea lui — compensație acordată"}, {"slug": "teodora-cork", "name": "Teodora", "city": "Cork", "gender": "f", "situation": "Concediată la scurt timp după ce a anunțat sarcina. Angajatorul a invocat alte motive.", "outcome": "Discriminare confirmată — compensație maximă"}, {"slug": "vlad-galway", "name": "Vlad", "city": "Galway", "gender": "m", "situation": "Dat afară după ce a raportat condiții nesigure. Niciun avertisment prealabil.", "outcome": "Concediere retaliativă — compensație suplimentară"}, {"slug": "oana-limerick", "name": "Oana", "city": "Limerick", "gender": "f", "situation": "Post eliminat dar o colegă mai tânără a preluat aceleași sarcini.", "outcome": "Restructurare falsă dovedită — compensație acordată"}]},
        {"slug": "probleme-chirias", "title": "Probleme cu Proprietarul în Irlanda", "h1": "Proprietarul<em> îți încalcă drepturile.</em><br>Iată ce poți face.", "search_query": "proprietar ma da afara ilegal irlanda drepturi chirias", "law": "Residential Tenancies Act — chiriașii au drepturi legale puternice. RTB mediază disputele.", "time_limit": "Depune plângere la RTB în termen de 28 zile de la incident", "practice_area": "property-law", "stories": [{"slug": "nicu-dublin", "name": "Nicu", "city": "Dublin", "gender": "m", "situation": "Proprietarul i-a dat 30 de zile să plece în ianuarie. 3 ani de chirie plătită la timp.", "outcome": "Evacuare blocată — a putut rămâne"}, {"slug": "irina-cork", "name": "Irina", "city": "Cork", "gender": "f", "situation": "Proprietarul a reținut toată caución invocând daune inexistente.", "outcome": "Cauțiunea returnată integral"}, {"slug": "daniel-galway", "name": "Daniel", "city": "Galway", "gender": "m", "situation": "Chiria mărită cu 25% fără notificare corespunzătoare.", "outcome": "Majorare anulată — chiria anterioară menținută"}, {"slug": "sorina-limerick", "name": "Sorina", "city": "Limerick", "gender": "f", "situation": "Proprietarul a intrat în apartament fără permisiune de mai multe ori.", "outcome": "RTB a emis ordin de respectare a drepturilor"}]},
        {"slug": "divort-irlanda", "title": "Divorț în Irlanda — Ghid pentru Români", "h1": "Divorț<em> în Irlanda.</em><br>Ce trebuie să știi.", "search_query": "cum fac divort in irlanda roman", "law": "Family Law Act — divorțul în Irlanda necesită separare de cel puțin 2 ani din ultimii 3.", "time_limit": "Nu există termen limită — dar acționează repede pentru protejarea activelor", "practice_area": "family-law", "stories": [{"slug": "carmen-dublin", "name": "Carmen", "city": "Dublin", "gender": "f", "situation": "Căsătorită 12 ani. Voia divorț dar nu știa dacă divorțul irlandez e recunoscut în România.", "outcome": "Divorț finalizat — recunoscut în UE"}, {"slug": "octavian-cork", "name": "Octavian", "city": "Cork", "gender": "m", "situation": "Soția a plecat în România cu copiii. Nu știa ce drepturi are.", "outcome": "Acord de custodie stabilit prin instanță"}, {"slug": "mihaela-galway", "name": "Mihaela", "city": "Galway", "gender": "f", "situation": "Proprietate în România și în Irlanda. Îngrijorată de cum se împarte.", "outcome": "Acord echitabil — proprietăți păstrate"}, {"slug": "george-limerick", "name": "George", "city": "Limerick", "gender": "m", "situation": "Divorț contestat. Soția solicita pensia lui irlandeză.", "outcome": "Pensia protejată parțial — acord negociat"}]},
        {"slug": "imigratie-irp", "title": "Probleme cu Viza sau IRP în Irlanda", "h1": "Probleme cu<em> viza sau IRP</em><br>în Irlanda.", "search_query": "viza refuzata irlanda ce fac roman", "law": "Immigration Act 2004 și reglementările UE — cetățenii UE au drepturi de ședere extinse în Irlanda.", "time_limit": "Contestă refuzul în termen de 15 zile lucrătoare", "practice_area": "immigration-law", "stories": [{"slug": "lucian-dublin", "name": "Lucian", "city": "Dublin", "gender": "m", "situation": "IRP expirat din cauza întârzierilor la programare. Angajatorul îi cerea documentul valid.", "outcome": "Statut regularizat — locul de muncă păstrat"}, {"slug": "gabriela-cork", "name": "Gabriela", "city": "Cork", "gender": "f", "situation": "Non-cetățean UE căsătorită cu român. Viza de reunificare refuzată.", "outcome": "Contestație acceptată — viză acordată"}, {"slug": "sorin-galway", "name": "Sorin", "city": "Galway", "gender": "m", "situation": "Ordin de deportare după o absență din Irlanda mai lungă decât permite regulamentul.", "outcome": "Ordin anulat — drept de ședere confirmat"}, {"slug": "raluca-limerick", "name": "Raluca", "city": "Limerick", "gender": "f", "situation": "Stamp 4 refuzat după 5 ani de reședință legală.", "outcome": "Stamp 4 acordat după contestație"}]},
        {"slug": "vatamari-corporale", "title": "Vătămare Corporală în Irlanda — Despăgubire", "h1": "Rănit<em> din vina altcuiva</em><br>în Irlanda.", "search_query": "am fost ranit la munca irlanda pot cere despagubire", "law": "Civil Liability Act — termenul de prescripție este 2 ani. Accidentele la locul de muncă sunt acoperite de Safety Health and Welfare at Work Act 2005.", "time_limit": "2 ani de la data accidentului — nu lăsa timpul să treacă", "practice_area": "personal-injury", "stories": [{"slug": "paul-dublin", "name": "Paul", "city": "Dublin", "gender": "m", "situation": "Accidentat la locul de muncă ridicând cutii grele fără antrenament. Angajatorul a spus că e normal.", "outcome": "Despăgubire — angajator găsit vinovat"}, {"slug": "natalia-cork", "name": "Natalia", "city": "Cork", "gender": "f", "situation": "Căzută pe un coridor ud în supermarket. Niciun semn de avertizare.", "outcome": "Despăgubire integrală inclusiv costuri medicale"}, {"slug": "alin-galway", "name": "Alin", "city": "Galway", "gender": "m", "situation": "Mâna prinsă în utilaj fără protecție de siguranță la fabrică.", "outcome": "Despăgubire semnificativă — vătămare permanentă"}, {"slug": "victoria-limerick", "name": "Victoria", "city": "Limerick", "gender": "f", "situation": "Agresată de un client la locul de muncă. Angajatorul nu avusese protocoale de siguranță.", "outcome": "Angajatorul găsit responsabil — despăgubire acordată"}]},
        {"slug": "accident-motocicleta-livrare", "title": "Accident cu Motocicleta sau la Livrare în Irlanda", "h1": "Accident<em> în timpul livrării</em><br>în Irlanda.", "search_query": "am lovit pe cineva cu masina in irlanda deliveroo amazon", "law": "Road Traffic Act și Civil Liability Act — curieri și șoferi de livrare au drepturi specifice în Irlanda.", "time_limit": "2 ani pentru reclamații civile — acționează cât mai curând", "practice_area": "personal-injury", "stories": [{"slug": "relu-dublin", "name": "Relu", "city": "Dublin", "gender": "m", "situation": "Curier pe motocicletă lovit de o mașină care a ignorat Stop. Angajatorul susținea că nu e responsabil.", "outcome": "Despăgubire — angajatorul și șoferul, ambii răspunzători"}, {"slug": "ionut-cork", "name": "Ionuț", "city": "Cork", "gender": "m", "situation": "Șofer de livrare Amazon — a lovit un pieton care a apărut brusc. Îngrijorat de dosarul penal.", "outcome": "Nicio urmărire penală — accident involuntar"}, {"slug": "madalina-galway", "name": "Mădălina", "city": "Galway", "gender": "f", "situation": "Șofer Uber Eats accidentat de o mașină. Compania a refuzat să plătească.", "outcome": "Despăgubire obținută din asigurarea obligatorie"}, {"slug": "silviu-limerick", "name": "Silviu", "city": "Limerick", "gender": "m", "situation": "Biciclist de livrare lovit de o ușă de mașină deschisă brusc.", "outcome": "Despăgubire integrală — proprietarul mașinii răspunzător"}]},
        {"slug": "permis-munca", "title": "Probleme cu Permisul de Muncă în Irlanda", "h1": "Probleme cu<em> permisul de muncă</em><br>în Irlanda.", "search_query": "permis de munca irlanda refuzat ce fac stamp 2 stamp 4", "law": "Employment Permits Act 2006 — angajatorii au obligații legale față de lucrătorii cu permis de muncă.", "time_limit": "Acționează imediat — permisele expirate sunt dificil de regularizat", "practice_area": "immigration-law", "stories": [{"slug": "costel-dublin", "name": "Costel", "city": "Dublin", "gender": "m", "situation": "Angajatorul a refuzat să sponsorizeze reînnoirea permisului de muncă după 2 ani.", "outcome": "Permis transferat la alt angajator — loc de muncă salvat"}, {"slug": "elena-cork", "name": "Elena", "city": "Cork", "gender": "f", "situation": "Stamp 2 expirat în timp ce schimba angajatorul. Se afla legal în Irlanda dar fără drept de muncă.", "outcome": "Statut regularizat — fără penalități"}, {"slug": "dorel-galway", "name": "Dorel", "city": "Galway", "gender": "m", "situation": "Angajatorul îi reținea pașaportul — o practică ilegală frecventă.", "outcome": "Pașaport returnat — angajator sancționat"}, {"slug": "corina-limerick", "name": "Corina", "city": "Limerick", "gender": "f", "situation": "Plătită sub salariul minim ca lucrătoare cu permis de muncă.", "outcome": "Salariile restante recuperate — angajator sancționat"}]},
        {"slug": "inselata-angajator-chirias", "title": "Înșelat de Angajator sau Proprietar în Irlanda", "h1": "<em>Înșelat</em> de angajator<br>sau proprietar în Irlanda.", "search_query": "angajatorul nu mi-a platit salariul irlanda ce fac", "law": "Payment of Wages Act 1991 și Residential Tenancies Act — există mecanisme legale clare pentru recuperarea banilor.", "time_limit": "6 ani pentru recuperarea salariilor restante — acționează înainte să expire", "practice_area": "employment-law", "stories": [{"slug": "petre-dublin", "name": "Petre", "city": "Dublin", "gender": "m", "situation": "Angajatorul nu i-a plătit ultimele 3 săptămâni de salariu când a demisionat.", "outcome": "Salarii recuperate integral prin WRC"}, {"slug": "adriana-cork", "name": "Adriana", "city": "Cork", "gender": "f", "situation": "Proprietarul a luat cauțiunea de €2,000 și a dispărut fără să returneze nimic.", "outcome": "Banii recuperați prin RTB și instanță"}, {"slug": "ciprian-galway", "name": "Ciprian", "city": "Galway", "gender": "m", "situation": "Angajat ca zilier — plătit cu €5/oră sub salariul minim legal.", "outcome": "Diferența recuperată — inspecție WRC declanșată"}, {"slug": "loredana-limerick", "name": "Loredana", "city": "Limerick", "gender": "f", "situation": "Agenție de recrutare a luat comision din salariu — practic ilegal în Irlanda.", "outcome": "Comisioane recuperate — agenție amendată"}]},
    ],
    "pt-br": [
        {"slug": "dirigindo-bebado", "title": "Preso Dirigindo Bêbado na Irlanda", "h1": "Preso <em>dirigindo bêbado</em><br>na Irlanda.", "search_query": "fui preso dirigindo bebado na irlanda o que fazer", "law": "Road Traffic Act 2010 — limite legal é 50mg/100ml de sangue. Suspensão automática da carteira.", "time_limit": "Aja imediatamente após receber a citação judicial", "practice_area": "criminal-law", "stories": [{"slug": "carlos-dublin", "name": "Carlos", "city": "Dublin", "gender": "m", "situation": "Parado numa blitz de rotina com 62mg — pouco acima do limite. Risco de perder a carteira e o emprego.", "outcome": "Acusação rejeitada — carteira mantida"}, {"slug": "ana-cork", "name": "Ana", "city": "Cork", "gender": "f", "situation": "Parada após um acidente menor. Primeira infração. Preocupada com o emprego na área da saúde.", "outcome": "Suspensão reduzida ao mínimo legal"}, {"slug": "rodrigo-galway", "name": "Rodrigo", "city": "Galway", "gender": "m", "situation": "Nível alto de álcool. Achava que não tinha saída. O advogado identificou um vício processual.", "outcome": "Processo arquivado — vício processual"}, {"slug": "patricia-limerick", "name": "Patrícia", "city": "Limerick", "gender": "f", "situation": "Enfermeira. Uma condenação destruiria sua carreira profissional.", "outcome": "Licença profissional protegida"}]},
        {"slug": "sem-seguro", "title": "Preso Sem Seguro na Irlanda", "h1": "Preso dirigindo<br><em>sem seguro</em> na Irlanda.", "search_query": "preso sem seguro carro irlanda o que acontece", "law": "Road Traffic Act — dirigir sem seguro é crime. Multa obrigatória e possível suspensão.", "time_limit": "Contate um advogado antes da data do tribunal", "practice_area": "criminal-law", "stories": [{"slug": "marcos-dublin", "name": "Marcos", "city": "Dublin", "gender": "m", "situation": "Dirigia o carro da namorada sem saber que não estava coberto como condutor adicional.", "outcome": "Multa reduzida — sem suspensão"}, {"slug": "juliana-cork", "name": "Juliana", "city": "Cork", "gender": "f", "situation": "Seguro vencido há dois dias. Não recebeu nenhum aviso.", "outcome": "Processo arquivado — circunstâncias atenuantes"}, {"slug": "fabio-galway", "name": "Fábio", "city": "Galway", "gender": "m", "situation": "Carro segurado pela empresa. A empresa esqueceu de renovar a apólice.", "outcome": "Empresa assumiu responsabilidade"}, {"slug": "renata-limerick", "name": "Renata", "city": "Limerick", "gender": "f", "situation": "Seguro comprado online mas não ativado corretamente.", "outcome": "Penalidade fixa — sem ficha criminal"}]},
        {"slug": "sem-carteira", "title": "Preso Sem Carteira na Irlanda", "h1": "Preso dirigindo<br><em>sem carteira</em> na Irlanda.", "search_query": "fui parado sem carteira de motorista irlanda", "law": "Road Traffic Act — dirigir sem carteira válida é crime. Carteira brasileira tem validade limitada na Irlanda.", "time_limit": "Aja antes da data do tribunal", "practice_area": "criminal-law", "stories": [{"slug": "eduardo-dublin", "name": "Eduardo", "city": "Dublin", "gender": "m", "situation": "Carteira brasileira vencida. Não sabia que precisava trocar pela carteira irlandesa.", "outcome": "Multa reduzida — circunstâncias atenuantes"}, {"slug": "camila-cork", "name": "Camila", "city": "Cork", "gender": "f", "situation": "Carteira provisória. Dirigia sozinha — achava que era permitido.", "outcome": "Penalidade mínima — primeira infração"}, {"slug": "thiago-galway", "name": "Thiago", "city": "Galway", "gender": "m", "situation": "Carteira suspensa por infração anterior. Não sabia que a suspensão ainda estava ativa.", "outcome": "Negociação — suspensão reduzida"}, {"slug": "fernanda-limerick", "name": "Fernanda", "city": "Limerick", "gender": "f", "situation": "Carteira de outro país fora da UE — não reconhecida automaticamente na Irlanda.", "outcome": "Processo retirado após regularização"}]},
        {"slug": "acidente-carro", "title": "Acidente de Carro com Lesão na Irlanda", "h1": "Acidente de carro.<br><em>Você tem direito à indenização.</em>", "search_query": "tive acidente de carro na irlanda tenho direito a indenizacao", "law": "Civil Liability Act — prazo de 2 anos a partir da data do acidente.", "time_limit": "2 anos do acidente — aja o quanto antes", "practice_area": "personal-injury", "stories": [{"slug": "rafael-dublin", "name": "Rafael", "city": "Dublin", "gender": "m", "situation": "Batido por trás na autoestrada. Seguro do outro motorista ofereceu €8,000. Advogado obteve muito mais.", "outcome": "Indenização de €32,000"}, {"slug": "paula-cork", "name": "Paula", "city": "Cork", "gender": "f", "situation": "Passageira no carro de um amigo que causou o acidente. Não sabia que podia reivindicar.", "outcome": "Indenização total concedida"}, {"slug": "lucas-galway", "name": "Lucas", "city": "Galway", "gender": "m", "situation": "Pedestre atropelado na faixa. Motorista negou responsabilidade.", "outcome": "Responsabilidade estabelecida — indenização concedida"}, {"slug": "aline-limerick", "name": "Aline", "city": "Limerick", "gender": "f", "situation": "Acidente no trabalho — atropelada por uma van no armazém.", "outcome": "Indenização inclui perda de salários"}]},
        {"slug": "demissao-injusta", "title": "Demissão Injusta na Irlanda", "h1": "Demitido<em> sem motivo justo</em><br>na Irlanda.", "search_query": "fui demitido injustamente na irlanda o que fazer", "law": "Unfair Dismissals Act 1977 — você tem direito de reclamar no WRC dentro de 6 meses.", "time_limit": "6 meses da demissão — não perca o prazo", "practice_area": "employment-law", "stories": [{"slug": "joao-dublin", "name": "João", "city": "Dublin", "gender": "m", "situation": "Demitido após 5 anos sem avisos ou processo disciplinar. Empresa disse que era reestruturação.", "outcome": "WRC decidiu a favor — compensação concedida"}, {"slug": "mariana-cork", "name": "Mariana", "city": "Cork", "gender": "f", "situation": "Demitida logo após anunciar a gravidez. Empresa inventou outros motivos.", "outcome": "Discriminação confirmada — compensação máxima"}, {"slug": "gustavo-galway", "name": "Gustavo", "city": "Galway", "gender": "m", "situation": "Dispensado após denunciar condições inseguras. Sem aviso prévio.", "outcome": "Demissão retaliatória — compensação adicional"}, {"slug": "bianca-limerick", "name": "Bianca", "city": "Limerick", "gender": "f", "situation": "Cargo eliminado mas colega mais jovem assumiu as mesmas funções.", "outcome": "Reestruturação falsa comprovada — compensação concedida"}]},
        {"slug": "problemas-senhorio", "title": "Problemas com Senhorio na Irlanda", "h1": "O senhorio<em> está violando seus direitos.</em><br>Veja o que fazer.", "search_query": "senhorio quer me despejar ilegalmente irlanda direitos inquilino", "law": "Residential Tenancies Act — inquilinos têm direitos legais fortes. RTB medeia disputas.", "time_limit": "Registre reclamação no RTB dentro de 28 dias do incidente", "practice_area": "property-law", "stories": [{"slug": "wellington-dublin", "name": "Wellington", "city": "Dublin", "gender": "m", "situation": "Senhorio deu 30 dias para sair em janeiro. 3 anos de aluguel sempre em dia.", "outcome": "Despejo bloqueado — pode continuar morando"}, {"slug": "priscila-cork", "name": "Priscila", "city": "Cork", "gender": "f", "situation": "Senhorio ficou com todo o depósito alegando danos inexistentes.", "outcome": "Depósito devolvido integralmente"}, {"slug": "anderson-galway", "name": "Anderson", "city": "Galway", "gender": "m", "situation": "Aluguel aumentado 25% sem aviso adequado.", "outcome": "Aumento anulado — aluguel anterior mantido"}, {"slug": "tatiane-limerick", "name": "Tatiane", "city": "Limerick", "gender": "f", "situation": "Senhorio entrava no apartamento sem permissão várias vezes.", "outcome": "RTB emitiu ordem de respeito aos direitos"}]},
        {"slug": "divorcio-irlanda", "title": "Divórcio na Irlanda — Guia para Brasileiros", "h1": "Divórcio<em> na Irlanda.</em><br>O que você precisa saber.", "search_query": "como fazer divorcio na irlanda brasileiro", "law": "Family Law Act — divórcio na Irlanda exige separação de pelo menos 2 anos dos últimos 3.", "time_limit": "Não há prazo — mas aja rápido para proteger seus bens", "practice_area": "family-law", "stories": [{"slug": "beatriz-dublin", "name": "Beatriz", "city": "Dublin", "gender": "f", "situation": "Casada por 10 anos. Queria divórcio mas não sabia se seria reconhecido no Brasil.", "outcome": "Divórcio finalizado — reconhecido internacionalmente"}, {"slug": "roberto-cork", "name": "Roberto", "city": "Cork", "gender": "m", "situation": "Esposa voltou para o Brasil com os filhos. Não sabia quais eram seus direitos.", "outcome": "Acordo de custódia estabelecido pelo tribunal"}, {"slug": "claudia-galway", "name": "Cláudia", "city": "Galway", "gender": "f", "situation": "Imóvel no Brasil e na Irlanda. Preocupada com a divisão.", "outcome": "Acordo justo — imóveis mantidos"}, {"slug": "sergio-limerick", "name": "Sérgio", "city": "Limerick", "gender": "m", "situation": "Divórcio contestado. Esposa reivindicava sua pensão irlandesa.", "outcome": "Pensão parcialmente protegida — acordo negociado"}]},
        {"slug": "visto-imigracao", "title": "Problemas com Visto ou Imigração na Irlanda", "h1": "Problemas com<em> visto ou imigração</em><br>na Irlanda.", "search_query": "visto recusado irlanda o que fazer brasileiro", "law": "Immigration Act 2004 — cidadãos não-UE têm direito de apelar de recusas de visto.", "time_limit": "Apele a recusa dentro de 15 dias úteis", "practice_area": "immigration-law", "stories": [{"slug": "leandro-dublin", "name": "Leandro", "city": "Dublin", "gender": "m", "situation": "IRP vencido por causa de atrasos no agendamento. Empregador exigia documento válido.", "outcome": "Status regularizado — emprego mantido"}, {"slug": "vanessa-cork", "name": "Vanessa", "city": "Cork", "gender": "f", "situation": "Não-cidadã da UE casada com brasileiro. Visto de reagrupamento familiar recusado.", "outcome": "Recurso aceito — visto concedido"}, {"slug": "diego-galway", "name": "Diego", "city": "Galway", "gender": "m", "situation": "Ordem de deportação após ausência longa da Irlanda.", "outcome": "Ordem anulada — direito de residência confirmado"}, {"slug": "natalia-limerick", "name": "Natália", "city": "Limerick", "gender": "f", "situation": "Stamp 4 recusado após 5 anos de residência legal.", "outcome": "Stamp 4 concedido após recurso"}]},
        {"slug": "lesao-trabalho", "title": "Lesão no Trabalho na Irlanda — Indenização", "h1": "Lesionado<em> por culpa de outro</em><br>na Irlanda.", "search_query": "sofri acidente no trabalho irlanda posso pedir indenizacao", "law": "Safety Health and Welfare at Work Act 2005 — empregadores têm obrigação legal de segurança. Prazo: 2 anos.", "time_limit": "2 anos do acidente — não deixe o tempo passar", "practice_area": "personal-injury", "stories": [{"slug": "antonio-dublin", "name": "Antônio", "city": "Dublin", "gender": "m", "situation": "Acidentado no trabalho carregando caixas pesadas sem treinamento. Patrão disse que era normal.", "outcome": "Indenização — empregador responsabilizado"}, {"slug": "jessica-cork", "name": "Jéssica", "city": "Cork", "gender": "f", "situation": "Caiu em corredor molhado em supermercado. Nenhum sinal de aviso.", "outcome": "Indenização total incluindo custos médicos"}, {"slug": "thiago2-galway", "name": "Thiago", "city": "Galway", "gender": "m", "situation": "Mão presa em máquina sem proteção de segurança na fábrica.", "outcome": "Indenização significativa — lesão permanente"}, {"slug": "larissa-limerick", "name": "Larissa", "city": "Limerick", "gender": "f", "situation": "Agredida por cliente no trabalho. Empresa não tinha protocolos de segurança.", "outcome": "Empregador responsabilizado — indenização concedida"}]},
        {"slug": "acidente-moto-entrega", "title": "Acidente de Moto ou Entrega na Irlanda", "h1": "Acidente<em> durante entrega</em><br>na Irlanda.", "search_query": "bati com moto fazendo entrega irlanda uber eats deliveroo", "law": "Road Traffic Act e Civil Liability Act — entregadores têm direitos específicos na Irlanda.", "time_limit": "2 anos para reclamações civis — aja o quanto antes", "practice_area": "personal-injury", "stories": [{"slug": "evandro-dublin", "name": "Evandro", "city": "Dublin", "gender": "m", "situation": "Entregador de moto atropelado por carro que ignorou Pare. Empresa dizia não ser responsável.", "outcome": "Indenização — empresa e motorista responsabilizados"}, {"slug": "vitor-cork", "name": "Vítor", "city": "Cork", "gender": "m", "situation": "Motorista de entrega Amazon atropelou pedestre que apareceu de repente. Preocupado com processo criminal.", "outcome": "Sem processo criminal — acidente involuntário"}, {"slug": "vanessa2-galway", "name": "Vanessa", "city": "Galway", "gender": "f", "situation": "Motorista Uber Eats atropelada por carro. Empresa recusou pagar.", "outcome": "Indenização obtida do seguro obrigatório"}, {"slug": "rogerio-limerick", "name": "Rogério", "city": "Limerick", "gender": "m", "situation": "Ciclista de entrega atingido por porta de carro aberta de repente.", "outcome": "Indenização total — proprietário do carro responsável"}]},
        {"slug": "permissao-trabalho", "title": "Problemas com Permissão de Trabalho na Irlanda", "h1": "Problemas com<em> permissão de trabalho</em><br>na Irlanda.", "search_query": "permissao de trabalho irlanda recusada o que fazer stamp 2", "law": "Employment Permits Act 2006 — empregadores têm obrigações legais para trabalhadores com permissão.", "time_limit": "Aja imediatamente — permissões vencidas são difíceis de regularizar", "practice_area": "immigration-law", "stories": [{"slug": "marcelo-dublin", "name": "Marcelo", "city": "Dublin", "gender": "m", "situation": "Empregador recusou patrocinar renovação da permissão após 2 anos.", "outcome": "Permissão transferida para outro empregador — emprego salvo"}, {"slug": "simone-cork", "name": "Simone", "city": "Cork", "gender": "f", "situation": "Stamp 2 vencido enquanto trocava de empregador.", "outcome": "Status regularizado — sem penalidades"}, {"slug": "alex-galway", "name": "Alex", "city": "Galway", "gender": "m", "situation": "Empregador retinha o passaporte — prática ilegal comum.", "outcome": "Passaporte devolvido — empregador sancionado"}, {"slug": "monica-limerick", "name": "Mônica", "city": "Limerick", "gender": "f", "situation": "Paga abaixo do salário mínimo como trabalhadora com permissão.", "outcome": "Salários atrasados recuperados — empregador sancionado"}]},
        {"slug": "golpe-empregador-senhorio", "title": "Enganado por Empregador ou Senhorio na Irlanda", "h1": "<em>Enganado</em> por empregador<br>ou senhorio na Irlanda.", "search_query": "empregador nao pagou salario irlanda o que fazer", "law": "Payment of Wages Act 1991 — mecanismos legais claros para recuperação de salários.", "time_limit": "6 anos para recuperação de salários — aja antes do prazo", "practice_area": "employment-law", "stories": [{"slug": "samuel-dublin", "name": "Samuel", "city": "Dublin", "gender": "m", "situation": "Empregador não pagou as últimas 3 semanas quando ele pediu demissão.", "outcome": "Salários recuperados integralmente via WRC"}, {"slug": "isabela-cork", "name": "Isabela", "city": "Cork", "gender": "f", "situation": "Senhorio ficou com depósito de €2,000 e sumiu.", "outcome": "Dinheiro recuperado via RTB e tribunal"}, {"slug": "igor-galway", "name": "Igor", "city": "Galway", "gender": "m", "situation": "Contratado como diarista — pago €5/hora abaixo do mínimo legal.", "outcome": "Diferença recuperada — inspeção WRC acionada"}, {"slug": "rebeka-limerick", "name": "Rebeka", "city": "Limerick", "gender": "f", "situation": "Agência de recrutamento descontava comissão do salário — ilegal na Irlanda.", "outcome": "Comissões recuperadas — agência multada"}]},
    ],
}

TOPICS.update({
    "pl": [
        {"slug": "jazda-po-alkoholu", "title": "Zatrzymany za Jazdę po Alkoholu w Irlandii", "h1": "Zatrzymany <em>za jazdę po alkoholu</em><br>w Irlandii.", "search_query": "zatrzymany za jazdę po alkoholu irlandia co robić", "law": "Road Traffic Act 2010 — limit prawny to 50mg/100ml krwi. Automatyczne zawieszenie prawa jazdy.", "time_limit": "Działaj natychmiast po otrzymaniu wezwania do sądu", "practice_area": "criminal-law", "stories": [{"slug": "marek-dublin", "name": "Marek", "city": "Dublin", "gender": "m", "situation": "Zatrzymany na rutynowej kontroli z 58mg — nieznacznie powyżej limitu. Ryzyko utraty prawa jazdy i pracy.", "outcome": "Zarzut oddalony — prawo jazdy zachowane"}, {"slug": "anna-cork", "name": "Anna", "city": "Cork", "gender": "f", "situation": "Zatrzymana po drobnej kolizji. Pierwsze wykroczenie. Obawy o pracę w służbie zdrowia.", "outcome": "Zawieszenie skrócone do ustawowego minimum"}, {"slug": "piotr-galway", "name": "Piotr", "city": "Galway", "gender": "m", "situation": "Wysoki poziom alkoholu. Myślał, że nie ma szans. Prawnik wykrył błąd proceduralny.", "outcome": "Sprawa oddalona — błąd proceduralny"}, {"slug": "katarzyna-limerick", "name": "Katarzyna", "city": "Limerick", "gender": "f", "situation": "Pielęgniarka. Skazanie zniszczyłoby jej licencję zawodową.", "outcome": "Licencja zawodowa ochroniona"}]},
        {"slug": "bez-ubezpieczenia", "title": "Zatrzymany bez Ubezpieczenia w Irlandii", "h1": "Zatrzymany bez<br><em>ubezpieczenia</em> w Irlandii.", "search_query": "zatrzymany bez ubezpieczenia samochód irlandia", "law": "Road Traffic Act — jazda bez ubezpieczenia to przestępstwo karne. Obowiązkowa grzywna i możliwe zawieszenie.", "time_limit": "Skontaktuj się z prawnikiem przed datą rozprawy", "practice_area": "criminal-law", "stories": [{"slug": "tomasz-dublin", "name": "Tomasz", "city": "Dublin", "gender": "m", "situation": "Prowadził samochód partnerki nie wiedząc, że nie jest ubezpieczony jako dodatkowy kierowca.", "outcome": "Grzywna obniżona — bez zawieszenia"}, {"slug": "monika-cork", "name": "Monika", "city": "Cork", "gender": "f", "situation": "Ubezpieczenie wygasło dwa dni wcześniej. Nie otrzymała żadnego powiadomienia.", "outcome": "Sprawa umorzona — okoliczności łagodzące"}, {"slug": "krzysztof-galway", "name": "Krzysztof", "city": "Galway", "gender": "m", "situation": "Samochód ubezpieczony przez pracodawcę. Pracodawca zapomniał odnowić polisę.", "outcome": "Pracodawca przejął odpowiedzialność"}, {"slug": "agnieszka-limerick", "name": "Agnieszka", "city": "Limerick", "gender": "f", "situation": "Ubezpieczenie kupione online ale nieprawidłowo aktywowane.", "outcome": "Stała kara — bez rejestru karnego"}]},
        {"slug": "bez-prawa-jazdy", "title": "Zatrzymany bez Prawa Jazdy w Irlandii", "h1": "Zatrzymany bez<br><em>prawa jazdy</em> w Irlandii.", "search_query": "zatrzymany bez prawa jazdy irlandia co robić", "law": "Road Traffic Act — jazda bez ważnego prawa jazdy to przestępstwo. Polskie prawo jazdy ma ograniczoną ważność w Irlandii.", "time_limit": "Działaj przed datą rozprawy", "practice_area": "criminal-law", "stories": [{"slug": "rafal-dublin", "name": "Rafał", "city": "Dublin", "gender": "m", "situation": "Polskie prawo jazdy wygasło. Nie wiedział, że musi je wymienić na irlandzkie.", "outcome": "Grzywna obniżona — okoliczności łagodzące"}, {"slug": "magdalena-cork", "name": "Magdalena", "city": "Cork", "gender": "f", "situation": "Prawo jazdy tymczasowe. Prowadziła sama — myślała, że jest dozwolone.", "outcome": "Minimalna kara — pierwsze wykroczenie"}, {"slug": "wojciech-galway", "name": "Wojciech", "city": "Galway", "gender": "m", "situation": "Prawo jazdy zawieszone za wcześniejsze wykroczenie. Nie wiedział, że zawieszenie nadal obowiązuje.", "outcome": "Negocjacje — zawieszenie skrócone"}, {"slug": "beata-limerick", "name": "Beata", "city": "Limerick", "gender": "f", "situation": "Prawo jazdy spoza UE — nieautomatycznie uznawane w Irlandii.", "outcome": "Sprawa wycofana po uregulowaniu statusu"}]},
        {"slug": "wypadek-samochodowy", "title": "Wypadek Samochodowy z Obrażeniami w Irlandii", "h1": "Wypadek samochodowy.<br><em>Masz prawo do odszkodowania.</em>", "search_query": "wypadek samochodowy irlandia odszkodowanie", "law": "Civil Liability Act — termin przedawnienia wynosi 2 lata od daty wypadku.", "time_limit": "2 lata od wypadku — działaj jak najszybciej", "practice_area": "personal-injury", "stories": [{"slug": "damian-dublin", "name": "Damian", "city": "Dublin", "gender": "m", "situation": "Uderzony od tyłu na autostradzie. Ubezpieczyciel drugiego kierowcy zaproponował €8,000. Prawnik uzyskał znacznie więcej.", "outcome": "Odszkodowanie €31,000"}, {"slug": "joanna-cork", "name": "Joanna", "city": "Cork", "gender": "f", "situation": "Pasażerka w samochodzie przyjaciela, który spowodował wypadek. Nie wiedziała, że może dochodzić roszczeń.", "outcome": "Pełne odszkodowanie przyznane"}, {"slug": "lukasz-galway", "name": "Łukasz", "city": "Galway", "gender": "m", "situation": "Pieszy potrącony na przejściu. Kierowca początkowo zaprzeczył odpowiedzialności.", "outcome": "Ustalono odpowiedzialność — odszkodowanie przyznane"}, {"slug": "ewelina-limerick", "name": "Ewelina", "city": "Limerick", "gender": "f", "situation": "Wypadek w pracy — potrącona przez furgonetkę w magazynie.", "outcome": "Odszkodowanie obejmuje utracone zarobki"}]},
        {"slug": "niesprawiedliwe-zwolnienie", "title": "Niesprawiedliwe Zwolnienie z Pracy w Irlandii", "h1": "Zwolniony<em> bez uzasadnionego powodu</em><br>w Irlandii.", "search_query": "niesprawiedliwe zwolnienie z pracy irlandia prawa", "law": "Unfair Dismissals Act 1977 — masz prawo złożyć skargę do WRC w ciągu 6 miesięcy.", "time_limit": "6 miesięcy od zwolnienia — nie przegap terminu", "practice_area": "employment-law", "stories": [{"slug": "michal-dublin", "name": "Michał", "city": "Dublin", "gender": "m", "situation": "Zwolniony po 5 latach bez ostrzeżeń ani postępowania dyscyplinarnego. Pracodawca powołał się na restrukturyzację.", "outcome": "WRC orzekł na korzyść — odszkodowanie przyznane"}, {"slug": "natalia-cork", "name": "Natalia", "city": "Cork", "gender": "f", "situation": "Zwolniona wkrótce po ogłoszeniu ciąży. Pracodawca podał inne powody.", "outcome": "Dyskryminacja potwierdzona — maksymalne odszkodowanie"}, {"slug": "bartosz-galway", "name": "Bartosz", "city": "Galway", "gender": "m", "situation": "Zwolniony po zgłoszeniu niebezpiecznych warunków pracy. Bez ostrzeżenia.", "outcome": "Zwolnienie odwetowe — dodatkowe odszkodowanie"}, {"slug": "aleksandra-limerick", "name": "Aleksandra", "city": "Limerick", "gender": "f", "situation": "Stanowisko zlikwidowane, ale młodsza koleżanka przejęła te same obowiązki.", "outcome": "Fałszywa restrukturyzacja udowodniona — odszkodowanie"}]},
        {"slug": "problemy-z-wynajmem", "title": "Problemy z Właścicielem Mieszkania w Irlandii", "h1": "Właściciel<em> narusza Twoje prawa.</em><br>Oto co możesz zrobić.", "search_query": "właściciel chce mnie eksmitować nielegalnie irlandia prawa najemcy", "law": "Residential Tenancies Act — najemcy mają silne prawa prawne. RTB rozpatruje spory.", "time_limit": "Złóż skargę do RTB w ciągu 28 dni od incydentu", "practice_area": "property-law", "stories": [{"slug": "grzegorz-dublin", "name": "Grzegorz", "city": "Dublin", "gender": "m", "situation": "Właściciel dał 30 dni na wyprowadzkę w styczniu. 3 lata terminowych płatności.", "outcome": "Eksmisja zablokowana — może pozostać"}, {"slug": "izabela-cork", "name": "Izabela", "city": "Cork", "gender": "f", "situation": "Właściciel zatrzymał cały kaucję powołując się na nieistniejące szkody.", "outcome": "Kaucja zwrócona w całości"}, {"slug": "przemyslaw-galway", "name": "Przemysław", "city": "Galway", "gender": "m", "situation": "Czynsz podwyższony o 25% bez odpowiedniego powiadomienia.", "outcome": "Podwyżka anulowana — poprzedni czynsz utrzymany"}, {"slug": "sylwia-limerick", "name": "Sylwia", "city": "Limerick", "gender": "f", "situation": "Właściciel wielokrotnie wchodził do mieszkania bez pozwolenia.", "outcome": "RTB wydało nakaz przestrzegania praw"}]},
        {"slug": "rozwod-w-irlandii", "title": "Rozwód w Irlandii — Przewodnik dla Polaków", "h1": "Rozwód<em> w Irlandii.</em><br>Co musisz wiedzieć.", "search_query": "jak zrobić rozwód w irlandii polak", "law": "Family Law Act — rozwód w Irlandii wymaga separacji przez co najmniej 2 lata z ostatnich 3.", "time_limit": "Brak terminu — ale działaj szybko, by chronić majątek", "practice_area": "family-law", "stories": [{"slug": "dorota-dublin", "name": "Dorota", "city": "Dublin", "gender": "f", "situation": "Zamężna od 10 lat. Chciała rozwodu, ale nie wiedziała, czy będzie uznany w Polsce.", "outcome": "Rozwód sfinalizowany — uznany w UE"}, {"slug": "slawomir-cork", "name": "Sławomir", "city": "Cork", "gender": "m", "situation": "Żona wyjechała do Polski z dziećmi. Nie wiedział, jakie ma prawa.", "outcome": "Porozumienie o opiece ustalone przez sąd"}, {"slug": "malgorzata-galway", "name": "Małgorzata", "city": "Galway", "gender": "f", "situation": "Nieruchomości w Polsce i Irlandii. Obawy o podział majątku.", "outcome": "Sprawiedliwe porozumienie — majątek zachowany"}, {"slug": "zbigniew-limerick", "name": "Zbigniew", "city": "Limerick", "gender": "m", "situation": "Sporny rozwód. Żona domagała się irlandzkiej emerytury.", "outcome": "Emerytura częściowo chroniona — porozumienie wynegocjowane"}]},
        {"slug": "problemy-wizowe", "title": "Problemy z Wizą lub Imigracją w Irlandii", "h1": "Problemy z<em> wizą lub imigracją</em><br>w Irlandii.", "search_query": "wiza odmowa irlandia co robić polak", "law": "Immigration Act 2004 oraz przepisy UE — obywatele UE mają rozszerzone prawa pobytu w Irlandii.", "time_limit": "Odwołaj się od odmowy w ciągu 15 dni roboczych", "practice_area": "immigration-law", "stories": [{"slug": "janusz-dublin", "name": "Janusz", "city": "Dublin", "gender": "m", "situation": "IRP wygasło z powodu opóźnień w rejestracji. Pracodawca wymagał ważnego dokumentu.", "outcome": "Status uregulowany — praca zachowana"}, {"slug": "marta-cork", "name": "Marta", "city": "Cork", "gender": "f", "situation": "Obywatelka spoza UE zamężna z Polakiem. Wiza łączenia rodzin odmówiona.", "outcome": "Odwołanie przyjęte — wiza przyznana"}, {"slug": "andrzej-galway", "name": "Andrzej", "city": "Galway", "gender": "m", "situation": "Nakaz deportacji po zbyt długiej nieobecności w Irlandii.", "outcome": "Nakaz uchylony — prawo pobytu potwierdzone"}, {"slug": "zofia-limerick", "name": "Zofia", "city": "Limerick", "gender": "f", "situation": "Stamp 4 odmówiony po 5 latach legalnego pobytu.", "outcome": "Stamp 4 przyznany po odwołaniu"}]},
        {"slug": "obra-zenia-ciala", "title": "Obrażenia Ciała w Irlandii — Odszkodowanie", "h1": "Ranny<em> z czyjejś winy</em><br>w Irlandii.", "search_query": "wypadek w pracy irlandia odszkodowanie", "law": "Civil Liability Act — termin przedawnienia 2 lata. Wypadki w pracy objęte Safety Health and Welfare at Work Act 2005.", "time_limit": "2 lata od wypadku — nie pozwól, by czas minął", "practice_area": "personal-injury", "stories": [{"slug": "dariusz-dublin", "name": "Dariusz", "city": "Dublin", "gender": "m", "situation": "Wypadek w pracy przy podnoszeniu ciężkich skrzynek bez szkolenia. Pracodawca twierdził, że to normalne.", "outcome": "Odszkodowanie — pracodawca uznany winnym"}, {"slug": "renata-cork", "name": "Renata", "city": "Cork", "gender": "f", "situation": "Upadek na mokrym korytarzu w supermarkecie. Brak znaków ostrzegawczych.", "outcome": "Pełne odszkodowanie łącznie z kosztami leczenia"}, {"slug": "pawel-galway", "name": "Paweł", "city": "Galway", "gender": "m", "situation": "Ręka wciągnięta w maszynę bez osłony bezpieczeństwa w fabryce.", "outcome": "Znaczące odszkodowanie — trwały uszczerbek"}, {"slug": "kinga-limerick", "name": "Kinga", "city": "Limerick", "gender": "f", "situation": "Napadnięta przez klienta w miejscu pracy. Pracodawca nie miał protokołów bezpieczeństwa.", "outcome": "Pracodawca uznany odpowiedzialnym — odszkodowanie"}]},
        {"slug": "nieuczciwy-pracodawca", "title": "Nieuczciwy Pracodawca lub Właściciel w Irlandii", "h1": "<em>Oszukany</em> przez pracodawcę<br>lub właściciela w Irlandii.", "search_query": "pracodawca nie zapłacił wynagrodzenia irlandia co robić", "law": "Payment of Wages Act 1991 — jasne mechanizmy prawne odzyskiwania zaległych wynagrodzeń.", "time_limit": "6 lat na odzyskanie zaległych wynagrodzeń — działaj przed terminem", "practice_area": "employment-law", "stories": [{"slug": "roman-dublin", "name": "Roman", "city": "Dublin", "gender": "m", "situation": "Pracodawca nie wypłacił ostatnich 3 tygodni wynagrodzenia po rezygnacji.", "outcome": "Wynagrodzenia odzyskane w całości przez WRC"}, {"slug": "elzbieta-cork", "name": "Elżbieta", "city": "Cork", "gender": "f", "situation": "Właściciel zabrał kaucję €2,000 i zniknął.", "outcome": "Pieniądze odzyskane przez RTB i sąd"}, {"slug": "szymon-galway", "name": "Szymon", "city": "Galway", "gender": "m", "situation": "Zatrudniony jako pracownik dzienny — płacony €5/godz. poniżej ustawowego minimum.", "outcome": "Różnica odzyskana — inspekcja WRC wszczęta"}, {"slug": "wioleta-limerick", "name": "Wioleta", "city": "Limerick", "gender": "f", "situation": "Agencja rekrutacyjna potrącała prowizję z wynagrodzenia — nielegalne w Irlandii.", "outcome": "Prowizje odzyskane — agencja ukarana"}]},
    ],
    "ar": [
        {"slug": "qiyadah-sukr", "title": "القبض عليك بتهمة القيادة تحت تأثير الكحول في أيرلندا", "h1": "القبض عليك <em>بتهمة القيادة<br>تحت تأثير الكحول</em> في أيرلندا.", "search_query": "قبض علي بسبب قيادة تحت تأثير الكحول في ايرلندا", "law": "قانون حركة المرور 2010 — الحد القانوني 50 ملغ/100 مل من الدم. تعليق تلقائي لرخصة القيادة.", "time_limit": "تصرف فوراً بعد استلام الاستدعاء للمحكمة", "practice_area": "criminal-law", "stories": [{"slug": "ahmad-dublin", "name": "أحمد", "city": "Dublin", "gender": "m", "situation": "أوقف في نقطة تفتيش روتينية بنسبة 58 ملغ — أعلى بقليل من الحد. خطر فقدان رخصة القيادة والعمل.", "outcome": "تمت تبرئته — احتفظ برخصة القيادة"}, {"slug": "fatima-cork", "name": "فاطمة", "city": "Cork", "gender": "f", "situation": "أوقفت بعد حادث بسيط. المخالفة الأولى. قلقة على عملها في مجال الصحة.", "outcome": "تقليص فترة التعليق إلى الحد الأدنى القانوني"}, {"slug": "omar-galway", "name": "عمر", "city": "Galway", "gender": "m", "situation": "نسبة كحول مرتفعة. اعتقد أنه لا أمل. اكتشف المحامي خللاً إجرائياً.", "outcome": "إسقاط القضية — خلل إجرائي"}, {"slug": "maryam-limerick", "name": "مريم", "city": "Limerick", "gender": "f", "situation": "ممرضة. الإدانة ستدمر مسيرتها المهنية.", "outcome": "حماية الترخيص المهني"}]},
        {"slug": "bila-tamin", "title": "القبض عليك بدون تأمين في أيرلندا", "h1": "القبض عليك بدون<br><em>تأمين</em> في أيرلندا.", "search_query": "قبض علي بدون تأمين سيارة في ايرلندا", "law": "قانون حركة المرور — القيادة بدون تأمين جريمة جنائية. غرامة إلزامية وتعليق محتمل.", "time_limit": "اتصل بمحامٍ قبل تاريخ المحكمة", "practice_area": "criminal-law", "stories": [{"slug": "khalid-dublin", "name": "خالد", "city": "Dublin", "gender": "m", "situation": "كان يقود سيارة زوجته دون أن يعلم أنه غير مؤمن عليها كسائق إضافي.", "outcome": "تخفيض الغرامة — بدون تعليق"}, {"slug": "nora-cork", "name": "نورا", "city": "Cork", "gender": "f", "situation": "انتهى التأمين قبل يومين. لم تتلقَ أي إشعار.", "outcome": "إسقاط القضية — ظروف مخففة"}, {"slug": "hassan-galway", "name": "حسن", "city": "Galway", "gender": "m", "situation": "السيارة مؤمنة من قبل صاحب العمل. نسي صاحب العمل تجديد الوثيقة.", "outcome": "صاحب العمل تحمّل المسؤولية"}, {"slug": "leila-limerick", "name": "ليلى", "city": "Limerick", "gender": "f", "situation": "تأمين مشترى عبر الإنترنت لم يُفعَّل بشكل صحيح.", "outcome": "غرامة ثابتة — بدون سجل جنائي"}]},
        {"slug": "bila-rukhsa", "title": "القبض عليك بدون رخصة قيادة في أيرلندا", "h1": "القبض عليك بدون<br><em>رخصة قيادة</em> في أيرلندا.", "search_query": "قبض علي بدون رخصة قيادة في ايرلندا", "law": "قانون حركة المرور — القيادة بدون رخصة سارية جريمة. رخصة القيادة العربية لها صلاحية محدودة في أيرلندا.", "time_limit": "تصرف قبل تاريخ المحكمة", "practice_area": "criminal-law", "stories": [{"slug": "ibrahim-dublin", "name": "إبراهيم", "city": "Dublin", "gender": "m", "situation": "رخصة القيادة منتهية. لم يعلم أنه بحاجة لاستبدالها برخصة أيرلندية.", "outcome": "تخفيض الغرامة — ظروف مخففة"}, {"slug": "sara-cork", "name": "سارة", "city": "Cork", "gender": "f", "situation": "رخصة مؤقتة. كانت تقود وحدها معتقدةً أنه مسموح.", "outcome": "عقوبة بسيطة — المخالفة الأولى"}, {"slug": "ali-galway", "name": "علي", "city": "Galway", "gender": "m", "situation": "رخصة معلقة بسبب مخالفة سابقة. لم يعلم أن التعليق لا يزال سارياً.", "outcome": "تفاوض — تقليص التعليق"}, {"slug": "hana-limerick", "name": "هناء", "city": "Limerick", "gender": "f", "situation": "رخصة من خارج الاتحاد الأوروبي — غير معترف بها تلقائياً في أيرلندا.", "outcome": "سحب القضية بعد تسوية الوضع"}]},
        {"slug": "hadith-siyara", "title": "حادث سيارة مع إصابات في أيرلندا", "h1": "حادث سيارة.<br><em>لديك الحق في التعويض.</em>", "search_query": "حادث سيارة في ايرلندا تعويض", "law": "قانون المسؤولية المدنية — مهلة التقادم سنتان من تاريخ الحادث.", "time_limit": "سنتان من الحادث — تصرف في أقرب وقت ممكن", "practice_area": "personal-injury", "stories": [{"slug": "yusuf-dublin", "name": "يوسف", "city": "Dublin", "gender": "m", "situation": "اصطدم به من الخلف على الطريق السريع. عرض تأمين السائق الآخر €8,000. المحامي حصل على أكثر بكثير.", "outcome": "تعويض €33,000"}, {"slug": "rania-cork", "name": "رانيا", "city": "Cork", "gender": "f", "situation": "راكبة في سيارة صديق تسبب في الحادث. لم تكن تعلم أنها تستطيع المطالبة.", "outcome": "تعويض كامل ممنوح"}, {"slug": "tariq-galway", "name": "طارق", "city": "Galway", "gender": "m", "situation": "راجل دهسه سيارة في ممر المشاة. السائق نفى المسؤولية.", "outcome": "ثبوت المسؤولية — تعويض ممنوح"}, {"slug": "amira-limerick", "name": "أميرة", "city": "Limerick", "gender": "f", "situation": "حادث في العمل — دهستها شاحنة في المستودع.", "outcome": "التعويض يشمل الأجور المفقودة"}]},
        {"slug": "fasl-ghair-adil", "title": "الفصل التعسفي في أيرلندا", "h1": "فُصلت<em> بدون سبب وجيه</em><br>في أيرلندا.", "search_query": "فصل تعسفي من العمل في ايرلندا حقوقي", "law": "قانون الفصل التعسفي 1977 — حق تقديم شكوى إلى WRC خلال 6 أشهر.", "time_limit": "6 أشهر من تاريخ الفصل — لا تفوّت الموعد", "practice_area": "employment-law", "stories": [{"slug": "mahmoud-dublin", "name": "محمود", "city": "Dublin", "gender": "m", "situation": "فُصل بعد 5 سنوات بدون إنذارات أو إجراءات تأديبية. ادّعى صاحب العمل إعادة الهيكلة.", "outcome": "WRC قضى لصالحه — تعويض ممنوح"}, {"slug": "nadia-cork", "name": "نادية", "city": "Cork", "gender": "f", "situation": "فُصلت بعد فترة وجيزة من إعلان حملها. ادّعى صاحب العمل أسباباً أخرى.", "outcome": "تأكد التمييز — تعويض أقصى"}, {"slug": "karim-galway", "name": "كريم", "city": "Galway", "gender": "m", "situation": "فُصل بعد الإبلاغ عن ظروف عمل خطرة. بدون إنذار مسبق.", "outcome": "فصل انتقامي — تعويض إضافي"}, {"slug": "yasmin-limerick", "name": "ياسمين", "city": "Limerick", "gender": "f", "situation": "مهمتها أُلغيت لكن زميلة أصغر منها تولّت نفس المهام.", "outcome": "إثبات زيف إعادة الهيكلة — تعويض"}]},
        {"slug": "mushkilat-malak", "title": "مشاكل مع المالك في أيرلندا", "h1": "المالك<em> ينتهك حقوقك.</em><br>إليك ما يمكنك فعله.", "search_query": "مالك يريد إخراجي بشكل غير قانوني ايرلندا حقوق المستأجر", "law": "قانون الإيجارات السكنية — للمستأجرين حقوق قانونية قوية. RTB يتوسط في النزاعات.", "time_limit": "قدّم شكوى إلى RTB خلال 28 يوماً من الحادثة", "practice_area": "property-law", "stories": [{"slug": "walid-dublin", "name": "وليد", "city": "Dublin", "gender": "m", "situation": "أعطاه المالك 30 يوماً للمغادرة في يناير. 3 سنوات من الإيجار المنتظم.", "outcome": "توقف الإخلاء — يستطيع البقاء"}, {"slug": "samira-cork", "name": "سميرة", "city": "Cork", "gender": "f", "situation": "احتجز المالك كامل الوديعة مدّعياً أضراراً غير موجودة.", "outcome": "الوديعة مُعادة بالكامل"}, {"slug": "jaber-galway", "name": "جابر", "city": "Galway", "gender": "m", "situation": "رُفع الإيجار بنسبة 25% بدون إشعار مناسب.", "outcome": "الزيادة مُلغاة — الإيجار السابق محتفظ به"}, {"slug": "dina-limerick", "name": "دينا", "city": "Limerick", "gender": "f", "situation": "المالك دخل الشقة عدة مرات بدون إذن.", "outcome": "RTB أصدر أمراً باحترام الحقوق"}]},
        {"slug": "talaq-airlanda", "title": "الطلاق في أيرلندا — دليل للعرب", "h1": "الطلاق<em> في أيرلندا.</em><br>ما تحتاج معرفته.", "search_query": "كيف أحصل على طلاق في ايرلندا", "law": "قانون الأسرة — الطلاق في أيرلندا يستلزم انفصالاً لمدة سنتين على الأقل من أصل 3.", "time_limit": "لا يوجد موعد نهائي — لكن تصرف بسرعة لحماية الأصول", "practice_area": "family-law", "stories": [{"slug": "layla-dublin", "name": "ليلى", "city": "Dublin", "gender": "f", "situation": "متزوجة منذ 10 سنوات. أرادت الطلاق لكن لم تكن تعلم إن كان سيُعترف به في بلدها.", "outcome": "اكتمل الطلاق — معترف به دولياً"}, {"slug": "sami-cork", "name": "سامي", "city": "Cork", "gender": "m", "situation": "زوجته عادت إلى بلدها مع الأطفال. لم يعرف حقوقه.", "outcome": "اتفاقية حضانة أسست من خلال المحكمة"}, {"slug": "reem-galway", "name": "ريم", "city": "Galway", "gender": "f", "situation": "عقار في بلدها وفي أيرلندا. قلقة من كيفية تقسيمه.", "outcome": "اتفاقية عادلة — الممتلكات محتفظ بها"}, {"slug": "fadi-limerick", "name": "فادي", "city": "Limerick", "gender": "m", "situation": "طلاق متنازع عليه. الزوجة تطالب بمعاشه الأيرلندي.", "outcome": "المعاش محمي جزئياً — اتفاقية مُتفاوض عليها"}]},
        {"slug": "mushkilat-tashira", "title": "مشاكل التأشيرة أو الهجرة في أيرلندا", "h1": "مشاكل في<em> التأشيرة أو الهجرة</em><br>في أيرلندا.", "search_query": "رفض تأشيرة ايرلندا ماذا أفعل", "law": "قانون الهجرة 2004 — لغير المواطنين الأوروبيين الحق في الاستئناف ضد رفض التأشيرة.", "time_limit": "استأنف الرفض خلال 15 يوم عمل", "practice_area": "immigration-law", "stories": [{"slug": "nasser-dublin", "name": "ناصر", "city": "Dublin", "gender": "m", "situation": "انتهت صلاحية IRP بسبب تأخر المواعيد. صاحب العمل يطلب وثيقة سارية.", "outcome": "تسوية الوضع — الوظيفة محتفظ بها"}, {"slug": "heba-cork", "name": "هبة", "city": "Cork", "gender": "f", "situation": "غير مواطنة أوروبية متزوجة من عربي. رُفض تأشيرة لم شمل العائلة.", "outcome": "قُبل الاستئناف — التأشيرة ممنوحة"}, {"slug": "khaled-galway", "name": "خالد", "city": "Galway", "gender": "m", "situation": "أمر ترحيل بعد غياب طويل عن أيرلندا.", "outcome": "إلغاء الأمر — تأكيد حق الإقامة"}, {"slug": "ola-limerick", "name": "علا", "city": "Limerick", "gender": "f", "situation": "رُفض Stamp 4 بعد 5 سنوات من الإقامة القانونية.", "outcome": "منح Stamp 4 بعد الاستئناف"}]},
        {"slug": "isabat-jismiya", "title": "الإصابات الجسدية في أيرلندا — التعويض", "h1": "مصاب<em> بسبب خطأ شخص آخر</em><br>في أيرلندا.", "search_query": "حادث عمل في ايرلندا تعويض", "law": "قانون المسؤولية المدنية — مهلة التقادم سنتان. حوادث العمل مشمولة بقانون السلامة والصحة في العمل 2005.", "time_limit": "سنتان من الحادث — لا تدع الوقت يمر", "practice_area": "personal-injury", "stories": [{"slug": "saeed-dublin", "name": "سعيد", "city": "Dublin", "gender": "m", "situation": "أصيب في العمل أثناء رفع صناديق ثقيلة دون تدريب. ادّعى صاحب العمل أنه أمر طبيعي.", "outcome": "تعويض — صاحب العمل وُجد مذنباً"}, {"slug": "asma-cork", "name": "أسماء", "city": "Cork", "gender": "f", "situation": "سقطت في ممر مبلل في السوبرماركت. لا لافتات تحذيرية.", "outcome": "تعويض كامل شامل التكاليف الطبية"}, {"slug": "ziad-galway", "name": "زياد", "city": "Galway", "gender": "m", "situation": "يده علقت في آلة بدون حماية في المصنع.", "outcome": "تعويض كبير — إعاقة دائمة"}, {"slug": "rula-limerick", "name": "رلى", "city": "Limerick", "gender": "f", "situation": "اعتُدي عليها من قِبَل عميل في العمل. لم يكن لدى صاحب العمل بروتوكولات سلامة.", "outcome": "صاحب العمل وُجد مسؤولاً — تعويض"}]},
        {"slug": "sahib-amal-ghashshash", "title": "صاحب عمل أو مالك غاشّ في أيرلندا", "h1": "<em>خداع</em> من صاحب عمل<br>أو مالك في أيرلندا.", "search_query": "صاحب العمل لم يدفع راتبي في ايرلندا", "law": "قانون دفع الأجور 1991 — آليات قانونية واضحة لاسترداد الأجور.", "time_limit": "6 سنوات لاسترداد الأجور — تصرف قبل انتهاء المهلة", "practice_area": "employment-law", "stories": [{"slug": "bilal-dublin", "name": "بلال", "city": "Dublin", "gender": "m", "situation": "لم يدفع صاحب العمل آخر 3 أسابيع من الراتب عند استقالته.", "outcome": "استرداد الرواتب كاملةً عبر WRC"}, {"slug": "ghada-cork", "name": "غادة", "city": "Cork", "gender": "f", "situation": "أخذ المالك وديعة €2,000 واختفى.", "outcome": "استرداد الأموال عبر RTB والمحكمة"}, {"slug": "ramzi-galway", "name": "رامزي", "city": "Galway", "gender": "m", "situation": "موظف يومي — يُدفع له €5/ساعة أقل من الحد الأدنى القانوني.", "outcome": "استرداد الفرق — فتح تحقيق WRC"}, {"slug": "mona-limerick", "name": "منى", "city": "Limerick", "gender": "f", "situation": "وكالة التوظيف تخصم عمولة من الراتب — غير قانوني في أيرلندا.", "outcome": "استرداد العمولات — تغريم الوكالة"}]},
    ],
    "es": [
        {"slug": "conduccion-borracho", "title": "Detenido por Conducir Borracho en Irlanda", "h1": "Detenido <em>conduciendo borracho</em><br>en Irlanda.", "search_query": "me detuvieron conduciendo borracho en irlanda qué hago", "law": "Road Traffic Act 2010 — límite legal 50mg/100ml de sangre. Suspensión automática del carnet.", "time_limit": "Actúa inmediatamente tras recibir la citación judicial", "practice_area": "criminal-law", "stories": [{"slug": "carlos-dublin", "name": "Carlos", "city": "Dublin", "gender": "m", "situation": "Parado en un control rutinario con 58mg — ligeramente por encima del límite. Riesgo de perder el carnet y el empleo.", "outcome": "Cargo rechazado — carnet conservado"}, {"slug": "lucia-cork", "name": "Lucía", "city": "Cork", "gender": "f", "situation": "Detenida tras un accidente menor. Primera infracción. Preocupada por su empleo sanitario.", "outcome": "Suspensión reducida al mínimo legal"}, {"slug": "miguel-galway", "name": "Miguel", "city": "Galway", "gender": "m", "situation": "Tasa alta de alcohol. Pensaba que no tenía salida. El abogado encontró un vicio procesal.", "outcome": "Caso archivado — vicio procesal"}, {"slug": "elena-limerick", "name": "Elena", "city": "Limerick", "gender": "f", "situation": "Enfermera. Una condena destruiría su carrera profesional.", "outcome": "Licencia profesional protegida"}]},
        {"slug": "sin-seguro", "title": "Detenido Sin Seguro en Irlanda", "h1": "Detenido conduciendo<br><em>sin seguro</em> en Irlanda.", "search_query": "me pararon sin seguro del coche en irlanda", "law": "Road Traffic Act — conducir sin seguro es delito penal. Multa obligatoria y posible suspensión.", "time_limit": "Contacta a un abogado antes de la fecha del tribunal", "practice_area": "criminal-law", "stories": [{"slug": "jose-dublin", "name": "José", "city": "Dublin", "gender": "m", "situation": "Conducía el coche de su pareja sin saber que no estaba cubierto como conductor adicional.", "outcome": "Multa reducida — sin suspensión"}, {"slug": "maria-cork", "name": "María", "city": "Cork", "gender": "f", "situation": "Seguro vencido dos días antes. No recibió ningún aviso.", "outcome": "Caso archivado — circunstancias atenuantes"}, {"slug": "antonio-galway", "name": "Antonio", "city": "Galway", "gender": "m", "situation": "Coche asegurado por el empleador. El empleador olvidó renovar la póliza.", "outcome": "El empleador asumió la responsabilidad"}, {"slug": "sara-limerick", "name": "Sara", "city": "Limerick", "gender": "f", "situation": "Seguro comprado online pero no activado correctamente.", "outcome": "Penalización fija — sin antecedentes penales"}]},
        {"slug": "sin-carnet", "title": "Detenido Sin Carnet de Conducir en Irlanda", "h1": "Detenido conduciendo<br><em>sin carnet</em> en Irlanda.", "search_query": "me pararon sin carnet de conducir en irlanda", "law": "Road Traffic Act — conducir sin carnet válido es delito. El carnet español tiene validez limitada en Irlanda.", "time_limit": "Actúa antes de la fecha del tribunal", "practice_area": "criminal-law", "stories": [{"slug": "pablo-dublin", "name": "Pablo", "city": "Dublin", "gender": "m", "situation": "Carnet español caducado. No sabía que tenía que canjearlo por uno irlandés.", "outcome": "Multa reducida — circunstancias atenuantes"}, {"slug": "ana-cork", "name": "Ana", "city": "Cork", "gender": "f", "situation": "Carnet provisional. Conducía sola creyendo que estaba permitido.", "outcome": "Penalización mínima — primera infracción"}, {"slug": "david-galway", "name": "David", "city": "Galway", "gender": "m", "situation": "Carnet suspendido por una infracción anterior. No sabía que la suspensión seguía vigente.", "outcome": "Negociación — suspensión reducida"}, {"slug": "isabel-limerick", "name": "Isabel", "city": "Limerick", "gender": "f", "situation": "Carnet de fuera de la UE — no reconocido automáticamente en Irlanda.", "outcome": "Caso retirado tras regularización"}]},
        {"slug": "accidente-coche", "title": "Accidente de Coche con Lesiones en Irlanda", "h1": "Accidente de coche.<br><em>Tienes derecho a indemnización.</em>", "search_query": "accidente de coche en irlanda tengo derecho a indemnización", "law": "Civil Liability Act — plazo de prescripción 2 años desde el accidente.", "time_limit": "2 años del accidente — actúa cuanto antes", "practice_area": "personal-injury", "stories": [{"slug": "fernando-dublin", "name": "Fernando", "city": "Dublin", "gender": "m", "situation": "Le chocaron por detrás en la autopista. El seguro del otro conductor ofreció €8,000. El abogado consiguió mucho más.", "outcome": "Indemnización de €35,000"}, {"slug": "laura-cork", "name": "Laura", "city": "Cork", "gender": "f", "situation": "Pasajera en el coche de un amigo que causó el accidente. No sabía que podía reclamar.", "outcome": "Indemnización total concedida"}, {"slug": "roberto-galway", "name": "Roberto", "city": "Galway", "gender": "m", "situation": "Peatón atropellado en el paso de cebra. El conductor negó la responsabilidad.", "outcome": "Responsabilidad establecida — indemnización concedida"}, {"slug": "pilar-limerick", "name": "Pilar", "city": "Limerick", "gender": "f", "situation": "Accidente laboral — atropellada por una furgoneta en el almacén.", "outcome": "Indemnización incluye salarios perdidos"}]},
        {"slug": "despido-injusto", "title": "Despido Injusto en Irlanda", "h1": "Despedido<em> sin motivo justificado</em><br>en Irlanda.", "search_query": "despido injusto en irlanda qué derechos tengo", "law": "Unfair Dismissals Act 1977 — tienes derecho a reclamar ante el WRC en 6 meses.", "time_limit": "6 meses desde el despido — no te pierdas el plazo", "practice_area": "employment-law", "stories": [{"slug": "manuel-dublin", "name": "Manuel", "city": "Dublin", "gender": "m", "situation": "Despedido tras 5 años sin advertencias ni proceso disciplinario. La empresa alegó reestructuración.", "outcome": "WRC falló a su favor — compensación concedida"}, {"slug": "carmen-cork", "name": "Carmen", "city": "Cork", "gender": "f", "situation": "Despedida poco después de anunciar su embarazo. La empresa inventó otros motivos.", "outcome": "Discriminación confirmada — compensación máxima"}, {"slug": "javier-galway", "name": "Javier", "city": "Galway", "gender": "m", "situation": "Despedido tras denunciar condiciones peligrosas. Sin aviso previo.", "outcome": "Despido represalia — compensación adicional"}, {"slug": "teresa-limerick", "name": "Teresa", "city": "Limerick", "gender": "f", "situation": "Puesto eliminado pero una compañera más joven asumió las mismas tareas.", "outcome": "Reestructuración falsa probada — compensación"}]},
        {"slug": "problemas-casero", "title": "Problemas con el Casero en Irlanda", "h1": "El casero<em> viola tus derechos.</em><br>Esto es lo que puedes hacer.", "search_query": "casero quiere echarme ilegalmente irlanda derechos inquilino", "law": "Residential Tenancies Act — los inquilinos tienen derechos legales fuertes. RTB media en disputas.", "time_limit": "Presenta reclamación al RTB en 28 días del incidente", "practice_area": "property-law", "stories": [{"slug": "rodrigo-dublin", "name": "Rodrigo", "city": "Dublin", "gender": "m", "situation": "El casero le dio 30 días para marcharse en enero. 3 años de alquiler siempre al día.", "outcome": "Desahucio bloqueado — puede quedarse"}, {"slug": "beatriz-cork", "name": "Beatriz", "city": "Cork", "gender": "f", "situation": "El casero retuvo toda la fianza alegando daños inexistentes.", "outcome": "Fianza devuelta íntegramente"}, {"slug": "sergio-galway", "name": "Sergio", "city": "Galway", "gender": "m", "situation": "Alquiler subido un 25% sin aviso adecuado.", "outcome": "Subida anulada — alquiler anterior mantenido"}, {"slug": "monica-limerick", "name": "Mónica", "city": "Limerick", "gender": "f", "situation": "El casero entró en el piso sin permiso varias veces.", "outcome": "RTB emitió orden de respeto de derechos"}]},
        {"slug": "divorcio-irlanda", "title": "Divorcio en Irlanda — Guía para Españoles", "h1": "Divorcio<em> en Irlanda.</em><br>Lo que debes saber.", "search_query": "cómo hacer el divorcio en irlanda español", "law": "Family Law Act — el divorcio en Irlanda requiere separación de al menos 2 años de los últimos 3.", "time_limit": "No hay plazo — pero actúa rápido para proteger tus bienes", "practice_area": "family-law", "stories": [{"slug": "rosa-dublin", "name": "Rosa", "city": "Dublin", "gender": "f", "situation": "Casada 12 años. Quería divorciarse pero no sabía si sería reconocido en España.", "outcome": "Divorcio finalizado — reconocido en la UE"}, {"slug": "alberto-cork", "name": "Alberto", "city": "Cork", "gender": "m", "situation": "Su esposa se fue a España con los hijos. No sabía qué derechos tenía.", "outcome": "Acuerdo de custodia establecido por el tribunal"}, {"slug": "consuelo-galway", "name": "Consuelo", "city": "Galway", "gender": "f", "situation": "Inmuebles en España e Irlanda. Preocupada por cómo se repartirían.", "outcome": "Acuerdo justo — bienes conservados"}, {"slug": "pedro-limerick", "name": "Pedro", "city": "Limerick", "gender": "m", "situation": "Divorcio contestado. Su esposa reclamaba su pensión irlandesa.", "outcome": "Pensión parcialmente protegida — acuerdo negociado"}]},
        {"slug": "problemas-visado", "title": "Problemas con el Visado o Inmigración en Irlanda", "h1": "Problemas con<em> visado o inmigración</em><br>en Irlanda.", "search_query": "visado denegado irlanda qué hago español", "law": "Immigration Act 2004 — los ciudadanos no comunitarios tienen derecho a recurrir denegaciones de visado.", "time_limit": "Recurre la denegación en 15 días hábiles", "practice_area": "immigration-law", "stories": [{"slug": "andres-dublin", "name": "Andrés", "city": "Dublin", "gender": "m", "situation": "IRP vencido por retrasos en las citas. El empleador exigía documento válido.", "outcome": "Estatus regularizado — empleo conservado"}, {"slug": "victoria-cork", "name": "Victoria", "city": "Cork", "gender": "f", "situation": "No ciudadana de la UE casada con español. Visado de reagrupación denegado.", "outcome": "Recurso aceptado — visado concedido"}, {"slug": "gabriel-galway", "name": "Gabriel", "city": "Galway", "gender": "m", "situation": "Orden de deportación tras ausencia prolongada de Irlanda.", "outcome": "Orden anulada — derecho de residencia confirmado"}, {"slug": "paloma-limerick", "name": "Paloma", "city": "Limerick", "gender": "f", "situation": "Stamp 4 denegado tras 5 años de residencia legal.", "outcome": "Stamp 4 concedido tras recurso"}]},
        {"slug": "lesiones-personales", "title": "Lesiones Personales en Irlanda — Indemnización", "h1": "Lesionado<em> por culpa de otro</em><br>en Irlanda.", "search_query": "accidente laboral irlanda puedo pedir indemnización", "law": "Civil Liability Act — plazo de prescripción 2 años. Accidentes laborales cubiertos por Safety Health and Welfare at Work Act 2005.", "time_limit": "2 años del accidente — no dejes pasar el tiempo", "practice_area": "personal-injury", "stories": [{"slug": "francisco-dublin", "name": "Francisco", "city": "Dublin", "gender": "m", "situation": "Accidentado en el trabajo levantando cajas pesadas sin formación. El jefe dijo que era lo normal.", "outcome": "Indemnización — empleador declarado culpable"}, {"slug": "amparo-cork", "name": "Amparo", "city": "Cork", "gender": "f", "situation": "Cayó en un pasillo mojado en el supermercado. Sin señales de advertencia.", "outcome": "Indemnización total incluidos gastos médicos"}, {"slug": "ernesto-galway", "name": "Ernesto", "city": "Galway", "gender": "m", "situation": "Mano atrapada en maquinaria sin protección en la fábrica.", "outcome": "Indemnización importante — daño permanente"}, {"slug": "maribel-limerick", "name": "Maribel", "city": "Limerick", "gender": "f", "situation": "Agredida por un cliente en el trabajo. La empresa no tenía protocolos de seguridad.", "outcome": "Empleador declarado responsable — indemnización"}]},
        {"slug": "empleador-estafador", "title": "Empleador o Casero Deshonesto en Irlanda", "h1": "<em>Engañado</em> por empleador<br>o casero en Irlanda.", "search_query": "el empleador no me ha pagado el sueldo en irlanda", "law": "Payment of Wages Act 1991 — mecanismos legales claros para recuperar salarios.", "time_limit": "6 años para recuperar salarios — actúa antes del plazo", "practice_area": "employment-law", "stories": [{"slug": "enrique-dublin", "name": "Enrique", "city": "Dublin", "gender": "m", "situation": "El empleador no le pagó las últimas 3 semanas al dimitir.", "outcome": "Salarios recuperados íntegramente por WRC"}, {"slug": "dolores-cork", "name": "Dolores", "city": "Cork", "gender": "f", "situation": "El casero se quedó con la fianza de €2,000 y desapareció.", "outcome": "Dinero recuperado por RTB y tribunal"}, {"slug": "gonzalo-galway", "name": "Gonzalo", "city": "Galway", "gender": "m", "situation": "Contratado como jornalero — pagado €5/hora por debajo del salario mínimo.", "outcome": "Diferencia recuperada — inspección WRC iniciada"}, {"slug": "rosario-limerick", "name": "Rosario", "city": "Limerick", "gender": "f", "situation": "La agencia de empleo descontaba comisión del sueldo — ilegal en Irlanda.", "outcome": "Comisiones recuperadas — agencia sancionada"}]},
    ],
    "ru": [
        {"slug": "ezda-pyanym", "title": "Задержан за Пьяную Езду в Ирландии", "h1": "Задержан <em>за пьяную езду</em><br>в Ирландии.", "search_query": "задержан за пьяную езду в ирландии что делать", "law": "Road Traffic Act 2010 — законный лимит 50мг/100мл крови. Автоматическое лишение прав.", "time_limit": "Действуй немедленно после получения судебной повестки", "practice_area": "criminal-law", "stories": [{"slug": "alexei-dublin", "name": "Алексей", "city": "Dublin", "gender": "m", "situation": "Остановлен на плановой проверке с 58мг — чуть выше лимита. Риск лишиться прав и работы.", "outcome": "Обвинение снято — права сохранены"}, {"slug": "natasha-cork", "name": "Наташа", "city": "Cork", "gender": "f", "situation": "Остановлена после небольшого ДТП. Первое нарушение. Беспокоится о работе в здравоохранении.", "outcome": "Срок лишения сокращён до минимума"}, {"slug": "dmitri-galway", "name": "Дмитрий", "city": "Galway", "gender": "m", "situation": "Высокое содержание алкоголя. Думал, что выхода нет. Адвокат нашёл процессуальную ошибку.", "outcome": "Дело закрыто — процессуальная ошибка"}, {"slug": "olga-limerick", "name": "Ольга", "city": "Limerick", "gender": "f", "situation": "Медсестра. Осуждение уничтожило бы её карьеру.", "outcome": "Профессиональная лицензия защищена"}]},
        {"slug": "bez-strakhovki", "title": "Задержан без Страховки в Ирландии", "h1": "Задержан без<br><em>страховки</em> в Ирландии.", "search_query": "задержан без страховки автомобиль ирландия", "law": "Road Traffic Act — езда без страховки — уголовное преступление. Обязательный штраф и возможное лишение прав.", "time_limit": "Свяжись с адвокатом до даты суда", "practice_area": "criminal-law", "stories": [{"slug": "sergei-dublin", "name": "Сергей", "city": "Dublin", "gender": "m", "situation": "Ехал на машине партнёрши, не зная, что не застрахован как дополнительный водитель.", "outcome": "Штраф снижен — без лишения прав"}, {"slug": "irina-cork", "name": "Ирина", "city": "Cork", "gender": "f", "situation": "Страховка закончилась два дня назад. Уведомления не получала.", "outcome": "Дело закрыто — смягчающие обстоятельства"}, {"slug": "pavel-galway", "name": "Павел", "city": "Galway", "gender": "m", "situation": "Машина застрахована работодателем. Работодатель забыл продлить полис.", "outcome": "Работодатель взял ответственность на себя"}, {"slug": "elena-limerick", "name": "Елена", "city": "Limerick", "gender": "f", "situation": "Страховка куплена онлайн, но не активирована правильно.", "outcome": "Фиксированный штраф — без судимости"}]},
        {"slug": "bez-prav", "title": "Задержан без Водительских Прав в Ирландии", "h1": "Задержан без<br><em>водительских прав</em> в Ирландии.", "search_query": "задержан без прав вождения в ирландии", "law": "Road Traffic Act — езда без действующих прав — преступление. Российские права имеют ограниченный срок действия в Ирландии.", "time_limit": "Действуй до даты судебного заседания", "practice_area": "criminal-law", "stories": [{"slug": "andrei-dublin", "name": "Андрей", "city": "Dublin", "gender": "m", "situation": "Российские права истекли. Не знал, что нужно обменять на ирландские.", "outcome": "Штраф снижен — смягчающие обстоятельства"}, {"slug": "marina-cork", "name": "Марина", "city": "Cork", "gender": "f", "situation": "Временные права. Ехала одна, думала, что это разрешено.", "outcome": "Минимальное наказание — первое нарушение"}, {"slug": "konstantin-galway", "name": "Константин", "city": "Galway", "gender": "m", "situation": "Права лишены за предыдущее нарушение. Не знал, что лишение ещё в силе.", "outcome": "Переговоры — срок лишения сокращён"}, {"slug": "vera-limerick", "name": "Вера", "city": "Limerick", "gender": "f", "situation": "Права из страны вне ЕС — не признаются автоматически в Ирландии.", "outcome": "Дело снято после урегулирования"}]},
        {"slug": "avtoavariya", "title": "ДТП с Травмами в Ирландии", "h1": "Автоавария.<br><em>Ты имеешь право на компенсацию.</em>", "search_query": "дтп авария в ирландии компенсация", "law": "Civil Liability Act — срок исковой давности 2 года со дня аварии.", "time_limit": "2 года с момента аварии — действуй как можно скорее", "practice_area": "personal-injury", "stories": [{"slug": "mikhail-dublin", "name": "Михаил", "city": "Dublin", "gender": "m", "situation": "Въехали сзади на трассе. Страховая другого водителя предложила €8,000. Адвокат добился намного больше.", "outcome": "Компенсация €32,000"}, {"slug": "anastasia-cork", "name": "Анастасия", "city": "Cork", "gender": "f", "situation": "Пассажир в машине друга, который спровоцировал аварию. Не знала, что может требовать компенсацию.", "outcome": "Полная компенсация выплачена"}, {"slug": "viktor-galway", "name": "Виктор", "city": "Galway", "gender": "m", "situation": "Пешеход сбит на зебре. Водитель поначалу отрицал вину.", "outcome": "Ответственность установлена — компенсация выплачена"}, {"slug": "lyudmila-limerick", "name": "Людмила", "city": "Limerick", "gender": "f", "situation": "Производственная травма — сбита фургоном на складе.", "outcome": "Компенсация включает потерянные доходы"}]},
        {"slug": "nezakonnoe-uvolnenie", "title": "Незаконное Увольнение в Ирландии", "h1": "Уволен<em> без уважительной причины</em><br>в Ирландии.", "search_query": "незаконное увольнение в ирландии мои права", "law": "Unfair Dismissals Act 1977 — право подать жалобу в WRC в течение 6 месяцев.", "time_limit": "6 месяцев с момента увольнения — не упусти срок", "practice_area": "employment-law", "stories": [{"slug": "nikolai-dublin", "name": "Николай", "city": "Dublin", "gender": "m", "situation": "Уволен после 5 лет без предупреждений или дисциплинарных процедур. Работодатель сослался на реструктуризацию.", "outcome": "WRC постановил в его пользу — компенсация выплачена"}, {"slug": "svetlana-cork", "name": "Светлана", "city": "Cork", "gender": "f", "situation": "Уволена вскоре после объявления о беременности. Работодатель придумал другие причины.", "outcome": "Дискриминация подтверждена — максимальная компенсация"}, {"slug": "roman-galway", "name": "Роман", "city": "Galway", "gender": "m", "situation": "Уволен после сообщения об опасных условиях труда. Без предупреждения.", "outcome": "Незаконное увольнение — дополнительная компенсация"}, {"slug": "tatiana-limerick", "name": "Татьяна", "city": "Limerick", "gender": "f", "situation": "Должность ликвидирована, но молодая коллега взяла те же обязанности.", "outcome": "Фиктивная реструктуризация доказана — компенсация"}]},
        {"slug": "problemy-arendodatel", "title": "Проблемы с Арендодателем в Ирландии", "h1": "Арендодатель<em> нарушает твои права.</em><br>Вот что делать.", "search_query": "арендодатель хочет выселить меня незаконно ирландия", "law": "Residential Tenancies Act — арендаторы имеют сильные правовые права. RTB разрешает споры.", "time_limit": "Подай жалобу в RTB в течение 28 дней с момента инцидента", "practice_area": "property-law", "stories": [{"slug": "igor-dublin", "name": "Игорь", "city": "Dublin", "gender": "m", "situation": "Арендодатель дал 30 дней на выезд в январе. 3 года своевременных платежей.", "outcome": "Выселение остановлено — может остаться"}, {"slug": "galina-cork", "name": "Галина", "city": "Cork", "gender": "f", "situation": "Арендодатель удержал весь залог, ссылаясь на несуществующий ущерб.", "outcome": "Залог возвращён полностью"}, {"slug": "stepan-galway", "name": "Степан", "city": "Galway", "gender": "m", "situation": "Аренда повышена на 25% без надлежащего уведомления.", "outcome": "Повышение аннулировано — прежняя аренда сохранена"}, {"slug": "natalya-limerick", "name": "Наталья", "city": "Limerick", "gender": "f", "situation": "Арендодатель несколько раз входил в квартиру без разрешения.", "outcome": "RTB вынес постановление о соблюдении прав"}]},
        {"slug": "razvod-v-irlandii", "title": "Развод в Ирландии — Гид для Русских", "h1": "Развод<em> в Ирландии.</em><br>Что нужно знать.", "search_query": "как получить развод в ирландии русский", "law": "Family Law Act — развод в Ирландии требует раздельного проживания не менее 2 лет из последних 3.", "time_limit": "Нет срока — но действуй быстро для защиты имущества", "practice_area": "family-law", "stories": [{"slug": "larisa-dublin", "name": "Лариса", "city": "Dublin", "gender": "f", "situation": "Замужем 10 лет. Хотела развода, но не знала, будет ли он признан на родине.", "outcome": "Развод завершён — признан международно"}, {"slug": "boris-cork", "name": "Борис", "city": "Cork", "gender": "m", "situation": "Жена уехала с детьми. Не знал своих прав.", "outcome": "Соглашение об опеке установлено судом"}, {"slug": "valentina-galway", "name": "Валентина", "city": "Galway", "gender": "f", "situation": "Недвижимость в России и Ирландии. Беспокоилась о разделе.", "outcome": "Справедливое соглашение — имущество сохранено"}, {"slug": "yuri-limerick", "name": "Юрий", "city": "Limerick", "gender": "m", "situation": "Спорный развод. Жена претендовала на его ирландскую пенсию.", "outcome": "Пенсия частично защищена — соглашение достигнуто"}]},
        {"slug": "problemy-vizy", "title": "Проблемы с Визой или Иммиграцией в Ирландии", "h1": "Проблемы с<em> визой или иммиграцией</em><br>в Ирландии.", "search_query": "отказ в визе ирландия что делать русский", "law": "Immigration Act 2004 — не-граждане ЕС имеют право оспорить отказ в визе.", "time_limit": "Обжалуй отказ в течение 15 рабочих дней", "practice_area": "immigration-law", "stories": [{"slug": "vasily-dublin", "name": "Василий", "city": "Dublin", "gender": "m", "situation": "IRP истёк из-за задержек с записью. Работодатель требовал действующий документ.", "outcome": "Статус урегулирован — работа сохранена"}, {"slug": "oksana-cork", "name": "Оксана", "city": "Cork", "gender": "f", "situation": "Не гражданка ЕС замужем за россиянином. Отказ в визе на воссоединение семьи.", "outcome": "Апелляция принята — виза выдана"}, {"slug": "timur-galway", "name": "Тимур", "city": "Galway", "gender": "m", "situation": "Депортационный ордер после длительного отсутствия в Ирландии.", "outcome": "Ордер отменён — право проживания подтверждено"}, {"slug": "zoya-limerick", "name": "Зоя", "city": "Limerick", "gender": "f", "situation": "Stamp 4 отклонён после 5 лет законного проживания.", "outcome": "Stamp 4 выдан после апелляции"}]},
        {"slug": "telesnye-povrezhdeniya", "title": "Телесные Повреждения в Ирландии — Компенсация", "h1": "Пострадал<em> по чужой вине</em><br>в Ирландии.", "search_query": "производственная травма ирландия компенсация", "law": "Civil Liability Act — срок исковой давности 2 года. Производственные травмы покрыты Safety Health and Welfare at Work Act 2005.", "time_limit": "2 года с момента травмы — не дай времени уйти", "practice_area": "personal-injury", "stories": [{"slug": "oleg-dublin", "name": "Олег", "city": "Dublin", "gender": "m", "situation": "Производственная травма при подъёме тяжёлых ящиков без инструктажа. Работодатель сказал, что это норма.", "outcome": "Компенсация — работодатель признан виновным"}, {"slug": "lyubov-cork", "name": "Любовь", "city": "Cork", "gender": "f", "situation": "Упала в мокром коридоре супермаркета. Предупреждающих знаков не было.", "outcome": "Полная компенсация включая медицинские расходы"}, {"slug": "artem-galway", "name": "Артём", "city": "Galway", "gender": "m", "situation": "Рука попала в машину без защиты на заводе.", "outcome": "Значительная компенсация — постоянная нетрудоспособность"}, {"slug": "zhanna-limerick", "name": "Жанна", "city": "Limerick", "gender": "f", "situation": "Нападение клиента на рабочем месте. У работодателя не было протоколов безопасности.", "outcome": "Работодатель признан ответственным — компенсация"}]},
        {"slug": "nesostoyatelny-rabotodatel", "title": "Нечестный Работодатель или Арендодатель в Ирландии", "h1": "<em>Обманут</em> работодателем<br>или арендодателем в Ирландии.", "search_query": "работодатель не заплатил зарплату ирландия что делать", "law": "Payment of Wages Act 1991 — чёткие правовые механизмы для взыскания заработной платы.", "time_limit": "6 лет на взыскание заработной платы — действуй до истечения срока", "practice_area": "employment-law", "stories": [{"slug": "gennady-dublin", "name": "Геннадий", "city": "Dublin", "gender": "m", "situation": "Работодатель не выплатил последние 3 недели зарплаты при увольнении.", "outcome": "Зарплата полностью взыскана через WRC"}, {"slug": "zinaida-cork", "name": "Зинаида", "city": "Cork", "gender": "f", "situation": "Арендодатель забрал залог €2,000 и исчез.", "outcome": "Деньги взысканы через RTB и суд"}, {"slug": "ruslan-galway", "name": "Руслан", "city": "Galway", "gender": "m", "situation": "Нанят поденщиком — платили €5/час ниже установленного минимума.", "outcome": "Разница взыскана — инспекция WRC инициирована"}, {"slug": "raisa-limerick", "name": "Раиса", "city": "Limerick", "gender": "f", "situation": "Агентство по трудоустройству удерживало комиссию из зарплаты — незаконно в Ирландии.", "outcome": "Комиссии взысканы — агентство оштрафовано"}]},
    ],
})

def slugify(text):
    text = unicodedata.normalize('NFD', text)
    text = ''.join(c for c in text if unicodedata.category(c) != 'Mn')
    text = text.lower().strip()
    text = re.sub(r'[^a-z0-9\s-]', '', text)
    text = re.sub(r'[\s,]+', '-', text).strip('-')
    return text

def call_claude(prompt, system=None, max_tokens=4000):
    messages = [{"role": "user", "content": prompt}]
    body = {"model": "claude-haiku-4-5-20251001", "max_tokens": max_tokens, "messages": messages}
    if system:
        body["system"] = system
    payload = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json", "x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"].strip()
    except Exception as e:
        print(f"API error: {e}")
        return None

def build_assistant_js(lang):
    cfg = LANGUAGES[lang]
    sols_json = json.dumps(cfg["solicitors"])
    return f"""
const ASSISTANT_IMG = "{cfg['assistant_img']}";
const ASSISTANT_NAME = "{cfg['assistant']}";
const ASSISTANT_SOLS = {sols_json};
let aHistory = [], aStage = "story", aCollected = {{}};
const ASSISTANT_PROMPT = {json.dumps(cfg['system_prompt'])};
function aAddMsg(text,isUser){{const msgs=document.getElementById('assistantMessages');if(!msgs)return;const row=document.createElement('div');row.className='amsg'+(isUser?' user':'');if(!isUser){{const av=document.createElement('div');av.className='amsg-av';av.innerHTML='<img src="'+ASSISTANT_IMG+'" alt="'+ASSISTANT_NAME+'"/>';row.appendChild(av);}}const b=document.createElement('div');b.className='amsg-bubble';b.textContent=text;row.appendChild(b);msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;}}
function aShowSols(){{const msgs=document.getElementById('assistantMessages');if(!msgs)return;const wrap=document.createElement('div');wrap.className='sol-cards';ASSISTANT_SOLS.forEach(sol=>{{const card=document.createElement('div');card.className='sol-card';card.innerHTML='<div class="sol-av"><img src="'+sol.img+'"/></div><div class="sol-info"><div class="sol-name">'+sol.name+'</div><div class="sol-area">'+sol.area+' · '+sol.county+'</div><div class="sol-stars">★★★★★</div></div><div class="sol-badge">✓</div>';wrap.appendChild(card);}});msgs.appendChild(wrap);msgs.scrollTop=msgs.scrollHeight;}}
function aShowTyping(){{const msgs=document.getElementById('assistantMessages');if(!msgs)return;const row=document.createElement('div');row.className='a-typing';row.id='aTyping';row.innerHTML='<div class="amsg-av"><img src="'+ASSISTANT_IMG+'"/></div><div class="a-typing-bubble"><div class="adot"></div><div class="adot"></div><div class="adot"></div></div>';msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;}}
function aRemoveTyping(){{const t=document.getElementById('aTyping');if(t)t.remove();}}
async function aSend(){{const input=document.getElementById('assistantInput');if(!input)return;const text=input.value.trim();if(!text)return;input.value='';input.style.height='auto';aAddMsg(text,true);aHistory.push({{role:'user',content:text}});if(aStage==='name')aCollected.name=text;if(aStage==='phone')aCollected.phone=text;aShowTyping();try{{const res=await fetch('/api/chat',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{system:ASSISTANT_PROMPT+'\\n\\nCurrent stage: '+aStage,messages:aHistory}})}});aRemoveTyping();if(!res.ok){{aAddMsg('Error. Please try again.',false);return;}}const data=await res.json();const raw=data.content?.[0]?.text||'';let parsed;try{{const m=raw.replace(/```json|```/g,'').trim().match(/\\{{[\\s\\S]*\\}}/);parsed=m?JSON.parse(m[0]):null;if(!parsed||!parsed.message)throw 0;}}catch{{parsed={{message:raw||'Something went wrong.',next_stage:aStage}};}}aAddMsg(parsed.message,false);aHistory.push({{role:'assistant',content:parsed.message}});if(parsed.show_solicitors)setTimeout(aShowSols,500);if(parsed.next_stage)aStage=parsed.next_stage;if(aStage==='done'&&aCollected.phone){{const transcript=aHistory.map(m=>(m.role==='user'?'Visitor: ':'Assistant: ')+m.content).join('\\n');fetch('/api/leads',{{method:'POST',headers:{{'Content-Type':'application/json'}},body:JSON.stringify({{name:aCollected.name||'',phone:aCollected.phone||'',issue:aHistory[0]?.content?.substring(0,120)||'',transcript:transcript,source:window.location.pathname}})}});}}}}catch(e){{aRemoveTyping();aAddMsg('Network error.',false);}}}}
const aTa=document.getElementById('assistantInput');if(aTa){{aTa.addEventListener('input',function(){{this.style.height='auto';this.style.height=Math.min(this.scrollHeight,70)+'px';}});aTa.addEventListener('keydown',function(e){{if(e.key==='Enter'&&!e.shiftKey){{e.preventDefault();aSend();}}}});}}
aAddMsg({json.dumps(cfg['greeting'])},false);"""

def build_widget_html(lang, placeholder):
    cfg = LANGUAGES[lang]
    return f"""<div class="assistant-widget">
      <div class="assistant-header">
        <div class="assistant-av"><img src="{cfg['assistant_img']}" alt="{cfg['assistant']}"/></div>
        <div class="assistant-header-text">
          <strong>{cfg['assistant']} — eSolicitors.ie</strong>
          <span>{cfg.get('header_sub', 'Legal intake · Here to help')}</span>
        </div>
        <div class="assistant-online"></div>
      </div>
      <div class="assistant-messages" id="assistantMessages"></div>
      <div class="assistant-input-area">
        <div class="assistant-input-row">
          <textarea id="assistantInput" rows="1" placeholder="{placeholder}"></textarea>
          <button class="assistant-send" onclick="aSend()">
            <svg width="14" height="14" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
          </button>
        </div>
        <div class="assistant-note">{cfg['confidential']}</div>
      </div>
    </div>"""

WIDGET_CSS = """
.assistant-widget{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 32px 64px rgba(0,0,0,.25)}
.assistant-header{background:var(--navy,#0c1f3d);padding:14px 18px;display:flex;align-items:center;gap:12px;border-bottom:1px solid rgba(200,146,42,.2);position:relative}
.assistant-av{width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid var(--gold,#c8922a);flex-shrink:0}
.assistant-av img{width:100%;height:100%;object-fit:cover}
.assistant-header-text strong{display:block;font-size:.88rem;font-weight:600;color:#fff}
.assistant-header-text span{font-size:.75rem;color:rgba(255,255,255,.45)}
.assistant-online{width:8px;height:8px;background:#4ade80;border-radius:50%;position:absolute;right:16px;top:50%;transform:translateY(-50%);animation:apulse 2s infinite}
@keyframes apulse{0%,100%{box-shadow:0 0 0 2px rgba(74,222,128,.25)}50%{box-shadow:0 0 0 6px rgba(74,222,128,.08)}}
.assistant-messages{height:280px;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;scroll-behavior:smooth;background:#f7f3ee}
.assistant-messages::-webkit-scrollbar{width:3px}
.assistant-messages::-webkit-scrollbar-thumb{background:#e2ddd6;border-radius:2px}
.amsg{display:flex;align-items:flex-end;gap:7px}
.amsg.user{flex-direction:row-reverse}
.amsg-av{width:26px;height:26px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1.5px solid var(--gold,#c8922a)}
.amsg-av img{width:100%;height:100%;object-fit:cover}
.amsg-bubble{max-width:78%;padding:9px 12px;border-radius:12px;font-size:.83rem;line-height:1.6}
.amsg.ai .amsg-bubble{background:#fff;color:#0c1f3d;border-bottom-left-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.amsg.user .amsg-bubble{background:#0c1f3d;color:#fff;border-bottom-right-radius:3px}
.a-typing{display:flex;align-items:flex-end;gap:7px}
.a-typing-bubble{background:#fff;border-radius:12px;border-bottom-left-radius:3px;padding:9px 12px;display:flex;gap:3px;align-items:center}
.adot{width:5px;height:5px;background:#bbb;border-radius:50%;animation:abounce 1.2s infinite}
.adot:nth-child(2){animation-delay:.2s}.adot:nth-child(3){animation-delay:.4s}
@keyframes abounce{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-4px)}}
.assistant-input-area{border-top:1px solid #e2ddd6;padding:10px 12px;background:#fff}
.assistant-input-row{display:flex;align-items:center;gap:8px;background:#f7f3ee;border:1px solid #e2ddd6;border-radius:10px;padding:8px 12px;transition:border-color .2s}
.assistant-input-row:focus-within{border-color:var(--gold,#c8922a)}
.assistant-input-row textarea{flex:1;border:none;background:transparent;font-family:'DM Sans',sans-serif;font-size:.83rem;color:#0c1f3d;resize:none;outline:none;line-height:1.5;max-height:70px;overflow-y:auto}
.assistant-input-row textarea::placeholder{color:#bbb}
.assistant-send{width:32px;height:32px;border-radius:7px;background:#0c1f3d;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0;transition:background .2s}
.assistant-send:hover{background:#162d52}
.assistant-note{text-align:center;font-size:.7rem;color:#bbb;margin-top:6px}
.sol-cards{display:flex;flex-direction:column;gap:7px;padding-left:33px}
.sol-card{background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:9px 11px;display:flex;align-items:center;gap:9px;box-shadow:0 2px 8px rgba(15,30,53,.06)}
.sol-av{width:36px;height:36px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1.5px solid #e8e2d9}
.sol-av img{width:100%;height:100%;object-fit:cover}
.sol-info{flex:1}
.sol-name{font-size:12.5px;font-weight:600;color:#0c1f3d}
.sol-area{font-size:10.5px;color:#8896a8;margin-top:1px}
.sol-stars{color:#f5a623;font-size:10px;margin-top:2px}
.sol-badge{background:#0c1f3d;color:#fff;font-size:8.5px;font-weight:600;border-radius:4px;padding:2px 6px;white-space:nowrap}
"""

PAGE_CSS_BASE = """
*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#0c1f3d;--navy-mid:#162d52;--gold:#c8922a;--gold-light:#e8b04a;--cream:#f7f3ee;--cream-dark:#ede7dc;--red:#c0392b;--red-light:#fdf0ee;--green:#1a7a4a;--white:#fff;--text-dark:#0c1f3d;--text-mid:#4a5568;--text-light:#8896a8;--border:#e8e2d9}
html{scroll-behavior:smooth}
body{font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--text-dark);overflow-x:hidden}
nav{position:sticky;top:0;z-index:100;background:var(--navy);border-bottom:1px solid rgba(200,146,42,.2);padding:0 5%;height:62px;display:flex;align-items:center;justify-content:space-between;overflow:hidden}
.logo{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none}.logo span{color:var(--gold)}
.nav-links{display:flex;gap:22px;list-style:none;align-items:center}
.nav-links a{color:rgba(255,255,255,.6);text-decoration:none;font-size:.85rem;font-weight:500;transition:color .2s}
.nav-links a:hover{color:var(--gold-light)}
.nav-cta{background:var(--gold)!important;color:var(--navy)!important;padding:8px 18px;border-radius:6px;font-weight:600!important}
.breadcrumb{background:var(--navy-mid);padding:10px 5%;font-size:.78rem;color:rgba(255,255,255,.4)}
.breadcrumb a{color:rgba(255,255,255,.4);text-decoration:none}.breadcrumb a:hover{color:var(--gold-light)}.breadcrumb span{margin:0 6px}
.hero{background:var(--navy);padding:60px 5% 70px;position:relative;overflow:hidden}
.hero::before{content:'';position:absolute;top:-150px;right:-150px;width:600px;height:600px;background:radial-gradient(circle,rgba(200,146,42,.09) 0%,transparent 70%);pointer-events:none}
.hero-inner{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 380px;gap:60px;align-items:start;position:relative;z-index:1}
.hero-badge{display:inline-flex;align-items:center;gap:7px;background:rgba(200,146,42,.12);border:1px solid rgba(200,146,42,.3);color:var(--gold-light);padding:5px 13px;border-radius:100px;font-size:.72rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:22px}
.hero h1{font-family:'Playfair Display',serif;font-size:clamp(1.9rem,3.8vw,3rem);font-weight:900;color:#fff;line-height:1.1;letter-spacing:-.02em;margin-bottom:18px}
.hero h1 em{font-style:italic;color:var(--gold)}
.hero-intro{font-size:1rem;color:rgba(255,255,255,.6);line-height:1.8;font-weight:300;margin-bottom:28px}
.fact-pills{display:flex;flex-wrap:wrap;gap:10px;margin-top:8px}
.fact-pill{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:10px 14px}
.fact-pill-value{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:var(--gold-light)}
.fact-pill-label{font-size:.7rem;color:rgba(255,255,255,.4);margin-top:2px}
.page-wrap{max-width:1100px;margin:0 auto;padding:0 5%}
.section{padding:56px 0;border-bottom:1px solid var(--border)}.section:last-child{border-bottom:none}
.section-label{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}
.section-title{font-family:'Playfair Display',serif;font-size:clamp(1.4rem,2.5vw,1.9rem);font-weight:700;color:var(--navy);line-height:1.15;letter-spacing:-.02em;margin-bottom:14px}
.body-text{font-size:.95rem;color:var(--text-mid);line-height:1.85;font-weight:300;max-width:720px;margin-bottom:20px}
.warning-box{background:var(--red-light);border:1.5px solid rgba(192,57,43,.2);border-left:4px solid var(--red);border-radius:0 10px 10px 0;padding:18px 20px;margin:24px 0}
.warning-title{font-size:.82rem;font-weight:700;color:var(--red);text-transform:uppercase;letter-spacing:.05em;margin-bottom:6px}
.warning-box p{font-size:.88rem;color:#7a2a20;line-height:1.7}
.cases-grid{display:flex;flex-direction:column;gap:14px;margin-top:24px}
.case-card{background:#fff;border:1px solid var(--border);border-left:3px solid var(--gold);border-radius:0 10px 10px 0;padding:18px;text-decoration:none;display:block;transition:border-color .2s,box-shadow .2s}
.case-card:hover{border-color:rgba(200,146,42,.5);box-shadow:0 4px 16px rgba(12,31,61,.08)}
.case-name{font-size:.87rem;font-weight:700;color:var(--navy);margin-bottom:5px}
.case-desc{font-size:.8rem;color:var(--text-mid);line-height:1.6;margin-bottom:7px}
.case-result{font-size:.75rem;color:var(--green);font-weight:700}
.cta-section{background:var(--navy);padding:60px 5%;text-align:center}
.cta-label{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:12px}
.cta-title{font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:14px;line-height:1.2}
.cta-sub{font-size:.95rem;color:rgba(255,255,255,.6);margin-bottom:32px;line-height:1.7}
footer{background:#080f1e;padding:40px 5% 28px}
.footer-inner{max-width:1100px;margin:0 auto}
.footer-top{display:flex;flex-wrap:wrap;gap:32px;justify-content:space-between;margin-bottom:32px}
.footer-logo{font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none}.footer-logo span{color:var(--gold)}
.footer-desc{font-size:.8rem;color:rgba(255,255,255,.3);margin-top:8px;max-width:240px;line-height:1.6}
.footer-col h4{font-size:.72rem;font-weight:700;letter-spacing:.08em;text-transform:uppercase;color:rgba(255,255,255,.5);margin-bottom:12px}
.footer-col ul{list-style:none;display:flex;flex-direction:column;gap:8px}
.footer-col a{color:rgba(255,255,255,.3);text-decoration:none;font-size:.83rem;transition:color .2s}
.footer-col a:hover{color:var(--gold-light)}
.footer-bottom{border-top:1px solid rgba(255,255,255,.07);padding-top:20px;display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px}
.footer-bottom span{font-size:.72rem;color:rgba(255,255,255,.22)}
@media(max-width:960px){.hero-inner{grid-template-columns:1fr;gap:36px}.nav-links{display:none}}
"""

def generate_topic_content(lang, topic):
    cfg = LANGUAGES[lang]
    system = f"""You write multilingual legal content pages for eSolicitors.ie, an Irish solicitor matching service.
Write in {cfg['name']} ONLY. Be warm, plain, and direct. Writing level: age 12.
STRICT RULES:
- Only write facts true about Irish law — no hallucination
- Reference real Irish laws only (Road Traffic Act, Unfair Dismissals Act, Civil Liability Act, etc.)
- No specific compensation figures unless from real Irish court data
- No made-up statistics
- Maximum 3 short paragraphs per section
- Output ONLY the requested content, no HTML, no markdown"""

    prompt = f"""For this topic: "{topic['title']}"
Search query this page targets: "{topic['search_query']}"
Relevant Irish law: {topic['law']}

Write these 3 sections in {cfg['name']}:
1. INTRO (2-3 sentences): What this situation means in Ireland. Who it affects.
2. CONSEQUENCES (3-4 bullet points): Real legal consequences in Ireland. Each bullet: one consequence, one sentence.
3. FAQ (3 questions + answers): Real questions people ask. Plain answers. No legal advice. Max 2 sentences each.

Format exactly:
INTRO:
[text]

CONSEQUENCES:
- [consequence 1]
- [consequence 2]
- [consequence 3]
- [consequence 4]

FAQ:
Q: [question]
A: [answer]
Q: [question]
A: [answer]
Q: [question]
A: [answer]"""

    return call_claude(prompt, system=system, max_tokens=1500)

def generate_story_content(lang, topic, story):
    cfg = LANGUAGES[lang]
    system = f"""You write short story pages for eSolicitors.ie.
Write in {cfg['name']} ONLY. Warm, plain, human. Age 12 reading level.
STRICT RULES:
- No hallucination — only write plausible situations based on real Irish law
- Do not invent specific figures, dates, or outcomes unless plausible
- No legal advice
- 3-4 paragraphs total across all sections
- Output ONLY the requested content"""

    prompt = f"""Write a story page in {cfg['name']} for eSolicitors.ie.

Person: {story['name']} from {story['city']}
Situation: {story['situation']}
Outcome: {story['outcome']}
Topic area: {topic['title']}
Irish law: {topic['law']}

Write these sections:
1. WHAT_HAPPENED (2 paragraphs): Tell the story in plain {cfg['name']}. What happened, how they felt, why they were worried.
2. WHAT_LAWYER_DID (1-2 paragraphs): What the solicitor examined. What they found or argued. Keep vague enough to not give legal advice.
3. LAW_EXPLAINED (2-3 sentences): Explain the relevant Irish law simply in {cfg['name']}.
4. TIME_WARNING (1-2 sentences): Urgent warning about time limits or deadlines.

Format:
WHAT_HAPPENED:
[text]

WHAT_LAWYER_DID:
[text]

LAW_EXPLAINED:
[text]

TIME_WARNING:
[text]"""

    return call_claude(prompt, system=system, max_tokens=1200)

def build_topic_page(lang, topic, content):
    cfg = LANGUAGES[lang]
    folder = cfg['folder']

    # Parse content sections
    sections = {}
    current = None
    for line in (content or "").split('\n'):
        line = line.strip()
        if line.endswith(':') and line.upper() == line.upper():
            current = line.rstrip(':')
            sections[current] = []
        elif current and line:
            sections[current].append(line)

    intro = ' '.join(sections.get('INTRO', ['']))
    consequences = sections.get('CONSEQUENCES', [])
    faq_lines = sections.get('FAQ', [])

    # Build consequence items
    cons_html = ''
    for c in consequences[:4]:
        c = c.lstrip('- •').strip()
        if c:
            cons_html += f'<div class="consequence-item"><div class="consequence-icon">⚠️</div><div><div class="consequence-desc">{c}</div></div></div>\n'

    # Build FAQ
    faq_html = ''
    i = 0
    while i < len(faq_lines) - 1:
        q = faq_lines[i].lstrip('Q:').strip() if faq_lines[i].startswith('Q:') else ''
        a = faq_lines[i+1].lstrip('A:').strip() if i+1 < len(faq_lines) and faq_lines[i+1].startswith('A:') else ''
        if q and a:
            faq_html += f'<div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">{q} <span class="faq-icon">+</span></button><div class="faq-a">{a}</div></div>\n'
        i += 2

    # Build story cards
    story_cards = ''
    for s in topic['stories']:
        story_url = f"/{folder}/{topic['slug']}/{s['slug']}/"
        story_cards += f'''<a href="{story_url}" class="case-card">
        <div class="case-name">{s['name']}, {s['city']}</div>
        <div class="case-desc">{s['situation']}</div>
        <div class="case-result">✓ {s['outcome']}</div>
      </a>\n'''

    # Build footer links
    other_topics = [t for t in TOPICS.get(lang, []) if t['slug'] != topic['slug']][:4]
    footer_links = '\n'.join([f'<li><a href="/{folder}/{t["slug"]}/">{t["title"]}</a></li>' for t in other_topics])

    widget = build_widget_html(lang, cfg['placeholder'])
    js = build_assistant_js(lang)

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{topic['title']} | eSolicitors.ie</title>
<meta name="description" content="{topic['search_query']} — {topic['title']}. {cfg['cta_label']} eSolicitors.ie.">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<style>
{PAGE_CSS_BASE}
{WIDGET_CSS}
.consequence-list{{display:flex;flex-direction:column;gap:12px;margin-top:20px}}
.consequence-item{{background:#fff;border:1.5px solid var(--border);border-radius:10px;padding:14px 16px;display:flex;gap:12px;align-items:flex-start}}
.consequence-icon{{width:32px;height:32px;background:var(--red-light,#fdf0ee);border-radius:8px;display:flex;align-items:center;justify-content:center;font-size:.9rem;flex-shrink:0}}
.consequence-desc{{font-size:.86rem;color:var(--text-mid);line-height:1.55}}
.faq-list{{display:flex;flex-direction:column;gap:0;margin-top:20px;border:1px solid var(--border);border-radius:10px;overflow:hidden}}
.faq-item{{border-bottom:1px solid var(--border)}}.faq-item:last-child{{border-bottom:none}}
.faq-q{{width:100%;text-align:left;background:#fff;border:none;padding:16px 18px;font-family:'DM Sans',sans-serif;font-size:.88rem;font-weight:600;color:var(--navy);cursor:pointer;display:flex;justify-content:space-between;align-items:center;transition:background .2s}}
.faq-q:hover{{background:var(--cream)}}.faq-icon{{font-size:1.1rem;color:var(--gold);flex-shrink:0;margin-left:12px}}
.faq-a{{display:none;padding:0 18px 16px;font-size:.85rem;color:var(--text-mid);line-height:1.75;background:#fff}}.faq-a.open{{display:block}}
</style>
</head>
<body>
<nav>
  <a href="/" class="logo">e<span>Solicitors</span>.ie</a>
  <ul class="nav-links">
    <li><a href="/{folder}/">{cfg['nav_home']}</a></li>
    <li><a href="/chat.html" class="nav-cta">{cfg['nav_cta']}</a></li>
  </ul>
</nav>
<div class="breadcrumb">
  <a href="/">eSolicitors.ie</a><span>›</span>
  <a href="/{folder}/">{cfg['nav_home']}</a><span>›</span>
  {topic['title']}
</div>
<section class="hero">
  <div class="hero-inner">
    <div>
      <div class="hero-badge">⚖️ {topic['law'][:50]}...</div>
      <h1>{topic['h1']}</h1>
      <p class="hero-intro">{intro}</p>
      <div class="fact-pills">
        <div class="fact-pill"><div class="fact-pill-value">FREE</div><div class="fact-pill-label">{cfg['cta_label']}</div></div>
        <div class="fact-pill"><div class="fact-pill-value">26</div><div class="fact-pill-label">Counties</div></div>
      </div>
    </div>
    {widget}
  </div>
</section>
<div class="page-wrap">
  <section class="section">
    <div class="section-label">⚠️</div>
    <h2 class="section-title">{topic['title']}</h2>
    <div class="consequence-list">
      {cons_html}
    </div>
    <div class="warning-box" style="margin-top:28px">
      <div class="warning-title">⏰ {topic['time_limit']}</div>
      <p>{topic['time_limit']}</p>
    </div>
  </section>
  <section class="section">
    <div class="section-label">Cases</div>
    <h2 class="section-title">{topic.get('cases_title', topic['title'])}</h2>
    <div class="cases-grid">
      {story_cards}
    </div>
  </section>
  <section class="section">
    <div class="section-label">FAQ</div>
    <h2 class="section-title">{topic['title']}</h2>
    <div class="faq-list">
      {faq_html if faq_html else '<div class="faq-item"><button class="faq-q" onclick="toggleFaq(this)">' + topic.get('search_query', '') + ' <span class="faq-icon">+</span></button><div class="faq-a">' + topic.get('law', '') + '</div></div>'}
    </div>
  </section>
</div>
<div class="cta-section">
  <div style="max-width:600px;margin:0 auto">
    <div class="cta-label">{cfg['cta_label']}</div>
    <h2 class="cta-title">{cfg['cta_title']}</h2>
    <p class="cta-sub">{cfg['cta_sub']}</p>
  </div>
</div>
<footer>
  <div class="footer-inner">
    <div class="footer-top">
      <div>
        <a href="/" class="footer-logo">e<span>Solicitors</span>.ie</a>
        <p class="footer-desc">{cfg['footer_disclaimer']}</p>
      </div>
      <div class="footer-col">
        <h4>{cfg['nav_home']}</h4>
        <ul>{footer_links}</ul>
      </div>
      <div class="footer-col">
        <h4>eSolicitors</h4>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/privacy/">Privacy</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 eSolicitors.ie Ltd.</span>
      <span>{cfg['footer_disclaimer']}</span>
    </div>
  </div>
</footer>
<script>
{js}
function toggleFaq(btn){{const a=btn.nextElementSibling;const i=btn.querySelector('.faq-icon');a.classList.toggle('open');i.textContent=a.classList.contains('open')?'−':'+';}}
</script>
</body>
</html>"""
    return html

def build_story_page(lang, topic, story, content):
    cfg = LANGUAGES[lang]
    folder = cfg['folder']

    # Parse content
    sections = {}
    current = None
    for line in (content or "").split('\n'):
        line = line.strip()
        if line.endswith(':') and line.replace('_','').replace(' ','').isupper():
            current = line.rstrip(':')
            sections[current] = []
        elif current and line:
            sections[current].append(line)

    what_happened = ' '.join(sections.get('WHAT_HAPPENED', [story['situation']]))
    what_lawyer = ' '.join(sections.get('WHAT_LAWYER_DID', ['The solicitor examined the case carefully and identified key procedural and legal points in the client\'s favour.']))
    law_explained = ' '.join(sections.get('LAW_EXPLAINED', [topic['law']]))
    time_warning = ' '.join(sections.get('TIME_WARNING', [topic['time_limit']]))

    js = build_assistant_js(lang)
    widget = build_widget_html(lang, cfg['placeholder'])

    html = f"""<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{story['name']}, {story['city']} — {topic['title']} | eSolicitors.ie</title>
<meta name="description" content="{story['situation']} {story['outcome']} — eSolicitors.ie">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
<style>
{PAGE_CSS_BASE}
{WIDGET_CSS}
.story-tag{{display:inline-flex;align-items:center;gap:7px;background:rgba(200,146,42,.12);border:1px solid rgba(200,146,42,.3);color:var(--gold-light);padding:5px 13px;border-radius:100px;font-size:.72rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:20px;text-decoration:none}}
.story-meta{{display:flex;gap:20px;flex-wrap:wrap;margin-top:16px}}
.story-meta-item{{font-size:.8rem;color:rgba(255,255,255,.45);display:flex;align-items:center;gap:6px}}
.story-meta-item strong{{color:rgba(255,255,255,.7);font-weight:600}}
.story-outcome{{display:inline-flex;align-items:center;gap:8px;background:rgba(26,122,74,.15);border:1px solid rgba(26,122,74,.3);color:#4ade80;padding:6px 14px;border-radius:100px;font-size:.78rem;font-weight:700;margin-top:16px}}
.story-text{{font-size:.95rem;color:var(--text-mid);line-height:1.9;font-weight:300}}
.story-text p{{margin-bottom:18px}}.story-text p:last-child{{margin-bottom:0}}
.law-box{{background:#fff;border:1.5px solid var(--border);border-left:4px solid var(--navy);border-radius:0 10px 10px 0;padding:20px 22px;margin-top:20px}}
.law-box-title{{font-size:.78rem;font-weight:700;color:var(--navy);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}}
.law-box p{{font-size:.87rem;color:var(--text-mid);line-height:1.75}}
</style>
</head>
<body>
<nav>
  <a href="/" class="logo">e<span>Solicitors</span>.ie</a>
  <ul class="nav-links">
    <li><a href="/{folder}/">{cfg['nav_home']}</a></li>
    <li><a href="/{folder}/{topic['slug']}/">{topic['title']}</a></li>
    <li><a href="/chat.html" class="nav-cta">{cfg['nav_cta']}</a></li>
  </ul>
</nav>
<div class="breadcrumb">
  <a href="/">eSolicitors.ie</a><span>›</span>
  <a href="/{folder}/">{cfg['nav_home']}</a><span>›</span>
  <a href="/{folder}/{topic['slug']}/">{topic['title']}</a><span>›</span>
  {story['name']}, {story['city']}
</div>
<div style="background:var(--navy);padding:56px 5%;position:relative;overflow:hidden">
  <div style="max-width:800px;margin:0 auto;position:relative;z-index:1">
    <a href="/{folder}/{topic['slug']}/" class="story-tag">← {cfg['back_label']}: {topic['title']}</a>
    <h1 style="font-family:'Playfair Display',serif;font-size:clamp(1.7rem,3.5vw,2.4rem);font-weight:900;color:#fff;line-height:1.15;letter-spacing:-.02em;margin-bottom:12px">{story['situation']}</h1>
    <div class="story-meta">
      <div class="story-meta-item">👤 <strong>{story['name']}</strong> — {story['city']}</div>
    </div>
    <div class="story-outcome">✓ {story['outcome']}</div>
  </div>
</div>
<div style="max-width:800px;margin:0 auto;padding:0 5%">
  <div style="padding:44px 0;border-bottom:1px solid var(--border)">
    <div class="section-label">Story</div>
    <h2 class="section-title">{story['name']}, {story['city']}</h2>
    <div class="story-text"><p>{what_happened}</p></div>
  </div>
  <div style="padding:44px 0;border-bottom:1px solid var(--border)">
    <div class="section-label">Solicitor</div>
    <h2 class="section-title">{topic['title']}</h2>
    <div class="story-text"><p>{what_lawyer}</p></div>
  </div>
  <div style="padding:44px 0;border-bottom:1px solid var(--border)">
    <div class="section-label">Law</div>
    <h2 class="section-title">{topic['law'][:60]}...</h2>
    <div class="law-box">
      <div class="law-box-title">{topic['practice_area'].replace('-', ' ').title()}</div>
      <p>{law_explained}</p>
    </div>
    <div class="warning-box" style="margin-top:20px">
      <div class="warning-title">⏰ Time Limit</div>
      <p>{time_warning}</p>
    </div>
  </div>
</div>
<div style="background:var(--navy);padding:60px 5%;text-align:center">
  <div style="max-width:600px;margin:0 auto;margin-bottom:32px">
    <div class="cta-label">{cfg['cta_label']}</div>
    <h2 class="cta-title">{cfg['cta_title']}</h2>
    <p class="cta-sub">{cfg['cta_sub']}</p>
  </div>
  <div style="max-width:480px;margin:0 auto">
    {widget}
  </div>
</div>
<footer>
  <div class="footer-inner">
    <div class="footer-top">
      <div><a href="/" class="footer-logo">e<span>Solicitors</span>.ie</a></div>
      <div class="footer-col">
        <h4>eSolicitors</h4>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/privacy/">Privacy</a></li>
          <li><a href="/contact/">Contact</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 eSolicitors.ie Ltd.</span>
      <span>{cfg['footer_disclaimer']}</span>
    </div>
  </div>
</footer>
<script>
{js}
</script>
</body>
</html>"""
    return html

def main():
    langs_to_process = os.environ.get("LANGS", "ro,pt-br").split(",")
    generated = 0
    skipped = 0

    for lang in langs_to_process:
        lang = lang.strip()
        if lang not in LANGUAGES:
            print(f"Unknown language: {lang}")
            continue
        if lang not in TOPICS:
            print(f"No topics defined for: {lang} — skipping")
            continue

        cfg = LANGUAGES[lang]
        folder = cfg['folder']
        topics = TOPICS[lang]

        print(f"\n{'='*50}")
        print(f"Processing: {cfg['name']} ({len(topics)} topics)")
        print(f"{'='*50}")

        for topic in topics:
            topic_path = f"./{folder}/{topic['slug']}/index.html"
            os.makedirs(os.path.dirname(topic_path), exist_ok=True)

            if not os.path.exists(topic_path):
                print(f"\n  Topic: {topic['title']}")
                content = generate_topic_content(lang, topic)
                time.sleep(0.5)
                html = build_topic_page(lang, topic, content)
                with open(topic_path, 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"  Saved: {topic_path}")
                generated += 1
            else:
                print(f"  Exists: {topic_path}")
                skipped += 1

            for story in topic['stories']:
                story_path = f"./{folder}/{topic['slug']}/{story['slug']}/index.html"
                os.makedirs(os.path.dirname(story_path), exist_ok=True)

                if not os.path.exists(story_path):
                    print(f"    Story: {story['name']}, {story['city']}")
                    content = generate_story_content(lang, topic, story)
                    time.sleep(0.5)
                    html = build_story_page(lang, topic, story, content)
                    with open(story_path, 'w', encoding='utf-8') as f:
                        f.write(html)
                    print(f"    Saved: {story_path}")
                    generated += 1
                else:
                    print(f"    Exists: {story_path}")
                    skipped += 1

    print(f"\n{'='*50}")
    print(f"Done. Generated: {generated} | Skipped: {skipped}")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
