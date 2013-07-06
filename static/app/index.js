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
	 * Set a target for the mission
	 */
	pendingMissionTarget: function(pending_mission, target_id) {
		http_actions._post(pending_mission.links.target(), {'target': target_id});
	},

	/*
	 * Set a value for the mission
	 */
	pendingMissionValue: function(pending_mission, value) {
		http_actions._post(pending_mission.links.value(), {'value': value});
	},

	/*
	 * Start the mission
	 */
	pendingMissionStart: function(pending_mission) {
		http_actions._post(pending_mission.links.start());
	},

	/*
	 * Cancel the mission
	 */
	pendingMissionCancel: function(pending_mission) {
		http_actions._post(pending_mission.links.cancel());
	},

	/*
	 * Cancel the bargain
	 */
	pendingBargainCreate: function(bargains_partners, partner) {
		http_actions._post(bargains_partners.links.create(), {'partner': partner});
	},

	/*
	 * Share a mission into the bargain
	 */
	pendingBargainShare: function(pending_bargain, pending_mission_id) {
		http_actions._post(pending_bargain.links.share(), {'pending_mission': pending_mission_id});
	},

	/*
	 * Set state for pending bargain
	 */
	pendingBargainState: function(pending_bargain, state_id) {
		http_actions._post(pending_bargain.links.state(), {'state': state_id});
	},

	/*
	 * Cancel the bargain
	 */
	pendingBargainDelete: function(pending_bargain) {
		http_actions._post(pending_bargain.links.delete());
	},

	/*
	 * Cancel the bargain
	 */
	sharedPendingMissionDelete: function(shared_pending_mission) {
		http_actions._post(shared_pending_mission.links.delete());
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
 * Update the target for the mission
 */
function change_pending_mission_update_target(context, event) {
	target_id = $(event.currentTarget).val()
	pending_mission = context

	if(target_id != '' && target_id != pending_mission.target())
		http_actions.pendingMissionTarget(pending_mission, target_id)
}


/**
 * Update the value for the mission
 */
function change_pending_mission_update_value(context, event) {
	value = $(event.currentTarget).val()
	pending_mission = context

	if(value != '' && value != pending_mission.value())
		http_actions.pendingMissionValue(pending_mission, value)
}


/**
 * Update the state for the pending bargain
 */
function change_pending_bargain_create(context, event) {
	partner = $(event.currentTarget).val()
	bargains_partners = context.bargains_partners
	if(partner != '')
		http_actions.pendingBargainCreate(bargains_partners, partner)
}

/**
 * Update the state for the pending bargain
 */
function click_pending_bargain_update_state(context, event) {
	state_id = $(event.currentTarget).data('state')
	pending_bargain = context

	if(state_id != pending_bargain.state())
		http_actions.pendingBargainState(pending_bargain, state_id)
}

/**
 * Delete the pending bargain
 */
function click_pending_bargain_delete(context, event) {
	pending_bargain = context

	http_actions.pendingBargainDelete(pending_bargain)
}

/**
 * Share a mission into the bargain
 */
function click_pending_bargain_share(context, event) {
	pending_bargain = ko.dataFor($(event.currentTarget).parents('div')[0]);
	pending_mission_id = context.id()

	http_actions.pendingBargainShare(pending_bargain, pending_mission_id)
}

/**
 * Remove a shared mission from the bargain
 */
function click_shared_pending_mission_delete(context, event) {
	shared_pending_mission = context

	http_actions.sharedPendingMissionDelete(shared_pending_mission)
}


/**
 * Update the target for the mission
 */
function change_pending_mission_update_target(context, event) {
	target_id = $(event.currentTarget).val()
	pending_mission = context

	if(target_id != '' && target_id != pending_mission.target())
		http_actions.pendingMissionTarget(pending_mission, target_id)
}

//##################################
// UI animation
//##################################

function yellow_fade_in(element, index, data) {
	console.log("ok")
	$(element).filter("li")
		.animate({ backgroundColor: 'yellow' }, 200)
		.animate({ backgroundColor: 'white' }, 800);
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


var pendingMissionModel = function(data) {
	var self = this;
	ko.mapping.fromJS(data, {}, this);

	self.target_name = ko.computed(function() {
		target = ko.utils.arrayFirst(self.targets(), function(t) { return t.id() == self.target()})
		if(target)
			return target.name()
		else
			return '∅'
	});
}


var pendingBargainModel = function(data, parent) {
	var self = this;

	ko.mapping.fromJS(data, {}, this);

	self.filter_pending_missions = function(pending_missions) {
		a = ko.utils.arrayFilter(pending_missions, function(pending_mission) {
			val = ko.utils.arrayFirst(self.shared_missions(), function(shared_mission) {
				return pending_mission.id() == shared_mission.pending_mission.id()
			});
			return null == val
		});
		return a
	};
};


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
			return new pendingMissionModel(options.data);
		}
	},
	'pending_bargains': {
		key: unwrapId,
		create: function(options) {
			return new pendingBargainModel(options.data, options.parent);
		}
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
