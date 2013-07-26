//##################################
// MAPPINGS & MODELS
//##################################

// Function used for mapping, to avoid updating DOM when no changes.
// See documentation for Knockout mapping plugin.
function unwrapId(data) {
	return ko.utils.unwrapObservable(data.id);
}

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
	mapping = {
		'grids': {
			key: unwrapId
		}
	}

	var self = this;
	ko.mapping.fromJS(data, mapping, this);

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
	},
	'available_titles': {
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
		});

		datas.unstarted_pending_missions = ko.computed(function() {
			return ko.utils.arrayFilter(self.pending_missions(), function(item) {
				return item.started() == null;
			})
		});

		datas.lol = ko.computed(function() {
			//console.log(self.pending_missions(), datas.unstarted_pending_missions());
		});

		datas.debug_info = ko.observable("")
		return datas;
	},
}
