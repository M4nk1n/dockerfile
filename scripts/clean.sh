#!/bin/bash

ImageName=''
DockerHubAccount='local'

# 打印的帮助信息
usage() {
  echo -ne "
  Usage:
    bash $(basename $0)
    -i, --image [name] \t\t\t\033[33m镜像名称\033[0m
    -a, --account [id] \t\t\t\033[33mDocker Hub Account ID\033[0m
";
}

[ $# -eq 0 ] && usage

ARGS=$(getopt -l "image:,account:" -o "i:a:" -- "$@")
if [ $? != 0 ] ; then exit 1 ; fi
eval set -- "$ARGS"

while true; do
  case $1 in
    -i|--image)
      ImageName="$2"
      shift 2
      ;;
    -a|--account)
      DockerHubAccount="$2"
      shift 2
      ;;
    --)
      shift
      break
      ;;
    *)
      usage
      exit 1;
      ;;
    esac
  done

[[ -z "$ImageName" ]] && echo -ne "Error: Invalid option\n" && usage && exit 1;

ImageID=$(docker images -q --filter reference=$DockerHubAccount/$ImageName)

echo -ne "docker image rm (ID: $ImageID) start...\n"

docker rmi --force $ImageID
