Helm chart
==========

This is a summary of the Helm chart parameters that can be used the customise
the SDP deployment. The current default values can be found in the chart's
`values file`_.


Configuration database
----------------------

The configuration database is implemented on top of `etcd`_.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``etcd.image``
    - etcd container image
    - ``quay.io/coreos/etcd``
  * - ``etcd.version``
    - etcd container version
    - ``3.3.25``
  * - ``etcd.imagePullPolicy``
    - etcd container image pull policy
    - ``IfNotPresent``
  * - ``etcd.useOperator``
    - Use `etcd-operator`_ to deploy the etcd cluster (deprecated)
    - ``false``
  * - ``etcd.maxTxnOps``
    -  Maximum number of operations per transaction (not supported by etcd-operator)
    - ``1024``


Console
-------

The console provides a command-line interface to monitor and control the SDP by
interacting with the configuration database.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``console.enabled``
    - Enable the console
    - ``true``
  * - ``console.image``
    - Console container image
    - ``artefact.skao.int/ska-sdp-console``
  * - ``console.version``
    - Console container version
    - See `values file`_
  * - ``console.imagePullPolicy``
    - Console container image pull policy
    - ``IfNotPresent``


Operator web interface
----------------------

The operator web interface can be used to control and monitor the SDP by
interacting with the configuration database.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``opinterface.enabled``
    - Enable the operator web interface
    - ``true``
  * - ``opinterface.image``
    - Operator web interface container image
    - ``artefact.skao.int/ska-sdp-opinterface``
  * - ``opinterface.version``
    - Operator web interface container version
    - See `values file`_
  * - ``opinterface.imagePullPolicy``
    - Operator web interface container image pull policy
    - ``IfNotPresent``


Processing controller
---------------------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``proccontrol.image``
    - Processing controller container image
    - ``artefact.skao.int/ska-sdp-proccontrol``
  * - ``proccontrol.version``
    - Processing controller container version
    - See `values file`_
  * - ``proccontrol.imagePullPolicy``
    - Processing controller container image pull policy
    - ``IfNotPresent``


Workflows
---------

Workflow definitions to be used by SDP. These map the workflow type, ID and
version to a container image. By default the definitions are read from the
`science pipeline workflows repository`_ in GitLab. A different URL may be
specified. Alternatively a list of workflow definitions can be passed to the
chart.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``workflows.url``
    - URL from which to read the workflow definitions
    - ``https://gitlab.com/ska-telescope/sdp/ska-sdp-science-pipelines/-/raw/master/workflows.json``
  * - ``workflows.definitions``
    - List of workflow definitions. If present, used instead of the URL. See the example below
    - Not set

Example of workflow definitions in a values file:

.. code-block:: yaml

  workflows:
    definitions:
    - type: realtime
      id: test_realtime
      version: 0.2.2
      image: artefact.skao.int/ska-sdp-wflow-test-batch:0.2.2
    - type: batch
      id: test_realtime
      version: 0.2.2
      image: artefact.skao.int/ska-sdp-wflow-test-realtime:0.2.2


Helm deployer
-------------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``helmdeploy.image``
    - Helm deployer container image
    - ``artefact.skao.int/ska-sdp-helmdeploy``
  * - ``helmdeploy.version``
    - Helm deployer container version
    - See `values file`_
  * - ``helmdeploy.imagePullPolicy``
    - Helm deployer container image pull policy
    - ``IfNotPresent``
  * - ``helmdeploy.namespace``
    - Namespace for SDP dynamic deployments
    - ``sdp``
  * - ``helmdeploy.prefix``
    - Prefix for Helm release names
    - ``''``
  * - ``helmdeploy.createNamespace``
    - Create the namespace for dynamic deployments
    - ``false``
  * - ``helmdeploy.createClusterRole``
    - Create a cluster role to allow dynamic deployments to create persistent volumes
    - ``false``
  * - ``helmdeploy.chart_repo.url``
    - Chart repository URL
    - ``https://gitlab.com/ska-telescope/sdp/ska-sdp-helmdeploy-charts/-/raw/master/chart-repo/``
  * - ``helmdeploy.chart_repo.refresh``
    - Chart repository refresh interval (in seconds)
    - ``300``


LMC (Tango devices)
-------------------

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``lmc.enabled``
    - Enable the LMC. If set to ``false``, the SDP will run in headless mode
    - ``true``
  * - ``lmc.image``
    - LMC container image
    - ``artefact.skao.int/ska-sdp-lmc``
  * - ``lmc.version``
    - LMC container version
    - See `values file`_
  * - ``lmc.imagePullPolicy``
    - LMC container image pull policy
    - ``IfNotPresent``
  * - ``lmc.allCommandsHaveArgument``
    - Enable all Tango device commands to receive a transaction ID
    - ``false``
  * - ``lmc.prefix``
    - Telescope prefix for Tango device names (e.g. ``low`` or ``mid``)
    - ``test``
  * - ``lmc.nsubarray``
    - Number of subarrays to deploy
    - ``1``


Tango infrastructure
--------------------

Parameters for the ska-tango-base subchart and Tango dsconfig. The
ska-tango-base subchart must be enabled to support the Tango devices when
running the SDP stand-alone.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``ska-tango-base.enabled``
    - Enable the ska-tango-base subchart
    - ``true``
  * - ``ska-tango-base.itango.enabled``
    - Enable the itango console in the ska-tango-base subchart
    - ``false``
  * - ``dsconfig.image.*``
    - Tango dsconfig container image settings
    - See `values file`_


Proxy settings
--------------

Proxy settings are applied to the components that retrive configuration data
via HTTPS: the workflow definitions and the Helm charts.

.. list-table::
  :widths: auto
  :header-rows: 1

  * - Parameter
    - Description
    - Default
  * - ``proxy.server``
    - Address of proxy server
    - Not set
  * - ``proxy.noproxy``
    - List of addresses or subnets for which the proxy should not be used
    - Not set

Example of proxy settings in a values file:

.. code-block:: yaml

  proxy:
    server: http://proxy.mydomain
    noproxy:
    - 192.168.0.1
    - 192.168.0.2


.. _values file: https://gitlab.com/ska-telescope/sdp/ska-sdp-integration/-/blob/master/charts/ska-sdp/values.yaml
.. _etcd: https://etcd.io
.. _etcd-operator: https://github.com/coreos/etcd-operator
.. _science pipeline workflows repository: https://gitlab.com/ska-telescope/sdp/ska-sdp-science-pipelines
