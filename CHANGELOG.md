# Changelog

## 0.3.6

* Update LMC to 0.16.1. This works around a problem in the etcd interface which
  could block the event loop and prevent it from updating the device
  attributes.

## 0.3.5

* Update processing controller to 0.8.0. This resolves the transaction
  operation limit problem in the main loop.

## 0.3.4

* Update LMC to 0.16.0. This enables log messages to be written to the Tango
  logging system in addition to the standard output.

## 0.3.3

* Update Helm deployer to 0.7.2. This enables it to use a prefix for chart
  releases. This is intended to enable deployment of the SDP in a single
  namespace for testing purposes.
* Add option for setting the Helm deployer release prefix.

## 0.3.2

* Update URLs for new repository locations.

## 0.3.1

* Fix Helm deployer chart repository environment variable.

## 0.3.0

* Update LMC to 0.15.0. This adds transaction IDs to commands.
* Add option to enable passing a transaction ID to all commands. By default it
  is only enabled on commands that previously accepted arguments, to avoid
  changing the argument type on the other commands.

## 0.2.1

* Update LMC to 0.14.2. This correctly configures the Tango device attributes
  to use change events. This also stores the master device state in the
  configuration database.

## 0.2.0

* Remove dependency on the etcd-operator chart. Add option to enable the use of
  etcd-operator if it is available.
* Add option to set the etcd transaction operation limit. This is not supported
  by etcd-operator.
* Disable the Helm deployer ClusterRole (used to manage persistent volumes) by
  default. Add option to re-enable it if needed.
* Update tango-base subchart to 0.2.8.

## 0.1.0

* Initial release of sdp chart.
