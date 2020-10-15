{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "sdp.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "sdp.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "sdp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "sdp.labels" }}
app: {{ template "sdp.name" . }}
chart: {{ template "sdp.chart" . }}
release: {{ .Release.Name }}
heritage: {{ .Release.Service }}
system: {{ .Values.system }}
telescope: {{ .Values.telescope }}
{{- end }}

{{/* Init container to wait for configuration database availability */}}
{{- define "sdp.etcd-host" -}}
{{ include "sdp.name" . }}-etcd-client.{{ .Release.Namespace }}.svc.cluster.local
{{- end -}}
{{- define "sdp.wait-for-etcd" -}}
- image: {{ .Values.etcd.image }}:v{{ .Values.etcd.version }}
  name: wait-for-etcd
  command: ["/bin/sh", "-c", "while ( ! etcdctl endpoint health ); do sleep 1; done"]
  env:
  - name: ETCDCTL_ENDPOINTS
    value: "http://{{ include "sdp.etcd-host" . }}:2379"
  - name: ETCDCTL_API
    value: "3"
{{- end -}}