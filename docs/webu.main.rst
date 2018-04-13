Webu API
========

.. contents:: :local:

.. py:module:: webu
.. py:currentmodule:: webu


.. py:class:: Webu(provider)

Each ``webu`` instance exposes the following APIs.

Providers
~~~~~~~~~

.. py:attribute:: Webu.HTTPProvider

    Convenience API to access :py:class:`webu.providers.rpc.HTTPProvider`

.. py:attribute:: Webu.IPCProvider

    Convenience API to access :py:class:`webu.providers.ipc.IPCProvider`

.. py:method:: Webu.setProviders(provider)

    Updates the current webu instance with the new list of providers. It
    also accepts a single provider.


Encoding and Decoding Helpers
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

See :ref:`overview_type_conversions`


Currency Conversions
~~~~~~~~~~~~~~~~~~~~~

See :ref:`overview_currency_conversions`


Addresses
~~~~~~~~~

See :ref:`overview_addresses`


RPC APIS
--------

Each ``webu`` instance also exposes these namespaced APIs.



.. py:attribute:: Webu.eth

    See :doc:`./webu.eth`

.. py:attribute:: Webu.shh

    See :doc:`./webu.shh`

.. py:attribute:: Webu.personal

    See :doc:`./webu.personal`

.. py:attribute:: Webu.version

    See :doc:`./webu.version`

.. py:attribute:: Webu.txpool

    See :doc:`./webu.txpool`

.. py:attribute:: Webu.miner

    See :doc:`./webu.miner`

.. py:attribute:: Webu.admin

    See :doc:`./webu.admin`


