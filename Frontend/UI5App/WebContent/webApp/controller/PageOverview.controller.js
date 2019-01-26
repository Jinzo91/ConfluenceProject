//sap.ui.define([
//	"sap/ui/core/mvc/Controller",
//	"sap/ui/model/json/JSONModel",
//	"../model/formatter",
//	"sap/ui/model/Filter",
//	"sap/ui/model/FilterOperator",
//	"sap/ui/core/UIComponent",
//	"sap/ui/model/resource/ResourceModel"
//	])
sap.ui.controller("webApp.controller.PageOverview",{
//	return Controller.extend("Webapp.controller.PageOverview", {
//
//		formatter: formatter,

		onInit: function () {
			this.myModel = new sap.ui.model.json.JSONModel();

	    	var oData = {
					recipient : {
						username : "Ben"
					}
				};
			var oModel = new sap.ui.model.json.JSONModel(oData);
			this.getView().setModel(oModel);
			
			var invoiceModel = new sap.ui.model.json.JSONModel({
		            bundleName: "webApp.Invoices"
		         });
		        this.getView().setModel(invoiceModel, "invoice");
	        
		},

		onFilterInvoices: function (oEvent) {
			// build filter array
			
			var aFilter = [];
			var sQuery = oEvent.getParameter("query");
			if (sQuery) {
				aFilter.push(new Filter("Title", FilterOperator.Contains, sQuery));
			}

			// filter binding
			var oList = this.byId("invoiceList");
			var oBinding = oList.getBinding("items");
			oBinding.filter(aFilter);
		},

		onPress: function (oEvent) {
			var oItem = oEvent.getSource();
			var oRouter = UIComponent.getRouterFor(this);
			var sPath = oItem.getBindingContext("invoice").getPath();
			oRouter.navTo("detail", {
			invoicePath: encodeURIComponent(sPath)
		});
			 
		}

});