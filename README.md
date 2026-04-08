# 🔗 CertChain PRO

**Blockchain-based certificate verification** — tamper-proof credential issuance and validation using Ethereum smart contracts, IPFS decentralized storage, and RSA cryptographic signatures.

![Python](https://img.shields.io/badge/Python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white)
![Ethereum](https://img.shields.io/badge/Ethereum-Sepolia-627EEA?style=flat-square&logo=ethereum&logoColor=white)
![IPFS](https://img.shields.io/badge/Storage-IPFS-65C2CB?style=flat-square&logo=ipfs&logoColor=white)
![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white)

---

## ✨ Features

| Feature | Description |
|---|---|
| 🔐 SHA-256 Hashing | Every certificate gets a unique cryptographic fingerprint — any tampering is instantly detectable |
| ⛓️ On-chain Verification | Hashes stored permanently on Ethereum via a Solidity smart contract |
| 🌐 IPFS Storage | Full certificate data lives on IPFS — decentralized and censorship-resistant |
| ✍️ RSA-2048 Signatures | Issuer identity cryptographically bound to every credential |
| ⚡ Real-time Validation | Dual-check pipeline verifies both the digital signature and on-chain record |

---

## 🏗️ System Architecture

```
User → Streamlit UI → SHA-256 → RSA Sign → IPFS → Ethereum → Verification
```

---

## 🛠️ Prerequisites

- Python 3.8+
- [IPFS Desktop or CLI](https://docs.ipfs.tech/install/)
- [MetaMask](https://metamask.io/) browser extension
- [Infura](https://infura.io/) account (for Sepolia RPC)
- [Remix IDE](https://remix.ethereum.org/) (for contract deployment)

---

## ⚙️ Setup

### 1 — Install dependencies

```bash
pip install streamlit web3 cryptography requests
```

### 2 — Start the IPFS daemon

```bash
ipfs init
ipfs daemon
```

The app connects to IPFS at `http://127.0.0.1:5001`.

### 3 — Set up MetaMask

1. Install the extension and create a wallet
2. Switch to **Sepolia Testnet**
3. Get free test ETH from a [Sepolia faucet](https://sepoliafaucet.com/)

### 4 — Deploy the smart contract

1. Open [Remix IDE](https://remix.ethereum.org/)
2. Create a new Solidity file and paste the `CertChain.sol` code below
3. Compile with Solidity `^0.8.0`
4. Under *Deploy & Run*, select **Injected Provider – MetaMask**
5. Deploy and copy the **Contract Address** and **ABI**

### 5 — Configure `app.py`

```python
INFURA_URL       = "https://sepolia.infura.io/v3/YOUR_INFURA_KEY"
CONTRACT_ADDRESS = "YOUR_CONTRACT_ADDRESS"
ABI              = [ ... ]  # paste from Remix compilation details
```

### 6 — Run

```bash
streamlit run app.py
```

---

## 🔍 How It Works

**Issuing a certificate**
1. User submits name, registration number, course, and institution
2. Data serialized to canonical JSON and hashed with SHA-256
3. RSA-2048 signature applied with the session private key
4. Full certificate record pushed to IPFS
5. Hash stored on Ethereum via `storeCertificate()`

**Verifying a certificate**
1. User pastes the certificate hash
2. Local record retrieved and RSA signature verified
3. `verifyCertificate()` called on-chain
4. Both checks must pass → **✅ VALID** — either failing → **❌ INVALID**

---

## 📄 Smart Contract — `CertChain.sol`

```solidity
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
```

| Function | Type | Description |
|---|---|---|
| `storeCertificate(hash)` | `nonpayable` | Stores hash and emits event with issuer address |
| `verifyCertificate(hash)` | `view` | Returns `true` if hash exists — no gas cost |

---

## 📦 Tech Stack

`Streamlit` · `Python 3.8+` · `Ethereum Sepolia` · `Web3.py` · `IPFS` · `SHA-256` · `RSA-2048` · `Solidity ^0.8.0` · `Remix IDE` · `Infura`

---

## 🎯 Use Cases

- 🎓 Academic certificates — degrees, diplomas, transcripts
- 🏢 Professional credentials — licences, certifications, badges
- 🏛️ Government records — identity documents, permits, attestations
- 🌐 Digital credentials — Web3 achievements, course completions

---

## ⚠️ Important Notes

> - IPFS daemon **must be running** before issuing certificates
> - Always use **Sepolia testnet** to avoid real gas costs
> - An active internet connection is required to reach Infura and the Ethereum network

---

## 🚀 Future Enhancements

- [ ] NFT-based certificates (ERC-721)
- [ ] MetaMask wallet authentication
- [ ] Multi-institution issuer support
- [ ] Role-based access control
- [ ] QR code verification flow
- [ ] Certificate revocation mechanism

---

## 👨‍💻 Author

Developed as an open-source blockchain solution for tamper-proof credential verification.
