// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract CertChain {

    mapping(string => bool) private certificates;

    event CertificateStored(string hash, address issuer);

    function storeCertificate(string memory hash) public {
        certificates[hash] = true;
        emit CertificateStored(hash, msg.sender);
    }

    function verifyCertificate(string memory hash) public view returns (bool) {
        return certificates[hash];
    }
}
