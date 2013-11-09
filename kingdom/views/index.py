import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.conf import settings


@login_required
def app(request):
	"""
	Display main app
	"""
	return render(request, 'app/index.html')


def errors(request):
	if settings.ERROR_FILE == '':
		raise Http404("Error file not configured -- set up ERROR_FILE in settings.")

	with open(settings.ERROR_FILE, 'r') as content_file:
		content = content_file.read()

	content = content.replace('<', '&lt;')
	content = content.replace('>', '&gt;');
	content = re.sub(r'\[(.+)(Internal Server Error.+)\n', r'<hr><span style="color:red;">\g<2></span>\n', content)
	content = re.sub(r'\[error\]([^\n]+module&gt;)', r'<b>\g<0></b>', content)
	content = re.sub(r'\[error\] (\S.*)\n', r'<b>\g<1></b>\n', content)
	return HttpResponse('<pre>' + content + '</pre>', content_type="text/html")


def dependencies(request, output_type):
	"""
	Display dependencies graph, automatically generated just for you.
	"""
	import subprocess

	from django.core.management import call_command
	from StringIO import StringIO


	dependencies_file_dot = '/tmp/dependencies.dot'

	params = request.GET.keys()

	content = StringIO()
	error = StringIO()
	call_command('dependencies', *params, stdout=content, stderr=error)
	content.seek(0)
	error.seek(0)
	error = error.read()
	if error != '':
		return HttpResponse(error)

	dot_file = content.read()

	# Dot file: return everything right now
	if output_type == 'dot':
		return HttpResponse(dot_file, mimetype='text/plain')

	# Else, store in temp file
	with open(dependencies_file_dot, 'wb+') as temp_file:
		temp_file.write(dot_file)

	if output_type not in ['png', 'svg']:
		raise Http404("Unknown output type.")

	params = [
		'dot',
		'-T',
		output_type,
		dependencies_file_dot
	]

	datas = subprocess.check_output(params)

	if output_type == 'svg':
		response = HttpResponse(datas)
	else:
		response = HttpResponse(datas, mimetype='image/png')
		response["Content-Length"] = len(datas)
	return response
