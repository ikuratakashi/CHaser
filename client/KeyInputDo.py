import sys
sys.path.append('lib\python\colorama')
import colorama
from colorama import Fore, Back, Style
import signal
import sys

import CHaser

#定数　行動
MV_0 = "5"  #待機
MV_L = "4"  #左
MV_R = "6"  #右
MV_U = "2"  #上
MV_D = "8"  #下
MV_N = "n"  #次の行動へ

#定数 方向
CH_T = 2
CH_D = 8
CH_L = 4
CH_R = 6

#定数 状態
NON = 0 #何もない
ENM = 1 #敵
BLC = 2 #ブロック
ITM = 3 #アイテム

# ANSIエスケープシーケンス
colorama.init()
R = Fore.RED
G = Fore.GREEN
Y = Fore.YELLOW
B = Fore.BLUE
RE = Style.RESET_ALL

def signal_handler(sig, frame):
    """
    Ctrl+Cが押された時の処理
    """
    print(f"{R}\nCtrl+Cが押されました。プログラムを終了します。")
    colorama.deinit()
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

def IsBlock(pValue,pNext):
    """
    移動しようとしている方向にブロックがあるかどうかを返す

    Args:
        pValue (list of int): 周りの状況配列
        pNext (int): 次に移動する先の値 0から

    Returns:
        bool: True:あり False:なし
    """    
    Result = False

    #print(pValue)
    #print(f"next={pNext}")

    if pValue[pNext] == BLC:
        Result = True

    return Result

def IsInt(s):
    """
    引数の値が数値かどうかを判定

    Args:
        s (string): 値

    Returns:
        bool: True:数値 False:数値以外
    """    
    try:
        int(s)
        return True
    except ValueError:
        return False
    
def main():
    
    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス

    BefInpVal = None
    
    while(True):

        value = client.get_ready()
        print(f"{G}*自分のターン*************{RE}")

        IsNextStep = False

        while(True):

            #キー入力
            if BefInpVal == None :
                InpVal = input("[移動] 5:待機 4:← 6:→ 2:↑ 8:↓ n:次 ...")
            else :
                InpVal = input(f"[移動] 5:待機 4:← 6:→ 2:↑ 8:↓ n:次 前回({BefInpVal}):未入力 ...")
                if InpVal == "":
                    InpVal = BefInpVal

            #移動先がブロックかどうかの判定
            IntInpVal = 0
            if IsInt(InpVal) == True :
                IntInpVal = int(InpVal) - 1
                if IsBlock(value,IntInpVal) == True :
                    Quest = input(f"{R}移動先はブロックですが、移動しますか？{RE} y/n...")
                    if Quest == "n" or Quest == "" :
                        continue

            #移動
            if InpVal == MV_0 :
                #待機
                client.search_up()
            elif InpVal == MV_L :
                client.walk_left()
            elif InpVal == MV_R :
                client.walk_right()
            elif InpVal == MV_U :
                client.walk_up()
            elif InpVal == MV_D :
                client.walk_down()
            elif InpVal == MV_N :
                IsNextStep = True
            else :
                print(f"{R}入力値が不正です!!!{RE}")
                continue

            BefInpVal = InpVal

            break
        
        #移動をせずに、次の処理を行う場合
        #ブロックの設置
        if IsNextStep == True :
            while(True):

                #キー入力
                InpVal = input("[ブロックを置く] 5:待機 4:← 6:→ 2:↑ 8:↓ ...")

                if InpVal == MV_0 : 
                    #待機
                    client.search_up()
                elif InpVal == MV_L :
                    client.put_left()
                elif InpVal == MV_R :
                    client.put_right()
                elif InpVal == MV_U :
                    client.put_up()
                elif InpVal == MV_D :
                    client.put_down()
                else :
                    continue

                break
        print(f"{B}*相手のターン*************{RE}")

if __name__ == "__main__":
    main()
