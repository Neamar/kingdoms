//##################################
// HTTP ACTIONS
//##################################

/*
 * Fire the selected action to resolve the event.
 */
function http_pendingEventActionFire(action) {
	$.post(action.links.fire(), {}, loadDatas);
}

/*
 * Affect folk_id to the specified mission grid.
 */
function http_pendingMissionGridAffect(grid, folk_id) {
	$.post(grid.links.affect(), {'folk': folk_id}, loadDatas);
}

/*
 * Affect folk_id to the specified title
 */
function http_availableTitleAffect(title, folk_id) {
	$.post(title.links.affect(), {'folk': folk_id}, loadDatas);
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
		var drop_function = valueAccessor()
		drop_function = ko.utils.unwrapObservable(drop_function)

		$(element).droppable({
			activeClass: "ui-state-hover",
			hoverClass: "ui-state-active",
			drop: drop_function
		});
	},
	update: function(element, valueAccessor, allBindingsAccessor, viewModel, bindingContext) {
		// This will be called once when the binding is first applied to an element,
		// and again whenever the associated observable changes value.
		// Update the DOM element based on the supplied values here.
	}
};


//##################################
// UI ACTIONS
//##################################

/**
 * Called when a folk is dropped onto a mission grid
 */
function droppable_pending_mission_grid_affect_folk(event, ui) {
	grid = ko.dataFor($(this)[0]);
	folk_id = ko.dataFor(ui.draggable[0]).id();
	http_pendingMissionGridAffect(grid, folk_id)
}

/**
 * Called when a folk is dropped onto an available title
 */
function droppable_available_title_affect_folk(event, ui) {
	available_title = ko.dataFor($(this)[0]);
	folk_id = ko.dataFor(ui.draggable[0]).id();
	console.log(available_title, folk_id);
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

	self.name = ko.computed(function() {
		return self.first_name() + " " + self.last_name()
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

var global_mapping = {
	create: function(options) {
		datas = ko.mapping.fromJS(options.data, mapping, this);

		self= datas
		datas.started_pending_missions = ko.computed(function() {
			return ko.utils.arrayFilter(self.pending_missions(), function(item) {
				return item.started() != null;
			})
		})

		datas.unstarted_pending_missions = ko.computed(function() {
			return ko.utils.arrayFilter(self.pending_missions(), function(item) {
				return item.started() == null;
			})
		})
		return datas;
	},
}

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
	});

}


//##################################
// LET'S ROLL
//##################################
$(function() {
	loadDatas();
});
