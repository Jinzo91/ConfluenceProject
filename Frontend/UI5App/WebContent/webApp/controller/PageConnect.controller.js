sap.ui.controller("webApp.controller.PageConnect",{
		onInit: function () {
			this.myModel = new sap.ui.model.json.JSONModel();
		},
		onPress: function (oEvent) {
			//hand the event when users click button with id "connect"
			
			//get value from PageConnect.view.xml
			var username = sap.ui.getCore().byId(this.createId("username")).getValue();
			var password = sap.ui.getCore().byId(this.createId("password")).getValue();
			var url = sap.ui.getCore().byId(this.createId("url")).getValue();
			var space = sap.ui.getCore().byId(this.createId("space")).getValue();
			//when submit, wether the information is empty
			if(url == "" || url == null){
				sap.m.MessageToast.show("Please enter your url");
			} else if(username == "" || username == null) {
				sap.m.MessageToast.show("Please enter your username");
			} else if(password == "" || password == null) {
				sap.m.MessageToast.show("Please enter your password");
			} else{
			//bind data to myModel and make myModel global
			this.myModel.setData({"username": username});
//			this.myModel.setData(password);
//			this.myModel.setData(url);
			sap.ui.getCore().setModel(this.myModel);
			console.log(this.myModel);
			var oRouter = sap.ui.core.routing.Router.getRouter("appRouter");
			}

			
			//sent the connection data to back end,and wait for response of success or error
			//if backend returns success then jumpt to page overview, and back end will download data
			//if back end returns error then show an error popup for message and jump to Overview.
			 $.ajax({
				  type : "POST", 
				  url : "http://localhost:5000/api/user/login",
				  async : false,
				  data: $.param({url, space, username, password}),
				  success: function (data) {
					  
					  oHashChanger = sap.ui.core.routing.HashChanger.getInstance();
					  oHashChanger.setHash(oRouter.getURL("PageOverview"));
					  console.log(oRouter.getURL("PageOverview"));
				 

				  },
				 error: function (oError){
					  sap.m.MessageToast.show("Please enter valid information");
				  }
				  
			  });
			
		},

});