// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract Invoice {
    address public issuer;
    uint256 public amount;
    uint256 public dueDate;
    bool public financed;
    address public financier;

    constructor(address _issuer, uint256 _amount, uint256 _dueDate) {
        issuer = _issuer;
        amount = _amount;
        dueDate = _dueDate;
        financed = false;
    }

    function finance(address _financier) public {
        require(!financed, "Invoice already financed");
        financed = true;
        financier = _financier;
    }
}