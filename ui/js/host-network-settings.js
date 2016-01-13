/*
 * Copyright IBM Corp, 2015
 *
 * This library is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * This library is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * You should have received a copy of the GNU Lesser General Public
 * License along with this library; if not, write to the Free Software
 * Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA
 */

ginger.initNwInterfaceSettings = function() {

  nwApplyButton = $('#nw-interface-settings-button-apply');

  nwGeneralForm = $('#form-nw-settings-general');
  nwIpv4Form = $('#form-nw-settings-ipv4');
  nwIpv6Form = $('#form-nw-settings-ipv6');
  nwAdvanceForm = $('#form-nw-settings-advance');
  subchannelForm = $('#form-group-subchannels');

  interfaceSettingTabs = $('#nw-settings-tabs');
  nwTitle = $('#nw-settings-title');
  hiddenDeviceTextbox = $('#interface-device', interfaceSettingTabs);
  nwDeviceTextbox = $('#nw-settings-device-textbox', interfaceSettingTabs);
  nwTypeTextbox = $('#nw-settings-type-textbox', interfaceSettingTabs);
  nwHwaddressTextbox = $('#nw-settings-hwaddress-textbox', interfaceSettingTabs);
  nwSubchTextbox = $('#nw-settings-subchannels-textbox', interfaceSettingTabs);
  onBootCheckbox = $('#nw-settings-connect-auto', interfaceSettingTabs);
  mtuTextbox = $('#nw-settings-mtu-textbox', interfaceSettingTabs);
  zoneSelect = $('#nw-settings-firewall-select', interfaceSettingTabs);
  ipv4MethodSelect = $('#nw-settings-ipv4-method', interfaceSettingTabs);
  ipv6GatewayTextbox = $('#nw-settings-ipv6-gateway-textbox', interfaceSettingTabs);
  ipv6MethodSelect = $('#nw-settings-ipv6-method', interfaceSettingTabs);

  ipv4AddressAddButton = $('#nw-settings-ipv4-add', interfaceSettingTabs);
  ipv4DnsAddButton = $('#nw-settings-ipv4-dns-add', interfaceSettingTabs);
  ipv4RoutesAddButton = $('#nw-settings-ipv4-routes-add', interfaceSettingTabs);

  ipv6AddressAddButton = $('#nw-settings-ipv6-add', interfaceSettingTabs);
  ipv6DnsAddButton = $('#nw-settings-ipv6-dns-add', interfaceSettingTabs);
  ipv6RoutesAddButton = $('#nw-settings-ipv6-routes-add', interfaceSettingTabs);

  selectedInterface = ginger.selectedInterface;

  hiddenDeviceTextbox.val(selectedInterface);

  // Get the interface setting details
  ginger.retrieveCfgInterface(selectedInterface, function suc(result) {
    ginger.populateNwSettingsGeneralTab(result); //populate general tab
    ginger.populateNwSettingsAdvanceTab(result); //populate advance tab
    ginger.populateNwSettingsIpv4SettingsTab(result); //populate ipv4 setting tab
    ginger.populateNwSettingsIpv6SettingsTab(result); //populate ipv6 setting tab
  }, function(result) {
    if (result['responseJSON']) {
      var errText = result['responseJSON']['reason'];
    }
    result && wok.message.error(errText, '#message-nw-container-area', true);
    wok.window.close();
  });

  ginger.action_apply_nwsettings();
};

ginger.action_apply_nwsettings = function() {

  // on Apply button click
  nwApplyButton.on('click', function() {
    var data = {};

    nwApplyButton.prop('disabled', true);
    var interfaceDevice = nwDeviceTextbox.val();

    var getNwSettingsBasicInfoData = function() {
      var basic_info = {};
      var general_form_data = nwGeneralForm.serializeObject();
      general_form_data['DEVICE'] = interfaceDevice;
      var adv_form_data = nwAdvanceForm.serializeObject();

      if (onBootCheckbox.is(":checked")) {
        general_form_data["ONBOOT"] = "yes";
      } else {
        general_form_data["ONBOOT"] = "no";
      }
      data['BASIC_INFO'] = $.extend(general_form_data, adv_form_data);
    }
    getNwSettingsBasicInfoData();

    var getNwSettingsIpv4InfoData = function() {
      var ipv4_info = {}; //All ipv4 info from ipv4 tab

      if ($('.ipv4-on-off').bootstrapSwitch('state')) {
        ipv4_info['IPV4INIT'] = 'yes';

        var method = ipv4MethodSelect.val();
        if (method == i18n['GINNWS0010M']) {
          ipv4_info['BOOTPROTO'] = 'dhcp';
        } else if (method == i18n['GINNWS0003M']) {
          ipv4_info['BOOTPROTO'] = 'none';
        }

        var opts = {};

        //Get IP address grid data
        opts['id'] = 'nw-settings-ipv4-addresses';
        opts['gridId'] = "nw-settings-ipv4-addresses-grid";
        ipv4Addresses = ginger.getCurrentRows(opts);

        //Get DNS grid data
        opts['id'] = 'nw-settings-ipv4-dns';
        opts['gridId'] = "nw-settings-ipv4-dns-grid";
        ipv4Dns = ginger.getCurrentRows(opts);

        //Get Routes grid data
        opts['id'] = 'nw-settings-ipv4-routes';
        opts['gridId'] = "nw-settings-ipv4-routes-grid";
        ipv4Routes = ginger.getCurrentRows(opts);

        if (method != i18n['GINNWS0010M'] && ipv4Addresses.length > 0) {
          ipv4_info['IPV4Addresses'] = ipv4Addresses;
          if (ipv4Dns.length > 0) {
            dns = []
            for (var i = 0; i < ipv4Dns.length; i++) {
              dnsValue = ipv4Dns[i].DNS;
              dns.push(dnsValue);
            }
            ipv4_info['DNSAddresses'] = dns;
          }

          if (ipv4Routes.length > 0) {
            ipv4_info['ROUTES'] = ipv4Routes;
          }
        }
      } else {
        ipv4_info['IPV4INIT'] = 'no';
      }

      data['IPV4_INFO'] = ipv4_info
    }
    getNwSettingsIpv4InfoData();

    var getNwSettingsIpv6InfoData = function() {
      var ipv6_info = {}; //All ipv6 info from ipv6 tab

      if ($('.ipv6-on-off').bootstrapSwitch('state')) {
        ipv6_info['IPV6INIT'] = 'yes';

        var method = ipv6MethodSelect.val();
        if (method == i18n['GINNWS0002M']) {
          ipv6_info['IPV6_AUTOCONF'] = 'yes';
        } else if (method == i18n['GINNWS0003M']) {
          ipv6_info['IPV6_AUTOCONF'] = 'no';
        }

        var opts = {};

        //Get IP address grid data
        opts['id'] = 'nw-settings-ipv6-addresses';
        opts['gridId'] = "nw-settings-ipv6-addresses-grid";
        ipv6Addresses = ginger.getCurrentRows(opts);

        //Get DNS grid data
        opts['id'] = 'nw-settings-ipv6-dns';
        opts['gridId'] = "nw-settings-ipv6-dns-grid";
        ipv6Dns = ginger.getCurrentRows(opts);

        //Get Routes grid data
        opts['id'] = 'nw-settings-ipv6-routes';
        opts['gridId'] = "nw-settings-ipv6-routes-grid";
        ipv6Routes = ginger.getCurrentRows(opts);

        if (method != i18n['GINNWS0002M'] && ipv6Addresses.length > 0) {
          ipv6_info['IPV6Addresses'] = ipv6Addresses;
          var nwIpv6FormData = nwIpv6Form.serializeObject();
          ipv6_info["IPV6_DEFAULTGW"] = nwIpv6FormData["GATEWAY"];

          if (ipv6Dns.length > 0) {
            var dns = []
            for (var i = 0; i < ipv6Dns.length; i++) {
              dnsValue = ipv6Dns[i].DNS;
              dns.push(dnsValue);
            }
            ipv6_info['DNSAddresses'] = dns;
          }

          if (ipv6Routes.length > 0) {
            ipv6_info['ROUTES'] = ipv6Routes;
          }
        }
      } else {
        ipv6_info['IPV6INIT'] = 'no';
      }

      data['IPV6_INFO'] = ipv6_info
    }
    getNwSettingsIpv6InfoData();

    ginger.updateCfgInterface(interfaceDevice, data, function() {
      wok.message.success(i18n['GINNWS0001M'] + interfaceDevice, '#alert-nw-settings-modal-container');
      $(nwApplyButton).prop('disabled', false);
    }, function(err) {
      wok.message.error(err.responseJSON.reason, '#alert-nw-settings-modal-container', true);
      $(nwApplyButton).prop('disabled', false);
    });
  });
}

// function to populate general tab
ginger.populateNwSettingsGeneralTab = function(interface) {
  nwTitle.append(interface.BASIC_INFO.DEVICE);
  nwDeviceTextbox.val(interface.BASIC_INFO.DEVICE);
  nwTypeTextbox.val(interface.BASIC_INFO.TYPE);
  nwHwaddressTextbox.val(interface.BASIC_INFO.HWADDR);
  if ("SUBCHANNEL" in (interface.BASIC_INFO)) {
    nwSubchTextbox.val(interface.BASIC_INFO.SUBCHANNEL);
    subchannelForm.removeClass("hidden");
  }
  if (interface.BASIC_INFO.ONBOOT == "\"yes\"" || interface.BASIC_INFO.ONBOOT == "yes") {
    onBootCheckbox.prop('checked', true);
  }
};

// function to populate advance tab
ginger.populateNwSettingsAdvanceTab = function(interface) {
  if ("MTU" in (interface.BASIC_INFO)) {
    mtuTextbox.val(interface.BASIC_INFO.MTU);
  }

  mtuTextbox.on('keyup', function() {
    // Validate MTU value, It should be i> 1500
    var mtu = mtuTextbox.val();
    $(this).toggleClass("invalid-field", !((ginger.isInteger(mtu) && mtu >= 1500)));
  });

  if ("ZONE" in (interface.BASIC_INFO)) {
    zoneSelect.append($("<option></option>")
      .attr("value", interface.BASIC_INFO.ZONE)
      .text(interface.BASIC_INFO.ZONE));
  }
};

// function to ipv4 Settings tab
ginger.populateNwSettingsIpv4SettingsTab = function(interface) {
  ginger.createNwSettingsIpv4AddressGrid(interface);
  ginger.createNwSettingsIpv4DnsGrid(interface);
  ginger.createNwSettingsIpv4RouteGrid(interface);

  if ("IPV4_INFO" in interface && "IPV4INIT" in (interface.IPV4_INFO)) {
    if (interface.IPV4_INFO.IPV4INIT == "yes" || interface.IPV4_INFO.IPV4INIT == "\"yes\"") {
      $('.ipv4-on-off').bootstrapSwitch('state', true);
      ginger.enableclass('form-nw-settings-ipv4-method');
    } else {
      $('.ipv4-on-off').bootstrapSwitch('state', false);
      ginger.disableclass('form-nw-settings-ipv4-method');
    }
  } else {
    $('.ipv4-on-off').bootstrapSwitch('state', false);
    ginger.disableclass('form-nw-settings-ipv4-method');
  }

  $('.ipv4-on-off').on('switchChange.bootstrapSwitch', function(event, state) {
    if (state) {
      ginger.enableclass('form-nw-settings-ipv4-method');
      changeState();
    } else {
      ginger.disableclass('form-nw-settings-ipv4-manual');
      ginger.disableclass('form-nw-settings-ipv4-method');
    }
  });

  if (interface.IPV4_INFO.BOOTPROTO && (interface.IPV4_INFO.BOOTPROTO == "None" || interface.IPV4_INFO.BOOTPROTO == "none")) {
    ipv4MethodSelect.val(i18n['GINNWS0003M']);
    ginger.enableclass('form-nw-settings-ipv4-manual');
  } else if (interface.IPV4_INFO.BOOTPROTO && (interface.IPV4_INFO.BOOTPROTO == "dhcp")) {
    ipv4MethodSelect.val(i18n['GINNWS0010M']);
    ginger.disableclass('form-nw-settings-ipv4-manual');
  }

  ipv4MethodSelect.change(function() {
    changeState();
  });

  var changeState = function() {
    if (ipv4MethodSelect.val() == i18n['GINNWS0010M']) {
      ginger.disableclass('form-nw-settings-ipv4-manual');
    } else {
      ginger.enableclass('form-nw-settings-ipv4-manual');
    }
  }

}

// function to ipv4 grid
ginger.createNwSettingsIpv4AddressGrid = function(interface) {
  var gridFields = [];
  var opts = [];
  opts['noResults'] = " ";

  opts['id'] = 'nw-settings-ipv4-addresses';
  opts['gridId'] = "nw-settings-ipv4-addresses-grid";
  opts['selection'] = false;
  opts['navigation'] = 0;

  gridFields = [{
    "column-id": 'IPADDR',
    "type": 'string',
    "width": "20%",
    "title": i18n['GINNWS0004M'],
    "identifier": true,
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "editable-nw-ipv4-addresses"
  }, {
    "column-id": 'PREFIX',
    "type": 'string',
    "width": "30%",
    "title": i18n['GINNWS0005M'],
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "editable-nw-ipv4-addresses"
  }, {
    "column-id": 'GATEWAY',
    "type": 'string',
    "width": "30%",
    "title": i18n['GINNWS0008M'],
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "editable-nw-ipv4-addresses"
  }, {
    "column-id": "IPADDR",
    "type": 'string',
    "title": " ",
    "width": "20%",
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "row-edit-delete"
  }];

  opts['gridFields'] = JSON.stringify(gridFields);
  var ipv4AddressesGrid = ginger.createBootgrid(opts);

  if ("IPV4_INFO" in interface && "IPV4Addresses" in (interface.IPV4_INFO)) {
    ginger.loadBootgridData(opts['gridId'], interface.IPV4_INFO.IPV4Addresses);
  }
  ginger.createEditableBootgrid(ipv4AddressesGrid, opts, 'IPADDR');

  ipv4AddressAddButton.on('click', function() {
    var columnSettings = [{
      'id': 'IPADDR',
      'width': '20%',
      'validation': function() {
        var isValid = ginger.validateIp($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'PREFIX',
      'width': '30%',
      'validation': function() {
        var isValid = ginger.validateMask($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'GATEWAY',
      'width': '30%',
      'validation': function() {
        var isValid = ginger.validateIp($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }]
    commandSettings = {
      "width": "20%",
      "td-class": "text-center"
    }
    ginger.addNewRecord(columnSettings, opts['gridId'], commandSettings);
  });

};

ginger.createNwSettingsIpv4DnsGrid = function(interface) {
  var gridFields = [];
  var opts = [];

  opts['id'] = 'nw-settings-ipv4-dns';
  opts['gridId'] = "nw-settings-ipv4-dns-grid";
  opts['noResults'] = " ";
  opts['selection'] = false;
  opts['navigation'] = 0;

  gridFields = [{
    "column-id": 'DNS',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "80%",
    "title": i18n['GINNWS0006M'],
    "identifier": true,
    "formatter": "editable-nw-ipv4-dns"
  }, {
    "column-id": "DNS",
    "type": 'string',
    "title": "",
    "width": "20%",
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "row-edit-delete"
  }];

  opts['gridFields'] = JSON.stringify(gridFields);
  var dnsGrid = ginger.createBootgrid(opts);

  if ("IPV4_INFO" in interface && "DNSAddresses" in (interface.IPV4_INFO)) {
    var DNSAddresses = interface.IPV4_INFO.DNSAddresses

    for (var i = 0; i < DNSAddresses.length; i++) {
      DNSAddresses[i] = {
          "DNS": DNSAddresses[i]
        } // convert from List to Map
    }

    ginger.loadBootgridData(opts['gridId'], DNSAddresses);
  }
  ginger.createEditableBootgrid(dnsGrid, opts, 'DNS');

  ipv4DnsAddButton.on('click', function() {
    var columnSettings = [{
      'id': 'DNS',
      'width': '80%',
      'validation': function() {
        var isValid = ginger.validateIp($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }]
    commandSettings = {
      "width": "20%",
      "td-class": "text-center"
    }
    ginger.addNewRecord(columnSettings, opts['gridId'], commandSettings);
  });

};

ginger.createNwSettingsIpv4RouteGrid = function(interface) {
  var gridFields = [];
  var opts = [];
  opts['noResults'] = " ";

  opts['id'] = 'nw-settings-ipv4-routes';
  opts['gridId'] = "nw-settings-ipv4-routes-grid";
  opts['selection'] = false;
  opts['navigation'] = 0;

  gridFields = [{
    "column-id": 'ADDRESS',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0004M'],
    "identifier": true,
    "formatter": "editable-nw-ipv4-routes"
  }, {
    "column-id": 'NETMASK',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "title": i18n['GINNWS0007M'],
    "width": "20%",
    "formatter": "editable-nw-ipv4-routes"
  }, {
    "column-id": 'GATEWAY',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0008M'],

    "formatter": "editable-nw-ipv4-routes"
  }, {
    "column-id": 'METRIC',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0009M'],
    "formatter": "editable-nw-ipv4-routes"
  }, {
    "column-id": "ADDRESS",
    "type": 'string',
    "title": "",
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "formatter": "row-edit-delete"
  }];

  opts['gridFields'] = JSON.stringify(gridFields);
  var routesGrid = ginger.createBootgrid(opts);

  if ("IPV4_INFO" in interface && "ROUTES" in (interface.IPV4_INFO)) {
    ginger.loadBootgridData(opts['gridId'], interface.IPV4_INFO.ROUTES);
  }
  ginger.createEditableBootgrid(routesGrid, opts, 'ADDRESS');

  ipv4RoutesAddButton.on('click', function() {
    var columnSettings = [{
      'id': 'ADDRESS',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.validateIp($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'NETMASK',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.validateMask($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'GATEWAY',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.validateIp($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'METRIC',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = /^[0-9]+$/.test($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }]
    commandSettings = {
      "width": "20%",
      "td-class": "text-center"
    }
    ginger.addNewRecord(columnSettings, opts['gridId'], commandSettings);
  });
};

// function to ipv4 Settings tab
ginger.populateNwSettingsIpv6SettingsTab = function(interface) {
  ginger.createNwSettingsIpv6AddressGrid(interface);
  ginger.createNwSettingsIpv6DnsGrid(interface);
  ginger.createNwSettingsIpv6RouteGrid(interface);

  if ("IPV6_INFO" in interface && "IPV6INIT" in (interface.IPV6_INFO)) {
    if (interface.IPV6_INFO.IPV6INIT == "yes" || interface.IPV6_INFO.IPV6INIT == "\"yes\"") {
      $('.ipv6-on-off').bootstrapSwitch('state', true);
      ginger.enableclass('form-nw-settings-ipv6-manual');
      ginger.enableclass('form-nw-settings-ipv6-method');
    } else {
      $('.ipv6-on-off').bootstrapSwitch('state', false);
      ginger.disableclass('form-nw-settings-ipv6-manual');
      ginger.disableclass('form-nw-settings-ipv6-method');
    }
  } else {
    $('.ipv6-on-off').bootstrapSwitch('state', false);
    ginger.disableclass('form-nw-settings-ipv6-manual');
    ginger.disableclass('form-nw-settings-ipv6-method');
  }

  $('.ipv6-on-off').on('switchChange.bootstrapSwitch', function(event, state) {
    if (state) {
      ginger.enableclass('form-nw-settings-ipv6-method');
      changeState();
    } else {
      ginger.disableclass('form-nw-settings-ipv6-manual');
      ginger.disableclass('form-nw-settings-ipv6-method');
    }
  });

  if (interface.IPV6_INFO.IPV6_AUTOCONF && (interface.IPV6_INFO.IPV6_AUTOCONF == "yes" || interface.IPV6_INFO.IPV6_AUTOCONF == "Yes")) {
    ipv6MethodSelect.val(i18n['GINNWS0002M']);
    ginger.disableclass('form-nw-settings-ipv6-manual');
  } else if (interface.IPV6_INFO.IPV6_AUTOCONF && (interface.IPV6_INFO.IPV6_AUTOCONF == "no" || interface.IPV6_INFO.IPV6_AUTOCONF == "No")) {
    ipv6MethodSelect.val(i18n['GINNWS0003M']);
    ginger.enableclass('form-nw-settings-ipv6-manual');
  }

  ipv6MethodSelect.change(function() {
    changeState();
  });

  var changeState = function() {
    if (ipv6MethodSelect.val() == i18n['GINNWS0002M']) {
      ginger.disableclass('form-nw-settings-ipv6-manual');
    } else {
      ginger.enableclass('form-nw-settings-ipv6-manual');
    }
  }

  if (interface.IPV6_INFO.IPV6_DEFAULTGW) {
    ipv6GatewayTextbox.val(interface.IPV6_INFO.IPV6_DEFAULTGW);
  }

  ipv6GatewayTextbox.on('keyup', function() {
    var ipv6_defaultgw = ipv6GatewayTextbox.val();
    $(this).toggleClass("invalid-field", !(ginger.isValidIPv6(ipv6_defaultgw)));
  });
}

// function to ipv6 grid
ginger.createNwSettingsIpv6AddressGrid = function(interface) {
  var gridFields = [];
  var opts = [];

  opts['id'] = 'nw-settings-ipv6-addresses';
  opts['gridId'] = "nw-settings-ipv6-addresses-grid";
  opts['noResults'] = " ";
  opts['selection'] = false;
  opts['navigation'] = 0;

  gridFields = [{
    "column-id": 'IPADDR',
    "type": 'string',
    "width": "20%",
    "title": i18n['GINNWS0004M'],
    "identifier": true,
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "editable-nw-ipv6-addresses"
  }, {
    "column-id": 'PREFIX',
    "type": 'string',
    "width": "30%",
    "title": i18n['GINNWS0005M'],
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "editable-nw-ipv6-addresses"
  }, {
    "column-id": "IPADDR",
    "type": 'string',
    "title": " ",
    "width": "20%",
    "header-class": "text-center",
    "data-class": "center",
    "formatter": "row-edit-delete"
  }];

  opts['gridFields'] = JSON.stringify(gridFields);
  var ipv6AddressesGrid = ginger.createBootgrid(opts);

  if ("IPV6_INFO" in interface && "IPV6Addresses" in (interface.IPV6_INFO)) {
    ginger.loadBootgridData(opts['gridId'], interface.IPV6_INFO.IPV6Addresses);
  }
  ginger.createEditableBootgrid(ipv6AddressesGrid, opts, 'IPADDR');

  ipv6AddressAddButton.on('click', function() {
    var columnSettings = [{
      'id': 'IPADDR',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.isValidIPv6($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'PREFIX',
      'width': '30%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.isValidIPv6($(this).val()) || ginger.isValidIPv6Prefix($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }];
    commandSettings = {
      "width": "20%",
      "td-class": "text-center"
    }
    ginger.addNewRecord(columnSettings, opts['gridId'], commandSettings);
  });
};

ginger.createNwSettingsIpv6DnsGrid = function(interface) {
  var gridFields = [];
  var opts = [];

  opts['id'] = 'nw-settings-ipv6-dns';
  opts['gridId'] = "nw-settings-ipv6-dns-grid";
  opts['noResults'] = " ";
  opts['selection'] = false;
  opts['navigation'] = 0;

  gridFields = [{
    "column-id": 'DNS',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "80%",
    "title": i18n['GINNWS0006M'],
    "identifier": true,
    "formatter": "editable-nw-ipv6-dns"
  }, {
    "column-id": "DNS",
    "type": 'string',
    "title": "",
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "formatter": "row-edit-delete"
  }];

  opts['gridFields'] = JSON.stringify(gridFields);
  var dnsGrid = ginger.createBootgrid(opts);

  if ("IPV6_INFO" in interface && "DNSAddresses" in (interface.IPV6_INFO)) {
    var DNSAddresses = interface.IPV6_INFO.DNSAddresses
    var dns = {}
    for (var i = 0; i < DNSAddresses.length; i++) {
      DNSAddresses[i] = {
        "DNS": DNSAddresses[i]
      };
    }
    ginger.loadBootgridData(opts['gridId'], dns);
  }
  ginger.createEditableBootgrid(dnsGrid, opts, 'DNS');
  ipv6DnsAddButton.on('click', function() {
    var columnSettings = [{
      'id': 'DNS',
      'width': '80%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.isValidIPv6($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }]
    commandSettings = {
      "width": "20%",
      "td-class": "text-center"
    }
    ginger.addNewRecord(columnSettings, opts['gridId'], commandSettings);
  });
};

ginger.createNwSettingsIpv6RouteGrid = function(interface) {
  var gridFields = [];
  var opts = [];
  opts['noResults'] = " ";

  opts['id'] = 'nw-settings-ipv6-routes';
  opts['gridId'] = "nw-settings-ipv6-routes-grid";
  opts['selection'] = false;
  opts['navigation'] = 0;

  gridFields = [{
    "column-id": 'ADDRESS',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0004M'],
    "identifier": true,
    "formatter": "editable-nw-ipv6-routes"
  }, {
    "column-id": 'NETMASK',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0007M'],
    "formatter": "editable-nw-ipv6-routes"
  }, {
    "column-id": 'GATEWAY',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0008M'],
    "formatter": "editable-nw-ipv6-routes"
  }, {
    "column-id": 'METRIC',
    "type": 'string',
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "title": i18n['GINNWS0009M'],
    "formatter": "editable-nw-ipv6-routes"
  }, {
    "column-id": "ADDRESS",
    "type": 'string',
    "title": "",
    "header-class": "text-center",
    "data-class": "center",
    "width": "20%",
    "formatter": "row-edit-delete"
  }];

  opts['gridFields'] = JSON.stringify(gridFields);
  var routesGrid = ginger.createBootgrid(opts);

  if ("IPV6_INFO" in interface && "ROUTES" in (interface.IPV6_INFO)) {
    ginger.loadBootgridData(opts['gridId'], interface.IPV6_INFO.ROUTES);
  }
  ginger.createEditableBootgrid(routesGrid, opts, 'ADDRESS');

  ipv6RoutesAddButton.on('click', function() {
    var columnSettings = [{
      'id': 'ADDRESS',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.isValidIPv6($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'NETMASK',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.isValidIPv6($(this).val()) || ginger.isValidIPv6Prefix($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'GATEWAY',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = ginger.isValidIPv6($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }, {
      'id': 'METRIC',
      'width': '20%',
      "td-class": "text-center",
      'validation': function() {
        var isValid = /^[0-9]+$/.test($(this).val());
        ginger.markInputInvalid($(this), isValid);
      }
    }]
    commandSettings = {
      "width": "20%",
      "td-class": "text-center"
    }
    ginger.addNewRecord(columnSettings, opts['gridId'], commandSettings);
  });

};
