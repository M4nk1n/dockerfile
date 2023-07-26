#!/bin/bash

Dir=''
ImageName=''
DockerHubAccount='local'
Tag=()
Build='0'
Publish='0'
Remove='0'

# 打印的帮助信息
usage() {
  echo -ne "
  Usage:
    bash $(basename $0)
    -d, --dir <dir>     \033[33m构建目录\033[0m
    -i, --image [name]  \033[33m镜像名称\033[0m
    -a, --account [id]  \033[33mDocker Hub Account ID\033[0m
    -t, --tag <tag>     \033[33mTag, 可多次传递以支持设置多个 tag\033[0m
    -b, --build         \033[33m构建镜像\033[0m
    -p, --publish       \033[33m自动发布镜像\033[0m
    --rm                \033[33m最后删除构建的镜像\033[0m
";
}

[ $# -eq 0 ] && usage

ARGS=$(getopt -l "help,build,publish,dir:,image:,account:,tag:,rm" -o "hbpd:i:a:t:" -- "$@")
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
      Tag[${#Tag[@]}]=$2
      shift 2
      ;;
    -b|--build)
      Build="1"
      shift
      ;;
    -p|--publish)
      Publish="1"
      shift
      ;;
    --rm)
      Remove="1"
      shift
      ;;
    -h|--help)
      usage
      shift
      exit 0;
      ;;
    --)
      shift
      break
      ;;
    *)
      if [[ "$1" != 'error' ]]; then echo -ne "\nInvaild option: '$1'\n\n"; fi
      usage
      exit 1;
      ;;
  esac
done

[[ -z "$Dir" ]] && echo -ne "Error: Invalid option\n" && usage && exit 1;

TagStr=""
for a in "${Tag[@]}"; do
  TagStr="${TagStr:+${TagStr}} -t ${a}"
done

if [ "$Build" == '1' ]; then
  ./build.sh -d $Dir -i ${ImageName:-${Dir}} -a $DockerHubAccount $TagStr
fi

if [ "$Publish" == '1' ]; then
  ./publish.sh -i ${ImageName:-${Dir}} -a $DockerHubAccount
fi

if [ "$Remove" == '1' ]; then
  ./clean.sh -i ${ImageName:-${Dir}} -a $DockerHubAccount
fi
