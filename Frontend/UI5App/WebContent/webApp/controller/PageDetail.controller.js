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
		generateTags: function(oEvent) {
			var docId = this.detailModel.getData(this.id);
			
//			$.ajax({
//				  type : "POST", 
//				  url : "http://localhost:5000/api/generateTags",
//				  async : false,
//				  data: $.param({docId}),
//				  success: function (data) {
//					  this.generateModel = new sap.ui.model.json.JSONModel("http://127.0.0.1:5000/api/generateTags");
//					  this.getView().setModel(this.oLocalModel);//global variable from sap.ui.getCore()
//		  },
//				 error: function (oError){
//					  sap.m.MessageToast.show("You have not downloaded anything yet!");
//				  }
//				  
//				  });
			
			
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