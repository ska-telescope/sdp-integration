.. _running_standalone:

Running the SDP stand-alone
===========================

Before running the SDP, your local development environment needs to be set up.
Details can be found in the :ref:`requirements <running_requirements>` section.

Create the namespace for SDP workflows
--------------------------------------

The SDP deploys its workflows and their execution engines into a separate
Kubernetes namespace from the controllers. Before deploying the SDP you need to
create this namespace, which by default is called ``sdp``:

.. code-block:: console

    $ kubectl create namespace sdp

Deploying the SDP
-----------------

Releases of the SDP Helm chart are published in the SKA artefact repository. To
install the released version, you need to add this chart repository to helm:

.. code-block:: console

    $ helm repo add ska https://artefact.skao.int/repository/helm-internal

The chart can be installed with the command (assuming the release name is ``test``):

.. code-block:: console

    $ helm install test ska/ska-sdp

You can watch the deployment in progress using ``kubectl``:

.. code-block:: console

    $ kubectl get pod --watch

or the ``k9s`` terminal-based UI (recommended):

.. code-block:: console

    $ k9s

Wait until all the pods are running:

.. code-block:: console

     default      databaseds-tango-base-test-0  ●  1/1          0 Running    172.17.0.12     m01   119s
     default      sdp-console-0                 ●  1/1          0 Running    172.17.0.15     m01   119s
     default      sdp-etcd-0                    ●  1/1          0 Running    172.17.0.6      m01   119s
     default      sdp-helmdeploy-0              ●  1/1          0 Running    172.17.0.14     m01   119s
     default      sdp-lmc-configuration-6vbtr   ●  0/1          0 Completed  172.17.0.11     m01   119s
     default      sdp-lmc-master-0              ●  1/1          0 Running    172.17.0.9      m01   119s
     default      sdp-lmc-subarray-01-0         ●  1/1          0 Running    172.17.0.10     m01   119s
     default      sdp-opinterface-0             ●  1/1          0 Running    172.17.0.13     m01   119s
     default      sdp-proccontrol-0             ●  1/1          0 Running    172.17.0.4      m01   119s
     default      sdp-wf-configuration-2hpdn    ●  0/1          0 Completed  172.17.0.5      m01   119s
     default      ska-tango-base-tangodb-0      ●  1/1          0 Running    172.17.0.8      m01   119s

You can check the logs of pods to verify that they are doing okay:

.. code-block:: console

    $ kubectl logs <pod_name>

For example:

.. code-block:: console

    $ kubectl logs sdp-lmc-subarray-01-0
    ...
    1|2021-05-25T11:32:53.161Z|INFO|MainThread|init_device|subarray.py#92|tango-device:test_sdp/elt/subarray_1|SDP Subarray initialising
    ...
    1|2021-05-25T11:32:53.185Z|INFO|MainThread|init_device|subarray.py#127|tango-device:test_sdp/elt/subarray_1|SDP Subarray initialised
    ...
    $ kubectl logs sdp-proccontrol-0
    1|2021-05-25T11:32:32.423Z|INFO|MainThread|main_loop|processing_controller.py#180||Connecting to config DB
    1|2021-05-25T11:32:32.455Z|INFO|MainThread|main_loop|processing_controller.py#183||Starting main loop
    1|2021-05-25T11:32:32.566Z|INFO|MainThread|main_loop|processing_controller.py#190||processing block ids []
    ...

If it looks like this, there is a good chance everything has been deployed correctly.

Testing it out
--------------

Connecting to the configuration database
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``ska-sdp`` chart deploys a 'console' pod which enables you to interact with the
configuration database. You can start a shell in the pod by doing:

.. code-block:: console

    $ kubectl exec -it sdp-console-0 -- bash

This will allow you to use the ``ska-sdp`` command:

.. code-block:: console

    # ska-sdp list -a
    Keys with prefix /:
    /master
    /subarray/01
    /workflow/batch:batch_imaging:0.1.0
    /workflow/batch:batch_imaging:0.1.1
    ...

Which shows that the configuration contains the state of the Tango devices and
the workflow definitions.

Details about the existing commands of the ``ska-sdp`` utility can be found in the
`CLI to interact with SDP <https://developer.skao.int/projects/ska-sdp-config/en/latest/cli.html>`_
section in the SDP Configuration Library documentation.

Starting a workflow
^^^^^^^^^^^^^^^^^^^

Assuming the configuration is prepared as explained in the previous
section, we can now add a processing block to the configuration:

.. code-block:: console

    # ska-sdp create pb <workflow_type>:<workflow_id>:<workflow_version>

For example

.. code-block:: console

    # ska-sdp create pb batch:test_dask:0.2.6
    Processing block created with pb_id: pb-sdpcli-20210802-00000

Note - the ska-sdp command can only create a PB with a batch workflow.
A real-time PB must be linked to a Scheduling Block Instance (SBI), and
there is currently no way to do that using ska-sdp. A PB with a real-time
workflow can only be created using the iTango interface.

The processing block is created with the ``/pb`` prefix in the
configuration:

.. code-block:: console

    # ska-sdp list -v pb
    Keys with prefix /pb:
    /pb/pb-sdpcli-20210802-00000 = {
      "dependencies": [],
      "id": "pb-sdpcli-20210802-00000",
      "parameters": {},
      "sbi_id": null,
      "workflow": {
        "id": "test_dask",
        "type": "batch",
        "version": "0.2.6"
      }
    }
    /pb/pb-sdpcli-20210802-00000/owner = {
      "command": [
        "test_dask.py",
        "pb-sdpcli-20210802-00000"
      ],
      "hostname": "proc-pb-sdpcli-20210802-00000-workflow-mvdnk",
      "pid": 1
    }
    /pb/pb-sdpcli-20210802-00000/state = {
      "deployments": {
        "proc-pb-sdpcli-20210802-00000-dask-1": "RUNNING",
        "proc-pb-sdpcli-20210802-00000-dask-2": "RUNNING"
      },
      "resources_available": true,
      "status": "RUNNING"
    }

The processing block is detected by the processing controller which
deploys the workflow. The workflow in turn deploys the execution engines
(in this case, Dask). The deployments are requested by creating entries
with ``/deploy`` prefix in the configuration, where they are detected by
the Helm deployer which actually makes the deployments:

.. code-block:: console

    # ska-sdp list -v deployment
    Keys with prefix /deploy:
    /deploy/proc-pb-sdpcli-20210802-00000-dask-1 = {
      "args": {
        "chart": "dask",
        "values": {
          "image": "artefact.skao.int/ska-sdp-wflow-test-dask:0.2.6",
          "worker.replicas": 2
        }
      },
      "id": "proc-pb-sdpcli-20210802-00000-dask-1",
      "type": "helm"
    }
    /deploy/proc-pb-sdpcli-20210802-00000-dask-2 = {
      "args": {
        "chart": "dask",
        "values": {
          "image": "artefact.skao.int/ska-sdp-wflow-test-dask:0.2.6",
          "worker.replicas": 2
        }
      },
      "id": "proc-pb-sdpcli-20210802-00000-dask-2",
      "type": "helm"
    }
    /deploy/proc-pb-sdpcli-20210802-00000-workflow = {
      "args": {
        "chart": "workflow",
        "values": {
          "env": {
            "SDP_CONFIG_HOST": "sdp-etcd-client.default.svc.cluster.local",
            "SDP_HELM_NAMESPACE": "sdp"
          },
          "pb_id": "pb-sdpcli-20210802-00000",
          "wf_image": "artefact.skao.int/ska-sdp-wflow-test-dask:0.2.6"
        }
      },
      "id": "proc-pb-sdpcli-20210802-00000-workflow",
      "type": "helm"
    }

The deployments associated with the processing block have been created
in the ``sdp`` namespace, so to view the created pods we have to ask as
follows (on the host):

.. code-block:: console

    $ kubectl get pod -n sdp
    NAME                                                              READY   STATUS    RESTARTS   AGE
    proc-pb-sdpcli-20210802-00000-dask-1-scheduler-6d84584948-t5kzz   1/1     Running   0          30s
    proc-pb-sdpcli-20210802-00000-dask-1-worker-5b568bb45b-7jcsr      1/1     Running   0          30s
    proc-pb-sdpcli-20210802-00000-dask-1-worker-5b568bb45b-rfxvs      1/1     Running   0          30s
    proc-pb-sdpcli-20210802-00000-dask-2-scheduler-5f6dfc6d56-r4rt5   1/1     Running   0          29s
    proc-pb-sdpcli-20210802-00000-dask-2-worker-78cd65b78f-dqkp4      1/1     Running   0          29s
    proc-pb-sdpcli-20210802-00000-dask-2-worker-78cd65b78f-jxbjz      1/1     Running   0          29s
    proc-pb-sdpcli-20210802-00000-workflow-mvdnk                      1/1     Running   0          33s

Cleaning up
^^^^^^^^^^^

Finally, let us remove the processing block from the configuration (in the SDP
console shell):

.. code-block:: console

    # ska-sdp delete pb pb-sdpcli-20210802-00000
    /pb/pb-sdpcli-20210802-00000
    /pb/pb-sdpcli-20210802-00000/state
    Deleted above keys with prefix /pb/pb-sdpcli-20210802-00000.

If you re-run the commands from the last section you will notice that
this correctly causes all changes to the cluster configuration to be
undone as well.

Accessing the Tango interface
-----------------------------

By default, the ``ska-sdp`` chart does not deploy the iTango shell pod from the
``ska-tango-base`` chart. To enable it, you can upgrade the release with:

.. code-block:: console

    $ helm upgrade test ska/ska-sdp --set ska-tango-base.itango.enabled=true

Then you can start an iTango session with:

.. code-block:: console

    $ kubectl exec -it ska-tango-base-itango-console -- itango3

You should be able to list the Tango devices:

.. code-block:: python

    In [1]: lsdev
    Device                                   Alias                     Server                    Class
    ---------------------------------------- ------------------------- ------------------------- --------------------
    test_sdp/elt/master                                                SDPMaster/0               SDPMaster
    test_sdp/elt/subarray_1                                            SDPSubarray/01            SDPSubarray
    sys/access_control/1                                               TangoAccessControl/1      TangoAccessControl
    sys/database/2                                                     DataBaseds/2              DataBase
    sys/rest/0                                                         TangoRestServer/rest      TangoRestServer
    sys/tg_test/1                                                      TangoTest/test            TangoTest

This allows direct interaction with the devices, such as querying and
changing attributes and issuing commands:

.. code-block:: python

    In [2]: d = DeviceProxy('test_sdp/elt/subarray_1')

    In [3]: d.state()
    Out[3]: tango._tango.DevState.OFF

    In [4]: d.On()

    In [5]: d.state()
    Out[5]: tango._tango.DevState.ON

    In [6]: d.obsState
    Out[6]: <obsState.EMPTY: 0>

    In [7]: config_sbi = '''
        ...: {
        ...:   "id": "sbi-test-20210525-00000",
        ...:   "max_length": 21600.0,
        ...:   "scan_types": [
        ...:     {
        ...:       "id": "science",
        ...:       "channels": [
        ...:         {"count": 5, "start": 0, "stride": 2, "freq_min": 0.35e9, "freq_max": 0.358e9, "link_map": [[0,0], [200,1]]}
        ...:       ]
        ...:     }
        ...:   ],
        ...:   "processing_blocks": [
        ...:     {
        ...:       "id": "pb-test-20210525-00000",
        ...:       "workflow": {"type": "realtime", "id": "test_realtime", "version": "0.2.4"},
        ...:       "parameters": {}
        ...:     },
        ...:     {
        ...:       "id": "pb-test-20210525-00001",
        ...:       "workflow": {"type": "realtime", "id": "test_receive_addresses", "version": "0.3.6"},
        ...:       "parameters": {}
        ...:     },
        ...:     {
        ...:       "id": "pb-test-20210525-00002",
        ...:       "workflow": {"type": "batch", "id": "test_batch", "version": "0.2.4"},
        ...:       "parameters": {},
        ...:       "dependencies": [
        ...:         {"pb_id": "pb-test-20210525-00000", "type": ["visibilities"]}
        ...:       ]
        ...:     },
        ...:     {
        ...:       "id": "pb-test-20210525-00003",
        ...:       "workflow": {"type": "batch", "id": "test_dask", "version": "0.2.5"},
        ...:       "parameters": {},
        ...:       "dependencies": [
        ...:         {"pb_id": "pb-test-20210525-00002", "type": ["calibration"]}
        ...:       ]
        ...:     }
        ...:   ]
        ...: }
        ...: '''

    In [8]: d.AssignResources(config_sbi)

    In [9]: d.obsState
    Out[9]: <obsState.IDLE: 0>

    In [10]: d.Configure('{"scan_type": "science"}')

    In [11]: d.obsState
    Out[11]: <obsState.READY: 2>

    In [12]: d.Scan('{"id": 1}')

    In [13]: d.obsState
    Out[13]: <obsState.SCANNING: 3>

    In [14]: d.EndScan()

    In [15]: d.obsState
    Out[15]: <obsState.READY: 2>

    In [16]: d.End()

    In [17]: d.obsState
    Out[17]: <obsState.IDLE: 0>

    In [18]: d.ReleaseResources()

    In [19]: d.obsState
    Out[19]: <obsState.EMPTY: 0>

    In [20]: d.Off()

    In [21]: d.state()
    Out[21]: tango._tango.DevState.OFF

More details about each of the SDP Subarray commands can be found `here
<https://developer.skao.int/projects/ska-sdp-lmc/en/latest/sdp_subarray.html>`_

Removing the SDP
----------------

To remove the SDP deployment from the cluster, do:

.. code-block:: console

    $ helm uninstall test

Developing the SDP chart
------------------------

If you want to install the chart from the source code in the SDP Integration
repository, for instance if you are developing a new version, then you can do
it like this:

.. code-block:: console

    $ helm install --dependency-update test charts/ska-sdp

The ``--dependency-update`` flag downloads the ``ska-tango-base`` chart on
which the ``ska-sdp`` chart depends.

Developing SDP Workflows
------------------------

Instructions on how to develop and test SDP workflows can be found in the
`Science Pipeline Workflows
<https://developer.skao.int/projects/ska-sdp-science-pipelines/en/latest/index.html>`_ documentation.
