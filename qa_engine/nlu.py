# qa_engine/nlu.py
import re

INDIAN_STATES = [
 'Andhra Pradesh','Arunachal Pradesh','Assam','Bihar','Chhattisgarh','Goa','Gujarat','Haryana',
 'Himachal Pradesh','Jharkhand','Karnataka','Kerala','Madhya Pradesh','Maharashtra','Manipur',
 'Meghalaya','Mizoram','Nagaland','Odisha','Punjab','Rajasthan','Sikkim','Tamil Nadu','Telangana',
 'Tripura','Uttar Pradesh','Uttarakhand','West Bengal','Delhi','Jammu and Kashmir','Ladakh'
]

COMMON_CROPS = ['rice','wheat','maize','sugarcane','cotton','millet','groundnut','pulses','paddy']

def find_states(text):
    found = []
    tl = text.lower()
    for s in INDIAN_STATES:
        if re.search(r'\b' + re.escape(s.lower()) + r'\b', tl):
            found.append(s)
    # fallback: capitalized words
    if not found:
        caps = re.findall(r'([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)', text)
        for c in caps:
            if c in INDIAN_STATES and c not in found:
                found.append(c)
    return found

def extract_entities(question):
    q = question.strip()
    ql = q.lower()
    intent = None
    if any(w in ql for w in ['compare','comparison']):
        intent='compare'
    if 'trend' in ql:
        intent='trend'
    if re.search(r'\btop\b', ql):
        intent='top_m'
    if any(w in ql for w in ['highest','lowest','maximum','minimum']):
        intent='max_min'
    years4 = re.findall(r'\b(19\d{2}|20\d{2})\b', q)
    m = re.search(r'last\s+(\d+)\s+year', ql)
    last_n = int(m.group(1)) if m else None
    m2 = re.search(r'top\s+(\d+)', ql)
    top_m = int(m2.group(1)) if m2 else None
    states = find_states(q)
    crops = [c for c in COMMON_CROPS if c in ql]
    return {'intent':intent, 'years':years4, 'last_n':last_n, 'states':states, 'crops':crops, 'top_m':top_m}

