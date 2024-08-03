import sys
sys.path.append('lib')
import colorama # type: ignore
from colorama import Fore, Back, Style # type: ignore
import signal
import sys
import math
import CHaser
import random
import copy

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
MV_B = "b"  #ブロックのメニューへ
MV_M = "m"  #基本メニューへ
MV_W = "w"  #上ポンメニューへ
MV_S = "s"  #Searchメニューへ
MV_LOOK = "l"  #Lookメニューへ

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

class clsWepon:
    """
    Wepon(武器)のクラス
    """

    # Wepon種類
    BOM = "BOM"
    CHAFF = "CHAFF"
    EYE = "EYE"
    BLOCK = "BLOCK"
    HELP = "HELP"

    # Wepon種類
    COMMAND_BOM = "bom"
    COMMAND_CHAFF = "c"
    COMMAND_EYE = "e"
    COMMAND_BLOCK = "b"
    COMMAND_RAND = "0"
    COMMAND_HELP = "h"

    #値
    Type = ""
    TypeCommand = ""
    Name = ""
    Cnt = 0
    IsRand = False

    def __init__(self,pType:str,pTypeCommand:str,pName:str,pCnt:int,pIsRand):
        if pName == "":
            self.Name = pType
        else:
            self.Name = pName

        self.Type = pType
        self.TypeCommand = pTypeCommand
        self.Cnt = pCnt
        self.IsRand = pIsRand
    
    def CleateMenuStr(self):
        '''
        武器のメニュー表示文字列を作成
        '''
        return f"{self.Name}({self.Cnt})"
    
    def CleateMenuStr(self):
        '''
        Weponメニュー
        '''
        return f"{self.Name}:{self.TypeCommand}"
    
    def CleateHelpStr(self):
        '''
        ヘルプの表示
        '''
        result = ""
        if self.Type == self.BLOCK :
            if self.IsRand == True:
                result = f"{self.Name} : フィ？ルド％ブロッ＊を置き？す＊"
            else:
                result = f"{self.BLOCK} : フィールドにブロックを置きます。"
        elif self.Type == self.CHAFF :
            if self.IsRand == True:
                result = f"{self.Name} : {R}未実装{RE} 相手の？図％示に＄％ングを＆＊ます。"
            else:
                result = f"{self.CHAFF} : {R}未実装{RE} 相手の地図表示にジャミングをかけます。"
        elif self.Type == self.BOM :
            if self.IsRand == True:
                result = f"{self.Name} : {R}未実装{RE} フィ？ルドに＊％弾を？？ます。自分＃は B と＠示さ＊＋相手には ?(OoooOOOooo) と表？＋＄れます。取＄＃H？が減＝ます。"
            else:
                result = f"{self.BOM} : {R}未実装{RE} フィールドに爆弾を置きます。自分には B と表示され、相手には $(アイテム) と表示されます。取るとHPが減ります。"
        elif self.Type == self.EYE :
            if self.IsRand == True:
                result = f"{self.Name} : {R}未実装{RE} 使＄する＊一定＃＊間表示＋る周＃マップ＠拡大＊＊れます。"
            else:
                result = f"{self.EYE} : {R}未実装{RE} 使用すると一定の時間表示される周辺マップが拡大されます。"
            
        return result

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

    # HP
    HP = 100

    # Exp
    Exp = 0
    NextExp = 100

    # Level
    Level = 1

    #装備しているWepon
    Wepon = []

    #Client
    Client = None

    def __init__(self,pCool_Hot:int,pClient:CHaser.Client):
        """
        コンストラクタ

        Args:
            pCool_Hot (int): CoolかHotか
            pClient (CHaser.Client): Clientのインスタンス

        """

        # Client
        self.Client = pClient

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
    
    def SetWepon(self,pWepon:list):
        """
        武器を持たせる
        """
        for wepon in pWepon:
            self.Wepon.append(copy.deepcopy(wepon))
    
    def ShowStatus(self):
        """
        ステータスの文字列を作成
        """
        WeponStrList = []
        for Wepon in self.Wepon:
            WeponStrList.append(Wepon.CleateMenuStr())

        if len(WeponStrList) <= 0:
            WeponStr = f'{R}Ops!! No Wepon...{RE}'
        else:
            WeponStr = ' / '.join(WeponStrList)

        print(f"Level:{self.Level} / HP:{self.HP} / Exp:{self.Exp}/{self.NextExp}")
        print(f"Wepon:[{WeponStr}]")

        return
    
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
    Player:clsPlayerData
    EnemyPlayer:clsPlayerData

    # ターン情報
    TurnCnt = 0

    # 武器の設定
    ## ランダムセットアイテム
    option = [clsWepon(clsWepon.BOM  ,clsWepon.COMMAND_RAND,"???"  ,1,True),
              clsWepon(clsWepon.CHAFF,clsWepon.COMMAND_RAND,"?????",1,True),
              clsWepon(clsWepon.EYE  ,clsWepon.COMMAND_RAND,"???"  ,3,True)]
    ramdomNo = random.randint(0, len(option) - 1)

    ## 武器
    Wepon = [clsWepon(clsWepon.BLOCK,clsWepon.COMMAND_BLOCK,"",999,False),
             clsWepon(clsWepon.BOM  ,clsWepon.COMMAND_BOM  ,"",1  ,False),
             clsWepon(clsWepon.CHAFF,clsWepon.COMMAND_CHAFF,"",2  ,False),
             clsWepon(clsWepon.EYE  ,clsWepon.COMMAND_EYE  ,"",5  ,False),
             option[ramdomNo],
             clsWepon(clsWepon.HELP ,clsWepon.COMMAND_HELP ,"",0,False)]
    
    def AddTurn(self):
        """
        ターンのカウント
        """
        self.TurnCnt += 1

    def CleateWeponMenu(self):
        """
        メニューに表示するWeponのメニューを作成する
        """
        tmpList = []
        for selWepon in self.Wepon:
            tmpList.append(selWepon.CleateMenuStr())

        return f"[Wepon] {' '.join(tmpList)} 未入力:Cancel ..."
    
    def CleateWeponHelp(self):
        """
        Weponヘルプを作成する
        """
        tmpList = []
        for selWepon in self.Wepon:
            tmpList.append(selWepon.CleateHelpStr())

        newline = '\n'
        return f"{B}-- Wepon Help --{RE}{newline}{newline.join(tmpList)}"
    
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
        self.Player.ShowStatus()
        print(f"{clsEtcValue.PRINT_LINE_NOMAL}") 
        return
    
    def GetPlayerColor(self):
        """
        プレイヤーカラーを取得
        """
        if self.Player.CoolHot == clsPlayerData.CH_COOL:
            return clsPlayerData.CH_COOL
        else:
            return clsPlayerData.CH_HOT
            
    def GetEnemyColor(self):
        """
        敵カラーを取得
        """
        if self.Player.CoolHot == clsPlayerData.CH_COOL:
            return clsPlayerData.CH_HOT
        else:
            return clsPlayerData.CH_COOL
        
    def SetWeponPlayer(self):
        """
        プレイヤーに武器を無理やり持たせる
        """
        self.Player.SetWepon(self.Wepon)
            

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

    # ゲームをなんとなく管理するGameMasterの設定
    GameMaster = clsGameMaster()
    GameMaster.Player = clsPlayerData(client.ChkCoolHot(False),client)
    GameMaster.EnemyPlayer = clsPlayerData(client.ChkCoolHot(True),client)

    # プレイヤーにWeponを装備してもらう
    GameMaster.SetWeponPlayer()

    # プレイヤー情報の参照コピー
    PlayerData = GameMaster.Player
    EnemyPlayerData = GameMaster.EnemyPlayer

    # 地図関連の管理（本当はGameMasterに管理してほしい...）
    AreaTable = clsAreaTable(3,3)
    AreaTableEx = clsAreaTalbeEx(101,PlayerData)

    # メイン処理
    BefInpVal = None
    while(True):

        GameMaster.AddTurn()

        value = client.get_ready()

        # タイトルの表示
        print(f"{PlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_ASTA}{RE}") 
        print(f"{PlayerData.PlayerColor} 自分のターン[Turn:{GameMaster.TurnCnt}]{RE}")
        #print(f"{PlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_ASTA}{RE}") 

        # 周辺の情報を表示
        AreaTable.SetAreaList(value)
        AreaTable.PrintArea(PlayerData,EnemyPlayerData,clsAction.AC_BEFOR)

        # その他ステータスの表示
        GameMaster.ShowGameStatus()

        while(True):

            IsMoveStep = True
            IsBlockStep = False
            IsWeponStep = False
            IsEndStep = False
            IsSearchStep = False
            IsLookStep = False

            #キー入力
            if BefInpVal == None :
                InpVal = input(f"[Move] ←:{MV_L} →:{MV_R} ↑:{MV_U} ↓:{MV_D} Serch:{MV_S} Look:{MV_LOOK} Wepon:{MV_W} ...")
            else :
                InpVal = input(f"[Move] ←:{MV_L} →:{MV_R} ↑:{MV_U} ↓:{MV_D} Serch:{MV_S} Look:{MV_LOOK} Wepon:{MV_W} Bef({BefInpVal}):未入力...")
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
            IsInputBefSetValue = False
            if InpVal == MV_L :
                value = client.walk_left()
                PlayerData.DoActionPlayer(clsAction.MV_LEFT,value)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_R :
                value = client.walk_right()
                PlayerData.DoActionPlayer(clsAction.MV_RIGHT,value)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_U :
                value = client.walk_up()
                PlayerData.DoActionPlayer(clsAction.MV_TOP,value)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_D :
                value = client.walk_down()
                PlayerData.DoActionPlayer(clsAction.MV_DOWN,value)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_S :
                IsSearchStep = True
            elif InpVal == MV_LOOK :
                IsLookStep = True
            elif InpVal == MV_W :
                IsWeponStep = True
            else :
                print(f"{R}入力値が不正です!!!{RE}")
                continue

            #前回と同じコマンドとして保存する場合
            if IsInputBefSetValue == True:
                BefInpVal = InpVal

            #Weponメニュー
            if IsWeponStep == True :
                while(True):

                    #キー入力
                    InpVal = input(f"{GameMaster.CleateWeponMenu()}")

                    if InpVal == clsWepon.COMMAND_BLOCK :
                        IsBlockStep = True
                        break
                    elif InpVal == clsWepon.COMMAND_HELP :
                        print(f"{GameMaster.CleateWeponHelp()}")
                        continue
                    else :
                        IsMoveStep = True
                        break

            #ブロックの設置メニュー
            if IsBlockStep == True :
                while(True):

                    #キー入力
                    InpVal = input(f"[Block] ←:{MV_L} →:{MV_R} ↑:{MV_U} ↓:{MV_D} 未入力:Cancel ...")

                    if InpVal == MV_L :
                        value = client.put_left()
                        PlayerData.DoActionPlayer(clsAction.PT_LEFT,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_R :
                        value = client.put_right()
                        PlayerData.DoActionPlayer(clsAction.PT_RIGHT,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_U :
                        value = client.put_up()
                        PlayerData.DoActionPlayer(clsAction.PT_UP,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_D :
                        value = client.put_down()
                        PlayerData.DoActionPlayer(clsAction.PT_DOWN,value)
                        IsEndStep = True
                        break
                    else :
                        IsMoveStep = True
                        break

            #Searchメニュー
            if IsSearchStep == True :
                while(True):

                    #キー入力
                    InpVal = input(f"[Search] ←:{MV_L} →:{MV_R} ↑:{MV_U} ↓:{MV_D} Cancel:未入力 ...")

                    if InpVal == MV_L :
                        value = client.search_left()
                        PlayerData.DoActionPlayer(clsAction.SR_LEFT,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_R :
                        value = client.search_right()
                        PlayerData.DoActionPlayer(clsAction.SR_RIGHT,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_U :
                        value = client.search_up()
                        PlayerData.DoActionPlayer(clsAction.SR_UP,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_D :
                        value = client.search_down()
                        PlayerData.DoActionPlayer(clsAction.SR_DOWN,value)
                        IsEndStep = True
                        break
                    else :
                        IsMoveStep = True
                        break

            #Lookメニュー
            if IsLookStep == True :
                while(True):

                    #キー入力
                    InpVal = input(f"[Look] ←:{MV_L} →:{MV_R} ↑:{MV_U} ↓:{MV_D} Cancel:未入力 ...")

                    if InpVal == MV_L :
                        value = client.look_left()
                        PlayerData.DoActionPlayer(clsAction.LO_LEFT,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_R :
                        value = client.look_right()
                        PlayerData.DoActionPlayer(clsAction.LO_RIGHT,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_U :
                        value = client.look_up()
                        PlayerData.DoActionPlayer(clsAction.LO_UP,value)
                        IsEndStep = True
                        break
                    elif InpVal == MV_D :
                        value = client.look_down()
                        PlayerData.DoActionPlayer(clsAction.LO_DOWN,value)
                        IsEndStep = True
                        break
                    else :
                        IsMoveStep = True
                        break

            if IsEndStep == True:
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
