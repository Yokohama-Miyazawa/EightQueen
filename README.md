# EightQueen  
[MiniSAT](http://minisat.se/)、[PySAT](https://pysathq.github.io/)を用いてNクイーンの解を求める  
MiniSATは自分でコンパイルした物をREADME.mdと同じディレクトリに配置すること  

## 各プログラム説明
| プログラム名 | SATソルバ | 高速化(※) |
| --- | --- | --- |
| eq.py | MiniSAT | なし |
| eq_gp02.py | PySAT | なし |
| eq_mk2.py | MiniSAT | あり |
| eq_z.py | PySAT | あり |

※ 高速化なしのプログラムは、一つの解が見つかるとその解の否定のみをCNFに追加する。  
高速化ありのプログラムは、一つの解が見つかるとその解の否定に加えてその鏡像と回転像の否定もCNFに追加する。

## 依存ライブラリ  
[PySAT](https://pysathq.github.io/installation/)(eq_gp02.py, eq_z.pyのみ)  

## 使い方(各プログラム共通)  
### Nの数  
Nの値をコマンドライン引数で与える。  
```
python3 eq.py 8
```

### オプション  
#### `-h, --help`
ヘルプ

#### `-a, -answers`
全ての答えを求めるか、一つだけ答えを求めるかを選択できる。  
全ての答えを求めるなら`all`、一つだけ答えを求めるなら`one`。  
```
python3 eq.py 8 -a all
```
```
python3 eq.py 10 -ansewrs 10
```

#### `-nd, --no_display`
Nクイーンの盤面を表示しない(`-a, --answers`が`all`の時のみ)。  
