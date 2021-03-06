Webu Internals
==============


.. warning:: This section of the documentation is for advanced users.  You should probably stay away from these APIs if you don't know what you are doing.

The Webu library has multiple layers of abstraction between the public api
exposed by the webu object and the backend or node that webu is connecting to.

* **Providers** are responsible for the actual communication with the
  blockchain such as sending JSON-RPC requests over HTTP or an IPC socket.
* **Middlewares** provide hooks for monitoring and modifying requests and
  responses to and from the provider.  These can be *global* operating on all
  providers or specific to one provider.
* **Managers** provide thread safety and primatives to allow for asyncronous usage of webu.

Here are some common things you might want to do with these APIs.

* Redirect certain RPC requests to different providers such as sending all
  *read* operations to a provider backed by Infura and all *write* operations
  to a happyuc-go node that you control.
* Transparently intercept transactions sent over ``eth_sendTransaction``, sign
  them locally, and then send them through ``eth_sendRawTransaction``.
* Modify the response from an RPC request so that it is returned in different
  format such as converting all integer values to their hexidecimal
  representation.
* Validate the inputs to RPC requests


Request Lifecycle
-----------------

Each webu RPC call passes through these layers in the following manner.

.. code-block:: none

                   ***********    ************
                   | Request |    | Response |
                   ***********    ************
                       |                ^
                       v                |
                 +-----------------------------+
                 |            Manager          |
                 +-----------------------------+
                       |                ^
                       v                |
                 +-----------------------------+
                 |     Global Middlewares      |
                 +-----------------------------+
                       |                ^
                       v                |
                 +-----------------------------+
                 |    Provider Middlewares     |
                 +-----------------------------+
                       |                ^
                       v                |
                 +-----------------------------+
                 |          Provider           |
                 +-----------------------------+


You can visualize this relationship like an onion, with the Provider at the
center.  The request originates from the Manager, outside of the onion, passing
down through each layer of the onion until it reaches the Provider at the
center.  The Provider then handles the request, producing a response which will
then pass back out from the center of the onion, through each layer until it is
finally returned by the Manager.

In the situation where webu is operating with multiple providers the same
lifecycle applies.  The manager will iterate over each provider, returning the
response from the first provider that returns a response.


Providers
---------

A provider is responsible for all direct blockchain interactions.  In most
cases this means interacting with the JSON-RPC server for an happyuc node over
HTTP or an IPC socket.  There is however nothing which requires providers to be
RPC based, allowing for providers designed for testing purposes which use an
in-memory EVM to fulfill requests.

In most simple cases you will be using a single provider.  However, if you
would like to use Webu with multiple providers, you can simply pass them in as
a list when instantiating your ``Webu`` object.


.. code-block:: python

    >>> webu = Webu([provider_a, provider_b])



Writing your own Provider
~~~~~~~~~~~~~~~~~~~~~~~~~

Writing your own provider requires implementing two required methods as well as
setting the middlewares the provider should use.


.. py:method:: BaseProvider.make_request(method, params)

    Each provider class **must** implement this method.  This method **should**
    return a JSON object with either a ``'result'`` key in the case of success,
    or an ``'error'`` key in the case of failure.


    * ``method``  This will be a string representing the JSON-RPC method that
      is being called such as ``'eth_sendTransaction'``.
    * ``params``  This will be a list or other iterable of the parameters for
      the JSON-RPC method being called.


.. py:method:: BaseProvider.isConnected()

    This function should return ``True`` or ``False`` depending on whhuc the
    provider should be considered *connected*.  For example, an IPC socket
    based provider should return ``True`` if the socket is open and ``False``
    if the socket is closed.


If a provider is unable to respond to certain RPC calls it should raise the
``webu.exceptions.CannotHandleRequest`` exception.  When this happens, the
request is issued to the next configured provider.  If no providers are able to
handle the request then a ``webu.exceptions.UnhandledRequest`` error will be
raised.

.. py:attribute:: BaseProvider.middlewares

    This should be an iterable of middlewares.

You can set a new list of middlewares by assigning to ``provider.middlewares``,
with the first middleware that processes the request at the beginning of the list.


.. _internals__middlewares:

Middlewares
-----------

.. note:: The Middleware API in webu borrows heavily from the Django middleware API introduced in version 1.10.0

Middlewares provide a simple yet powerful api for implementing layers of
business logic for webu requests.  Writing middleware is simple.

.. code-block:: python

    def simple_middleware(make_request, webu):
        # do one-time setup operations here

        def middleware(method, params):
            # do pre-processing here

            # perform the RPC request, getting the response
            response = make_request(method, params)

            # do post-processing here

            # finally return the response
            return response
        return middleware


It is also possible to implement middlewares as a class.


.. code-block:: python

    class SimpleMiddleware:
        def __init__(self, make_request, webu):
            self.webu = webu
            self.make_request = make_request

        def __call__(self, method, params):
            # do pre-processing here

            # perform the RPC request, getting the response
            response = self.make_request(method, params)

            # do post-processing here

            # finally return the response
            return response


The ``make_request`` parameter is a callable which takes two
positional arguments, ``method`` and ``params`` which correspond to the RPC
method that is being called.  There is no requirement that the ``make_request``
function be called.  For example, if you were writing a middleware which cached
responses for certain methods your middleware would likely not call the
``make_request`` method, but instead get the response from some local cache.

By default, Webu will use the ``webu.middleware.pythonic_middleware``.  This
middleware performs the following translations for requests and responses.

* Numeric request parameters will be converted to their hexidecimal representation
* Numeric responses will be converted from their hexidecimal representations to
  their integer representations.

The ``RequestManager`` object exposes the ``middleware_stack`` object to manage middlewares. It
is also exposed on the ``Webu`` object for convenience. That API is detailed in
:ref:`Modifying_Middleware`.


Managers
--------

The Manager acts as a gatekeeper for the request/response lifecycle.  It is
unlikely that you will need to change the Manager as most functionality can be
implemented in the Middleware layer.
