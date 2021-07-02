.. _running_integration:

Running the SDP in the integration environment
==============================================

The Science Data Processor (SDP) is integrated with the other telescope subsystems as part of the
SKA evolutionary prototype, also known as the *Minimum Viable Product* (MVP).
The integration is done in the `SKA MVP Prototype Integration (SKAMPI)
repository <https://gitlab.com/ska-telescope/skampi/>`_.

Instructions for installing and running the MVP can be found in the `SKAMPI
documentation TODO: this needs exact, better links (probably need to wait for skampi docs to be updated)
<https://developer.skatelescope.org/projects/skampi/en/latest/>`_.

The default namespace into which SKAMPI deploys is ``integration``. You can change this by
setting the `KUBECONFIG` `KUBE_NAMESPACE_SDP` environment variables before deploying SKAMPI. E.g.

.. code-block::

    $ export KUBECONFIG=test-skampi-deployment
    $ export KUBE_NAMESPACE_SDP=test-skampi-deployment-sdp

If you are deploying on a shared machine, make sure your namspace doesn't clash with existing
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

If your deployment doesn't have the ska-tango-base-itango-console running, you should create a custom
values.yml file and add the following:

.. code-block::

    ska-tango-base:
      itango:
        enabled: true

And then upgrade your SKAMPI installation via its Makefile (``make upgrade-chart``) or
using ``helm upgrade``

Once you have a running iTango console, follow the steps to test it out
in :ref:`running_standalone` at "Accessing the Tango interface" section.

Using the Observation Execution Tool (OET)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^






#####
Alternatively, you can configure the namespace that ``kubectl`` uses by default

.. code-block::

    $ kubectl config set-context --current --namespace=integration

to allow you to run the commands without alteration.
