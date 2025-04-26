const InvoiceFactory = artifacts.require("InvoiceFactory");

contract("InvoiceFactory", accounts => {
  it("should create an invoice", async () => {
    const factory = await InvoiceFactory.deployed();
    await factory.createInvoice(accounts[1], 1000, 1640995200);
    const invoices = await factory.getInvoices();
    assert.equal(invoices.length, 1, "Invoice not created");
  });
});