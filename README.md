# SDP Integration

This repository integrates the components of the SKA Science Data Processor
(SDP). It contains the Helm chart to launch the SDP as a subsystem of the SKA
prototype (SKAMPI), or stand-alone for testing.

The components are built as Docker images from the following repositories:

* [Local monitoring and control](https://gitlab.com/ska-telescope/sdp/ska-sdp-lmc/)
* [Processing controller](https://gitlab.com/ska-telescope/sdp/ska-sdp-proccontrol/)
* [Helm deployer](https://gitlab.com/ska-telescope/sdp/ska-sdp-helmdeploy/)
* [Console](https://gitlab.com/ska-telescope/sdp/ska-sdp-console/)
