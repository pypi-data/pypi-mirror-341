# Breaking Version Changes

## 15.0.0

### sqlalchemy update

A full sqlalchemy migration guide can be found [here](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#sqlalchemy-2-0-major-migration-guide).
Many things could be changed to new API however are not necessary. This includes e.g. completely changing from .query() to 2.0 style.

However, the newer sqlalchemy version (2.0.x) has many breaking changes. Most regularly encountered are:
* declarative_base() is now in `sqlalchemy.orm` instead of `sqlalchemy.ext.declarative`
* `session.query(Model).get(primary_key)` is replaced with `session.get(Model, primary_key)`
* `__allow_unmapped__ = True` might be necessary for relationships: [docs](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-to-2-0-step-six-add-allow-unmapped-to-explicitly-typed-orm-models)

For complex services it's advised to first migrate to 1.4.x where you can run with env `RemovedIn20Warning=1` ([docs](https://docs.sqlalchemy.org/en/20/changelog/migration_20.html#migration-to-2-0-step-two-turn-on-removedin20warnings))

### Schedule library update

* removed dependency on arivo.schedule by copying the code into openmodule replace
  * `import schedule` with `import openmodule.utils.schedule as schedule`
  * `from openmodule.utils.schedule import ...` instead of `from schedule import ...`

### PyYaml update
* `yaml.load` now requires a `Loader` argument (only warning before)

## 14.0.0
* sentry_sdk version was updated
* redis was removed
* The `RPCServer` does no longer call `os._exit` if `"status"` is in the handler return value.
It raises a `ValueError` instead.
* The `init_openmodule` now takes a sentry `dsn` as an argument. This is required if sentry is enabled 
(is enabled by default if not `TESTING` and not `DEBUG`).
* The `receive_message_from_socket` is now a context manager and should be used with a `with` statement.
This was done, so that any received zmq message automatically continues an existing sentry trace.
  * Example: `with receive_message_from_socket(socket) as (topic, message):`

## 13.6.0
* messaging:
  * the `get_pub_socket` now raises an AssertionError because we no longer support multiple publishers. 
    This was done because pub sockets receive all subscriptions and queue them until the next message is sent.
    This can lead to a memory leak.
* logging:
  * logs will now be written to stdout instead of stderr

## 13.5.0:
* changes in env.py of alembic: <br>
  `from openmodule.database.database import run_env_py` -> <br> 
  `from openmodule.database.migration import run_env_py`

## 13.0.0
* access_service:
  * changes in AccessCheckAccess (removed media field) and AccessCheckResponse (removed error field)
  * the class `AccessServiceWithDatabase` was removed and the Access Service now provides some commonly used functions
  * the class variable `auth_request_request_model` was removed
* kv_store:
  * the `run()` and `run_as_thread()` methods were removed from the `KVStore` class and where migrated to the
    `KVStoreHandler` class
  *  every `KVStore` now has to be added to the `KVStoreHandler` class

## 12.0.0
* topics and rpc-channels must be strings and cannot be bytes anymore
* access_service: 
  * removed parking_area_id and cost_entries from AccessCheckAccess
  * changed init parameters of AccessServiceWithDatabase
  * check_accesses_valid_at_gate adapted to new behavior
* kv_store:
  * removed debug_entries
* settings_provider
  * use result type from settings-models and added optional alternative type
  * removed get_no_exception and get_many_no_exception
* openmodule-test
  * Changed settings syntax in SettingsMocker

## 11.0.0

* MediumType copied from backend.py to vehicle.py as backend.py will be removed in the future
* `prep_upgrade()` was removed.
* return type of topics changed from bytes to string which might break code, especially in tests
* RPCClient refactor: Changed functions and error handling
* fix for freezgun's FakeDatetime cannot be serialized (only for settings.TESTING=True)
* changed usage of InterruptTestMixin.signal_in_function

### Connection Listener:

* `ConnectionStatus` now consists of 4 states (startup, online, shutdown, offline) instead of a boolean.
* `ConnectionStatusListener` should not be created by services anymore, an instance of the class now runs in the
  internal thread instead (`core.connection_listener`).
* It has no callback anymore. Instead, the service should check the status with
  `core.connection_listener.get() -> ConnectionStatus` and react accordingly, or use the
  `core.connection_listener.wait_for_change(timeout=None) -> bool` method.

### Package Reader:

* The `PackageReader` refactored. It now requires a `service-misc` to be running on the system.
* The reader's methods have been renamed and always return the config and the parent package.

### Health

* The core no longer uses a (possible) provided health_handler, use the new [health framework](./health.md)
* The core now sends responses to `healthz` ping messages to the topic `healthpong` instead of `healthz`


## 10.0.4

* removed some fields in session message definitions used in backend

## 10.0.2

If you are using backends and want to support the new parking logic version, please check in and out handlers for the
new session start and finish message. These are separate to the old check in and out messages.

If you do not add support, your backend will raise a `NotImplementedError` when you try to use the new parking logic. If
you use an old openmodule version (< 10.0.2) with the new parking logic, you will get no check in and out events!

```python
class MyBackend(Backend):
    def check_in_session(self, message: SessionStartMessage):
        ...

    def check_out_session(self, message: SessionFinishMessage):
        ... 
  ```

## 10.0.1

Deprecation warning: `prep_upgrade()` is deprecated and will be removed in 11.0.0.

## 10.0.0

### Testcases:

* The `MockEvent.wait_for_call` method now requires arguments to be named explicitly
* The `openmodule_test.io` module was renamed to `openmodule_test.io_simulator`

### Presence Listener:

Event constraints (changed slightly to previous versions):

* For every enter a leave is sent. The vehicle_id of enter and leave always matches!
* There is never a vehicle is present on enter and backward (ensured by faking leave in case there is a lingering
  vehicle)

There are no further constraints, especially there might be no forward/backward for a vehicle!  
Therefore you must not rely on forward/backward to free up memory, instead use leave for cleanup! If you need some data
until forward/backward, you have to cleanup this data even if no forward/backward occurs. Also keep in mind that another
enter and even leave events might happen before the forward/backward of the last vehicle.

### Privacy

* session_id in AnonymizeMessage is now optional

## 9.0.0

This version refactored the RPC client, especially asynchronous retrieval of rpc results. See
the [RPC Documentation](./rpc.md) for more information about asynchronous rpc calls and the RPC Client. Critically the
common issue of "cannot do RPC's while inside an RPC handler" has been solved by creating a dedicated thread for the rpc
client and some future openmodule core internals which should not be blocked by badly behaving user code anyways.

* the `RPCClient.check_results()` function was removed, and is replaced by a `.result()`.
* The RPCClient together with the HealthHandler how has a dedicated thread in the open module core. It is discouraged to
  create an rpc client of your own. Please use the rpc client of openmodule core. A deprecation warning hints this also.

Also some things have been deprecated and will be removed

* the RPC Server no longer requires a config object to be passed. It takes the global openmodule settings instead.
* the RPC Client now warns if a `OpenModuleCore` is passed to it's constructor
* the RPC Client now warns if a dictionary is used for RPC requests
* MockEvent's `reset_call_count()` and `reset_all_call_counts()` was replaced by analog `reset_mock()`
  and `reset_all_mocks()`

Furthermore, fields were renamed in python (with aliases, so the serialized version stays the same):

* `Backend -> AccessRequest: id -> medium_id`
* `Backend -> MediumAccesses: id -> medium_id, type -> medium_type`
* `Backend -> CountMessage: id -> medium_id`
* `Backend -> CountMessage: previous_id ->  previous_medium_id`

In the backend test utils the `create_access_request()` method was removed.

The default value for `match_type` in `MessageDispatcher.register_handler` is now `True`.

`filter` in MessageDispatcher.register_handler is now a callable. Passing a dict will crash.

The `api` class, aswell as the test utils were removed from the framework. You can still find it
in [docs/deprecated_code/api](./deprecated_code/README.md) if you used it in your service.

## 8.1.1

This version includes breaking changes for testcases only.

* The main test mixin was refactored and `exception_in_function` was removed.

## 8.0.0

* Drops support for python 3.7

## 7.0.0

* Removed all support for direct config changes in all test classes. Now everything is controlled by the lazy settings.

## 6.1.6

* Removed redis_kv from Version 6.1.5

## 6.1.2

* Please add the following snippet to your `tox.ini`, before `[testenv:clean]`.
  ```
  [testenv:openmodule_test]
  deps =
  skip_install = true
  changedir = {toxinidir}/src
  whitelist_externals = bash
  commands = bash -c 'if grep -ri "openmodule_test" . ; then echo ; echo "You must not import openmodule_test inside the openmodule project!" ; echo ; exit 1; else exit 0 ; fi'
  ```
* SETTINGS_MODULE now needs a module instead of a path

## 6.1.0

* The new lazy settings need a `src/config.py` file or you need to set the `SETTINGS_MODULE` environment variable to a
  module

## 6.0.0

* All `OpenModuleModel` fields of type `datetime` require a timezone validator which is checked during testing /
  debugging. After this version **all datetime objects should be timezone naive**.
* All sqlalchemy database models disallow the use of `DateTime` and require the use of `TZDateTime`. This preemptively
  avoids bugs, because sqlalchemy with sqlite looses timezone information.
* `models.backend.Access` now uses timezone naive datetimes instead of timezone aware datetimes. The `is_valid` method
  still accepts both.
* in MessageDispatcher `raise_validation_errors` and `raise_handler_errors` are now required to be named arguments
* `MockEvent.wait_for_call()` now raises a Timeout error instead of an assertion error

## 5.0.0

* AlertHandler.send() and get_or_add_alert_id() were refactored:
    * `source` is now a keyword argument, with default value `""`
    * most arguments are forced to keyword arguments

## 4.0.0

* the Category Enum was renamed to AccessCategory
* all member variables of Category/AccessCategory are lowercased
* the Medium Enum was renamed to MediumType
* all member variables of Medium/MediumType are lowercased
* the default database folder changed to a mounted volume

## 3.0.0

* the registration of bases for the database changed from `register_bases([...])` to `run_env_py([...])`

## 2.0.0

* Pydantic models are now defined in a model folder
