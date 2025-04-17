import sys
from tqdm import tqdm
from glob import glob

from PyPDF2 import PdfMerger

def flatten(l: list) -> list:
	return [i for sl in l for i in sl]

def pdf_join(files, out):
	'''
	Merges all PDFs in files in order. Globs first.
	'''
	files = [f'{file}.pdf' if (not file.endswith('.pdf') and not file.endswith('.PDF')) else file for file in files]
	files = [glob(file, recursive=True) for file in files]
	files = flatten(files)
	
	if not files:
		print(f'No PDFs found: {files=}.')
		return
	
	merger = PdfMerger()
	print('Merging PDFs...')
	for file in tqdm(files):
		merger.append(file)
	
	merger.write(out)

if __name__ == '__main__':
	out = [arg for i, arg in enumerate(sys.argv[1:]) if sys.argv[1:][i-1] == '--out']
	if not out:
		out = 'merged.pdf'
	else:
		out = out[0]
	
	args = [arg for i, arg in enumerate(sys.argv[1:]) if arg not in ['pdf_join.py', '--out'] and not sys.argv[1:][i-1] == '--out']
	pdf_join(args, out=out)
