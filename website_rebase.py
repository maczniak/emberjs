#!/usr/bin/python
#
# The original Ember.js website is under http://emberjs.com/.  And translation
# website is under http://maczniak.github.io/emberjs/.  Then all absolute urls
# were broken. I failed to search generic html rebase tools, made a simple
# script in Python.  It is a specific solution to this problem.
#   see also: http://a3nm.net/blog/htmlrebase.html

#-- configuration start --
BUILD_ROOT = 'build/'
PREFIX = 'emberjs/' # must include a trailing slash only
#-- configuration end --

import os
import os.path
import re

# <link href="/stylesheets/fonts/fontello-ie7.css" media="screen" rel="stylesheet" type="text/css" />
html_link_str = '<link.*?href="/'
html_link_pattern = re.compile(html_link_str)

# _gaq.push(['_setAccount', 'UA-27675533-1']);
# from layout.erb
html_ga_str = 'UA-27675533-1'
html_ga_pattern = re.compile(html_ga_str)

# <script type="text/javascript" src="/javascripts/common-old-ie.js"></script>
html_script_str = '<script.*?src="/(?=[^/])'
html_script_pattern = re.compile(html_script_str)

# <a id="logo" href="/">
# <a href="/guides">
html_a_str = '<a .*?href="/'
html_a_pattern = re.compile(html_a_str)

# <img src="/images/about/mhelabs.png">
# exclude src="//ssl.gstatic.com/images/icons/gplus-32.png"
html_img_str = '<img.*?src="/(?=[^/])'
html_img_pattern = re.compile(html_img_str)

# var i=r.map(function(e){return $.ajax("/javascripts/app/examples/"+n+"/
# from javascripts/app/about/inline-examples.js
# <div class="example-app example-loading" data-name="loading" data-files="app.js templates/application.hbs">
js_ajax_str = '[$][.]ajax[(]"/'
js_ajax_pattern = re.compile(js_ajax_str)

# background-image:url("/images/background-shades.svg")
css_url_str = 'url[(]"/'
css_url_pattern = re.compile(css_url_str)

# url("../../fonts -> url("../fonts
css_font_str = 'url[(]"../../'
css_font_pattern = re.compile(css_font_str)

def read(filename):
	f = open(filename, 'r')
	content = f.read()
	f.close()
	return content

def write(filename, content):
	f = open(filename, 'w')
	content = f.write(content)
	f.close()

def handle_html(filename):
	content = read(filename)
	content = html_link_pattern.sub('\g<0>' + PREFIX, content)
	content = html_ga_pattern.sub('UA-45832618-1', content)
	content = html_script_pattern.sub('\g<0>' + PREFIX, content)
	content = html_a_pattern.sub('\g<0>' + PREFIX, content)
	content = html_img_pattern.sub('\g<0>' + PREFIX, content)
	write(filename, content)

def handle_js(filename):
	content = read(filename)
	content = js_ajax_pattern.sub('\g<0>' + PREFIX, content)
	write(filename, content)

def handle_css(filename):
	content = read(filename)
	content = css_url_pattern.sub('\g<0>' + PREFIX, content)
	content = css_font_pattern.sub('url("../', content)
	write(filename, content)

def extension(filename):
	idx = filename.rfind('.')
	if idx == -1:
		return ''
	else:
		return filename[idx:]

for root, dirs, files in os.walk(BUILD_ROOT):
	for file in files:
		ext = extension(file)
		if ext == '.html':
			handle_html(os.path.join(root, file))
		elif ext == '.js':
			handle_js(os.path.join(root, file))
		elif ext == '.css':
			handle_css(os.path.join(root, file))

