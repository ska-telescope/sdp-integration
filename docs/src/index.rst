SDP Integration
===============

The ``ska-sdp-integration`` repository integrates the components of the SKA
Science Data Processor (SDP). It contains the Helm chart to deploy the SDP as a
subsystem of the SKA, or stand-alone for testing.

This documentation also gives a overview of the design of the SDP. It describes
the components that make up the system, and the software modules from which
they are built.

.. toctree::
  :maxdepth: 1
  :caption: SDP Design

  design/overview
  design/components
  design/modules

.. toctree::
  :maxdepth: 1
  :caption: Running the SDP

  running/requirements
  running/standalone
  running/integration
  running/helm-chart

Indices and tables
------------------

- :ref:`genindex`
- :ref:`modindex`
- :ref:`search`
