<h1 align="center">arrakis-schema</h1>

<p align="center">Schemas for the Arrakis API</p>

<p align="center">
</p>

---

## Endpoints

The Arrakis server responds to API requests corresponding to the four
main actions exposed by the client API:

* **stream**
* **describe**
* **find**
* **count**

as well as two actions which aid in publication:

* **partition**
* **publish**

All API requests are done in a two-stage approach by first sending an
Arrow Flight descriptor to the server, returning back a Flight info object
which contains the request and the server to contact, contained within
a Flight ticket. This ticket is then sent to receive back the expected
payload with a specific Arrow flight schema dependent on the request,
serialized in the Arrow 
![streaming format](https://arrow.apache.org/docs/format/Columnar.html#ipc-streaming-format).

The Flight descriptors sent to the server in the first stage are all
specified here as JSON packets which are UTF-8-encoded, using the command
variant of the Flight descriptor, which can be used to specify any
application-specific command.

## Schemas

The generic Flight descriptor schema is described within each endpoint in
`{endpoint}.json`. In addition, a generic descriptor specification for all
endpoints is described in `descriptor.json`.

## Usage


```python

from arrakis_schema import load_schema

schema = load_schema("count.json")

```
