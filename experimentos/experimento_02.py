#!/usr/bin/env python3
"""Generaciones del voto · Experimento 02
"""
import argparse
import hashlib
import itertools
import json
import platform
import re
import zipfile
from pathlib import Path

import numpy as np
import pandas as pd

YEARS = [2009, 2012, 2015, 2018, 2021, 2024]
BANDS = [18, 21, 24, 27]
COUNTS = ['LN', 'SV', 'NV', 'NS']
EXPECTED_DATES = {2009:'5/7/2009',2012:'1/7/2012',2015:'7/6/2015',
                  2018:'1/7/2018',2021:'6/6/2021',2024:'06/02/2024'}
VERSION = '2.0'
TEMPLATE = '<!doctype html>\n<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">\n<title>Generaciones del voto · Explorador 02</title>\n<style>\n:root{--ink:#142c3a;--muted:#617481;--paper:#f4f5f1;--line:#dce3df;--teal:#087f83;--gold:#d39b41;--navy:#102c3a}*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font:15px/1.5 system-ui,-apple-system,Segoe UI,sans-serif}header{background:var(--navy);color:#fff;padding:30px 5% 28px;position:relative}header:after{content:\'2009 → 2024\';position:absolute;right:5%;bottom:32px;color:#9ccecc;font:600 24px monospace}.eyebrow{font-size:11px;text-transform:uppercase;letter-spacing:2px;color:#9ccecc}h1{font-size:clamp(28px,4vw,42px);letter-spacing:-1.4px;margin:8px 0}header p{margin:0;color:#c5d5db;max-width:65%}main{max-width:1500px;margin:auto;padding:24px 4% 50px}h2{font-size:21px;letter-spacing:-.4px;margin:0 0 6px}h3{font-size:16px;margin:0 0 12px}.sub{color:var(--muted);font-size:13px;margin:0 0 16px}.notice{border-left:4px solid var(--gold);padding:13px 18px;background:#fff5df;font-size:13px;margin:0 0 22px}.controls{display:grid;grid-template-columns:1.25fr .8fr 1.2fr 1.1fr 1.4fr;gap:14px;background:white;padding:18px;border:1px solid var(--line);border-radius:12px}label{display:block;font-size:11px;font-weight:700;text-transform:uppercase;letter-spacing:.5px;color:var(--muted)}select,input{width:100%;background:#fff;border:1px solid #c7d3d1;border-radius:6px;padding:10px 8px;color:var(--ink);margin-top:5px;font:14px system-ui}input:focus,select:focus,button:focus-visible{outline:3px solid #a6d6d3;outline-offset:2px}button{border:1px solid #bccfca;background:white;color:var(--ink);padding:8px 12px;border-radius:6px;cursor:pointer;font:600 12px system-ui}button:hover{background:#e9f3f0}button.active{background:var(--teal);color:white;border-color:var(--teal)}button:disabled{opacity:.45;cursor:not-allowed}.stats{display:grid;grid-template-columns:repeat(4,1fr);gap:14px;margin:18px 0}.stat{background:white;padding:18px;border:1px solid var(--line);border-radius:10px}.stat b{display:block;font-size:29px;letter-spacing:-1px}.stat span{font-size:12px;color:var(--muted)}nav{display:flex;gap:8px;margin:22px 0;flex-wrap:wrap}nav button{padding:11px 17px}section[hidden]{display:none}.card{min-width:0;overflow-x:auto;background:white;border:1px solid var(--line);border-radius:12px;padding:24px;margin-bottom:18px}.grid{display:grid;grid-template-columns:1.4fr 1fr;gap:18px}.row{display:flex;gap:12px;align-items:center;flex-wrap:wrap;justify-content:space-between}.chip{display:inline-flex;gap:8px;align-items:center;background:#eaf4f1;border:1px solid #c9ded7;border-radius:30px;padding:5px 10px;margin:3px;font-size:12px}.chip button{border:0;background:transparent;padding:0 3px}.pill{display:inline-block;padding:3px 7px;border-radius:5px;background:#fff2d6;color:#77551d;font-size:11px}.good{background:#e1f3ea;color:#216247}.chart{width:100%;height:auto;min-height:240px}.axis{font:12px system-ui;fill:#667a83}.gridline{stroke:#e4ebe7;stroke-width:1}.data-dot{cursor:pointer}.data-dot:hover{stroke:#142c3a;stroke-width:3}.muted{color:var(--muted)}.small{font-size:12px}table{border-collapse:collapse;width:100%;font-size:12px}th{text-align:left;color:var(--muted);background:#f6f8f5;position:sticky;top:0;font-size:11px}td,th{padding:10px;border-bottom:1px solid #e5ebe7}tbody tr:hover{background:#f0f7f4}.tablewrap{overflow:auto;max-height:440px;margin-top:12px}#tooltip{display:none;position:fixed;z-index:100;background:#102c3a;color:white;padding:13px 16px;border-radius:9px;font-size:12px;box-shadow:0 8px 30px #102c3a40;pointer-events:none;max-width:310px}#tooltip strong{font-size:14px;display:block;margin-bottom:4px}a{color:var(--teal)}details{border-top:1px solid var(--line);padding:14px 0}summary{cursor:pointer;font-weight:600}code,pre{font:12px/1.6 monospace;background:#f1f5f2;white-space:pre-wrap;overflow-wrap:anywhere}pre{padding:16px}footer{font-size:12px;color:var(--muted);border-top:1px solid var(--line);padding-top:20px}.empty{padding:40px 20px;border:1px dashed #b9cbc5;border-radius:8px;background:#f7faf7;text-align:center;color:var(--muted)}.keyline{width:25px;display:inline-block;border-top:2px solid;margin-right:6px;vertical-align:middle}#legend{font-size:12px;margin:12px 0}.filehash{max-width:240px;overflow-wrap:anywhere;font:10px monospace}.hscroll{overflow:auto}#modelMetrics .stats{grid-template-columns:repeat(3,1fr)}.two{display:grid;grid-template-columns:1fr 1fr;gap:16px}ul{padding-left:20px}.statusline{color:#835d20;font-size:12px;margin-top:8px}@media(max-width:950px){header:after{display:none}header p{max-width:100%}.controls{grid-template-columns:1fr 1fr}.grid,.two{grid-template-columns:1fr}.stats{grid-template-columns:1fr 1fr}.card{padding:16px}}@media(max-width:500px){#modelMetrics .stats{grid-template-columns:1fr 1fr}.chart{min-width:640px}main{padding:18px 12px}.controls{grid-template-columns:1fr}.stat b{font-size:24px}h1{font-size:30px}}\n.profilegrid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:14px;margin:18px 0}.profile{border:1px solid var(--line);border-top:4px solid;border-radius:9px;padding:16px;min-width:0}.profile h3{font-size:15px}.profile svg{width:100%;height:auto}.profile button{margin:4px 2px;font-size:11px}.profile p{font-size:12px}@media(max-width:950px){.profilegrid{grid-template-columns:1fr 1fr}}@media(max-width:600px){.profilegrid{grid-template-columns:1fr}}</style></head><body>\n<header><div class="eyebrow">Investigación electoral · Experimentos 01 + 02</div><h1>Generaciones del voto</h1><p>Explora cohortes juveniles de 2009 a lo largo de seis elecciones. Observaciones agregadas, territorios y trayectorias.</p></header>\n<main>\n<div id="status" class="notice"></div>\n<div class="controls">\n <label>Cohorte inicial · 2009<select id="cohort"><option value="0">18–20 años → 33–35 en 2024</option><option value="1">21–23 años → 36–38 en 2024</option><option value="2">24–26 años → 39–41 en 2024</option><option value="3">27–29 años → 42–44 en 2024</option></select></label>\n <label>Sexo registrado<select id="sex"><option value="0">Hombres (0)</option><option value="1">Mujeres (1)</option></select></label>\n <label>Entidad<select id="state"></select></label>\n <label>Indicador<select id="metric"><option value="centered">Trayectoria centrada · pp</option><option value="p">SV / LN · %</option><option value="specified">SV / (SV + NV) · %</option><option value="q">NS / LN · %</option><option value="relative">Diferencia ref. nacional · pp</option></select></label>\n <label>Buscar municipio<input id="search" placeholder="Nombre o clave INE…" type="search"></label>\n</div>\n<div class="stats"><div class="stat"><b id="nMunicipal">—</b><span>Municipios en la selección</span></div><div class="stat"><b id="nComplete">—</b><span>Con seis agregados válidos</span></div><div class="stat"><b id="nGeo">—</b><span>Con el mismo conjunto de secciones</span></div><div class="stat"><b id="nMissing">—</b><span>Observaciones ausentes o no válidas</span></div></div>\n<nav aria-label="Vistas"><button class="active" data-tab="trajectories">01 / Trayectorias</button><button data-tab="comparison">02 / Comparador</button><button data-tab="clusters">03 / Agrupamientos</button><button data-tab="quality">04 / Calidad y método</button></nav>\n<section id="trajectories"><div class="card"><div class="row"><div><h2>Una cohorte, seis momentos</h2><p class="sub">Pasa el cursor por un punto para consultar sus conteos. Haz clic para añadir el municipio al comparador.</p></div><button id="download">Descargar selección CSV</button></div><div id="lineCaption" class="small muted"></div><svg id="lines" class="chart" viewBox="0 0 1000 390" role="img" aria-label="Trayectorias por municipio"></svg><div class="small muted">Líneas discontinuas: continuidad territorial pendiente. No prueban persistencia de una población o territorio constante. Los huecos no se interpolan.</div></div>\n<div class="grid"><div class="card"><h2>Inicio y final observados</h2><p class="sub">Cada punto es un municipio: 2009 en el eje horizontal y 2024 en el vertical. No es una proyección de clústeres.</p><svg id="scatter" class="chart" viewBox="0 0 600 380" role="img" aria-label="Comparación entre 2009 y 2024"></svg><p id="scatterCaption" class="small muted"></p></div><div class="card"><h2>Encuentra un municipio</h2><p class="sub">Usa la búsqueda superior o añade municipios desde la tabla. El comparador conserva las selecciones al cambiar de entidad.</p><div id="municipalTable" class="tablewrap"></div><div class="row small" style="margin-top:10px"><button id="prev">← Anterior</button><span id="pageLabel"></span><button id="next">Siguiente →</button></div></div></div></section>\n<section id="comparison" hidden><div class="card"><h2>Comparador de territorios</h2><p class="sub">Hasta ocho municipios. La cohorte, el sexo y el indicador siguen los filtros superiores; entidad y búsqueda no ocultan los municipios fijados.</p><div id="pins"></div><svg id="compareChart" class="chart" viewBox="0 0 1000 390" role="img" aria-label="Trayectorias de municipios seleccionados"></svg><div id="legend"></div><div id="compareTable" class="tablewrap"></div><button id="clearPins">Vaciar comparador</button></div></section>\n<section id="clusters" hidden><div class="card"><div class="row"><h2>Agrupamientos y estabilidad</h2><button id="downloadClusters">Descargar clasificación CSV</button></div><p class="sub">Los modelos exploratorios se ajustan por cohorte y sexo, con seis observaciones válidas. La continuidad cartográfica no se da por verificada. Los filtros de entidad no vuelven a ajustar el modelo. El experimento 02 abre seis perfiles candidatos para examinarlos; puedes contrastar de dos a ocho grupos. No son seis tipos universales ni una solución validada. El experimento 01 abre la mayor silueta del estrato. Los números de grupo no equivalen entre modelos.</p><div id="modelStatus"></div><div class="two" style="margin:18px 0"><label>Experimento<select id="experiment"><option value="centered">02 · Forma de la trayectoria</option><option value="level">01 · Nivel de participación</option></select></label><label>Solución<select id="model"></select></label><label>Grupo<select id="clusterGroup"></select></label></div><div id="modelMetrics"></div><h3>Perfiles candidatos de esta cohorte y sexo</h3><p class="small muted">Curvas medias del modelo completo, sin filtrar por entidad. Los nombres describen extremos y máximos observados, no comportamiento individual. Ejemplos: municipios cercanos al centroide, hasta tres entidades distintas. Pulsa un ejemplo para incorporarlo al comparador.</p><div id="profiles" class="profilegrid"></div><div id="transition" class="hscroll"></div><h3>Perfiles medios de los grupos</h3><p class="small muted">Media simple de porcentajes municipales, según el indicador seleccionado. Pasa el cursor por cada celda. Estos grupos no son aún los seis perfiles institucionales.</p><div id="groupSummary" class="hscroll"></div><h3 style="margin-top:24px">Sensibilidad al retirar una elección</h3><svg id="stabilityPlot" class="chart" viewBox="0 0 1000 230" aria-label="ARI al retirar cada elección"></svg><svg id="clusterChart" class="chart" viewBox="0 0 1000 390" role="img" aria-label="Trayectorias por agrupamiento"></svg><div id="clusterTable" class="tablewrap"></div></div></section>\n<section id="quality" hidden><div class="card"><h2>Qué sabemos y qué falta verificar</h2><div class="two"><div><h3>Lectura correcta de los datos</h3><ul class="small"><li>Son cohortes aproximadas por edad cumplida en cada jornada; las fechas cambian y sus límites de nacimiento no coinciden exactamente.</li><li>No se sigue a los mismos individuos. Migración y cambios del registro pueden modificar la composición.</li><li>SV: marca de voto; NV: sin marca; NS: participación no especificada; LN: lista nominal contabilizada.</li><li>No se contempla la participación en casillas especiales ni desde el extranjero, según los diccionarios.</li><li>El código 2 de 2024 no se reconstruye en años anteriores. 2025 es una extensión independiente, fuera de este experimento.</li></ul></div><div><h3>Controles que condicionan el modelo</h3><ul class="small"><li>No hay imputación, interpolación ni sustitución por ceros.</li><li>Una clave repetida por sección, edad y sexo invalida los agregados afectados; no se deduplica automáticamente.</li><li>Se exige LN positivo, identidad LN = SV + NV + NS y las tres edades representadas en el agregado municipal.</li><li>No se ha demostrado cobertura completa de secciones contra un catálogo externo.</li><li>El catálogo geográfico adjunto contiene nombres, no polígonos: no se fabrica un mapa municipal.</li><li>Modo exploratorio autorizado: la continuidad territorial pendiente no impide ajustar modelos. Se contrasta la solución al restringirla a municipios con el mismo conjunto de secciones en las seis elecciones. Esa estabilidad observada no demuestra límites cartográficos invariables.</li></ul></div></div>\n<details open><summary>Resumen de auditoría · todos los registros de los seis ZIP ordinarios</summary><div id="auditSummary" class="hscroll"></div><p class="small muted">Las incidencias pueden solaparse. Los conteos abarcan todas las edades y categorías de los archivos, no sólo las cuatro cohortes del explorador.</p></details>\n<details><summary>Observaciones de esta selección y motivo de exclusión</summary><div id="exclusionTable" class="tablewrap"></div></details>\n<details><summary>Modelos, parámetros y comparación de soluciones</summary><p class="small">K-means: k=2…8, k-means++, n_init=50, max_iter=500, tol=0.0001, semillas 0…19; ajuste mostrado: semilla 0. Ward: enlace de mínima variación con distancia euclidiana. Cada municipio y elección tienen el mismo peso. Experimento 01: seis tasas en escala porcentual. Experimento 02: se resta a cada municipio su propia media de las seis elecciones; se conservan las amplitudes en puntos porcentuales, sin dividir por desviación estándar. Al retirar una elección se vuelve a centrar con las cinco restantes. Las siluetas de espacios distintos no se comparan como si midieran la misma estructura. Se exploran k=2…8; k=6 se abre para examinar candidatos, no por superioridad estadística. La estabilidad de cada grupo usa el máximo Jaccard frente a los grupos del reajuste sin una elección: se reportan mínimo y media de seis reajustes. No es una probabilidad de pertenencia.</p><p class="small">Silueta: cohesión y separación. ARI: acuerdo de particiones; se comparan todos los pares de semillas y se excluye una elección cada vez. Sensibilidad: repetir con SV/(SV+NV) sobre las mismas unidades con denominador válido. Ninguna métrica acredita por sí sola validez sociológica. No se identifican efectos causales de edad, periodo o cohorte.</p><p class="small">Restar la misma referencia nacional a todos los municipios de un estrato no altera las distancias euclidianas; la vista relativa es interpretativa, no un modelo distinto. La referencia nacional usa razones de sumas de todos los conteos disponibles del estrato/año, incluidos los municipios con edades ausentes; no se imputan esas ausencias. No se presenta si se detectan errores de conteos. Es una referencia de registros disponibles, no una garantía de cobertura nacional completa.</p></details>\n<details><summary>Reproducir el experimento y elegir el modo</summary><pre>pip install numpy pandas scipy scikit-learn threadpoolctl\npython experimento_02.py --input-dir ./originales --output-dir ./resultados\n\n# Modo exploratorio (predeterminado):\npython experimento_02.py --input-dir ./originales --output-dir ./resultados --reuse --mode exploratory\n\n# Alternativa estricta, sólo con evidencia territorial revisada:\npython experimento_02.py --input-dir ./originales --output-dir ./resultados --reuse --mode strict --territories ./territorios_verificados.csv\n\n# Columnas del CSV (no se incluyen aprobaciones ficticias):\nEDOCVE,MPIOCVE,estado,fuente,justificacion\n\n# estado: verificado / excluido / pendiente\n# Una verificación requiere fuente y justificación de continuidad 2009–2024.</pre><p class="small">El script verifica SHA-256 antes y después, conserva los originales y comprueba las huellas de los derivados al reutilizarlos. No necesitas Python para abrir este HTML.</p></details>\n<details><summary>Fuentes y fundamento metodológico</summary><ul class="small"><li><a href="https://doi.org/10.1016/0304-4076(85)90134-4" target="_blank" rel="noopener">Deaton (1985)</a>: cohortes en cortes transversales sucesivos; no convierte estos datos en un panel individual.</li><li><a href="https://doi.org/10.1080/01621459.1963.10500845" target="_blank" rel="noopener">Ward (1963)</a>: agrupamiento por función objetivo.</li><li><a href="https://doi.org/10.1016/0377-0427(87)90125-7" target="_blank" rel="noopener">Rousseeuw (1987)</a>: silueta.</li><li><a href="https://doi.org/10.1007/BF01908075" target="_blank" rel="noopener">Hubert y Arabie (1985)</a>: acuerdo entre particiones.</li><li><a href="https://doi.org/10.1016/j.csda.2006.11.025" target="_blank" rel="noopener">Hennig (2007)</a>: estabilidad y sus límites.</li><li><a href="https://scikit-learn.org/stable/modules/clustering.html" target="_blank" rel="noopener">Documentación de scikit-learn</a>: implementación y supuestos de k-means.</li><li><a href="https://ine.mx/transparencia/datos-abiertos/visualizacion-datos/conteos-censales-participacion/" target="_blank" rel="noopener">INE: plataforma CCPC</a>: declara cartografía de mayo de 2023 para su visualización. No se extrapola esa homologación automáticamente a los ZIP adjuntos; sus diccionarios difieren.</li></ul><p class="small">Las bandas de tres edades, la ponderación y la parrilla de parámetros son decisiones del diseño acordado. No se atribuyen a la bibliografía como reglas universales.</p></details>\n<details><summary>Archivos originales y huellas de integridad</summary><div id="sourceTable" class="tablewrap"></div><pre id="runtime"></pre></details>\n</div></section>\n<footer>Generaciones del voto · Explorador local, sin servicios externos ni datos personales. Los colores identifican municipios o grupos provisionales; no son categorías institucionales definitivas. <span id="build"></span></footer>\n</main><div id="tooltip" role="status"></div>\n<script id="dataset" type="application/json">__DATA__</script>\n<script>\n\'use strict\';\nconst D=JSON.parse(document.getElementById(\'dataset\').textContent), $=id=>document.getElementById(id);\nconst palette=[\'#087f83\',\'#ce8545\',\'#7561a8\',\'#3976af\',\'#bd5577\',\'#6c8744\',\'#a36e35\',\'#486b73\'];\nlet page=0,pinned=[],modelIndex=-1;\nconst esc=s=>String(s??\'\').replace(/[&<>"\']/g,c=>({\'&\':\'&amp;\',\'<\':\'&lt;\',\'>\':\'&gt;\',\'"\':\'&quot;\',"\'":\'&#39;\'}[c]));\nconst nf=new Intl.NumberFormat(\'es-MX\'),fmt=x=>x==null||!Number.isFinite(x)?\'—\':x.toFixed(2);\nconst norm=x=>String(x).normalize(\'NFD\').replace(/[\\u0300-\\u036f]/g,\'\').toLowerCase();\nconst cval=()=>+$(\'cohort\').value,sval=()=>+$(\'sex\').value;\nfunction selected(){let q=norm($(\'search\').value),st=$(\'state\').value;return D.records.filter(r=>r.cohort===cval()&&r.sex===sval()&&(!st||r.ed===+st)&&(!q||norm(r.name+\' \'+r.key).includes(q))).sort((a,b)=>a.name.localeCompare(b.name,\'es\'));}\nfunction values(r){let kind=$(\'metric\').value;if(kind===\'centered\'){if(!r.complete)return Array(6).fill(null);let v=r.counts.map(x=>100*x[1]/x[0]),a=v.reduce((a,b)=>a+b,0)/6;return v.map(x=>x-a);}return r.counts.map((x,j)=>{if(!x)return null;if(kind===\'q\')return 100*x[3]/x[0];if(kind===\'specified\')return x[1]+x[2]>0?100*x[1]/(x[1]+x[2]):null;let p=100*x[1]/x[0];if(kind===\'relative\'){let n=D.national[`${r.cohort}-${r.sex}-${D.years[j]}`];return n?p-100*n[1]/n[0]:null;}return p;});}\nfunction tooltip(e,r,j){let x=r.counts[j],v=values(r)[j],a=D.bands[r.cohort]+D.years[j]-2009;\n $(\'tooltip\').innerHTML=`<strong>${esc(r.name)}</strong>${esc(r.state)} · INE ${r.key}<br>${D.years[j]} · ${a}–${a+2} años · ${r.sex?\'Mujeres\':\'Hombres\'}<br><b>${esc($(\'metric\').selectedOptions[0].text)}: ${fmt(v)}</b>${x?`<br>LN ${nf.format(x[0])} · SV ${nf.format(x[1])}<br>NV ${nf.format(x[2])} · NS ${nf.format(x[3])}<br>Indeterminación: ${fmt(100*x[3]/x[0])}%`:\'\'}${r.clusterLabel!=null?\'<br>Grupo provisional: \'+(r.clusterLabel+1):\'\'}<br>Cartografía: ${esc(r.geo)}<br>Mismo conjunto de secciones: ${r.stable_sections?\'sí\':\'no\'}<br><span style="color:#a8d2cc">Clic: añadir al comparador</span>`;\n $(\'tooltip\').style.display=\'block\';$(\'tooltip\').style.left=Math.max(8,Math.min(e.clientX+14,innerWidth-320))+\'px\';$(\'tooltip\').style.top=Math.max(8,Math.min(e.clientY+14,innerHeight-240))+\'px\';}\nfunction hideTip(){$(\'tooltip\').style.display=\'none\';}\nfunction addPin(key){if(!pinned.includes(key)){if(pinned.length>=8){alert(\'El comparador admite hasta ocho municipios. Retira uno para añadir otro.\');return;}pinned.push(key);}renderCompare();}\nfunction domain(rows){if(![\'relative\',\'centered\'].includes($(\'metric\').value))return [0,100];let v=rows.flatMap(values).filter(x=>x!==null);let m=Math.max(10,...v.map(Math.abs));m=Math.ceil(m/10)*10;return [-m,m];}\nfunction lineChart(id,rows,{colors=null,limit=80}={}){let svg=$(id),shown=rows.slice(0,limit),w=1000,h=390,p={l:65,r:65,t:24,b:52},[lo,hi]=domain(shown),x=j=>p.l+j*(w-p.l-p.r)/5,y=v=>h-p.b-(v-lo)/(hi-lo)*(h-p.t-p.b),html=\'\';\n for(let i=0;i<=5;i++){let v=lo+(hi-lo)*i/5;html+=`<line x1="${p.l}" x2="${w-p.r}" y1="${y(v)}" y2="${y(v)}" class="gridline"/><text x="${p.l-10}" y="${y(v)+4}" text-anchor="end" class="axis">${v.toFixed(0)}</text>`;}\n D.years.forEach((yr,j)=>{html+=`<text x="${x(j)}" y="${h-24}" text-anchor="middle" class="axis">${yr}</text><text x="${x(j)}" y="${h-7}" text-anchor="middle" class="axis">${D.bands[cval()]+yr-2009}–${D.bands[cval()]+yr-2009+2} años</text>`;});\n shown.forEach((r,i)=>{let vs=values(r),color=colors?colors(r,i):palette[i%palette.length],dash=r.geo===\'verificado\'?\'\':\'stroke-dasharray="5 4"\';for(let j=1;j<6;j++)if(vs[j]!=null&&vs[j-1]!=null)html+=`<line x1="${x(j-1)}" y1="${y(vs[j-1])}" x2="${x(j)}" y2="${y(vs[j])}" stroke="${color}" stroke-width="${shown.length>20?1:2}" opacity="${shown.length>20?.4:.85}" ${dash}/>`;\n vs.forEach((v,j)=>{if(v!=null)html+=`<circle class="data-dot" data-i="${i}" data-j="${j}" cx="${x(j)}" cy="${y(v)}" r="${shown.length>20?3:4.5}" fill="${color}"><title>${esc(r.name)} · ${D.years[j]} · ${fmt(v)}</title></circle>`;});});\n if(!shown.length)html+=\'<text x="500" y="185" text-anchor="middle" class="axis">No hay municipios para esta vista.</text>\';\n svg.innerHTML=html;svg.querySelectorAll(\'.data-dot\').forEach(el=>{let r=shown[+el.dataset.i],j=+el.dataset.j;el.onmousemove=e=>tooltip(e,r,j);el.onmouseleave=hideTip;el.onclick=()=>addPin(r.key);});}\nfunction scatter(rows){let svg=$(\'scatter\'),valid=rows.filter(r=>values(r)[0]!=null&&values(r)[5]!=null),[lo,hi]=domain(valid),x=v=>60+(v-lo)/(hi-lo)*510,y=v=>325-(v-lo)/(hi-lo)*290,s=\'\';for(let i=0;i<=5;i++){let v=lo+(hi-lo)*i/5;s+=`<line x1="60" x2="570" y1="${y(v)}" y2="${y(v)}" class="gridline"/><text x="50" y="${y(v)+4}" text-anchor="end" class="axis">${v.toFixed(0)}</text><text x="${x(v)}" y="345" text-anchor="middle" class="axis">${v.toFixed(0)}</text>`;}s+=`<line x1="60" y1="325" x2="570" y2="35" stroke="#adbbb6" stroke-dasharray="4 4"/><text x="320" y="375" text-anchor="middle" class="axis">2009 · ${[\'relative\',\'centered\'].includes($(\'metric\').value)?\'pp\':\'%\'}</text><text x="14" y="180" transform="rotate(-90 14 180)" text-anchor="middle" class="axis">2024 · ${[\'relative\',\'centered\'].includes($(\'metric\').value)?\'pp\':\'%\'}</text>`;\n valid.forEach((r,i)=>{let v=values(r);s+=`<circle class="data-dot" data-i="${i}" cx="${x(v[0])}" cy="${y(v[5])}" r="4" opacity=".65" fill="#087f83"><title>${esc(r.name)}: ${fmt(v[0])} → ${fmt(v[5])}</title></circle>`;});svg.innerHTML=s;svg.querySelectorAll(\'circle\').forEach(el=>{let r=valid[+el.dataset.i];el.onmousemove=e=>tooltip(e,r,5);el.onmouseleave=hideTip;el.onclick=()=>addPin(r.key);});$(\'scatterCaption\').textContent=`${nf.format(valid.length)} municipios con ambos extremos válidos. La diagonal indica igualdad de los dos valores; no valida continuidad territorial.`;}\nfunction table(rows,where,includeAll=false){let shown=includeAll?rows:rows.slice(page*30,page*30+30);$(where).innerHTML=`<table><thead><tr><th>Municipio / entidad</th><th>2009</th><th>2024</th><th>Observaciones</th><th></th></tr></thead><tbody>${shown.map(r=>{let v=values(r);return `<tr><td><b>${esc(r.name)}</b><br>${esc(r.state)} · ${r.key}</td><td>${fmt(v[0])}</td><td>${fmt(v[5])}</td><td>${r.clusterLabel!=null?\'G\'+(r.clusterLabel+1)+\' · \':\'\'}${r.counts.filter(Boolean).length}/6<br><span class="pill ${r.geo===\'verificado\'?\'good\':\'\'}">${esc(r.geo)}</span></td><td><button data-pin="${r.key}" aria-label="Añadir ${esc(r.name)}">+</button></td></tr>`;}).join(\'\')}</tbody></table>`;$(where).querySelectorAll(\'[data-pin]\').forEach(b=>b.onclick=()=>addPin(b.dataset.pin));}\nfunction renderCompare(){let rs=pinned.map(key=>D.records.find(r=>r.key===key&&r.cohort===cval()&&r.sex===sval())).filter(Boolean);$(\'pins\').innerHTML=pinned.map((k,i)=>`<span class="chip">${esc(D.records.find(r=>r.key===k)?.name||k)}<button data-remove="${k}" aria-label="Quitar municipio">×</button></span>`).join(\'\')||\'<p class="muted">Añade municipios haciendo clic en los puntos o en el botón + de la tabla.</p>\';$(\'pins\').querySelectorAll(\'[data-remove]\').forEach(b=>b.onclick=()=>{pinned=pinned.filter(k=>k!==b.dataset.remove);renderCompare();});lineChart(\'compareChart\',rs);$(\'legend\').innerHTML=rs.map((r,i)=>`<span style="margin-right:18px"><span class="keyline" style="color:${palette[i]}"></span>${esc(r.name)} · ${esc(r.state)}</span>`).join(\'\');$(\'compareTable\').innerHTML=`<table><thead><tr><th>Municipio</th>${D.years.map(y=>`<th>${y}</th>`).join(\'\')}</tr></thead><tbody>${rs.map(r=>`<tr><td>${esc(r.name)}</td>${values(r).map((v,j)=>`<td title="${esc(r.reasons[j])}">${fmt(v)}${r.counts[j]?`<br><small>LN ${nf.format(r.counts[j][0])}</small>`:\'\'}</td>`).join(\'\')}</tr>`).join(\'\')}</tbody></table>`;}\nfunction renderModels(reset=false){let ms=D.models.map((m,i)=>({...m,index:i})).filter(m=>m.cohort===cval()&&m.sex===sval()&&m.experiment===$(\'experiment\').value);if(reset||!$(\'model\').options.length||!ms.some(m=>m.index===+$(\'model\').value)){$(\'model\').innerHTML=ms.map(m=>`<option value="${m.index}">${m.method===\'ward\'?\'Ward\':\'K-means\'} · ${m.k} grupos · ${m.ids.length} municipios · silueta ${fmt(m.silhouette)}</option>`).join(\'\');if(ms.length)$(\'model\').value=String(($(\'experiment\').value===\'centered\'?ms.find(m=>m.method===\'kmeans\'&&m.k===6)||ms[0]:ms.reduce((a,b)=>a.silhouette>=b.silhouette?a:b)).index);}let m=D.models[+$(\'model\').value];if(!ms.length){$(\'model\').disabled=true;$(\'clusterGroup\').disabled=true;$(\'modelStatus\').innerHTML=\'<div class="empty"><h3>Sin modelos ejecutados en este estrato</h3>La auditoría territorial sigue pendiente o no hay suficientes trayectorias elegibles. No se han inventado etiquetas ni resultados.<br>El Python incluye los modelos y la validación; se habilitan con un registro territorial documentado.</div>\';$(\'modelMetrics\').innerHTML=\'\';$(\'clusterChart\').innerHTML=\'\';$(\'clusterTable\').innerHTML=\'\';$(\'groupSummary\').innerHTML=\'\';$(\'stabilityPlot\').innerHTML=\'\';return;}\n $(\'model\').disabled=false;$(\'clusterGroup\').disabled=false;$(\'modelStatus\').innerHTML=\'<span class="pill good">Resultados calculados · clasificación exploratoria; número de grupo sin significado ordinal</span>\';if(reset||modelIndex!==+$(\'model\').value){$(\'clusterGroup\').innerHTML=\'<option value="">Todos los grupos</option>\'+m.sizes.map((n,i)=>`<option value="${i}">Grupo ${i+1} · ${n} municipios</option>`).join(\'\');modelIndex=+$(\'model\').value;}\n let labels=new Map(m.ids.map((id,i)=>[id,m.labels[i]])),rs=selected().filter(r=>labels.has(r.id)&&($(\'clusterGroup\').value===\'\'||labels.get(r.id)===+$(\'clusterGroup\').value)).map(r=>({...r,clusterLabel:labels.get(r.id)}));$(\'modelMetrics\').innerHTML=`<div class="stats"><div class="stat"><b>${fmt(m.silhouette)}</b><span>Silueta</span></div><div class="stat"><b>${fmt(m.seed_ari_median)}</b><span>ARI mediano entre semillas</span></div><div class="stat"><b>${fmt(Math.min(...m.jackknife_ari))}</b><span>ARI mínimo al excluir elección</span></div><div class="stat"><b>${fmt(m.specified_ari)}</b><span>ARI con participación especificada</span></div><div class="stat"><b>${fmt(m.territorial_ari)}</b><span>ARI · restricción territorial</span></div><div class="stat"><b>${nf.format(m.territorial_n)}</b><span>Municipios en sensibilidad territorial</span></div></div><p class="small">Sensibilidad por elección excluida: ${D.years.map((y,i)=>y+\': \'+fmt(m.jackknife_ari[i])).join(\' · \')}. Se muestran hasta 80 trayectorias; ${rs.length} municipios coinciden con los filtros.</p>`;lineChart(\'clusterChart\',rs,{colors:r=>palette[labels.get(r.id)%8]});table(rs,\'clusterTable\',true);renderGroupSummary(m,labels);renderStability(m);renderProfiles(m);}\n\nfunction renderGroupSummary(m,labels){\n let all=D.records.filter(r=>labels.has(r.id));\n $(\'groupSummary\').innerHTML=\'<table><thead><tr><th>Grupo</th><th>Municipios</th><th>Silueta</th>\'+D.years.map(y=>\'<th>\'+y+\'</th>\').join(\'\')+\'</tr></thead><tbody>\'+Array.from({length:m.k},(_,g)=>{let rs=all.filter(r=>labels.get(r.id)===g);return \'<tr><td><span class="keyline" style="color:\'+palette[g%8]+\'"></span>G\'+(g+1)+\'</td><td>\'+rs.length+\'</td><td>\'+fmt(m.silhouette_by_group?.[g])+\'</td>\'+D.years.map((yr,j)=>{let v=rs.map(values).map(x=>x[j]).filter(x=>x!=null),mean=v.length?v.reduce((a,b)=>a+b,0)/v.length:null;let title=\'Grupo \'+(g+1)+\' · \'+yr+\' · \'+v.length+\' municipios; mínimo \'+fmt(v.length?Math.min(...v):null)+\'; máximo \'+fmt(v.length?Math.max(...v):null);return \'<td title="\'+esc(title)+\'" style="background:rgba(8,127,131,\'+(mean==null?0:Math.min(.5,Math.abs(mean)/180))+\')">\'+fmt(mean)+\'</td>\';}).join(\'\')+\'</tr>\';}).join(\'\')+\'</tbody></table><p class="small muted">Resumen del modelo completo: no cambia con el filtro de entidad. Las trayectorias individuales de abajo sí responden a entidad, búsqueda y grupo.</p>\';\n}\nfunction renderStability(m){let y=v=>170-(v+1)*70,x=j=>100+j*155;let s=\'\';[-1,0,1].forEach(v=>s+=\'<line class="gridline" x1="60" x2="975" y1="\'+y(v)+\'" y2="\'+y(v)+\'"/><text class="axis" x="45" y="\'+(y(v)+4)+\'">\'+v+\'</text>\');m.jackknife_ari.forEach((v,j)=>{s+=\'<rect x="\'+x(j)+\'" y="\'+Math.min(y(v),y(0))+\'" width="75" height="\'+Math.max(1,Math.abs(y(v)-y(0)))+\'" fill="#087f83"><title>Sin \'+D.years[j]+\': ARI \'+fmt(v)+\'</title></rect><text class="axis" text-anchor="middle" x="\'+(x(j)+37)+\'" y="\'+(y(v)-8)+\'">\'+fmt(v)+\'</text><text class="axis" text-anchor="middle" x="\'+(x(j)+37)+\'" y="200">Sin \'+D.years[j]+\'</text>\';});$(\'stabilityPlot\').innerHTML=s;}\n\n\nfunction renderProfiles(m){\n $(\'profiles\').innerHTML=(m.profiles||[]).map(p=>{let v=$(\'metric\').value===\'centered\'?p.centered_mean:p.mean,lo=$(\'metric\').value===\'centered\'?-40:0,hi=$(\'metric\').value===\'centered\'?40:100;lo=Math.min(lo,...v);hi=Math.max(hi,...v);let x=j=>25+j*48,y=z=>115-(z-lo)/(hi-lo)*95;return `<article class="profile" style="border-top-color:${palette[p.group]}"><div class="small muted">G${p.group+1} · ${nf.format(p.n)} municipios</div><h3>${esc(p.name)}</h3><svg viewBox="0 0 300 145" role="img" aria-label="Curva media del grupo ${p.group+1}"><line x1="25" x2="265" y1="${y(0)}" y2="${y(0)}" stroke="#ccc"/><polyline points="${v.map((z,j)=>x(j)+\',\'+y(z)).join(\' \')}" fill="none" stroke="${palette[p.group]}" stroke-width="3"/>${v.map((z,j)=>`<circle cx="${x(j)}" cy="${y(z)}" r="5" fill="${palette[p.group]}"><title>${D.years[j]}: ${fmt(z)} ${$(\'metric\').value===\'centered\'?\'pp centrados\':\'% SV/LN\'}; NS/LN ${fmt(p.q_mean[j])}%</title></circle><text x="${x(j)}" y="135" text-anchor="middle" font-size="10">${String(D.years[j]).slice(2)}</text>`).join(\'\')}</svg><p>2009: <b>${fmt(p.mean[0])}%</b> → 2024: <b>${fmt(p.mean[5])}%</b><br>Cambio: <b>${p.delta>0?\'+\':\'\'}${fmt(p.delta)} pp</b> · mínimo: ${p.low_year}<br>Silueta: ${fmt(m.silhouette_by_group[p.group])}<br>Jaccard mínimo / medio: <b>${fmt(p.jaccard_min)} / ${fmt(p.jaccard_mean)}</b></p><div>${p.representatives.map(r=>`<button data-example="${r.key}" title="${esc(r.state)} · ${r.key} · distancia al centroide ${fmt(r.distance)}">${esc(r.name)} · ${esc(r.state)}</button>`).join(\'\')}</div><p class="muted">${$(\'metric\').value===\'centered\'?\'Curva: desviación de la media propia (pp).\':\'Curva: SV/LN (%), independientemente de otros indicadores.\'} ${p.jaccard_min==null?\'Jaccard por grupo sólo calculado en experimento 02.\':\'Jaccard bajo indica que el grupo cambia al retirar una elección.\'}</p></article>`;}).join(\'\');\n $(\'profiles\').querySelectorAll(\'[data-example]\').forEach(b=>b.onclick=()=>{addPin(b.dataset.example);b.textContent=\'✓ \'+b.textContent.replace(/^✓ /,\'\');});\n if(!m.transition_matrix){$(\'transition\').innerHTML=\'\';return;}let mx=Math.max(...m.transition_matrix.flat());$(\'transition\').innerHTML=`<h3>¿Cómo cambia la clasificación al centrar?</h3><p class="small">ARI frente al experimento 01 con el mismo método y k: <b>${fmt(m.level_ari)}</b>. Filas: grupos de niveles; columnas: grupos de formas. Los números no implican correspondencia. Pasa el cursor para ver los cruces.</p><table><thead><tr><th>Nivel / forma</th>${m.sizes.map((_,i)=>\'<th>G\'+(i+1)+\'</th>\').join(\'\')}</tr></thead><tbody>${m.transition_matrix.map((row,i)=>\'<tr><th>G\'+(i+1)+\'</th>\'+row.map((n,j)=>`<td style="background:rgba(8,127,131,${n/mx*.65})" title="Nivel G${i+1} → forma G${j+1}: ${n} municipios">${n}</td>`).join(\'\')+\'</tr>\').join(\'\')}</tbody></table><p class="small muted">Cruces del modelo completo. Describen acuerdo de etiquetas, no migración ni cambios de voto.</p>`;\n}\n\nfunction renderQuality(rows){let ys=D.years.map(y=>({year:y,files:D.audit.files.filter(f=>f.year===y)})),keys=Object.keys(D.audit.files[0]?.issues||{});$(\'auditSummary\').innerHTML=`<table><thead><tr><th>Año</th><th>Filas leídas</th>${keys.map(k=>`<th>${esc(k.replaceAll(\'_\',\' \'))}</th>`).join(\'\')}</tr></thead><tbody>${ys.map(o=>`<tr><td>${o.year}</td><td>${nf.format(o.files.reduce((a,f)=>a+f.rows,0))}</td>${keys.map(k=>`<td>${nf.format(o.files.reduce((a,f)=>a+f.issues[k],0))}</td>`).join(\'\')}</tr>`).join(\'\')}</tbody></table>`;\n let bad=rows.filter(r=>!r.eligible);$(\'exclusionTable\').innerHTML=`<p class="small">${nf.format(bad.length)} trayectorias fuera del modelo en esta selección. Se listan las primeras 200; el CSV descarga todas.</p><table><thead><tr><th>Municipio</th><th>Motivo</th></tr></thead><tbody>${bad.slice(0,200).map(r=>`<tr><td>${esc(r.name)} · ${r.key}</td><td>${r.geo!==\'verificado\'?\'Estado cartográfico: \'+esc(r.geo)+\'. \':\'\'}${r.reasons.map((v,j)=>v?D.years[j]+\': \'+esc(v):\'\').filter(Boolean).join(\'; \')}</td></tr>`).join(\'\')}</tbody></table>`;}\nfunction render(){let rs=selected();page=Math.min(page,Math.max(0,Math.ceil(rs.length/30)-1));$(\'nMunicipal\').textContent=nf.format(rs.length);$(\'nComplete\').textContent=nf.format(rs.filter(r=>r.complete).length);$(\'nGeo\').textContent=nf.format(rs.filter(r=>r.stable_sections).length);$(\'nMissing\').textContent=nf.format(rs.reduce((a,r)=>a+r.counts.filter(x=>!x).length,0));$(\'lineCaption\').textContent=`${rs.length>80?\'Primeros 80 municipios por nombre de \'+nf.format(rs.length):nf.format(rs.length)+\' municipios\'} · ${$(\'metric\').selectedOptions[0].text}. Filtra para reducir el número de líneas.`;lineChart(\'lines\',rs);scatter(rs);table(rs,\'municipalTable\');$(\'pageLabel\').textContent=`${rs.length?page+1:0} / ${Math.ceil(rs.length/30)}`;$(\'prev\').disabled=page===0;$(\'next\').disabled=(page+1)*30>=rs.length;renderCompare();renderModels();renderQuality(rs);}\nfunction downloadClusters(){let m=D.models[+$(\'model\').value];if(!m)return;let labels=new Map(m.ids.map((id,i)=>[id,m.labels[i]]));let rs=selected().filter(r=>labels.has(r.id)&&($(\'clusterGroup\').value===\'\'||labels.get(r.id)===+$(\'clusterGroup\').value));let rows=[[\'clave_INE\',\'municipio\',\'entidad\',\'cohorte_edad_2009\',\'sexo\',\'experimento\',\'modelo\',\'k\',\'grupo_provisional\',\'mismo_conjunto_secciones\',...D.years.map(y=>\'P_\'+y)]];rs.forEach(r=>rows.push([r.key,r.name,r.state,D.bands[r.cohort]+\'-\'+(D.bands[r.cohort]+2),r.sex,m.experiment,m.method,m.k,labels.get(r.id)+1,r.stable_sections,...r.counts.map(x=>100*x[1]/x[0])]));let csv=\'\\ufeff\'+rows.map(row=>row.map(v=>{let t=String(v);if(typeof v===\'string\'&&/^[=+@-]/.test(t))t="\'"+t;return \'"\'+t.replaceAll(\'"\',\'""\')+\'"\';}).join(\',\')).join(\'\\r\\n\');let url=URL.createObjectURL(new Blob([csv],{type:\'text/csv;charset=utf-8\'})),a=document.createElement(\'a\');a.href=url;a.download=\'clasificacion_\'+m.experiment+\'_\'+m.method+\'_k\'+m.k+\'.csv\';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}\nfunction download(){let rows=[[\'clave_INE\',\'municipio\',\'entidad\',\'cohorte_edad_2009\',\'sexo\',\'eleccion\',\'edad_min\',\'edad_max\',\'LN\',\'SV\',\'NV\',\'NS\',\'P\',\'P_especificada\',\'Q\',\'continuidad_territorial\',\'motivo_dato_ausente\']];selected().forEach(r=>D.years.forEach((yr,j)=>{let x=r.counts[j],age=D.bands[r.cohort]+yr-2009;rows.push([r.key,r.name,r.state,`${D.bands[r.cohort]}-${D.bands[r.cohort]+2}`,r.sex,yr,age,age+2,...(x||[\'\',\'\',\'\',\'\']),x?100*x[1]/x[0]:\'\',x&&x[1]+x[2]>0?100*x[1]/(x[1]+x[2]):\'\',x?100*x[3]/x[0]:\'\',r.geo,r.reasons[j]]);}));let csv=\'\\ufeff\'+rows.map(row=>row.map(v=>{let s=String(v);if(typeof v===\'string\'&&/^[=+@-]/.test(s))s="\'"+s;return \'"\'+s.replaceAll(\'"\',\'""\')+\'"\';}).join(\',\')).join(\'\\r\\n\');let a=document.createElement(\'a\'),url=URL.createObjectURL(new Blob([csv],{type:\'text/csv;charset=utf-8\'}));a.href=url;a.download=\'seleccion_generaciones.csv\';a.click();setTimeout(()=>URL.revokeObjectURL(url),2000);}\nlet states=[...new Map(D.records.map(r=>[r.ed,r.state])).entries()].sort((a,b)=>a[0]-b[0]);$(\'state\').innerHTML=\'<option value="">Todas las entidades</option>\'+states.map(([k,v])=>`<option value="${k}">${esc(v)}</option>`).join(\'\');$(\'state\').value=\'\';\n$(\'status\').innerHTML=D.models.length?`<b>${D.models.length} soluciones exploratorias calculadas.</b> Se utilizan trayectorias completas. La cartografía pendiente no bloquea la segmentación; consulta la sensibilidad territorial en Agrupamientos.`:\'<b>Datos reales disponibles · agrupamiento pendiente de validación territorial.</b> Puedes explorar y comparar observaciones. Las líneas aún no acreditan continuidad de límites municipales; el código no ha asignado clústeres sin esa comprobación.\';\n[\'cohort\',\'sex\',\'state\',\'metric\'].forEach(id=>$(id).onchange=()=>{page=0;if(id===\'cohort\'||id===\'sex\')renderModels(true);render();});$(\'search\').oninput=()=>{page=0;render();};$(\'prev\').onclick=()=>{page--;render();};$(\'next\').onclick=()=>{page++;render();};$(\'clearPins\').onclick=()=>{pinned=[];renderCompare();};$(\'download\').onclick=download;$(\'downloadClusters\').onclick=downloadClusters;$(\'experiment\').onchange=()=>{renderModels(true);};$(\'model\').onchange=()=>renderModels();$(\'clusterGroup\').onchange=()=>renderModels();document.querySelectorAll(\'nav button\').forEach(b=>b.onclick=()=>{document.querySelectorAll(\'nav button\').forEach(x=>x.classList.toggle(\'active\',x===b));document.querySelectorAll(\'main>section\').forEach(s=>s.hidden=s.id!==b.dataset.tab);hideTip();});\n$(\'sourceTable\').innerHTML=`<table><thead><tr><th>Año</th><th>Archivo</th><th>SHA-256</th></tr></thead><tbody>${Object.entries(D.manifest.sources).map(([y,s])=>`<tr><td>${y}</td><td>${esc(s.filename)}</td><td class="filehash">${s.sha256}</td></tr>`).join(\'\')}</tbody></table>`;$(\'runtime\').textContent=JSON.stringify(D.manifest.runtime,null,2);$(\'build\').textContent=\'Versión \'+D.version+\' · generado \'+D.created_utc.slice(0,10);render();if(D.models.length)document.querySelector(\'[data-tab="clusters"]\').click();\n</script></body></html>\n'


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for block in iter(lambda: f.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, allow_nan=False,
                                   separators=(',', ':')), encoding='utf-8')


def locate(root):
    found = {}
    for y in YEARS:
        matches = [p for p in Path(root).glob('*.zip')
                   if re.search(r'ConteosCensales'+str(y)+r'\D', p.name, re.I)]
        if len(matches) != 1:
            raise ValueError(f'{y}: encontrados {matches}')
        found[y] = matches[0]
    return found


def aggregate(sources, out):
    frames, audits, examples = [], [], []
    for year, path in sources.items():
        print(f'Lectura y comprobación {year}', flush=True)
        with zipfile.ZipFile(path) as z:
            files = sorted(n for n in z.namelist() if n.lower().endswith('.csv'))
            for name in files:
                with z.open(name) as f:
                    d = pd.read_csv(f, dtype=str, keep_default_na=False)
                required = ['AELEC','FELECCION','EDOCVE','EDONOM','MPIOCVE',
                            'MPIONOM','SECCION','SEXO','EDAD']+COUNTS
                if not set(required).issubset(d.columns):
                    raise ValueError(f'Esquema inesperado: {name}')
                nums = ['AELEC','EDOCVE','MPIOCVE','SECCION','SEXO','EDAD']+COUNTS
                n = d[nums].apply(pd.to_numeric, errors='coerce')
                integer = n.notna().all(axis=1) & np.isfinite(n).all(axis=1) & (n.mod(1)==0).all(axis=1)
                invalid_count = (n[COUNTS]<0).any(axis=1) | n[COUNTS].isna().any(axis=1)
                identity = n.LN != n.SV+n.NV+n.NS
                key = ['EDOCVE','MPIOCVE','SECCION','SEXO','EDAD']
                duplicate = n.duplicated(key, keep=False)
                bad_date = d.FELECCION != EXPECTED_DATES[year]
                bad_geo = ~n.EDOCVE.between(1,32) | (n.MPIOCVE<=0) | (n.SECCION<=0)
                bad_age_sex = (n.EDAD<18) | ~n.SEXO.isin([0,1,2] if year==2024 else [0,1])
                wrong_year = n.AELEC != year
                issues = {'no_entero_o_ausente':~integer,'conteo_negativo_o_ausente':invalid_count,
                          'identidad_conteos':identity,'clave_duplicada':duplicate,
                          'fecha_inesperada':bad_date,'geografia_invalida':bad_geo,
                          'edad_sexo_invalido':bad_age_sex,'anio_incorrecto':wrong_year}
                bad = pd.DataFrame(issues).any(axis=1)
                audit = {'year':year,'file':name,'rows':len(d),
                         'issues':{k:int(v.sum()) for k,v in issues.items()}}
                audits.append(audit)
                for reason, mask in issues.items():
                    for idx in d.index[mask][:3]:
                        examples.append({'year':year,'file':name,'csv_line':int(idx)+2,
                                         'reason':reason,'raw':d.loc[idx].to_dict()})

                if n[['EDOCVE','MPIOCVE','EDAD','SEXO']].isna().any().any():
                    raise ValueError(f'Clave ilegible en {name}; resolver auditoría antes de agregar')
                age2009 = n.EDAD-(year-2009)
                select = age2009.between(18,29) & n.SEXO.isin([0,1])
                t = n.loc[select].copy()
                t['cohort'] = ((age2009[select]-18)//3).astype(int)
                t['bad'] = bad[select].astype(int)
                t['name'] = d.loc[select,'MPIONOM']
                t['state'] = d.loc[select,'EDONOM']
                group = ['EDOCVE','MPIOCVE','cohort','SEXO']
                g = t.groupby(group,sort=True).agg(
                    **{c:(c,lambda s:s.sum(min_count=1)) for c in COUNTS},
                    bad=('bad','sum'),name=('name','first'),state=('state','first'),
                    names=('name','nunique'),rows=('EDAD','size'),ages=('EDAD','nunique'))
                g['year'] = year
                g['valid'] = (g.bad==0)&(g.names==1)&(g.ages==3)&(g.LN>0)
                frames.append(g.reset_index())
    result = pd.concat(frames, ignore_index=True)
    if result.duplicated(['EDOCVE','MPIOCVE','cohort','SEXO','year']).any():
        raise ValueError('Agregado repetido entre archivos; revisar composición de ZIP')
    result.to_csv(out/'agregados.csv',index=False)
    write_json(out/'auditoria.json',{'files':audits,'examples':examples,
        'note':'Ejemplos limitados a tres por motivo y archivo; los conteos de incidencias son completos. No se verificó cobertura sección×edad contra un padrón externo.'})
    return result


def territory_registry(path):
    if not path:
        return {}
    d = pd.read_csv(path,dtype=str,keep_default_na=False)
    required = ['EDOCVE','MPIOCVE','estado','fuente','justificacion']
    if not set(required).issubset(d):
        raise ValueError('Registro territorial requiere '+','.join(required))
    result={}
    for row in d.to_dict('records'):
        key=f"{int(row['EDOCVE']):02d}-{int(row['MPIOCVE']):03d}"
        if key in result: raise ValueError('Clave territorial repetida: '+key)
        if row['estado'] not in ['verificado','excluido','pendiente']:
            raise ValueError('Estado territorial inválido: '+key)
        if row['estado']=='verificado' and not (row['fuente'].strip() and row['justificacion'].strip()):
            raise ValueError('Verificación sin fuente y justificación: '+key)
        result[key]=row
    return result


def build_records(df, registry, mode='exploratory'):
    records=[]
    for (ed,mu,c,s), g in df.groupby(['EDOCVE','MPIOCVE','cohort','SEXO'],sort=True):
        byyear={int(r['year']):r for r in g.to_dict('records')}
        key=f'{int(ed):02d}-{int(mu):03d}'
        latest=byyear[max(byyear)]
        counts=[]; reasons=[]
        for y in YEARS:
            r=byyear.get(y)
            if r is None:
                counts.append(None);reasons.append('Sin agregado en el archivo');continue
            if not r['valid']:
                counts.append(None)
                reasons.append(f"Agregado no válido: incidencias={int(r['bad'])}, edades={int(r['ages'])}, nombres={int(r['names'])}, LN={r['LN']}")
                continue
            counts.append([int(r[k]) for k in COUNTS]);reasons.append('')
        geo=registry.get(key,{'estado':'pendiente','fuente':'','justificacion':''})
        complete=all(x is not None for x in counts)
        records.append({'id':f'{key}-{int(c)}-{int(s)}','key':key,'ed':int(ed),
            'name':latest['name'],'state':latest['state'],'cohort':int(c),'sex':int(s),
            'counts':counts,'reasons':reasons,'complete':complete,'geo':geo['estado'],
            'eligible':complete and (mode=='exploratory' or geo['estado']=='verificado')})
    return records


def audit_sections(sources, out):
    """Comparabilidad observada, no certificación de límites geográficos."""
    parts=[]
    for year,path in sources.items():
        pairs=set()
        with zipfile.ZipFile(path) as z:
            for name in sorted(z.namelist()):
                if not name.endswith('.csv'): continue
                with z.open(name) as f:
                    for d in pd.read_csv(f,usecols=['EDOCVE','MPIOCVE','SECCION'],chunksize=300000):
                        pairs.update(d.drop_duplicates().itertuples(index=False,name=None))
        x=pd.DataFrame(sorted(pairs),columns=['EDOCVE','MPIOCVE','SECCION'])
        x['year']=year;parts.append(x)
    x=pd.concat(parts,ignore_index=True)
    sets={(int(a),int(b),int(c)):set(g.SECCION)
          for (a,b,c),g in x.groupby(['EDOCVE','MPIOCVE','year'])}
    changed=x.groupby(['EDOCVE','SECCION']).MPIOCVE.nunique()
    changed=changed[changed>1]
    reassigned=x.set_index(['EDOCVE','SECCION']).loc[changed.index].reset_index()
    risk=set(reassigned[['EDOCVE','MPIOCVE']].itertuples(index=False,name=None))
    rows=[]
    for ed,mu in x[['EDOCVE','MPIOCVE']].drop_duplicates().itertuples(index=False,name=None):
        seq=[sets.get((ed,mu,y)) for y in YEARS]
        present=all(s is not None for s in seq)
        rows.append({'EDOCVE':ed,'MPIOCVE':mu,'six_years':present,
            'same_section_set':present and all(s==seq[0] for s in seq),
            'shared_section_changed_municipality':(ed,mu) in risk})
    result=pd.DataFrame(rows)
    result.to_csv(out/'diagnostico_territorial.csv',index=False)
    return result


def rate(r, specified=False):
    return np.array([100*x[1]/(x[1]+x[2] if specified else x[0])
                     if x is not None and (x[1]+x[2] if specified else x[0])>0
                     else np.nan for x in r['counts']])


def fit_levels(records,out):
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_samples,adjusted_rand_score
    from scipy.cluster.hierarchy import linkage,cut_tree
    from threadpoolctl import threadpool_limits
    models=[]
    for c,s in itertools.product(range(4),range(2)):
        rs=[r for r in records if r['cohort']==c and r['sex']==s and r['eligible']]
        if len(rs)<3: continue
        X=np.vstack([rate(r) for r in rs]); Xs=np.vstack([rate(r,True) for r in rs])
        n_unique=len(np.unique(X,axis=0))
        valid_s=np.isfinite(Xs).all(axis=1)
        with threadpool_limits(limits=1):
            for method in ['kmeans','ward']:
                Z=linkage(X,method='ward',metric='euclidean') if method=='ward' else None
                for k in range(2,min(8,len(rs)-1,n_unique)+1):
                    print(f'Modelo cohorte={c} sexo={s} {method} k={k}',flush=True)
                    def fit(a,seed=0):
                        if method=='kmeans':
                            return KMeans(n_clusters=k,init='k-means++',n_init=50,
                                max_iter=500,tol=1e-4,random_state=seed,algorithm='lloyd').fit_predict(a)
                        return cut_tree(linkage(a,method='ward'),n_clusters=[k]).ravel()
                    labels=fit(X) if method=='kmeans' else cut_tree(Z,n_clusters=[k]).ravel()
                    seeds=[fit(X,seed) for seed in range(20)] if method=='kmeans' else []
                    seed_ari=[adjusted_rand_score(a,b) for a,b in itertools.combinations(seeds,2)]
                    jack=[float(adjusted_rand_score(labels,fit(np.delete(X,j,axis=1)))) for j in range(6)]
                    sensitivity=None
                    if valid_s.sum()>k and len(np.unique(Xs[valid_s],axis=0))>=k:
                        sensitivity=float(adjusted_rand_score(labels[valid_s],fit(Xs[valid_s])))
                    stable=np.array([r.get('stable_sections',False) for r in rs])
                    territorial_ari=None
                    if stable.sum()>k and len(np.unique(X[stable],axis=0))>=k:
                        territorial_ari=float(adjusted_rand_score(labels[stable],fit(X[stable])))
                    sizes=np.bincount(labels,minlength=k).tolist()
                    silhouettes=silhouette_samples(X,labels)
                    models.append({'cohort':c,'sex':s,'method':method,'k':k,
                        'ids':[r['id'] for r in rs],'labels':[int(x) for x in labels],
                        'silhouette':float(silhouettes.mean()),
                        'silhouette_by_group':[float(silhouettes[labels==j].mean())
                                               if np.any(labels==j) else None for j in range(k)],
                        'seed_ari_median':float(np.median(seed_ari)) if seed_ari else None,
                        'seed_ari_min':float(min(seed_ari)) if seed_ari else None,
                        'jackknife_ari':jack,'specified_ari':sensitivity,
                        'specified_n':int(valid_s.sum()),'sizes':sizes,
                        'territorial_n':int(stable.sum()),'territorial_ari':territorial_ari})
    write_json(out/'modelos_nivel.json',models)
    return models


def fit_models(records,out):
   
    def center(a): return a-a.mean(axis=1,keepdims=True)
    from sklearn.cluster import KMeans
    from sklearn.metrics import silhouette_samples,adjusted_rand_score
    from scipy.cluster.hierarchy import linkage,cut_tree
    from threadpoolctl import threadpool_limits
    models=[]
    for c,s in itertools.product(range(4),range(2)):
        rs=[r for r in records if r['cohort']==c and r['sex']==s and r['eligible']]
        if len(rs)<3: continue
        X=np.vstack([rate(r) for r in rs]); Xs=np.vstack([rate(r,True) for r in rs])
        raw=X.copy(); X=center(X); Xs=center(Xs)
        n_unique=len(np.unique(X,axis=0))
        valid_s=np.isfinite(Xs).all(axis=1)
        with threadpool_limits(limits=1):
            for method in ['kmeans','ward']:
                Z=linkage(X,method='ward',metric='euclidean') if method=='ward' else None
                for k in range(2,min(8,len(rs)-1,n_unique)+1):
                    print(f'Modelo cohorte={c} sexo={s} {method} k={k}',flush=True)
                    def fit(a,seed=0):
                        if method=='kmeans':
                            return KMeans(n_clusters=k,init='k-means++',n_init=50,
                                max_iter=500,tol=1e-4,random_state=seed,algorithm='lloyd').fit_predict(a)
                        return cut_tree(linkage(a,method='ward'),n_clusters=[k]).ravel()
                    labels=fit(X) if method=='kmeans' else cut_tree(Z,n_clusters=[k]).ravel()
                    seeds=[fit(X,seed) for seed in range(20)] if method=='kmeans' else []
                    seed_ari=[adjusted_rand_score(a,b) for a,b in itertools.combinations(seeds,2)]
                    jack_labels=[fit(center(np.delete(raw,j,axis=1))) for j in range(6)]
                    jack=[float(adjusted_rand_score(labels,a)) for a in jack_labels]
                    group_jaccard=[]
                    for g in range(k):
                        A=labels==g; js=[]
                        for other in jack_labels:
                            js.append(max(float(np.sum(A & (other==h))/np.sum(A | (other==h))) for h in np.unique(other)))
                        group_jaccard.append(js)
                    sensitivity=None
                    if valid_s.sum()>k and len(np.unique(Xs[valid_s],axis=0))>=k:
                        sensitivity=float(adjusted_rand_score(labels[valid_s],fit(Xs[valid_s])))
                    stable=np.array([r.get('stable_sections',False) for r in rs])
                    territorial_ari=None
                    if stable.sum()>k and len(np.unique(X[stable],axis=0))>=k:
                        territorial_ari=float(adjusted_rand_score(labels[stable],fit(X[stable])))
                    sizes=np.bincount(labels,minlength=k).tolist()
                    silhouettes=silhouette_samples(X,labels)
                    models.append({'cohort':c,'sex':s,'method':method,'k':k,
                        'experiment':'centered','group_jaccard':group_jaccard,'ids':[r['id'] for r in rs],'labels':[int(x) for x in labels],
                        'silhouette':float(silhouettes.mean()),
                        'silhouette_by_group':[float(silhouettes[labels==j].mean())
                                               if np.any(labels==j) else None for j in range(k)],
                        'seed_ari_median':float(np.median(seed_ari)) if seed_ari else None,
                        'seed_ari_min':float(min(seed_ari)) if seed_ari else None,
                        'jackknife_ari':jack,'specified_ari':sensitivity,
                        'specified_n':int(valid_s.sum()),'sizes':sizes,
                        'territorial_n':int(stable.sum()),'territorial_ari':territorial_ari})
                    write_json(out/'modelos_centrados_checkpoint.json',models)
    write_json(out/'modelos_centrados.json',models)
    return models


def describe_profiles(records,levels,centered):
 
    
 
    from sklearn.metrics import adjusted_rand_score
    lookup={r['id']:r for r in records}
    baseline={(m['cohort'],m['sex'],m['method'],m['k']):m for m in levels}
    for m in levels:m['experiment']='level'
    for m in centered:m['experiment']='centered'
    for m in levels+centered:
        rs=[lookup[i] for i in m['ids']]
        X=np.vstack([rate(r) for r in rs])
        V=X-X.mean(axis=1,keepdims=True) if m['experiment']=='centered' else X
        labels=np.array(m['labels']);profiles=[]
        for g in range(m['k']):
            ix=np.flatnonzero(labels==g);means=X[ix].mean(axis=0)
            shape=(X[ix]-X[ix].mean(axis=1,keepdims=True)).mean(axis=0)
            delta=float(means[-1]-means[0]);peak=int(np.argmax(means));low=int(np.argmin(means))
            direction='Ascenso neto' if delta>0 else ('Descenso neto' if delta<0 else 'Extremos iguales')
            name=f'{direction} {delta:+.1f} pp · máximo en {YEARS[peak]}'
            distances=np.linalg.norm(V[ix]-V[ix].mean(axis=0),axis=1)
            seen=set();representatives=[]
            for j in np.argsort(distances,kind='stable'):
                r=rs[ix[j]]
                if r['ed'] in seen:continue
                seen.add(r['ed']);representatives.append({'id':r['id'],'key':r['key'],
                    'name':r['name'],'state':r['state'],'distance':float(distances[j])})
                if len(representatives)==3:break
            q=np.array([[100*x[3]/x[0] for x in rs[i]['counts']] for i in ix])
            js=m.get('group_jaccard',[None]*m['k'])[g]
            profiles.append({'group':g,'name':name,'n':len(ix),'mean':means.tolist(),
                'centered_mean':shape.tolist(),'delta':delta,'mean_level':float(means.mean()),
                'peak_year':YEARS[peak],'low_year':YEARS[low],
                'q_mean':q.mean(axis=0).tolist(),
                'jaccard_min':min(js) if js else None,
                'jaccard_mean':float(np.mean(js)) if js else None,
                'representatives':representatives})
        m['profiles']=profiles
        if m['experiment']=='centered':
            b=baseline[(m['cohort'],m['sex'],m['method'],m['k'])]
            assert b['ids']==m['ids'],'Comparación requiere exactamente las mismas unidades y orden'
            matrix=np.zeros((m['k'],m['k']),dtype=int)
            for a,c in zip(b['labels'],m['labels']):matrix[a,c]+=1
            m['level_ari']=float(adjusted_rand_score(b['labels'],m['labels']))
            m['transition_matrix']=matrix.tolist()
    return levels+centered


def render(df,records,models,audit,manifest,registry,out):
    data={'version':VERSION,'years':YEARS,'bands':BANDS,'records':records,
          'models':models,'audit':audit,'manifest':manifest,'registry':registry,
          'created_utc':pd.Timestamp.now(tz='UTC').isoformat()}

    national={}
    for (c,s,y),g in df.groupby(['cohort','SEXO','year']):
        national[f'{int(c)}-{int(s)}-{int(y)}']=([int(g[col].sum()) for col in COUNTS]
            if (g.bad==0).all() and g.LN.sum()>0 else None)
    data['national']=national
    data['coverage']=[{'year':y,'keys':int(len(df[df.year==y][['EDOCVE','MPIOCVE']].drop_duplicates()))}
                       for y in YEARS]
    template=TEMPLATE
    if template is None:
        template=Path(__file__).with_name('explorador_template.html').read_text(encoding='utf-8')
    payload=json.dumps(data,ensure_ascii=False,allow_nan=False,separators=(',',':')).replace('<','\\u003c')
    (out/'explorador_generaciones.html').write_text(template.replace('__DATA__',payload),encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(description=__doc__,formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument('--input-dir',type=Path,required=True)
    ap.add_argument('--output-dir',type=Path,default=Path('resultados'))
    ap.add_argument('--territories',type=Path)
    ap.add_argument('--mode',choices=['exploratory','strict'],default='exploratory')
    ap.add_argument('--reuse',action='store_true')
    args=ap.parse_args();out=args.output_dir.resolve();out.mkdir(parents=True,exist_ok=True)
    sources=locate(args.input_dir)
    if any(out==p.parent.resolve() for p in sources.values()):
        raise ValueError('Usar una carpeta de salida separada de los originales')
    fingerprints={str(y):{'filename':p.name,'sha256':sha256(p),'bytes':p.stat().st_size}
                  for y,p in sources.items()}
    mf=out/'fuentes.json'
    if args.reuse:
        if not mf.exists() or json.loads(mf.read_text())['sources']!=fingerprints:
            raise ValueError('Las huellas no coinciden: ejecutar sin --reuse')
        old=json.loads(mf.read_text())
        for name,digest in old['derived'].items():
            if sha256(out/name)!=digest: raise ValueError('Derivado alterado: '+name)
        df=pd.read_csv(out/'agregados.csv')
    else:
        df=aggregate(sources,out)
    for y,p in sources.items():
        if sha256(p)!=fingerprints[str(y)]['sha256']:
            raise RuntimeError('Original cambió durante la ejecución: '+p.name)
    import scipy,sklearn
    manifest={'version':VERSION,'sources':fingerprints,
        'runtime':{'python':platform.python_version(),'numpy':np.__version__,
                   'pandas':pd.__version__,'scipy':scipy.__version__,'sklearn':sklearn.__version__},
        'derived':{n:sha256(out/n) for n in ['agregados.csv','auditoria.json']}}
    write_json(mf,manifest)
    diagpath=out/'diagnostico_territorial.csv'
    diag=audit_sections(sources,out)
    manifest['derived']['diagnostico_territorial.csv']=sha256(diagpath)
    manifest['mode']=args.mode
    write_json(mf,manifest)
    registry=territory_registry(args.territories)
    records=build_records(df,registry,args.mode)
    stable={(int(r.EDOCVE),int(r.MPIOCVE)):bool(r.same_section_set and not r.shared_section_changed_municipality)
            for r in diag.itertuples(index=False)}
    for r in records:r['stable_sections']=stable.get((r['ed'],int(r['key'].split('-')[1])),False)
    levels=fit_levels(records,out)
    centered=fit_models(records,out)
    models=describe_profiles(records,levels,centered)
    write_json(out/'modelos_comparados.json',models)
    audit=json.loads((out/'auditoria.json').read_text())
    render(df,records,models,audit,manifest,registry,out)
    print(json.dumps({'trajectories':len(records),'complete':sum(r['complete'] for r in records),
                      'eligible':sum(r['eligible'] for r in records),'models':len(models),
                      'html':str(out/'explorador_generaciones.html')},ensure_ascii=False),flush=True)


if __name__=='__main__': main()
