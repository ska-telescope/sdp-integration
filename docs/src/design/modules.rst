.. _design_modules:

Modules
=======

.. figure:: ../images/sdp_modules.svg
  :align: center

  SDP software modules.

The SDP is built from software modules which produce a number of different
types of artefacts. The components of the system are built as Docker images
which are deployed on a cluster using a Helm chart. The Docker images depend on
libraries containing common code. The diagram shows the SDP modules and the
dependencies beween them.

The source code is hosted in `GitLab in the ska-telescope group
<https://gitlab.com/ska-telescope/>`_, in the following repositories:

* `sdp-integration <https://gitlab.com/ska-telescope/sdp-integration>`_

  Integration of components into the SDP subsystem. Contains the Helm chart to
  deploy the SDP and this documentation.

* `sdp-config <https://gitlab.com/ska-telescope/sdp-config>`_

  Library providing the interface to the configuration database.

* `sdp-workflow <https://gitlab.com/ska-telescope/sdp-workflow>`_

  Library providing the high-level interface for writing workflows.

* `sdp-lmc <https://gitlab.com/ska-telescope/sdp-lmc>`_

  Tango devices for local monitoring and control.

* `sdp-proccontrol <https://gitlab.com/ska-telescope/sdp-proccontrol>`_

  Processing controller.

* `sdp-helmdeploy <https://gitlab.com/ska-telescope/sdp-helmdeploy>`_

  Helm deployer.

* `sdp-console <https://gitlab.com/ska-telescope/sdp-console>`_

  Console used to interact with the configuration database.

* `sdp-workflows-procfunc
  <https://gitlab.com/ska-telescope/sdp-workflows-procfunc>`_

  Workflows and processing components/functions.

* `sdp-helmdeploy-charts
  <https://gitlab.com/ska-telescope/sdp-helmdeploy-charts>`_

  Charts used by the Helm deployer to deploy workflows and processing
  components/functions.
