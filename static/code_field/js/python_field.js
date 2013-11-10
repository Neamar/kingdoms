CodeMirrorConfig.stylesheet = "/static/code_field/css/pythoncolors.css";
CodeMirrorConfig.path = "/static/code_field/js/";
CodeMirrorConfig.parserfile = "parsepython.js";
CodeMirrorConfig.height = "dynamic";
CodeMirrorConfig.indentUnit = 2;
CodeMirrorConfig.lineNumbers = true;

var convert_to_CodeMirror = function(obj){
	// alert(obj);
	var id = $(obj).attr('id');
	if (!id.match(/__prefix__/)) {
	// alert(id);
	var editor = CodeMirror.fromTextArea(id);
	}
};

$(document).ready(function(){
	function convert()
	{
		$('.python-code:visible').each(function(i,obj){
			convert_to_CodeMirror($(obj));
		});
	}

	$('.add-row a, a.collapse-toggle').click(function(){
		setTimeout(convert, 50);
	})

	convert()
});
