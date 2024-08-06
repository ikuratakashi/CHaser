import sys
sys.path.append('lib')
import colorama # type: ignore
from colorama import Fore, Back, Style # type: ignore
import pyfiglet # type: ignore
from pyfiglet import Figlet # type: ignore
import psutil  # type: ignore
import signal
import sys
import math
import CHaser
import random
import copy
from enum import Enum
import time
import numpy as np # type: ignore
import sounddevice as sd # type: ignore

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
    MV_UP = "MV_UP"
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
    AC_BEFOR  = "AC_BEFOR"
    AC_AFTER  = "AC_AFTER"
    AC_SEARCH = "SEARCH"
    AC_LOOK   = "LOOK"
    AC_WEPON  = "WEPON"

def signal_handler(sig, frame):
    """
    Ctrl+Cが押された時の処理
    """
    print(f"{R}\nCtrl+Cが押されました。プログラムを終了します。")
    colorama.deinit()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

class clsBeep:
    """
    beep音のクラス
    """    
    # サンプリングレート
    sample_rate = 44100

    # 音の周波数（Hz）と持続時間（秒）のペア
    SE_PIPO = "SE_PIPO"
    SE_KEYINPUT = "SE_KEYINPUT"
    SE_OK = "SE_OK"
    SE_NG = "SE_NG"
    notes = {   
                SE_PIPO:
                [
                    (1000, 0.1),  # 高音（1000 Hz）0.1秒（「ぴ」）
                    (500, 0.1),   # 低音（500 Hz）0.1秒（「ぽ」）
                    (1000, 0.1)   # 高音（1000 Hz）0.1秒（「っ」）
                ],
                SE_OK:
                [
                    (1500, 0.01)    # 低音（500 Hz）0.1秒（「」）
                ],
                SE_NG:
                [
                    (500, 0.01)    # 低音（500 Hz）0.1秒（「」）
                ]
    }
    
    def generate_tone(self,frequency, duration, sample_rate):
        """
        各音の信号を生成
        """
        t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
        signal = 0.5 * np.sin(2 * np.pi * frequency * t)
        return signal

    def generate_sequence(self,notes, sample_rate):
        """
        シーケンスを生成
        """
        sequence = np.concatenate([self.generate_tone(frequency, duration, sample_rate) for frequency, duration in notes])
        return sequence
    
    def CreateSound(self,pKey):
        """
        音を作る
        """
        # 音を生成
        return self.generate_sequence(self.notes[pKey], self.sample_rate)

    def SoundStart(self,pSound,pIsWait:bool = False):
        """
        再生
        """
        # 音を再生
        sd.play(pSound, self.sample_rate)
        # 再生が終わるのを待つ
        if pIsWait:
            sd.wait()
            time.sleep(0.3)
            

class clsSystemAdministrator:
    """
    システムクラス
    """    
    Version = "FG204 2nd EDITION Ver2.31"

    def StartupSound(self):
        """
        起動音のようなものを鳴らす
        """
        sound = clsBeep().CreateSound(clsBeep.SE_PIPO)
        clsBeep().SoundStart(sound,True)

    def TitleShow(self) :
        """
        起動タイトルの表示
        """
        figlet = Figlet()
        self.PrintTextDelay(figlet.renderText("CHaser GAME"),0.001)
        print(f"-- {self.Version} --")
        print()
        print(f"{B}[System Initialization]{RE}")

        # システム起動
        self.Initialize()

    class clsInitList:
        """
        初期化項目
        """
        Item:str = ""
        Action:str = ""
        Result:str = ""
        def __init__(self,pItem:str,pAction:str,pResult:str):
            self.Item = pItem
            self.Action = pAction
            self.Result = pResult
        
        def Run(self):
            """
            実行
            """
            print(f"{self.Item} {self.Action} ",end='')
            delay = random.randint(1, 2) / 800
            cnt = 40 - len(self.Item) - len(self.Action)
            print(G,end="")
            self.PrintTextDelay('━' * cnt,delay)
            print(RE,end="")

            if self.Item == "MEMORY-VMS":
                process = psutil.Process()
                memory_info = process.memory_info()  
                str =  f"[{memory_info.vms} Byte]"
                print(f" {self.Result} {str}")
            elif self.Item == "MEMORY-RSS":
                process = psutil.Process()
                memory_info = process.memory_info()  
                str =  f"[{memory_info.rss} Byte]"
                print(f" {self.Result} {str}")
            else:
                print(f" {self.Result}")

        def PrintTextDelay(self,text: str, delay: float = 0.1) -> None:
            """
            指定されたテキストを一文字ずつ順番に表示します。
            Args:
                text (str): 表示するテキスト
                delay (float): 各文字を表示する間隔（秒）
            """
            counter = 0
            for char in text:
                print(char, end='', flush=True)
                time.sleep(delay)
                counter += 1 
                if delay <= 0.001:
                    if counter % 10 == 0:
                        time.sleep(delay)
                else:
                    time.sleep(delay)
    
    def Initialize(self):
        """
        システムの初期化
        """
        InitList = [ 
                     self.clsInitList("MEMORY-VMS","Check",f"{G}OK{RE}")
                    ,self.clsInitList("MEMORY-RSS","Check",f"{G}OK{RE}")
                    ,self.clsInitList("BIOS","Loading",f"{G}OK{RE}")
                    ,self.clsInitList("ASURA","Loading",f"{G}OK{RE}")
                    ,self.clsInitList("BABEL","Loading",f"{G}OK{RE}")
                    ,self.clsInitList("L.O.S","Loading",f"{R}NG{RE} [Update To HOS]")
                    ,self.clsInitList("HOS","DownLoading",f"{G}OK{RE}")
                    ,self.clsInitList("HOS System","Updateing",f"{G}OK{RE} [L.O.S -> HOS(ver.shige)]")
                    ,self.clsInitList("HOS System","Loading",f"{G}OK{RE}")
                    ,self.clsInitList("ISO27001","Check",f"{G}OK{RE}")
                   ]
    
        #se_ok = clsBeep().CreateSound(clsBeep.SE_OK)
        #se_ng = clsBeep().CreateSound(clsBeep.SE_NG)

        for InitItem in InitList:
            InitItem.Run()
            """
            if "OK" in InitItem.Result :
                clsBeep().SoundStart(se_ok)
            else:
                clsBeep().SoundStart(se_ng)
            """

        print(f"<<Result : {G}ALL GREEN{RE}>>")
        print()
        print()
        self.PrintTextDelay("Wellcome To CHaser Game.",0.007)
        print()
        print()

    def PrintTextDelay(self,text: str, delay: float = 0.1) -> None:
        """
        指定されたテキストを一文字ずつ順番に表示します。
        Args:
            text (str): 表示するテキスト
            delay (float): 各文字を表示する間隔（秒）
        """
        counter = 0
        for char in text:
            print(char, end='', flush=True)
            counter += 1 
            if delay <= 0.001:
                if counter % 10 == 0:
                    time.sleep(delay)
            else:
                time.sleep(delay)

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
    FieldList:list
    def __init__(self,pAction:clsAction,pFieldList:list,pCol:int,pRow:int):
        self.col = pCol
        self.row = pRow
        self.Action = pAction
        self.FieldList = list(pFieldList)

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

        if pIsRand == True:
            self.Type = f"{pType}_RRRR"
        else:
            self.Type = pType

        self.TypeCommand = pTypeCommand
        self.Cnt = pCnt
        self.IsRand = pIsRand
    
    def CleateStatusStr(self) -> str:
        '''
        武器のメニュー表示文字列を作成
        '''
        return f"{self.Name}({self.Cnt})"
    
    def CleateMenuStr(self,pCommandColor:str):
        '''
        Weponメニュー
        '''
        return f"{self.Name}:{pCommandColor}{self.TypeCommand}{RE}"
    
    def CleateHelpStr(self):
        '''
        ヘルプの表示
        '''
        result = ""
        ChkType = self.Type.replace("_RRRR","") 
        if ChkType == self.BLOCK :
            # BLOCK
            if self.IsRand == True:
                result = f"{self.Name} : フィ？ルド％ブロッ＊を置き？す＊"
            else:
                result = f"{self.BLOCK} : フィールドにブロックを置きます。"
        elif ChkType == self.CHAFF :
            # CHAFF
            if self.IsRand == True:
                result = f"{self.Name} : {R}未実装{RE} 相手の？図％示に＄％ングを＆＊ます。"
            else:
                result = f"{self.CHAFF} : {R}未実装{RE} 相手の地図表示にジャミングをかけます。"
        elif ChkType == self.BOM :
            # BOM
            if self.IsRand == True:
                result = f"{self.Name} : {R}未実装{RE} フィ？ルドに＊％弾を？？ます。自分＃は B と＠示さ＊＋相手には ?(OoooOOOooo) と表？＋＄れます。取＄＃H？が減＝ます。"
            else:
                result = f"{self.BOM} : {R}未実装{RE} フィールドに爆弾を置きます。自分には B と表示され、相手には $(アイテム) と表示されます。取るとHPが減ります。"
        elif ChkType == self.EYE :
            # EYE
            if self.IsRand == True:
                result = f"{self.Name} : {R}未実装{RE} 使＄する＊一定＃＊間表示＋る周＃マップ＠拡大＊＊れます。"
            else:
                result = f"{self.EYE} : {R}未実装{RE} 使用すると一定の時間表示される周辺マップが拡大されます。"
            
        return result
    
    def UseWepon(self,pCnt:int=1):
        """
        武器の使用
        """    
        self.Cnt -= pCnt

    def AddWepon(self,pCnt:int=1):
        """
        武器の回数追加
        """    
        self.Cnt += pCnt

class clsWepons:
    """
    武器の管理
    """

    # 武器の辞書
    Wepons = {}

    def AddWepon(self,pWepon:clsWepon):
        """
        武器の追加
        """
        self.Wepons.update({pWepon.Type:copy.deepcopy(pWepon)})
    
    def GetWepon(self,pType:str) -> clsWepon:
        """
        武器をタイプによって返す
        """
        return self.Wepons[pType]
    
    def GetWepons(self) -> list[clsWepon]:
        """
        武器をリストにして返す
        """
        result:list[clsWepon] = []
        for key,wepon in self.Wepons.items():
            result.append(wepon)
        return result 

class enmActionResult(Enum):
    """
    行動の結果の定数クラス
    """    
    BLOCK = 1 #移動先がブロック
    OK = 0 #OK

class clsActionResult:
    """
    行動の結果クラス
    """    
    FieldList: list = []
    Action: clsAction = None
    Result: enmActionResult = None

class clsDirection:
    """
    向いている方向
    """    
    DF = 0   #初期値
    UP = 1   #上
    DW = 8   #下
    LF = 3   #左
    RI = 2   #右

class clsLookDirection:
    """
    見ている方向
    """    
    DF = 0   #初期値
    UP = 1   #上
    DW = 8   #下
    LF = 3   #左
    RI = 2   #右

class clsPlayerData:
    """
    プレイヤーのクラス
    """    

    # 向いている方向(行動でロジックを判定するときに使用する)
    direction:clsDirection = clsDirection.DF

    # 見ている方向(向いている方向を画面に表示する時に使用する)
    LookDirection:clsLookDirection = clsLookDirection.DF

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
    Wepons:clsWepons = clsWepons()

    #Client
    Client:CHaser.Client = None


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
    
    def SetWepon(self,pWepons:clsWepons):
        """
        武器を持たせる
        """
        self.Wepons = copy.deepcopy(pWepons)

    def ShowStatus(self):
        """
        ステータスの文字列を作成

        # GameMasterに処理があった方がよいかも
        """

        WeponStrList = []

        for Wepon in self.Wepons.GetWepons():
            if Wepon.Type != clsWepon.HELP:
                WeponStrList.append(Wepon.CleateStatusStr())

        if len(WeponStrList) <= 0:
            WeponStr = f'{R}Ops!! No Wepon...{RE}'
        else:
            WeponStr = ' / '.join(WeponStrList)

        print(f"Level:{self.Level} / HP:{self.HP} / Exp:{self.Exp}/{self.NextExp}")
        print(f"Wepon:{WeponStr}")

        return
    
    def setDirection(self,pDr:clsDirection):
        """
        プレイヤーの方向を設定する（行動のロジックで使用する）
        """    
        self.direction = pDr
        return
    
    def setLookDirection(self,pDr:clsLookDirection):
        """
        プレイヤーの方向を設定する（向いている方向を画面に表示するときに使用する）
        """    
        self.LookDirection = pDr
        return
    
    def setPosition(self,pCol:int,pRow:int):
        """
        プレイヤーの位置を設定する
        """    
        self.col = pCol
        self.row = pRow
        return
    
    def DoActionPlayerTest(self,pAction:clsAction,pAreaList:list) -> clsActionResult:
        """
        プレイヤーの行動テスト
        Args:
            pAction (clsAction): 行動種類
            pAreaList (list): 行動時の周辺情報 3x3
        Returns:
            clsActionResult: 行動結果
        """
        result = clsActionResult()
        result.Action = pAction 
        result.Result = enmActionResult.OK

        if (pAction == clsAction.MV_UP or 
            pAction == clsAction.MV_DOWN or
            pAction == clsAction.MV_LEFT or
            pAction == clsAction.MV_RIGHT):

            # 移動 #1
            if pAction == clsAction.MV_UP:
                if self.IsBlock(pAreaList, MV_U) == True:
                    result.Result = enmActionResult.BLOCK
            elif pAction == clsAction.MV_DOWN:
                if self.IsBlock(pAreaList, MV_D):
                    result.Result = enmActionResult.BLOCK
            elif pAction == clsAction.MV_LEFT:
                if self.IsBlock(pAreaList, MV_L):
                    result.Result = enmActionResult.BLOCK
            elif pAction == clsAction.MV_RIGHT:
                if self.IsBlock(pAreaList, MV_R):
                    result.Result = enmActionResult.BLOCK
        
        return result

    def IsBlock(pValue:list,pNext:int) -> bool:
        """
        移動しようとしている方向にブロックがあるかどうかを返す

        Args:
            pValue (list of int): 周りの状況配列
            pNext (int): 次に移動する先の値 0から

        Returns:
            bool: True:あり False:なし
        """    
        Result = False
        if pValue[pNext] == BLC:
            Result = True
        return Result

    def DoActionPlayer(self,pAction:clsAction,pAreaList:list) -> clsActionResult:
        """
        プレイヤーの行動
        Args:
            pAction (clsAction): 行動種類
            pAreaList (list): 行動時の周辺情報 3x3
        Returns:
            clsActionResult: 行動結果
        """

        result = clsActionResult()
        result.Action = pAction 
        Dr = self.direction
        LDr = self.LookDirection

        #履歴を残す(後で何かにつかう)
        self.logColRow.append(clslogRowCol(pAction,pAreaList,self.col,self.row))

        if (pAction == clsAction.MV_UP or 
            pAction == clsAction.MV_DOWN or
            pAction == clsAction.MV_LEFT or
            pAction == clsAction.MV_RIGHT):

            # 移動
            if pAction == clsAction.MV_UP:
                Dr = clsDirection.UP
                LDr = clsLookDirection.UP
                result.FieldList = self.Client.walk_up()
            elif pAction == clsAction.MV_DOWN:
                Dr = clsDirection.DW
                LDr = clsLookDirection.DW
                result.FieldList = self.Client.walk_down()
            elif pAction == clsAction.MV_LEFT:
                Dr = clsDirection.LF
                LDr = clsLookDirection.LF
                result.FieldList = self.Client.walk_left()
            elif pAction == clsAction.MV_RIGHT:
                Dr = clsDirection.RI
                LDr = clsLookDirection.RI
                result.FieldList = self.Client.walk_right()

            # 位置
            if Dr == clsDirection.LF :
                self.col -= 1
            elif Dr == clsDirection.RI :
                self.col += 1
            elif Dr == clsDirection.UP :
                self.row -= 1
            elif Dr == clsDirection.DW :
                self.row += 1

        elif (pAction == clsAction.PT_UP or 
              pAction == clsAction.PT_DOWN or
              pAction == clsAction.PT_LEFT or
              pAction == clsAction.PT_RIGHT):
            
            # ブロックを置く
            if pAction == clsAction.PT_UP:
                LDr = clsLookDirection.UP
                result.FieldList = self.Client.put_up()
            elif pAction == clsAction.PT_DOWN:
                LDr = clsLookDirection.DW
                result.FieldList = self.Client.put_down()
            elif pAction == clsAction.PT_LEFT:
                LDr = clsLookDirection.LF
                result.FieldList = self.Client.put_left()
            elif pAction == clsAction.PT_RIGHT:
                LDr = clsLookDirection.RI
                result.FieldList = self.Client.put_right()
            
            SelWepon:clsWepon = self.Wepons.GetWepon(clsWepon.BLOCK)
            SelWepon.UseWepon()

        elif (pAction == clsAction.LO_UP or 
              pAction == clsAction.LO_DOWN or
              pAction == clsAction.LO_LEFT or
              pAction == clsAction.LO_RIGHT):
            
            # 見る
            if pAction == clsAction.LO_UP:
                LDr = clsLookDirection.UP
                result.FieldList = self.Client.look_up()
            elif pAction == clsAction.LO_DOWN:
                LDr = clsLookDirection.DW
                result.FieldList = self.Client.look_down()
            elif pAction == clsAction.LO_LEFT:
                LDr = clsLookDirection.LF
                result.FieldList = self.Client.look_left()
            elif pAction == clsAction.LO_RIGHT:
                LDr = clsLookDirection.RI
                result.FieldList = self.Client.look_right()

        elif (pAction == clsAction.SR_UP or 
              pAction == clsAction.SR_DOWN or
              pAction == clsAction.SR_LEFT or
              pAction == clsAction.SR_RIGHT):
            
            # サーチ
            if pAction == clsAction.SR_UP:
                LDr = clsLookDirection.UP
                result.FieldList = self.Client.search_up()
            elif pAction == clsAction.SR_DOWN:
                LDr = clsLookDirection.DW
                result.FieldList = self.Client.search_down()
            elif pAction == clsAction.SR_LEFT:
                LDr = clsLookDirection.LF
                result.FieldList = self.Client.search_left()
            elif pAction == clsAction.SR_RIGHT:
                LDr = clsLookDirection.RI
                result.FieldList = self.Client.search_right()

        # 方向
        self.setDirection(Dr)
        self.setLookDirection(LDr)

        #履歴を残す(後で何かにつかう)
        self.logColRow.append(clslogRowCol(pAction,result.FieldList,self.col,self.row))

        return result

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

    # 武器
    Wepons = clsWepons()

    # Client
    Client = None
    
    def __init__(self,pClient:CHaser.Client):
        """
        コンストラクタ
        """

        #Client
        self.Client = pClient

        #武器の追加
        self.Wepons.AddWepon(clsWepon(clsWepon.BLOCK,clsWepon.COMMAND_BLOCK,"",999,False))
        self.Wepons.AddWepon(clsWepon(clsWepon.BOM  ,clsWepon.COMMAND_BOM  ,"",1  ,False))
        self.Wepons.AddWepon(clsWepon(clsWepon.EYE  ,clsWepon.COMMAND_EYE  ,"",5  ,False))
        option = [clsWepon(clsWepon.BOM  ,clsWepon.COMMAND_RAND,"???"  ,1,True),
                  clsWepon(clsWepon.CHAFF,clsWepon.COMMAND_RAND,"?????",1,True),
                  clsWepon(clsWepon.EYE  ,clsWepon.COMMAND_RAND,"???"  ,3,True)]
        WeponRandom = random.choice(option)
        self.Wepons.AddWepon(WeponRandom)
        self.Wepons.AddWepon(clsWepon(clsWepon.HELP ,clsWepon.COMMAND_HELP ,"",0,False))

    def AddTurn(self):
        """
        ターンのカウント
        """
        self.TurnCnt += 1

    def CleateWeponMenu(self,pCommandColor:str):
        """
        メニューに表示するWeponのメニューを作成する
        """
        tmpList = []
        for selWepon in self.Wepons.GetWepons():
            tmpList.append(selWepon.CleateMenuStr(pCommandColor))

        return f"[Wepon] {' '.join(tmpList)} Cancel:未入力 ..."
    
    def CleateWeponHelp(self):
        """
        Weponヘルプを作成する
        """
        tmpList = []
        for selWepon in self.Wepons.GetWepons():
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
        self.Player.SetWepon(self.Wepons)

    def CleateHelpStr(self,pAction:clsAction) -> str:
        """
        ヘルプの文字列作成
        """
        result = ""
        if pAction == clsAction.AC_LOOK:
            result = "Look : 指定した方向の3x3のフィールドを調べます。"
        elif pAction == clsAction.AC_SEARCH:
            result = "Search : 指定した方向の直線9マスを調べます。"
        elif pAction == clsAction.AC_WEPON:
            result = "Wepon : 武器を選択して使用します。"

        return result

            
class PrintAreaPutPlayerMode(Enum):
    """
    周辺情報のプレイヤーの表示モード
    """    
    P_3x3 = 1   #3x3の周辺情報
    P_REAL = 2  #フィールド全体
    
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
    PrintAreaPutPlayerMode = PrintAreaPutPlayerMode.P_3x3

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
                if self.PrintAreaPutPlayerMode == PrintAreaPutPlayerMode.P_3x3:
                    if curCol == 1 and curRow == 1:
                        field = self.A_PLAYER_ME

                # プレイヤーの表示
                ## print の end="" は、出力しても改行しない意味
                if field == self.A_PLAYER_ME:
                    Coler = pPlayerData.PlayerColor
                    if pPlayerData.LookDirection == clsLookDirection.UP:
                        print(f"{Coler}^ {RE}",end="")
                    elif pPlayerData.LookDirection == clsLookDirection.DW:
                        print(f"{Coler}v {RE}",end="")
                    elif pPlayerData.LookDirection == clsLookDirection.LF:
                        print(f"{Coler}< {RE}",end="")
                    elif pPlayerData.LookDirection == clsLookDirection.RI:
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

class clsAreaTalbeEx(clsAreaTable):
    """
    周辺の情報を退避するクラス

    ### 開発途中 ###

    """ 
    player = None
    def __init__(self,pSize:int,pPlayer:clsPlayerData):
        """
        コンストラクタ

            ・退避するリストのサイズを設定
            ・プレイヤーの初期位置を設定

        Args:
            pSize (int): 退避する領域の列数と行数(必ず奇数)
            pPlayer (clsPlayerData): プレイヤー情報
        """    
        super().__init__(pSize,pSize)

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

def main():
    
    # プログラムを管理するクラスの使用
    Administrator = clsSystemAdministrator()
    # 起動音を鳴らす
    Administrator.StartupSound()
    # タイトルの表示
    Administrator.TitleShow()

    return

    value = [] # フィールド情報を保存するリスト
    client = CHaser.Client() # サーバーと通信するためのインスタンス

    # ゲームをなんとなく管理するGameMasterの設定
    GameMaster = clsGameMaster(client)
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

        GetReadyValue = client.get_ready()

        # タイトルの表示
        print(f"{PlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_ASTA}{RE}") 
        print(f"{PlayerData.PlayerColor} 自分のターン[Turn:{GameMaster.TurnCnt}]{RE}")
        #print(f"{PlayerData.PlayerColor}{clsEtcValue.PRINT_LINE_ASTA}{RE}") 

        # 周辺の情報を表示
        AreaTable.SetAreaList(GetReadyValue)
        AreaTable.PrintArea(PlayerData,EnemyPlayerData,clsAction.AC_BEFOR)

        # その他ステータスの表示
        GameMaster.ShowGameStatus()

        # コマンドの文字色
        ComColor = G

        # 行動の結果
        ActionResult = clsActionResult()

        while(True):

            IsMoveStep = True
            IsBlockStep = False
            IsWeponStep = False
            IsEndStep = False
            IsSearchStep = False
            IsLookStep = False

            #キー入力
            InputMenu = f"←:{ComColor}{MV_L}{RE} →:{ComColor}{MV_R}{RE} ↑:{ComColor}{MV_U}{RE} ↓:{ComColor}{MV_D}{RE} Serch:{ComColor}{MV_S}{RE} Look:{ComColor}{MV_LOOK}{RE} Wepon:{ComColor}{MV_W}{RE}"
            if BefInpVal == None :
                InpVal = input(f"[Move] {InputMenu} ...")
            else :
                InpVal = input(f"[Move] {InputMenu} Bef({BefInpVal}):{ComColor}未入力{RE}...")
                if InpVal == "":
                    InpVal = BefInpVal

            #移動先がブロックかどうかの判定
            if InpVal == MV_L:
                ActionResult = PlayerData.DoActionPlayerTest(clsAction.MV_LEFT,GetReadyValue)
            elif InpVal == MV_R:
                ActionResult = PlayerData.DoActionPlayerTest(clsAction.MV_RIGHT,GetReadyValue)
            elif InpVal == MV_U:
                ActionResult = PlayerData.DoActionPlayerTest(clsAction.MV_UP,GetReadyValue)
            elif InpVal == MV_D:
                ActionResult = PlayerData.DoActionPlayerTest(clsAction.MV_DOWN,GetReadyValue)
            else:
                ActionResult = None

            if ActionResult != None and ActionResult.Result == enmActionResult.BLOCK :
                tmpResult = input(f"{R}移動先はブロックですが、移動しますか？{RE} y/n...")
                if tmpResult == "n" or tmpResult == "" :
                    continue
 
            #移動
            IsInputBefSetValue = False
            if InpVal == MV_L :
                ActionResult = PlayerData.DoActionPlayer(clsAction.MV_LEFT,GetReadyValue)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_R :
                ActionResult = PlayerData.DoActionPlayer(clsAction.MV_RIGHT,GetReadyValue)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_U :
                ActionResult = PlayerData.DoActionPlayer(clsAction.MV_UP,GetReadyValue)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_D :
                ActionResult = PlayerData.DoActionPlayer(clsAction.MV_DOWN,GetReadyValue)
                IsEndStep = True
                IsInputBefSetValue = True
            elif InpVal == MV_S :
                IsSearchStep = True
            elif InpVal == MV_LOOK :
                IsLookStep = True
            elif InpVal == MV_W :
                IsWeponStep = True
            else :
                #print(f"{R}入力値が不正です!!!{RE}")
                continue

            #前回と同じコマンドとして保存する場合
            if IsInputBefSetValue == True:
                BefInpVal = InpVal

            #Weponメニュー
            if IsWeponStep == True :
                while(True):
                    # Helpの表示
                    print(f"{GameMaster.CleateHelpStr(clsAction.AC_WEPON)}")
                    # キー入力
                    InpVal = input(f"{GameMaster.CleateWeponMenu(ComColor)}")
                    if InpVal == clsWepon.COMMAND_BLOCK :
                        IsBlockStep = True
                        break
                    elif InpVal == clsWepon.COMMAND_HELP :
                        print(f"{GameMaster.CleateWeponHelp()}")
                        continue
                    if InpVal == clsWepon.COMMAND_BOM :
                        print(f"{R}未実装のため使用できません!{RE}")
                        continue
                    if InpVal == clsWepon.COMMAND_EYE :
                        print(f"{R}未実装のため使用できません!{RE}")
                        continue
                    if InpVal == clsWepon.COMMAND_RAND :
                        print(f"{R}未実装のため使用できません!{RE}")
                        continue
                    else :
                        IsMoveStep = True
                        break

            #ブロックの設置メニュー
            InputMenu = f"←:{ComColor}{MV_L}{RE} →:{ComColor}{MV_R}{RE} ↑:{ComColor}{MV_U}{RE} ↓:{ComColor}{MV_D}{RE} Cancel:未入力 ..."
            if IsBlockStep == True :
                while(True):
                    # Helpの表示
                    print(f"{GameMaster.Wepons.GetWepon(clsWepon.BLOCK).CleateHelpStr()}")
                    # キー入力
                    InpVal = input(f"[Block] {InputMenu}")
                    if InpVal == MV_L :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.PT_LEFT,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_R :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.PT_RIGHT,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_U :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.PT_UP,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_D :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.PT_DOWN,GetReadyValue)
                        IsEndStep = True
                        break
                    else :
                        IsMoveStep = True
                        break

            #Searchメニュー
            if IsSearchStep == True :
                while(True):
                    # Helpの表示
                    print(f"{GameMaster.CleateHelpStr(clsAction.AC_SEARCH)}")
                    #キー入力
                    InpVal = input(f"[Search] {InputMenu}")
                    if InpVal == MV_L :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.SR_LEFT,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_R :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.SR_RIGHT,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_U :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.SR_UP,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_D :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.SR_DOWN,GetReadyValue)
                        IsEndStep = True
                        break
                    else :
                        IsMoveStep = True
                        break

            # Lookメニュー
            if IsLookStep == True :
                while(True):
                    # Helpの表示
                    print(f"{GameMaster.CleateHelpStr(clsAction.AC_LOOK)}")
                    # キー入力
                    InpVal = input(f"[Look] {InputMenu}")
                    if InpVal == MV_L :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.LO_LEFT,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_R :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.LO_RIGHT,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_U :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.LO_UP,GetReadyValue)
                        IsEndStep = True
                        break
                    elif InpVal == MV_D :
                        ActionResult = PlayerData.DoActionPlayer(clsAction.LO_DOWN,GetReadyValue)
                        IsEndStep = True
                        break
                    else :
                        IsMoveStep = True
                        break

            if IsEndStep == True:
                break

        #周辺の情報を表示
        AreaTable.SetAreaList(ActionResult.FieldList)
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
