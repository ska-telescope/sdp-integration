.. _running_integration:

Running the SDP in the integration environment
==============================================

The SDP is being integrated with the other telescope subsystems as part of the
so-called *Minimum Viable Product* (MVP). The integration is done in the `SKA
MVP Prototype Integration (SKAMPI) repository
<https://gitlab.com/ska-telescope/skampi/>`_.

Instructions for installing and running the MVP can be found in the `SKAMPI
documentation
<https://developer.skatelescope.org/projects/skampi/en/latest/>`_.

To then deploy an SDP workflow without using the Tango interface, follow the
instructions in :ref:`running_standalone`. However, you will must specify the
namespace in which the SDP is running.

..
    `standalone SDP documentation
    <https://developer.skatelescope.org/projects/sdp-prototype/en/latest/running/running_standalone.html#connecting-to-the-configuration-database>`_.

.. code-block::

    $ kubectl -n <namespace> exec -it deploy/test-sdp-prototype-console -- /bin/bash

The default namespace into which SKAMPI deploys is ``integration``.

Alternatively, you can configure the namespace that ``kubectl`` uses by default

.. code-block::

    $ kubectl config set-context --current --namespace=integration

to allow you to run the commands without alteration.
