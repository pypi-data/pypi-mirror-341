from dataclasses import dataclass
from typing import Annotated

from mm_std import BaseConfig, Err, Ok, fatal
from pydantic import BeforeValidator
from rich.live import Live
from rich.table import Table

from mm_eth import erc20, rpc
from mm_eth.cli.cli_utils import BaseConfigParams
from mm_eth.cli.validators import Validators
from mm_eth.utils import from_token_wei_str, from_wei_str


class Config(BaseConfig):
    addresses: Annotated[list[str], BeforeValidator(Validators.eth_addresses(unique=True))]
    tokens: Annotated[list[str], BeforeValidator(Validators.eth_addresses(unique=True))]
    nodes: Annotated[list[str], BeforeValidator(Validators.nodes())]
    round_ndigits: int = 5


@dataclass
class Token:
    address: str
    decimals: int
    symbol: str


class BalancesCmdParams(BaseConfigParams):
    wei: bool
    show_nonce: bool


def run(params: BalancesCmdParams) -> None:
    config = Config.read_toml_config_or_exit(params.config_path)
    if params.print_config:
        config.print_and_exit()

    tokens = _get_tokens_info(config)

    table = Table(title="balances")
    table.add_column("address")
    if params.show_nonce:
        table.add_column("nonce")
    table.add_column("wei" if params.wei else "eth")
    for t in tokens:
        table.add_column(t.symbol)

    base_sum = 0
    token_sum: dict[str, int] = {t.address: 0 for t in tokens}
    with Live(table, refresh_per_second=0.5):
        for address in config.addresses:
            row = [address]
            if params.show_nonce:
                row.append(str(rpc.eth_get_transaction_count(config.nodes, address, attempts=5).ok_or_err()))

            base_balance_res = rpc.eth_get_balance(config.nodes, address, attempts=5)
            if isinstance(base_balance_res, Ok):
                base_sum += base_balance_res.ok
                if params.wei:
                    row.append(str(base_balance_res.ok))
                else:
                    row.append(
                        from_wei_str(base_balance_res.ok, "eth", round_ndigits=config.round_ndigits, print_unit_name=False),
                    )
            else:
                row.append(base_balance_res.err)

            for t in tokens:
                token_balance_res = erc20.get_balance(config.nodes, t.address, address, attempts=5)
                if isinstance(token_balance_res, Ok):
                    token_sum[t.address] += token_balance_res.ok
                    if params.wei:
                        row.append(str(token_balance_res.ok))
                    else:
                        row.append(
                            from_token_wei_str(
                                token_balance_res.ok,
                                decimals=t.decimals,
                                round_ndigits=config.round_ndigits,
                            ),
                        )
                else:
                    row.append(token_balance_res.err)

            table.add_row(*row)

        sum_row = ["sum"]
        if params.show_nonce:
            sum_row.append("")
        if params.wei:
            sum_row.append(str(base_sum))
            sum_row.extend([str(token_sum[t.address]) for t in tokens])
        else:
            sum_row.append(from_wei_str(base_sum, "eth", round_ndigits=config.round_ndigits, print_unit_name=False))
            sum_row.extend(
                [from_token_wei_str(token_sum[t.address], t.decimals, round_ndigits=config.round_ndigits) for t in tokens]
            )

        table.add_row(*sum_row)


def _get_tokens_info(config: Config) -> list[Token]:
    result: list[Token] = []
    for address in config.tokens:
        decimals_res = erc20.get_decimals(config.nodes, address, attempts=5)
        if isinstance(decimals_res, Err):
            fatal(f"can't get token {address} decimals: {decimals_res.err}")
        decimal = decimals_res.ok

        symbols_res = erc20.get_symbol(config.nodes, address, attempts=5)
        if isinstance(symbols_res, Err):
            fatal(f"can't get token {address} symbol: {symbols_res.err}")
        symbol = symbols_res.ok

        result.append(Token(address=address, decimals=decimal, symbol=symbol))

    return result
