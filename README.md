# EightQueen  
MiniSATを用いてNクイーンの解を求める  
MiniSATは自分でコンパイルした物をREADME.mdと同じディレクトリに配置すること  

## 使い方  
### Nの数  
デフォルトではN=8となる。  
```
python3 eq.py
```

Nの値をコマンドライン引数で与えられる。  
```
python3 eq.py 10
```

### モード選択  
全ての答えを求めるか、一つだけ答えを求めるかを選択できる。  
Nの値の後ろに、全ての答えを求めるなら`all`を、  
一つだけ答えを求めるなら`one`を入力する。  
```
python3 eq.py 8 one
```
