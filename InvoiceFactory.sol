// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "./Invoice.sol";

contract InvoiceFactory {
    address[] public invoices;
    event InvoiceCreated(address invoiceAddress, address issuer, uint256 amount);

    function createInvoice(address _issuer, uint256 _amount, uint256 _dueDate) public {
        Invoice invoice = new Invoice(_issuer, _amount, _dueDate);
        invoices.push(address(invoice));
        emit InvoiceCreated(address(invoice), _issuer, _amount);
    }

    function getInvoices() public view returns (address[] memory) {
        return invoices;
    }
}