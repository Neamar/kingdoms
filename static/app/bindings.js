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
