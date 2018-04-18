.. _providers:

Providers
=========

The provider is how webu talks to the blockchain.  Providers take JSON-RPC
requests and return the response.  This is normally done by submitting the
request to an HTTP or IPC socket based server.

If you are already happily connected to your HappyUC node, then you
can skip the rest of the Providers section.

Automatic vs Manual Providers
-----------------------------

The ``Webu`` object will look for the HappyUC node in a few
standard locations if no providers are specified. Auto-detection happens
when you initialize like so:

.. code-block:: python

    from webu.auto import w3

    # which is equivalent to:

    from webu import Webu
    w3 = Webu()

You can manually create a connection by specifying a provider like so:

.. code-block:: python

    from webu import Webu, HTTPProvider
    provider = HTTPProvider('http://localhost:8545')
    webu = Webu(provider)

.. _automatic_provider_detection:

How Automated Detection Works
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Webu attempts to connect to nodes in the following order, using the first
succesful connection it can make:

1. The connection specified by an environment variable, see :ref:`provider_uri`
2. :class:`~webu.providers.ipc.IPCProvider`, which looks for several IPC file locations
3. :class:`~webu.providers.rpc.HTTPProvider`, which attempts to connect to "http://localhost:8545"
4. None - if no providers are successful, you can still use Webu APIs
   that do not require a connection, like:

   - :ref:`overview_type_conversions`
   - :ref:`overview_currency_conversions`
   - :ref:`overview_addresses`
   - :class:`~webu.account.Account`
   - etc.

.. _automatic_provider_detection_examples:

Examples Using Automated Detection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    There are client specific APIs.  If you are writing client agnostic code, in some situations
    you may want to know what happyuc implementation is connected, and proceed
    accordingly.

    The following retrieves the client enode endpoint verifying there is a connected provider:

.. code-block:: python

    from webu.auto import w3

    connected = any(provider.isConnected for provider in w3.providers)

    if connected and w3.version.node.startswith('Parity'):
        enode = w3.parity.enode

    elif connected and w3.version.node.startswith('Ghuc'):
        enode = w3.admin.nodeInfo['enode']

    else:
        enode = None


Built In Providers
------------------

Webu ships with the following providers which are appropriate for connecting to
local and remote JSON-RPC servers.


HTTPProvider
~~~~~~~~~~~~

.. py:class:: webu.providers.rpc.HTTPProvider(endpoint_uri[, request_kwargs])

    This provider handles interactions with an HTTP or HTTPS based JSON-RPC server.

    * ``endpoint_uri`` should be the full URI to the RPC endpoint such as
      ``'https://localhost:8545'``.  For RPC servers behind HTTP connections
      running on port 80 and HTTPS connections running on port 443 the port can
      be omitted from the URI.
    * ``request_kwargs`` this should be a dictionary of keyword arguments which
      will be passed onto the http/https request.

    .. code-block:: python

        >>> from webu import Webu
        >>> webu = Webu(Webu.HTTPProvider("http://127.0.0.1:8545")

    Under the hood, the ``HTTPProvider`` uses the python requests library for
    making requests.  If you would like to modify how requests are made, you can
    use the ``request_kwargs`` to do so.  A common use case for this is increasing
    the timeout for each request.


    .. code-block:: python

        >>> from webu import Webu
        >>> webu = Webu(Webu.HTTPProvider("http://127.0.0.1:8545", request_kwargs={'timeout': 60}))


IPCProvider
~~~~~~~~~~~

.. py:class:: webu.providers.ipc.IPCProvider(ipc_path=None, testnet=False, timeout=10)

    This provider handles interaction with an IPC Socket based JSON-RPC
    server.

    *  ``ipc_path`` is the filesystem path to the IPC socket.:56

    .. code-block:: python

        >>> from webu import Webu
        >>> webu = Webu(Webu.IPCProvider("~/Library/HappyUC/ghuc.ipc"))

    If no ``ipc_path`` is specified, it will use the first IPC file
    it can find from this list:

    - On Linux:

      - ``~/.happyuc/ghuc.ipc``
      - ``~/.local/share/io.parity.happyuc/jsonrpc.ipc``
    - On Mac OS:

      - ``~/Library/HappyUC/ghuc.ipc``
      - ``~/Library/Application Support/io.parity.happyuc/jsonrpc.ipc``
    - On Windows:

      - ``\\\.\pipe\ghuc.ipc``
      - ``\\\.\pipe\jsonrpc.ipc``


WebsocketProvider
~~~~~~~~~~~~~~~~~

.. py:class:: webu.providers.websocket.WebsocketProvider(endpoint_uri)

    This provider handles interactions with an WS or WSS based JSON-RPC server.

    .. code-block:: python

        >>> from webu import Webu
        >>> webu = Webu(Webu.WebsocketProvider("ws://127.0.0.1:8546")


.. py:currentmodule:: webu.providers.eth_tester

HappyUCTesterProvider
~~~~~~~~~~~~~~~~~~~~~~

.. warning:: Experimental:  This provider is experimental. There are still significant gaps in
    functionality. However, it is the default replacement for
    :class:`webu.providers.tester.HappyUCTesterProvider`
    and is being actively developed and supported.

.. py:class:: HappyUCTesterProvider(eth_tester=None)

    This provider integrates with the ``eth-tester`` library.  The
    ``eth_tester`` constructor argument should be an instance of the
    :class:`~eth_tester.HappyUCTester` class provided by the ``eth-tester``
    library.  If you would like a custom eth-tester instance to test with,
    see the ``eth-tester`` library documentation for details.

    .. code-block:: python

        >>> from webu import Webu, HappyUCTesterProvider
        >>> w3 = Webu(HappyUCTesterProvider())



HappyUCTesterProvider (legacy)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. warning:: Deprecated:  This provider is deprecated in favor of
    :class:`~webu.providers.eth_tester.HappyUCTesterProvider` and the newly created eth-tester.

.. py:class:: webu.providers.tester.HappyUCTesterProvider()

    This provider can be used for testing.  It uses an ephemeral blockchain
    backed by the ``happyuc.tester`` module.

    .. code-block:: python

        >>> from webu import Webu
        >>> from webu.providers.tester import HappyUCTesterProvider
        >>> w3 = Webu(HappyUCTesterProvider())

TestRPCProvider
~~~~~~~~~~~~~~~

.. warning:: Deprecated:  This provider is deprecated in favor of
    :class:`~webu.providers.eth_tester.HappyUCTesterProvider` and the newly created eth-tester.

.. py:class:: TestRPCProvider()

    This provider can be used for testing.  It uses an ephemeral blockchain
    backed by the ``happyuc.tester`` module.  This provider will be slower
    than the ``HappyUCTesterProvider`` since it uses an HTTP server for RPC
    interactions with.


AutoProvider
~~~~~~~~~~~~

:class:`~webu.providers.auto.AutoProvider` is the default used when initializing
:class:`webu.Webu` without any providers. There's rarely a reason to use it
explicitly.


Using Multiple Providers
------------------------

Webu supports the use of multiple providers.  This is useful for cases where
you wish to delegate requests across different providers.  To use this feature,
simply instantiate your webu instance with an iterable of provider instances.


.. code-block:: python

    >>> from webu import Webu, HTTPProvider
    >>> from . import MySpecialProvider
    >>> special_provider = MySpecialProvider()
    >>> infura_provider = HTTPProvider('https://ropsten.infura.io')
    >>> webu = Webu([special_provider, infura_provider])


When webu has multiple providers it will iterate over them in order, trying the
RPC request and returning the first response it receives.  Any provider which
*cannot* respond to a request **must** throw a
``webu.exceptions.CannotHandleRequest`` exception.

If none of the configured providers are able to handle the request, then a
``webu.exceptions.UnhandledRequest`` exception will be thrown.
