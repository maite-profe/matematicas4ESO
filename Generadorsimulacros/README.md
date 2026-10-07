# Generador de simulacros · Matemáticas B · 4.º ESO

Cinco formatos independientes: seguimiento y examen de la primera evaluación, seguimiento y examen de la segunda, y examen de la tercera. Cada pestaña conserva su selección y el simulacro generado mientras la página permanece abierta.

## Referencias de la ampliación

Se revisó el archivo `Examenes-20260922T053351Z-1-001.zip` aportado por la profesora. La referencia principal son los exámenes de 2021–2022:

- Primera evaluación, 30 de noviembre de 2021: ecuaciones racionales, con radicales y polinómicas; clasificación de sistemas; problemas de rectángulos; factorización y teorema del resto.
- Seguimiento de la segunda, 7 de febrero de 2022: inecuaciones, sistemas de inecuaciones, relaciones y problemas de trigonometría; dominio, cortes y simetría; gráficas de situaciones cotidianas.
- Segunda evaluación, 15 de marzo de 2022: representación de funciones racionales y a trozos; interpretación de gráficas; trigonometría e inecuaciones.
- Tercera evaluación, 1 de junio de 2022: geometría analítica, combinatoria, probabilidad y repaso de logaritmos.

Se revisaron también los documentos de 2023–2024. El examen de la tercera evaluación del 17 de mayo de 2024 aporta el estudio estadístico; sus problemas de asignación de viajes y ordenaciones completan las variantes de combinatoria. Las copias de exámenes de 2021–2022 archivadas en `22-23` se identificaron por la fecha impresa y no se contaron como modelos nuevos.

**Se excluyó íntegramente la carpeta `25-26`.** Las fechas de modificación de Drive no se usan para atribuir un examen a un curso. El enlace de Drive facilitado mostró únicamente dos documentos de seguimiento de la primera evaluación; la ampliación se fundamenta en el archivo de exámenes previamente aportado.

Las 311 preguntas nuevas son variantes propias de los tipos observados, con otros datos y soluciones calculadas. El banco anterior se conserva: hay 649 preguntas en total. No se publican los documentos originales ni sus escaneos.

## Contenidos previstos y tiempos

Las casillas de los contenidos pendientes aparecen en claro y no intervienen en el tiempo ni en la generación. «Habilitar estos contenidos para elegir cuáles practicar» permite seleccionarlos individualmente. Esta opción se conserva al cambiar de pestaña, sin obligar a incluir todo el formato.

Los tiempos acordados para los bloques anteriores se mantienen. Los de los nuevos bloques son orientativos y se definen en `MINUTES`, dentro de `index.html`. Para pasar un contenido a disponible por defecto, se retira de `upcoming` en el formato correspondiente. Los bloques disponibles y previstos se definen en `FORMATS`.

La primera pestaña conserva el seguimiento original. Los nuevos formatos reúnen las ecuaciones e inecuaciones en ejercicios con apartados. Las gráficas necesarias para interpretar se incluyen en el enunciado; las gráficas que debe construir el alumnado se muestran en la solución. La impresión oculta las soluciones y adapta la extensión a la selección.

## Mantenimiento y comprobaciones

`tools/build_historical.py` reconstruye únicamente las preguntas con prefijo `H-` y conserva las demás. Ejecutarlo desde la raíz del repositorio, con Python y SymPy instalados:

```sh
python Generadorsimulacros/tools/build_historical.py
```

Los scripts localizan el banco junto a su propia carpeta y pueden ejecutarse desde cualquier directorio. Los archivos auxiliares se escriben en `tmp/`.

`tools/verify_historical.py` comprueba independientemente 168 resultados mediante lectura de las expresiones LaTeX, sustitución y cálculo estadístico. Requiere SymPy y `antlr4-python3-runtime` 4.11. Las demás familias se revisaron por sus fórmulas y condiciones. Las pruebas de navegador comprobaron los cinco formatos, la selección independiente, la conservación del estado, ausencia de repeticiones, 2.087 fórmulas nuevas renderizadas y 60 gráficas, pantalla móvil e impresión A4. El seguimiento de la primera evaluación ocupa una página; las selecciones completas probadas de segunda y tercera, dos.
