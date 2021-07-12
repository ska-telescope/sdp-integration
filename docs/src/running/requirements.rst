.. _running_requirements:

Requirements
============

To run the SDP, you need to have `Kubernetes <https://kubernetes.io/>`_ and
`Helm <https://helm.sh>`_ installed.

Kubernetes
----------

There are a number of way to install and run Kubernetes in your development
environment. There are many ways of doing this, including Docker Desktop,
Minikube (recommended) and microk8s.

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

Minikube can be started with the default configurations by doing:

.. code-block:: console

    $ minikube start

If you need to increase the amount of memory that the Minikube VM uses, you can:

.. code-block:: console

    $ minikube start --memory='4096m'

Alternatively, you may configure this as a default by doing:

.. code-block:: console

    $ minikube config set memory 4096

If you are developing SDP components and you would like to build and test them
in Minikube, you need to configure Docker to use the daemon inside the VM.
This can be done by setting the environment variables:

.. code-block:: console

    $ minikube docker-env
    $ eval $(minikube -p minikube docker-env)



Microk8s
^^^^^^^^

Canonical supports `microk8s <https://microk8s.io>`_ for Linux, macOS and
Windows.

Helm
----

Helm is available from most typical package managers, see `Introduction to Helm
<https://helm.sh/docs/intro/>`_.


K9s
---

`K9s <https://k9scli.io>`_ is terminal-based UI for Kubernetes clusters which
provides a convenient interactive interface. It is not required to run the SDP,
but it is recommended for its ease of use.


Commands Help Guide
-------------------

To know more about the available commands, here are some useful links:

* Helm - `<https://helm.sh/docs/helm/helm/>`_.
* Kubectl - `<https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands>`_.
* Docker  - `<https://docs.docker.com/engine/reference/commandline/cli/>`_.


