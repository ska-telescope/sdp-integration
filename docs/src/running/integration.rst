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
is an application, which provides on-demand Python script execution for the SKA.
For interactive telescope control (and hence SDP control), and experimentation, one can use the OET
Jupyter Notebooks and OET scripts:

- `OET Jupyter Notebooks <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html>`_
- `OET scripts <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/observing_scripts.html>`_

Using the OET Jupyter Notebooks
"""""""""""""""""""""""""""""""

An OET Jupyter Notebook server is automatically deployed when SKAMPI is started. The pod running it
has the name ``oet-jupyter-test-...``, where ``...`` will be a multi-character string, specific to the deployment.

The webserver running in this pod can be accessed via a web link of the following structure:

.. code-block::

    http://<ingress_host>/<namespace>/jupyter

``<namespace>`` is the `KUBE_NAMESPACE`, while the ``<ingress_host>`` is either an environment variable
called ``INGRESS_HOST``, or the default one can be found in the `Makefile` of SKAMPI under the same variable name.
You can also find this value by running this command:

.. code-block::

    kubectl describe ingress <pod_name> -n <namespace>

Depending on how you access the website (i.e. with port forwarding or directly), you may need to
replace the ``<ingress_host>`` with your localhost or similar.

More information on how to access the Notebooks on SKAMPI (including the required password) can be found in the
`OET docs <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html#accessing-jupyter-on-skampi>`_.

You can access the existing Notebooks in `scripts/notebooks`. Based on these examples,
you may also `create your own <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html>`_
version of an SKA control Notebook.

You may also use the OET scripts as a starting point for your own development. For example,
the steps in the script at `Control using static JSON <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/writing_control_scripts_without_sbs.html#control-using-static-json>`_
can be copy-pasted into a Jupyter Notebook. You will need to specify a JSON file, which contains the necessary
configuration string to control the subarray device and hence, SDP.
Example JSON files can be found in the `OET Scripts repository <https://gitlab.com/ska-telescope/ska-oso-scripting/-/tree/master/scripts/data>`_.
Here is an example how you can update the lines which require JSON files:

.. code-block::

    # Allocate resources, provide a path to a file with allocation JSON
    subarray.allocate_from_file('../data/example_allocate.json')

    # Configure sub-array, provide a path to a file with configuration JSON
    subarray.configure_from_file('../data/example_configure.json', scan_duration=10.0)

The above assumes that your Notebook is started from the ``scripts/notebooks`` directory.

Using the OET Rest Client
"""""""""""""""""""""""""

The `OET Rest Client <https://developer.skao.int/projects/ska-telescope-ska-oso-oet/en/latest/rest_client.html#rest-client>`_
provides a command line interface to communicate with a backend, which allows one to
`run SKA control scripts <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/script_execution.html#script-execution-on-oet-rest-server>`_.

The easiest to do this is through the
`terminal window of the Jupyter <https://developer.skao.int/projects/ska-telescope-ska-oso-scripting/en/latest/oet_with_skampi.html#accessing-oet-rest-client-in-jupyter-terminal>`_
server deployed in SKAMPI. Please follow the above links to learn more about OET and how to use Python scripts
to control an SKA telescope via this interface.

