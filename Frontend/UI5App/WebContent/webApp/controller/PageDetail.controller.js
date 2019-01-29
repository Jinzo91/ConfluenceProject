sap.ui.require([
  "sap/m/FormattedText",
  "sap/ui/core/HTML"
], function(HTML) {

  new HTML({
    content: "<b>Hello</b> <i>world</i>"
  }).placeAt("body");

});
sap.ui.controller("webApp.controller.PageDetail",{

		onInit: function () {
			var oModel = sap.ui.getCore().getModel(this.dataModel);
			console.log("On Detail Page: ", oModel);
			this.getView().setModel(oModel);
		},
		onNavBack:function()
		{
			var oHistory = sap.ui.core.routing.History.getInstance();
			var sPreviousHash = oHistory.getPreviousHash();
			console.log("Back to: " + sPreviousHash);
			if (sPreviousHash !== undefined) {
				window.history.go(-1);
			} 
			else {
				oHashChanger.setHash(oRouter.getURL('PageDetail'))
			}
		},
		updateDetails: function(oEvent) {
//
//			
//			var rowContext = oEvent.getParameter("rowContext");
//			var documentTitle = rowContext.getObject().title;
//			var body = rowContext.getObject().body;
//			var tags = rowContext.getObject().tags;
//			console.log(documentTitle);
//			this.dataModel.setData(rowContext);
//			console.log(this.dataModel);
//			sap.ui.getCore().setModel(this.dataModel);
//			var oRouter = sap.ui.core.routing.Router.getRouter("appRouter");
//			oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
//			oHashChanger.setHash(oRouter.getURL('PageDetail'));
			},

});