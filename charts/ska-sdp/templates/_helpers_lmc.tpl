{{/*
Generate Job to configure Tango DB.
This template should be called with a context containing:
  - config: configuration to be written to Tango DB
  - tangohost: the location of the Tango DB
  - root: the root context of the chart
*/}}
{{- define "ska-sdp.lmc-config" }}
---
# Configmap containing device server configuration
apiVersion: v1
kind: ConfigMap
metadata:
  name: {{ include "ska-sdp.name" .root }}-lmc-configuration
  namespace: {{ .root.Release.Namespace }}
  labels:
    {{- include "ska-sdp.labels" .root | indent 4 }}
    component: {{ .root.Values.lmc.component }}-configuration
    subsystem: enabling-system
    function: deployment
    domain: self-configuration
    intent: enabling
data:
  {{- (.root.Files.Glob "data/safe-dsconfig.sh").AsConfig | nindent 2 }}
  sdp-devices.json: |
    {{- toPrettyJson .config | nindent 4 }}
---
# Job to apply device server configuration to Tango database
apiVersion: batch/v1
kind: Job
metadata:
  name: {{ include "ska-sdp.name" .root }}-lmc-configuration
  namespace: {{ .root.Release.Namespace }}
  labels:
    {{- include "ska-sdp.labels" .root | indent 4 }}
    component: {{ .root.Values.lmc.component }}-configuration
    subsystem: enabling-system
    function: deployment
    domain: self-configuration
    intent: enabling
spec:
  template:
    spec:
      containers:
      - name: dsconfig
        image: {{ .root.Values.dsconfig.image.registry }}/{{ .root.Values.dsconfig.image.image }}:{{ .root.Values.dsconfig.image.tag }}
        imagePullPolicy: {{ .root.Values.dsconfig.image.pullPolicy }}
        command:
          - /usr/local/bin/wait-for-it.sh
          - {{ .tangohost }}
          - --timeout=180
          - --strict
          - --
          - /bin/bash
          - data/safe-dsconfig.sh -w -a -u data/sdp-devices.json
        env:
        - name: TANGO_HOST
          value: {{ .tangohost }}
        volumeMounts:
          - name: configuration
            mountPath: data
            readOnly: true
      volumes:
        - name: configuration
          configMap:
            name: {{ include "ska-sdp.name" .root }}-lmc-configuration
      restartPolicy: Never
{{- end}}

{{/*
Generate StatefulSet containing a Tango device server.
This template should be called with a context containing:
  - device: the details of the device, with entries:
    + name: Name (e.g. master)
    + tangoname: Tango device name (e.g. mid_sdp/elt/master)
    + command: Command to run the device (e.g. ["SDPMaster"])
    + args: Arguments to pass to command (e.g. ["0", "-v4"])
    + function: function label (e.g. sdp-monitoring)
    + domain: domain label (e.g. sdp-central-control)
  - tangohost: location of the Tango DB
  - root: the root context of the chart
*/}}
{{- define "ska-sdp.lmc-device" }}
---
# Dummy Service to ensure Pod is DNS addressable
apiVersion: v1
kind: Service
metadata:
  name: {{ include "ska-sdp.name" .root }}-lmc-{{ .device.name }}
  namespace: {{ .root.Release.Namespace }}
  labels:
    {{- include "ska-sdp.labels" .root | indent 4 }}
    component: {{ .root.Values.lmc.component }}-{{ .device.name }}
    subsystem: {{ .root.Values.lmc.subsystem }}
    function: {{ .device.function }}
    domain: {{ .device.domain }}
    intent: production
spec:
  clusterIP: None
  selector:
    component: {{ .root.Values.lmc.component }}-{{ .device.name }}
    subsystem: {{ .root.Values.lmc.subsystem }}
---
# StatefulSet with single Pod
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: {{ include "ska-sdp.name" .root }}-lmc-{{ .device.name }}
  namespace: {{ .root.Release.Namespace }}
  labels:
    {{- include "ska-sdp.labels" .root | indent 4 }}
    component: {{ .root.Values.lmc.component }}-{{ .device.name }}
    subsystem: {{ .root.Values.lmc.subsystem }}
    function: {{ .device.function }}
    domain: {{ .device.domain }}
    intent: production
spec:
  selector:
    matchLabels:
      component: {{ .root.Values.lmc.component }}-{{ .device.name }}
      subsystem: {{ .root.Values.lmc.subsystem }}
  serviceName: {{ include "ska-sdp.name" .root }}-lmc-{{ .device.name }}
  replicas: 1
  template:
    metadata:
      labels:
        {{- include "ska-sdp.labels" .root | indent 8 }}
        component: {{ .root.Values.lmc.component }}-{{ .device.name }}
        subsystem: {{ .root.Values.lmc.subsystem }}
        function: {{ .device.function }}
        domain: {{ .device.domain }}
        intent: production
    spec:
      initContainers:
      {{- include "ska-sdp.wait-for-etcd" .root | nindent 6 }}
      - name: wait-for-device-config
        image: {{ .root.Values.dsconfig.image.registry }}/{{ .root.Values.dsconfig.image.image }}:{{ .root.Values.dsconfig.image.tag }}
        imagePullPolicy: {{ .root.Values.dsconfig.image.pullPolicy }}
        command:
          - retry
          - --max=10
          - --
          - tango_admin
          - --check-device
          - {{ .device.tangoname | toString }}
        env:
        - name: TANGO_HOST
          value: {{ .tangohost }}
      containers:
      - name: {{ .device.name }}
        image: {{ .root.Values.lmc.image }}:{{ .root.Values.lmc.version }}
        imagePullPolicy: {{ .root.Values.lmc.imagePullPolicy }}
        command: {{ toJson .device.command }}
        args: {{ toJson .device.args}}
        env:
        - name: SDP_CONFIG_HOST
          value: {{ include "ska-sdp.etcd-host" .root }}
        - name: TANGO_HOST
          value: {{ .tangohost }}
        - name: FEATURE_ALL_COMMANDS_HAVE_ARGUMENT
          value: {{ .root.Values.lmc.allCommandsHaveArgument | int | quote }}
{{- end }}
