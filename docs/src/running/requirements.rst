.. _running_requirements:

Requirements
============

To run the SDP, you need to have `Kubernetes <https://kubernetes.io/>`_ and
`Helm <https://helm.sh>`_ installed.

Kubernetes
----------

There are a number of way to install and run Kubernetes in your development
environment.

Docker Desktop
^^^^^^^^^^^^^^

`Docker Desktop <https://www.docker.com/products/docker-desktop>`_ for Windows
and macOS includes a single-node Kubernetes installation. You need to activate
it in the settings. You may need to increase the memory limit from its default
value of 2 GB to allow the SDP to run.

Minikube
^^^^^^^^

`Minikube <https://minikube.sigs.k8s.io>`_ provides a way to run a single-node
Kubernetes installation on Linux, macOS and Windows. It can use a number of
different `drivers <https://minikube.sigs.k8s.io/docs/drivers/>`_ to run
Kubernetes in a virtual machine or container. On Windows, the Hyper-V
hypervisor can be enabled in the settings, after which a reboot is required.

If you need to increase the amount of memory that the Minikube VM uses, you can
specify it on the command line when starting a new instance, for example:

.. code-block::

    $ minikube start --memory='4096m'

Alternatively, you may configure this as a default by doing:

.. code-block::

    $ minikube config set memory 4096m


Microk8s
^^^^^^^^

Canonical supports `microk8s <https://microk8s.io>`_ for Linux, macOS and
Windows.

Helm
----

Helm is available from most typical package managers, see `Introduction to Helm
<https://helm.sh/docs/intro/>`_.

If you are using Helm for the first time, you need to add the ``stable`` chart
repository:

.. code-block::

    $ helm repo add stable https://kubernetes-charts.storage.googleapis.com/
