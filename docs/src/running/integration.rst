.. _running_integration:

Running the SDP in the integration environment
==============================================

The Science Data Processor (SDP) is integrated with the other telescope subsystems as part of the
SKA evolutionary prototype, also known as the *Minimum Viable Product* (MVP).
The integration is done in the `SKA MVP Prototype Integration (SKAMPI)
repository <https://gitlab.com/ska-telescope/skampi/>`_.

Instructions for installing and running the MVP can be found in the `SKAMPI
documentation <https://developer.skatelescope.org/projects/skampi/en/latest/>`_.
`TODO: this needs exact, better links (probably need to wait for skampi docs to be updated)`

The default namespace into which SKAMPI deploys is ``integration``. You can change this by
setting the `KUBE_NAMESPACE` `KUBE_NAMESPACE_SDP` environment variables before deploying SKAMPI. E.g.

.. code-block::

    $ export KUBE_NAMESPACE=test-skampi-deployment
    $ export KUBE_NAMESPACE_SDP=test-skampi-deployment-sdp

If you are deploying on a shared machine, make sure your namespace doesn't clash with existing
SKAMPI deployments.

SDP is integrated within both SKAMPI for Mid and SKAMPI for Low. All of the standard SDP pods
will start up upon SKAMPI deployment.

Interacting with SDP within SKAMPI
----------------------------------

Using the SDP console
^^^^^^^^^^^^^^^^^^^^^

Follow the "Testing it out" steps in :ref:`running_standalone`. Remember, that when you want
to access a pod in your namespace, you will have to specify that namespace. E.g. to start the
console pod, run:

.. code-block::

    $ kubectl -n <namespace> exec -it sdp-console-0 -- bash

Using the iTango pod
^^^^^^^^^^^^^^^^^^^^

If your deployment doesn't have the `ska-tango-base-itango-console` running, you should create a custom
`values.yml` file and add the following:

.. code-block::

    tango-base:
      itango:
        enabled: true

And then upgrade your SKAMPI installation via its Makefile (``make upgrade-chart ..``) or
using ``helm upgrade ..``.

Once you have a running iTango console, follow the steps to test it out
in :ref:`running_standalone` at "Accessing the Tango interface" section.
Again, you will have to specify the namespace you deployed in, when interacting with
the iTango pod.

Using the Observation Execution Tool
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

`Observation Execution Tool (OET)
<https://developer.skao.int/projects/ska-telescope-ska-oso-oet/en/latest/index.html>`_,
is an SKA application, which provides on-demand Python script execution for the SKA.
It has two main interfaces through which one can control the SDP:

- `OET scripts <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/observing_scripts.html>`_
- `OET Jupyter Notebooks <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html>`_

Running OET scripts via the `oet-itango-console`
""""""""""""""""""""""""""""""""""""""""""""""""

Start the OET iTango console with pre-loaded OET functionality:

.. code-block::

     $ kubectl exec -n <namespace> -it oet-itango-console-test-0 -- sudo -u tango /bin/bash -c ". /etc/environment; export TANGO_HOST; itango3 --profile=ska"

Note, that at time of testing the description which appears when the iTango console starts is out-of-date.
There are various Python objects that no longer exist, which are listed under "You can now use".
However, you should be able to interact with SDP via this console, following the instructions at the following links.

The steps in the script at `Control using static JSON <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/writing_control_scripts_without_sbs.html#control-using-static-json>`_
can be copy-pasted into the iTango console. You will need to specify a JSON file, which contains the necessary
configuration string to control the subarray device and hence, SDP.
Example JSON files can be found in the `OET Scripts repository <https://gitlab.com/ska-telescope/ska-oso-scripting/-/tree/master/scripts/data>`_.
Here is an example how you can update the lines which require JSON files:

.. code-block::

    # Allocate resources, provide a path to a file with allocation JSON
    subarray.allocate_from_file('scripts/data/example_allocate.json')

    # Configure sub-array, provide a path to a file with configuration JSON
    subarray.configure_from_file('scripts/data/example_configure.json', scan_duration=10.0)

Using the OET Jupyter Notebooks
"""""""""""""""""""""""""""""""

An OET Jupyter Notebook server is automatically deployed when SKAMPI is started. The pod running it
has the name ``oet-jupyter-test-...``, where ``...`` will be a multi-character string, specific to the deployment.

The logs of the pod will tell you the web-address where you can access the server:

.. code-block::

    kubectl logs -n <namespace> <pod_name>

The output will be similar to:

.. code-block::

    [I 22:29:15.891 NotebookApp] Writing notebook server cookie secret to /home/tango/.local/share/jupyter/runtime/notebook_cookie_secret
    [I 22:29:16.114 NotebookApp] Serving notebooks from local directory: /app
    [I 22:29:16.114 NotebookApp] Jupyter Notebook 6.4.0 is running at:
    [I 22:29:16.114 NotebookApp] http://oet-jupyter-test-5d6f76f9f9-lp5vd:8888/my-skampi/jupyter/
    [I 22:29:16.114 NotebookApp] Use Control-C to stop this server and shut down all kernels (twice to skip confirmation).

In the above example ``my-skampi`` is the namespace in which the pod is running. From this,
we can see that the Jupyter Notebook server can be accessed at
``http://oet-jupyter-test-5d6f76f9f9-lp5vd:8888/my-skampi/jupyter/``. Depending on where you have
deployed SKAMPI (e.g. locally, or on a remote machine), you may have to replace
``oet-jupyter-test-5d6f76f9f9-lp5vd`` with the public IP address of the pod. More information
on how to access the Notebooks on SKAMPI (including the required password) can be found in the
`OET docs <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html#accessing-jupyter-on-skampi>`_.

You can access the existing Notebooks in `scripts/notebooks`. Based on these examples,
you may also `create your own <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html>`_
version of an SKA control Notebook.