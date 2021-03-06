Migrating your code from v3 to v4
=======================================

Webu.py follows `Semantic Versioning <http://semver.org>`_, which means
that version 4 introduced backwards-incompatible changes. If your
project depends on Webu.py v3, then you'll probably need to make some changes.

Here are the most common required updates:

Python 2 to Python 3
----------------------

Only Python 3 is supported in v4. If you are running in Python 2,
it's time to upgrade. We recommend using `2to3` which can make
most of your code compatible with Python 3, automatically.

The most important update, relevant to Webu.py, is the new :class:`bytes`
type. It is used regularly, throughout the library, whenever dealing with data
that is not guaranteed to be text.

Many different methods in Webu.py accept text or binary data, like contract methods,
transaction details, and cryptographic functions. The following example
uses :meth:`~Webu.sha3`, but the same pattern applies elsewhere.

In v3 & Python 2, you might have calculated the hash of binary data this way:

.. code-block:: python

    >>> Webu.sha3('I\xe2\x99\xa5SF')
    '0x50a826df121f4d076a3686d74558f40082a8e70b3469d8e9a16ceb2a79102e5e'

Or, you might have calculated the hash of text data this way:

.. code-block:: python

    >>> Webu.sha3(text=u'I♥SF')
    '0x50a826df121f4d076a3686d74558f40082a8e70b3469d8e9a16ceb2a79102e5e'

After switching to Python 3, these would instead be executed as:

.. code-block:: python

    >>> Webu.sha3(b'I\xe2\x99\xa5SF')
    HexBytes('0x50a826df121f4d076a3686d74558f40082a8e70b3469d8e9a16ceb2a79102e5e')

    >>> Webu.sha3(text='I♥SF')
    HexBytes('0x50a826df121f4d076a3686d74558f40082a8e70b3469d8e9a16ceb2a79102e5e')

Note that the return value is different too: you can treat :class:`hexbytes.main.HexBytes`
like any other bytes value, but the representation on the console shows you the hex encoding of
those bytes, for easier visual comparison.

It takes a little getting used to, but the new py3 types are much better. We promise.

Filters
---------

Filters usually don't work quite the way that people want them to.

The first step toward fixing them was to simplify them by removing the polling
logic. Now, you must request an update on your filters explicitly. That
means that any exceptions during the request will bubble up into your code.

In v3, those exceptions (like "filter is not found") were swallowed silently
in the automated polling logic. Here was the invocation for
printing out new block hashes as they appear:

.. code-block:: python

    >>> def new_block_callback(block_hash):
    ...     print "New Block: {0}".format(block_hash)
    ...
    >>> new_block_filter = webu.eth.filter('latest')
    >>> new_block_filter.watch(new_block_callback)

In v4, that same logic:

.. code-block:: python

    >>> new_block_filter = webu.eth.filter('latest')
    >>> for block_hash in new_block_filter.get_new_entries():
    ...     print("New Block: {}".format(block_hash))

The caller is responsible for polling the results from ``get_new_entries()``.
See :ref:`asynchronous_filters` for examples of filter-event handling with webu v4.

TestRPCProvider and HappyUCTesterProvider
------------------------------------------------

These providers are fairly uncommon. If you don't recognize the names,
you can probably skip the section.

However, if you were using webu.py for testing contracts,
you might have been using TestRPCProvider or HappyUCTesterProvider. 

In v4 there is a new :class:`HappyUCTesterProvider`, and the old v3 implementation has been 
removed. Webu.py v4 uses :class:`eth_tester.main.HappyUCTester` under the hood, instead
of eth-testrpc. While ``eth-tester`` is still in beta, many parts are
already in better shape than testrpc, so we decided to replace it in v4.

If you were using TestRPC, or were explicitly importing HappyUCTesterProvider, like:
``from webu.providers.tester import HappyUCTesterProvider``, then you will need to update.

With v4 you should import with ``from webu import HappyUCTesterProvider``. As before, you'll 
need to install Webu.py with the ``tester`` extra to get these features, like:

.. code-block:: bash

    $ pip install webu[tester]


Changes to base API convenience methods
---------------------------------------

Webu.toDecimal()
~~~~~~~~~~~~~~~~~

In v4 ``Webu.toDecimal()`` is renamed: :meth:`~Webu.toInt` for improved clarity. It does not return a :class:`decimal.Decimal`, it returns an :class:`int`.


Removed Methods
~~~~~~~~~~~~~~~~~~

- ``Webu.toUtf8`` was removed for :meth:`~Webu.toText`.
- ``Webu.fromUtf8`` was removed for :meth:`~Webu.toHex`.
- ``Webu.toAscii`` was removed for :meth:`~Webu.toBytes`.
- ``Webu.fromAscii`` was removed for :meth:`~Webu.toHex`.
- ``Webu.fromDecimal`` was removed for :meth:`~Webu.toHex`.

Provider Access
~~~~~~~~~~~~~~~~~

In v4, ``w3.currentProvider`` was removed, in favor of ``w3.providers``.

Disambiguating String Inputs
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There are a number of places where an arbitrary string input might be either
a byte-string that has been hex-encoded, or unicode characters in text.
These are named ``hexstr`` and ``text`` in Webu.py.
You specify which kind of :class:`str` you have by using the appropriate
keyword argument. See examples in :ref:`overview_type_conversions`.

In v3, some methods accepted a :class:`str` as the first positional argument.
In v4, you must pass strings as one of ``hexstr`` or ``text`` keyword arguments.

Notable methods that no longer accept ambiguous strings:

- :meth:`~Webu.sha3`
- :meth:`~Webu.toBytes`

Contracts
-----------

- When a contract returns the ABI type ``string``, Webu.py v4 now returns a :class:`str`
  value by decoding the underlying bytes using UTF-8.
- When a contract returns the ABI type ``bytes`` (of any length),
  Webu.py v4 now returns a :class:`bytes` value
