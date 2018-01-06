The speed-monitor offers a rest API (at `/api`) which handles speed-monitor
results.  There are three major models: a client, a server and a result.  The
application stores these data in a database.  It is possible to view these
results via the `/chart` url.  It is also possible to edit these results
via the `/admin` interface.