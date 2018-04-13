Version API
===========

.. py:module:: webu.version
.. py:currentmodule:: webu.version

.. py:class:: Version

The ``webu.version`` object exposes methods to interact with the RPC APIs under
the ``version_`` namespace.


Properties
----------

The following properties are available on the ``webu.eth`` namespace.

.. py:method:: Version.api(self)

    Returns the current Webu version.

    .. code-block:: python

        >>> webu.version.api
        "2.6.0"


.. py:method:: Version.node(self)

    * Delegates to ``webu_clientVersion`` RPC Method

    Returns the current client version.

    .. code-block:: python

        >>> webu.version.node
        'Ghuc/v1.4.11-stable-fed692f6/darwin/go1.7'


.. py:method:: Version.network(self)

    * Delegates to ``net_version`` RPC Method

    Returns the current network protocol version.

    .. code-block:: python

        >>> webu.version.network
        1


.. py:method:: Version.ethereum(self)

    * Delegates to ``eth_protocolVersion`` RPC Method

    Returns the current ethereum protocol version.

    .. code-block:: python

        >>> webu.version.ethereum
        63
