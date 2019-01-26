sap.ui.jsview("webApp.view.Page1", {

	/** Specifies the Controller belonging to this View. 
	* In the case that it is not implemented, or that "null" is returned, this View does not have a Controller.
	* @memberOf demo.Page1
	*/ 
	getControllerName : function() {
		return "webApp.controller.Page1";
	},

	/** Is initially called once after the Controller has been instantiated. It is the place where the UI is constructed. 
	* Since the Controller is given to this method, its event handlers can be attached right away. 
	* @memberOf demo.Page1
	*/ 
	createContent : function(oController) {
		
		var oText1 = new sap.ui.commons.TextView({
			text: "Confluence URL: "
		});
		
		var oInput1 = new sap.ui.commons.TextField(this.createId("url"),{
			value: "url"
		});
		
		
		var oButton = new sap.ui.commons.Button({
			text: "save and connect",
			press: function() {
				oController.navigateToPage2("Page2");
			}
		});
		
		var ele = [oText1,oInput1,oText2,oInput2,oText3,oInput3, oButton];
		
		return ele;
		
	}

});
