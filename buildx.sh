#!/bin/bash

work_path=$(dirname $0)
cd ./${work_path} # 跳到脚本位置

Dir=''
ImageName=''
DockerHubAccount='local'
Tag=()
Platform='linux/amd64'

# 打印的帮助信息
usage() {
  echo -ne "
  Usage:
    bash $(basename $0)
    -d, --dir <dir> \t\t\t\033[33m构建目录\033[0m
    -i, --image [name] \t\t\t\033[33m镜像名称\033[0m
    -a, --account [id] \t\t\t\033[33mDocker Hub Account ID\033[0m
    -t, --tag <tag> \t\033[33mTag, 可多次传递以支持设置多个 tag\033[0m
    -p, --platform <platforms> \t\033[33mPlatform, 如: linux/arm64,linux/amd64\033[0m
";
}

[ $# -eq 0 ] && usage

ARGS=$(getopt -l "dir:,image:,account:,tag:,platform:" -o "d:i:a:t:p:" -- "$@")
if [ $? != 0 ] ; then exit 1 ; fi
eval set -- "$ARGS"

while true; do
  case $1 in
    -d|--dir)
      Dir="$2"
      shift 2
      ;;
    -i|--image)
      ImageName="$2"
      shift 2
      ;;
    -a|--account)
      DockerHubAccount="$2"
      shift 2
      ;;
    -t|--tag)
      Tag[${#Tag[@]}]="$2"
      shift 2
      ;;
    -p|--platform)
      Platform="$2"
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

[[ -z "$Dir" ]] && echo -ne "Error: Invalid option\n" && usage && exit 1;

if [ -d "./packages/$Dir" ]; then
  echo -ne "docker build start...\n"
  
  echo -ne "docker tag: ${Tag[@]}\n"
  
  for a in "${Tag[@]}"; do
    TagStr+=" -t ${DockerHubAccount}/${ImageName:-${Dir}}:${a}"
  done

  echo "docker buildx build -t $DockerHubAccount/${ImageName:-${Dir}} $TagStr --platform=$Platform ./packages/$Dir --push"
  docker buildx build -t $DockerHubAccount/${ImageName:-${Dir}} $TagStr --platform=$Platform ./packages/$Dir --push
fi
