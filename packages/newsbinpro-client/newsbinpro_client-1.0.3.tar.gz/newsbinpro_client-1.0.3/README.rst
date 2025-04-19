Python-NewsbinPro-Client
========================

|PyPI version| |PyPI pyversions| |PyPI license|

This is an asyncio Python library to communicate with the `Newsbin
Pro <https://www.newsbin.com/>`__ Remote Control interface.

It implements all of `Remote Control Version 6.10 Interface
Spec <https://help.newsbin.com/index.php/Version_6.10_Interface_Spec>`__.

Installation
------------

::

   pip install newsbinpro_client

Documentation
-------------

The full library documentation can be found
`here <https://jonnybergdahl.github.io/newsbinpro_client/>`__.

Getting started
---------------

In order to activate the remote control interface, go to *Options* -
*Settings*, select ``Remote Control`` in the left menu, and check
``Enable Remote Control``. You can optionally set a password and change
the port. Then click *OK* to save. If you have a firewall active in your
machine, you need to `open the TCP port for
access <https://www.windowscentral.com/how-open-port-windows-firewall>`__.

The ``src/newsbinpro_sample.py`` file shows how to use the library. To
use the sample, change the ``HOST`` variable to the host name or IP
address of your Newsbin Pro install and the ``PASSWORD`` variable to the
password you setup.

Basic usage
~~~~~~~~~~~

The following code connects to Newsbin Pro and prints out the version
number and basic statistics.

.. code:: python

   import asyncio

   from newsbinpro_client import NewsbinProClient

   HOST = "172.30.1.60"
   PORT = 118
   PASSWORD = "password"

   async def main(host: str, port: int, password: str) -> None:

       # Create a client instance
       client = NewsbinProClient(host,
                                 port,
                                 password)

       print(f"Connecting to {host}:{port}")
       await client.connect()
       print(f"Newsbin Pro version        : {client.newsbin_version}")
       status = await client.get_status()
       print(f"Current speed              : {status.speed}")
       print(f"Data folder free space     : {status.data_folder_free_space_str}")
       print(f"Download folder free space : {status.download_folder_free_space_str}")

       await client.disconnect()
   if __name__ == "__main__":
       asyncio.run(main(HOST, PORT, PASSWORD))

.. |PyPI version| image:: https://badge.fury.io/py/newsbinpro_client.svg
   :target: https://badge.fury.io/py/newsbinpro_client
.. |PyPI pyversions| image:: https://img.shields.io/pypi/pyversions/newsbinpro_client.svg
   :target: https://pypi.python.org/pypi/newsbinpro_client/
.. |PyPI license| image:: https://img.shields.io/pypi/l/ansicolortags.svg
   :target: https://pypi.python.org/pypi/ansicolortags/
