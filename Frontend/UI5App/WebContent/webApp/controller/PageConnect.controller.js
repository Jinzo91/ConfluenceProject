
sap.ui.define([
	"sap/ui/core/mvc/Controller",
	"sap/ui/model/json/JSONModel",
	"../model/formatter",
	"sap/ui/model/Filter",
	"sap/ui/model/FilterOperator",
	"sap/ui/core/UIComponent",
	])
sap.ui.controller("webApp.controller.PageConnect",{
//	return Controller.extend("webApp.controller.PageConnect", {
//
//		formatter: formatter,

		onInit: function () {
			this.myModel = new sap.ui.model.json.JSONModel();
		},

		onPress: function (oEvent) {
			//var json = {};
			var username = sap.ui.getCore().byId(this.createId("username")).getValue();
			var password = sap.ui.getCore().byId(this.createId("password")).getValue();
			
			this.myModel.setData(username);
			this.myModel.setData(password);
			sap.ui.getCore().setModel(this.myModel);
			var oRouter = sap.ui.core.routing.Router.getRouter("appRouter");
			console.log(username);
			console.log(password);
			
			oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
			oHashChanger.setHash(oRouter.getURL("PageOverview"));
			console.log(oRouter.getURL("PageOverview"));
			
			
			
			 $.ajax({

				  type : "POST",

				  url : "http://localhost:5000/users",

				  //dataType : "json",

				  async : false,

				  //data : '{"name": "' + username + '", "password" : "' + password + '"}',
				  data: $.param({username, password}),
				  success: function (data) {

				  if(username == value.user_name && password == value.user_name) {

//				  var MP = new sap.ui.view({viewName:"test.Menu",type:sap.ui.core.mvc.ViewType.XML});
//
//				  var DP = new sap.ui.view({viewName:"test.Dashboard",type:sap.ui.core.mvc.ViewType.XML});

				  var split_container = new sap.m.SplitContainer({

				  masterPages: MP,

				  detailPages: DP

				  });

				  app.addPage(split_container);

				  app.to(split_container);

				  }

				  }

				  });
			
		},

});