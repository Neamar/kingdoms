$(function() {
	datas = {
		"kingdom": [{
			"money": 50,
			"prestige": 12,
		}]
	}

	function kingdom_value(){
		var self = this;
		self.money = datas.kingdom[0].money;
		self.prestige = datas.kingdom[0].prestige;
	}


	ko.applyBindings(new kingdom_json());
});