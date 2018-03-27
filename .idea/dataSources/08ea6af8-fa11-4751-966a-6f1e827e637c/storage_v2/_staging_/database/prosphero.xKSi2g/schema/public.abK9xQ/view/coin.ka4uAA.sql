alter VIEW coins
select
      id,
      code,
      short_name,
      full_name,
      algorithm,
      proof_type,
      is_trading,
      premined_value,
      fully_premined,
      total_coin_supply,
      total_coins_free_float,
      sponsored,
      url
from (
  SELECT
    coin.id,
    coin.valid_from_dttm,
    coin.code,
    coin.short_name,
    coin.full_name,
    coin.algorithm,
    coin.proof_type,
    coin.is_trading,
    coin.premined_value,
    coin.fully_premined,
    coin.total_coin_supply,
    coin.total_coins_free_float,
    coin.sponsored,
    coin.url,
    row_number()
    OVER (
      PARTITION BY coin.code
      ORDER BY valid_from_dttm DESC ) AS rn
  FROM cryptocompare.coin
) t
where 1 = 1
  and rn = 1

;

