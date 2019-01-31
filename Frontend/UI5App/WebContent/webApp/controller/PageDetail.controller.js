sap.ui.controller("webApp.controller.PageDetail",{
		//set Model for view, and the data is from global model "dataModel" to local model "detailModel"  
		onInit: function () {
			this.detailModel = new sap.ui.model.json.JSONModel();
			this.detailModel = sap.ui.getCore().getModel(this.dataModel);
			this.getView().setModel(this.detailModel);
		},
		//go back to pageOverview
		onNavBack:function()
		{
			var oHistory = sap.ui.core.routing.History.getInstance();
			var sPreviousHash = oHistory.getPreviousHash();
			console.log("Back to: " + sPreviousHash);
			if (sPreviousHash !== undefined) {
				window.history.go(-1);
			} 
			else {
				oHashChanger.setHash(oRouter.getURL('PageOverview'))
			}
		},
		tagging: function(oEvent) {
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
		acceptTags: function(oEvent) {
			
		},
		rejectTags: function(oEvent) {
			
		},

});