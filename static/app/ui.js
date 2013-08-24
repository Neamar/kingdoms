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
 * Create a new pending mission
 */
function click_available_mission(context, event) {
	http_actions.availableMissionStart(context);
	document.location = "#mission";
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
	bargain_partner = ko.utils.arrayFirst(context.bargains_partners(), function(b) { return b.id() == partner });

	if(partner != '')
		http_actions.pendingBargainCreate(bargain_partner)
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

/**
 * Create a new freeze
 */
function click_create_freeze(context, event) {
	http_actions.createFreeze(context.freezes);
}

/**
 * Restore previous freeze
 */
function click_restore_freeze(context, event) {
	http_actions.restoreFreeze(context.freezes);
}


//##################################
// UI animation
//##################################

function yellow_fade_in(element, index, data) {
	$(element).filter("li")
		.animate({ backgroundColor: 'yellow' }, 200)
		.animate({ backgroundColor: 'white' }, 800);
}
