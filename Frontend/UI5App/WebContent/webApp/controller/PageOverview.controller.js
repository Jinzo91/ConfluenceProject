sap.ui.controller("webApp.controller.PageOverview",{
//	return Controller.extend("Webapp.controller.PageOverview", {
//
//		formatter: formatter,

		onInit: function () {
//			this.myModel = new sap.ui.model.json.JSONModel();
//			var oModel = new sap.ui.model.json.JSONModel("http://127.0.0.1:5000/confluencedata");
//			this.getView().setModel(oModel);
		
			//var oModel = this.oModel;//NOT WORKING：temporary variable from ajax request
			//console.log("Ajax data: ", this.oModel);

			this.getView().setModel(sap.ui.getCore().getModel(this.oModel));//global variable from sap.ui.getCore()
			
			this.dataModel = new sap.ui.model.json.JSONModel();
		},
		updateDetails: function(oEvent) {
			// first, we need to get the context of the selected
			// row from the event
			
			var rowContext = oEvent.getParameter("rowContext");
			var title = rowContext.getObject().title;
			var date = rowContext.getObject().date;
			var body = rowContext.getObject().body;
			var id = rowContext.getObject().body;
			var tags = rowContext.getObject().tags;
			var toDetail = {
					title: title,
					date: date,
					body: body,
					id:id,
					tags:tags
			}
			// now we can set the Input to the value of a
			// field of the selected row
			console.info("Detail: ", toDetail);
			this.dataModel.setData(toDetail);
			console.log("data Model: ", this.dataModel)
			sap.ui.getCore().setModel(this.dataModel);
			var oRouter = sap.ui.core.routing.Router.getRouter("appRouter");
			oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
			oHashChanger.setHash(oRouter.getURL('PageDetail'));
			console.info("Data model from Overview: ", this.dataModel);
			},
			
			HandleSearch: function (oEvent) {
				// build filter array
				var aFilter = [];
				var sQuery = oEvent.getParameter("query");
				if (sQuery) {
					aFilter.push(new sap.ui.model.Filter("title", sap.ui.model.FilterOperator.Contains, sQuery));
					
				}
				// filter binding
				var oList = this.byId("pageoverview");
				console.log(oList);
				var oBinding = oList.getBinding("rows");
				console.log(aFilter);
				oBinding.filter(aFilter);
			}

});