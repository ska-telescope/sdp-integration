# Running the SDP stand-alone

## Create the namespace for SDP workflows

The SDP deploys its workflows and their execution engines into a separate
Kubernetes namespace from the controllers. Before deploying the SDP you need to
create this namespace, which by default is called `sdp`:

```console
$ kubectl create namespace sdp
```

## Deploying the SDP

Releases of the SDP Helm chart are published in the EngageSKA Nexus repository.
To install the released version, you need to add this chart repository to helm:

```console
$ helm repo add ska https://nexus.engageska-portugal.pt/repository/helm-chart
```

The chart can be installed with the command (assuming the release name is `test`):

```console
$ helm install test ska/sdp
```

You can watch the deployment in progress using `kubectl`:

```console
$ kubectl get pod --watch
```


You can check the logs of pods to verify that they are doing okay:

```console
$ kubectl logs sdp-lmc-subarray-1-0
...
1|2020-11-04T20:05:03.615Z|INFO|MainThread|init_device|subarray.py#101|SDPSubarray|Initialising SDP Subarray: mid_sdp/elt/subarray_1
...
1|2020-11-04T20:05:03.640Z|INFO|MainThread|init_device|subarray.py#137|SDPSubarray|SDP Subarray initialised: mid_sdp/elt/subarray_1
...
$ kubectl logs sdp-proccontrol-0
...
1|2020-11-04T20:04:24.528Z|DEBUG|MainThread|main_loop|processing_controller.py#221||Waiting...
...
$ kubectl logs sdp-helmdeploy-0
...
1|2020-11-04T20:04:19.989Z|INFO|MainThread|main|ska_sdp_helmdeploy.py#187||Found 0 existing deployments.
...
```

If it looks like this, there is a good chance everything has been deployed
correctly.

## Testing it out

### Connecting to the configuration database

The `sdp` chart deploys a 'console' pod which enables you to interact with the
configuration database. You can start a shell in the pod by doing:

```console
$ kubectl exec -it sdp-console-0 -- bash
```

This will allow you to use the `sdpcfg` command:

```console
# sdpcfg ls -R /
Keys with / prefix:
/subarray/01
/subarray/02
/subarray/03
```

Which shows that the configuration contains the state of the Tango devices.

### Starting a workflow

Assuming the configuration is prepared as explained in the previous
section, we can now add a processing block to the configuration:

```console
# sdpcfg process batch:test_dask:0.2.2
OK, pb_id = pb-sdpcfg-20201104-00000
```

The processing block is created with the `/pb` prefix in the
configuration:

```console
# sdpcfg ls values -R /pb
Keys with /pb prefix:
/pb/pb-sdpcfg-20201104-00000 = {
  "dependencies": [],
  "id": "pb-sdpcfg-20201104-00000",
  "parameters": {},
  "sbi_id": null,
  "workflow": {
    "id": "test_dask",
    "type": "batch",
    "version": "0.2.2"
  }
}
/pb/pb-sdpcfg-20201104-00000/owner = {
  "command": [
    "test_dask.py",
    "pb-sdpcfg-20201104-00000"
  ],
  "hostname": "proc-pb-sdpcfg-20201104-00000-workflow-97p8g",
  "pid": 1
}
/pb/pb-sdpcfg-20201104-00000/state = {
  "resources_available": true,
  "status": "RUNNING"
}
```

The processing block is detected by the processing controller which
deploys the workflow. The workflow in turn deploys the execution engines
(in this case, Dask). The deployments are requested by creating entries
with `/deploy` prefix in the configuration, where they are detected by
the Helm deployer which actually makes the deployments:

```console
# sdpcfg ls values -R /deploy
Keys with /deploy prefix:
/deploy/proc-pb-sdpcfg-20201104-00000-dask = {
  "args": {
    "chart": "dask/dask",
    "values": {
      "jupyter.enabled": "false",
      "jupyter.rbac": "false",
      "scheduler.serviceType": "ClusterIP",
      "worker.replicas": 2
    }
  },
  "id": "proc-pb-sdpcfg-20201104-00000-dask",
  "type": "helm"
}
/deploy/proc-pb-sdpcfg-20201104-00000-workflow = {
  "args": {
    "chart": "workflow",
    "values": {
      "env.SDP_CONFIG_HOST": "sdp-etcd-client.default.svc.cluster.local",
      "env.SDP_HELM_NAMESPACE": "sdp",
      "pb_id": "pb-sdpcfg-20201104-00000",
      "wf_image": "nexus.engageska-portugal.pt/sdp-prototype/workflow-test-dask:0.2.2"
    }
  },
  "id": "proc-pb-sdpcfg-20201104-00000-workflow",
  "type": "helm"
}
```

The deployments associated with the processing block have been created
in the `sdp` namespace, so to view the created pods we have to ask as
follows (on the host):

```console
$ kubectl get pod -n sdp
NAME                                                            READY   STATUS    RESTARTS   AGE
proc-pb-sdpcfg-20201104-00000-dask-scheduler-55c74999f6-tvrtx   1/1     Running   0          52s
proc-pb-sdpcfg-20201104-00000-dask-worker-677545d9f9-j9ffv      1/1     Running   0          52s
proc-pb-sdpcfg-20201104-00000-dask-worker-677545d9f9-jphzr      1/1     Running   0          52s
proc-pb-sdpcfg-20201104-00000-workflow-97p8g                    1/1     Running   0          54s
```

### Cleaning up

Finally, let us remove the processing block from the configuration (in the SDP
console shell):

```console
# sdpcfg delete -R /pb/pb-sdpcfg-20201104-00000
/pb/pb-sdpcfg-20201104-00000
/pb/pb-sdpcfg-20201104-00000/owner
/pb/pb-sdpcfg-20201104-00000/state
OK
```

If you re-run the commands from the last section you will notice that
this correctly causes all changes to the cluster configuration to be
undone as well.

## Accessing the Tango interface

By default, the `sdp` chart does not deploy the iTango shell pod from the
`tango-base` chart. To enable it, you can upgrade the release with:

```console
helm upgrade test ska/sdp --set tango-base.itango.enabled=true
```

Then you can start an iTango session with:

```console
$ kubectl exec -it tango-base-itango-console -- itango3
```

You should be able to list the Tango devices:

```python
In [1]: lsdev
Device                                   Alias                     Server                    Class
---------------------------------------- ------------------------- ------------------------- --------------------
mid_sdp/elt/master                                                 SDPMaster/1               SDPMaster
mid_sdp/elt/subarray_1                                             SDPSubarray/1             SDPSubarray
mid_sdp/elt/subarray_2                                             SDPSubarray/2             SDPSubarray
mid_sdp/elt/subarray_3                                             SDPSubarray/3             SDPSubarray
sys/access_control/1                                               TangoAccessControl/1      TangoAccessControl
sys/database/2                                                     DataBaseds/2              DataBase
sys/rest/0                                                         TangoRestServer/rest      TangoRestServer
sys/tg_test/1                                                      TangoTest/test            TangoTest
```

This allows direct interaction with the devices, such as querying and
and changing attributes and issuing commands:

```python
In [2]: d = DeviceProxy('mid_sdp/elt/subarray_1')

In [3]: d.state()
Out[3]: tango._tango.DevState.OFF

In [4]: d.On()

In [5]: d.state()
Out[5]: tango._tango.DevState.ON

In [6]: d.obsState
Out[6]: <obsState.EMPTY: 0>

In [7]: config_sbi = '''
    ...: {
    ...:   "id": "sbi-mvp01-20201104-00000",
    ...:   "max_length": 21600.0,
    ...:   "scan_types": [
    ...:     {
    ...:       "id": "science",
    ...:       "channels": [
    ...:         {"count": 372, "start": 0, "stride": 2, "freq_min": 0.35e9, "freq_max": 0.358e9, "link_map": [[0,0], [200,1]]}
    ...:       ]
    ...:     }
    ...:   ],
    ...:   "processing_blocks": [
    ...:     {
    ...:       "id": "pb-mvp01-20201104-00000",
    ...:       "workflow": {"type": "realtime", "id": "test_realtime", "version": "0.2.1"},
    ...:       "parameters": {}
    ...:     },
    ...:     {
    ...:       "id": "pb-mvp01-20201104-00001",
    ...:       "workflow": {"type": "realtime", "id": "test_realtime", "version": "0.2.1"},
    ...:       "parameters": {}
    ...:     },
    ...:     {
    ...:       "id": "pb-mvp01-20201104-00002",
    ...:       "workflow": {"type": "batch", "id": "test_batch", "version": "0.2.1"},
    ...:       "parameters": {},
    ...:       "dependencies": [
    ...:         {"pb_id": "pb-mvp01-20201104-00000", "type": ["visibilities"]}
    ...:       ]
    ...:     },
    ...:     {
    ...:       "id": "pb-mvp01-20201104-00003",
    ...:       "workflow": {"type": "batch", "id": "test_batch", "version": "0.2.1"},
    ...:       "parameters": {},
    ...:       "dependencies": [
    ...:         {"pb_id": "pb-mvp01-20201104-00002", "type": ["calibration"]}
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
```

## Removing the SDP

To remove the SDP deployment from the cluster, do:

```console
$ helm uninstall test
```

## Developing the SDP chart

If you want to install the chart from the source code in the SDP Integration
repository, for instance if you are developing a new version, then you can do
it like this:

```console
$ cd charts
$ helm install --dependency-update test sdp
```

The `--dependency-update` flag downloads the `tango-base` chart on which the
`sdp` chart depends.
