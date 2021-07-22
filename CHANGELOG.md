# Changelog

## 0.7.0

* Rename chart to ska-sdp.
* Update components to use images from the central artefact repository:
  - LMC 0.17.2
  - Console 0.3.1
  - Operator interface 0.2.1
  - Processing controller 0.10.1
  - Helm deployer 0.9.1

## 0.6.1

* Update Tango base chart dependency to ska-tango-base 0.2.23.
* Remove time-to-live settings from configuration jobs so they are not deleted
  on Kubernetes 1.21.

## 0.6.0

* Update LMC to 0.17.1. This adds support for version 0.3 of the command
  interface schemas. Support for version 0.2 is retained for backwards
  compatibility.

## 0.5.0

* Add operator web interface, version 0.2.0.
* Update console to 0.3.0. This makes the new ska-sdp command-line interface
  available.
* Update processing controller to 0.10.0. This reads the workflow definitions
  from the configuration database.
* Add Job to import the workflow definitions into the configuration database.
* Update Helm deployer to 0.9.0. This uses a configuration watcher in the main
  loop and improves the handling of temporary YAML files.
* Reduce size of component Docker images by using slim Python base image.

## 0.4.1

* Update Helm deployer to 0.8.0. Values to pass to a Helm chart are now written
  to a temporary YAML file. This allows hierarchical structures in the values to
  be passed to the charts.
* Update processing controller to 0.9.0. This is needed to work with the new
  version of the Helm deployer.
* Update console to 0.2.1. This updates the software versions installed in this
  component.

## 0.4.0

* Add parameters to set the telescope prefix in Tango device names and the
  number of subarrays to be deployed.
* Update tango-base subchart to 0.2.16.

## 0.3.7

* Update LMC to 0.16.2. This implements ADR-22 (versioning of JSON schemas) in
  the subarray device. Only the latest version of the interface (0.2) is
  supported by the AssignResources and Configure commands.

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
