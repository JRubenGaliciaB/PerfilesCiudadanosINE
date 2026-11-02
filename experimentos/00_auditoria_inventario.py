rom pathlib import Path
from zipfile import ZipFile
from collections import Counter
import hashlib, csv, io, json

ROOT = Path(__file__).parent
FILES = sorted(ROOT.glob('DatosAbiertos_DECEyEC_ConteosCensales*.zip'))
REFERENCE = {'ags','bc','bcs','camp','cdmx','chih','chis','coah','col','dgo','gro','gto','hgo','jal','mex','mich','mor','nay','nl','oax','pue','qro','qroo','sin','slp','son','tab','tamps','tlax','ver','yuc','zac'}
ALIASES = {'tam': 'tamps'}  # Normalizacion SOLO para comparar nombres en el inventario.

def sha256_file(path):
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024*1024), b''):
            h.update(block)
    return h.hexdigest()

results = []
for path in FILES:
    with ZipFile(path) as z:
        members = [m for m in z.infolist() if not m.is_dir()]
        csv_files = [m for m in members if m.filename.lower().endswith('.csv')]
        docs = [m.filename for m in members if m.filename.lower().endswith('.txt')]
        state_codes = [m.filename.rsplit('/',1)[-1].rsplit('_',1)[-1].removesuffix('.csv') for m in csv_files]
        normalized = [ALIASES.get(x,x) for x in state_codes]
        header_versions = {}
        for member in csv_files:
            with z.open(member) as stream:
                header_line = stream.readline().decode('utf-8-sig', errors='replace').strip('\r\n')
            columns = next(csv.reader([header_line]))
            header_versions[member.filename.rsplit('/',1)[-1]] = columns
        uniq = {tuple(cols) for cols in header_versions.values()}
        results.append({'archivo':path.name, 'sha256':sha256_file(path),
            'total_csv_estatales':len(csv_files),'codigos_de_archivo':state_codes,
            'faltantes_por_nombre':sorted(REFERENCE-set(normalized)),
            'duplicados_por_nombre':sorted(x for x,n in Counter(normalized).items() if n>1),
            'documentacion':docs,'esquemas_de_cabecera':[list(x) for x in sorted(uniq)],
            'archivos_por_cabecera':header_versions})

out = ROOT / '00_inventario_ccpc.json'
out.write_text(json.dumps({'alcance':'Solo metadatos y encabezados; no se han inspeccionado las filas de datos.',
                            'archivos':results},ensure_ascii=False,indent=2),encoding='utf-8')
print('Inventario escrito en:',out)
for r in results:
    print(r['archivo'], '| CSV:',r['total_csv_estatales'], '| faltantes:',r['faltantes_por_nombre'], '| esquemas:',len(r['esquemas_de_cabecera']))

