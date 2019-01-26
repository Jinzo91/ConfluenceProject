sap.ui.define([
	"sap/ui/core/UIComponent",
	"sap/ui/model/json/JSONModel",
	"sap/ui/Device"
], function (UIComponent, JSONModel, Device) {
	"use strict";

	return UIComponent.extend("webApp.Component", {

		metadata: {
			manifest: "json"
		},

		init: function () {
			// call the init function of the parent
			UIComponent.prototype.init.apply(this, arguments);
			var oModel = new sap.ui.model.odata.ODataModel("https://jsonplaceholder.typicode.com/todos/1", false);
			this.setModel(oModel);

			// set device model
			var oDeviceModel = new JSONModel(Device);
			oDeviceModel.setDefaultBindingMode("OneWay");
			this.setModel(oDeviceModel, "device");

			// set dialog
			//this._helloDialog = new HelloDialog(this.getRootControl());

			// create the views based on the url/hash
			this.getRouter().initialize();

		},

//		exit : function () {
//			this._helloDialog.destroy();
//			delete this._helloDialog;
//		},
//
//		openHelloDialog : function () {
//			this._helloDialog.open();
//		},

		getContentDensityClass : function () {
			if (!this._sContentDensityClass) {
				if (!Device.support.touch) {
					this._sContentDensityClass = "sapUiSizeCompact";
				} else {
					this._sContentDensityClass = "sapUiSizeCozy";
				}
			}
			return this._sContentDensityClass;
		}

	});

});