import os
import sys

src_dir = os.getcwd()

languages = {
	'.py': 'python',
	'.js': 'javascript',
	'.html': 'html',
	'.css': 'css',
}

exclude_dirs = [
	os.path.join(src_dir, 'flask'),
	os.path.join(src_dir, 'werkzeug'),
]

def writeHeader(output):
	output.write('\n')
	output.write('# Source Code for Nebulous Adventure')
	output.write('\n\n')

def writeSource(output, file, lang):
	rel_file = os.path.relpath(file, src_dir)
	# Write Markdown header info
	output.write('\n')
	output.write('## {0}'.format(rel_file))
	output.write('\n\n')
	
	# Write GitHub flavored Markdown info
	output.write('```{0}'.format(lang))
	output.write('\n')
	
	# Write file source
	src_file = open(file)
	output.writelines(src_file.xreadlines())
	
	output.write('\n')
	output.write('```')
	output.write('\n')
	

def visit(output, dirname, files):
	print 'Visiting {0}'.format(dirname)
	
	prefix = ''
	for exclude in exclude_dirs:
		prefix = os.path.commonprefix((exclude, dirname))
		if prefix == exclude:
			return

	if dirname in exclude_dirs:
		return
	
	for file in files:
		print 'Iterating with file: {0}'.format(file)
		root, ext = os.path.splitext(file)
		
		if ext in languages:
			lang = languages[ext]
			file_path = os.path.join(dirname, file)
			writeSource(output, file_path, lang)
			
def main(args):
	output = open(os.path.join(src_dir, 'SOURCE.md'), 'w')
	writeHeader(output)
	
	# Well this function is short =]
	os.path.walk(src_dir, visit, output)
	
	output.close()
	
	return 0

	
if __name__ == '__main__':
	sys.exit(main(sys.argv))
