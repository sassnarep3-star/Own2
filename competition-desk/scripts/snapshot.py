"""Publish/check only generated static files needed by existing main/root GitHub Pages."""
import argparse,pathlib,shutil
ROOT=pathlib.Path(__file__).resolve().parents[1];OUT=ROOT/'_site'
parser=argparse.ArgumentParser();parser.add_argument('--check',action='store_true');args=parser.parse_args()
paths=['index.html','404.html','.nojekyll','assets/catalog.json','data/competitions.csv']
paths += [str(p.relative_to(OUT)) for folder in ('categories','review','summary') for p in (OUT/folder).rglob('*.html')]
for path in paths:
 src=OUT/path;dst=ROOT/path
 if args.check:
  assert dst.exists() and src.read_bytes()==dst.read_bytes(),f'Stale generated snapshot: {path}. Run build.py then snapshot.py.'
 else:dst.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(src,dst)
print(f'{"Checked" if args.check else "Published"} {len(paths)} static snapshot files for main/root Pages.')
