Middleware
==========

Webu manages layers of middlewares by default. They sit between the public Webu methods and the
:doc:`providers`, which handle native communication with the HappyUC client. Each layer
can modify the request and/or response. Some middlewares are enabled by default, and
others are available for optional use.

Each middleware layer gets invoked before the request reaches the provider, and then
processes the result after the provider returns, in reverse order. However, it is
possible for a middleware to return early from a
call without the request ever getting to the provider (or even reaching the middlewares
that are in deeper layers).

More information is available in the "Internals: :ref:`internals__middlewares`" section.


Default Middleware
------------------

Some middlewares are added by default if you do not supply any. The defaults
are likely to change regularly, so this list may not include the latest version's defaults.
You can find the latest defaults in the constructor in `webu/manager.py`

AttributeDict
~~~~~~~~~~~~~~~~~~

.. py:method:: webu.middleware.attrdict_middleware

    This middleware converts the output of a function from a dictionary to an ``AttributeDict``
    which enables dot-syntax access, like ``eth.getBlock('latest').number``
    in addition to ``eth.getBlock('latest')['number']``.

.eth Name Resolution
~~~~~~~~~~~~~~~~~~~~~

.. py:method:: webu.middleware.name_to_address_middleware

    This middleware converts HappyUC Name Service (ENS) names into the
    address that the name points to. For example :meth:`~webu.Eth.sendTransaction` will
    accept .eth names in the 'from' and 'to' fields.

Pythonic
~~~~~~~~~~~~

.. py:method:: webu.middleware.pythonic_middleware

    This converts arguments and returned values to python primitives,
    where appropriate. For example, it converts the raw hex string returned by the RPC call
    ``eth_blockNumber`` into an ``int``.

Gas Price Strategy
~~~~~~~~~~~~~~~~~~~~~~~~

.. py:method:: webu.middleware.gas_price_strategy_middleware

    This adds a gasPrice to transactions if applicable and when a gas price strategy has
    been set. See :ref:`Gas_Price` for information about how gas price is derived.

HTTPRequestRetry
~~~~~~~~~~~~~~~~~~

.. py:method:: webu.middleware.http_retry_request_middleware

    This middleware is a default specifically for HTTPProvider that retries failed
    requests that return the following errors: `ConnectionError`, `HTTPError`, `Timeout`,
    `TooManyRedirects`. Additionally there is a whitelist that only allows certain
    methods to be retried in order to not resend transactions, excluded methods are:
    `eth_sendTransaction`, `personal_signAndSendTransaction`, `personal_sendTransaction`.

.. _Modifying_Middleware:

Configuring Middleware
-----------------------

Middleware can be added, removed, replaced, and cleared at runtime. To make that easier, you
can name the middleware for later reference. Alternatively, you can use a reference to the
middleware itself.

Middleware Order
~~~~~~~~~~~~~~~~~~

Think of the middleware as being layered in an onion, where you initiate a webu.py request at
the outermost layer of the onion, and the HappyUC node (like ghuc or parity) receives and responds
to the request inside the innermost layer of the onion. Here is a (simplified) diagram:

.. code-block:: none

                                         New request from webu.py

                                                     |
                                                     |
                                                     v

                                             `````Layer 2``````
                                      ```````                  ```````
                                 `````               |                ````
                              ````                   v                    ````
                           ```                                                ```
                         `.               ````````Layer 1```````                `.`
                       ``             ````                      `````              .`
                     `.            ```               |               ```            `.`
                    .`          ```                  v                  ```           `.
                  `.          `.`                                         ```           .`
                 ``          .`                  `Layer 0`                  ``           .`
                ``         `.               `````        ``````               .           .`
               `.         ``             ```         |        ```              .`          .
               .         ``            `.`           |           ``             .           .
              .         `.            ``       JSON-RPC call       .`            .          .`
              .         .            ``              |              .            ``          .
             ``         .            .               v               .            .          .
             .         .`           .                                .            .          ``
             .         .            .          HappyUC node         .`           .           .
             .         .            .                                .            .           .
             .         ``           `.               |               .            .           .
             .          .            .`              |              .`            .          .
             `.         .`            .`          Response         .`            .`          .
              .          .             `.`           |           `.`            `.           .
              `.          .              ```         |        ````             `.           .
               .          `.               `````     v     ````               `.           ``
                .           .`                 ```Layer 0``                  ``           `.
                 .           `.                                            `.`           `.
                  .            `.                    |                   `.`            `.
                   .`            ```                 |                 ```             .`
                    `.              ```              v             ````              `.`
                      ``               ``````                 `````                 .`
                        ``                   `````Layer 1`````                   `.`
                          ```                                                  ```
                            ````                     |                      ```
                               `````                 v                  ````
                                   ``````                          `````
                                         `````````Layer 2``````````

                                                     |
                                                     v

                                          Returned value in Webu.py


The middlewares are maintained in ``Webu.middleware_stack``. See
below for the API.

When specifying middlewares in a list, or retrieving the list of middlewares, they will
be returned in the order of outermost layer first and innermost layer last. In the above
example, that means that ``list(w3.middleware_stack)`` would return the middlewares in
the order of: ``[2, 1, 0]``.

See "Internals: :ref:`internals__middlewares`" for a deeper dive to how middlewares work.

Middleware Stack API
~~~~~~~~~~~~~~~~~~~~~

To add or remove items in different layers, use the following API:

.. py:method:: Webu.middleware_stack.add(middleware, name=None)

    Middleware will be added to the outermost layer. That means the new middleware will modify the
    request first, and the response last. You can optionally name it with any hashable object,
    typically a string.

    .. code-block:: python

        >>> w3 = Webu(...)
        >>> w3.middleware_stack.add(webu.middleware.pythonic_middleware)
        # or
        >>> w3.middleware_stack.add(webu.middleware.pythonic_middleware, 'pythonic')

.. py:method:: Webu.middleware_stack.inject(middleware, name=None, layer=None)

    Inject a named middleware to an arbitrary layer.

    The current implementation only supports injection at the innermost or
    outermost layers. Note that injecting to the outermost layer is equivalent to calling
    :meth:`Webu.middleware_stack.add` .

    .. code-block:: python

        # Either of these will put the pythonic middleware at the innermost layer
        >>> w3 = Webu(...)
        >>> w3.middleware_stack.inject(webu.middleware.pythonic_middleware, layer=0)
        # or
        >>> w3.middleware_stack.inject(webu.middleware.pythonic_middleware, 'pythonic', layer=0)

.. py:method:: Webu.middleware_stack.remove(middleware)

    Middleware will be removed from whatever layer it was in. If you added the middleware with
    a name, use the name to remove it. If you added the middleware as an object, use the object
    again later to remove it:

    .. code-block:: python

        >>> w3 = Webu(...)
        >>> w3.middleware_stack.remove(webu.middleware.pythonic_middleware)
        # or
        >>> w3.middleware_stack.remove('pythonic')

.. py:method:: Webu.middleware_stack.replace(old_middleware, new_middleware)

    Middleware will be replaced from whatever layer it was in. If the middleware was named, it will
    continue to have the same name. If it was un-named, then you will now reference it with the new
    middleware object.

    .. code-block:: python

        >>> from webu.middleware import pythonic_middleware, attrdict_middleware
        >>> w3 = Webu(...)

        >>> w3.middleware_stack.replace(pythonic_middleware, attrdict_middleware)
        # this is now referenced by the new middleware object, so to remove it:
        >>> w3.middleware_stack.remove(attrdict_middleware)

        # or, if it was named

        >>> w3.middleware_stack.replace('pythonic', attrdict_middleware)
        # this is still referenced by the original name, so to remove it:
        >>> w3.middleware_stack.remove('pythonic')

.. py:method:: Webu.middleware_stack.clear()

    Empty all the middlewares, including the default ones.

    .. code-block:: python

        >>> w3 = Webu(...)
        >>> w3.middleware_stack.clear()
        >>> assert len(w3.middleware_stack) == 0


Optional Middleware
-----------------------

Webu ships with non-default middleware, for your custom use. In addition to the other ways of
:ref:`Modifying_Middleware`, you can specify a list of middleware when initializing Webu, with:

.. code-block:: python

    Webu(middlewares=[my_middleware1, my_middleware2])

.. warning::
  This will
  *replace* the default middlewares. To keep the default functionality,
  either use ``middleware_stack.add()`` from above, or add the default middlewares to your list of
  new middlewares.

Below is a list of built-in middleware, which is not enabled by default.

Stalecheck
~~~~~~~~~~~~

.. py:method:: webu.middleware.make_stalecheck_middleware(allowable_delay)

    This middleware checks how stale the blockchain is, and interrupts calls with a failure
    if the blockchain is too old.

    * ``allowable_delay`` is the length in seconds that the blockchain is allowed to be
      behind of ``time.time()``

    Because this middleware takes an argument, you must create the middleware
    with a method call.

    .. code-block:: python

        two_day_stalecheck = make_stalecheck_middleware(60 * 60 * 24 * 2)
        webu.middleware_stack.add(two_day_stalecheck)

    If the latest block in the blockchain is older than 2 days in this example, then the
    middleware will raise a ``StaleBlockchain`` exception on every call except
    ``webu.eth.getBlock()``.


Cache
~~~~~~~~~~~

All of the caching middlewares accept these common arguments.

* ``cache_class`` must be a callable which returns an object which implements the dictionary API.
* ``rpc_whitelist`` must be an iterable, preferably a set, of the RPC methods that may be cached.
* ``should_cache_fn`` must be a callable with the signature ``fn(method, params, response)`` which returns whhuc the response should be cached.


.. py:method:: webu.middleware.construct_simple_cache_middleware(cache_class, rpc_whitelist, should_cache_fn)

    Constructs a middleware which will cache the return values for any RPC
    method in the ``rpc_whitelist``.

    A ready to use version of this middleware can be found at
    ``webu.middlewares.simple_cache_middleware``.


.. py:method:: webu.middleware.construct_time_based_cache_middleware(cache_class, cache_expire_seconds, rpc_whitelist, should_cache_fn)

    Constructs a middleware which will cache the return values for any RPC
    method in the ``rpc_whitelist`` for an amount of time defined by
    ``cache_expire_seconds``.

    * ``cache_expire_seconds`` should be the number of seconds a value may
      remain in the cache before being evicted.

    A ready to use version of this middleware can be found at
    ``webu.middlewares.time_based_cache_middleware``.


.. py:method:: webu.middleware.construct_latest_block_based_cache_middleware(cache_class, average_block_time_sample_size, default_average_block_time, rpc_whitelist, should_cache_fn)

    Constructs a middleware which will cache the return values for any RPC
    method in the ``rpc_whitelist`` for an amount of time defined by
    ``cache_expire_seconds``.

    * ``average_block_time_sample_size`` The number of blocks which should be
      sampled to determine the average block time.
    * ``default_average_block_time`` The initial average block time value to
      use for cases where there is not enough chain history to determine the
      average block time.

    A ready to use version of this middleware can be found at
    ``webu.middlewares.latest_block_based_cache_middleware``.

.. _ghuc-poa:

Ghuc-style Proof of Authority
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This middleware is required to connect to ``ghuc --dev`` or the Rinkeby public network.

For example, to connect to a local ``ghuc --dev`` instance on Linux:


.. code-block:: python

    >>> from webu import Webu, IPCProvider

    # connect to the default ghuc --dev IPC location
    >>> w3 = Webu(IPCProvider('/tmp/ghuc.ipc'))

    >>> from webu.middleware import ghuc_poa_middleware

    # inject the poa compatibility middleware to the innermost layer
    >>> w3.middleware_stack.inject(ghuc_poa_middleware, layer=0)

    # confirm that the connection succeeded
    >>> w3.version.node
    'Ghuc/v1.7.3-stable-4bb3c89d/linux-amd64/go1.9'

Why is ``ghuc_poa_middleware`` necessary?
''''''''''''''''''''''''''''''''''''''''''''''''''''''''

There is no strong community consensus on a single Proof-of-Authority (PoA) standard yet.
Some nodes have successful experiments running, though. One is happyuc-go (ghuc),
which uses a prototype PoA for it's development mode and the Rinkeby test network.

Unfortunately, it does deviate from the yellow paper specification, which constrains the
``extraData`` field in each block to a maximum of 32-bytes. Ghuc's PoA uses more than
32 bytes, so this middleware modifies the block data a bit before returning it.
