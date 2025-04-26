require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

module.exports = {
  solidity: "0.8.9",
  networks: {
    hardhat: {},
    goerli: {
      url: process.env.WEB3_PROVIDER_URL,
      accounts: [process.env.PRIVATE_KEY]
    }
  }
};