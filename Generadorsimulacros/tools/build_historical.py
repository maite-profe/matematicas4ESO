import json, math, random, pathlib, collections
import sympy as s
x=s.symbols('x',real=True)
L=s.latex
root=pathlib.Path(__file__).resolve().parents[1]
pathlib.Path('tmp').mkdir(exist_ok=True)
bank=json.loads(root.joinpath('questions.js').read_text().split('=',1)[1].rstrip().rstrip(';'))
bank=[q for q in bank if not q['id'].startswith('H-')]
new=[]; checks=[]
B={
'eqrat':'18 Ecuaciones racionales','eqrad':'19 Ecuaciones con radicales','eqpoly':'20 Ecuaciones bicuadradas y polinómicas',
'systems':'21 Clasificación de sistemas lineales','sysproblem':'22 Problemas con sistemas de ecuaciones',
'ineq':'23 Inecuaciones de segundo grado','ineqsys':'24 Sistemas de inecuaciones','trigid':'25 Relaciones trigonométricas',
'trig':'26 Problemas de trigonometría','domain':'27 Dominio, cortes y simetría','context':'28 Gráficas de situaciones cotidianas',
'rgraph':'29 Representación de funciones racionales','piece':'30 Funciones definidas a trozos','readgraph':'31 Interpretación de gráficas',
'vectors':'32 Geometría con puntos y vectores','line':'33 Ecuaciones de la recta','position':'34 Posición relativa de rectas',
'combi':'35 Problemas de combinatoria','prob':'36 Probabilidad','stats':'37 Estudio estadístico'}
def m(tex):return '\\('+str(tex)+'\\)'
def add(key,prompt,latex,answer,steps,ref='2021–2022',**extra):
 i=sum(q['block']==B[key] for q in new)+1
 q=dict(id=f'H-{key.upper()}-{i:03}',block=B[key],level='Media',prompt=prompt,latex=latex,answerLatex=answer,solution={'steps':steps},reference={'schoolYear':ref,'kind':'Variante propia de examen antiguo'},**extra)
 assert steps and answer
 new.append(q);return q
def samples(fn,lo,hi,n=100):
 return [[round(float(t),4),round(float(fn(t)),4)] for t in [lo+(hi-lo)*i/n for i in range(n+1)]]
def graph(series,bounds,markers=[]):return dict(series=series,bounds=bounds,markers=markers)
# Ecuaciones racionales con restricciones y comprobación.
for a in range(1,9):
 b=a+3; r=a+1; c=b-a
 eq=s.Eq((x+b)/(x+a)-2*(b-a)/(x+b),1)
 sols=s.solve(eq,x); valid=[t for t in sols if t not in [-a,-b]]
 numerator=s.factor(s.together(eq.lhs-eq.rhs)*(x+a)*(x+b))
 assert valid==[s.Integer(b-2*a)]
 add('eqrat','Resuelve e indica los valores excluidos del dominio.',L(eq),r'S=\{'+L(valid[0])+r'\}',[
 'Los denominadores imponen '+m(f'x\\ne {-a},\\;x\\ne {-b}')+'.',
 'Multiplicamos por el denominador común '+m(L((x+a)*(x+b)))+' y agrupamos: '+m(L(numerator)+'=0')+'.',
 'Se obtiene '+m('x='+L(valid[0]))+'. No coincide con ningún valor excluido.',
 'Comprobación en la ecuación inicial: '+m(L(eq.lhs.subs(x,valid[0]))+'=1')+'.'])
 # Una raíz algebraica excluida: exigir dominio evita falsa solución.
 eq=s.Eq((x*x-a*a)/(x-a),2*a,evaluate=False)
 assert s.simplify(eq.lhs-2*a)==x-a
 add('eqrat','Resuelve teniendo en cuenta el dominio.',L(eq),r'S=\varnothing',[
 'Debe cumplirse '+m(f'x\\ne {a}')+'.',
 'Factorizamos el numerador: '+m(L((x-a)*(x+a)))+'. Para '+m(f'x\\ne {a}')+' la fracción se reduce a '+m(f'x+{a}')+'.',
 'La ecuación da '+m(f'x+{a}={2*a}\\Rightarrow x={a}')+'.',
 'Ese valor está excluido del dominio: la ecuación no tiene solución.'])
# Radicales: resolver por elevación al cuadrado y rechazar raíces extrañas.
for a in range(2,14):
 rhs=x-a; n=a*a+2*a
 eq=s.Eq(s.sqrt(2*x+n),rhs)
 roots=s.solve((2*x+n)-rhs**2,x);valid=[v for v in roots if v>=a and s.simplify(eq.lhs.subs(x,v)-rhs.subs(x,v))==0]
 add('eqrad','Resuelve y comprueba las posibles soluciones.',L(eq),'S=\\{'+','.join(map(L,valid))+'\\}',[
 'El radical exige '+m(L(2*x+n)+r'\ge0')+' y el segundo miembro no puede ser negativo: '+m(f'x\\ge {a}')+'.',
 'Elevamos al cuadrado: '+m(L(2*x+n)+'='+L(s.expand(rhs**2)))+'.',
 'Resolvemos '+m(L(s.expand(rhs**2-2*x-n))+'=0')+': '+m('x='+L(roots[0])+r'\;\text{o}\;x='+L(roots[1]))+'.',
 'Comprobando en la ecuación original, solo '+m('x='+L(valid[0]))+' cumple las condiciones.'])
 checks.append(('radical',a,valid))
for a in range(1,9):
 poly=s.expand((x*x-a*a)*(x*x+a+1)); add('eqpoly','Resuelve la ecuación en los números reales.',L(poly)+'=0',f'S=\\{{{-a},{a}\\}}',[
 'Hacemos '+m('t=x^2')+' y resolvemos '+m(L(poly.subs(x,s.sqrt(s.Symbol('t',nonnegative=True)))))+'=0.',
 'Los valores son '+m(f't={a*a}')+' y '+m(f't={-a-1}')+'.',
 'El valor negativo de '+m('t')+' no puede ser '+m('x^2')+' para '+m(r'x\in\mathbb{R}')+'.',
 'De '+m(f'x^2={a*a}')+' resulta '+m(f'x=\\pm {a}')+'.'])
 poly=s.expand(x*x*(x-a)**2*(x+a+1));add('eqpoly','Resuelve por factorización e indica las multiplicidades.',L(poly)+'=0',f'S=\\{{{-a-1},0,{a}\\}}',[
 'Extraemos factor común y factorizamos: '+m(L(x*x*(x-a)**2*(x+a+1)))+'=0.',
 'Un producto es cero cuando al menos uno de sus factores es cero.',
 m(f'x=0')+' es doble, '+m(f'x={a}')+' es doble y '+m(f'x={-a-1}')+' es simple.'])
# Clasificación: mezcla de SCD, SCI y SI.
for i in range(12):
 a=i%4+1;b=i%3+2;c=i+4;k=i%3+2;kind=i%3
 d=k*a if kind else a+1; e=k*b if kind else b+2;f=k*c+(1 if kind==2 else 0)
 det=a*e-b*d
 if kind==0 and det==0:e+=1;det=a*e-b*d
 eq=r'\begin{cases}'+L(a*x+b*s.Symbol('y'))+'='+str(c)+r'\\'+L(d*x+e*s.Symbol('y'))+'='+str(f)+r'\end{cases}'
 if det:
  sol=s.solve([a*x+b*s.Symbol('y')-c,d*x+e*s.Symbol('y')-f],(x,s.Symbol('y')))
  answer='\\text{SCD}:\\;(x,y)=('+L(sol[x])+','+L(sol[s.Symbol('y')])+')'
  steps=['Calculamos el determinante: '+m(f'\\Delta={a}\\cdot {e}-{b}\\cdot {d}={det}\\ne0')+'.','Hay una única solución: el sistema es compatible determinado.', 'Por eliminación se obtiene '+m(answer)+'.']
 elif kind==1:
  answer=r'\text{SCI}:\quad y='+L((c-a*x)/b)
  steps=['La segunda ecuación es '+m(str(k))+' veces la primera, incluido el término independiente.','Representan la misma recta: hay infinitas soluciones y el sistema es compatible indeterminado.','Despejamos '+m('y')+' en la primera ecuación: '+m(answer)+'.']
 else:
  answer=r'\text{SI}:\quad S=\varnothing';steps=['Los coeficientes de la segunda ecuación son '+m(str(k))+' veces los de la primera, pero el término independiente no lo es.','Al restar '+m(str(k))+' veces la primera a la segunda aparece '+m('0=1')+'.','Las rectas son paralelas distintas: sistema incompatible, sin solución.']
 add('systems','Clasifica el sistema, interpreta geométricamente el resultado y resuélvelo si es posible.',eq,answer,steps)
for a,b in [(5,8),(6,10),(7,11),(8,13),(9,15),(10,14),(11,16),(12,17),(13,18),(14,19),(15,20),(16,21)]:
 p=2*(a+b);d2=a*a+b*b
 add('sysproblem',f'El perímetro de un rectángulo es {p} cm y su diagonal mide √{d2} cm. Plantea un sistema y calcula sus dimensiones.','',f'{a}\\,\\text{{cm}}\\;\\text{{y}}\\;{b}\\,\\text{{cm}}',[
 'Llamamos '+m('x,y>0')+' a sus lados. Por el perímetro y Pitágoras: '+m(f'\\begin{{cases}}x+y={a+b}\\\\x^2+y^2={d2}\\end{{cases}}')+'.',
 'Como '+m('(x+y)^2=x^2+y^2+2xy')+', se obtiene '+m(f'xy={a*b}')+'.',
 'Los lados son las raíces de '+m(f't^2-{a+b}t+{a*b}=0')+', es decir, '+m(f't={a},\\;t={b}')+'.',
 f'Comprobamos: {a} y {b} son positivos, suman {a+b} y sus cuadrados suman {d2}.'])
# Inecuaciones y sistemas con tabla de signos explícita.
for i in range(16):
 a=-5+i%5;b=a+3+i//5; strict=i%2==0; positive=i%4<2
 poly=s.expand((x-a)*(x-b));op=('>' if strict else r'\ge') if positive else ('<' if strict else r'\le')
 br=('(',')') if strict else ('[',']')
 ans=(f'(-\\infty,{a}{br[1]}\\cup{br[0]}{b},\\infty)') if positive else f'{br[0]}{a},{b}{br[1]}'
 add('ineq','Resuelve y representa el conjunto solución en la recta real.',L(poly)+op+'0',ans,[
 'Factorizamos: '+m(L(poly)+f'=(x-({a}))(x-({b}))')+'.',
 f'Los puntos críticos son {a} y {b}. El signo es positivo fuera de ellos y negativo entre ellos.',
 'Elegimos los intervalos con signo '+('positivo' if positive else 'negativo')+' y '+('excluimos' if strict else 'incluimos')+' los ceros.',
 'Solución: '+m(ans)+'. En la recta real, los extremos son '+('abiertos.' if strict else 'cerrados.')])
 a=-3+i%4;b=a+5;c=a+2
 eq=r'\begin{cases}'+L(2*x-2*c)+r'\ge0\\'+L(s.expand((x-a)*(x-b)))+r'<0\end{cases}'
 ans=f'[{c},{b})'
 add('ineqsys','Resuelve el sistema y representa su solución.',eq,ans,[
 'La primera inecuación equivale a '+m(f'x\\ge{c}')+'.',
 'La segunda se factoriza como '+m(f'(x-({a}))(x-({b}))<0')+' y da '+m(f'x\\in({a},{b})')+'.',
 'En un sistema deben cumplirse ambas: '+m(f'[{c},\\infty)\\cap({a},{b})={ans}')+'.'])
for a,b,c in [(3,4,5),(5,12,13),(8,15,17),(7,24,25),(20,21,29),(12,35,37)]:
 for sign in [1,-1]:
  quadrant='primer' if sign==1 else 'segundo';co=s.Rational(sign*b,c);si=s.Rational(a,c);ta=s.Rational(a,sign*b)
  add('trigid',f'Sabiendo que α está en el {quadrant} cuadrante, calcula cos α y tan α y justifica las relaciones utilizadas.',r'\sin\alpha='+L(si),r'\cos\alpha='+L(co)+r',\quad\tan\alpha='+L(ta),[
  'En un triángulo rectángulo, el teorema de Pitágoras dividido por el cuadrado de la hipotenusa da '+m(r'\sin^2\alpha+\cos^2\alpha=1')+'.',
  'Por tanto, '+m(r'\cos^2\alpha=1-'+L(si*si)+'='+L(co*co))+'. Elegimos el signo '+('positivo' if sign==1 else 'negativo')+' del coseno por el cuadrante.',
  'Usamos '+m(r'\tan\alpha=\frac{\sin\alpha}{\cos\alpha}')+' y obtenemos '+m(r'\tan\alpha='+L(ta))+'.'])
for i in range(12):
 alpha=25+i;beta=45+i;distance=40+10*i;t1=math.tan(math.radians(alpha));t2=math.tan(math.radians(beta));near=distance*t1/(t2-t1);h=near*t2
 add('trig',f'Desde un punto de terreno horizontal vemos la parte más alta de una torre bajo un ángulo de {alpha}°. Nos acercamos {distance} m en línea recta y el ángulo pasa a {beta}°. Calcula la altura de la torre y la distancia desde el segundo punto a su base. Supón que los ojos están a nivel del suelo. Redondea a dos decimales.','',f'h\\approx {h:.2f}\\,\\text{{m}},\\quad d\\approx {near:.2f}\\,\\text{{m}}',[
 'Llamamos '+m('d')+' a la distancia más cercana y '+m('h')+' a la altura. La distancia inicial es '+m(f'd+{distance}')+'.',
 'Las tangentes dan '+m(f'h=(d+{distance})\\tan {alpha}^\\circ=d\\tan {beta}^\\circ')+'.',
 'Despejamos '+m(f'd=\\frac{{{distance}\\tan {alpha}^\\circ}}{{\\tan {beta}^\\circ-\\tan {alpha}^\\circ}}\\approx {near:.2f}')+'.',
 'Sustituimos para la altura: '+m(f'h=d\\tan {beta}^\\circ\\approx {h:.2f}\\,\\text{{m}}')+'.'],numeric={'height':h,'distance':near,'angles':[alpha,beta],'advance':distance})
 # Isósceles: una segunda familia distinta.
 base=24+4*i;ang=40+i;hh=base/2/math.tan(math.radians(ang/2));side=base/2/math.sin(math.radians(ang/2));area=base*hh/2;per=base+2*side
 add('trig',f'La base de un triángulo isósceles mide {base} cm y el ángulo entre sus lados iguales es {ang}°. Calcula su altura, perímetro y área. Redondea a dos decimales.','',f'h\\approx{hh:.2f}\\,\\text{{cm}},\\quad P\\approx{per:.2f}\\,\\text{{cm}},\\quad A\\approx{area:.2f}\\,\\text{{cm}}^2',[
 'La altura divide el triángulo en dos triángulos rectángulos con base '+m(str(base/2))+' y ángulo superior '+m(f'{ang/2}^\\circ')+'.',
 'Por la tangente, '+m(f'h=\\frac{{{base/2}}}{{\\tan({ang/2}^\\circ)}}\\approx{hh:.2f}')+'.',
 'Por el seno, cada lado igual mide '+m(f'l=\\frac{{{base/2}}}{{\\sin({ang/2}^\\circ)}}\\approx{side:.2f}')+'.',
 'Finalmente '+m(f'P={base}+2l\\approx{per:.2f}')+' y '+m(f'A=\\frac{{{base}h}}2\\approx{area:.2f}')+'.'])
for a in range(1,7):
 for typ in ['radical','rational']:
  if typ=='radical':
   f=s.sqrt(x*x-a*a);dom=f'(-\\infty,{-a}]\\cup[{a},\\infty)';cuts=f'({-a},0),({a},0)';sym='par';calc='La raíz exige '+m(f'x^2-{a*a}\\ge0')+'.';y='No corta el eje Y porque 0 no pertenece al dominio.'
  else:
   f=(x**4-a**4)/x;dom=r'\mathbb{R}\setminus\{0\}';cuts=f'({-a},0),({a},0)';sym='impar';calc='El denominador impone '+m('x\\ne0')+'.';y='No corta el eje Y porque 0 está excluido.'
  add('domain','Calcula el dominio, los puntos de corte con los ejes y la simetría.',r'f(x)='+L(f),f'D={dom};\\quad X: {cuts};\\quad\\text{{{sym}}}',[
  calc+' Dominio: '+m(dom)+'.','Para el eje X resolvemos '+m('f(x)=0')+' y obtenemos '+m(cuts)+'.',y,
  'Comparamos '+m('f(-x)')+' con '+m('f(x)')+': '+m('f(-x)='+('f(x)' if sym=='par' else '-f(x)'))+'. Es '+sym+' y simétrica respecto '+('del eje Y.' if sym=='par' else 'del origen.')])
for i in range(12):
 a=2+i%4;b=-3+i%7;k=-2+i%5
 f=a/(x-b)+k;zero=s.Rational(k*b-a,k) if k else None;y=s.Rational(-a,b)+k if b else None
 ans=f'D=\\mathbb{{R}}\\setminus\\{{{b}\\}};\\;R=\\mathbb{{R}}\\setminus\\{{{k}\\}}'
 series=[samples(lambda t:a/(t-b)+k,b-7,b-.15),samples(lambda t:a/(t-b)+k,b+.15,b+7)]
 add('rgraph','Representa la función. Indica dominio, recorrido, cortes, asíntotas, monotonía y centro de simetría.',r'f(x)='+L(f),ans,[
 'El denominador se anula en '+m(f'x={b}')+'. Dominio: '+m(f'\\mathbb{{R}}\\setminus\\{{{b}\\}}')+'.',
 'Asíntota vertical '+m(f'x={b}')+' y horizontal '+m(f'y={k}')+'. El recorrido excluye '+m(str(k))+'.',
 'Corte con X: '+(m('('+L(zero)+',0)') if zero is not None else 'ninguno, el numerador nunca se anula')+'. Corte con Y: '+(m('(0,'+L(y)+')') if y is not None else 'ninguno, 0 no está en el dominio')+'.',
 f'Es estrictamente decreciente en cada intervalo de su dominio porque, al aumentar x sin cruzar {b}, el cociente {a}/(x−({b})) disminuye. No tiene extremos.',
 'Es una hipérbola trasladada con centro de simetría '+m(f'({b},{k})')+'. La gráfica muestra sus dos ramas.'],solutionGraph=graph(series,[b-6,b+6,k-6,k+6]),asymptotes={'x':b,'y':k})
for i in range(12):
 b=2+i%2;c=1+i%4;k=s.Rational(1,b);h=3+i%3
 tex=f'f(x)=\\begin{{cases}}{b}^{{x-{c}}}-{L(k)}&x<{c}\\\\{h}&x\\ge {c}\\end{{cases}}'
 y=s.Rational(1,b**c)-k;left=1-k;ans=f'D=\\mathbb{{R}};\\quad R=({L(-k)},{L(left)})\\cup\\{{{h}\\}}'
 series=[samples(lambda t:b**(t-c)-float(k),-5,c-.001),[[c,h],[c+5,h]]]
 add('piece','Representa la función e indica dominio, recorrido, cortes con los ejes, continuidad y monotonía.',tex,ans,[
 'Los tramos cubren todos los reales. Para '+m(f'x<{c}')+' usamos la expresión exponencial y para '+m(f'x\\ge{c}')+' la constante.',
 'La rama exponencial se aproxima a '+m('y='+L(-k))+' al ir hacia la izquierda y a '+m('y='+L(left))+' cuando '+m(f'x\\to {c}^-')+', sin alcanzar esos valores.',
 'El valor '+m(f'f({c})={h}')+' pertenece al segundo tramo. Recorrido: '+m(f'({L(-k)},{L(left)})\\cup\\{{{h}\\}}')+'.',
 'Cortes: con X en '+m(f'({c-1},0)')+' y con Y en '+m('(0,'+L(y)+')')+'.',
 f'Es continua en cada tramo y tiene un salto en x={c}. Es estrictamente creciente en (−∞,{c}) y constante en [{c},∞). El punto de la rama izquierda es abierto y el del segundo tramo es cerrado.'],solutionGraph=graph(series,[-5,c+5,-2,h+2],[{'x':c,'y':float(left),'open':True},{'x':c,'y':h,'open':False}]))
for i in range(12):
 t1=10+i*2;stay=20+i;ret=10+i;stay2=25+i;out2=15+i;stay3=30+i;ret2=20+i;d1=2+i%3;d2=5+i%4
 ts=[0,t1,t1+stay,t1+stay+ret,t1+stay+ret+stay2,t1+stay+ret+stay2+out2,t1+stay+ret+stay2+out2+stay3,t1+stay+ret+stay2+out2+stay3+ret2];ds=[0,d1,d1,0,0,d2,d2,0]
 add('context',f'Una persona sale de casa y tarda {t1} minutos en llegar a una tienda situada a {d1} km. Permanece allí {stay} minutos y regresa en {ret} minutos. Tras estar {stay2} minutos en casa, viaja a una cafetería a {d2} km en {out2} minutos. Se queda {stay3} minutos y vuelve a casa en {ret2} minutos. Dibuja la gráfica tiempo–distancia a casa, suponiendo velocidad constante en cada desplazamiento. Indica cuándo se aleja, se acerca y permanece parada.','',f'\\text{{Duración total}}={ts[-1]}\\,\\text{{min}}',[
 'El eje horizontal mide minutos y el vertical distancia a casa en kilómetros. Acumulamos los tiempos de cada etapa.',
 'Los vértices de la gráfica son '+m(r'\;'.join(f'({t},{d})' for t,d in zip(ts,ds)))+'. Los unimos por segmentos.',
 f'Se aleja en (0,{ts[1]}) y ({ts[4]},{ts[5]}). Se acerca en ({ts[2]},{ts[3]}) y ({ts[6]},{ts[7]}).',
 f'Permanece parada en [{ts[1]},{ts[2]}], [{ts[3]},{ts[4]}] y [{ts[5]},{ts[6]}].'],solutionGraph=graph([list(map(list,zip(ts,ds)))],[0,ts[-1]+5,0,d2+1]),graphLabels=['Tiempo (min)','Distancia (km)'])
# Gráfica de lectura: trazado continuo de segmentos con valores exactos.
for i in range(12):
 shift=i-5;v=i%4;points=[[shift-4,v-2],[shift-2,v+2],[shift,v],[shift+2,v],[shift+4,v+3]]
 g=graph([points],[shift-5,shift+5,v-3,v+4], [{'x':points[0][0],'y':points[0][1],'open':False},{'x':points[-1][0],'y':points[-1][1],'open':True}])
 ans=f'D=[{shift-4},{shift+4});\\;R=[{v-2},{v+3})'
 add('readgraph','A partir de la gráfica, indica dominio, recorrido, continuidad, intervalos de crecimiento, decrecimiento y constancia, y los extremos relativos interiores. Los puntos rellenos pertenecen a la gráfica; los huecos no.','',ans,[
 'La proyección sobre X da '+m(f'[{shift-4},{shift+4})')+' y sobre Y da '+m(f'[{v-2},{v+3})')+'.',
 'Los segmentos se unen sin saltos: es continua en todo su dominio.',
 'Crece en '+m(f'({shift-4},{shift-2})')+' y '+m(f'({shift+2},{shift+4})')+'; decrece en '+m(f'({shift-2},{shift})')+'; es constante en '+m(f'[{shift},{shift+2}]')+'.',
 'Máximo relativo estricto interior en '+m(f'({shift-2},{v+2})')+'. El tramo '+m(f'[{shift},{shift+2}]')+' es una meseta de mínimos locales no estrictos.'],questionGraph=g)
# Geometría analítica, rectas y posiciones.
for i in range(16):
 ax=i%5-3;ay=i%4+1;bx=ax+3+i%3;by=ay+4;cx=ax-2;cy=ay-3
 dist=s.sqrt((bx-ax)**2+(by-ay)**2);per=dist+s.sqrt((cx-bx)**2+(cy-by)**2)+s.sqrt((cx-ax)**2+(cy-ay)**2)
 mid=[s.Rational(ax+bx,2),s.Rational(ay+by,2)];sym=[2*ax-bx,2*ay-by]
 add('vectors',f'Dados A({ax},{ay}), B({bx},{by}) y C({cx},{cy}), calcula el vector AB, el punto medio de AB, el simétrico de B respecto de A y el perímetro del triángulo ABC.','',r'\overrightarrow{AB}=('+str(bx-ax)+','+str(by-ay)+r');\;M=('+','.join(map(L,mid))+r');\;B^{\prime}=('+','.join(map(str,sym))+r');\;P='+L(per),[
 'Restamos coordenadas: '+m(r'\overrightarrow{AB}=B-A=('+str(bx-ax)+','+str(by-ay)+')')+'.',
 'Promediamos las coordenadas: '+m('M=('+','.join(map(L,mid))+')')+'.',
 'A es el punto medio de '+m(r'BB^{\prime}')+', por tanto '+m(r'B^{\prime}=2A-B=('+','.join(map(str,sym))+')')+'.',
 'Usamos '+m(r'd(U,V)=\sqrt{(v_x-u_x)^2+(v_y-u_y)^2}')+' para cada lado y sumamos: '+m('P='+L(per))+' unidades.'])
 dx=2+i%3;dy=-3-i%2;y=s.Symbol('y');general=s.expand(dy*(x-ax)-dx*(y-ay));explicit=s.solve(general,y)[0]
 ans=L(general)+'=0'
 add('line',f'Escribe las ecuaciones vectorial, paramétricas, continua, general, explícita y punto–pendiente de la recta que pasa por P({ax},{ay}) y tiene vector director ({dx},{dy}).','',ans,[
 'Vectorial: '+m(f'(x,y)=({ax},{ay})+t({dx},{dy}),\\;t\\in\\mathbb{{R}}')+'.',
 'Paramétricas: '+m(f'\\begin{{cases}}x={ax}+{dx}t\\\\y={ay}+({dy})t\\end{{cases}}')+'.',
 'Continua: '+m(f'\\frac{{x-({ax})}}{{{dx}}}=\\frac{{y-({ay})}}{{{dy}}}')+'.',
 'Punto–pendiente: '+m(f'y-({ay})={L(s.Rational(dy,dx))}(x-({ax}))')+'.',
 'Al multiplicar en cruz, general: '+m(ans)+'. Al despejar, explícita: '+m('y='+L(explicit))+'.'])
for i in range(15):
 y=s.Symbol('y');a=i%3+1;b=i%4+2;c=i+2;kind=i%3;k=2+i%2
 d=k*a if kind else a+1;e=k*b if kind else -b;f=k*c+(3 if kind==2 else 0);det=a*e-b*d
 tex=r'r:\;'+L(a*x+b*y)+'='+str(c)+r'\qquad s:\;'+L(d*x+e*y)+'='+str(f)
 if det:
  sol=s.solve([a*x+b*y-c,d*x+e*y-f],(x,y));ans=r'\text{Secantes en }('+L(sol[x])+','+L(sol[y])+')'
  steps=['Determinante de los coeficientes: '+m(str(det))+', distinto de cero. Las rectas son secantes.', 'Resolvemos el sistema por eliminación y obtenemos '+m('x='+L(sol[x])+',y='+L(sol[y]))+'.','Sustituimos las coordenadas en ambas ecuaciones: satisfacen las dos rectas.']
 elif kind==1:ans=r'\text{Coincidentes}';steps=['La segunda ecuación completa es '+m(str(k))+' veces la primera.','Los coeficientes y el término independiente son proporcionales: representan la misma recta.']
 else:ans=r'\text{Paralelas distintas}';steps=['Los coeficientes de '+m('x,y')+' son proporcionales con razón '+m(str(k))+', pero los términos independientes no.','Al eliminar las incógnitas se obtiene '+m('0=3')+'. No existe punto común: paralelas distintas.']
 add('position','Estudia la posición relativa de las rectas. Si se cortan, calcula el punto de intersección.',tex,ans,steps)
# Combinatoria: cuatro familias distinguiendo orden/repetición.
for n in range(5,13):
 k=3
 for typ in range(4):
  if typ==0:prompt=f'De un grupo de {n} personas se eligen tres para tres viajes con destinos diferentes. Una persona no puede recibir dos viajes. ¿Cuántas asignaciones son posibles?';ans=math.perm(n,k);formula=f'V_{{{n},3}}={n}\\cdot{n-1}\\cdot{n-2}';why='Los destinos distinguen los puestos: importa el orden y no se repiten personas.'
  elif typ==1:prompt=f'De un grupo de {n} personas se eligen tres para el mismo viaje. ¿Cuántos grupos distintos pueden elegirse?';ans=math.comb(n,k);formula=f'C_{{{n},3}}=\\frac{{{n}!}}{{3!({n}-3)!}}';why='Solo importa quiénes forman el grupo: el orden no cambia la elección y no hay repetición.'
  elif typ==2:prompt=f'Con {n} símbolos distintos, ¿cuántos códigos de cuatro posiciones pueden formarse si se permite repetir símbolos?';ans=n**4;formula=f'VR_{{{n},4}}={n}^4';why='Hay cuatro posiciones diferentes y en cada una se dispone de los mismos símbolos: orden con repetición.'
  else:prompt=f'¿De cuántas maneras pueden sentarse {n} personas en una fila de {n} butacas?';ans=math.factorial(n);formula=f'P_{{{n}}}={n}!';why='Se ordenan todas las personas y ninguna puede repetirse.'
  add('combi',prompt,'',str(ans),[why,'Aplicamos '+m(formula+'='+str(ans))+'.'],'2021–2022' if typ in [1,2] else '2023–2024')
for i in range(12):
 pa=25+i;both=8+i%5;pb=35+i%4;union=pa+pb-both
 add('prob',f'En un grupo, al {union} % le gusta el fútbol o el baloncesto y al {both} % le gustan ambos. Al {100-pa} % no le gusta el fútbol. Calcula la probabilidad de que a una persona elegida al azar le guste el baloncesto.','',L(s.Rational(pb,100)),[
 'Sea '+m('F')+' el suceso «le gusta el fútbol» y '+m('B')+' «le gusta el baloncesto». Por el complementario '+m(f'P(F)=1-{(100-pa)/100:.2f}={pa/100:.2f}')+'.',
 'Usamos '+m(r'P(F\cup B)=P(F)+P(B)-P(F\cap B)')+'.',
 'Despejando: '+m(f'P(B)={union/100:.2f}-{pa/100:.2f}+{both/100:.2f}={pb/100:.2f}')+'.'])
 n=5+i%5;allowed=list(range(1,n+1));end=allowed[i%n];total=math.perm(n,4);fav=math.perm(n-1,3)
 add('prob',f'Un código se forma con cuatro dígitos distintos elegidos de {allowed}. Todos los códigos posibles son equiprobables. ¿Cuál es la probabilidad de que termine en {end}?','',L(s.Rational(fav,total)),[
 'Importa el orden y no se repiten dígitos. Hay '+m(f'V_{{{n},4}}={total}')+' códigos posibles.',
 f'Fijamos el último dígito en {end}; las otras tres posiciones se eligen sin repetir entre {n-1} dígitos: '+m(f'V_{{{n-1},3}}={fav}')+'.',
 'Por la regla de Laplace: '+m(f'P=\\frac{{{fav}}}{{{total}}}={L(s.Rational(fav,total))}')+'.'])
# Estadística observada en 2023–2024: frecuencias, centralización y dispersión.
rng=random.Random(2021)
for i in range(12):
 data=[rng.randrange(7) for _ in range(20)];freq=collections.Counter(data);vals=sorted(freq);ordered=sorted(data);mean=s.Rational(sum(data),20);median=s.Rational(ordered[9]+ordered[10],2);maxf=max(freq.values());modes=[v for v in vals if freq[v]==maxf];var=s.Rational(sum(v*v for v in data),20)-mean*mean;sd=s.sqrt(var);span=max(data)-min(data)
 table=r'\begin{array}{c|r|r|r}x_i&f_i&F_i&h_i\\\hline';cum=0
 for v in vals:
  cum+=freq[v];table+=f'{v}&{freq[v]}&{cum}&{L(s.Rational(freq[v],20))}\\\\'
 table+=r'\end{array}'
 answer=r'\bar x='+L(mean)+r',\;Me='+L(median)+r',\;Mo='+','.join(map(str,modes))+r',\;R='+str(span)+r',\;\sigma^2='+L(var)+r',\;\sigma\approx'+f'{float(sd):.3f}'
 add('stats','Estos datos indican los días por semana en que 20 personas hacen deporte: '+', '.join(map(str,data))+'. Construye la tabla de frecuencias absolutas, acumuladas y relativas y un diagrama de barras. Calcula media, mediana, moda, rango, varianza y desviación típica poblacionales.','',answer,[
 'La variable es cuantitativa discreta. Contamos los datos y dividimos las frecuencias por 20: '+m(table)+'.',
 'La media es '+m(r'\bar x=\frac{\sum x_if_i}{20}='+L(mean))+'. La mediana es la media de las posiciones 10 y 11: '+m(L(median))+'.',
 'La mayor frecuencia es '+str(maxf)+': moda '+m(','.join(map(str,modes)))+'. Rango: '+m(f'{max(data)}-{min(data)}={span}')+'.',
 'Usamos la varianza poblacional '+m(r'\sigma^2=\frac{\sum x_i^2f_i}{20}-\bar x^2='+L(var))+'. La desviación típica es '+m(r'\sigma=\sqrt{'+L(var)+'}\\approx'+f'{float(sd):.3f}')+'.'],ref='2023–2024',barChart={'values':vals,'frequencies':[freq[v] for v in vals]},data=data,statistics={'mean':float(mean),'median':float(median),'modes':modes,'variance':float(var),'stdev':float(sd)})
assert len({q['id'] for q in bank+new})==len(bank+new)
root.joinpath('questions.js').write_text('window.QUESTION_BANK='+json.dumps(bank+new,ensure_ascii=False,indent=2)+';\n')
pathlib.Path('tmp/historical-blocks.json').write_text(json.dumps(B,ensure_ascii=False))
pathlib.Path('tmp/historical-questions.json').write_text(json.dumps(new,ensure_ascii=False))
print('Added',len(new),'Total',len(bank+new));print(collections.Counter(q['block'] for q in new))
