# Connor's Remote Events (RE)

Connor's Remote Events (RE) is a simple library that allows the end-user to call python functions from another server. This is highly powerful if you are coding an application that offloads processes to another server.

If you want to offload automation tasks to another device, this is the package to use. It is extremely reliable and robust for minimum-effort python automation.

To install: `pip install remote-events`

## First example

### `main.py`

```py
"""
Main Example Script for RemoteFunctions

This script demonstrates remote function execution over HTTP using the RemoteFunctions class.
It operates in two modes:
    1. Server mode: Registers functions and starts a Flask server to handle remote calls.
    2. Client mode: Connects to the server, retrieves available functions, and invokes them remotely.

All communications are serialized with pickle for reliable data exchange.

Usage:
    To run as a server:
        python main.py server
    To run as a client:
        python main.py client

Note: Ensure the server is running before starting the client.
"""

from remote_functions import RemoteFunctions
from remote_functions import run_self_with_output_filename
from typing import Any
import sys

# Initialize RemoteFunctions with password authentication.
# set is_queue=True for a queue-based call system, to act similarly as a mutex
rf = RemoteFunctions(password="Whoop!-", is_queue=False) 

@rf.as_remote()
def a(b: Any) -> Any:
    """Return the input value."""
    return b

@rf.as_remote()
def add(x: float, y: float) -> float:
    """Return the sum of x and y."""
    return x + y

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "server":

        # Start the server (blocking call) on 0.0.0.0:5001.
        rf.start_server(host="0.0.0.0", port=5001)

    elif len(sys.argv) > 1 and sys.argv[1] == "client":
        # Connect to the server running on localhost:5001.
        rf.connect_to_server("localhost", 5001)

        print("Invoking function 'a' with argument 'Hello World!'")
        result = a("Hello World!")
        print("Result:", result)

        print("Invoking function 'add' with arguments 1 and 3")
        result = add(1, 3)
        print("Result:", result)
    else:
        print("Usage: python main.py [server|client]")
```

In two terminals:
1. First terminal, run the server with `python main.py server`

2. Second terminal, run the client with `python main.py client`


## Second example

The purpose is for you to create your own script, like my_functions.py
and replicate the python script to the server and client. 

### `my_functions.py`

```py
from remote_functions import RemoteFunctions
from typing import Any

# Initialize RemoteFunctions
# set is_queue=True for a queue-based call system, to act similarly as a mutex
rf = RemoteFunctions(is_queue=False) 

@rf.as_remote()
def a(b: Any) -> Any:
    """Return the input value."""
    return b

@rf.as_remote()
def add(x: float, y: float) -> float:
    """Return the sum of x and y."""
    return x + y

```

### `server.py`

You will run this on the server-side:
```py
import my_functions

if __name__ == "__main__":
    my_functions.rf.set_password("Whoop!-")
    my_functions.start_server(host="0.0.0.0", port=5001)
```

### `client.py`

You will run this on your local device:
```py
import my_functions

if __name__ == "__main__":
    my_functions.rf.set_password("Whoop!-")
    my_functions.connect_to_server("localhost", 5001)

    print("Invoking function 'a' with argument 'Hello World!'")
    result = my_functions.a("Hello World!")
    print("Result:", result)

    print("Invoking function 'add' with arguments 1 and 3")
    result = my_functions.add(1, 3)
    print("Result:", result)

```

In two terminals:
1. First terminal, run the server with `python server.py`

2. Second terminal, run the client with `python client.py`


## Last note

You can set SSL context via

```

rf.set_ssl_context("cert.pem", "key.pem")
```


More information about creating FLASK SSL contexts [here](https://kracekumar.com/post/54437887454/ssl-for-flask-local-development/)