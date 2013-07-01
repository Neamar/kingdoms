$(function() {
	var datas = null;

	function loadDatas()
	{
		$.getJSON('/api', function(result) {
			old_datas = datas;
			datas = ko.mapping.fromJS(result);

			if(!old_datas)
				ko.applyBindings(datas);
		});
	}

	loadDatas();
});
