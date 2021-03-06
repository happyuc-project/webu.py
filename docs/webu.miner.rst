Miner API
=========

.. py:module:: webu.miner

.. py:class:: Miner

The ``webu.miner`` object exposes methods to interact with the RPC APIs under
the ``miner_`` namespace.


Properties
----------

The following properties are available on the ``webu.miner`` namespace.

.. py:attribute:: Miner.hashrate

    * Delegates to ``eth_hashrate`` RPC Method

    Returns the current number of hashes per second the node is mining with.

    .. code-block:: python

        >>> webu.eth.hashrate
        906


    .. note:: This property is an alias to ``webu.eth.hashrate``.


Methods
-------

The following methods are available on the ``webu.miner`` namespace.


.. py:method:: Miner.makeDAG(number)

    * Delegates to ``miner_makeDag`` RPC Method

    Generate the DAG for the given block number.

    .. code-block:: python

        >>> webu.eth.makeDag(10000)


.. py:method:: Miner.setExtra(extra)

    * Delegates to ``miner_setExtra`` RPC Method

    Set the 32 byte value ``extra`` as the extra data that will be included
    when this node mines a block.

    .. code-block:: python

        >>> webu.eth.setExtra('abcdefghijklmnopqrstuvwxyzABCDEF')


.. py:method:: Miner.setGasPrice(gas_price)

    * Delegates to ``miner_setGasPrice`` RPC Method

    Sets the minimum accepted gas price that this node will accept when mining
    transactions.  Any transactions with a gas price below this value will be
    ignored.

    .. code-block:: python

        >>> webu.eth.setGasPrice(19999999999)


.. py:method:: Miner.start(num_threads)

    * Delegates to ``miner_start`` RPC Method

    Start the CPU mining proccess using the given number of threads.

    .. code-block:: python

        >>> webu.eth.start(2)


.. py:method:: Miner.stop()

    * Delegates to ``miner_stop`` RPC Method

    Stop the CPU mining operation

    .. code-block:: python

        >>> webu.eth.stop()


.. py:method:: Miner.startAutoDAG()

    * Delegates to ``miner_startAutoDag`` RPC Method

    Enable automatic DAG generation.

    .. code-block:: python

        >>> webu.eth.startAutoDAG()


.. py:method:: Miner.stopAutoDAG()

    * Delegates to ``miner_stopAutoDag`` RPC Method

    Disable automatic DAG generation.

    .. code-block:: python

        >>> webu.eth.stopAutoDAG()
