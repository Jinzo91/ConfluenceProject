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
			var url = sap.ui.getCore().byId(this.createId("url")).getValue();
			
			if(url == "" || url == null){
				sap.m.MessageToast.show("Please enter your url");
			} else if(username == "" || username == null) {
				sap.m.MessageToast.show("Please enter your username");
			} else if(password == "" || password == null) {
				sap.m.MessageToast.show("Please enter your password");
			}  else{
			this.myModel.setData(username);
			this.myModel.setData(password);
			this.myModel.setData(url);
			sap.ui.getCore().setModel(this.myModel);
			var oRouter = sap.ui.core.routing.Router.getRouter("appRouter");}
//			console.log(username);
//			console.log(password);
			//
//			oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
//			oHashChanger.setHash(oRouter.getURL("PageOverview"));
//			console.log(oRouter.getURL("PageOverview"));
//			
			
			
			 $.ajax({
				  type : "GET", //should be POST
				  url : "http://localhost:5000/users",
				  //dataType : "json",
				  async : false,
				  //data : '{"name": "' + username + '", "password" : "' + password + '"}',
				  data: $.param({username, password,url}),
				  success: function (data) {
					  
					  var oModel = new sap.ui.model.json.JSONModel("http://127.0.0.1:5000/confluencedata");
					  sap.ui.getCore().setModel(oModel);
					  
					  oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
					  oHashChanger.setHash(oRouter.getURL("PageOverview"));
					  console.log(oRouter.getURL("PageOverview"));
//				  if(username == value.user_name && password == value.user_name) {
//				  var MP = new sap.ui.view({viewName:"test.Menu",type:sap.ui.core.mvc.ViewType.XML});
//				  var DP = new sap.ui.view({viewName:"test.Dashboard",type:sap.ui.core.mvc.ViewType.XML});
//				  var split_container = new sap.m.SplitContainer({
//				  masterPages: MP,
//				  detailPages: DP
//				  });
//				  app.addPage(split_container);
//				  app.to(split_container);
//				  }

				  }

				  });
			
		},

});