# __main__.py

import sys

from .pdf_join import pdf_join

def main():
	'''
	Run pdfmerge to merge PDFs.
	'''
	out = [arg for i, arg in enumerate(sys.argv[1:]) if sys.argv[1:][i-1] == '--out']
	if not out:
		out = 'merged.pdf'
	else: 
		out = out[0]
	
	args = [arg for i, arg in enumerate(sys.argv[1:]) if arg not in ['pdf_join.py', '--out'] and not sys.argv[1:][i-1] == '--out']
	pdf_join(args, out=out)

if __name__ == '__main__':
	main()