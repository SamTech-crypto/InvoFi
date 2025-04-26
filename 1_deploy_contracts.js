const InvoiceFactory = artifacts.require("InvoiceFactory");

module.exports = function (deployer) {
  deployer.deploy(InvoiceFactory);
};