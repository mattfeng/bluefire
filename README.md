# BlueFire AI

## Directory structure
* `pytorch`
    * An initial run of `lda2vec` using PyTorch (credits: https://github.com/TropComplique/lda2vec-pytorch/).
* `pytorch2`
    * A second run of `lda2vec` using PyTorch but with more stopwords removed.
    * Additional words that were removed (see: `specialized.txt`)
        * `公司, 市场, 同比, 增长, 投资, 业务, 行业`
        * `风险, 预期, 预计, 亿, 亿元, 可能, 占, 亿美元`
