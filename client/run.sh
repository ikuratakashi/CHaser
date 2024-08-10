#!/bin/bash

#シェルを作成したら、実行権限を当ててください
# chmod +x run.sh

# 起動パラメータ
# -n 名前
# -p ポート2009(COOL)、2010(HOT)
# -h ホストのIP

# 引数に応じた動作を実行
case $1 in
  c)
    echo "COLL Run"
    python CHaserGame.py -n COOL -p 2009 -h 192.168.3.15
    ;;
  h)
    echo "HOT Run"
    python CHaserGame.py -n HOT -p 2010 -h 192.168.3.15
    ;;
  *)
    echo "引数が設定されていません: $1"
    echo "実行方法: $0 {c|h}"
    exit 1
    ;;
esac

