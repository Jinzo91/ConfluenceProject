sap.ui.controller("webApp.controller.PageDetail",{
		//set Model for view, and the data is from global model "dataModel" to local model "detailModel"  
		onInit: function () {
			this.detailModel = new sap.ui.model.json.JSONModel();
			this.detailModel = sap.ui.getCore().getModel(this.dataModel);
			this.getView().setModel(this.detailModel);
			this.setTagModel = new sap.ui.model.json.JSONModel();
			this.getags = {};
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
			console.log(this.detailModel);
			var docId = this.detailModel.oData.id
			//var that = this;
			console.log('Model from Detail: ', docId);
			$.ajax({
				  type : "POST", 
				  url : "http://localhost:5000/api/confluencedata/tag",
				  async : false,
				  data: $.param({docId}),
				  success: function (data) {
					  this.getags = data;
					  console.log(this.getags);
					  this.detailModel = sap.ui.getCore().getModel();
					  //this.detailModel.setData({tags: this.getags});
					  this.detailModel.setProperty("/newtags", this.getags.tags);
					  //console.log(this.detailModel);
					  //that.getView().setModel().setProperty("/recipient/newtags", this.getags);
				  },
				 error: function (oError){
					  sap.m.MessageToast.show("Something went wrong with tag generation!");
				  }
			  });
		},
		acceptTags: function() {
			var originalTags = this.detailModel.getProperty("/tags");
			var newTags = this.detailModel.getProperty("/newtags");
			var docId = this.detailModel.oData.id
			$.ajax({
				  type : "POST", 
				  url : "http://localhost:5000/api/confluencedata/save/tag",
				  async : false,
				  data: $.param({docId, originalTags, newTags}),
				  success: function (data) {
					  this.getags = data;
					  var updatedTags = this.getags.tags
					  console.log("new tags", this.getags);
					  this.detailModel = sap.ui.getCore().getModel();
					  this.detailModel.setProperty("/tags", updatedTags);
					  //console.log(this.detailModel);
					  sap.m.MessageToast.show("Tags saved to database and uploaded to Confluence!");
				  },
				 error: function (oError){
					  sap.m.MessageToast.show("Something went wrong with saving the tags!");
				  }
			  });
		},
		rejectTags: function() {
			this.getags={};
			this.detailModel = sap.ui.getCore().getModel();
			this.detailModel.setProperty("/newtags", this.getags.tags);
			sap.m.MessageToast.show("The tags will not be saved.");
		},

});