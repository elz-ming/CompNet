var Contracts = {
    HouseRegistrationContract: {
        abi: [
            {
                "inputs": [
                    {
                        "internalType": "string",
                        "name": "_owner",
                        "type": "string"
                    }
                ],
                "name": "registerNewHouse",
                "outputs": [],
                "stateMutability": "nonpayable",
                "type": "function"
            },
            {
                "inputs": [],
                "stateMutability": "nonpayable",
                "type": "constructor"
            },
            {
                "inputs": [],
                "name": "houseCount",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            },
            {
                "inputs": [
                    {
                        "internalType": "uint256",
                        "name": "",
                        "type": "uint256"
                    }
                ],
                "name": "houseList",
                "outputs": [
                    {
                        "internalType": "uint256",
                        "name": "houseNo",
                        "type": "uint256"
                    },
                    {
                        "internalType": "string",
                        "name": "owner",
                        "type": "string"
                    }
                ],
                "stateMutability": "view",
                "type": "function"
            }
        ],
        address: "0x5b082475700c68bc768A68295C07f6352468cE53",
        endpoint: "https://sepolia.infura.io/v3/" // ipv4 address "https://192.168.20.2" replace with private network's IPv4 address and port
    }
};

function HouseRegistrationApp(Contract) {
    this.web3 = null;
    this.instance = null;
    this.Contract = Contract;
}

HouseRegistrationApp.prototype.onReady= async function() {
    await this.init();
    $('#message').append("DApp loaded successfully.");
    this.loadHouseRegistration();
}


HouseRegistrationApp.prototype.init = async function() {
    if (typeof window.ethereum !== 'undefined') {
        this.web3 = new Web3(ethereum);
        console.log('Web3 version:', Web3.version); // Check the Web3 version
        console.log('Web3:', this.web3); // Verify Web3 instance
        try {
            await ethereum.request({ method: 'eth_requestAccounts' });
        } catch (error) {
            console.error('Error requesting account access:', error);
            return;
        }
        console.log('Web3 instance:', this.web3); // Verify the Web3 instance
        const abi = this.Contract.abi;
        const address = this.Contract.address;
        // Make sure the new keyword is used and this.web3 is correctly referencing Web3 instance
        this.instance = new this.web3.eth.Contract(abi, address);
        console.log('Contract instance:', this.instance);
    } else {
        console.error('MetaMask not found. Please install MetaMask.');
        // const endpoint = this.Contract.endpoint;
        // this.web3 = new Web3(new Web3.providrs.HttpProvider(endpoint));
        return;
    }
};

if (typeof Contracts === "undefined")
  var Contracts = { HouseRegistrationContract: { abi: [] } };
var houseRegistrationApp = new HouseRegistrationApp(
  Contracts["HouseRegistrationContract"]
);

$(document).ready(function () {
  houseRegistrationApp.onReady();
});

//Calls the houseCount function in the smart contract
HouseRegistrationApp.prototype.getHouseCount = function (cb) {
  this.instance.methods.houseCount().call(function (error, houseCount) {
    cb(error, houseCount);
  });
};

// Calls the houseList function in the smart contract
HouseRegistrationApp.prototype.getHouse = function (houseNo, cb) {
this.instance.methods.houseList(houseNo).call(function (error, house) {
    cb(error, house);
});
};  

HouseRegistrationApp.prototype.loadHouseRegistration = function () {
var that = this;
this.getHouseCount(function (error, houseCount) {
    if (error) {
        console.log(error)
    }
$("#message").text("House Count: " + houseCount);
for (let i = 1; i <= houseCount; i++) {
    var houseNo = i;
    that.getHouse(houseNo, function (error, house) {
        if (error) {
            console.log(error)
            }
            var number = house[0];
            var owner = house[1];
            var houseTemplate = "<tr><td>" + number + "</td><td>" + owner + "</td></tr>"
            $("#houseListResults").append(houseTemplate);
        });
    }
});
}