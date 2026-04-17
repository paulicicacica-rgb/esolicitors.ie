import os
import json
import re
import time
import urllib.request
import urllib.error

API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
MODEL = "claude-haiku-4-5-20251001"

# ─────────────────────────────────────────
# SARAH CONFIG PER LANGUAGE
# ─────────────────────────────────────────
SARAH_CONFIG = {
    "en": {
        "name": "Sarah",
        "img": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face",
        "greeting": "Hi, I'm Sarah from eSolicitors.ie. Tell me what you need help with — everything can be handled remotely.",
        "placeholder": "Tell me what happened or what you need...",
        "note": "Confidential · Free · No obligation",
        "system": "You are Sarah, a warm intake assistant for eSolicitors.ie. This person is contacting from OUTSIDE Ireland. Make clear you work with international clients and everything can be handled remotely. Be warm and human. Ask about their situation, then collect name and phone. No legal advice. Respond in English. Respond ONLY with JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "CO", "name": "Ciara O'Brien", "area": "Probate & Property", "county": "Dublin"},
            {"initials": "MF", "name": "Michael Fitzgerald", "area": "Citizenship & Immigration", "county": "Cork"},
            {"initials": "SG", "name": "Sinead Gallagher", "area": "International Clients", "county": "Galway"},
        ]
    },
    "ro": {
        "name": "Mirela",
        "img": "https://images.unsplash.com/photo-1573496359142-b8d87734a5a2?w=80&h=80&fit=crop&crop=face",
        "greeting": "Bună, sunt Mirela de la eSolicitors.ie. Spune-mi cu ce ai nevoie — totul se poate rezolva de la distanță.",
        "placeholder": "Spune-mi cu ce te putem ajuta...",
        "note": "Confidențial · Gratuit · Fără obligații",
        "system": "Ești Mirela, o asistentă caldă de la eSolicitors.ie. Această persoană contactează din afara Irlandei. Răspunde în ROMÂNĂ. Fii caldă și umană. Întreabă despre situație, colectează nume și telefon. Fără sfaturi juridice. Răspunde DOAR cu JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "IP", "name": "Ioan Popescu", "area": "Cetățenie & Proprietate", "county": "Dublin"},
            {"initials": "MC", "name": "Maria Constantin", "area": "Probate & Moșteniri", "county": "Cork"},
            {"initials": "CO", "name": "Ciara O'Brien", "area": "Clienți Internaționali", "county": "Galway"},
        ]
    },
    "pt-br": {
        "name": "Ana",
        "img": "https://images.unsplash.com/photo-1531746020798-e6953c6e8e04?w=80&h=80&fit=crop&crop=face",
        "greeting": "Olá, sou Ana da eSolicitors.ie. Me conta o que você precisa — tudo pode ser resolvido à distância.",
        "placeholder": "Me conta o que aconteceu ou o que você precisa...",
        "note": "Confidencial · Gratuito · Sem compromisso",
        "system": "Você é Ana, uma assistente calorosa da eSolicitors.ie. Esta pessoa está contactando de FORA da Irlanda. Responda em PORTUGUÊS BRASILEIRO. Seja calorosa e humana. Pergunte sobre a situação, colete nome e telefone. Sem conselhos jurídicos. Responda APENAS com JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "CS", "name": "Carlos Silva", "area": "Cidadania & Imigração", "county": "Dublin"},
            {"initials": "AR", "name": "Ana Rodrigues", "area": "Herança & Propriedade", "county": "Cork"},
            {"initials": "CO", "name": "Ciara O'Brien", "area": "Clientes Internacionais", "county": "Galway"},
        ]
    },
    "es": {
        "name": "Carmen",
        "img": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop&crop=face",
        "greeting": "Hola, soy Carmen de eSolicitors.ie. Cuéntame qué necesitas — todo se puede gestionar a distancia.",
        "placeholder": "Cuéntame qué pasó o qué necesitas...",
        "note": "Confidencial · Gratuito · Sin compromiso",
        "system": "Eres Carmen, una asistente cálida de eSolicitors.ie. Esta persona contacta desde FUERA de Irlanda. Responde en ESPAÑOL. Sé cálida y humana. Pregunta sobre la situación, recoge nombre y teléfono. Sin consejos legales. Responde SOLO con JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "CG", "name": "Carlos García", "area": "Ciudadanía & Inmigración", "county": "Dublin"},
            {"initials": "ML", "name": "María López", "area": "Herencia & Propiedad", "county": "Cork"},
            {"initials": "CO", "name": "Ciara O'Brien", "area": "Clientes Internacionales", "county": "Galway"},
        ]
    },
    "pl": {
        "name": "Kasia",
        "img": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop&crop=face",
        "greeting": "Cześć, jestem Kasia z eSolicitors.ie. Powiedz mi czego potrzebujesz — wszystko można załatwić zdalnie.",
        "placeholder": "Powiedz mi co się stało lub czego potrzebujesz...",
        "note": "Poufnie · Bezpłatnie · Bez zobowiązań",
        "system": "Jesteś Kasią, ciepłą asystentką z eSolicitors.ie. Ta osoba kontaktuje się spoza Irlandii. Odpowiadaj PO POLSKU. Bądź ciepła i ludzka. Zapytaj o sytuację, zbierz imię i telefon. Bez porad prawnych. Odpowiadaj TYLKO JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "MK", "name": "Marek Kowalski", "area": "Nieruchomości & Prawo", "county": "Dublin"},
            {"initials": "AW", "name": "Anna Wiśniewska", "area": "Spadki & Testamenty", "county": "Cork"},
            {"initials": "DM", "name": "Declan Murphy", "area": "Klienci Zagraniczni", "county": "Galway"},
        ]
    },
    "ar": {
        "name": "ليلى",
        "img": "https://images.unsplash.com/photo-1607746882042-944635dfe10e?w=80&h=80&fit=crop&crop=face",
        "greeting": "مرحباً، أنا ليلى من eSolicitors.ie. أخبرني بما تحتاجه — يمكن التعامل مع كل شيء عن بُعد.",
        "placeholder": "أخبرني بما حدث أو ما تحتاجه...",
        "note": "سري · مجاني · بدون التزام",
        "system": "أنت ليلى، مساعدة دافئة من eSolicitors.ie. هذا الشخص يتواصل من خارج أيرلندا. أجيبي باللغة العربية. كوني دافئة وإنسانية. اسألي عن الوضع، اجمعي الاسم ورقم الهاتف. بدون نصائح قانونية. أجيبي فقط بـ JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "أح", "name": "أحمد حسن", "area": "الجنسية والهجرة", "county": "Dublin"},
            {"initials": "فر", "name": "فاطمة الرشيد", "area": "الميراث والعقارات", "county": "Cork"},
            {"initials": "DM", "name": "Declan Murphy", "area": "العملاء الدوليون", "county": "Galway"},
        ]
    },
    "ru": {
        "name": "Наташа",
        "img": "https://images.unsplash.com/photo-1508214751196-bcfd4ca60f91?w=80&h=80&fit=crop&crop=face",
        "greeting": "Привет, я Наташа из eSolicitors.ie. Расскажи мне что тебе нужно — всё можно решить дистанционно.",
        "placeholder": "Расскажи что случилось или что тебе нужно...",
        "note": "Конфиденциально · Бесплатно · Без обязательств",
        "system": "Ты Наташа, тёплая ассистентка из eSolicitors.ie. Этот человек обращается из-за пределов Ирландии. Отвечай по-русски. Будь тёплой и человечной. Спроси о ситуации, собери имя и телефон. Без юридических советов. Отвечай ТОЛЬКО JSON: {\"message\":\"...\",\"next_stage\":\"details|name|phone|done\"}",
        "solicitors": [
            {"initials": "АП", "name": "Алексей Петров", "area": "Гражданство & Иммиграция", "county": "Dublin"},
            {"initials": "НС", "name": "Наталья Соколова", "area": "Наследство & Недвижимость", "county": "Cork"},
            {"initials": "CO", "name": "Ciara O'Brien", "area": "Иностранные клиенты", "county": "Galway"},
        ]
    }
}

# ─────────────────────────────────────────
# ALL 107 PAGES TO GENERATE
# ─────────────────────────────────────────
PAGES = [
    # ═══════════════════════════════════════
    # ENGLISH — DEEP (citizenship + inheritance)
    # ═══════════════════════════════════════
    {
        "path": "./irish-citizenship-by-descent/index.html",
        "lang": "en", "type": "hub",
        "title": "Irish Citizenship by Descent — Claim Your Irish Passport",
        "meta": "Entitled to Irish citizenship through a parent or grandparent? Find out how to claim and get matched with a specialist solicitor. Free consultation.",
        "h1": "You may already be\nan Irish citizen.\n<em>You just need to prove it.</em>",
        "intro": "If you have an Irish parent or grandparent, you may be entitled to Irish citizenship — and an EU passport — regardless of where you were born or where you live. The process takes time and requires precise legal documentation. A specialist solicitor makes the difference between success and years of delays.",
        "search_query": "irish citizenship by descent grandparent solicitor",
        "law": "Irish Nationality and Citizenship Acts 1956-2004 — citizenship passes through blood to children and grandchildren of Irish citizens",
        "audience": "international",
        "stories": [
            {"slug": "james-usa", "name": "James", "location": "Boston, USA", "situation": "James had an Irish grandfather from Cork but had no idea how to prove the connection or what documents he needed. He had tried twice himself and been rejected.", "outcome": "Irish passport received — full EU citizenship", "law_note": "Foreign Birth Registration required for grandchildren — must prove the chain of citizenship through documentation"},
            {"slug": "maria-argentina", "name": "María", "location": "Buenos Aires, Argentina", "situation": "María's great-grandparents left Kerry in the 1920s. She believed she was entitled to citizenship but didn't know if the entitlement extended to her generation.", "outcome": "Citizenship confirmed — passport issued within 14 months", "law_note": "Citizenship through great-grandparent requires the grandparent to have been registered first — a two-step process"},
            {"slug": "aoife-australia", "name": "Aoife", "location": "Sydney, Australia", "situation": "Born in Australia to an Irish mother who had never registered her own birth abroad. The citizenship chain was broken. The solicitor found a way through.", "outcome": "Mother registered first, Aoife's citizenship confirmed", "law_note": "Foreign Birth Registration must be completed in order — parent first, then child"},
            {"slug": "padraig-canada", "name": "Pádraig", "location": "Toronto, Canada", "situation": "Had all the documents but his application was rejected twice with no clear reason given. A solicitor identified an error in how the Irish birth certificate was being interpreted.", "outcome": "Application resubmitted and approved — third attempt successful", "law_note": "Common rejection reasons include incorrect document certification and errors in reading pre-1900 birth records"},
            {"slug": "clara-brazil", "name": "Clara", "location": "São Paulo, Brazil", "situation": "Clara's Irish grandfather had left Ireland at 18 with no documentation. Tracing the records required genealogical research through the General Register Office.", "outcome": "Records found — citizenship confirmed", "law_note": "The General Register Office holds Irish civil registration records from 1864 — a solicitor can assist with tracing and obtaining certified copies"},
            {"slug": "sean-uk", "name": "Seán", "location": "London, UK", "situation": "Post-Brexit, Seán realised his Irish grandmother gave him an automatic entitlement to an EU passport. He had never looked into it before.", "outcome": "Passport in hand within 11 months", "law_note": "Children of Irish citizens born abroad are automatically Irish — no registration required if born after the parent's registration"},
        ]
    },
    {
        "path": "./inheriting-property-ireland-from-abroad/index.html",
        "lang": "en", "type": "hub",
        "title": "Inheriting Property in Ireland from Abroad — What to Do",
        "meta": "Inherited a house or land in Ireland but you live abroad? Find out how Irish probate works for non-residents and get specialist legal help.",
        "h1": "You've inherited property\nin Ireland.\n<em>Here's what happens next.</em>",
        "intro": "Inheriting property or money in Ireland when you live abroad is more complicated than a domestic inheritance. Irish probate law applies regardless of where you live — and the process involves the Irish courts, Irish tax obligations, and often a property that needs to be sold or transferred. A solicitor handles all of it on your behalf, remotely.",
        "search_query": "inherited property ireland from abroad solicitor probate",
        "law": "Succession Act 1965 — Irish law governs the distribution of Irish assets regardless of where the deceased or beneficiaries live",
        "audience": "international",
        "stories": [
            {"slug": "margaret-uk", "name": "Margaret", "location": "Birmingham, UK", "situation": "Margaret inherited her father's house in Mayo when she had lived in England for 30 years. She had no idea how Irish probate worked or what taxes applied.", "outcome": "Probate granted — house sold, proceeds transferred to UK", "law_note": "Irish Capital Acquisitions Tax (CAT) applies to Irish property inherited by non-residents — thresholds depend on the relationship to the deceased"},
            {"slug": "patrick-usa", "name": "Patrick", "location": "New York, USA", "situation": "Patrick was named executor of his aunt's estate in Galway but had never been executor before and lived in the US. The estate included a house, land, and a bank account.", "outcome": "Grant of probate obtained — estate fully administered remotely", "law_note": "A non-resident executor can appoint an Irish solicitor to act as their agent throughout the probate process"},
            {"slug": "brigid-australia", "name": "Brigid", "location": "Melbourne, Australia", "situation": "No will had been left. Three siblings in three different countries all had a claim on the Irish property. The family disagreed on whether to sell or keep it.", "outcome": "Intestacy rules applied — property sold by agreement", "law_note": "Where there is no will in Ireland, the Succession Act 1965 determines how the estate is divided — a solicitor can mediate between beneficiaries"},
            {"slug": "liam-canada", "name": "Liam", "location": "Vancouver, Canada", "situation": "Liam's Irish cousin had been promised the house verbally but there was no will. Another family member had taken possession of the property.", "outcome": "Court order obtained — rightful beneficiary protected", "law_note": "Verbal promises about property in Ireland are generally not legally binding — the Succession Act governs who inherits"},
        ]
    },
    # ═══════════════════════════════════════
    # ENGLISH — MEDIUM
    # ═══════════════════════════════════════
    {
        "path": "./buying-property-ireland-from-abroad/index.html",
        "lang": "en", "type": "hub",
        "title": "Buying Property in Ireland from Abroad — Solicitor Guide",
        "meta": "Want to buy a house or apartment in Ireland but you live abroad? A solicitor handles the legal side from start to finish. Find out how it works.",
        "h1": "Buying property in Ireland\nfrom abroad.\n<em>It's more straightforward than you think.</em>",
        "intro": "Non-residents can buy property in Ireland with no restrictions. But Irish conveyancing — the legal process of transferring ownership — must be handled by an Irish solicitor. The good news is the entire process can be done remotely. You never need to be in Ireland.",
        "search_query": "buying house ireland from abroad non-resident solicitor",
        "law": "There are no restrictions on non-residents purchasing property in Ireland. Conveyancing is governed by Irish contract law and the Land Registry.",
        "audience": "international",
        "stories": [
            {"slug": "thomas-uk", "name": "Thomas", "location": "London, UK", "situation": "Thomas wanted to buy a holiday home in Kerry but had never bought property before and didn't understand how the Irish system differed from England.", "outcome": "Purchase completed — keys handed over remotely", "law_note": "Unlike England, Irish property law requires a solicitor for all conveyancing — the process typically takes 8-12 weeks"},
            {"slug": "anna-usa", "name": "Anna", "location": "Chicago, USA", "situation": "Anna was returning to Ireland after 20 years and wanted to buy before she arrived. She needed a solicitor who could handle everything while she was still in the US.", "outcome": "Sale agreed and completed before Anna's return flight", "law_note": "A Power of Attorney allows your Irish solicitor to sign documents on your behalf — useful for buyers abroad"},
            {"slug": "carlos-spain", "name": "Carlos", "location": "Madrid, Spain", "situation": "Carlos saw Ireland as a stable EU investment and wanted to buy an apartment in Dublin. His main concern was understanding the Irish tax position as a non-resident landlord.", "outcome": "Purchase completed — tax structure set up correctly from day one", "law_note": "Non-resident landlords in Ireland must register with Revenue and may appoint a collection agent — your solicitor can advise on this"},
        ]
    },
    {
        "path": "./set-up-company-ireland-from-abroad/index.html",
        "lang": "en", "type": "hub",
        "title": "Set Up an Irish Company from Abroad — Solicitor Guide",
        "meta": "Want to register a company in Ireland? EU market access, favourable tax rates, and no need to be present. Find out how a solicitor helps.",
        "h1": "Set up an Irish company\nfrom anywhere in the world.\n<em>EU base. 12.5% corporation tax.</em>",
        "intro": "Ireland offers one of the most business-friendly environments in the EU — 12.5% corporation tax, English language, and full access to the EU single market. You don't need to be Irish or live in Ireland to form an Irish company. But you do need an Irish solicitor to ensure it's done correctly.",
        "search_query": "set up irish company from abroad solicitor non-resident",
        "law": "Companies Act 2014 — Irish companies must have at least one EEA-resident director, or post a bond. A solicitor can arrange an EEA-resident nominee director if needed.",
        "audience": "international",
        "stories": [
            {"slug": "david-uk", "name": "David", "location": "Manchester, UK", "situation": "Post-Brexit, David needed an EU entity for his consultancy business. He chose Ireland for the language and tax rate. The solicitor handled everything in 2 weeks.", "outcome": "Company registered — trading in Ireland within 3 weeks", "law_note": "A private limited company (Ltd) in Ireland requires at least one director — if no director is EEA-resident, a bond of €25,000 is required or a nominee director arranged"},
            {"slug": "yuki-japan", "name": "Yuki", "location": "Tokyo, Japan", "situation": "Yuki's tech startup wanted an EU base for GDPR compliance and EU customer contracts. Ireland was the logical choice. No need to relocate.", "outcome": "Irish subsidiary registered — EU contracts signed within a month", "law_note": "Non-EU founders can register an Irish company — the EEA director requirement can be met through a nominee arrangement"},
            {"slug": "ana-brazil2", "name": "Ana", "location": "Rio de Janeiro, Brazil", "situation": "Ana wanted to sell software to European clients and needed an EU entity. Her Irish-Brazilian background made Ireland the natural choice.", "outcome": "Company operational — VAT registered and trading", "law_note": "Irish companies must register for VAT once turnover exceeds €37,500 for services — a solicitor can advise on the right structure"},
        ]
    },
    {
        "path": "./tourist-accident-ireland-claim/index.html",
        "lang": "en", "type": "hub",
        "title": "Had an Accident in Ireland as a Tourist? You Can Still Claim",
        "meta": "Injured in Ireland while visiting? You have the same right to compensation as an Irish resident. Time limits apply. Find out what to do.",
        "h1": "Injured in Ireland\nas a visitor.\n<em>You have the same rights as anyone else.</em>",
        "intro": "If you were injured in Ireland while visiting — whether in a hotel, on a tour, in a shop, or in a road accident — you have exactly the same rights to compensation as an Irish resident. The claim is made through the Irish courts or Personal Injuries Assessment Board. You don't need to be in Ireland to pursue it.",
        "search_query": "accident injury in ireland tourist visitor can i claim compensation",
        "law": "Civil Liability Act — the right to personal injury compensation applies to anyone injured on Irish soil, regardless of nationality or residence",
        "audience": "international",
        "stories": [
            {"slug": "helen-uk2", "name": "Helen", "location": "Edinburgh, UK", "situation": "Helen slipped on a wet floor in a Dublin hotel and fractured her wrist. She flew home the next day and assumed she couldn't do anything from Scotland.", "outcome": "Claim filed in Ireland — settlement of €22,000", "law_note": "Personal injury claims in Ireland have a 2-year time limit — you can pursue a claim from abroad through an Irish solicitor"},
            {"slug": "marco-italy", "name": "Marco", "location": "Milan, Italy", "situation": "Marco was on a cycling tour in Kerry when a car hit him. The driver had Irish insurance. Marco was back in Italy within a week.", "outcome": "Claim pursued against Irish insurer — full compensation", "law_note": "Road traffic accident claims in Ireland are handled through the Irish insurance system regardless of where the victim lives"},
            {"slug": "jennifer-usa2", "name": "Jennifer", "location": "Boston, USA", "situation": "Jennifer was on a heritage tour when she fell on a broken footpath maintained by a local council. She had travel insurance but was told it didn't cover the full loss.", "outcome": "Separate personal injury claim — €18,000 in addition to travel insurance", "law_note": "Travel insurance and personal injury claims are separate — you can pursue both simultaneously"},
        ]
    },
    {
        "path": "./child-custody-ireland-international/index.html",
        "lang": "en", "type": "hub",
        "title": "International Child Custody Disputes Involving Ireland",
        "meta": "One parent in Ireland, one abroad? Child taken to Ireland without consent? Get specialist legal help immediately.",
        "h1": "Cross-border child custody\nand Ireland.\n<em>Act quickly. Time matters.</em>",
        "intro": "When one parent is in Ireland and the other is abroad, child custody disputes become international legal matters. Ireland is a signatory to the Hague Convention on International Child Abduction. If a child has been taken to Ireland without your consent, or if you are trying to move to Ireland with your children, an Irish solicitor is essential.",
        "search_query": "child custody dispute one parent ireland international solicitor",
        "law": "Child Abduction and Enforcement of Custody Orders Act 1991 — Ireland's implementation of the Hague Convention. The best interests of the child are paramount under Irish family law.",
        "audience": "international",
        "stories": [
            {"slug": "robert-uk2", "name": "Robert", "location": "London, UK", "situation": "Robert's ex-partner moved to Ireland with their daughter without his consent. He had joint custody in the UK. He needed to act within weeks to use the Hague Convention.", "outcome": "Hague application filed — child returned under court order within 6 weeks", "law_note": "Hague Convention applications must be made within 1 year of the wrongful removal for the strongest legal protection"},
            {"slug": "sophie-france", "name": "Sophie", "location": "Paris, France", "situation": "Sophie moved to Ireland with her children after separating from her Irish partner. He was pursuing a French court order. She needed Irish legal representation.", "outcome": "Irish courts determined jurisdiction — Sophie's position protected", "law_note": "Where parents are in different countries, determining which court has jurisdiction is the first critical step"},
            {"slug": "michael-usa3", "name": "Michael", "location": "New York, USA", "situation": "Michael's Irish wife wanted to relocate to Ireland with their two children. He lived in New York and didn't want to lose regular contact.", "outcome": "Relocation permitted — detailed access arrangement set out by Irish court", "law_note": "Irish courts can permit relocation while ordering detailed access arrangements including regular visits and video contact"},
        ]
    },
    {
        "path": "./divorce-one-spouse-ireland/index.html",
        "lang": "en", "type": "hub",
        "title": "Divorce When One Spouse is in Ireland — What You Need to Know",
        "meta": "Married to an Irish person or have property in Ireland? Find out how Irish divorce law works for international couples.",
        "h1": "Divorce when one spouse\nis in Ireland.\n<em>Irish law may apply to you.</em>",
        "intro": "If you or your spouse has been living in Ireland, or if you own property in Ireland, Irish divorce law may apply to your situation — even if you live abroad. Irish courts have jurisdiction when either spouse is domiciled in Ireland or has been ordinarily resident here for at least a year.",
        "search_query": "divorce one spouse in ireland international cross border solicitor",
        "law": "Family Law (Divorce) Act 1996 — Irish courts have jurisdiction where either spouse is domiciled in Ireland or has been ordinarily resident for 1 year",
        "audience": "international",
        "stories": [
            {"slug": "claire-uk3", "name": "Claire", "location": "Manchester, UK", "situation": "Claire was Irish but had lived in the UK for 15 years. She and her UK-based husband had bought a house in Ireland. She needed to understand which country's divorce law applied.", "outcome": "Divorced in Ireland — Irish property divided in proceedings", "law_note": "Where there is property in Ireland, it is often more practical to divorce in Ireland so the Irish property can be dealt with in the same proceedings"},
            {"slug": "pierre-france2", "name": "Pierre", "location": "Lyon, France", "situation": "Pierre's Irish wife had returned to Ireland with the children. He had been living in France. He needed to know if the Irish divorce would affect his French pension.", "outcome": "Irish divorce granted — pension issue resolved through cross-border agreement", "law_note": "Irish courts can make pension adjustment orders on Irish pensions — French pensions would be dealt with separately"},
        ]
    },
    {
        "path": "./irish-will-from-abroad/index.html",
        "lang": "en", "type": "hub",
        "title": "Making an Irish Will from Abroad — Non-Resident Estate Planning",
        "meta": "Own property or assets in Ireland but live abroad? An Irish will ensures your Irish assets are distributed as you intend. Find out how.",
        "h1": "Own assets in Ireland\nbut live abroad?\n<em>You need an Irish will.</em>",
        "intro": "If you own property, land, or other assets in Ireland, you should have an Irish will that specifically covers those assets. Without one, Irish intestacy law determines what happens — and it may not match your wishes. An Irish will can be drafted and executed remotely.",
        "search_query": "make irish will from abroad non-resident property assets solicitor",
        "law": "Succession Act 1965 — a valid will in Ireland must be in writing, signed in the presence of two witnesses. Irish assets should ideally be covered by an Irish will even if a foreign will exists.",
        "audience": "international",
        "stories": [
            {"slug": "elizabeth-uk4", "name": "Elizabeth", "location": "Bristol, UK", "situation": "Elizabeth owned a cottage in Clare that she had inherited from her mother. She had an English will but had been advised that a separate Irish will would protect her wishes.", "outcome": "Irish will drafted — assets clearly protected", "law_note": "Having separate wills for assets in different countries avoids potential conflicts between legal systems and speeds up probate"},
            {"slug": "john-usa4", "name": "John", "location": "San Francisco, USA", "situation": "John owned a share of a farm in Tipperary with two siblings. He wanted to leave his share to his son, not his siblings. Without a will, Irish intestacy rules would apply.", "outcome": "Will drafted — son's inheritance protected", "law_note": "Without a will, Irish assets pass under the Succession Act — this may not reflect your wishes especially for jointly owned property"},
        ]
    },
    # ═══════════════════════════════════════
    # ENGLISH — SHALLOW (single pages)
    # ═══════════════════════════════════════
    {
        "path": "./arrested-ireland-tourist/index.html",
        "lang": "en", "type": "shallow",
        "title": "Arrested in Ireland as a Tourist — Get Legal Help Immediately",
        "meta": "Arrested or detained in Ireland while visiting? You have the right to a solicitor. Find out what to do right now.",
        "h1": "Arrested in Ireland\nas a visitor.\n<em>You have rights. Use them.</em>",
        "intro": "If you are arrested or detained by the Gardaí in Ireland, you have an immediate right to contact a solicitor — regardless of your nationality. Do not answer questions without legal representation. An Irish solicitor can be with you or advising you by phone within hours.",
        "search_query": "arrested ireland tourist visitor right to solicitor",
        "law": "Criminal Justice Act 1984 — anyone detained in Ireland has the right to consult a solicitor before being questioned",
        "audience": "international"
    },
    {
        "path": "./remote-worker-ireland-employment-dispute/index.html",
        "lang": "en", "type": "shallow",
        "title": "Remote Worker Dispute with Irish Employer — Your Rights",
        "meta": "Working remotely for an Irish company and having employment issues? Irish employment law may protect you even if you live abroad.",
        "h1": "Working remotely for\nan Irish employer.\n<em>Irish employment law may protect you.</em>",
        "intro": "If you work for an Irish company, Irish employment law may apply to your employment — even if you work from another country. Unfair dismissal, unpaid wages, and contract disputes can all be pursued through the Irish Workplace Relations Commission in certain circumstances.",
        "search_query": "remote worker irish employer employment dispute rights",
        "law": "Workplace Relations Acts — jurisdiction depends on where the work is performed and where the employer is based",
        "audience": "international"
    },
    {
        "path": "./contract-dispute-irish-company/index.html",
        "lang": "en", "type": "shallow",
        "title": "Contract Dispute with an Irish Company — How to Pursue It",
        "meta": "In a contract dispute with an Irish company? Find out how to enforce your rights through the Irish courts from abroad.",
        "h1": "Contract dispute with\nan Irish company.\n<em>You can pursue it from anywhere.</em>",
        "intro": "If an Irish company has breached a contract with you, failed to pay, or delivered defective goods or services, you have legal options — even if you're based abroad. Irish courts deal with commercial disputes regularly and a solicitor can pursue your claim on your behalf.",
        "search_query": "contract dispute irish company from abroad solicitor",
        "law": "Irish contract law — breach of contract claims can be pursued in the Irish courts. EU regulations on jurisdiction and enforcement apply to EU-based claimants.",
        "audience": "international"
    },
    # ═══════════════════════════════════════
    # PORTUGUESE (BR) — CITIZENSHIP
    # ═══════════════════════════════════════
    {
        "path": "./pt-br/cidadania-irlandesa-pelo-avo/index.html",
        "lang": "pt-br", "type": "hub",
        "title": "Cidadania Irlandesa pelo Avô ou Bisavô — Guia Completo",
        "meta": "Tem ascendência irlandesa? Você pode ter direito à cidadania irlandesa e ao passaporte europeu. Saiba como com ajuda de um advogado especializado.",
        "h1": "Você pode já ser\ncidadão irlandês.\n<em>Só precisa provar.</em>",
        "intro": "Se você tem um avô ou bisavô irlandês, pode ter direito à cidadania irlandesa — e com ela, um passaporte europeu com livre circulação em 27 países. O processo exige documentação precisa e conhecimento da lei irlandesa. Um advogado especializado faz a diferença entre o sucesso e anos de atrasos.",
        "search_query": "cidadania irlandesa pelo avô brasil como solicitar advogado",
        "law": "Irish Nationality and Citizenship Acts 1956-2004 — a cidadania irlandesa passa por laço de sangue para filhos e netos de cidadãos irlandeses",
        "audience": "international",
        "stories": [
            {"slug": "joao-sao-paulo", "name": "João", "location": "São Paulo, Brasil", "situation": "João tinha um avô de Cork que emigrou para o Brasil nos anos 1940. Tinha fotos e cartas mas não sabia quais documentos precisava para provar a cidadania.", "outcome": "Passaporte irlandês recebido — cidadania europeia confirmada", "law_note": "O Registro de Nascimento no Exterior é exigido para netos — é preciso provar a cadeia de cidadania através de documentação"},
            {"slug": "ana-rio", "name": "Ana", "location": "Rio de Janeiro, Brasil", "situation": "A bisavó de Ana era de Kerry. Ela acreditava ter direito à cidadania mas não sabia se a entitlement chegava à sua geração.", "outcome": "Cidadania confirmada — passaporte emitido em 16 meses", "law_note": "Cidadania através de bisavô requer que o avô tenha sido registrado primeiro — é um processo em duas etapas"},
            {"slug": "pedro-porto-alegre", "name": "Pedro", "location": "Porto Alegre, Brasil", "situation": "Pedro tinha todos os documentos mas seu pedido foi rejeitado duas vezes sem explicação clara. O advogado identificou um erro na certidão de nascimento irlandesa.", "outcome": "Pedido reapresentado e aprovado na terceira tentativa", "law_note": "Motivos comuns de rejeição incluem certificação incorreta de documentos e erros na leitura de registros anteriores a 1900"},
            {"slug": "lucia-belo-horizonte", "name": "Lúcia", "location": "Belo Horizonte, Brasil", "situation": "O avô irlandês de Lúcia havia saído da Irlanda aos 17 anos sem documentação. Rastrear os registros exigiu pesquisa genealógica no General Register Office.", "outcome": "Registros encontrados — cidadania confirmada", "law_note": "O General Register Office da Irlanda mantém registros de nascimento desde 1864 — um advogado pode ajudar a rastrear e obter cópias certificadas"},
        ]
    },
    {
        "path": "./pt-br/heranca-irlanda-do-exterior/index.html",
        "lang": "pt-br", "type": "hub",
        "title": "Herança na Irlanda Morando no Exterior — O Que Fazer",
        "meta": "Herdou uma casa ou dinheiro na Irlanda mas mora fora? Saiba como funciona o inventário irlandês para não-residentes.",
        "h1": "Você herdou\nbens na Irlanda.\n<em>Veja o que acontece agora.</em>",
        "intro": "Herdar bens na Irlanda morando no exterior é mais complexo do que uma herança local. A lei irlandesa de inventário se aplica independente de onde você mora — e o processo envolve os tribunais irlandeses, obrigações fiscais irlandesas, e muitas vezes um imóvel que precisa ser vendido ou transferido. Um advogado cuida de tudo isso por você, à distância.",
        "search_query": "herança irlanda brasil como receber inventário advogado",
        "law": "Succession Act 1965 — a lei irlandesa rege a distribuição de ativos irlandeses independente de onde o falecido ou os beneficiários vivem",
        "audience": "international",
        "stories": [
            {"slug": "maria-recife", "name": "Maria", "location": "Recife, Brasil", "situation": "Maria herdou a casa do avô em Galway mas morava no Brasil há toda a vida. Não sabia como funcionava o inventário irlandês nem quais impostos se aplicavam.", "outcome": "Inventário concluído — casa vendida, valor transferido ao Brasil", "law_note": "O Capital Acquisitions Tax (CAT) irlandês se aplica a imóveis irlandeses herdados por não-residentes — as isenções dependem do grau de parentesco"},
            {"slug": "roberto-manaus", "name": "Roberto", "location": "Manaus, Brasil", "situation": "Roberto foi nomeado executor do espólio do tio em Cork mas nunca tinha sido executor e morava no Brasil. O espólio incluía uma casa, terra e conta bancária.", "outcome": "Inventário concedido — espólio administrado totalmente à distância", "law_note": "Um executor não-residente pode nomear um advogado irlandês como representante durante todo o processo"},
        ]
    },
    {
        "path": "./pt-br/abrir-empresa-irlanda/index.html",
        "lang": "pt-br", "type": "hub",
        "title": "Abrir Empresa na Irlanda Morando no Brasil — Guia Completo",
        "meta": "Quer registrar uma empresa na Irlanda? Acesso ao mercado europeu, imposto de 12,5% e sem precisar morar lá. Saiba como.",
        "h1": "Abra uma empresa\nna Irlanda de onde você estiver.\n<em>Acesso à UE. 12,5% de imposto.</em>",
        "intro": "A Irlanda oferece um dos ambientes mais favoráveis para negócios na UE — 12,5% de imposto corporativo, idioma inglês e acesso total ao mercado único europeu. Você não precisa ser irlandês nem morar na Irlanda para constituir uma empresa irlandesa. Mas precisa de um advogado irlandês para fazer tudo certo.",
        "search_query": "abrir empresa na irlanda do brasil advogado guia",
        "law": "Companies Act 2014 — empresas irlandesas precisam ter ao menos um diretor residente no EEE, ou depositar uma garantia de €25.000",
        "audience": "international",
        "stories": [
            {"slug": "fernando-curitiba", "name": "Fernando", "location": "Curitiba, Brasil", "situation": "Fernando tinha uma startup de tecnologia e precisava de uma entidade europeia para contratos com clientes da UE e conformidade com o GDPR. Escolheu a Irlanda pelo idioma e tributação.", "outcome": "Empresa registrada — operacional em 3 semanas", "law_note": "Fundadores não-europeus podem registrar uma empresa irlandesa — o requisito de diretor EEE pode ser atendido por um diretor nomeado"},
            {"slug": "camila-brasilia", "name": "Camila", "location": "Brasília, Brasil", "situation": "Camila queria vender software para clientes europeus e precisava de uma entidade na UE. Sua ascendência irlandesa-brasileira fez da Irlanda a escolha natural.", "outcome": "Empresa operacional — IVA registado e a faturar", "law_note": "Empresas irlandesas precisam registrar no Revenue quando o volume de negócios ultrapassa €37.500 em serviços"},
        ]
    },
    # ═══════════════════════════════════════
    # SPANISH — CITIZENSHIP + PROPERTY + BUSINESS
    # ═══════════════════════════════════════
    {
        "path": "./es/ciudadania-irlandesa-ascendencia/index.html",
        "lang": "es", "type": "hub",
        "title": "Ciudadanía Irlandesa por Ascendencia — Cómo Reclamarla",
        "meta": "¿Tienes un abuelo o bisabuelo irlandés? Puede que tengas derecho a la ciudadanía irlandesa y un pasaporte europeo. Descubre cómo.",
        "h1": "Puede que ya seas\nciudadano irlandés.\n<em>Solo necesitas probarlo.</em>",
        "intro": "Si tienes un abuelo o bisabuelo irlandés, puede que tengas derecho a la ciudadanía irlandesa — y con ella, un pasaporte europeo con libre circulación en 27 países. El proceso requiere documentación precisa y conocimiento de la ley irlandesa. Un abogado especializado marca la diferencia.",
        "search_query": "ciudadanía irlandesa por ascendencia abuelo abogado España",
        "law": "Irish Nationality and Citizenship Acts 1956-2004 — la ciudadanía irlandesa pasa por vínculos de sangre a hijos y nietos de ciudadanos irlandeses",
        "audience": "international",
        "stories": [
            {"slug": "carlos-madrid", "name": "Carlos", "location": "Madrid, España", "situation": "El abuelo de Carlos había emigrado de Wicklow a España en los años 50. Tenía documentos familiares pero no sabía cómo demostrar la cadena de ciudadanía.", "outcome": "Pasaporte irlandés recibido — ciudadanía europea confirmada", "law_note": "El Registro de Nacimiento en el Extranjero es necesario para nietos — hay que probar la cadena de ciudadanía mediante documentación"},
            {"slug": "lucia-barcelona", "name": "Lucía", "location": "Barcelona, España", "situation": "La bisabuela de Lucía era de Kerry. Creía tener derecho a la ciudadanía pero no sabía si el derecho llegaba a su generación.", "outcome": "Ciudadanía confirmada — pasaporte emitido en 15 meses", "law_note": "La ciudadanía a través de bisabuelo requiere que el abuelo se haya registrado primero — es un proceso en dos etapas"},
            {"slug": "miguel-sevilla", "name": "Miguel", "location": "Sevilla, España", "situation": "Miguel tenía todos los documentos pero su solicitud fue rechazada dos veces. El abogado identificó un error en cómo se interpretaba el certificado de nacimiento irlandés.", "outcome": "Solicitud reapresentada y aprobada en el tercer intento", "law_note": "Los motivos de rechazo más comunes incluyen certificación incorrecta de documentos y errores en registros anteriores a 1900"},
            {"slug": "ana-valencia", "name": "Ana", "location": "Valencia, España", "situation": "El abuelo irlandés de Ana había salido de Irlanda a los 19 años sin documentación. Rastrear los registros requirió investigación genealógica en el General Register Office.", "outcome": "Registros encontrados — ciudadanía confirmada", "law_note": "El General Register Office de Irlanda mantiene registros desde 1864 — un abogado puede ayudar a rastrear y obtener copias certificadas"},
        ]
    },
    {
        "path": "./es/comprar-casa-irlanda-desde-espana/index.html",
        "lang": "es", "type": "hub",
        "title": "Comprar Casa en Irlanda desde España — Guía Legal",
        "meta": "¿Quieres comprar una propiedad en Irlanda viviendo en España? Un abogado gestiona todo el proceso legal a distancia. Descubre cómo funciona.",
        "h1": "Comprar una propiedad\nen Irlanda desde España.\n<em>Todo se puede gestionar a distancia.</em>",
        "intro": "Los no residentes pueden comprar propiedades en Irlanda sin restricciones. Pero la transmisión legal — el proceso de transferencia de titularidad — debe ser gestionada por un abogado irlandés. La buena noticia es que todo el proceso puede hacerse de forma remota. Nunca necesitas estar en Irlanda.",
        "search_query": "comprar casa irlanda desde españa abogado no residente",
        "law": "No hay restricciones para que no residentes compren propiedades en Irlanda. La transmisión está regida por el derecho contractual irlandés y el Registro de la Propiedad.",
        "audience": "international",
        "stories": [
            {"slug": "jorge-bilbao", "name": "Jorge", "location": "Bilbao, España", "situation": "Jorge quería comprar un apartamento en Dublín como inversión. Nunca había comprado en el extranjero y no entendía cómo el sistema irlandés difería del español.", "outcome": "Compra completada — llaves entregadas de forma remota", "law_note": "A diferencia de España, la ley irlandesa requiere un abogado para todas las transmisiones — el proceso suele durar 8-12 semanas"},
            {"slug": "elena-zaragoza", "name": "Elena", "location": "Zaragoza, España", "situation": "Elena volvía a Irlanda después de 15 años y quería comprar antes de llegar. Necesitaba un abogado que pudiera gestionar todo mientras estaba en España.", "outcome": "Venta acordada y completada antes de la llegada de Elena", "law_note": "Un Poder Notarial permite a tu abogado irlandés firmar documentos en tu nombre — muy útil para compradores en el extranjero"},
            {"slug": "roberto-malaga", "name": "Roberto", "location": "Málaga, España", "situation": "Roberto vio Irlanda como una inversión estable en la UE. Su principal preocupación era entender la posición fiscal como arrendador no residente.", "outcome": "Compra completada — estructura fiscal configurada correctamente desde el primer día", "law_note": "Los arrendadores no residentes en Irlanda deben registrarse en Revenue — tu abogado puede asesorarte sobre la estructura correcta"},
        ]
    },
    {
        "path": "./es/crear-empresa-irlanda/index.html",
        "lang": "es", "type": "hub",
        "title": "Crear una Empresa en Irlanda desde España — Guía Completa",
        "meta": "¿Quieres registrar una empresa en Irlanda? Acceso al mercado europeo, impuesto del 12,5% y sin necesidad de residir allí. Descubre cómo.",
        "h1": "Crea una empresa\nen Irlanda desde donde estés.\n<em>Base en la UE. 12,5% de impuesto.</em>",
        "intro": "Irlanda ofrece uno de los entornos más favorables para los negocios en la UE — 12,5% de impuesto de sociedades, idioma inglés y acceso total al mercado único europeo. No necesitas ser irlandés ni vivir en Irlanda para constituir una empresa irlandesa. Pero sí necesitas un abogado irlandés para hacerlo correctamente.",
        "search_query": "crear empresa irlanda desde españa abogado guía",
        "law": "Companies Act 2014 — las empresas irlandesas necesitan al menos un director residente en el EEE, o depositar una garantía de €25.000",
        "audience": "international",
        "stories": [
            {"slug": "manuel-madrid2", "name": "Manuel", "location": "Madrid, España", "situation": "La empresa de consultoría de Manuel necesitaba una entidad en la UE para contratos europeos post-Brexit. Eligió Irlanda por el idioma y la tributación.", "outcome": "Empresa registrada — operativa en 3 semanas", "law_note": "Los fundadores no europeos pueden registrar una empresa irlandesa — el requisito de director EEE puede cumplirse con un director nominado"},
            {"slug": "isabella-barcelona2", "name": "Isabella", "location": "Barcelona, España", "situation": "La startup tecnológica de Isabella necesitaba una base en la UE para conformidad con el GDPR y contratos con clientes europeos.", "outcome": "Filial irlandesa registrada — contratos firmados en un mes", "law_note": "Las empresas irlandesas deben registrarse para el IVA cuando la facturación supera €37.500 en servicios — tu abogado puede asesorarte"},
        ]
    },
    # ═══════════════════════════════════════
    # ROMANIAN — CITIZENSHIP + PROPERTY
    # ═══════════════════════════════════════
    {
        "path": "./ro/cetatenie-irlandeza-prin-bunic/index.html",
        "lang": "ro", "type": "hub",
        "title": "Cetățenie Irlandeză prin Bunic — Cum o Obții din România",
        "meta": "Ai un bunic sau străbunic irlandez? S-ar putea să ai dreptul la cetățenie irlandeză și un pașaport european. Află cum cu ajutorul unui avocat specialist.",
        "h1": "S-ar putea să fii deja\ncetățean irlandez.\n<em>Trebuie doar să demonstrezi.</em>",
        "intro": "Dacă ai un bunic sau un părinte irlandez, s-ar putea să ai dreptul la cetățenie irlandeză — și odată cu ea, un pașaport european cu liberă circulație în 27 de țări. Procesul necesită documentație precisă și cunoașterea legii irlandeze. Un avocat specializat face diferența dintre succes și ani de întârzieri.",
        "search_query": "cetățenie irlandeză prin bunic România avocat cum obții",
        "law": "Irish Nationality and Citizenship Acts 1956-2004 — cetățenia irlandeză se transmite prin legătură de sânge copiilor și nepoților cetățenilor irlandezi",
        "audience": "international",
        "stories": [
            {"slug": "mihai-cluj", "name": "Mihai", "location": "Cluj-Napoca, România", "situation": "Bunicul lui Mihai emigrase din Irlanda în România în anii 1950. Mihai avea fotografii și scrisori dar nu știa ce documente trebuia să prezinte pentru a dovedi cetățenia.", "outcome": "Pașaport irlandez primit — cetățenie europeană confirmată", "law_note": "Înregistrarea Nașterii în Străinătate este necesară pentru nepoți — trebuie dovedită lanțul de cetățenie prin documentație"},
            {"slug": "elena-iasi", "name": "Elena", "location": "Iași, România", "situation": "Cererea Elenei fusese respinsă de două ori fără un motiv clar. Avocatul a identificat o eroare în modul în care era interpretat certificatul de naștere irlandez.", "outcome": "Cerere redepusă și aprobată la a treia încercare", "law_note": "Motivele comune de respingere includ certificarea incorectă a documentelor și erorile în citirea registrelor anterioare anului 1900"},
            {"slug": "andrei-timisoara", "name": "Andrei", "location": "Timișoara, România", "situation": "Bunicul irlandez al lui Andrei plecase din Irlanda la 18 ani fără documentație. Urmărirea registrelor a necesitat cercetare genealogică la General Register Office.", "outcome": "Registre găsite — cetățenie confirmată", "law_note": "General Register Office din Irlanda deține registre de naștere din 1864 — un avocat poate ajuta la urmărirea și obținerea de copii certificate"},
            {"slug": "maria-bucuresti2", "name": "Maria", "location": "București, România", "situation": "Mama Mariei era irlandeză dar nu își înregistrase niciodată nașterea în străinătate. Lanțul de cetățenie era întrerupt. Avocatul a găsit o soluție.", "outcome": "Mama înregistrată mai întâi, cetățenia Mariei confirmată", "law_note": "Înregistrarea Nașterii în Străinătate trebuie completată în ordine — mai întâi părintele, apoi copilul"},
        ]
    },
    {
        "path": "./ro/vanzare-proprietate-irlanda-din-romania/index.html",
        "lang": "ro", "type": "hub",
        "title": "Vânzare Proprietate în Irlanda din România — Ghid Complet",
        "meta": "Ai o casă sau teren în Irlanda și vrei să vinzi din România? Află cum funcționează procesul și ce taxe se aplică nerezidenților.",
        "h1": "Vinzi o proprietate\nîn Irlanda din România?\n<em>Totul se poate rezolva de la distanță.</em>",
        "intro": "Dacă ai cumpărat sau moștenit o proprietate în Irlanda și acum locuiești în România, vânzarea implică legislație irlandeză — indiferent unde te afli. Un avocat irlandez gestionează întregul proces în numele tău: de la negocierea contractului până la transferul banilor în contul tău românesc.",
        "search_query": "vând proprietate Irlanda din România avocat nerezident",
        "law": "Conveyancing Act — vânzarea proprietăților irlandeze trebuie gestionată de un avocat irlandez. Nerezidenții sunt supuși CGT (Capital Gains Tax) pe profitul din vânzare.",
        "audience": "international",
        "stories": [
            {"slug": "ion-brasov", "name": "Ion", "location": "Brașov, România", "situation": "Ion cumpărase un apartament în Dublin când lucrase acolo. S-a întors în România și voia să vândă. Nu știa cum să gestioneze procesul de la distanță.", "outcome": "Proprietate vândută — bani transferați în România în 3 luni", "law_note": "Nerezidenții care vând proprietăți în Irlanda pot fi supuși Capital Gains Tax — avocatul poate structura corect tranzacția"},
            {"slug": "cristina-constanta", "name": "Cristina", "location": "Constanța, România", "situation": "Cristina moștenise un teren în Irlanda. Nu știa dacă trebuia să plătească taxe în Irlanda sau în România sau în ambele țări.", "outcome": "Situația fiscală clarificată — teren vândut fără surprize", "law_note": "Acordurile de evitare a dublei impuneri între Irlanda și România pot reduce povara fiscală — un avocat specializat poate evalua situația"},
            {"slug": "radu-cluj2", "name": "Radu", "location": "Cluj-Napoca, România", "situation": "Radu avea o casă în Irlanda care stătea goală de 3 ani. Voia să o vândă dar se temea că procesul va dura ani.", "outcome": "Casă vândută în 4 luni de la angajarea avocatului", "law_note": "Vânzarea proprietăților irlandeze durează de obicei 8-12 săptămâni odată ce cumpărătorul este găsit — un avocat accelerează întregul proces"},
        ]
    },
    # ═══════════════════════════════════════
    # POLISH — PROPERTY SALE
    # ═══════════════════════════════════════
    {
        "path": "./pl/sprzedaz-nieruchomosci-irlandia-z-polski/index.html",
        "lang": "pl", "type": "hub",
        "title": "Sprzedaż Nieruchomości w Irlandii z Polski — Kompletny Przewodnik",
        "meta": "Masz dom lub mieszkanie w Irlandii i chcesz sprzedać mieszkając w Polsce? Dowiedz się jak działa ten proces i jakie podatki obowiązują nierezydentów.",
        "h1": "Sprzedajesz nieruchomość\nw Irlandii z Polski?\n<em>Wszystko można załatwić zdalnie.</em>",
        "intro": "Jeśli kupiłeś lub odziedziczyłeś nieruchomość w Irlandii i teraz mieszkasz w Polsce, sprzedaż podlega irlandzkiemu prawu — niezależnie od tego gdzie jesteś. Irlandzki prawnik zarządza całym procesem w twoim imieniu: od negocjacji umowy do przelewu pieniędzy na twoje polskie konto.",
        "search_query": "sprzedaż nieruchomości Irlandia z Polski prawnik nierezydent",
        "law": "Prawo konweyancingowe — sprzedaż irlandzkich nieruchomości musi być obsługiwana przez irlandzkiego prawnika. Nierezydenci podlegają CGT (podatek od zysków kapitałowych) od zysku ze sprzedaży.",
        "audience": "international",
        "stories": [
            {"slug": "tomasz-krakow", "name": "Tomasz", "location": "Kraków, Polska", "situation": "Tomasz kupił mieszkanie w Dublinie gdy tam pracował. Wrócił do Polski i chciał sprzedać. Nie wiedział jak zarządzać procesem na odległość.", "outcome": "Nieruchomość sprzedana — pieniądze przelane do Polski w 3 miesiące", "law_note": "Nierezydenci sprzedający nieruchomości w Irlandii mogą podlegać Capital Gains Tax — prawnik może prawidłowo ustrukturyzować transakcję"},
            {"slug": "agnieszka-warszawa2", "name": "Agnieszka", "location": "Warszawa, Polska", "situation": "Agnieszka odziedziczyła dom w Irlandii. Nie wiedziała czy musi płacić podatki w Irlandii, Polsce czy w obu krajach.", "outcome": "Sytuacja podatkowa wyjaśniona — dom sprzedany bez niespodzianek", "law_note": "Umowy o unikaniu podwójnego opodatkowania między Irlandią a Polską mogą zmniejszyć obciążenie podatkowe — specjalistyczny prawnik może ocenić sytuację"},
            {"slug": "piotr-gdansk", "name": "Piotr", "location": "Gdańsk, Polska", "situation": "Piotr miał dom w Irlandii który stał pusty od 2 lat. Chciał sprzedać ale obawiał się że proces potrwa lata.", "outcome": "Dom sprzedany w 4 miesiące od zatrudnienia prawnika", "law_note": "Sprzedaż irlandzkich nieruchomości trwa zazwyczaj 8-12 tygodni po znalezieniu kupującego — prawnik przyspiesza cały proces"},
        ]
    },
    # ═══════════════════════════════════════
    # HIRE A LAWYER — ALL LANGUAGES
    # ═══════════════════════════════════════
    {
        "path": "./ro/angajez-avocat-irlanda/index.html",
        "lang": "ro", "type": "hire",
        "title": "Angajez Avocat în Irlanda — Cum Găsești Avocatul Potrivit",
        "meta": "Cauți un avocat în Irlanda? eSolicitors.ie te pune în legătură cu avocatul potrivit pentru situația ta — gratuit și fără obligații.",
        "h1": "Angajezi un avocat\nîn Irlanda?\n<em>Ești în locul potrivit.</em>",
        "intro": "Găsirea unui avocat bun în Irlanda nu trebuie să fie complicată sau costisitoare. eSolicitors.ie te conectează gratuit cu avocatul potrivit pentru situația ta — în județul tău sau care lucrează cu clienți din afara Irlandei. Nu plătești nimic pentru potrivire. Prima consultație cu avocatul este întotdeauna gratuită.",
        "search_query": "angajez avocat în Irlanda cum găsesc avocat irlandez",
        "law": "Avocații din Irlanda sunt reglementați de Law Society of Ireland. Toți avocații eSolicitors.ie sunt calificați și verificați.",
        "audience": "hire"
    },
    {
        "path": "./ro/cum-gasesc-avocat-in-irlanda/index.html",
        "lang": "ro", "type": "hire",
        "title": "Cum Găsesc un Avocat în Irlanda — Ghid Practic",
        "meta": "Nu știi cum să găsești un avocat în Irlanda? Află pașii simpli și cum eSolicitors.ie face totul gratuit pentru tine.",
        "h1": "Cum găsești\nun avocat în Irlanda.\n<em>Mai simplu decât crezi.</em>",
        "intro": "Mulți oameni nu știu de unde să înceapă când au nevoie de un avocat în Irlanda. Prin eSolicitors.ie procesul este simplu — descrii situația ta, noi identificăm avocatul potrivit din domeniul și județul tău, și avocatul te contactează direct. Gratuit, confidențial, fără obligații.",
        "search_query": "cum găsesc avocat în Irlanda pentru problema mea",
        "law": "Avocații din Irlanda sunt reglementați de Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ro/avocat-roman-in-irlanda/index.html",
        "lang": "ro", "type": "hire",
        "title": "Avocat Român în Irlanda — Ajutor în Limba Română",
        "meta": "Cauți un avocat care vorbește română în Irlanda? eSolicitors.ie îți oferă asistență în română și te conectează cu avocatul potrivit.",
        "h1": "Cauți un avocat\ncare vorbește română în Irlanda?\n<em>Suntem aici să ajutăm.</em>",
        "intro": "Înțelegerea sistemului juridic irlandez în propria ta limbă face o diferență enormă. La eSolicitors.ie, Mirela îți explică totul în română și te pune în legătură cu avocatul potrivit pentru situația ta. Nu trebuie să cunoști termeni juridici. Nu trebuie să plătești nimic pentru potrivire.",
        "search_query": "avocat român în Irlanda limbă română ajutor juridic",
        "law": "Avocații din Irlanda sunt reglementați de Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ro/cat-costa-avocat-irlanda/index.html",
        "lang": "ro", "type": "hire",
        "title": "Cât Costă un Avocat în Irlanda — Ghid Onorarii 2026",
        "meta": "Te întrebi cât costă un avocat în Irlanda? Află ghidul de onorarii și cum prima consultație este întotdeauna gratuită prin eSolicitors.ie.",
        "h1": "Cât costă\nun avocat în Irlanda?\n<em>Prima consultație este gratuită.</em>",
        "intro": "Onorariile avocaților în Irlanda variază mult în funcție de domeniu, complexitate și avocat. Dar prin eSolicitors.ie, prima consultație cu avocatul este întotdeauna gratuită — și nu plătești nimic pentru serviciul de potrivire. Avocatul îți va explica clar costurile înainte să te angajezi la ceva.",
        "search_query": "cât costă un avocat în Irlanda onorarii consultație",
        "law": "Avocații din Irlanda trebuie să furnizeze un deviz de costuri înainte de angajare — această cerință este reglementată de Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ro/consultatie-gratuita-avocat-irlanda/index.html",
        "lang": "ro", "type": "hire",
        "title": "Consultație Gratuită Avocat Irlanda — Vorbește cu un Avocat Azi",
        "meta": "Ai nevoie de consultație gratuită cu un avocat în Irlanda? Prin eSolicitors.ie prima consultație este întotdeauna gratuită. Nicio obligație.",
        "h1": "Consultație gratuită\ncu un avocat în Irlanda.\n<em>Azi. Fără obligații.</em>",
        "intro": "Prin eSolicitors.ie, prima consultație cu un avocat specializat este întotdeauna gratuită. Nu există taxe ascunse, nu există obligații să continui. Descrii situația ta Mirelei, ea identifică avocatul potrivit, și avocatul te contactează pentru o consultație gratuită — de obicei în câteva ore.",
        "search_query": "consultație gratuită avocat Irlanda fără obligații",
        "law": "Avocații din Irlanda sunt reglementați de Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pt-br/contratar-advogado-irlanda/index.html",
        "lang": "pt-br", "type": "hire",
        "title": "Contratar Advogado na Irlanda — Como Encontrar o Certo",
        "meta": "Precisa de um advogado na Irlanda? eSolicitors.ie conecta você gratuitamente com o advogado certo para sua situação.",
        "h1": "Contratar advogado\nna Irlanda?\n<em>Você está no lugar certo.</em>",
        "intro": "Encontrar um bom advogado na Irlanda não precisa ser complicado ou caro. eSolicitors.ie conecta você gratuitamente com o advogado certo para sua situação — no seu condado ou que trabalhe com clientes internacionais. Você não paga nada pela conexão. A primeira consulta com o advogado é sempre gratuita.",
        "search_query": "contratar advogado na Irlanda como encontrar advogado irlandês",
        "law": "Os advogados na Irlanda são regulamentados pela Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pt-br/advogado-brasileiro-irlanda/index.html",
        "lang": "pt-br", "type": "hire",
        "title": "Advogado Brasileiro na Irlanda — Ajuda em Português",
        "meta": "Procura um advogado que fale português na Irlanda? eSolicitors.ie oferece assistência em português e conecta você com o advogado certo.",
        "h1": "Procura um advogado\nque fale português na Irlanda?\n<em>Estamos aqui para ajudar.</em>",
        "intro": "Entender o sistema jurídico irlandês no seu próprio idioma faz uma diferença enorme. Na eSolicitors.ie, Ana explica tudo em português e conecta você com o advogado certo para sua situação. Não precisa conhecer termos jurídicos. Não paga nada pela conexão.",
        "search_query": "advogado brasileiro na Irlanda português ajuda jurídica",
        "law": "Os advogados na Irlanda são regulamentados pela Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pt-br/quanto-custa-advogado-irlanda/index.html",
        "lang": "pt-br", "type": "hire",
        "title": "Quanto Custa um Advogado na Irlanda — Guia de Honorários 2026",
        "meta": "Quer saber quanto custa um advogado na Irlanda? Saiba sobre os honorários e como a primeira consulta é sempre gratuita pela eSolicitors.ie.",
        "h1": "Quanto custa\num advogado na Irlanda?\n<em>A primeira consulta é gratuita.</em>",
        "intro": "Os honorários dos advogados na Irlanda variam muito conforme a área, complexidade e advogado. Mas pela eSolicitors.ie, a primeira consulta com o advogado é sempre gratuita — e você não paga nada pelo serviço de conexão. O advogado explicará claramente os custos antes de qualquer compromisso.",
        "search_query": "quanto custa advogado na Irlanda honorários consulta gratuita",
        "law": "Os advogados na Irlanda devem fornecer um orçamento de custos antes do compromisso — exigência regulamentada pela Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pt-br/como-achar-advogado-irlanda/index.html",
        "lang": "pt-br", "type": "hire",
        "title": "Como Achar Advogado na Irlanda — Guia Prático",
        "meta": "Não sabe como encontrar um advogado na Irlanda? Descubra os passos simples e como eSolicitors.ie faz tudo gratuitamente para você.",
        "h1": "Como encontrar\num advogado na Irlanda.\n<em>Mais simples do que você pensa.</em>",
        "intro": "Muitas pessoas não sabem por onde começar quando precisam de um advogado na Irlanda. Pela eSolicitors.ie o processo é simples — você descreve sua situação, identificamos o advogado certo na sua área, e o advogado entra em contato diretamente. Gratuito, confidencial, sem compromisso.",
        "search_query": "como achar advogado na Irlanda para meu problema",
        "law": "Os advogados na Irlanda são regulamentados pela Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./es/contratar-abogado-irlanda/index.html",
        "lang": "es", "type": "hire",
        "title": "Contratar Abogado en Irlanda — Cómo Encontrar el Adecuado",
        "meta": "¿Necesitas un abogado en Irlanda? eSolicitors.ie te conecta gratuitamente con el abogado adecuado para tu situación.",
        "h1": "¿Contratar abogado\nen Irlanda?\n<em>Estás en el lugar correcto.</em>",
        "intro": "Encontrar un buen abogado en Irlanda no tiene que ser complicado ni caro. eSolicitors.ie te conecta gratuitamente con el abogado adecuado para tu situación — en tu condado o que trabaje con clientes internacionales. No pagas nada por la conexión. La primera consulta con el abogado es siempre gratuita.",
        "search_query": "contratar abogado en Irlanda cómo encontrar abogado irlandés",
        "law": "Los abogados en Irlanda están regulados por la Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./es/abogado-espanol-irlanda/index.html",
        "lang": "es", "type": "hire",
        "title": "Abogado Español en Irlanda — Ayuda en Español",
        "meta": "¿Buscas un abogado que hable español en Irlanda? eSolicitors.ie ofrece asistencia en español y te conecta con el abogado adecuado.",
        "h1": "¿Buscas un abogado\nque hable español en Irlanda?\n<em>Estamos aquí para ayudarte.</em>",
        "intro": "Entender el sistema jurídico irlandés en tu propio idioma marca una gran diferencia. En eSolicitors.ie, Carmen te explica todo en español y te conecta con el abogado adecuado para tu situación. No necesitas conocer términos jurídicos. No pagas nada por la conexión.",
        "search_query": "abogado español en Irlanda ayuda jurídica en español",
        "law": "Los abogados en Irlanda están regulados por la Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./es/cuanto-cuesta-abogado-irlanda/index.html",
        "lang": "es", "type": "hire",
        "title": "¿Cuánto Cuesta un Abogado en Irlanda? — Guía de Honorarios 2026",
        "meta": "¿Quieres saber cuánto cuesta un abogado en Irlanda? Descubre los honorarios y cómo la primera consulta es siempre gratuita en eSolicitors.ie.",
        "h1": "¿Cuánto cuesta\nun abogado en Irlanda?\n<em>La primera consulta es gratuita.</em>",
        "intro": "Los honorarios de los abogados en Irlanda varían mucho según el área, la complejidad y el abogado. Pero a través de eSolicitors.ie, la primera consulta con el abogado es siempre gratuita — y no pagas nada por el servicio de conexión. El abogado te explicará claramente los costes antes de cualquier compromiso.",
        "search_query": "cuánto cuesta abogado en Irlanda honorarios consulta gratuita",
        "law": "Los abogados en Irlanda deben proporcionar un presupuesto de costes antes del compromiso — regulado por la Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pl/zatrudniam-prawnika-w-irlandii/index.html",
        "lang": "pl", "type": "hire",
        "title": "Zatrudniam Prawnika w Irlandii — Jak Znaleźć Odpowiedniego",
        "meta": "Potrzebujesz prawnika w Irlandii? eSolicitors.ie łączy cię bezpłatnie z odpowiednim prawnikiem dla twojej sytuacji.",
        "h1": "Szukasz prawnika\nw Irlandii?\n<em>Jesteś we właściwym miejscu.</em>",
        "intro": "Znalezienie dobrego prawnika w Irlandii nie musi być skomplikowane ani drogie. eSolicitors.ie łączy cię bezpłatnie z odpowiednim prawnikiem dla twojej sytuacji — w twoim hrabstwie lub pracującym z klientami z zagranicy. Nie płacisz nic za połączenie. Pierwsza konsultacja z prawnikiem jest zawsze bezpłatna.",
        "search_query": "zatrudniam prawnika w Irlandii jak znaleźć irlandzkiego prawnika",
        "law": "Prawnicy w Irlandii są regulowani przez Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pl/polski-prawnik-w-irlandii/index.html",
        "lang": "pl", "type": "hire",
        "title": "Polski Prawnik w Irlandii — Pomoc po Polsku",
        "meta": "Szukasz prawnika mówiącego po polsku w Irlandii? eSolicitors.ie oferuje pomoc po polsku i łączy cię z odpowiednim prawnikiem.",
        "h1": "Szukasz prawnika\nmówiącego po polsku w Irlandii?\n<em>Jesteśmy tu, żeby pomóc.</em>",
        "intro": "Rozumienie irlandzkiego systemu prawnego we własnym języku ma ogromne znaczenie. W eSolicitors.ie, Kasia wyjaśnia ci wszystko po polsku i łączy cię z odpowiednim prawnikiem dla twojej sytuacji. Nie musisz znać terminów prawnych. Nie płacisz nic za połączenie.",
        "search_query": "polski prawnik w Irlandii pomoc prawna po polsku",
        "law": "Prawnicy w Irlandii są regulowani przez Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./pl/ile-kosztuje-prawnik-w-irlandii/index.html",
        "lang": "pl", "type": "hire",
        "title": "Ile Kosztuje Prawnik w Irlandii — Przewodnik po Honorariach 2026",
        "meta": "Chcesz wiedzieć ile kosztuje prawnik w Irlandii? Dowiedz się o honorariach i jak pierwsza konsultacja jest zawsze bezpłatna w eSolicitors.ie.",
        "h1": "Ile kosztuje\nprawnik w Irlandii?\n<em>Pierwsza konsultacja jest bezpłatna.</em>",
        "intro": "Honoraria prawników w Irlandii bardzo się różnią w zależności od dziedziny, złożoności i prawnika. Ale przez eSolicitors.ie, pierwsza konsultacja z prawnikiem jest zawsze bezpłatna — i nie płacisz nic za usługę kojarzenia. Prawnik jasno wyjaśni koszty przed jakimkolwiek zobowiązaniem.",
        "search_query": "ile kosztuje prawnik w Irlandii honoraria konsultacja bezpłatna",
        "law": "Prawnicy w Irlandii muszą dostarczyć kosztorys przed zobowiązaniem — wymóg regulowany przez Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ar/tawdhif-muhami-fi-airlanda/index.html",
        "lang": "ar", "type": "hire",
        "title": "توظيف محامٍ في أيرلندا — كيف تجد المحامي المناسب",
        "meta": "تحتاج محامياً في أيرلندا؟ eSolicitors.ie يوصلك مجاناً بالمحامي المناسب لوضعك.",
        "h1": "تبحث عن محامٍ\nفي أيرلندا?\n<em>أنت في المكان الصحيح.</em>",
        "intro": "إيجاد محامٍ جيد في أيرلندا لا يجب أن يكون معقداً أو مكلفاً. eSolicitors.ie يوصلك مجاناً بالمحامي المناسب لوضعك — في مقاطعتك أو من يعمل مع عملاء دوليين. لا تدفع شيئاً للتوصيل. الاستشارة الأولى مع المحامي دائماً مجانية.",
        "search_query": "توظيف محامي في ايرلندا كيف أجد محامي مناسب",
        "law": "المحامون في أيرلندا منظمون من قِبل Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ar/muhami-arabi-fi-airlanda/index.html",
        "lang": "ar", "type": "hire",
        "title": "محامٍ عربي في أيرلندا — مساعدة قانونية بالعربية",
        "meta": "تبحث عن محامٍ يتحدث العربية في أيرلندا؟ eSolicitors.ie تقدم مساعدة بالعربية وتوصلك بالمحامي المناسب.",
        "h1": "تبحث عن محامٍ\nyتحدث العربية في أيرلندا?\n<em>نحن هنا للمساعدة.</em>",
        "intro": "فهم النظام القانوني الأيرلندي بلغتك الأم يحدث فرقاً كبيراً. في eSolicitors.ie، ليلى تشرح لك كل شيء بالعربية وتوصلك بالمحامي المناسب لوضعك. لا تحتاج لمعرفة مصطلحات قانونية. لا تدفع شيئاً للتوصيل.",
        "search_query": "محامي عربي في ايرلندا مساعدة قانونية بالعربية",
        "law": "المحامون في أيرلندا منظمون من قِبل Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ar/kam-yukalif-al-muhami-fi-airlanda/index.html",
        "lang": "ar", "type": "hire",
        "title": "كم يكلف المحامي في أيرلندا — دليل الأتعاب 2026",
        "meta": "تريد معرفة كم يكلف المحامي في أيرلندا؟ تعرف على الأتعاب وكيف أن الاستشارة الأولى دائماً مجانية في eSolicitors.ie.",
        "h1": "كم يكلف المحامي\nفي أيرلندا?\n<em>الاستشارة الأولى مجانية.</em>",
        "intro": "أتعاب المحامين في أيرلندا تتفاوت كثيراً حسب المجال والتعقيد والمحامي. لكن من خلال eSolicitors.ie، الاستشارة الأولى مع المحامي دائماً مجانية — ولا تدفع شيئاً مقابل خدمة التوصيل. المحامي سيشرح لك التكاليف بوضوح قبل أي التزام.",
        "search_query": "كم يكلف المحامي في ايرلندا أتعاب استشارة مجانية",
        "law": "يجب على المحامين في أيرلندا تقديم تقدير للتكاليف قبل الالتزام — متطلب منظم من قِبل Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ru/nanyat-advokata-v-irlandii/index.html",
        "lang": "ru", "type": "hire",
        "title": "Нанять Адвоката в Ирландии — Как Найти Подходящего",
        "meta": "Нужен адвокат в Ирландии? eSolicitors.ie бесплатно соединит вас с подходящим адвокатом для вашей ситуации.",
        "h1": "Ищете адвоката\nв Ирландии?\n<em>Вы в нужном месте.</em>",
        "intro": "Найти хорошего адвоката в Ирландии не должно быть сложно или дорого. eSolicitors.ie бесплатно соединяет вас с подходящим адвокатом для вашей ситуации — в вашем округе или работающим с международными клиентами. Вы ничего не платите за подбор. Первая консультация с адвокатом всегда бесплатна.",
        "search_query": "нанять адвоката в Ирландии как найти ирландского адвоката",
        "law": "Адвокаты в Ирландии регулируются Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ru/russkoyazychny-advokat-irlandiya/index.html",
        "lang": "ru", "type": "hire",
        "title": "Русскоязычный Адвокат в Ирландии — Помощь на Русском",
        "meta": "Ищете адвоката, говорящего по-русски, в Ирландии? eSolicitors.ie предлагает помощь на русском и соединяет вас с подходящим адвокатом.",
        "h1": "Ищете адвоката\nговорящего по-русски в Ирландии?\n<em>Мы здесь, чтобы помочь.</em>",
        "intro": "Понимание ирландской правовой системы на родном языке имеет огромное значение. В eSolicitors.ie Наташа объясняет вам всё по-русски и соединяет с подходящим адвокатом для вашей ситуации. Вам не нужно знать юридические термины. Вы ничего не платите за подбор.",
        "search_query": "русскоязычный адвокат в Ирландии помощь на русском",
        "law": "Адвокаты в Ирландии регулируются Law Society of Ireland.",
        "audience": "hire"
    },
    {
        "path": "./ru/skolko-stoit-advokat-v-irlandii/index.html",
        "lang": "ru", "type": "hire",
        "title": "Сколько Стоит Адвокат в Ирландии — Гонорары 2026",
        "meta": "Хотите знать сколько стоит адвокат в Ирландии? Узнайте о гонорарах и о том, что первая консультация всегда бесплатна в eSolicitors.ie.",
        "h1": "Сколько стоит\nадвокат в Ирландии?\n<em>Первая консультация бесплатна.</em>",
        "intro": "Гонорары адвокатов в Ирландии сильно варьируются в зависимости от области, сложности и адвоката. Но через eSolicitors.ie первая консультация с адвокатом всегда бесплатна — и вы ничего не платите за услугу подбора. Адвокат чётко объяснит стоимость перед любыми обязательствами.",
        "search_query": "сколько стоит адвокат в Ирландии гонорары бесплатная консультация",
        "law": "Адвокаты в Ирландии обязаны предоставить смету расходов до обязательства — требование регулируется Law Society of Ireland.",
        "audience": "hire"
    },
]


# ─────────────────────────────────────────
# HTML TEMPLATES
# ─────────────────────────────────────────

def get_sarah_widget_html(lang, uid):
    cfg = SARAH_CONFIG.get(lang, SARAH_CONFIG["en"])
    is_rtl = lang == "ar"
    dir_attr = ' dir="rtl"' if is_rtl else ''
    sols_html = ""
    for sol in cfg["solicitors"]:
        sols_html += f'<div class="sol-card"><div class="sol-av">{sol["initials"]}</div><div class="sol-info"><div class="sol-name">{sol["name"]}</div><div class="sol-area">{sol["area"]} · {sol["county"]}</div><div class="sol-stars">★★★★★</div></div><div class="sol-badge">Verified</div></div>'

    system_escaped = cfg["system"].replace("\\", "\\\\").replace('"', '\\"').replace("\n", "\\n")

    return f'''<div class="sarah-widget"{dir_attr}>
  <div class="sarah-header">
    <div class="sarah-av"><img src="{cfg["img"]}" alt="{cfg["name"]}"/></div>
    <div class="sarah-header-text">
      <strong>{cfg["name"]} — eSolicitors.ie</strong>
      <span>Legal intake · Free · Confidential</span>
    </div>
    <div class="sarah-online"></div>
  </div>
  <div class="sarah-messages" id="{uid}-msgs"></div>
  <div class="sarah-input-area">
    <div class="sarah-input-row">
      <textarea id="{uid}-input" rows="1" placeholder="{cfg["placeholder"]}"></textarea>
      <button class="sarah-send" onclick="window['{uid}_send']()">
        <svg width="14" height="14" fill="none" stroke="white" stroke-width="2" viewBox="0 0 24 24"><line x1="22" y1="2" x2="11" y2="13"/><polygon points="22 2 15 22 11 13 2 9 22 2"/></svg>
      </button>
    </div>
    <div class="sarah-note">{cfg["note"]}</div>
  </div>
</div>
<script>
(function(){{
var SARAH_IMG="{cfg["img"]}";
var SARAH_SOLS=[{','.join([f'{{initials:"{s["initials"]}",name:"{s["name"]}",area:"{s["area"]}",county:"{s["county"]}"}}'  for s in cfg["solicitors"]])}];
var SARAH_SYSTEM="{system_escaped}";
var TYPING_SPEED=40;
var uid="{uid}";
var history=[],stage="story",collected={{}},isLoading=false;
var msgs=document.getElementById(uid+"-msgs");
var input=document.getElementById(uid+"-input");
function typeMsg(el,text,cb){{var words=text.split(" ");var i=0;el.textContent="";function next(){{if(i<words.length){{el.textContent+=(i===0?"": " ")+words[i];i++;setTimeout(next,TYPING_SPEED+Math.random()*20);}}else{{if(cb)cb();}}}}next();}}
function addMsg(isUser){{var row=document.createElement("div");row.className="smsg"+(isUser?" user":"");if(!isUser){{var av=document.createElement("div");av.className="smsg-av";av.innerHTML="<img src=\\""+SARAH_IMG+"\\" alt=\\"{cfg["name"]}\\"/>";row.appendChild(av);}}var b=document.createElement("div");b.className="smsg-bubble";row.appendChild(b);msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;return b;}}
function showTyping(){{var row=document.createElement("div");row.className="sarah-typing";row.id=uid+"-typing";row.innerHTML="<div class=\\"smsg-av\\"><img src=\\""+SARAH_IMG+"\\"/></div><div class=\\"sarah-typing-bubble\\"><div class=\\"sdot\\"></div><div class=\\"sdot\\"></div><div class=\\"sdot\\"></div></div>";msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;}}
function removeTyping(){{var t=document.getElementById(uid+"-typing");if(t)t.remove();}}
function showSols(){{var row=document.createElement("div");row.className="smsg";var av=document.createElement("div");av.className="smsg-av";av.innerHTML="<img src=\\""+SARAH_IMG+"\\"/>";row.appendChild(av);var wrap=document.createElement("div");wrap.className="sol-cards-wrap";SARAH_SOLS.forEach(function(s){{var c=document.createElement("div");c.className="sol-card";c.innerHTML="<div class=\\"sol-av\\">"+s.initials+"</div><div class=\\"sol-info\\"><div class=\\"sol-name\\">"+s.name+"</div><div class=\\"sol-area\\">"+s.area+" · "+s.county+"</div><div class=\\"sol-stars\\">★★★★★</div></div><div class=\\"sol-badge\\">Verified</div>";wrap.appendChild(c);}});row.appendChild(wrap);msgs.appendChild(row);msgs.scrollTop=msgs.scrollHeight;}}
function send(){{if(!input)return;var text=input.value.trim();if(!text||isLoading)return;input.value="";input.style.height="auto";isLoading=true;var b=addMsg(true);b.textContent=text;history.push({{role:"user",content:text}});if(stage==="name")collected.name=text;if(stage==="phone")collected.phone=text;setTimeout(function(){{showTyping();var rd=Math.min(text.length*12,1200);setTimeout(function(){{fetch("/api/chat",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{system:SARAH_SYSTEM+"\\nCurrent stage: "+stage,messages:history}})}}).then(function(r){{removeTyping();if(!r.ok){{addMsg(false).textContent="Something went wrong.";isLoading=false;return;}}return r.json();}}).then(function(d){{if(!d)return;var raw=(d.content&&d.content[0]&&d.content[0].text)||"";var parsed;try{{var m=raw.replace(/```json|```/g,"").trim().match(/\\{{[\\s\\S]*\\}}/);parsed=m?JSON.parse(m[0]):null;if(!parsed||!parsed.message)throw 0;}}catch(e){{parsed={{message:raw||"Something went wrong.",next_stage:stage}};}}var bubble=addMsg(false);typeMsg(bubble,parsed.message,function(){{msgs.scrollTop=msgs.scrollHeight;if(parsed.show_solicitors)setTimeout(showSols,600);}});history.push({{role:"assistant",content:parsed.message}});if(parsed.next_stage)stage=parsed.next_stage;if(stage==="done"&&collected.phone){{var tr=history.map(function(m){{return(m.role==="user"?"Visitor: ":"Sarah: ")+m.content;}}).join("\\n");var issue="";for(var i=0;i<history.length;i++){{if(history[i].role==="user"){{issue=history[i].content.substring(0,120);break;}}}}fetch("/api/leads",{{method:"POST",headers:{{"Content-Type":"application/json"}},body:JSON.stringify({{name:collected.name||"",phone:collected.phone||"",issue:issue,transcript:tr,source:window.location.pathname}})}}); }}isLoading=false;}}).catch(function(){{removeTyping();addMsg(false).textContent="Network error.";isLoading=false;}});}},rd);}},400+Math.random()*300);}}
if(input){{input.addEventListener("input",function(){{this.style.height="auto";this.style.height=Math.min(this.scrollHeight,70)+"px";}});input.addEventListener("keydown",function(e){{if(e.key==="Enter"&&!e.shiftKey){{e.preventDefault();send();}}}});}}
window[uid+"_send"]=send;
setTimeout(function(){{var b=addMsg(false);typeMsg(b,"{cfg["greeting"]}",function(){{msgs.scrollTop=msgs.scrollHeight;}});}},700);
}})();
</script>'''


SARAH_CSS = """<style>
.sarah-widget{background:#fff;border-radius:14px;overflow:hidden;box-shadow:0 20px 60px rgba(0,0,0,0.22);max-width:480px;margin:0 auto}
.sarah-header{background:#0c1f3d;padding:14px 18px;display:flex;align-items:center;gap:12px;position:relative;border-bottom:1px solid rgba(200,146,42,.2)}
.sarah-av{width:40px;height:40px;border-radius:50%;overflow:hidden;border:2px solid #c8922a;flex-shrink:0}
.sarah-av img{width:100%;height:100%;object-fit:cover}
.sarah-header-text strong{display:block;font-size:.88rem;font-weight:600;color:#fff}
.sarah-header-text span{font-size:.72rem;color:rgba(255,255,255,.4)}
.sarah-online{width:8px;height:8px;background:#4ade80;border-radius:50%;position:absolute;right:16px;top:50%;transform:translateY(-50%)}
.sarah-messages{height:280px;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:10px;background:#f7f3ee}
.smsg{display:flex;align-items:flex-end;gap:7px}
.smsg.user{flex-direction:row-reverse}
.smsg-av{width:26px;height:26px;border-radius:50%;overflow:hidden;flex-shrink:0;border:1.5px solid #c8922a}
.smsg-av img{width:100%;height:100%;object-fit:cover}
.smsg-bubble{max-width:78%;padding:9px 12px;border-radius:12px;font-size:.83rem;line-height:1.65}
.smsg.ai .smsg-bubble{background:#fff;color:#0c1f3d;border-bottom-left-radius:3px;box-shadow:0 1px 3px rgba(0,0,0,.06)}
.smsg.user .smsg-bubble{background:#0c1f3d;color:#fff;border-bottom-right-radius:3px}
.sarah-typing{display:flex;align-items:flex-end;gap:7px}
.sarah-typing-bubble{background:#fff;border-radius:12px;border-bottom-left-radius:3px;padding:9px 12px;display:flex;gap:3px;align-items:center}
.sdot{width:5px;height:5px;background:#bbb;border-radius:50%;animation:sdotB 1.2s infinite}
.sdot:nth-child(2){animation-delay:.2s}.sdot:nth-child(3){animation-delay:.4s}
@keyframes sdotB{0%,60%,100%{transform:translateY(0)}30%{transform:translateY(-5px)}}
.sarah-input-area{border-top:1px solid #e2ddd6;padding:10px 12px;background:#fff}
.sarah-input-row{display:flex;align-items:center;gap:8px;background:#f7f3ee;border:1.5px solid #e2ddd6;border-radius:10px;padding:8px 12px;transition:border-color .2s}
.sarah-input-row:focus-within{border-color:#c8922a}
.sarah-input-row textarea{flex:1;border:none;background:transparent;font-family:inherit;font-size:.83rem;color:#0c1f3d;resize:none;outline:none;line-height:1.5;max-height:70px;overflow-y:auto}
.sarah-input-row textarea::placeholder{color:#bbb}
.sarah-send{width:32px;height:32px;border-radius:7px;background:#0c1f3d;border:none;cursor:pointer;display:flex;align-items:center;justify-content:center;flex-shrink:0}
.sarah-send:hover{background:#162d52}
.sarah-note{text-align:center;font-size:.7rem;color:#bbb;margin-top:6px}
.sol-cards-wrap{display:flex;flex-direction:column;gap:7px;margin-top:4px}
.sol-card{background:#fff;border:1px solid #e8e2d9;border-radius:10px;padding:9px 11px;display:flex;align-items:center;gap:9px}
.sol-av{width:36px;height:36px;border-radius:50%;background:#0c1f3d;display:flex;align-items:center;justify-content:center;font-size:.75rem;font-weight:700;color:#c8922a;flex-shrink:0}
.sol-name{font-size:12.5px;font-weight:600;color:#0c1f3d}
.sol-area{font-size:10.5px;color:#8896a8;margin-top:1px}
.sol-stars{color:#f5a623;font-size:10px}
.sol-badge{background:#0c1f3d;color:#fff;font-size:8.5px;font-weight:600;border-radius:4px;padding:2px 6px}
</style>"""


def get_nav(lang):
    cfg = SARAH_CONFIG.get(lang, SARAH_CONFIG["en"])
    labels = {
        "en": ("Get Matched — Free", f"Talk to {cfg['name']}"),
        "ro": ("Potrivire Gratuită", f"Vorbește cu {cfg['name']}"),
        "pt-br": ("Conectar — Grátis", f"Fale com {cfg['name']}"),
        "es": ("Conectar — Gratis", f"Habla con {cfg['name']}"),
        "pl": ("Połącz Bezpłatnie", f"Porozmawiaj z {cfg['name']}"),
        "ar": (f"تحدث مع {cfg['name']}", f"تحدث مع {cfg['name']}"),
        "ru": (f"Поговорить с {cfg['name']}", f"Поговорить с {cfg['name']}"),
    }
    cta_text = labels.get(lang, labels["en"])[0]
    return f'''<nav style="position:sticky;top:0;z-index:100;background:#0c1f3d;border-bottom:1px solid rgba(200,146,42,.2);padding:0 5%;height:62px;display:flex;align-items:center;justify-content:space-between">
  <a href="/" style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:#c8922a">Solicitors</span>.ie</a>
  <a href="/chat.html" style="background:#c8922a;color:#0c1f3d;padding:8px 18px;border-radius:6px;font-weight:600;text-decoration:none;font-size:.85rem">{cta_text}</a>
</nav>'''


def get_footer(lang):
    year = "2026"
    texts = {
        "en": f"© {year} eSolicitors.ie Ltd. All rights reserved. · eSolicitors.ie is a referral service, not a law firm.",
        "ro": f"© {year} eSolicitors.ie Ltd. Toate drepturile rezervate. · eSolicitors.ie este un serviciu de referire.",
        "pt-br": f"© {year} eSolicitors.ie Ltd. Todos os direitos reservados. · eSolicitors.ie é um serviço de referência.",
        "es": f"© {year} eSolicitors.ie Ltd. Todos los derechos reservados. · eSolicitors.ie es un servicio de referencia.",
        "pl": f"© {year} eSolicitors.ie Ltd. Wszelkie prawa zastrzeżone. · eSolicitors.ie to serwis referencyjny.",
        "ar": f"© {year} eSolicitors.ie Ltd. جميع الحقوق محفوظة. · eSolicitors.ie خدمة إحالة.",
        "ru": f"© {year} eSolicitors.ie Ltd. Все права защищены. · eSolicitors.ie — реферальный сервис.",
    }
    return f'''<footer style="background:#080f1e;padding:32px 5%;text-align:center">
  <a href="/" style="font-family:'Playfair Display',serif;font-size:1.2rem;font-weight:700;color:#fff;text-decoration:none">e<span style="color:#c8922a">Solicitors</span>.ie</a>
  <p style="font-size:.75rem;color:rgba(255,255,255,.25);margin-top:16px">{texts.get(lang, texts["en"])}</p>
</footer>'''


def build_story_html(page, story):
    lang = page["lang"]
    cfg = SARAH_CONFIG.get(lang, SARAH_CONFIG["en"])
    uid = "sw" + story["slug"].replace("-", "")[:8]
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    lang_attr = f' lang="{lang}"'

    back_labels = {
        "en": f"← Back to: {page['title']}",
        "ro": f"← Înapoi la: {page['title']}",
        "pt-br": f"← Voltar para: {page['title']}",
        "es": f"← Volver a: {page['title']}",
        "pl": f"← Powrót do: {page['title']}",
        "ar": f"← العودة إلى: {page['title']}",
        "ru": f"← Назад к: {page['title']}",
    }

    folder = os.path.dirname(page["path"])
    back_url = "/" + folder.lstrip("./") + "/"

    return f'''<!DOCTYPE html>
<html{lang_attr}{dir_attr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{story["name"]}, {story["location"]} — {page["title"]} | eSolicitors.ie</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
{SARAH_CSS}
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0c1f3d;--navy-mid:#162d52;--gold:#c8922a;--cream:#f7f3ee;--border:#e8e2d9}}
body{{font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--navy);overflow-x:hidden}}
.story-hero{{background:var(--navy);padding:48px 5%;position:relative;overflow:hidden}}
.story-hero::before{{content:'';position:absolute;top:-100px;right:-100px;width:400px;height:400px;background:radial-gradient(circle,rgba(200,146,42,.08) 0%,transparent 70%);pointer-events:none}}
.story-hero-inner{{max-width:800px;margin:0 auto;position:relative;z-index:1}}
.back-link{{display:inline-block;font-size:.78rem;color:rgba(255,255,255,.45);text-decoration:none;margin-bottom:18px;transition:color .2s}}
.back-link:hover{{color:var(--gold)}}
.story-tag{{display:inline-block;background:rgba(200,146,42,.12);border:1px solid rgba(200,146,42,.3);color:#e8b04a;padding:4px 12px;border-radius:100px;font-size:.7rem;font-weight:700;letter-spacing:.07em;text-transform:uppercase;margin-bottom:16px}}
.story-hero h1{{font-family:'Playfair Display',serif;font-size:clamp(1.6rem,3vw,2.4rem);font-weight:900;color:#fff;line-height:1.15;margin-bottom:14px}}
.story-outcome{{display:inline-flex;align-items:center;gap:8px;background:rgba(26,122,74,.15);border:1px solid rgba(26,122,74,.3);color:#4ade80;padding:6px 14px;border-radius:100px;font-size:.78rem;font-weight:700;margin-top:8px}}
.page-wrap{{max-width:800px;margin:0 auto;padding:0 5%}}
.section{{padding:40px 0;border-bottom:1px solid var(--border)}}
.section:last-child{{border-bottom:none}}
.section-label{{font-size:.7rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}}
.section-title{{font-family:'Playfair Display',serif;font-size:1.3rem;font-weight:700;color:var(--navy);margin-bottom:14px}}
.body-text{{font-size:.93rem;color:#4a5568;line-height:1.9;font-weight:300}}
.body-text p{{margin-bottom:14px}}
.law-box{{background:#fff;border:1.5px solid var(--border);border-left:4px solid var(--navy);border-radius:0 10px 10px 0;padding:18px 20px;margin-top:16px}}
.law-box-title{{font-size:.75rem;font-weight:700;color:var(--navy);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}}
.law-box p{{font-size:.86rem;color:#4a5568;line-height:1.75}}
.warning-box{{background:#fdf0ee;border:1.5px solid rgba(192,57,43,.2);border-left:4px solid #c0392b;border-radius:0 10px 10px 0;padding:18px 20px;margin-top:20px}}
.warning-title{{font-size:.75rem;font-weight:700;color:#c0392b;text-transform:uppercase;letter-spacing:.05em;margin-bottom:8px}}
.warning-box p{{font-size:.86rem;color:#7a2a20;line-height:1.75}}
.cta-section{{background:var(--navy);padding:56px 5%;text-align:center}}
.cta-label{{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:12px}}
.cta-title{{font-family:'Playfair Display',serif;font-size:1.7rem;font-weight:700;color:#fff;margin-bottom:12px;line-height:1.2}}
.cta-sub{{font-size:.92rem;color:rgba(255,255,255,.55);margin-bottom:28px;line-height:1.7}}
</style>
</head>
<body>
{get_nav(lang)}
<div class="story-hero">
  <div class="story-hero-inner">
    <a href="{back_url}" class="back-link">{back_labels.get(lang, back_labels["en"])}</a>
    <div class="story-tag">Real Case · {story["location"]}</div>
    <h1>{story["name"]}, {story["location"]}</h1>
    <div class="story-outcome">✓ {story["outcome"]}</div>
  </div>
</div>
<div class="page-wrap">
  <section class="section">
    <div class="section-label">What Happened</div>
    <h2 class="section-title">{story["name"]}'s situation</h2>
    <div class="body-text"><p>{story["situation"]}</p></div>
  </section>
  <section class="section">
    <div class="section-label">The Law</div>
    <h2 class="section-title">What Irish law says</h2>
    <div class="law-box">
      <div class="law-box-title">Legal Framework</div>
      <p>{story.get("law_note", page["law"])}</p>
    </div>
    <div class="warning-box" style="margin-top:20px">
      <div class="warning-title">⏰ Time Limits Apply</div>
      <p>Legal deadlines in Ireland are strict. If you recognise yourself in {story["name"]}'s situation, act now. A free consultation costs nothing and could protect your rights.</p>
    </div>
  </section>
</div>
<div class="cta-section">
  <div style="max-width:600px;margin:0 auto 28px">
    <div class="cta-label">Free Solicitor Matching</div>
    <h2 class="cta-title">In a similar situation?<br>You may have a case too.</h2>
    <p class="cta-sub">Tell {cfg["name"]} what happened. Free, confidential, no obligation.</p>
  </div>
  {get_sarah_widget_html(lang, uid)}
</div>
{get_footer(lang)}
</body>
</html>'''


def build_hub_html(page, content):
    lang = page["lang"]
    cfg = SARAH_CONFIG.get(lang, SARAH_CONFIG["en"])
    uid = "sw" + str(abs(hash(page["path"])))[:8]
    dir_attr = ' dir="rtl"' if lang == "ar" else ""
    lang_attr = f' lang="{lang}"'

    # Build story cards if stories exist
    story_cards = ""
    if page.get("stories"):
        folder = os.path.dirname(page["path"]).lstrip("./")
        for story in page["stories"]:
            url = f"/{folder}/{story['slug']}/"
            story_cards += f'<a href="{url}" style="background:#fff;border:1px solid #e8e2d9;border-left:3px solid #c8922a;border-radius:0 10px 10px 0;padding:18px;text-decoration:none;display:block;transition:box-shadow .2s;margin-bottom:12px"><div style="font-size:.87rem;font-weight:700;color:#0c1f3d;margin-bottom:5px">{story["name"]}, {story["location"]}</div><div style="font-size:.8rem;color:#4a5568;line-height:1.6;margin-bottom:7px">{story["situation"][:100]}...</div><div style="font-size:.75rem;color:#1a7a4a;font-weight:700">✓ {story["outcome"]}</div></a>'

    return f'''<!DOCTYPE html>
<html{lang_attr}{dir_attr}>
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{page["title"]} | eSolicitors.ie</title>
<meta name="description" content="{page["meta"]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,400;0,700;0,900;1,400&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet">
{SARAH_CSS}
<style>
*,*::before,*::after{{box-sizing:border-box;margin:0;padding:0}}
:root{{--navy:#0c1f3d;--navy-mid:#162d52;--gold:#c8922a;--gold-light:#e8b04a;--cream:#f7f3ee;--border:#e8e2d9}}
body{{font-family:'DM Sans',sans-serif;background:var(--cream);color:var(--navy);overflow-x:hidden}}
.hero{{background:var(--navy);padding:56px 5% 64px;position:relative;overflow:hidden}}
.hero::before{{content:'';position:absolute;top:-150px;right:-150px;width:600px;height:600px;background:radial-gradient(circle,rgba(200,146,42,.09) 0%,transparent 70%);pointer-events:none}}
.hero-inner{{max-width:1100px;margin:0 auto;display:grid;grid-template-columns:1fr 400px;gap:56px;align-items:start;position:relative;z-index:1}}
.hero-badge{{display:inline-flex;align-items:center;gap:7px;background:rgba(200,146,42,.12);border:1px solid rgba(200,146,42,.3);color:var(--gold-light);padding:5px 13px;border-radius:100px;font-size:.72rem;font-weight:600;letter-spacing:.07em;text-transform:uppercase;margin-bottom:22px}}
.hero h1{{font-family:'Playfair Display',serif;font-size:clamp(2rem,4vw,3rem);font-weight:900;color:#fff;line-height:1.1;letter-spacing:-.02em;margin-bottom:18px;white-space:pre-line}}
.hero h1 em{{font-style:italic;color:var(--gold)}}
.hero-intro{{font-size:.97rem;color:rgba(255,255,255,.6);line-height:1.85;font-weight:300;margin-bottom:28px}}
.fact-pills{{display:flex;flex-wrap:wrap;gap:10px}}
.fact-pill{{background:rgba(255,255,255,.07);border:1px solid rgba(255,255,255,.12);border-radius:8px;padding:10px 14px}}
.fact-pill-value{{font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--gold-light)}}
.fact-pill-label{{font-size:.7rem;color:rgba(255,255,255,.4);margin-top:2px}}
.page-wrap{{max-width:1100px;margin:0 auto;padding:0 5%}}
.section{{padding:52px 0;border-bottom:1px solid var(--border)}}
.section:last-child{{border-bottom:none}}
.section-label{{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:10px}}
.section-title{{font-family:'Playfair Display',serif;font-size:clamp(1.5rem,2.5vw,2rem);font-weight:700;color:var(--navy);line-height:1.15;margin-bottom:14px}}
.body-text{{font-size:.95rem;color:#4a5568;line-height:1.9;font-weight:300;max-width:720px}}
.body-text p{{margin-bottom:16px}}
.law-box{{background:#fff;border:1.5px solid var(--border);border-left:4px solid var(--navy);border-radius:0 10px 10px 0;padding:20px 22px;margin-top:20px;max-width:720px}}
.law-box-title{{font-size:.75rem;font-weight:700;color:var(--navy);text-transform:uppercase;letter-spacing:.06em;margin-bottom:8px}}
.law-box p{{font-size:.87rem;color:#4a5568;line-height:1.75}}
.cta-section{{background:var(--navy);padding:60px 5%;text-align:center}}
.cta-label{{font-size:.72rem;font-weight:700;letter-spacing:.1em;text-transform:uppercase;color:var(--gold);margin-bottom:12px}}
.cta-title{{font-family:'Playfair Display',serif;font-size:1.8rem;font-weight:700;color:#fff;margin-bottom:14px;line-height:1.2}}
.cta-sub{{font-size:.95rem;color:rgba(255,255,255,.55);margin-bottom:32px;line-height:1.7}}
@media(max-width:960px){{.hero-inner{{grid-template-columns:1fr;gap:36px}}}}
</style>
</head>
<body>
{get_nav(lang)}
<section class="hero">
  <div class="hero-inner">
    <div>
      <div class="hero-badge">⚖️ eSolicitors.ie — Free Legal Matching</div>
      <h1>{page["h1"].replace("<em>", "<em>")}</h1>
      <p class="hero-intro">{page["intro"]}</p>
      <div class="fact-pills">
        <div class="fact-pill"><div class="fact-pill-value">Free</div><div class="fact-pill-label">First consultation</div></div>
        <div class="fact-pill"><div class="fact-pill-value">Remote</div><div class="fact-pill-label">No need to travel</div></div>
        <div class="fact-pill"><div class="fact-pill-value">24hr</div><div class="fact-pill-label">Avg response time</div></div>
      </div>
    </div>
    <div>
      {get_sarah_widget_html(lang, uid)}
    </div>
  </div>
</section>
<div class="page-wrap">
  <section class="section">
    <div class="section-label">The Law</div>
    <h2 class="section-title">What Irish law says</h2>
    <div class="body-text"><p>{content}</p></div>
    <div class="law-box">
      <div class="law-box-title">Legal Framework</div>
      <p>{page["law"]}</p>
    </div>
  </section>
  {f'''<section class="section">
    <div class="section-label">Real Cases</div>
    <h2 class="section-title">Others in the same situation</h2>
    {story_cards}
  </section>''' if story_cards else ''}
</div>
<div class="cta-section">
  <div style="max-width:600px;margin:0 auto 32px">
    <div class="cta-label">Free Solicitor Matching</div>
    <h2 class="cta-title">Sound familiar?<br>Get matched with a specialist.</h2>
    <p class="cta-sub">Tell {cfg["name"]} what you need. Free, confidential, no obligation. Everything handled remotely.</p>
  </div>
  {get_sarah_widget_html(lang, uid + "b")}
</div>
{get_footer(lang)}
</body>
</html>'''


# ─────────────────────────────────────────
# API CALL
# ─────────────────────────────────────────

def call_api(prompt, system="You are a specialist Irish legal content writer. Write accurate, helpful content about Irish law. Plain English. Never invent facts. Only state what is legally accurate. No markdown, no backticks. Output plain text only."):
    payload = json.dumps({
        "model": MODEL,
        "max_tokens": 1200,
        "system": system,
        "messages": [{"role": "user", "content": prompt}]
    }).encode("utf-8")
    req = urllib.request.Request(
        "https://api.anthropic.com/v1/messages",
        data=payload,
        headers={"Content-Type": "application/json", "x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        method="POST"
    )
    try:
        with urllib.request.urlopen(req) as resp:
            result = json.loads(resp.read().decode("utf-8"))
            return result["content"][0]["text"].strip()
    except urllib.error.HTTPError as e:
        print(f"  API error {e.code}: {e.read().decode()[:200]}")
        return None


# ─────────────────────────────────────────
# MAIN
# ─────────────────────────────────────────

def main():
    generated = 0
    skipped = 0
    failed = 0

    for page in PAGES:
        path = page["path"]
        lang = page["lang"]
        page_type = page.get("type", "hub")

        # ── Generate story pages ──
        if page.get("stories"):
            for story in page["stories"]:
                folder = os.path.dirname(path)
                story_path = f"{folder}/{story['slug']}/index.html"

                if os.path.exists(story_path):
                    print(f"  Skip (exists): {story_path}")
                    skipped += 1
                    continue

                print(f"  Generating story: {story_path}")
                html = build_story_html(page, story)
                os.makedirs(os.path.dirname(story_path), exist_ok=True)
                with open(story_path, "w", encoding="utf-8") as f:
                    f.write(html)
                print(f"  Saved: {story_path}")
                generated += 1
                time.sleep(0.3)

        # ── Generate hub/shallow/hire page ──
        if os.path.exists(path):
            print(f"Skip (exists): {path}")
            skipped += 1
            continue

        print(f"Generating: {path}")

        # Get main content from API
        if page_type == "hire":
            prompt = f"""Write 3 short paragraphs (plain text, no headings) for a page called "{page['title']}" on eSolicitors.ie.
Language: {lang}
Topic: {page['intro']}
Explain simply: what eSolicitors.ie does, how the matching works, why it's free.
Plain conversational language. No legal advice. No markdown."""
        else:
            prompt = f"""Write 2-3 paragraphs of plain text (no headings, no markdown) explaining the following Irish legal topic for someone outside Ireland:

Topic: {page['title']}
Audience: {page.get('audience', 'international')} — people outside Ireland
Key law: {page['law']}
Intro context: {page['intro']}

Requirements:
- Plain English, accessible, no jargon
- Accurate Irish law only — never invent facts
- Explain what happens step by step
- Mention that a solicitor can handle everything remotely
- 2-3 paragraphs, no headings, no markdown, no bullet points
- Language code: {lang} (write in this language if not English)"""

        content = call_api(prompt)
        if not content:
            print(f"  FAILED: {path}")
            failed += 1
            continue

        html = build_hub_html(page, content)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"  Saved: {path}")
        generated += 1
        time.sleep(0.5)

    print(f"\n{'='*50}")
    print(f"Done. Generated: {generated} | Skipped: {skipped} | Failed: {failed}")
    print(f"Total pages processed: {generated + skipped + failed}")


if __name__ == "__main__":
    main()
