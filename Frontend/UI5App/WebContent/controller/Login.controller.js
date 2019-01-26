sap.ui.define([
	"sap/ui/core/mvc/Controller",
	"sap/ui/model/json/JSONModel",
	"../model/formatter",
	"sap/m/MessageToast",
	"sap/ui/core/UIComponent"
], function (Controller, formatter,JSONModel,UIComponent) {
	"use strict";

	return Controller.extend("sap.ui.demo.walkthrough.controller.Login", {
		formatter: formatter,
		
		onInit: function () {
			
		},
		onLogin : function (oEvent) {
//
//			var username = this.getView().getModel().getProperty("/recipient/name");
			if(true){
				var oRouter = sap.ui.core.UIComponent.getRouterFor(this); 
				var oModel = new sap.ui.model.json.JSONModel();
				oModel.loadData("https://jsonplaceholder.typicode.com/todos/1");
//				oRouter.navTo("firstpage");
				console.log(oModel);
			}
		}

	});

});