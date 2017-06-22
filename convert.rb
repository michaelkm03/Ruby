require 'reverse_markdown'
require 'FileUtils'

Dir.chdir("/Users/michaelmontgomery/Desktop/html")
txt_dir = "/Users/michaelmontgomery/Desktop/txt"
all_html = Dir.glob "*.html"

Dir.foreach(Dir.pwd) {|x|
	puts Dir.pwd
	puts x
	next if x == '.' or x == '..' or x =='.DS_Store' or x == 'attachments' or x == 'styles' or x =='images'
	file = File.open("/Users/michaelmontgomery/Desktop/html/#{x}", 'r')
	data = file.read
	result = ReverseMarkdown.convert data

	# Create a new file and write to it  
	f = File.new('/Users/michaelmontgomery/Desktop/txt/#{x}', 'w+')
	f.puts result
}