//##################################
// ACTIONS
//##################################

/*
 * Fire the selected action to resolve the event.
 */
function pendingEventActionFire(val) {
	$.post(val.links.fire())
}

//##################################
// MAPPINGS & MODELS
//##################################
var folkModel = function(data) {
	var self = this;
	ko.mapping.fromJS(data, {}, this);

	self.nameLength = ko.computed(function() {
		return self.first_name().length;
	});
}

function unwrapId(data) {
	return ko.utils.unwrapObservable(data.id);
}
var mapping = {
	'pending_events': {
		key: unwrapId
	},
	'folks': {
		key: unwrapId,
		create: function(options) {
			return new folkModel(options.data);
		}
	},
	'kingdom': {
		key: unwrapId
	},
	'pending_missions': {
		key: unwrapId
	},
	'messages': {
		key: unwrapId
	}
}


//##################################
// DATA BINDING
//##################################
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
