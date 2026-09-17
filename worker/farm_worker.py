import json, os, sys
from datetime import datetime, timezone

role = os.environ.get('ROLE','UNKNOWN_ROLE')
model = os.environ.get('MODEL','huggingface-projects/llama-3.2-3B-Instruct')
mission = os.environ.get('MISSION','Analyze the economics/finance question rigorously.')

prompt = f'''You are {role} in CEREBRON OMEGA Farm 21 Economics Finance.
Mission: {mission}
Rules: REALITY > COHERENCE; CLAIM <= EVIDENCE; FORECAST != FACT; MODEL != REALITY; CORRELATION != CAUSATION; UNKNOWN REMAINS UNKNOWN.
Make assumptions explicit. Distinguish ESTABLISHED / SUPPORTED / PLAUSIBLE / SPECULATIVE / CONFLICTED / UNKNOWN. Report uncertainty, time period, geography, units, data vintage and sensitivity when relevant.
Return a concise technical analysis with claims, assumptions, counterarguments, verification needs, and residual unknowns.'''

result = {
  'role': role,
  'model': model,
  'status': 'UNREVIEWED_EXTERNAL_AGENT_OUTPUT',
  'timestamp_utc': datetime.now(timezone.utc).isoformat(),
  'prompt': prompt,
  'output': None,
  'error': None
}

try:
    from gradio_client import Client
    client = Client(model)
    try:
        out = client.predict(message=prompt, api_name='/chat')
    except Exception:
        try:
            out = client.predict(prompt, api_name='/chat')
        except Exception:
            out = client.predict(prompt)
    result['output'] = out
except Exception as e:
    result['error'] = repr(e)

os.makedirs('results', exist_ok=True)
path = f"results/{role}.json"
with open(path,'w',encoding='utf-8') as f:
    json.dump(result,f,ensure_ascii=False,indent=2,default=str)
print(path)
if result['error']:
    sys.exit(1)
