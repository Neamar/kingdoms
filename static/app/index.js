$(function() {
	var datas = null;

	function loadDatas()
	{
		$.getJSON('/api/', function(result) {
			if(!datas)
			{
				datas = ko.mapping.fromJS(result);
				pager.extendWithPage(datas);
				ko.applyBindings(datas);
				pager.start();
			}
			else
			{
				ko.mapping.fromJS(result, datas);
			}
		});

		setTimeout(loadDatas, 4000);
	}

	loadDatas();
});
