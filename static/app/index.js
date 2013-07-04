//##################################
// HTTP ACTIONS
//##################################

/*
 * Fire the selected action to resolve the event.
 */
function http_pendingEventActionFire(action) {
	$.post(action.links.fire());
}

function http_pendingMissionGridAffect(grid, folk_id) {
	$.post(grid.links.affect(), {'folk': folk_id});
}


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
			hoverClass: "ui-state-active",
			drop: function( event, ui ) {
				grid = ko.dataFor($(this)[0]);
				folk_id = ko.dataFor(ui.draggable[0]).id();
				http_pendingMissionGridAffect(grid, folk_id)
			}
		});
	},
	update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
		// This will be called once when the binding is first applied to an element,
		// and again whenever the associated observable changes value.
		// Update the DOM element based on the supplied values here.
	}
};


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
