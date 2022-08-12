import numpy as np


# 盤面配列bを画面表示する
def viewban(b):
    print("  1 2 3 4 5 6 7 8")
    for y in range(8):
        print(" " + str(y + 1), end="")
        for x in range(8):
            # print("○　●"[b[x, y] + 1], end="")
            print("白　黒"[b[x, y] + 1], end="")
        print("")


# 指定した場所にコマを置く。
# x, y = 座標（1〜8。パスのときは両方0）
# n = 1のとき黒、-1のとき白
# b = 盤面配列
def setput(x, y, n, b):
    m = np.zeros((8, 8), dtype=bool)

    # パスのときは何もしない
    if x == 0 and y == 0:
        return b

    x = x - 1
    y = y - 1
    # 横
    for i in range(x - 1, -1, -1):
        if b[i, y] == 0:
            break
        if b[i, y] == n:
            m[i:x, y] = True
            break
    for i in range(x + 1, 8):
        if b[i, y] == 0:
            break
        if b[i, y] == n:
            m[x:i, y] = True
            break
    # 縦
    for j in range(y - 1, -1, -1):
        if b[x, j] == 0:
            break
        if b[x, j] == n:
            m[x, j:y] = True
            break
    for j in range(y + 1, 8):
        if b[x, j] == 0:
            break
        if b[x, j] == n:
            m[x, y:j] = True
            break
    # 斜め
    (i, j) = (x - 1, y - 1)
    c = 0
    while (i >= 0) and (j >= 0):
        if b[i, j] == 0:
            break
        if b[i, j] == n:
            for k in range(c):
                m[x - 1 - k, y - 1 - k] = True
            break
        c += 1
        i -= 1
        j -= 1

    (i, j) = (x + 1, y + 1)
    c = 0
    while (i < 8) and (j < 8):
        if b[i, j] == 0:
            break
        if b[i, j] == n:
            for k in range(c):
                m[x + 1 + k, y + 1+k] = True
            break
        c += 1
        i += 1
        j += 1

    (i, j) = (x - 1, y + 1)
    c = 0
    while (i >= 0) and (j < 8):
        if b[i, j] == 0:
            break
        if b[i, j] == n:
            for k in range(c):
                m[x - 1 - k, y + 1 + k] = True
            break
        c += 1
        i -= 1
        j += 1

    (i, j) = (x + 1, y - 1)
    c = 0
    while (i < 8) and (j >= 0):
        if b[i, j] == 0:
            break
        if b[i, j] == n:
            for k in range(c):
                m[x + 1 + k, y - 1 - k] = True
                break
        c += 1
        i += 1
        j -= 1

    m[x, y] = True
    return np.where(m, n, b)


# 盤面bの座標x, y に、 石n (黒 = 1、 白=-1) が置けるかどうかを確認する
def chkput(x, y, n, b):
    # 空白でないなら置けない
    if b[x - 1][y - 1] != 0:
        return False

    # そこに置いてみる
    newban = setput(x, y, n, b)

    # 黒の数
    new_one = np.count_nonzero(newban == 1)
    b_one = np.count_nonzero(b == 1)

    # 白の数
    new_minus = np.count_nonzero(newban == -1)
    b_minus = np.count_nonzero(b == -1)

    # 操作前と操作後で石の数が同じ(=ひとつもひっくり返せない)なら置けない
    if n == 1:
        return not ((new_one == b_one + 1) and (new_minus == b_minus))
    else:
        return not ((new_one == b_one) and (new_minus == b_minus + 1))


# パスできるかどうかを返す
def canpass(n, b):
    for x in range(8):
        for y in range(8):
            if chkput(x + 1, y + 1, n, b):
                return False
    return True


def computercalc_01(b, n):
    # 打てる場所を探す
    (cx, cy) = (0, 0)
    for x in range(8):
        for y in range(8):
            if chkput(x + 1, y + 1, n, b):
                # 優先順位を引っ張る
                # 50%の確率でランダムに打つ場所をきめる
                if (np.random.rand() >= 0.5):
                    (cx, cy) = (x + 1, y + 1)
    return (cx, cy)


# コンピュータの次の手を返す
def computercalc(b, n):
    # 優先順位
    m = [
        [40, 15, 30, 15, 15, 30, 15, 40],
        [15, 15, 20, 15, 15, 20, 15, 15],
        [30, 15, 40, 15, 15, 40, 15, 30],
        [20, 15, 20, 15, 15, 20, 15, 20],
        [20, 15, 20, 15, 15, 20, 15, 20],
        [30, 15, 40, 15, 15, 40, 15, 30],
        [15, 15, 20, 15, 15, 20, 15, 15],
        [40, 15, 30, 15, 15, 30, 15, 40]
    ]

    # 打てる場所を探す
    (cx, cy) = (0, 0)
    val = 0
    for x in range(8):
        for y in range(8):
            if chkput(x + 1, y + 1, n, b):
                # 優先順位を引っ張る
                if (val < m[x][y]) or (val == m[x][y] and np.random.rand() >= 0.5):
                    (cx, cy) = (x + 1, y + 1)
                    val = m[x][y]
    return (cx, cy)


def main():
    # 盤面を作る e=空、1=黒、-1 = 白
    ban = np.zeros((8, 8), dtype=int)
    ban[3][3] = ban[4][4] = -1
    ban[4][3] = ban[3][4] = 1

    while np.count_nonzero(ban == 0) > 0:
        # 人間の手を入力
        p = False
        while not p:
            viewban(ban)
            human = input("打ちたい場所を「x, y」（xは1〜8、yは1〜8）のようにカンマ区切りで入力。パスのときは0,0\n")
            if not ',' in human:
                print("書式が正しくありません。 カンマ区切りで入力してください")
                continue
            (x, y) = human.split(',')
            if not (x.isdecimal() and y. isdecimal()):
                print("x,yが整数ではありません")
                continue
            x = int(x)
            y = int(y)
            if not ((0 <= x <= 8) and (0 <= y <= 8)):
                print("x,yが0から8の範囲ではありません")
                continue
            if x == 0 and y == 0:
                if not canpass(1, ban):
                    print("打てる手があるのでパスできません")
                    continue
            if not chkput(x, y, 1, ban):
                print("その場所には置けません")
                continue
            p = True

            # 人間の手を置く
            ban = setput(x, y, 1, ban)

            # コンピュータの手
            (cx, cy) = computercalc(ban, -1)
            ban = setput(cx, cy, -1, ban)

            # 両方パスなら投了
            if x == 0 and y == 0 and cx == 0 and cy == 0:
                break

    # 勝ち負け表示
    kuro = np.count_nonzero(ban == 1)
    shiro = np.count_nonzero(ban == -1)

    if kuro > shiro:
        msg = "あなたの勝ち"
    elif kuro < shiro:
        msg = "あなたの負け"
    else:
        msg = "引き分け"

    print("黒{0}対白{1}で{2}".format(kuro, shiro, msg))


if __name__ == "__main__":
    main()
