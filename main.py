import re

soc_lbl = 'Social: related to community outreach, social media, health and medical, education and schools, housing, religious, poltical, and information campaign initiatives by a foreign actor'
inf_lbl = 'Infrastructure: related to energy, water supply, waste, gas supply, oil supply, roads, highways, bridges, engineering, public utilities, public transporation, construction, and critical infrastructure development initiatives by a foreign actor'
econ_lbl = 'Economic: related to financial, business, trade, international trade, or investment initiatives'
irr = "Irrelevant"
short_labels = {soc_lbl: 'Social',
                inf_lbl: 'Infrastructure',
                econ_lbl: "Economic",
                irr: 'Irrelevant'
                }

label_scores = {'Social': 0,
                'Infrastructure': 0,
                'Economic': 0,
                'Irrelevant': 0,
                }            
  
def zero_shot(text):
  labels = [  'Social: related to community outreach, social media, health and medical, education and schools, housing, religious, poltical, and information campaign initiatives by a foreign actor',      
              'Infrastructure: related to energy, water supply, waste, gas supply, oil supply, roads, highways, bridges, engineering, public utilities, public transporation, construction, and critical infrastructure development initiatives by a foreign actor',
              'Economic: related to financial, business, trade, international trade, or investment initiatives',
                "Niether economic, nor infrastructure, nor social"]
  
  prompt = "The text is about {}"

  result = classifier(text, labels, hypothesis_template=prompt)
  
  return result

def get_scores(result):

  return result['scores']

def top_category(result):
  scores = get_scores(result)
  
  if max(scores) < .5:
    
    return "Irrelevant"
  
  else:
    
    return result['labels'][scores.index(max(scores))]

def score_segment(segment):

  result = zero_shot(segment)

  category = top_category(result)

  label_scores[short_labels[category]] += len(segment)
  
def score_document(document):
  segments =re.split(r'\n|\.',document)
  segments = [seg.strip() for seg in segments]
  segments = [seg for seg in segments if len(seg)>0]
  for segment in segments:
    score_segment(segment)

score_document(document)
