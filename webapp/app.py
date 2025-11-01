# webapp/app.py
import streamlit as st
from qa_engine.nlu import extract_entities
from qa_engine.planner import plan
from qa_engine.executor import compare_states_avg_rain_and_top_crops, compose_answer

st.set_page_config(page_title='OGD QnA Prototype', layout='wide')
st.title('OGD QnA Prototype — Agriculture + Climate')
st.markdown('Ask a question about crop production and rainfall (e.g., "Compare rainfall in Karnataka and Tamil Nadu for last 5 years")')

q = st.text_input('Question', value='Compare rainfall in Karnataka and Tamil Nadu for last 5 years and list top 3 crops')
if st.button('Ask'):
    ent = extract_entities(q)
    st.write('Detected entities:', ent)
    plan_steps = plan(ent)
    st.write('Plan:', plan_steps)
    states = ent.get('states', [])
    if len(states) >= 2:
        try:
            n_years = ent.get('last_n') or 5
            top_m = ent.get('top_m') or 3
            res = compare_states_avg_rain_and_top_crops(states[0], states[1], n_years=n_years, top_m=top_m)
        except Exception as e:
            st.error('Error: ' + str(e))
        else:
            if 'error' in res:
                st.error(res['error'])
            else:
                answer = compose_answer(res)
                st.subheader('Answer (computed)')
                st.code(answer, language='text')
                st.subheader('Sources (click to open)')
                st.markdown(f"- Crop data resource page: [{res['sources']['crop_resource_page']}]({res['sources']['crop_resource_page']})")
                st.markdown(f"- Rainfall resource page: [{res['sources']['rain_resource_page']}]({res['sources']['rain_resource_page']})")
    else:
        st.info('Please type two state names (e.g., Karnataka and Tamil Nadu) with capitalization for detection.')

