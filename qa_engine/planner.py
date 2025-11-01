# qa_engine/planner.py
def plan(entities):
    plan = []
    intent = entities.get('intent')
    if intent in ('compare','trend','top_m','max_min'):
        plan.append('crop_production')
        plan.append('rainfall')
    return plan

