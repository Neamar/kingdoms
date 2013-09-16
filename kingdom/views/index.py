from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404


@login_required
def app(request):
	"""
	Display main app
	"""
	return render(request, 'app/index.html')


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

	if subprocess.call(params) == 0:
		svg_datas = subprocess.check_output(params)

		if output_type == 'svg':
			response = HttpResponse(svg_datas)
		else:
			response = HttpResponse(svg_datas, mimetype='image/png')
			response["Content-Length"] = len(svg_datas)
		return response
	else:
		raise Http404("Unable to generate dependencies.")
