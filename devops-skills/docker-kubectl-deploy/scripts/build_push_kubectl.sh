#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Build a Docker image, push it, then update a Kubernetes Deployment via kubectl.

Usage:
  build_push_kubectl.sh --image IMAGE_REPO[[:TAG]] --deployment NAME --container NAME [options]

Required:
  --image IMAGE_REPO[[:TAG]]   Example: ghcr.io/org/app or registry:5000/team/app:dev-123
  --deployment NAME            Kubernetes Deployment name
  --container NAME             Container name inside the pod spec

Options:
  --tag TAG                    If omitted, derive from git SHA (if available) else timestamp
  --namespace, -n NS            Default: default
  --kube-context CONTEXT        Optional kubectl context
  --dockerfile, -f PATH         Default: Dockerfile
  --context PATH                Docker build context directory (default: .)
  --build-arg KEY=VAL           Repeatable; forwarded to docker build
  --platform PLATFORM           Forwarded to docker build (requires compatible Docker)
  --no-cache                    Forwarded to docker build
  --rollout-timeout DURATION    Default: 120s (passed to kubectl rollout status)
  --dry-run                     Print commands without executing
  -h, --help                    Show this help

Examples:
  ./build_push_kubectl.sh \
    --image ghcr.io/org/app \
    --deployment app \
    --container app \
    --namespace dev

  ./build_push_kubectl.sh \
    --image registry:5000/team/app:staging-42 \
    --deployment app \
    --container app \
    --kube-context staging \
    --namespace app
EOF
}

die() {
  echo "Error: $*" >&2
  exit 2
}

require_cmd() {
  command -v "$1" >/dev/null 2>&1 || die "missing command: $1"
}

run() {
  printf '+'
  for arg in "$@"; do
    printf ' %q' "$arg"
  done
  printf '\n'

  if [[ "${dry_run}" == "true" ]]; then
    return 0
  fi

  "$@"
}

image_input=""
tag=""
dockerfile="Dockerfile"
context_dir="."
namespace="default"
deployment=""
container=""
kube_context=""
rollout_timeout="120s"
dry_run="false"
docker_build_args=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --image)
      [[ $# -ge 2 ]] || die "--image requires a value"
      image_input="$2"
      shift 2
      ;;
    --tag)
      [[ $# -ge 2 ]] || die "--tag requires a value"
      tag="$2"
      shift 2
      ;;
    --dockerfile|-f)
      [[ $# -ge 2 ]] || die "--dockerfile requires a value"
      dockerfile="$2"
      shift 2
      ;;
    --context)
      [[ $# -ge 2 ]] || die "--context requires a value"
      context_dir="$2"
      shift 2
      ;;
    --namespace|-n)
      [[ $# -ge 2 ]] || die "--namespace requires a value"
      namespace="$2"
      shift 2
      ;;
    --deployment)
      [[ $# -ge 2 ]] || die "--deployment requires a value"
      deployment="$2"
      shift 2
      ;;
    --container)
      [[ $# -ge 2 ]] || die "--container requires a value"
      container="$2"
      shift 2
      ;;
    --kube-context)
      [[ $# -ge 2 ]] || die "--kube-context requires a value"
      kube_context="$2"
      shift 2
      ;;
    --rollout-timeout)
      [[ $# -ge 2 ]] || die "--rollout-timeout requires a value"
      rollout_timeout="$2"
      shift 2
      ;;
    --build-arg)
      [[ $# -ge 2 ]] || die "--build-arg requires a value"
      docker_build_args+=(--build-arg "$2")
      shift 2
      ;;
    --platform)
      [[ $# -ge 2 ]] || die "--platform requires a value"
      docker_build_args+=(--platform "$2")
      shift 2
      ;;
    --no-cache)
      docker_build_args+=(--no-cache)
      shift
      ;;
    --dry-run)
      dry_run="true"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    --)
      shift
      docker_build_args+=("$@")
      break
      ;;
    *)
      echo "Unknown argument: $1" >&2
      usage >&2
      exit 2
      ;;
  esac
done

[[ -n "${image_input}" ]] || die "--image is required"
[[ "${image_input}" != *@* ]] || die "image digest references (@sha256:...) are not supported; use a tag"
[[ -n "${deployment}" ]] || die "--deployment is required"
[[ -n "${container}" ]] || die "--container is required"

image_repo="${image_input}"

after_last_slash="${image_input##*/}"
before_last_slash=""
if [[ "${image_input}" == */* ]]; then
  before_last_slash="${image_input%/*}"
fi

if [[ "${after_last_slash}" == *:* ]]; then
  tag_from_image="${after_last_slash##*:}"
  name_from_image="${after_last_slash%:*}"

  [[ -z "${tag}" ]] || die "provide tag either via --tag or in --image, not both"
  tag="${tag_from_image}"

  if [[ -n "${before_last_slash}" ]]; then
    image_repo="${before_last_slash}/${name_from_image}"
  else
    image_repo="${name_from_image}"
  fi
fi

if [[ -z "${tag}" ]]; then
  if command -v git >/dev/null 2>&1 && git -C "${context_dir}" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
    tag="$(git -C "${context_dir}" rev-parse --short HEAD)"
  else
    tag="$(date +%Y%m%d%H%M%S)"
  fi
fi

image_ref="${image_repo}:${tag}"

if [[ "${dry_run}" != "true" ]]; then
  require_cmd docker
  require_cmd kubectl
fi

run docker build "${docker_build_args[@]}" -f "${dockerfile}" -t "${image_ref}" "${context_dir}"
run docker push "${image_ref}"

kubectl_cmd=(kubectl)
if [[ -n "${kube_context}" ]]; then
  kubectl_cmd+=(--context "${kube_context}")
fi
kubectl_cmd+=(-n "${namespace}")

run "${kubectl_cmd[@]}" set image "deployment/${deployment}" "${container}=${image_ref}"
run "${kubectl_cmd[@]}" rollout status "deployment/${deployment}" --timeout="${rollout_timeout}"

echo "Deployed: ${image_ref}"
