{{/* vim: set filetype=mustache: */}}
{{/*
Expand the name of the chart.
*/}}
{{- define "ska-sdp.name" -}}
{{- default "sdp" .Values.nameOverride | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "ska-sdp.fullname" -}}
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
{{- define "ska-sdp.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "ska-sdp.labels" }}
app: {{ include "ska-sdp.name" . }}
chart: {{ include "ska-sdp.chart" . }}
release: {{ .Release.Name }}
heritage: {{ .Release.Service }}
system: {{ .Values.system }}
{{- end }}

{{/* Configuration database host */}}
{{- define "ska-sdp.etcd-host" -}}
{{ include "ska-sdp.name" . }}-etcd-client.{{ .Release.Namespace }}.svc.cluster.local
{{- end -}}

{{/* Init container to wait for configuration database availability */}}
{{- define "ska-sdp.wait-for-etcd" -}}
- name: wait-for-etcd
  image: {{ .Values.etcd.image }}:v{{ .Values.etcd.version }}
  imagePullPolicy: {{ .Values.etcd.imagePullPolicy }}
  command: ["/bin/sh", "-c", "while ( ! etcdctl endpoint health ); do sleep 1; done"]
  env:
  - name: ETCDCTL_ENDPOINTS
    value: "http://{{ include "ska-sdp.etcd-host" . }}:2379"
  - name: ETCDCTL_API
    value: "3"
{{- end -}}

{{/* Environment variables for HTTP proxy settings */}}
{{- define "ska-sdp.http-proxy" -}}
{{- if .Values.proxy -}}
{{- $noproxy := list (include "ska-sdp.etcd-host" .) "localhost" "127.0.0.1" "10.96.0.0/12" "172.17.0.1/16" -}}
{{- $noproxy := concat $noproxy .Values.proxy.noproxy -}}
- name: http_proxy
  value: {{ .Values.proxy.server | quote }}
- name: https_proxy
  value: {{ .Values.proxy.server | quote }}
- name: no_proxy
  value: {{ join "," $noproxy | quote }}
{{- end -}}
{{- end -}}
