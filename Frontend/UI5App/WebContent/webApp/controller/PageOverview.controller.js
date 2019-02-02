sap.ui.controller("webApp.controller.PageOverview",{

		onInit: function () {
			
			this.dataModel = new sap.ui.model.json.JSONModel();
			this.oDownload = new sap.ui.model.json.JSONModel();
			this.oLocalModel = new sap.ui.model.json.JSONModel();
			var localName = {};
			this.i = 1;
			this.j = 1;
			this.q = 1;
		},
		Download: function(oEvent){
			this.oDownload = new sap.ui.model.json.JSONModel("http://127.0.0.1:5000/api/confluencedata/download");
			sap.m.MessageToast.show("Downloading...");
			console.log(this.oDownload);
			this.getView().setModel(this.oDownload);
			this.showLocalData();
			  
			  
		},
		showLocalData: function(oEvent){
			this.oLocalModel = new sap.ui.model.json.JSONModel("http://127.0.0.1:5000/api/confluencedata");
			this.getView().setModel(this.oLocalModel);//global variable from sap.ui.getCore()
		},
		updateDetails: function(oEvent) {
			// first, we can get the selected row and information of this row from the event
			//and these information is binded to "toDetail"
			var rowContext = oEvent.getParameter("rowContext");
			var title = rowContext.getObject().title;
			var date = rowContext.getObject().date;
			var body = rowContext.getObject().body;
			var id = rowContext.getObject().documentId;
			var tags = rowContext.getObject().tags;
			var toDetail = {
					title: title,
					date: date,
					body: body,
					id:id,
					tags:tags
			}
			// now we bind toDetail to dataModel and make it global
			this.dataModel.setData(toDetail);
			//console.log("data Model: ", this.dataModel)
			sap.ui.getCore().setModel(this.dataModel);
			// then we will rout to detail page
			var oRouter = sap.ui.core.routing.Router.getRouter("appRouter");
			oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
			oHashChanger.setHash(oRouter.getURL('PageDetail'));
			console.info("Data model from Overview: ", this.dataModel);
		},
			//we get the data from event,and find rows contain them 
			HandleSearch: function (oEvent) {
				// build filter array
				var aFilters = [];
				var sQuery = oEvent.getParameter("query");
				var oList = this.byId("pageoverview");
				console.log(oList);
				console.log(sQuery);
				// bind the filter result with table content with table id "pageOverview"
				var oBinding = oList.getBinding("rows");
				aFilters.push(new sap.ui.model.Filter("title", sap.ui.model.FilterOperator.Contains, sQuery));
				aFilters.push(new sap.ui.model.Filter("date", sap.ui.model.FilterOperator.Contains, sQuery));
				aFilters.push(new sap.ui.model.Filter("tags", sap.ui.model.FilterOperator.Contains, sQuery));	
				console.log(aFilters);
				oBinding.filter(new sap.ui.model.Filter({filters: aFilters, and: false}));
			},
			//when click button at first time, show table content in descending sort based on "tags"
			//the second click show in ascending sort 
			sortByTags: function(oEvent){
				if (this.i % 2 == 1){
					var cFilter = [];
					var oList = this.byId("pageoverview");
					var oBinding = oList.getBinding("rows");
					cFilter.push(new sap.ui.model.Sorter("tags", bDescending=true));
					oBinding.sort(cFilter);}
				else {
				var cFilter = [];
				var oList = this.byId("pageoverview");
				var oBinding = oList.getBinding("rows");
				cFilter.push(new sap.ui.model.Sorter("tags", bDescending=false));
				oBinding.sort(cFilter);
				}
				this.i = this.i+1
				//new sap.ui.model.Filter("title", sap.ui.model.FilterOperator.Contains, sQuery)
				
			},
			//when click button at first time, show table content in descending sort based on "date"
			//the second click show in ascending sort 
			sortByDate: function(oEvent){
				console.log(this.j);
				if (this.j % 2 == 1){
					var cFilter = [];
					var oList = this.byId("pageoverview");
					var oBinding = oList.getBinding("rows");
					cFilter.push(new sap.ui.model.Sorter("date", bDescending=true));
					oBinding.sort(cFilter);}
				else {
				var cFilter = [];
				var oList = this.byId("pageoverview");
				var oBinding = oList.getBinding("rows");
				cFilter.push(new sap.ui.model.Sorter("date", bDescending=false));
				oBinding.sort(cFilter);
					
				}
				this.j = this.j+1
				//new sap.ui.model.Filter("title", sap.ui.model.FilterOperator.Contains, sQuery)
				
			},
			//when click button at first time, show table content in descending sort of alphabet based on "title"
			//the second click show in ascending sort 
			sortByTitle: function(oEvent){
				if (this.q % 2 == 1){
					var cFilter = [];
					var oList = this.byId("pageoverview");
					var oBinding = oList.getBinding("rows");
					cFilter.push(new sap.ui.model.Sorter("title", bDescending=true));
					oBinding.sort(cFilter);}
				else {
				var cFilter = [];
				var oList = this.byId("pageoverview");
				var oBinding = oList.getBinding("rows");
				cFilter.push(new sap.ui.model.Sorter("title", bDescending=false));
				oBinding.sort(cFilter);
					
				}
				this.q = this.q+1
				//new sap.ui.model.Filter("title", sap.ui.model.FilterOperator.Contains, sQuery)
				
			}
			

});