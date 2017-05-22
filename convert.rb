require 'reverse_markdown'
require 'FileUtils'

html_dir = Dir.chdir("/Users/michaelmontgomery/Desktop/html")
txt_dir = "/Users/michaelmontgomery/Desktop/txt"
all_text_files = Dir.glob "*.html"

Dir.foreach(Dir.pwd) {|x|
	next if x == '.' or x == '..' or x =='.DS_Store' or x == 'attachments' or x == 'styles' or x =='images'
	file = File.open("/Users/michaelmontgomery/Desktop/html/#{x}", 'r')
	data = file.read

	result = ReverseMarkdown.convert data

	destination = File.new("/Users/michaelmontgomery/Desktop/txt/#{x}.txt", "w")
}
