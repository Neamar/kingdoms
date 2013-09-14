from django.shortcuts import render_to_response, render
from django.contrib.auth import authenticate, login as login_user
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404


@login_required
def app(request):
	"""
	Display main app
	"""
	return render(request, 'app/index.html')


def dependencies(request, output_type="svg"):
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

	if output_type=="png":
		dependencies_file_image = '/tmp/dependencies.png'

		# Export as PNG image
		params = [
			'dot',
			'-T',
			'png',
			'-o',
			dependencies_file_image,
			dependencies_file_dot
		]

		if subprocess.call(params) == 0:
			contents = open(dependencies_file_image, 'rb').read()
			response = HttpResponse(contents, mimetype='image/png')
			response["Content-Length"] = len(contents)
			return response
	else:
		# Export as SVG
		params = [
			'dot',
			'-T',
			'svg',
			dependencies_file_dot
		]

		svg_datas = subprocess.check_output(params)
		response = HttpResponse(svg_datas)

		return response
