import streamlit as st
import hashlib
import json
from datetime import datetime
from web3 import Web3
import requests
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding

# =========================
# CONFIG (EDIT THESE)
# =========================
INFURA_URL = "https://sepolia.infura.io/v3/YOUR_INFURA_KEY"
CONTRACT_ADDRESS = "YOUR_CONTRACT_ADDRESS"

ABI = [
    {
        "inputs": [{"internalType": "string","name": "hash","type": "string"}],
        "name": "storeCertificate",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function"
    },
    {
        "inputs": [{"internalType": "string","name": "hash","type": "string"}],
        "name": "verifyCertificate",
        "outputs": [{"internalType": "bool","name": "","type": "bool"}],
        "stateMutability": "view",
        "type": "function"
    }
]

IPFS_API = "http://127.0.0.1:5001/api/v0/add"

# =========================
# WEB3 SETUP
# =========================
w3 = Web3(Web3.HTTPProvider(INFURA_URL))
contract = w3.eth.contract(address=CONTRACT_ADDRESS, abi=ABI)

# =========================
# RSA KEYS
# =========================
if "private_key" not in st.session_state:
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    st.session_state.private_key = private_key
    st.session_state.public_key = public_key

# =========================
# FUNCTIONS
# =========================
def make_hash(data):
    return hashlib.sha256(data.encode()).hexdigest()

def sign_data(data):
    signature = st.session_state.private_key.sign(
        data.encode(),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )
    return signature.hex()

def verify_signature(data, signature_hex):
    try:
        st.session_state.public_key.verify(
            bytes.fromhex(signature_hex),
            data.encode(),
            padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
            hashes.SHA256()
        )
        return True
    except:
        return False

def upload_to_ipfs(data):
    files = {'file': ('cert.json', json.dumps(data))}
    res = requests.post(IPFS_API, files=files)
    return res.json()['Hash']

def save_local(cert):
    try:
        with open("chain.json", "r") as f:
            data = json.load(f)
    except:
        data = []
    data.append(cert)
    with open("chain.json", "w") as f:
        json.dump(data, f, indent=2)

def store_on_blockchain(cert_hash):
    account = w3.eth.accounts[0]  # for local ganache
    tx = contract.functions.storeCertificate(cert_hash).transact({
        'from': account
    })
    w3.eth.wait_for_transaction_receipt(tx)

def verify_on_blockchain(cert_hash):
    return contract.functions.verifyCertificate(cert_hash).call()

# =========================
# UI
# =========================
st.set_page_config(page_title="CertChain PRO", page_icon="🔗")
st.title("🔗 CertChain PRO")
st.caption("Real Blockchain Certificate Verification")

tab1, tab2 = st.tabs(["📋 Issue", "🔍 Verify"])

# =========================
# ISSUE
# =========================
with tab1:
    st.subheader("Issue Certificate")

    name = st.text_input("Name")
    reg = st.text_input("Register Number")
    course = st.text_input("Course")
    inst = st.text_input("Institution")

    if st.button("Issue Certificate"):
        if not all([name, reg, course, inst]):
            st.error("All fields required")
        else:
            cert = {
                "name": name,
                "reg": reg,
                "course": course,
                "institution": inst,
                "timestamp": str(datetime.now())
            }

            raw = json.dumps(cert, sort_keys=True)
            cert_hash = make_hash(raw)

            signature = sign_data(raw)

            cert["hash"] = cert_hash
            cert["signature"] = signature

            # Upload to IPFS
            ipfs_hash = upload_to_ipfs(cert)
            cert["ipfs"] = ipfs_hash

            # Save locally
            save_local(cert)

            # Store on blockchain
            try:
                store_on_blockchain(cert_hash)
                st.success("Stored on Blockchain ✅")
            except:
                st.warning("Blockchain connection failed")

            st.success("Certificate Issed!")
            st.write("Hash:", cert_hash)
            st.write("IPFS:", ipfs_hash)

# =========================
# VERIFY
# =========================
with tab2:
    st.subheader("Verify Certificate")

    query = st.text_input("Enter Certificate Hash")

    if st.button("Verify"):
        try:
            with open("chain.json", "r") as f:
                data = json.load(f)
        except:
            data = []

        found = None
        for cert in data:
            if cert["hash"] == query:
                found = cert
                break

        if found:
            raw = json.dumps({
                "name": found["name"],
                "reg": found["reg"],
                "course": found["course"],
                "institution": found["institution"],
                "timestamp": found["timestamp"]
            }, sort_keys=True)

            valid_sig = verify_signature(raw, found["signature"])

            try:
                on_chain = verify_on_blockchain(query)
            except:
                on_chain = False

            if valid_sig and on_chain:
                st.success("✅ VALID CERTIFICATE (Blockchain Verified)")
                st.json(found)
            else:
                st.error("❌ Tampered or Not on Blockchain")
        else:
            st.error("❌ Not Found")
