//##################################
// CUSTOM BINDINGS
//##################################
ko.bindingHandlers.draggable = {
	init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
		$(element).draggable({ opacity: 0.9, helper: "clone" });
	},
	update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
		// This will be called once when the binding is first applied to an element,
		// and again whenever the associated observable changes value.
		// Update the DOM element based on the supplied values here.
	}
};

ko.bindingHandlers.droppable = {
	init: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
		$(element).droppable({
			activeClass: "ui-state-hover",
			hoverClass: "ui-state-active"
		});
	},
	update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
		// This will be called once when the binding is first applied to an element,
		// and again whenever the associated observable changes value.
		// Update the DOM element based on the supplied values here.
	}
};

//##################################
// HTTP ACTIONS
//##################################

/*
 * Fire the selected action to resolve the event.
 */
function http_pendingEventActionFire(action) {
	$.post(val.links.fire())
}

function http_pendingMissionGridAffect(mission, grid_id, folk_id) {
	console.log(mission, grid_id, folk_id);
}

//##################################
// UI ACTIONS
//##################################

/**
 * Affect someone to some grid.
 */
function pendingMissionGridAffect(val)
{
	if(!val.targetOrigin)
	{
		//http_pendingMissionGridAffect
		mission_id = ko.dataFor($(val.sourceParentNode).parent().parent()[0]).id();
		grid_id = ko.dataFor(val.sourceParentNode).id();
		folk_id = val.item.id()

		http_pendingMissionGridAffect(mission_id, grid_id, folk_id);
	}

	val.cancelDrop = true;
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

			//setTimeout(loadDatas, 1000);
		});

	}

	loadDatas();
});
