# ccxtools

CryptoCurrency eXchange TOOLS

암호화폐 자동매매 관련 라이브러리인 CCXT를 기반으로 만들어진 암호화폐 자동매매용 Python 3 라이브러리입니다.

## Install

[ccxtools in PyPI](https://pypi.org/project/ccxtools/)

```
pip install ccxtools
```

## Features

ccxtools는 ccxt에서 함수로 구현되지 않은 API와 저 개인적으로 매매 프로그램을 개발할 때 필요한 함수들을 구현한 라이브러리이기 때문에 암호화폐 매매에 필요한 모든 API를 담고있지는 않습니다. 기본적인 API는 [ccxt](https://github.com/ccxt/ccxt)를 참조하시기 바랍니다.

- 거래소별로 다른 ticker 형식을 일일이 작성할 필요없이 코인 이름만으로 사용할 수 있습니다. 

  ```python
  {ticker}USDT, {ticker}-USDT, {ticker}/USDT
  => {ticker}만 입력하면 됩니다.
  ```

- ccxt에서 함수로 구현해놓지 않은 API를 함수로 구현해 놓았습니다.

  - Bybit
    - max_trading_qty
    - risk_limit 관련

- pytest로 테스트를 구현해놓아 API나 CCXT 내용 변경에 신속히 대응할 수 있습니다.

