Net API
===========

.. py:module:: webu.net
.. py:currentmodule:: webu.net

.. py:class:: Net

The ``webu.net`` object exposes methods to interact with the RPC APIs under
the ``net_`` namespace.


Properties
----------

The following properties are available on the ``webu.net`` namespace.

.. py:method:: Net.chainId(self)

    * Delegates to ``net_version`` RPC Method

    Returns the current network chainId/version and is an alias of ``webu.net.version``.

    .. code-block:: python

        >>> webu.net.chainId
        1


.. py:method:: Net.version(self)

    * Delegates to ``net_version`` RPC Method

    Returns the current network chainId/version.

    .. code-block:: python

        >>> webu.net.version
        1

