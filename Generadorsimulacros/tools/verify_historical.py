import json,re,math,statistics,pathlib
import sympy as s
from sympy.parsing.latex import parse_latex as parse
bank=json.loads((pathlib.Path(__file__).resolve().parents[1]/'questions.js').read_text().split('=',1)[1].rstrip().rstrip(';'))
qs=[q for q in bank if q['id'].startswith('H-')];counts={}
def tally(k):counts[k]=counts.get(k,0)+1
def expected_roots(tex):
 if 'varnothing' in tex:return set()
 t=tex.removeprefix('S=\\{').removesuffix('\\}')
 return set(parse(v.strip()) for v in t.split(','))
def interval(tex):
 def n(t):return -s.oo if t=='-\\infty' else s.oo if t=='\\infty' else s.Rational(t)
 parts=[]
 for p in tex.split('\\cup'):
  a,b=p[1:-1].split(',');parts.append(s.Interval(n(a),n(b),left_open=p[0]=='(',right_open=p[-1]==')'))
 return s.Union(*parts)
for q in qs:
 kind=q['id'].split('-')[1]
 if kind in ['EQRAT','EQRAD','EQPOLY']:
  eq=parse(q['latex']);xx=s.Symbol('x');roots=[r for r in s.solve(eq,xx) if s.simplify(s.im(r))==0]
  actual=set(roots);expected=expected_roots(q['answerLatex']);assert len(actual)==len(expected),(q['id'],actual,expected)
  assert all(any(s.simplify(a-b)==0 for b in expected) for a in actual),(q['id'],actual,expected)
  # Substitute each claimed root into the original printed equation.
  for r in expected:assert s.simplify(eq.lhs.subs(xx,r)-eq.rhs.subs(xx,r))==0,q['id']
  tally('equations')
 elif kind=='INEQ':
  rel=parse(q['latex']);sol=s.solve_univariate_inequality(rel,s.Symbol('x'),relational=False)
  assert sol==interval(q['answerLatex']),(q['id'],sol,q['answerLatex']);tally('inequalities')
 elif kind=='RGRAPH':
  expr=parse(q['latex'].split('=',1)[1]);xx=s.Symbol('x');f=s.lambdify(xx,expr,'math')
  for line in q['solutionGraph']['series']:
   for px,py in line:assert abs(f(px)-py)<.03,(q['id'],px,py,f(px))
  assert s.limit(expr,xx,s.oo)==q['asymptotes']['y'];tally('function graphs')
 elif kind=='STATS':
  d=q['data'];v=q['statistics'];assert abs(statistics.mean(d)-v['mean'])<1e-12
  assert statistics.median(d)==v['median'];assert set(statistics.multimode(d))==set(v['modes'])
  assert abs(statistics.pvariance(d)-v['variance'])<1e-12;assert abs(statistics.pstdev(d)-v['stdev'])<1e-12;tally('statistics')
 elif kind=='TRIG' and 'numeric' in q:
  v=q['numeric'];a,b=v['angles'];hh=v['height'];dd=v['distance'];assert abs(hh/dd-math.tan(math.radians(b)))<1e-12
  assert abs(hh/(dd+v['advance'])-math.tan(math.radians(a)))<1e-12;tally('trigonometry')
 elif kind=='LINE':
  points=re.findall(r'\((-?\d+),(-?\d+)\)',q['prompt']);(a,b),(dx,dy)=[tuple(map(int,p)) for p in points]
  eq=parse(q['answerLatex']);xx,yy=s.symbols('x y')
  for t in [0,1,2,-3]:assert s.simplify(eq.lhs.subs({xx:a+t*dx,yy:b+t*dy})-eq.rhs)==0
  tally('line equations')
 elif kind=='COMBI':
  n=int(re.search(r'\d+',q['prompt']).group());text=q['prompt']
  if 'destinos diferentes' in text:ans=math.perm(n,3)
  elif 'mismo viaje' in text:ans=math.comb(n,3)
  elif 'códigos' in text:ans=n**4
  else:ans=math.factorial(n)
  assert int(q['answerLatex'])==ans;q['verification']='passed';tally('combinatorics')
 elif kind=='PROB':
  if 'baloncesto' in q['prompt']:
   union,both,nonf=[int(v) for v in re.findall(r'(\d+) %',q['prompt'])];ans=s.Rational(union-(100-nonf)+both,100)
  else:
   digits=re.search(r'\[([^]]+)\]',q['prompt']).group(1).split(',');ans=s.Rational(1,len(digits))
  assert s.simplify(parse(q['answerLatex'])-ans)==0;q['verification']='passed';tally('probability')
assert not any(q['reference']['schoolYear']=='2025–2026' for q in qs)
assert len({q['id'] for q in bank})==len(bank)
print('PASS independent checks:',counts,'total',sum(counts.values()))
