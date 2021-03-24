Helm chart
==========

This is a summary of the Helm chart values that can be used the customise the
SDP deployment. The current default values can be found in the chart's `values
file`_.


Configuration database
----------------------

The configuration database is implemented on top of `etcd`_.

========================  =======================  ===========
Value                     Default                  Description
========================  =======================  ===========
``etcd.image``            ``quay.io/coreos/etcd``  etcd image
``etcd.version``          ``3.3.25``               etcd version
``etcd.imagePullPolicy``  ``IfNotPresent``         etcd image pull policy
``etcd.useOperator``      ``false``                Use `etcd-operator`_ to deploy the etcd cluster (deprecated)
``etcd.maxTxnOps``        ``1024``                 Maximum number of operations per transaction (not supported by etcd-operator)
========================  =======================  ===========


Processing controller
---------------------

=================================  ==============================================================================================  ===========
Value                              Default                                                                                         Description
=================================  ==============================================================================================  ===========
``proccontrol.image``              ``nexus.engageska-portugal.pt/sdp-prototype/ska-sdp-proccontrol``                               Processing controller image
``proccontrol.version``            (see `values file`_)                                                                            Processing controller version
``proccontrol.imagePullPolicy``    ``IfNotPresent``                                                                                Processing controller image pull policy
``proccontrol.workflows.url``      ``https://gitlab.com/ska-telescope/sdp/ska-sdp-science-pipelines/-/raw/master/workflows.json``  Workflow list URL
``proccontrol.workflows.refresh``  ``300``                                                                                         Workflow list refresh interval (in seconds)
=================================  ==============================================================================================  ===========


Helm deployer
-------------

=================================  ===========================================================================================  ===========
Value                              Default                                                                                      Description
=================================  ===========================================================================================  ===========
``helmdeploy.image``               ``nexus.engageska-portugal.pt/sdp-prototype/ska-sdp-helmdeploy``                             Helm deployer image
``helmdeploy.version``             (See `values file`_)                                                                         Helm deployer version
``helmdeploy.imagePullPolicy``     ``IfNotPresent``                                                                             Helm deployer image pull policy
``helmdeploy.namespace``           ``sdp``                                                                                      Namespace for SDP dynamic deployments
``helmdeploy.prefix``              ``''``                                                                                       Prefix for Helm release names
``helmdeploy.createNamespace``     ``false``                                                                                    Create the namespace for dynamic deployments
``helmdeploy.createClusterRole``   ``false``                                                                                    Create a cluster role to allow dynamic deployments to create persistent volumes
``helmdeploy.chart_repo.url``      ``https://gitlab.com/ska-telescope/sdp/ska-sdp-helmdeploy-charts/-/raw/master/chart-repo/``  Chart repository URL
``helmdeploy.chart_repo.refresh``  ``300``                                                                                      Chart repository refresh interval (in seconds)
=================================  ===========================================================================================  ===========


LMC (Tango devices)
-------------------

===============================  =========================================================  ===========
Value                            Default                                                    Description
===============================  =========================================================  ===========
``lmc.image``                    ``nexus.engageska-portugal.pt/sdp-prototype/ska-sdp-lmc``  LMC image
``lmc.version``                  (see `values file`_)                                       LMC version
``lmc.imagePullPolicy``          ``IfNotPresent``                                           LMC image pull policy
``lmc.enabled``                  ``true``                                                   Enable the LMC. If set to false, the SDP will run in headless mode
``lmc.allCommandsHaveArgument``  ``false``                                                  Enable all Tango device commands to receive a transaction ID
``lmc.prefix``                   ``test``                                                   Telescope prefix for Tango device names (e.g. ``low`` or ``mid``)
``lmc.nsubarray``                ``1``                                                      Number of subarrays to deploy
===============================  =========================================================  ===========


Tango infrastructure
--------------------

Values for the tango-base subchart and Tango dsconfig. The tango-base subchart
needs to be enabled to support the Tango devices when running the SDP
stand-alone.

=============================  ==========================================  ===========
Value                          Default                                     Description
=============================  ==========================================  ===========
``tango-base.enabled``         ``true``                                    Enable the tango-base subchart
``dsconfig.image.registry``    ``nexus.engageska-portugal.pt/ska-docker``  Tango dsconfig registry
``dsconfig.image.image``       ``tango-dsconfig``                          Tango dsconfig image
``dsconfig.image.tag``         ``1.5.0``                                   Tango dsconfig version
``dsconfig.image.pullPolicy``  ``IfNotPresent``                            Tango dsconfig image pull policy
=============================  ==========================================  ===========


Proxy settings
--------------

Proxy settings are applied to the processing controller and Helm deployer,
which use HTTPS to retrieve the workflow list and Helm charts, respectively.

=================  =======  ===========
Value              Default  Description
=================  =======  ===========
``proxy.server``   Not set  Address of proxy server
``proxy.noproxy``  Not set  List of addresses or subnets for which the proxy should not be used
=================  =======  ===========


.. _values file: https://gitlab.com/ska-telescope/sdp/ska-sdp-integration/-/blob/master/charts/sdp/values.yaml
.. _etcd: https://etcd.io
.. _etcd-operator: https://github.com/coreos/etcd-operator
