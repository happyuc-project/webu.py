Quickstart
==========

.. contents:: :local:


Environment
------------

Webu.py requires Python 3. Often, the
best way to guarantee a clean Python 3 environment is with ``virtualenv``, like:

.. code-block:: shell

    # once:
    $ virtualenv -p python3 ~/.venv-py3

    # each session:
    $ source ~/.venv-py3/bin/activate

    # with virtualenv active, install...

Installation
------------

Webu.py can be installed using ``pip`` as follows.

.. code-block:: shell

   $ pip install webu


Installation from source can be done from the root of the project with the
following command.

.. code-block:: shell

   $ pip install .


Using Webu
----------

To use the webu library you will need to initialize the
:class:`~webu.Webu` class.

Use the ``auto`` module to guess at common node connection options.

.. code-block:: python

    >>> from webu.auto import w3
    >>> w3.eth.blockNumber
    4000000

To peek under the hood, see: :ref:`automatic_provider_detection`

This ``w3`` instance will now allow you to interact with the Ethereum
blockchain.


Connecting to your Node
-----------------------

Sometimes, webu cannot automatically detect where your node is.

You can connect to your Ethereum node (for example: ghuc or parity) using one of
the available :ref:`providers`, typically IPC or HTTP.

If your node is running locally, IPC will be faster and safer to expose.
If sharing the node across machines on a network, use HTTP instead.

IPC Provider
~~~~~~~~~~~~

.. code-block:: python

    >>> from webu import Webu, IPCProvider

    # for an IPC based connection
    >>> w3 = Webu(IPCProvider('/path/to/node/rpc-json/file.ipc'))

    >>> w3.eth.blockNumber
    4000000


HTTP Provider
~~~~~~~~~~~~~

.. code-block:: python

    >>> from webu import Webu, HTTPProvider

    # Note that you should create only one HTTPProvider per
    # process, as it recycles underlying TCP/IP network connections between
    # your process and Ethereum node
    >>> w3 = Webu(HTTPProvider('http://192.168.1.2:8545'))

    >>> w3.eth.blockNumber
    4000000

.. _provider_uri:

Provider via Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Alternatively, you can set the environment variable ``WEB3_PROVIDER_URI``
before starting your script, and webu will look for that provider first.

Valid formats for the this environment variable are:

- ``file:///path/to/node/rpc-json/file.ipc``
- ``http://192.168.1.2:8545``

Simple Contract Example
-----------------------

.. code-block:: python

    import json
    import webu

    from webu import Webu, TestRPCProvider
    from solc import compile_source
    from webu.contract import ConciseContract

    # Solidity source code
    contract_source_code = '''
    pragma solidity ^0.4.0;

    contract Greeter {
        string public greeting;

        function Greeter() {
            greeting = 'Hello';
        }

        function setGreeting(string _greeting) public {
            greeting = _greeting;
        }

        function greet() constant returns (string) {
            return greeting;
        }
    }
    '''

    compiled_sol = compile_source(contract_source_code) # Compiled source code
    contract_interface = compiled_sol['<stdin>:Greeter']

    # webu.py instance
    w3 = Webu(TestRPCProvider())

    # Instantiate and deploy contract
    contract = w3.eth.contract(abi=contract_interface['abi'], bytecode=contract_interface['bin'])

    # Get transaction hash from deployed contract
    tx_hash = contract.deploy(transaction={'from': w3.eth.accounts[0], 'gas': 410000})

    # Get tx receipt to get contract address
    tx_receipt = w3.eth.getTransactionReceipt(tx_hash)
    contract_address = tx_receipt['contractAddress']

    # Contract instance in concise mode
    contract_instance = w3.eth.contract(abi=contract_interface['abi'], address=contract_address, ContractFactoryClass=ConciseContract)

    # Getters + Setters for webu.eth.contract object
    print('Contract value: {}'.format(contract_instance.greet()))
    contract_instance.setGreeting('Nihao', transact={'from': w3.eth.accounts[0]})
    print('Setting value to: Nihao')
    print('Contract value: {}'.format(contract_instance.greet()))
