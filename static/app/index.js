//##################################
// DATA BINDING
//##################################
var viewModel = null;

function loadDatas()
{
	$.getJSON('/api/', function(result) {
		if(!viewModel) //first dada mapping
		{
			viewModel = ko.mapping.fromJS(result, global_mapping);
			pager.extendWithPage(viewModel);

			ko.applyBindings(viewModel);
			pager.start();
		}
		else
		{
			ko.mapping.fromJS(result, viewModel);
		}

		setTimeout(loadDatas, 1000)
	});

}


//##################################
// LET'S ROLL
//##################################
$(function() {
	loadDatas();
});
