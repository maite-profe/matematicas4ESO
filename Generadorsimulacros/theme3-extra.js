(function(){
  const bank=window.QUESTION_BANK||(window.QUESTION_BANK=[]);
  const add=(block,prefix,items)=>items.forEach((item,i)=>bank.push({id:`${prefix}-${String(i+1).padStart(2,'0')}`,block,level:'Media',prompt:item[2]||'Resuelve:',latex:item[0]||'',answerLatex:item[1]||'',answer:item[3]||'',solution:{steps:[]}}));

  add('20A Ecuaciones exponenciales','EXP',[
    ['2^{x+1}=16','x=3'],['3^{2x-1}=27','x=2'],['5^{x-2}=\\frac1{25}','x=0'],['4^x=2^{x+3}','x=3'],['9^x=27','x=\\frac32'],
    ['2^{2x}-5\\cdot2^x+4=0','x=0,\\;2'],['3^{2x}-10\\cdot3^x+9=0','x=0,\\;2'],['5^x+5^{x+1}=750','x=3'],['2^x+2^{x+1}=24','x=3'],['4^x-5\\cdot2^x+4=0','x=0,\\;2']
  ]);

  add('20B Ecuaciones logarítmicas','ELOG',[
    ['\\log_2(x-1)=3','x=9'],['\\log_3(x+2)=2','x=7'],['\\log x=2','x=100'],['\\log_5(2x-1)=2','x=13'],
    ['\\log_2x+\\log_2(x-2)=3','x=4'],['\\log_3(x+1)-\\log_3(x-1)=1','x=2'],['2\\log x=\\log49','x=7'],
    ['\\log_2x+\\log_2(x-3)=2','x=4'],['\\log(x-1)=\\log(3x-7)','x=3'],['\\log_2(x^2-5x+6)=1','x=1,\\;4']
  ]);

  add('20C Ecuaciones con factores','EFAC',[
    ['(x-3)(x+2)=0','x=3,\\;-2'],['(x+1)(x-4)(x-2)=0','x=-1,\\;2,\\;4'],['x(x-5)(2x+1)=0','x=0,\\;5,\\;-\\frac12'],
    ['(x^2-9)(x-1)=0','x=-3,\\;1,\\;3'],['(3x-6)(x^2-4)=0','x=-2,\\;2'],['(x^2-5x+6)(x+1)=0','x=-1,\\;2,\\;3'],
    ['(x-4)^2(x+3)=0','x=4,\\;-3'],['(2x-6)(x^2+1)=0','x=3'],['(x+2)(x^2-4x)=0','x=-2,\\;0,\\;4'],['(x^2-1)(x^2-4)=0','x=-2,\\;-1,\\;1,\\;2']
  ]);

  add('21A Sistemas de ecuaciones no lineales','SNL',[
    ['\\begin{cases}x+y=7\\\\xy=12\\end{cases}','(x,y)=(3,4),(4,3)'],
    ['\\begin{cases}x-y=1\\\\x^2+y^2=25\\end{cases}','(x,y)=(4,3),(-3,-4)'],
    ['\\begin{cases}x+y=5\\\\x^2+y^2=13\\end{cases}','(x,y)=(2,3),(3,2)'],
    ['\\begin{cases}y=x^2\\\\x+y=6\\end{cases}','(x,y)=(2,4),(-3,9)'],
    ['\\begin{cases}y=2x\\\\x^2+y^2=20\\end{cases}','(x,y)=(2,4),(-2,-4)'],
    ['\\begin{cases}x^2+y^2=25\\\\y=3\\end{cases}','(x,y)=(4,3),(-4,3)'],
    ['\\begin{cases}xy=8\\\\x+y=6\\end{cases}','(x,y)=(2,4),(4,2)'],
    ['\\begin{cases}y=x+1\\\\xy=12\\end{cases}','(x,y)=(3,4),(-4,-3)'],
    ['\\begin{cases}y=x^2\\\\x+y=2\\end{cases}','(x,y)=(1,1),(-2,4)'],
    ['\\begin{cases}x-y=2\\\\xy=15\\end{cases}','(x,y)=(5,3),(-3,-5)']
  ]);

  add('24A Sistemas de inecuaciones con dos incógnitas','SI2',[
    ['\\begin{cases}2x+y\\le4\\\\3x-2y>0\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Intersección de los semiplanos \\(y\\le4-2x\\) e \\(y<\\frac32x\\).'],
    ['\\begin{cases}x+y\\le5\\\\2x-3y\\le0\\\\y\\ge0\\\\x>-1\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Recinto común: \\(y\\le5-x\\), \\(y\\ge\\frac23x\\), \\(y\\ge0\\) y \\(x>-1\\).'],
    ['\\begin{cases}x+y\\le6\\\\x\\ge0\\\\y\\ge0\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Triángulo cerrado de vértices \\((0,0)\\), \\((6,0)\\) y \\((0,6)\\).'],
    ['\\begin{cases}y>x-1\\\\y\\le-x+5\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Región situada por encima de \\(y=x-1\\) y sobre o por debajo de \\(y=-x+5\\).'],
    ['\\begin{cases}x\\ge1\\\\y\\ge1\\\\x+y\\le5\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Triángulo cerrado de vértices \\((1,1)\\), \\((4,1)\\) y \\((1,4)\\).'],
    ['\\begin{cases}2x+y<6\\\\x-y\\ge0\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Intersección de \\(y<6-2x\\) e \\(y\\le x\\).'],
    ['\\begin{cases}x+y\\ge2\\\\x+y\\le6\\\\x\\ge0\\\\y\\ge0\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Franja cerrada del primer cuadrante comprendida entre \\(x+y=2\\) y \\(x+y=6\\).'],
    ['\\begin{cases}y\\ge2x-2\\\\y<-x+4\\\\x\\ge0\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Región a la derecha del eje \\(Y\\), sobre \\(y=2x-2\\) y bajo \\(y=-x+4\\).'],
    ['\\begin{cases}x\\le3\\\\y\\le2\\\\x+y\\ge1\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Intersección de \\(x\\le3\\), \\(y\\le2\\) y \\(x+y\\ge1\\).'],
    ['\\begin{cases}x-y>0\\\\2x+y\\le8\\\\y\\ge0\\end{cases}','', 'Resuelve y representa gráficamente el sistema:', 'Región con \\(y<x\\), \\(y\\le8-2x\\) e \\(y\\ge0\\).']
  ]);

  add('22A Problemas de ecuaciones','PEQ',[
    ['', 'x=13', 'La suma de un número y su doble es 39. Calcula el número.'],
    ['', 'x=12', 'El cuadrado de un número positivo supera en 132 unidades al propio número. Halla dicho número.'],
    ['', 'x=8', 'La suma de dos números consecutivos es 17. Calcula el menor.'],
    ['', 'x=9', 'Un rectángulo tiene 3 cm más de largo que de ancho y su área es 108 cm². Calcula el ancho.'],
    ['', 'x=15', 'El perímetro de un rectángulo es 70 cm y el largo mide 5 cm más que el ancho. Calcula el ancho.'],
    ['', 'x=20', 'Dentro de 5 años, la edad de Lucía será el doble de la que tenía hace 5 años. ¿Qué edad tiene ahora?'],
    ['', 'x=6', 'El producto de un número natural por su consecutivo es 42. Calcula el menor.'],
    ['', 'x=10', 'La diagonal de un rectángulo mide 26 cm y uno de sus lados mide 24 cm. Calcula el otro lado.'],
    ['', 'x=25', 'Después de aumentar un precio un 20 %, se obtienen 30 €. Calcula el precio inicial.'],
    ['', 'x=7', 'El cuadrado de un número menos cinco veces dicho número es 14. Halla la solución positiva.']
  ]);
})();
