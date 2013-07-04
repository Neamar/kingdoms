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
var folkModel = function(data, qualities) {
	var self = this;
	ko.mapping.fromJS(data, {}, this);

	self.qualities = ko.computed(function() {
		return ko.utils.arrayMap(self.raw_qualities(), function(raw_quality) {
				return qualities[raw_quality];
		});
	});
}

var pendingMissionModel = function(data, qualities) {
	var self = this;
	ko.mapping.fromJS(data, {}, this);

	self.affectations = ko.utils.arrayMap(self.affectations, function(affectation) {
			if(affectation != null)
				return new folkModel(affectation);
			else
				return null;
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
			return new folkModel(options.data, options.parent.qualities);
		}
	},
	'kingdom': {
		key: unwrapId
	},
	'pending_missions': {
		key: unwrapId,
		create: function(options) {
			return new pendingMissionModel(options.data, options.parent.folks);
		}
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
