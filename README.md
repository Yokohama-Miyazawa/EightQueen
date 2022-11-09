# EightQueen  
MiniSATを用いてNクイーンの解を求める  
MiniSATは自分でコンパイルした物をREADME.mdと同じディレクトリに配置すること  

## 使い方  
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
