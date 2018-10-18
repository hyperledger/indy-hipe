- Name: postgres-storage-plugin
- Author: Ian Costanzo iancostanzo@gmail.com
- Start Date: 2018-10-18
- PR:
- Jira Issue:

# Summary
[summary]: #summary

This HIPE describes a common framework and set of tools for developing wallet storage plug-ins, including:

- Standard rust software components to facilitate building new plug-ins (in rust)
- A standard test suite for verifying correct implementation of the storage plug-in
- Standard interfaces and constants exposed from the indy-sdk shared library

A Postgres plug-in has been developed illustrating some aspects of the proposed framework, and to be used to facilitate discussion of how the above points will be implemented.  The initial codebase for the Postgres plug-in is available at https://github.com/ianco/indy-sdk/tree/postgres_plugin

This document contains the following sections:

- "Motivation" - Based on experience building the Postgres plug-in, this HIPE is necessary
- "Tutorial" - Describes how to install, test and integrate the initial implementation of the Postgres storage plug-in
- "Reference" - Describes the design and initial implementation of the initial Postgres plug-in
- "Drawbacks (and outstanding questions)".  Describes outstanding issues and questions (including "hacks" that had to be made to get the Postgres plug-in working)

# Motivation
[motivation]: #motivation

The default wallet as delivered with the Indy-sdk is based on SQLite, a file-based database platform.  Although this database can provide excellent performance with large data volumes, testing with the BC Government applications demonstrated that this platform is not scalable on the OpenShift platform.  The decision was made by the BC Government team to migrate to a Postgres-based wallet.  In addition, other organizations have expressed interest in alternate database platforms for wallet storage.

The Indy-sdk provides an API definition for developing new wallet storage plug-ins, and an example "in-memory" storage plug-ins, this has some limitations:

- The in-memory sample is not implemented in a shared library, does not implement a back-end database, and does not fully implement the storage API (for example wallet search is not implemented)
- Rust code is available for supporting functionality (e.g. search operations, error codes, other utilities) however these are not implemented in a manner to allow the code to be shared with plug-ins, resulting in duplicated code
- A common test framework is not provided

These issues were all encountered when developing a new Postgres plug-in.  Work-arounds and other solutions were implemented specifically for the Postgres plug-in, however it is desired to surface these issues with the Indy community and confirm the desired approach.

Ideally, new wallet plug-ins should be easy to develop and test, and common functionality should be implemented in a single codebase, shared between the plug-ins and Indy-sdk codebase.

# Tutorial
[tutorial]: #tutorial

The Postgres storage plug-in is based on the indy-sdk wallet plug-in storage design:

- https://github.com/hyperledger/indy-sdk/tree/master/doc/design/003-wallet-storage

This plug-in is implemented for a Postgres database, and the codebase is available in the following repository:

- https://github.com/ianco/indy-sdk/tree/postgres_plugin

## Installing and Testing the Postgres Plug-in

Before you can test the Postgres plug-in you need to have an Indy network running, as well as a local Postgres database.

You can startup an Indy network in many ways, for example as documented in the Indy-sdk README (https://github.com/hyperledger/indy-sdk#1-starting-the-test-pool-on-localhost)

```
cd indy-sdk
docker build -f ci/indy-pool.dockerfile -t indy_pool .
docker run -itd -p 9701-9708:9701-9708 indy_pool
```

You can startup a local Postgres database with the following command:

```
docker run --name some-postgres -e POSTGRES_PASSWORD=mysecretpassword -d -p 5432:5432 postgres -c 'log_statement=all' -c 'logging_collector=on' -c 'log_destination=stderr'
```

You should have two docker containers running - one for the Indy network and one for the Postgres database.

Note that with the above command (it starts the Postgres database in debug mode) you can monitor database command activity as follows:

```
# first get the id of the Postgres docker container
docker ps
# then connect to the Postgres container and watch the log file:
docker exec -it <container id> bash
# in the Postgres docker container run the following:
cd /var/lib/postgresql/data/log
tail -f <the latest postgres log file>
# you will see each SQL command executed
```

This is useful to see when the Indy-sdk unit tests are actually connecting to Postgres.

To build and run the Postgres plug-in:

- Clone (or fork and clone) the above repository
- Build each project (indy-sdk/libindy, indy-sdk/cli, indy-sdk/samples/storage/storage-postgres):

```
git clone https://github.com/ianco/indy-sdk.git
git checkout postgres_plugin
cd <to each project directory>
cargo build
```

To run the unit tests for the Postgres storage plug-in:

```
cd indy-sdk/samples/storage/storage-postgres
RUST_BACKTRACE=1 cargo test -- --nocapture --test-threads=1
```

## Running Indy-sdk Tests with the Postgres Plug-in

Note that the Postgres shared library is built in the "indy-sdk/samples/storage/storage-postgres/target/debug" directory - this directory needs to be added to the LD_LIBRARY_PATH environment variable in order to load this shared library.  You can set this variable globally ("export LD_LIBRARY_PATH=<path to shared lib>"), or it can be set when running each command.

Several environment variables have been setup to specify when the non-default wallet storage is to be used for unit tests:

| Variable | Value (e.g.) | Description |
|-|-|-|
| STG_CONFIG | {} | Configuration json to be passed to the plug-in |
| STG_CREDS | {} | Credentials json to be passed to the plug-in |
| STG_TYPE | postgres | Name of the storage plug-in type within Indy |
| STG_LIB | libindystrgpostgres.dylib | Name of the shared library |
| STG_FN_PREFIX | postgreswallet_fn_ | Prefix for all wallet API functions within the shared library |

Alternately, a shortcut is also available to default all of these parameters for the Postgres plug-in:

| Variable | Value (e.g.) | Description |
|-|-|-|
| STG_USE | postgres | Set all the above variables for the Postgres plug-in |

If none of these variables are specified, the tests will run against the default storage.

For example to run indy-sdk unit tests using the postgres wallet storage:

```
cd indy-sdk/libindy
export LD_LIBRARY_PATH=<path to shared lib>
RUST_BACKTRACE=1 STG_USE=postgres cargo test <test to run> -- --nocapture --test-threads=1
```

Sample test targets, that have been "shimmed" to understand plug-ins, include the following:

- dynamic_storage_cases - Tests that plug-ins can be loaded and executed
- wallet_tests - Unit tests for the wallet service, includes a large test suite for wallet search (which is currently not implemented within the plug-in unit tests)
- high_cases - Specifically for anoncreds and wallet - These are high-level tests within the "libindy/tests" directory

You can specify one of the above, or just run "STG_USE=postgres cargo test" to run *all* the tests.  If you monitor the Postgres database (as described above) you will see when a unit test interacts with the Postgres database.

Note that STG_USE in the above example is a shortcut for Postgres, you can also individually specify STG_CONFIG, STG_CREDS, STG_TYPE, etc.

## Running CLI with the Postgres Plug-in

The CLI in this repository has an additional command to load an external plug-in, and extra parameters to specify configuration and credentials when creating, opening and deleting a wallet:

```
indy> wallet register help
Command:
	wallet register - Register a new wallet storage type

Usage:
	wallet register <name-value> so_file=<so_file-value> [prefix=<prefix-value>]

Parameters are:
	name - The name of new wallet storage type
	so_file - Path to shared library file containing the storage plug-in
	prefix - (optional) Prefix for all exported functions within this plug-in

Examples:
	wallet register inmem so_file=inmem.so
	wallet register postgres so_file=postgres.so prefix=postgres_fn_

indy> wallet create help
Command:
	wallet create - Create new wallet and attach to Indy CLI

Usage:
	wallet create <name-value> key[=<key-value>] [key_derivation_method=<key_derivation_method-value>] [storage_type=<storage_type-value>] [storage_config=<storage_config-value>] [storage_credentials=<storage_credentials-value>]

Parameters are:
	name - Identifier of the wallet
	key - (leave empty for deferred input) Key or passphrase used for wallet key derivation.
                                               Look to key_derivation_method param for information about supported key derivation methods.
	key_derivation_method - (optional) Algorithm to use for wallet key derivation. One of:
                                    argon2m - derive secured wallet key (used by default)
                                    argon2i - derive secured wallet key (less secured but faster)
                                    raw - raw wallet key provided (skip derivation)
	storage_type - (optional) Type of the wallet storage.
	storage_config - (optional) The list of key:value pairs defined by storage type.
	storage_credentials - (optional) The list of key:value pairs defined by storage type.

Examples:
	wallet create wallet1 key
	wallet create wallet1 key storage_type=default
	wallet create wallet1 key storage_type=default storage_config={"key1":"value1","key2":"value2"}

indy>
```

To run a CLI demo using hte Postgres plug-in, there is a batch script which illustrates these commands:

```
cd indy-sdk/cli
RUST_BACKTRACE=1 LD_LIBRARY_PATH=../samples/storage/storage-postgres/target/debug/ cargo run ../samples/storage/storage-postgres/cli_ps_test.txt
```

This script dynamically loads the Postgres storage, creates and opens a wallet, creates a DID, and then closes and deletes the wallet.

# Reference
[reference]: #reference

Provide guidance for implementers, procedures to inform testing,
interface definitions, formal function prototypes, error codes,
diagrams, and other technical details that might be looked up.
Strive to guarantee that:

- Interactions with other features are clear.
- Implementation trajectory is well defined.
- Corner cases are dissected by example.

## Postgres Plug-in Design and Implementation

## Indy-sdk Testing Integration

- Unit test architecture (how to "shim" the postgres plug-in into unit tests)
    - can be used with any wallet (plug-in or not)
    - provides acceptance suite that storage implements design correctly

## CLI Integration

- Plug-in architecture (layers)
    - API layer and implementation layer
- Shared code (what are all the common components?)
    - indy-sdk dependencies
    - potential for shared rust library
- Database connection pools and storage iterators
    - share connections between threads
    - free database connections
- Search queries (marshalling and unmarshalling between Query operations and json)


# Drawbacks (and outstanding questions)
[drawbacks]: #drawbacks

Why should we *not* do this?

- Some issues with the current implementation:
- Sharing database connections in a multi-threaded environment
    - connections not being freed, implementation of storage iterator
- Shared codebase to facilitate development of storage plug-ins
    - wallet queries and unit testing search functions
- Updates to indy-sdk core code
    - public visibility
    - updates to plug-in/mod.rs

# Rationale and alternatives
[alternatives]: #alternatives

- Why is this design the best in the space of possible designs?
- What other designs have been considered and what is the rationale for not
choosing them?
- What is the impact of not doing this?

- TODO pending discussion of drawbacks/outstanding questions
- There is not a lot of support currently for developing storage plug-ins


# Prior art
[prior-art]: #prior-art

- Following existing storage plug-in design
- Existing plug-in is inmem-storage example, but it is not complete
   - Not in shared library (has been re-factored)
   - Does not implement search
   - No back-end database
   - Many unit tests fail ("STG_USE=inmem cargo test")
   - Etc.


Discuss prior art, both the good and the bad, in relation to this proposal.
A few examples of what this can include are:

- Does this feature exist in other SSI ecosystems and what experience have
their community had?
- For other teams: What lessons can we learn from other attempts?
- Papers: Are there any published papers or great posts that discuss this?
If you have some relevant papers to refer to, this can serve as a more detailed
theoretical background.

This section is intended to encourage you as an author to think about the
lessons from other implementers, provide readers of your proposal with a
fuller picture. If there is no prior art, that is fine - your ideas are
interesting to us whether they are brand new or if they are an adaptation
from other communities.

Note that while precedent set by other communities is some motivation, it
does not on its own motivate an enhancement proposal here. Please also take
into consideration that Indy sometimes intentionally diverges from common
identity features.

# Unresolved questions
[unresolved]: #unresolved-questions

- What parts of the design do you expect to resolve through the
enhancement proposal process before this gets merged?
- What parts of the design do you expect to resolve through the
implementation of this feature before stabilization?
- What related issues do you consider out of scope for this
proposal that could be addressed in the future independently of the
solution that comes out of this doc?
