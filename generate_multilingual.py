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

# Add Polish, Arabic, Spanish, Russian topics (simplified for brevity — generator uses Claude to expand)
# The full topic data for pl, ar, es, ru will be generated dynamically

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
