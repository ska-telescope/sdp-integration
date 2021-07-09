.. _running_requirements:

Requirements
============

To run the SDP, you need to have `Kubernetes <https://kubernetes.io/>`_ and
`Helm <https://helm.sh>`_ installed.

Kubernetes
----------

There are a number of way to install and run Kubernetes in your development
environment. Depending on the operating system, choose either Docker Desktop,
Minikube (recommended) or Microk8s.

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

Depending on the machine increase or decrease the amount of memory that the Minikube VM uses, you can
specify it on the command line when starting a new instance, for example:

.. code-block::

    $ minikube start --memory='4096m'

Alternatively, you may configure this as a default by doing:

.. code-block::

    $ minikube config set memory 4096

To use minikube's Docker daemon, configure environment by doing:

.. code-block::

    $ minikube docker-env
    $ eval $(minikube -p minikube docker-env)



Microk8s
^^^^^^^^

Canonical supports `microk8s <https://microk8s.io>`_ for Linux, macOS and
Windows.

Helm
^^^^^

Helm is available from most typical package managers, see `Introduction to Helm
<https://helm.sh/docs/intro/>`_.


K9s
^^^

`K9s <https://k9scli.io>`_ is terminal-based UI for Kubernetes clusters which
provides a convenient interactive interface. It is not required to run the SDP,
but it is recommended for its ease of use.


Commands Help Guide
^^^^^^^^^^^^^^^^^^^

Here are a list of key commands for Docker:

=============== ===========
commands        Description
=============== ===========
docker images   List docker images
--------------- -----------
docker build    Build an image from a Dockerfile
--------------- -----------
docker pull     Pull an image or a repository from a registry
--------------- -----------
docker push     Push an image or a repository to a registry
--------------- -----------
docker rmi      Remove one or more images
=============== ===========

List of all other docker commands can be found at
`<https://docs.docker.com/engine/reference/commandline/cli/>`_.

Here are a list of key commands for kubectl:

==================================== ===========
commands                             Description
==================================== ===========
kubectl create namespace             Create a namespace with the specified name.
------------------------------------ -----------
kubectl logs                         Print the logs for a container in a pod or specified resource
------------------------------------ -----------
kubectl run                          Create and run a particular image in a pod.
------------------------------------ -----------
kubectl get pods/services/namespaces List all pods, services or namespaces
------------------------------------ -----------
kubectl delete deployments/services  Delete deployments or services
==================================== ===========

List of all other kubectl commands can be found at
`<https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands>`_.


