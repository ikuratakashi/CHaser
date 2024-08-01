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
C = Fore.CYAN
M = Fore.MAGENTA
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

class clsPlayerData:
    """
    プレイヤーのクラス
    """    

    # 向いている方向
    DR_DF = 0   #初期値
    DR_TP = 1   #上
    DR_DW = 8   #下
    DR_LF = 3   #左
    DR_RI = 2   #右

    direction = DR_DF   #現在の方向

    # CoolかHot
    CH_COOL = 0
    CH_HOT = 1
    CoolHot = CH_COOL

    def __init__(self,pCool_Hot:int):
        """
        コンストラクタ

        Args:
            pCool_Hot (int): CoolかHotか

        """    
        self.CoolHot = pCool_Hot
        return

    def setDirection(self,pDf):
        """
        プレイヤーの方向を設定する
        """    
        self.direction = pDf
        return

class clsAreaTable:
    """
    周辺の情報を退避するクラス
    """    
    cols = 0
    rows = 0
    arealist = []
    
    A_PLAYER = 1
    A_BLOCK = 2
    A_ITEM = 3

    #周辺情報のプレイヤーの表示モード
    P_3x3 = 1   #3x3の周辺情報
    P_REAL = 2  #フィールド全体
    PrintAreaPutPlayerMode = P_3x3

    def __init__(self,pCols:int,pRows:int):
        """
        コンストラクタ
        """    
        self.cols = pCols
        self.rows = pRows
        return
    
    def SetAreaList(self,pArea:list):
        """
        周辺の情報を設定する
        """
        self.arealist = []    
        self.arealist = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        col = 0
        row = 0
        for field in pArea:
            if row <= self.rows - 1:
                self.arealist[col][row] = field
                row += 1
                if row >= self.rows:
                    col += 1
                    row = 0
            else:
                break
        return
    
    def PrintArea(self,pPData:clsPlayerData):
        """
        周辺の状態をコンソールに出力する
        """
        curCol = 0
        curRow = 0
        print("-- 周辺マップ --")
        for row in self.arealist:
            for field in row:

                # 地図の表示モードによってプレイヤーの位置の表示方法を設定する
                if self.PrintAreaPutPlayerMode == self.P_3x3:
                    if curCol == 1 and curRow == 1:
                        field = self.A_PLAYER

                # プレイヤー
                if field == self.A_PLAYER:

                    Coler = 0
                    if pPData.CoolHot == clsPlayerData.CH_COOL:
                        Coler = C
                    else:
                        Coler = M

                    if pPData.direction == clsPlayerData.DR_TP:
                        print(f"{Coler}^ {RE}",end="")
                    elif pPData.direction == clsPlayerData.DR_DW:
                        print(f"{Coler}v {RE}",end="")
                    elif pPData.direction == clsPlayerData.DR_LF:
                        print(f"{Coler}< {RE}",end="")
                    elif pPData.direction == clsPlayerData.DR_RI:
                        print(f"{Coler}> {RE}",end="")
                    else:
                        print(f"{Coler}+ {RE}",end="")
                elif field == self.A_BLOCK:
                        print("# ",end="")
                elif field == self.A_ITEM:
                        print("$ ",end="")
                else:
                    print("  ",end="")
            
                curRow += 1

            #改行
            print()

            curCol += 1
            curRow = 0
    
def main():
    
    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス

    AreaTable = clsAreaTable(3,3)
    PlayerData = clsPlayerData(client.ChkCoolHot())

    BefInpVal = None
    
    while(True):

        value = client.get_ready()

        #周辺の情報を表示
        AreaTable.SetAreaList(value)
        AreaTable.PrintArea(PlayerData)
        
        print(f"{G}*自分のターン{RE}")
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
                PlayerData.direction = clsPlayerData.DR_DF
            elif InpVal == MV_L :
                value = client.walk_left()
                PlayerData.direction = clsPlayerData.DR_LF
            elif InpVal == MV_R :
                value = client.walk_right()
                PlayerData.direction = clsPlayerData.DR_RI
            elif InpVal == MV_U :
                value = client.walk_up()
                PlayerData.direction = clsPlayerData.DR_TP
            elif InpVal == MV_D :
                value = client.walk_down()
                PlayerData.direction = clsPlayerData.DR_DW
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

        #周辺の情報を表示
        AreaTable.SetAreaList(value)
        AreaTable.PrintArea(PlayerData)
        
        print(f"{B}*相手のターン{RE}")

if __name__ == "__main__":
    main()
