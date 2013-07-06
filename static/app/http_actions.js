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
