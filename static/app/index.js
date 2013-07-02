/*
 * Fire the selected action to resolve the event.
 */
function pendingEventActionFire(val) {
	$.post(val.links.fire())
}
function unwrapId(data) {
	return ko.utils.unwrapObservable(data.id);
}
var mapping = {
	'pending_events': {
		key: unwrapId
	}
	'folks': {
		key: unwrapId 
	}
	'kingdoms': {
		key: unwrapId
	}
}

$(function() {
	var datas = null;

	function loadDatas()
	{
		$.getJSON('/api/', function(result) {
			if(!datas) //first dada mapping
			{
				datas = ko.mapping.fromJS(result, mapping);
				pager.extendWithPage(datas);
				ko.applyBindings(datas);
				pager.start();
			}
			else
			{
				ko.mapping.fromJS(result, datas);
			}

			setTimeout(loadDatas, 1000);
		});

	}

	loadDatas();
});
