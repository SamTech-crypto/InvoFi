const SupplyChainToken = artifacts.require("SupplyChainToken");

contract("SupplyChainToken", accounts => {
  it("should mint initial tokens", async () => {
    const token = await SupplyChainToken.deployed();
    const balance = await token.balanceOf(accounts[0]);
    assert.equal(balance.toString(), "1000000000000000000000000", "Incorrect initial balance");
  });
});