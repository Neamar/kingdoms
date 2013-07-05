//##################################
// HTTP ACTIONS
//##################################
http_actions = {
	_post: function(url, param)
	{
		var jqxhr = $.post(url, param, function(data) {
			if(data.status != 'ok')
			{
				alert(data.status);
			}
		});

		jqxhr.fail(function(datas) {
			viewModel.debug_info(datas.responseText);
			document.location = "#debug";
		});

		// Always reload datas
		jqxhr.always(loadDatas);
	},

	/*
	 * Fire the selected action to resolve the event.
	 */
	pendingEventActionFire: function(action) {
		http_actions._post(action.links.fire(), {});
	},


	/*
	 * Affect folk_id to the specified mission grid.
	 */
	availableMissionStart: function(available_mission) {
		http_actions._post(available_mission.links.start());
	},


	/*
	 * Affect folk_id to the specified mission grid.
	 */
	pendingMissionGridAffect: function(grid, folk_id) {
		http_actions._post(grid.links.affect(), {'folk': folk_id});
	},

	/*
	 * Defect folk_id from the specified mission grid.
	 */
	pendingMissionGridDefect: function(affectation) {
		http_actions._post(affectation.links.defect());
	},

	/*
	 * Start the mission
	 */
	pendingMissionTarget: function(pending_mission, target_id) {
		http_actions._post(pending_mission.links.target(), {'target': target_id});
	},

	/*
	 * Start the mission
	 */
	pendingMissionStart: function(pending_mission) {
		http_actions._post(pending_mission.links.start());
	},


	/*
	 * Affect folk_id to the specified title
	 */
	availableTitleAffect: function(title, folk_id) {
		http_actions._post(title.links.affect(), {'folk': folk_id});
	},

	/*
	 * Defect the specified title
	 */
	availableTitleDefect: function(title) {
		http_actions._post(title.links.defect());
	}
}




//##################################
// CUSTOM BINDINGS
//##################################

/*
 * Allow the item to be dragged.
 */
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

/*
 * Allow dragged items to be dropped on those items.
 */
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
	http_actions.pendingMissionGridAffect(grid, folk_id)
}

/**
 * Called when a folk is dropped onto an available title
 */
function droppable_available_title_affect_folk(event, ui) {
	available_title = ko.dataFor($(this)[0]);
	folk_id = ko.dataFor(ui.draggable[0]).id();
	http_actions.availableTitleAffect(available_title, folk_id);
}

/**
 * Called when a folk is dropped onto an available title
 */
function change_pending_mission_update_target(context, event) {
	target_id = $(event.currentTarget).val()
	pending_mission = context

	if(target_id != '' && target_id != pending_mission.target())
		http_actions.pendingMissionTarget(pending_mission, target_id)

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

		datas.debug_info = ko.observable("")
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
