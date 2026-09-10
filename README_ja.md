*This project has been created as part of the 42 curriculum by mnoda-ta, rkato.*

## Description
このプロジェクトは、`config.txt`ファイルに記載された設定を読み込み、
「42」パターンが埋め込まれた迷路（完全迷路・非完全（Pac-Man風）迷路の
2種類に対応）を生成するプログラム `a_maze_ing.py` を作成することが
目的です。

生成後、`OUTPUT_FILE`キーに指定された出力ファイルに迷路データを書き込み、
ASCII形式で迷路を画面に表示します。ユーザーは迷路の再生成、最短経路の
表示切り替え、壁の色変更などの操作をインタラクティブに行うことができます。


## Instructions

- 依存パッケージをインストールする
```bash
    make install
```
`.venv`という仮想環境を作成し、`requirements.txt`に記載された本プログラムが依存する外部パッケージ（`typing_extensions`など）をインストールします。

- 実行する
```bash
    make run
```
`config.txt`を設定ファイルとして実行します。
別の設定ファイルを使いたい場合は、直接以下のように実行してください。
```bash
    python3 a_maze_ing.py <設定ファイル>
```

- 不要なファイルを削除する
```bash
    make clean
```
実行時に生成されたキャッシュ（`__pycache__`, `.mypy_cache`）や、`make build`によるビルド成果物（`build`, `dist`, `*.egg-info`）を削除します。生成された迷路の出力ファイル（例：`maze.txt`）は削除されません。

- コードスタイルと型をチェックする
```bash
    make lint
```
または
```bash
    make lint-strict
```
`flake8`と`mypy`（`lint-strict`は`--strict`オプション付き）を実行します。

- pipパッケージをビルドする
```bash
    make build
```
再利用可能な`mazegen`モジュールを、pipでインストール可能なパッケージ（`.whl`/`.tar.gz`）としてビルドします。



## Resources
以下のサイトを参考にしました。
- [迷路生成アルゴリズム](https://www.cs.cmu.edu/~112-s23/notes/student-tp-guides/Mazes.pdf)
- [random()について](https://note.nkmk.me/python-random-choice-sample-choices/)
- [迷路生成におけるDFSとBFSについて](https://qiita.com/ophhdn/items/fb10c932d44b18d12656)
- [**二重アスタリスクの使い方](https://note.com/engneer_hino/n/n9c6c6297845d)
- [一部のキーが存在しない型を定義する(NotRequired)](https://zenn.dev/t_yng/articles/bc3d779f4bbb70)
- [TypedDictについて](https://qiita.com/fgshun/items/587cbc7b5b06c3676622)
- [GoogleスタイルのPython Docstringの入門](https://qiita.com/11ohina017/items/118b3b42b612e527dc1d)
- [Queue in Python](https://www.geeksforgeeks.org/python/queue-in-python/)
- [deque(),キューを扱う方法](https://note.nkmk.me/python-collections-deque/#deque)
- [Pythonにおけるパッケージ化概要](https://packaging.python.org/en/latest/overview/)
- [パッケージ化の方法](https://packaging.python.org/ja/latest/tutorials/packaging-projects/)
- [pyproject.tomlについて](https://packaging.python.org/ja/latest/guides/writing-pyproject-toml/)
- [pyproject.tomlについて その2](https://packaging.python.org/en/latest/guides/writing-pyproject-toml/#license)
- [リポジトリのライセンス](https://docs.github.com/ja/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository)

### How AI was used
使用モデル: [Claude](claude.ai)
私たちはAIを以下の用途で使用しました
- 課題概要の整理
- イメージ図の生成
    display.pyの作成途中の情報整理のためや、fix_large_open_areas()の理解のために使用しました
- エラー分析、改善案の提案
    具体例：mypyでconvert_keys(現在のbuild_maze_config)がエラーになったとき、設計修正の提案をさせた
```bash
    def convert_keys(
            key_dict: dict[str, str],
        ) -> dict[str, int | tuple[int, int] | bool | str] | None:
```
のように全部まとめて一つの辞書としてループして型ごとに分岐→変換するやり方だと、mypyが型まで追えない→エラーになった
※辞書は「キーごとに違う型」を持つのに、型注釈上は「全部まとめた共用体」としか表現できていないため、mypyはどのキーがどの型かを個別に検証できない。
→なので、TypedDictを使用し「キーごとに正しい型」を明示する形に変える提案をしてもらった
- コードレビュー、エッジケースの確認
- docstringsの修正・改善・翻訳
- README.mdの修正・改善・翻訳


## Config file format

`config.txt`は1行につき1つの`KEY=VALUE`形式で設定を記述します。
`#`で始まる行はコメントとして無視されます。

| キー | 必須 | 説明 | 例 |
|---|---|---|---|
| WIDTH | 必須 | 迷路の幅（セル数） | WIDTH=20 |
| HEIGHT | 必須 | 迷路の高さ（セル数） | HEIGHT=15 |
| ENTRY | 必須 | 入口の座標 (x,y) | ENTRY=0,0 |
| EXIT | 必須 | 出口の座標 (x,y) | EXIT=19,14 |
| OUTPUT_FILE | 必須 | 出力ファイル名 | OUTPUT_FILE=maze.txt |
| PERFECT | 必須 | 完全迷路かどうか | PERFECT=True |
| SEED | 任意 | 指定されている場合はその値を使用し、指定されていない場合は0〜100のランダムな整数が選ばれる | SEED=42 |


## Algorithm
使用したアルゴリズム: 再帰的バックトラッカー法（DFS: 深さ優先探索）

### アルゴリズムの説明
深さ優先探索（DFS）とは、現在地点から進めるところまで一方向に
どんどん深く進み、行き詰まったら1つ前の地点まで戻ってやり直す、
という探索方法です（近い場所から順に広く探索するBFS: 幅優先探索とは
対照的な性質を持ちます）。

これを迷路生成に応用したのが再帰的バックトラッカー法です。具体的には
以下のサイクルを繰り返します。

1. 現在のセルから、まだ訪れていない隣接セルをランダムに1つ選ぶ
2. そのセルとの間の壁を壊して道をつなげ、そのセルへ進む
3. 未訪問の隣接セルが無くなった（行き止まりに達した）場合は、
   1つ前のセルまで戻る（バックトラック）
4. すべてのセルを訪れ終わるまで1〜3を繰り返す

この動きにより、迷路全体が1本の連続した通路（木構造）としてつながり、
すべてのセル間にちょうど1つの経路が存在する「完全迷路」が生成されます。

### 選定理由
条件に合う壁の中からランダムに選んだ壁を壊していく、という考え方が
シンプルで分かりやすかったため、このアルゴリズムを採用しました。


## Reusable module

迷路生成ロジックは `mazegen` パッケージ内の `generator.py` モジュール内の
`MazeGenerator` クラスとして実装されており、他のプロジェクトから独立して
再利用できます。
pipでインストール可能な `mazegen-*` パッケージとしてビルドされています
（`make build` を参照。詳細な使用方法は `mazegen/README.md` も参照）。

### 基本的な使い方

```python
from mazegen import MazeGenerator

maze = MazeGenerator(
    width=20,
    height=15,
    entry=(0, 0),
    exit=(19, 14),
)
maze.generate()

# 生成されたグリッド構造にアクセスする
print(maze.grid[0][0].walls)

# entryからexitまでの最短経路を取得する
solution = maze.solve()
print(solution)
```

`perfect`を指定しない場合はデフォルトで`False`となり、
ループを含む非完全（Pac-Man風）迷路が生成されます。

### カスタムパラメータ

```python
maze = MazeGenerator(
    width=30,
    height=20,
    entry=(0, 0),
    exit=(29, 19),
    perfect=True,
    seed=42,
)
```


## Team & project management

### 役割分担

| ファイル | 担当 |
|---------|------|
| `mazegen/generator.py` | mnoda-ta （ただし`calc_42patern`関数はrkato）|
| `read_config.py` | rkato |
| `make_outputfile.py` | rkato |
| `display.py` | rkato |
| `a_maze_ing.py` | rkato |
| `Makefile` | mnoda-ta |
| `LICENSE.md` | mnoda-ta |
| `pyproject.toml` | mnoda-ta |
| `README.md` | rkato mnoda-ta|

迷路生成のアルゴリズムを`mnoda-ta`が、表示部分を`rkato`が担当すると割り振ってから、それぞれ取り組み、完了したら必要なタスクを整理→手が空いている方が担当すると言ったように随時割り振っていった。
タスクが完了したらGitHubでPullRequestを送り、相手の同意を得てからマージするという流れで進めた。
タスク管理及び共有のメモとして、[Google Document](https://docs.google.com/document/d/1fioY9jzPlAP8k5x66gox01MW8rBHqUK5eF2OBc1lST0/edit?usp=sharing)を使用した

### 良かった点・改善できる点

**良かった点**
- 実装する度に相手の確認を取れた(互いに相手の実装内容を確認できた)
- タスクを分けていたので重複がなかった

**改善できる点**
- (記入)

### 使用したツール
- GitHub（Pull Requestによるコードレビューとマージ）
- Discord（コミュニケーション）
- Google Document（タスク管理・共有メモ）