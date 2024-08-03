import sys
sys.path.append('lib')
import colorama # type: ignore
from colorama import Fore, Back, Style # type: ignore
import signal
import sys
import math
import CHaser
import random

"""""
 # 起動方法

 ・Cool
   python KeyInputDo.py -c c

 ・Hot
   python KeyInputDo.py -c h

  ※接続情報は、CHaser.pyに記載してあります。探してみてね。

"""""

#定数　行動
MV_0 = "5"  #待機
MV_L = "4"  #左
MV_R = "6"  #右
MV_U = "2"  #上
MV_D = "8"  #下
MV_N = "n"  #次の行動へ
MV_B = "b"  #前の行動へ

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

class clsEtcValue:
    """
    その他定数
    """
    PRINT_LINE_NOMAL = "--------------------------------------------------------"
    PRINT_LINE_ASTA  = "********************************************************"

class clsItem:
    """
    アイテムの定数
    """
    NOMAL = 3    #得点
    WEPON = 400  #武器

class clsAction:
    """
    動作の定数
    """
    MV_WAITE = "MV_WAITE" # 移動：動かない
    # 移動：左
    MV_LEFT = "MV_LEFT"
    # 移動：下
    MV_DOWN = "MV_DOWN"
    # 移動：上
    MV_TOP = "MV_TOP"
    # 移動：右
    MV_RIGHT = "MV_RIGHT"
    # 見る：上
    LO_UP = "LO_UP"
    # 見る：左
    LO_LEFT = "LO_LEFT"
    # 見る：右
    LO_RIGHT = "LO_RIGHT"
    # 見る：下
    LO_DOWN = "LO_DOWN"
    # 検索：上
    SR_UP = "SR_UP"
    # 検索：左
    SR_LEFT = "SR_LEFT"
    # 検索：右
    SR_RIGHT = "SR_RIGHT"
    # 検索：下
    SR_DOWN = "SR_DOWN"
    # 置く：上
    PT_UP = "PT_UP"
    # 置く：左
    PT_LEFT = "PT_LEFT"
    # 置く：右
    PT_RIGHT = "PT_RIGHT"
    # 置く：下
    PT_DOWN = "PT_DOWN"

    #アクション
    AC_BEFOR = "AC_BEFOR"
    AC_AFTER = "AC_AFTER"

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

class clslogRowCol:
    """
    ログ情報
    """    
    col = 0
    row = 0
    Action:clsAction
    def __init__(self,pAction:clsAction,pCol:int,pRow:int):
        self.col = pCol
        self.row = pRow
        self.Action = pAction


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

    #プレイヤーの位置(当プログラムの内部的での位置)
    col = 0
    row = 0
    logColRow = []

    # CoolかHot
    CH_COOL = 0
    CH_HOT = 1
    CoolHot = CH_COOL

    # coolとhotの色
    ColorCool = Fore.CYAN
    ColorHot = Fore.MAGENTA

    # プレイヤーマーク
    MarkCool = "C"
    MarkHot = "H"

    #プレイヤーの色
    PlayerColor = ColorCool

    #プレイヤーマーク
    PlayerMark = MarkCool

    # Wepon
    class clsWepon:
        # Wepon種類
        BOM = "BOM"
        CHAFF = "CHAFF"
        EYE = "EYE"
        BLOCK = "BLOCK"

        #値
        Type = ""
        Name = ""
        Cnt = 0

        def __init__(self,pType:str,pName:str,pCnt:int):
            if pName == "":
                self.Name = pType
            else:
                self.Name = pName

            self.Type = pType
            self.Cnt = pCnt
        
        def showStr(self):
            return f"{self.Name}({self.Cnt})"
        
    # ランダムセットアイテム
    option = [clsWepon(clsWepon.BOM,"???",1),
              clsWepon(clsWepon.CHAFF,"?????",1),
              clsWepon(clsWepon.EYE,"???",3)]
    ramdomNo = random.randint(0, 2)

    # 武器の設定
    Wepon = [clsWepon(clsWepon.BOM,"",1),
             clsWepon(clsWepon.CHAFF,"",2),
             clsWepon(clsWepon.EYE,"",5),
             option[ramdomNo]]

    # HP
    HP = 100

    # Exp
    Exp = 0
    NextExp = 100

    # Level
    Level = 1

    def __init__(self,pCool_Hot:int):
        """
        コンストラクタ

        Args:
            pCool_Hot (int): CoolかHotか

        """

        #CoolかHotかを設定    
        self.CoolHot = pCool_Hot

        #プレイヤーの色を設定
        if self.CoolHot == self.CH_COOL:
            self.PlayerColor = self.ColorCool
            self.PlayerMark = self.MarkCool
        else:
            self.PlayerColor = self.ColorHot
            self.PlayerMark = self.MarkHot

        return
    
    def ShowStatus(self):
        """
        ステータスの文字列を作成
        """
        WeponStrList = []
        for Wepon in self.Wepon:
            WeponStrList.append(Wepon.showStr())
        WeponStr = ' / '.join(WeponStrList)

        print(f"Level:{self.Level} / HP:{self.HP} / Exp:{self.Exp}/{self.NextExp}")
        print(f"Wepon:[{WeponStr}]")

        return
    
    def GetItem(self,pItem:clsItem):
        """
        アイテムの保存
        """
        self.cntItem.append(pItem)

    def setDirection(self,pDr):
        """
        プレイヤーの方向を設定する
        """    
        self.direction = pDr
        return
    
    def setPosition(self,pCol:int,pRow:int):
        """
        プレイヤーの位置を設定する
        """    
        self.col = pCol
        self.row = pRow
        return
    
    def DoActionPlayer(self,pAction:clsAction,pAreaList:list):
        """
        移動したときのプレイヤーの設定
        """

        #履歴を残す(後で何かにつかう)
        self.logColRow.append(clslogRowCol(pAction,self.col,self.row))

        if (pAction == clsAction.MV_WAITE or
            pAction == clsAction.MV_TOP or 
            pAction == clsAction.MV_DOWN or
            pAction == clsAction.MV_LEFT or
            pAction == clsAction.MV_RIGHT):
            # 移動

            Dr = clsPlayerData.DR_DF
            if pAction == clsAction.MV_WAITE:
                Dr = clsPlayerData.DR_DF
            elif pAction == clsAction.MV_TOP:
                Dr = clsPlayerData.DR_TP
            elif pAction == clsAction.MV_DOWN:
                Dr = clsPlayerData.DR_DW
            elif pAction == clsAction.MV_LEFT:
                Dr = clsPlayerData.DR_LF
            elif pAction == clsAction.MV_RIGHT:
                Dr = clsPlayerData.DR_RI

            # 方向
            self.setDirection(Dr)

            # 位置
            if Dr == clsPlayerData.DR_DF :
                #待機
                pass
            elif Dr == clsPlayerData.DR_LF :
                self.col -= 1
            elif Dr == clsPlayerData.DR_RI :
                self.col += 1
            elif Dr == clsPlayerData.DR_TP :
                self.row -= 1
            elif Dr == clsPlayerData.DR_DW :
                self.row += 1         

class clsGameMaster:
    """
    ゲームマスター（ゲームの管理）のクラス
    """  
    # プレイヤーの得点  
    MePoint = 0
    EnemyPoint = 0

    # プレイヤー情報
    MePlayer:clsPlayerData
    EnemyPlayer:clsPlayerData

    def AddMePoint(self,pItem:clsItem):
        """
        自分の点数加算
        """    
        if pItem == clsItem.NOMAL:
            self.MePoint = 1
    
    def ShowGameStatus(self):
        """
        ゲームのステータス表示
        """
        print(f"{clsEtcValue.PRINT_LINE_NOMAL}") 
        self.MePlayer.ShowStatus()
        print(f"{clsEtcValue.PRINT_LINE_NOMAL}") 
        return
    
    def GetPlayerColor(self):
        if self.MePlayer.CoolHot == clsPlayerData.CH_COOL:
            return clsPlayerData.CH_HOT

class clsAreaTalbeEx:
    """
    周辺の情報を退避するクラス
    """ 
    cols = 31     #必ず奇数を設定
    rows = cols
    player = None
    arealist = []
    def __init__(self,pSize:int,pPlayer:clsPlayerData):
        """
        コンストラクタ

            ・退避するリストのサイズを設定
            ・プレイヤーの初期位置を設定

        Args:
            pSize (int): 退避する領域の列数と行数(必ず奇数)
            pPlayer (clsPlayerData): プレイヤー情報
        """    
        self.cols = pSize
        self.rows = pSize
        self.player = pPlayer
        self.arealist = [[None for _ in range(self.cols)] for _ in range(self.rows)]
        self.player.setPosition(math.ceil(self.cols / 2) - 1,math.ceil(self.rows / 2) - 1)

    def addArea(self,pArea:list,pAction:int):
        """
        周辺情報の追加
        Args:
            pArea (list): 追加する周辺情報
            pAction (int): 周辺情報を取得した時の動作
        """    



class clsAreaTable:
    """
    周辺の情報を退避するクラス
    """    
    cols = 0
    rows = 0
    arealist = []
    
    A_PLAYER_ME = 10
    A_PLAYER_EM = 1
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
    
    def AddAreaList(self,pArea:list):
        """
        周辺の情報を設定する
        """
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
    
    def PrintArea(self,pPlayerData:clsPlayerData,pEnemyPlayerData:clsPlayerData,pMode:clsAction):
        """
        周辺の状態をコンソールに出力する
        """
        curCol = 0
        curRow = 0

        print(f"{clsEtcValue.PRINT_LINE_NOMAL}") 
        if pMode == clsAction.AC_BEFOR:
            print("周辺マップ [行動前]")
        elif pMode == clsAction.AC_AFTER:
            print("周辺マップ [行動後]")
        else:
            print("周辺マップ")
        print(f"{clsEtcValue.PRINT_LINE_NOMAL}") 

        for row in self.arealist:
            for field in row:

                # 地図の表示モードによってプレイヤーの位置の表示方法を設定する
                if self.PrintAreaPutPlayerMode == self.P_3x3:
                    if curCol == 1 and curRow == 1:
                        field = self.A_PLAYER_ME

                # プレイヤー
                if field == self.A_PLAYER_ME:
                    Coler = pPlayerData.PlayerColor
                    if pPlayerData.direction == clsPlayerData.DR_TP:
                        print(f"{Coler}^ {RE}",end="")
                    elif pPlayerData.direction == clsPlayerData.DR_DW:
                        print(f"{Coler}v {RE}",end="")
                    elif pPlayerData.direction == clsPlayerData.DR_LF:
                        print(f"{Coler}< {RE}",end="")
                    elif pPlayerData.direction == clsPlayerData.DR_RI:
                        print(f"{Coler}> {RE}",end="")
                    else:
                        print(f"{Coler}+ {RE}",end="")
                elif field == self.A_BLOCK:
                        print("# ",end="")
                elif field == self.A_ITEM:
                        print(f"{Y}$ {RE}",end="")
                elif field == self.A_PLAYER_EM:
                    #敵の表示
                    print(f"{pEnemyPlayerData.PlayerColor}{pEnemyPlayerData.PlayerMark} {RE}",end="")
                else:
                    print(". ",end="")
            
                curRow += 1

            #改行
            print()

            curCol += 1
            curRow = 0
    
def main():
    
    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス

    GameMaster = clsGameMaster()
    AreaTable = clsAreaTable(3,3)

    PlayerData = clsPlayerData(client.ChkCoolHot(False))
    EnemyPlayerData = clsPlayerData(client.ChkCoolHot(True))

    GameMaster.MePlayer = PlayerData
    GameMaster.EnemyPlayer = EnemyPlayerData

    AreaTableEx = clsAreaTalbeEx(101,PlayerData)

    BefInpVal = None

    cntTurn = 0
    
    while(True):

        cntTurn += 1

        value = client.get_ready()

        # タイトルの表示
        print(f"{PlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_ASTA}{RE}") 
        print(f"{PlayerData.PlayerColor} 自分のターン[Turn:{cntTurn}]{RE}")
        #print(f"{PlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_ASTA}{RE}") 

        # 周辺の情報を表示
        AreaTable.SetAreaList(value)
        AreaTable.PrintArea(PlayerData,EnemyPlayerData,clsAction.AC_BEFOR)

        # その他ステータスの表示
        GameMaster.ShowGameStatus()

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
                valueTmp = client.search_up()
                PlayerData.DoActionPlayer(clsAction.MV_WAITE,valueTmp)
            elif InpVal == MV_L :
                value = client.walk_left()
                PlayerData.DoActionPlayer(clsAction.MV_LEFT,value)
            elif InpVal == MV_R :
                value = client.walk_right()
                PlayerData.DoActionPlayer(clsAction.MV_RIGHT,value)
            elif InpVal == MV_U :
                value = client.walk_up()
                PlayerData.DoActionPlayer(clsAction.MV_TOP,value)
            elif InpVal == MV_D :
                value = client.walk_down()
                PlayerData.DoActionPlayer(clsAction.MV_DOWN,value)
            elif InpVal == MV_N :
                IsNextStep = True
            else :
                print(f"{R}入力値が不正です!!!{RE}")
                continue

            BefInpVal = InpVal

            #移動をせずに、次の処理を行う場合
            #ブロックの設置
            if IsNextStep == True :
                while(True):

                    #キー入力
                    InpVal = input("[ブロックを置く] 5:待機 4:← 6:→ 2:↑ 8:↓ 戻る:b ...")

                    if InpVal == MV_0 : 
                        #待機
                        value = client.search_up()
                        PlayerData.DoActionPlayer(clsAction.SR_UP,value)
                    elif InpVal == MV_L :
                        value = client.put_left()
                        PlayerData.DoActionPlayer(clsAction.PT_LEFT,value)
                    elif InpVal == MV_R :
                        value = client.put_right()
                        PlayerData.DoActionPlayer(clsAction.PT_RIGHT,value)
                    elif InpVal == MV_U :
                        value = client.put_up()
                        PlayerData.DoActionPlayer(clsAction.PT_UP,value)
                    elif InpVal == MV_D :
                        value = client.put_down()
                        PlayerData.DoActionPlayer(clsAction.PT_DOWN,value)
                    else :
                        continue

                    break

        #周辺の情報を表示
        AreaTable.SetAreaList(value)
        AreaTable.PrintArea(PlayerData,EnemyPlayerData,clsAction.AC_AFTER)

        # その他ステータスの表示
        GameMaster.ShowGameStatus()

        #print(f"{EnemyPlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_NOMAL}{RE}") 
        print("")
        print(f"{EnemyPlayerData.PlayerColor} 相手のターン...please wait{RE}")
        print("")
        #print(f"{EnemyPlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_NOMAL}{RE}") 

if __name__ == "__main__":
    main()
