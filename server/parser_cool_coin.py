import requests
from bs4 import BeautifulSoup
from database.base import SessionLocal
from database.models import CurrencyRate, Exchanges
import re
from multiprocessing import Process


def unify_data(row_data):
    # Функция для унификации данных
    give_pair_name_mapping_dict = {
        "Сбербанк RUB": "Сбербанк(RUB)",
        "EOS EOS": "EOS(EOS)",
        "BinanceCoin BEP20 BNB": "BinanceCoin BEP20(BNB)",
        "Binance Coin BEP20 BNB": "BinanceCoin BEP20(BNB)",
        "BinanceCoin BEP2 BNB": "BinanceCoin BEP20(BNB)",
        "Binance Coin (BSC) BNB": "BinanceCoin BEP20(BNB)",
        "Polygon MATIC": "Polygon(MATIC)",
        "Bitcoin BTC": "Bitcoin(BTC)",
        "Ethereum ETH": "Ethereum(ETH)",
        "Ethereum BEP20 ETH": "Ethereum BEP20(ETH)",
        "Bitcoin Cash BCH": "Bitcoin Cash(BCH)",
        "Ripple XRP": "Ripple(XRP)",
        "ERC20 USDT": "Tether ERC20(USDT)",
        "OMNI USDT": "Tether OMNI(USDT)",
        "TRC20 USDT": "Tether TRC20(USDT)",
        "BEP20 USDT": "Tether BEP20(USDT)",
        "Tether BEP20 USDT": "Tether BEP20(USDT)",
        "USDCoin ERC20 USDC": "USDCoin ERC20(USDC)",
        "Dai DAI": "DAI(DAI)",
        "Stellar XLM": "Stellar(XLM)",
        "Pax Dollar USDP": "Pax Dollar(USDP)",
        "NEM XEM": "NEM(XEM)",
        "USD Coin ERC20 USDC": "USD Coin ERC20(USDC)",
        "NEO NEO": "NEO(NEO)",
        "TUSD": "TUSD(True USD ERC20)",
        "MIOTA IOTA": "IOTA(MIOTA)",
        "Cardano ADA": "Cardano(ADA)",
        "OmiseGO OMG": "OMG Network(OMG)",
        "Verge XVG": "Verge(XVG)",
        "Solana SOL": "Solana(SOL)",
        "ICON ICX": "ICON(ICX)",
        "Cosmos ATOM": "Cosmos(ATOM)",
        "Chainlink LINK": "Chainlink(LINK)",
        "Ontology ONT": "Ontology(ONT)",
        "BAT BAT": "BAT(BAT)",
        "USD Coin TRC20 USDC": "USDCoin TRC20(USDC)",
        "Тинькофф RUB": "Тинькофф(RUB)",
        "Visa MasterCard RUB": "Visa/MasterCard(RUB)",
        "СБП RUB": "СБП(RUB)",
        "Росбанк RUB": "Росбанк(RUB)",
        "Альфа банк RUB": "Альфа-банк(RUB)",
        "Карта Мир RUB": "Карта Мир(RUB)",
        "Почта Банк RUB": "Почта Банк(RUB)",
        "ВТБ RUB": "ВТБ(RUB)",
        "Kaspi Bank KZT": "Kaspi Bank(KZT)",
        "Райффайзен Банк RUB": "Райффайзен(RUB)",
        "BinanceCoin ERC20 BNB": "BinanceCoin ERC20(BNB)",
        "Наличные МСК RUB": "Наличные(RUB)",
        "Dash DASH": "Dash(DASH)",
        "ForteBank KZT": "ForteBank(KZT)",
        "Zcash ZEC": "Zcash(ZEC)",
        "HalykBank KZT": "HalykBank(KZT)",
        "Waves WAVES": "Waves(WAVES)",
        "Jusan Bank KZT": "Jusan Bank(KZT)",
        "VISA MASTERCARD Казахстан KZT": "VISA/MASTERCARD(KZT)",
        "Dogecoin DOGE": "Dogecoin(DOGE)",
        "TRON TRX": "TRON(TRX)",
        "Авангард RUB": "Авангард(RUB)",
        "Тинькофф Онлайн RUB": "Тинькофф(RUB)",
        "ВТБ 24 RUB": "ВТБ(RUB)",
        "Tether ERC20 USDT": "Tether ERC20(USDT)",
        "Tether (ERC20) USDT": "USDT(ERC20)",
        "Альфа-Банк RUB": "Альфа-банк(RUB)",
        "VeChain VET": "VeChain(VET)",
        "Ethereum (ERC-20) ETH": "Ethereum(ETH)",
        "Uniswap UNI": "Uniswap(UNI)",
        "Payeer EUR": "Payeer(EUR)",
        "Tether TRC20 USDT": "Tether TRC20(USDT)",
        "VISA/MC RUB": "Visa/MasterCard(RUB)",
        "USDCoin TRC20 USDC": "USDCoin TRC20(USDC)",
        "Наличные RUB": "Наличные(RUB)",
        "Любая карта RUB": "Любая карта(RUB)",
        "Райффайзен RUB": "Райффайзен(RUB)",
        "QIWI RUB": "QIWI(RUB)",
        "ЮMoney RUB": "ЮMoney(RUB)",
        "Тезер TRC20 USDT": "Tether TRC20(USDT)",
        "Сальдо LTC": "Tether TRC20(USDT)",
        "Visa/MasterCard KZT": "Visa/MasterCard(KZT)",
        "Евразийский KZT": "Евразийский(KZT)",
        "Тезер BEP20 USDT": "Tether BEP20(USDT)",
        "0x (ERC20) ZRX": "0x(ZRX)",
        "0x ZRX": "0x(ZRX)",
        "ADV Cash EUR": "Advcash(EUR)",
        "ADV Cash KZT": "Advcash(KZT)",
        "Advcash RUB": "Advcash(RUB)",
        "ADV Cash TRY": "Advcash(TRY)",
        "Advcash USD": "Advcash(USD)",
        "ADV Cash USD": "Advcash(USD)",
        "Alipay CNY": "Alipay(CNY)",
        "Avalanche AVAX": "Avalanche(AVAX)",
        "Avalanche (CCHAIN) AVAX": "Avalanche(AVAX)",
        "BAT BAT": "BAT(BAT)",
        "BAT (ERC20) BAT": "BAT(BAT)",
        "Binance USD (BEP20) BUSD": "Binance USD(BUSD)",
        "Binance USD (BSC) BUSD": "Binance USD(BUSD)",
        "Binance USD BUSD": "Binance USD(BUSD)",
        "Bitcoin Antalya BTC": "Bitcoin(BTC)",
        "Bitcoin Bep20 BTC": "Bitcoin BEP20(BTCB)",
        "BitCoin BTC": "Bitcoin(BTC)",
        "Bitcoin (BTC) BTC": "Bitcoin(BTC)",
        "Bitcoin Cash BCH": "Bitcoin Cash(BCH)",
        "Bitcoin Cash (BCH) BCH": "Bitcoin Cash(BCH)",
        "Bitcoin Gold BTG": "Bitcoin Gold(BTG)",
        "Bitcoin Sankt-Peterburg BTC": "Bitcoin(BTC)",
        "Bitcoin Stambul BTC": "Bitcoin(BTC)",
        #"+ BTC": "Bitcoin(BTC)",
        "'BTC'": "Bitcoin(BTC)",
        "Cardano (ADA) ADA": "Cardano(ADA)",
        "ChainLink (ERC20) LINK": "ChainLink(LINK)",
        "Chainlink LINK": "ChainLink(LINK)",
        "ChainLink LINK": "ChainLink(LINK)",
        "DAI DAI": "DAI(DAI)",
        "DAI ERC20 DAI": "DAI(DAI)",
        "DAI (ERC20) DAI": "DAI(DAI)",
        "Dash DASH": "Dash(DASH)",
        "DASH DASH": "Dash(DASH)",
        "Dash (DASH) DASH": "Dash(DASH)",
        "Decentraland (ERC20) MANA": "Decentraland(MANA)",
        "Dogecoin DOGE": "Dogecoin(DOGE)",
        "DogeCoin DOGE": "Dogecoin(DOGE)",
        "Doge (DOGE) DOGE": "Dogecoin(DOGE)",
        "EOS EOS": "EOS(EOS)",
        "EOS (EOS) EOS": "EOS(EOS)",
        "ERC20 USDT": "Tether ERC20(USDT)",
        "ETH": "Ethereum(ETH)",
        "Ethereum Antalya ETH": "Ethereum(ETH)",
        "Ethereum ERC20 ETH": "Ethereum(ETH)",
        "Ethereum (ERC20) ETH": "Ethereum(ETH)",
        "Ethereum Sankt-Peterburg ETH": "Ethereum(ETH)",
        "Ethereum Stambul ETH": "Ethereum(ETH)",
        "Ether Classic ETC": "Ethereum Classic(ETC)",
        "Faster Payment systеm HKD": "Банковский счет(HKD)",
        "Halyk Bank KZT": "HalykBank(KZT)",
        "Humo UZS": "Карта HUMO(UZS)",
        "Jysan Bank KZT": "Jysan Bank(KZT)",
        "KASPI BANK KZT": "Kaspi Bank(KZT)",
        "Komodo KMD": "Komodo(KMD)",
        "LISK LSK": "LISK(LSK)",
        "Litecoin LTC": "Litecoin(LTC)",
        "LiteCoin LTC": "Litecoin(LTC)",
        "Litecoin (LTC) LTC": "Litecoin(LTC)",
        "Maker (ERC20) MKR": "Maker(MKR)",
        "Master/Visa RUB": "Visa/MasterCard(RUB)",
        "Mercado Pago ARS": "Mercado Pago(ARS)",
        "Monero XMR": "Monero(XMR)",
        "Monero (XMR) XMR": "Monero(XMR)",
        "NEM XEM": "NEM(XEM)",
        "NEO NEO": "NEO(NEO)",
        "OMG Network": "OMG Network(OMG)",
        "OMG Network (ERC20) OMG": "OMG Network(OMG)",
        "Paxos PAX": "Paxos(PAX)",
        "Payeer RUB": "Payeer(RUB)",
        "Payeer USD": "Payeer(USD)",
        "PayPal USD": "PayPal(USD)",
        "Perfect Money EUR": "Perfect Money(EUR)",
        "Perfect Money USD": "Perfect Money(USD)",
        "PM e-Voucher USD": "PM e-Voucher(USD)",
        "Polkadot DOT": "Polkadot(DOT)",
        "PolkaDOT DOT": "Polkadot(DOT)",
        "Polygon (ERC20) MATIC": "Polygon(MATIC)",
        "Polygon (Polygon) MATIC": "Polygon(MATIC)",
        "Qiwi RUB": "QIWI(RUB)",
        "Qtum QTUM": "Qtum(QTUM)",
        "Ravencoin RVN": "Ravencoin(RVN)",
        "Revolut EUR": "Revolut(EUR)",
        "Revolut USD": "Revolut(USD)",
        "Ripple XRP": "Ripple(XRP)",
        "Ripple (XRP) XRP": "Ripple(XRP)",
        "|В|Т|Б| RUB": "ВТБ(RUB)",
        "Тинькофф RUB": "Тинькофф(RUB)",
        "JasmyCoin JASMY": "JasmyCoin(JASMY)",
        "Mercadopago ARS": "Mercado Pago(ARS)",
        "LItecoin LTC": "Litecoin(LTC)",
        "OMG Network OMG": "OMG Network(OMG)",
        "Sepa EUR": "SEPA(EUR)",
        "Shiba BEP20 SHIB": "Shiba (SHIB)",
        "Shiba Inu SHIB": "Shiba (SHIB)",
        "SOL SOL": "Solana(SOL)",
        "Stellarlumens XLM": "Stellar(XLM)",
        "TEST TEST": "other",
        "Tether BEP-20 USDT": "Tether BEP20(USDT)",
        "Tether ERC20 Antalya USDTERC": "Tether ERC20(USDT)",
        "Tether ERC20 Sankt-Peterburg USDTERC": "Tether ERC20(USDT)",
        "Tether ERC20 Stambul USDTERC": "Tether ERC20(USDT)",
        "Tether SOL USDT": "Tether SOL(USDT)",
        "Tether TRC20 Antalya USDTTRC": "Tether TRC20(USDT)",
        "Tether TRC-20 USDT": "Tether TRC20(USDT)",
        "Tether (TRC-20) USDT": "Tether TRC20(USDT)",
        "Tezos XTZ": "Tezos(XTZ)",
        "Toncoin TON": "Toncoin(TON)",
        "Tron TRX": "TRON(TRX)",
        "True USD ERC20 TUSD": "TrueUSD ERC20(TUSD)",
        "TrueUSD ERC20 TUSD": "TrueUSD ERC20(TUSD)",
        "UnionPay CNY": "UnionPay(CNY)",
        "USDCoin BEP20 USDC": "USDCoin BEP20(USDC)",
        "USD coin ERC20 USDC": "USDCoin ERC20(USDC)",
        "USDCoin SOL USDC": "USDCoin SOL(USDC)",
        "Visa MasterCard EUR": "Visa/MasterCard(EUR)",
        "Visa/MasterCard KGS KGS": "Visa/MasterCard(KGS)",
        "Visa/MasterCard KZT KZT": "Visa/MasterCard(KZT)",
        "Visa/MasterCard RUB": "Visa/MasterCard(RUB)",
        "VISA MASTERCARD TRY": "Visa/MasterCard(TRY)",
        "Visa/Mastercard UAH": "Visa/MasterCard(UAH)",
        "Visa/Master Card UAH": "Visa/MasterCard(UAH)",
        "Visa MasterCard USD": "Visa/MasterCard(USD)",
        "VISAMASTERCARD Грузия GEL": "Visa/MasterCard(GEL)",
        "VISA/MasterCard КZ KZT": "Visa/MasterCard(KZT)",
        "Visa/MasterCard Казахстан KZT": "Visa/MasterCard(KZT)",
        "VISA MASTER КЗТ KZT": "Visa/MasterCard(KZT)",
        "VISA MASTER Турции TRY": "Visa/MasterCard(TRY)",
        "VISA/MC KGS": "Visa/MasterCard(KGS)",
        "VISA/MC KZT": "Visa/MasterCard(KZT)",
        "Webmoney USD": "Webmoney(USD)",
        "WeChat CNY": "WeChat(CNY)",
        "WhiteBit ERC20 WBT": "WhiteBit(WBT)",
        "WhiteBIT TRC20 WBT": "WhiteBit(WBT)",
        "WISE EUR": "WISE(EUR)",
        "Альфа (cash-in) RUB": "Альфа cash-in(RUB)",
        "Альфа Cash-in RUB": "Альфа cash-in(RUB)",
        "Альфа-банк Cash-in RUB": "Альфа cash-in(RUB)",
        "Альфа Банк RUB": "Альфа-банк(RUB)",
        "Альфа-Банк UAH": "Альфа-банк(UAH)",
        "Ethereum Classic ETC": "Ethereum Classic(ETC)",
        "Sepa Instant EUR": "Sepa(EUR)",
        "TrueUSD TRC20 TUSD": "TrueUSD ERC20(TUSD)",
        "WebMoney USD": "Webmoney(USD)",
        "WISE USD": "WISE(USD)",
        "Банковский счёт AED": "Банковский счёт(AED)",
        "Банковский счёт ARS": "Банковский счёт(ARS)",
        "Банковский счёт AUD": "Банковский счёт(AUD)",
        "Банковский счёт CAD": "Банковский счёт(CAD)",
        "Банковский счёт CNY": "Банковский счёт(CNY)",
        "Банковский счет EUR": "Банковский счет(EUR)",
        "Банковский счёт GEL": "Банковский счёт(GEL)",
        "Банковский счёт HKD": "Банковский счёт(HKD)",
        "Банковский счет IDR": "Банковский счет(IDR)",
        "Банковский счёт INR": "Банковский счёт(INR)",
        "Банковский счёт JPY": "Банковский счёт(JPY)",
        "Банковский счёт KRW": "Банковский счёт(KRW)",
        "Банковский счёт MNT": "Банковский счёт(MNT)",
        "Банковский счёт NZD": "Банковский счёт(NZD)",
        "Банковский счёт PHP": "Банковский счёт(PHP)",
        "Банковский счет THB": "Банковский счет(THB)",
        "Банковский счет THB THB": "Банковский счет(THB)",
        "Банковский счёт TRY": "Банковский счёт(TRY)",
        "Банковский счет USD": "Банковский счет(USD)",
        "ВТБ банк RUB": "ВТБ(RUB)",
        "Газпромбанк RUB": "Газпромбанк(RUB)",
        "Карта UnionPay CNY": "Карта UnionPay(CNY)",
        "Карта Элкарт KGS": "Карта Элкарт(KGS)",
        "Карты КZ KZT": "Visa/MasterCard(KZT)",
        "Карты РФ RUB": "Visa/MasterCard(RUB)",
        "Любая карта(RUB)": "Visa/MasterCard(RUB)",
        "Любой банк Таиланда": "Visa/MasterCard(THB)",
        "Любой банк Турции": "Visa/MasterCard(TRY)",
        "Монобанк UAH": "Монобанк(UAH)",
        "МТС Банк RUB": "МТС банк(RUB)",
        "НАЛ AED": "Наличные(AED)",
        "НАЛ EUR": "Наличные(EUR)",
        "НАЛ TRY": "Наличные(TRY)",
        "НАЛ USD": "Наличные(USD)",
        "Наличные AED": "Наличные(AED)",
        "Наличные AMD": "Наличные(AMD)",
        "Наличные Antalya TRY": "Наличные(TRY)",
        "Наличные Antalya USD": "Наличные(USD)",
        "Наличные(USD)": "Наличные(EUR)",
        "Наличные IDR": "Наличные(IDR)",
        "Наличные ILS": "Наличные(ILS)",
        "Наличные Sankt-Peterburg RUB": "Наличные(RUB)",
        "Наличные Stambul TRY": "Наличные(TRY)",
        "Наличные Stambul USD": "Наличные(USD)",
        "Наличные THB": "Наличные(THB)",
        "Наличные USD": "Наличные(USD)",
        "Наличные Аланья TRY": "Наличные(TRY)",
        "Наличные(TRY)": "Наличные(USD)",
        "Наличные Анталия USD": "Наличные(USD)",
        "Наличные Анталья TRY": "Наличные(TRY)",
        "Наличные Астрахань RUB": "Наличные(RUB)",
        "Наличные(TRY)": "Наличные(USD)",
        "Наличные Бали IDR": "Наличные(IDR)",
        "Наличные Бали USD": "Наличные(USD)",
        "Наличные Бангкок": "Наличные(USD)",
        "Наличные Батуми USD": "Наличные(USD)",
        "Наличные Валенсия EUR": "Наличные(EUR)",
        "Наличные Владивосток USD": "Наличные(USD)",
        "Наличные-Владимир RUB": "Наличные(RUB)",
        "Наличные Волгоград RUB": "Наличные(RUB)",
        "Наличные Волгоград USD": "Наличные(USD)",
        "Наличные Дубай AED": "Наличные(AED)",
        "Наличные Дубай USD": "Наличные(USD)",
        "Наличные Екатеринбург RUB": "Наличные(RUB)",
        "Наличные ЕКБ RUB": "Наличные(RUB)",
        "Наличные-Елец RUB": "Наличные(RUB)",
        "Наличные Ереван USD": "Наличные(USD)",
        "Наличные (ЕС) EUR": "Наличные(USD)",
        "Наличные Йошкар-Ола USD": "Наличные(USD)",
        "Наличные Казань RUB": "Наличные(RUB)",
        "Наличные-Калуга RUB": "Наличные(RUB)",
        "Наличные Кито USD": "Наличные(USD)",
        "Наличные(USD)": "Наличные(RUB)",
        "Наличные Краби": "Наличные(RUB)",
        "Наличные Красноярск RUB": "Наличные(RUB)",
        "Наличные Красноярск USD": "Наличные(USD)",
        "Наличные Магнитогорск USD": "Наличные(USD)",
        "Наличные Москва EUR": "Наличные(EUR)",
        "Наличные Москва RUB": "Наличные(RUB)",
        "Наличные Москва USD": "Наличные(USD)",
        "Наличные МСК EUR": "Наличные(EUR)",
        "Наличные МСК USD": "Наличные(USD)",
        "Наличные Мурманск RUB": "Наличные(RUB)",
        "Наличные-Наб. Челны RUB": "Наличные(RUB)",
        "Наличные Омск RUB": "Наличные(RUB)",
        "Наличные Омск USD": "Наличные(RUB)",
        "Наличные Паттайя": "Наличные(THB)",
        "Наличные Пермь RUB": "Наличные(RUB)",
        "Наличные Пермь USD": "Наличные(RUB)",
        "Наличные Пханган": "Наличные(THB)",
        "Наличные Пхукет": "Наличные(THB)",
        "Наличные-Ростов RUB": "Наличные(RUB)",
        "Наличные Ростов-на-Дону RUB": "Наличные(RUB)",
        "Наличные-Рязань RUB": "Наличные(RUB)",
        "Наличные Самара RUB": "Наличные(RUB)",
        "Наличные Аланья USD": "Наличные(USD)",
        "Наличные Астрахань USD": "Наличные(USD)",
        "Наличные ЕКБ USD": "Наличные(USD)",
        "Наличные-Казань RUB": "Наличные(RUB)",
        "Наличные Казань USD": "Наличные(USD)",
        "Наличные-Кострома RUB": "Наличные(RUB)",
        "Наличные-Орел RUB": "Наличные(RUB)",
        "Наличные Самара USD": "Наличные(USD)",
        "Наличные Самуи": "Наличные(THB)",
        "Наличные Санкт-Петербург RUB": "Наличные(RUB)",
        "Наличные Санкт-Петербург USD": "Наличные(USD)",
        "Наличные Саратов RUB": "Наличные(RUB)",
        "Наличные Саратов USD": "Наличные(USD)",
        "Наличные (Северный Кипр) USD": "Наличные(USD)",
        "Наличные СПБ RUB": "Наличные(RUB)",
        "Наличные Стамбул USD": "Наличные(USD)",
        "Наличные-Тамбов RUB": "Наличные(RUB)",
        "Наличные Тбилиси USD": "Наличные(USD)",
        "Наличные-Тверь RUB": "Наличные(RUB)",
        "Наличные-Тула RUB": "Наличные(RUB)",
        "Наличные Тюмень RUB": "Наличные(RUB)",
        "Наличные Тюмень USD": "Наличные(USD)",
        "Наличные (Украина) USD": "Наличные(USD)",
        "Наличные Чанг": "Наличные(THB)",
        "Наличные Челябинск RUB": "Наличные(RUB)",
        "Наличные-Ярославль RUB": "Наличные(RUB)",
        "Открытие RUB": "Открытие(RUB)",
        "ОщадБанк UAH": "ОщадБанк(UAH)",
        "Приват24 UAH": "Приват24(UAH)",
        "Промсвязьбанк RUB": "Промсвязьбанк(RUB)",
        "Райфайзен RUB": "Райффайзен(RUB)",
        "Райффайзен UAH": "Райффайзен(UAH)",
        "Райффайзен банк RUB": "Райффайзен(RUB)",
        "РНКБ RUB": "РНКБ(RUB)",
        "Россельхоз банк RUB": "Россельхозбанк(RUB)",
        "Россельхозбанк RUB": "Россельхозбанк(RUB)",
        "Ростов-на-Дону RUB": "Наличные(RUB)",
        "РС (cash-in) RUB": "Русский Стандарт(RUB) ",
        "Русский Стандарт RUB": "Русский Стандарт(RUB)",
        "Сальдо BTC": "Bitcoin(BTC)",
        "Сальдо USDT": "Tether ERC20(USDT)",
        "Сбербанк KZT": "Сбербанк(KZT)",
        "СберБанк RUB": "Сбербанк(RUB)",
        "Ситибанк RUB": "Ситибанк(RUB)",
        "Совкомбанк RUB": "Совкомбанк(RUB)",
        "Тинькофф cash-in RUB": "Тинькофф cash-in(RUB)",
        "Тинькофф Mir Pay RUB": "Карта Мир(RUB)",
        "Тинькофф QR RUB": "Тинькофф QR(RUB)",
        "Тинькофф Банк RUB": "Тинькофф(RUB)",
        "ТКС (cash-in) RUB": "Тинькофф cash-in(RUB)",
        "ТКС cash-in RUB": "Тинькофф cash-in(RUB)",
        "Турецкая Лира TRY": "Visa/MasterCard(TRY)",
        "Укрсиббанк UAH": "Укрсиббанк(UAH)",
        "Уралсиб RUB": "Уралсиб(RUB)",
        "Хоум Кредит RUB": "Хоум Кредит(RUB)",
        "Хоум Кредит Банк RUB": "Хоум Кредит(RUB)",
        "Пумб UAH": "Пумб(UAH)",
        "Наличные Челябинск USD": "Наличные(USD)",
        "Наличные СПБ USD": "Наличные(USD)",
        "Наличные Sankt-Peterburg USD": "Наличные(USD)",
        "Tether TRC20 Sankt-Peterburg USDTTRC": "Наличные(USD)",
        "Tether TRC20 Stambul USDTTRC": "Наличные(USD)",
        "Tether OMNI USDT": "Tether OMNI(USDT)",
        "Банковский счёт EUR": "Банковский счёт(EUR)",
        "Банковский счёт USD": "Банковский счёт(USD)",
        "Наличные EUR": "Наличные(EUR)",
        "Bat BAT": "BAT(BAT)",
        "Bitcoin (BEP-20) BTC": "Bitcoin BEP20(BTCB)",
        "Bitcoin CashSV BSV": "Bitcoin SV(BSV)",
        "Dai (BEP-20) DAI": "DAI(DAI)",
        "Dai DAI USD": "DAI(DAI)",
        "Dai (ERC-20) DAI": "DAI(DAI)",
        "Dashcoin DASH": "Dashcoin(DASH)",
        "Ethereum (BEP-20) ETH": "Ethereum BEP20(ETH)",
        "IOTA MIOTA": "IOTA(MIOTA)",
        "MONERO XMR": "Monero(XMR)",
        "Tether Omni USDT": "Tether OMNI(USDT)",
        "VISA/MasterCard/Мир RUB": "Visa/MasterCard(RUB)",
        "Visa/MasterCard РФ RUB": "Visa/MasterCard(RUB)",
        "ZCash ZEC": "Zcash(ZEC)",
        "Альфабанк RUB": "Альфа-банк(RUB)",
        "ВТБ Банк RUB": "ВТБ(RUB)",
        "Карта МИР RUB": "Карта Мир(RUB)",
        "МоноБанк UAH": "Монобанк(UAH)",
        "Наличные TRY": "Наличные(TRY)",
        "Счет ИП или ООО RUB": "Наличные(RUB)",
        "Тинькофф банк RUB": "Тинькофф(RUB)",
        "ТКС QR-код RUB": "Тинькофф QR(RUB)",

        # Добавьте другие соответствия по мере необходимости
    }

    receive_pair_name_mapping_dict = {
        "Сбербанк RUB": "Сбербанк(RUB)",
        "EOS EOS": "EOS(EOS)",
        "BinanceCoin BEP20 BNB": "BinanceCoin BEP20(BNB)",
        "Binance Coin BEP20 BNB": "BinanceCoin BEP20(BNB)",
        "BinanceCoin BEP2 BNB": "BinanceCoin BEP20(BNB)",
        "Binance Coin (BSC) BNB": "BinanceCoin BEP20(BNB)",
        "Polygon MATIC": "Polygon(MATIC)",
        "Bitcoin BTC": "Bitcoin(BTC)",
        "Ethereum ETH": "Ethereum(ETH)",
        "Ethereum BEP20 ETH": "Ethereum BEP20(ETH)",
        "Bitcoin Cash BCH": "Bitcoin Cash(BCH)",
        "Ripple XRP": "Ripple(XRP)",
        "ERC20 USDT": "Tether ERC20(USDT)",
        "OMNI USDT": "Tether OMNI(USDT)",
        "TRC20 USDT": "Tether TRC20(USDT)",
        "BEP20 USDT": "Tether BEP20(USDT)",
        "Tether BEP20 USDT": "Tether BEP20(USDT)",
        "USDCoin ERC20 USDC": "USDCoin ERC20(USDC)",
        "Dai DAI": "DAI(DAI)",
        "Stellar XLM": "Stellar(XLM)",
        "Pax Dollar USDP": "Pax Dollar(USDP)",
        "NEM XEM": "NEM(XEM)",
        "USD Coin ERC20 USDC": "USDCoin ERC20(USDC)",
        "NEO NEO": "NEO(NEO)",
        "TUSD": "TUSD(True USD ERC20)",
        "MIOTA IOTA": "IOTA(MIOTA)",
        "Cardano ADA": "Cardano(ADA)",
        "OmiseGO OMG": "OMG Network(OMG)",
        "Verge XVG": "Verge(XVG)",
        "Solana SOL": "Solana(SOL)",
        "ICON ICX": "ICON(ICX)",
        "Cosmos ATOM": "Cosmos(ATOM)",
        "Chainlink LINK": "Chainlink(LINK)",
        "Ontology ONT": "Ontology(ONT)",
        "BAT BAT": "BAT(BAT)",
        "USD Coin TRC20 USDC": "USDCoin TRC20(USD)",
        "Тинькофф RUB": "Тинькофф(RUB)",
        "Visa MasterCard RUB": "Visa/MasterCard(RUB)",
        "СБП RUB": "СБП(RUB)",
        "Росбанк RUB": "Росбанк(RUB)",
        "Альфа банк RUB": "Альфа-банк(RUB)",
        "Карта Мир RUB": "Карта Мир(RUB)",
        "Почта Банк RUB": "Почта Банк(RUB)",
        "ВТБ RUB": "ВТБ(RUB)",
        "Kaspi Bank KZT": "Kaspi Bank(KZT)",
        "Райффайзен Банк RUB": "Райффайзен(RUB)",
        "BinanceCoin ERC20 BNB": "BinanceCoin ERC20(BNB)",
        "Наличные МСК RUB": "Наличные(RUB)",
        "Dash DASH": "Dash(DASH)",
        "ForteBank KZT": "ForteBank(KZT)",
        "Zcash ZEC": "Zcash(ZEC)",
        "HalykBank KZT": "HalykBank(KZT)",
        "Waves WAVES": "Waves(WAVES)",
        "Jusan Bank KZT": "Jusan Bank(KZT)",
        "VISA MASTERCARD Казахстан KZT": "VISA/MASTERCARD(KZT)",
        "Dogecoin DOGE": "Dogecoin(DOGE)",
        "TRON TRX": "TRON(TRX)",
        "Авангард RUB": "Авангард(RUB)",
        "Тинькофф Онлайн RUB": "Тинькофф(RUB)",
        "ВТБ 24 RUB": "ВТБ(RUB)",
        "Tether ERC20 USDT": "Tether ERC20(USDT)",
        "Tether (ERC20) USDT": "USDT(ERC20)",
        "Альфа-Банк RUB": "Альфа-банк(RUB)",
        "VeChain VET": "VeChain(VET)",
        "Ethereum (ERC-20) ETH": "Ethereum(ETH)",
        "Uniswap UNI": "Uniswap(UNI)",
        "Payeer EUR": "Payeer(EUR)",
        "Tether TRC20 USDT": "Tether TRC20(USDT)",
        "VISA/MC RUB": "Visa/MasterCard(RUB)",
        "USDCoin TRC20 USDC": "USDCoin TRC20(USDC)",
        "Наличные RUB": "Наличные(RUB)",
        "Любая карта RUB": "Любая карта(RUB)",
        "Райффайзен RUB": "Райффайзен(RUB)",
        "QIWI RUB": "QIWI(RUB)",
        "ЮMoney RUB": "ЮMoney(RUB)",
        "Тезер TRC20 USDT": "Tether TRC20(USDT)",
        "Сальдо LTC": "Tether TRC20(USDT)",
        "Visa/MasterCard KZT": "Visa/MasterCard(KZT)",
        "Евразийский KZT": "Евразийский(KZT)",
        "Тезер BEP20 USDT": "Tether BEP20(USDT)",
        "0x (ERC20) ZRX": "0x(ZRX)",
        "0x ZRX": "0x(ZRX)",
        "ADV Cash EUR": "Advcash(EUR)",
        "ADV Cash KZT": "Advcash(KZT)",
        "Advcash RUB": "Advcash(RUB)",
        "ADV Cash TRY": "Advcash(TRY)",
        "Advcash USD": "Advcash(USD)",
        "ADV Cash USD": "Advcash(USD)",
        "Alipay CNY": "Alipay(CNY)",
        "Avalanche AVAX": "Avalanche(AVAX)",
        "Avalanche (CCHAIN) AVAX": "Avalanche(AVAX)",
        "BAT BAT": "BAT(BAT)",
        "BAT (ERC20) BAT": "BAT(BAT)",
        "Binance USD (BEP20) BUSD": "Binance USD(BUSD)",
        "Binance USD (BSC) BUSD": "Binance USD(BUSD)",
        "Binance USD BUSD": "Binance USD(BUSD)",
        "Bitcoin Antalya BTC": "Bitcoin(BTC)",
        "Bitcoin Bep20 BTC": "Bitcoin(BTCB)",
        "BitCoin BTC": "Bitcoin(BTC)",
        "Bitcoin (BTC) BTC": "Bitcoin(BTC)",
        "Bitcoin Cash BCH": "Bitcoin Cash(BCH)",
        "Bitcoin Cash (BCH) BCH": "Bitcoin Cash(BCH)",
        "Bitcoin Gold BTG": "Bitcoin Gold(BTG)",
        "Bitcoin Sankt-Peterburg BTC": "Bitcoin(BTC)",
        "Bitcoin Stambul BTC": "Bitcoin(BTC)",
        #"+ BTC": "Bitcoin(BTC)",
        "'BTC'": "Bitcoin(BTC)",
        "Cardano (ADA) ADA": "Cardano(ADA)",
        "ChainLink (ERC20) LINK": "ChainLink(LINK)",
        "Chainlink LINK": "ChainLink(LINK)",
        "ChainLink LINK": "ChainLink(LINK)",
        "DAI DAI": "DAI(DAI)",
        "DAI ERC20 DAI": "DAI(DAI)",
        "DAI (ERC20) DAI": "DAI(DAI)",
        "Dash DASH": "Dash(DASH)",
        "DASH DASH": "Dash(DASH)",
        "Dash (DASH) DASH": "Dash(DASH)",
        "Decentraland (ERC20) MANA": "Decentraland(MANA)",
        "Dogecoin DOGE": "Dogecoin(DOGE)",
        "DogeCoin DOGE": "Dogecoin(DOGE)",
        "Doge (DOGE) DOGE": "Dogecoin(DOGE)",
        "EOS EOS": "EOS(EOS)",
        "EOS (EOS) EOS": "EOS(EOS)",
        "ERC20 USDT": "Tether ERC20(USDT)",
        "ETH": "Ethereum(ETH)",
        "Ethereum Antalya ETH": "Ethereum(ETH)",
        "Ethereum ERC20 ETH": "Ethereum(ETH)",
        "Ethereum (ERC20) ETH": "Ethereum(ETH)",
        "Ethereum Sankt-Peterburg ETH": "Ethereum(ETH)",
        "Ethereum Stambul ETH": "Ethereum(ETH)",
        "Ether Classic ETC": "Ethereum Classic(ETC)",
        "Faster Payment systеm HKD": "Банковский счет(HKD)",
        "Halyk Bank KZT": "HalykBank(KZT)",
        "Humo UZS": "Карта HUMO(UZS)",
        "Jysan Bank KZT": "Jysan Bank(KZT)",
        "KASPI BANK KZT": "Kaspi Bank(KZT)",
        "Komodo KMD": "Komodo(KMD)",
        "LISK LSK": "LISK(LSK)",
        "Litecoin LTC": "Litecoin(LTC)",
        "LiteCoin LTC": "Litecoin(LTC)",
        "Litecoin (LTC) LTC": "Litecoin(LTC)",
        "Maker (ERC20) MKR": "Maker(MKR)",
        "Master/Visa RUB": "Visa/MasterCard(RUB)",
        "Mercado Pago ARS": "Mercado Pago(ARS)",
        "Monero XMR": "Monero(XMR)",
        "Monero (XMR) XMR": "Monero(XMR)",
        "NEM XEM": "NEM(XEM)",
        "NEO NEO": "NEO(NEO)",
        "OMG Network": "OMG Network(OMG)",
        "OMG Network (ERC20) OMG": "OMG Network(OMG)",
        "Paxos PAX": "Paxos(PAX)",
        "Payeer RUB": "Payeer(RUB)",
        "Payeer USD": "Payeer(USD)",
        "PayPal USD": "PayPal(USD)",
        "Perfect Money EUR": "Perfect Money(EUR)",
        "Perfect Money USD": "Perfect Money(USD)",
        "PM e-Voucher USD": "PM e-Voucher(USD)",
        "Polkadot DOT": "Polkadot(DOT)",
        "PolkaDOT DOT": "Polkadot(DOT)",
        "Polygon (ERC20) MATIC": "Polygon(MATIC)",
        "Polygon (Polygon) MATIC": "Polygon(MATIC)",
        "Qiwi RUB": "QIWI(RUB)",
        "Qtum QTUM": "Qtum(QTUM)",
        "Ravencoin RVN": "Ravencoin(RVN)",
        "Revolut EUR": "Revolut(EUR)",
        "Revolut USD": "Revolut(USD)",
        "Ripple XRP": "Ripple(XRP)",
        "Ripple (XRP) XRP": "Ripple(XRP)",
        "|В|Т|Б| RUB": "ВТБ(RUB)",
        "Тинькофф RUB": "Тинькофф(RUB)",
        "JasmyCoin JASMY": "JasmyCoin(JASMY)",
        "Mercadopago ARS": "Mercado Pago(ARS)",
        "LItecoin LTC": "Litecoin(LTC)",
        "OMG Network OMG": "OMG Network(OMG)",
        "Sepa EUR": "SEPA(EUR)",
        "Shiba BEP20 SHIB": "Shiba (SHIB)",
        "Shiba Inu SHIB": "Shiba (SHIB)",
        "SOL SOL": "Solana(SOL)",
        "Stellarlumens XLM": "Stellar(XLM)",
        "TEST TEST": "other",
        "Tether BEP-20 USDT": "Tether BEP20(USDT)",
        "Tether ERC20 Antalya USDTERC": "Tether ERC20(USDT)",
        "Tether ERC20 Sankt-Peterburg USDTERC": "Tether ERC20(USDT)",
        "Tether ERC20 Stambul USDTERC": "Tether ERC20(USDT)",
        "Tether SOL USDT": "Tether SOL(USDT)",
        "Tether TRC20 Antalya USDTTRC": "Tether TRC20(USDT)",
        "Tether TRC-20 USDT": "Tether TRC20(USDT)",
        "Tether (TRC-20) USDT": "Tether TRC20(USDT)",
        "Tezos XTZ": "Tezos(XTZ)",
        "Toncoin TON": "Toncoin(TON)",
        "Tron TRX": "TRON(TRX)",
        "True USD ERC20 TUSD": "TrueUSD ERC20(TUSD)",
        "TrueUSD ERC20 TUSD": "TrueUSD ERC20(TUSD)",
        "UnionPay CNY": "UnionPay(CNY)",
        "USDCoin BEP20 USDC": "USDCoin BEP20(USDC)",
        "USD coin ERC20 USDC": "USDCoin ERC20(USDC)",
        "USDCoin SOL USDC": "USDCoin SOL(USDC)",
        "Visa MasterCard EUR": "Visa/MasterCard(EUR)",
        "Visa/MasterCard KGS KGS": "Visa/MasterCard(KGS)",
        "Visa/MasterCard KZT KZT": "Visa/MasterCard(KZT)",
        "Visa/MasterCard RUB": "Visa/MasterCard(RUB)",
        "VISA MASTERCARD TRY": "Visa/MasterCard(TRY)",
        "Visa/Mastercard UAH": "Visa/MasterCard(UAH)",
        "Visa/Master Card UAH": "Visa/MasterCard(UAH)",
        "Visa MasterCard USD": "Visa/MasterCard(USD)",
        "VISAMASTERCARD Грузия GEL": "Visa/MasterCard(GEL)",
        "VISA/MasterCard КZ KZT": "Visa/MasterCard(KZT)",
        "Visa/MasterCard Казахстан KZT": "Visa/MasterCard(KZT)",
        "VISA MASTER КЗТ KZT": "Visa/MasterCard(KZT)",
        "VISA MASTER Турции TRY": "Visa/MasterCard(TRY)",
        "VISA/MC KGS": "Visa/MasterCard(KGS)",
        "VISA/MC KZT": "Visa/MasterCard(KZT)",
        "Webmoney USD": "Webmoney(USD)",
        "WeChat CNY": "WeChat(CNY)",
        "WhiteBit ERC20 WBT": "WhiteBit(WBT)",
        "WhiteBIT TRC20 WBT": "WhiteBit(WBT)",
        "WISE EUR": "WISE(EUR)",
        "Альфа (cash-in) RUB": "Альфа cash-in(RUB)",
        "Альфа Cash-in RUB": "Альфа cash-in(RUB)",
        "Альфа-банк Cash-in RUB": "Альфа cash-in(RUB)",
        "Альфа Банк RUB": "Альфа-банк(RUB)",
        "Альфа-Банк UAH": "Альфа-банк(UAH)",
        "Ethereum Classic ETC": "Ethereum Classic(ETC)",
        "Sepa Instant EUR": "Sepa(EUR)",
        "TrueUSD TRC20 TUSD": "TrueUSD ERC20(TUSD)",
        "WebMoney USD": "Webmoney(USD)",
        "WISE USD": "WISE(USD)",
        "Банковский счёт AED": "Банковский счёт(AED)",
        "Банковский счёт ARS": "Банковский счёт(ARS)",
        "Банковский счёт AUD": "Банковский счёт(AUD)",
        "Банковский счёт CAD": "Банковский счёт(CAD)",
        "Банковский счёт CNY": "Банковский счёт(CNY)",
        "Банковский счет EUR": "Банковский счет(EUR)",
        "Банковский счёт GEL": "Банковский счёт(GEL)",
        "Банковский счёт HKD": "Банковский счёт(HKD)",
        "Банковский счет IDR": "Банковский счет(IDR)",
        "Банковский счёт INR": "Банковский счёт(INR)",
        "Банковский счёт JPY": "Банковский счёт(JPY)",
        "Банковский счёт KRW": "Банковский счёт(KRW)",
        "Банковский счёт MNT": "Банковский счёт(MNT)",
        "Банковский счёт NZD": "Банковский счёт(NZD)",
        "Банковский счёт PHP": "Банковский счёт(PHP)",
        "Банковский счет THB": "Банковский счет(THB)",
        "Банковский счет THB THB": "Банковский счет(THB)",
        "Банковский счёт TRY": "Банковский счёт(TRY)",
        "Банковский счет USD": "Банковский счет(USD)",
        "ВТБ банк RUB": "ВТБ(RUB)",
        "Газпромбанк RUB": "Газпромбанк(RUB)",
        "Карта UnionPay CNY": "Карта UnionPay(CNY)",
        "Карта Элкарт KGS": "Карта Элкарт(KGS)",
        "Карты КZ KZT": "Visa/MasterCard(KZT)",
        "Карты РФ RUB": "Visa/MasterCard(RUB)",
        "Любая карта(RUB)": "Visa/MasterCard(RUB)",
        "Любой банк Таиланда": "Visa/MasterCard(THB)",
        "Любой банк Турции": "Visa/MasterCard(TRY)",
        "Монобанк UAH": "Монобанк(UAH)",
        "МТС Банк RUB": "МТС банк(RUB)",
        "НАЛ AED": "Наличные(AED)",
        "НАЛ EUR": "Наличные(EUR)",
        "НАЛ TRY": "Наличные(TRY)",
        "НАЛ USD": "Наличные(USD)",
        "Наличные AED": "Наличные(AED)",
        "Наличные AMD": "Наличные(AMD)",
        "Наличные Antalya TRY": "Наличные(TRY)",
        "Наличные Antalya USD": "Наличные(USD)",
        "Наличные(USD)": "Наличные(EUR)",
        "Наличные IDR": "Наличные(IDR)",
        "Наличные ILS": "Наличные(ILS)",
        "Наличные Sankt-Peterburg RUB": "Наличные(RUB)",
        "Наличные Stambul TRY": "Наличные(TRY)",
        "Наличные Stambul USD": "Наличные(USD)",
        "Наличные THB": "Наличные(THB)",
        "Наличные USD": "Наличные(USD)",
        "Наличные Аланья TRY": "Наличные(TRY)",
        "Наличные(TRY)": "Наличные(USD)",
        "Наличные Анталия USD": "Наличные(USD)",
        "Наличные Анталья TRY": "Наличные(TRY)",
        "Наличные Астрахань RUB": "Наличные(RUB)",
        "Наличные(TRY)": "Наличные(USD)",
        "Наличные Бали IDR": "Наличные(IDR)",
        "Наличные Бали USD": "Наличные(USD)",
        "Наличные Бангкок": "Наличные(USD)",
        "Наличные Батуми USD": "Наличные(USD)",
        "Наличные Валенсия EUR": "Наличные(EUR)",
        "Наличные Владивосток USD": "Наличные(USD)",
        "Наличные-Владимир RUB": "Наличные(RUB)",
        "Наличные Волгоград RUB": "Наличные(RUB)",
        "Наличные Волгоград USD": "Наличные(USD)",
        "Наличные Дубай AED": "Наличные(AED)",
        "Наличные Дубай USD": "Наличные(USD)",
        "Наличные Екатеринбург RUB": "Наличные(RUB)",
        "Наличные ЕКБ RUB": "Наличные(RUB)",
        "Наличные-Елец RUB": "Наличные(RUB)",
        "Наличные Ереван USD": "Наличные(USD)",
        "Наличные (ЕС) EUR": "Наличные(USD)",
        "Наличные Йошкар-Ола USD": "Наличные(USD)",
        "Наличные Казань RUB": "Наличные(RUB)",
        "Наличные-Калуга RUB": "Наличные(RUB)",
        "Наличные Кито USD": "Наличные(USD)",
        "Наличные(USD)": "Наличные(RUB)",
        "Наличные Краби": "Наличные(RUB)",
        "Наличные Красноярск RUB": "Наличные(RUB)",
        "Наличные Красноярск USD": "Наличные(USD)",
        "Наличные Магнитогорск USD": "Наличные(USD)",
        "Наличные Москва EUR": "Наличные(EUR)",
        "Наличные Москва RUB": "Наличные(RUB)",
        "Наличные Москва USD": "Наличные(USD)",
        "Наличные МСК EUR": "Наличные(EUR)",
        "Наличные МСК USD": "Наличные(USD)",
        "Наличные Мурманск RUB": "Наличные(RUB)",
        "Наличные-Наб. Челны RUB": "Наличные(RUB)",
        "Наличные Омск RUB": "Наличные(RUB)",
        "Наличные Омск USD": "Наличные(RUB)",
        "Наличные Паттайя": "Наличные(THB)",
        "Наличные Пермь RUB": "Наличные(RUB)",
        "Наличные Пермь USD": "Наличные(RUB)",
        "Наличные Пханган": "Наличные(THB)",
        "Наличные Пхукет": "Наличные(THB)",
        "Наличные-Ростов RUB": "Наличные(RUB)",
        "Наличные Ростов-на-Дону RUB": "Наличные(RUB)",
        "Наличные-Рязань RUB": "Наличные(RUB)",
        "Наличные Самара RUB": "Наличные(RUB)",
        "Наличные Аланья USD": "Наличные(USD)",
        "Наличные Астрахань USD": "Наличные(USD)",
        "Наличные ЕКБ USD": "Наличные(USD)",
        "Наличные-Казань RUB": "Наличные(RUB)",
        "Наличные Казань USD": "Наличные(USD)",
        "Наличные-Кострома RUB": "Наличные(RUB)",
        "Наличные-Орел RUB": "Наличные(RUB)",
        "Наличные Самара USD": "Наличные(USD)",
        "Наличные Самуи": "Наличные(THB)",
        "Наличные Санкт-Петербург RUB": "Наличные(RUB)",
        "Наличные Санкт-Петербург USD": "Наличные(USD)",
        "Наличные Саратов RUB": "Наличные(RUB)",
        "Наличные Саратов USD": "Наличные(USD)",
        "Наличные (Северный Кипр) USD": "Наличные(USD)",
        "Наличные СПБ RUB": "Наличные(RUB)",
        "Наличные Стамбул USD": "Наличные(USD)",
        "Наличные-Тамбов RUB": "Наличные(RUB)",
        "Наличные Тбилиси USD": "Наличные(USD)",
        "Наличные-Тверь RUB": "Наличные(RUB)",
        "Наличные-Тула RUB": "Наличные(RUB)",
        "Наличные Тюмень RUB": "Наличные(RUB)",
        "Наличные Тюмень USD": "Наличные(USD)",
        "Наличные (Украина) USD": "Наличные(USD)",
        "Наличные Чанг": "Наличные(THB)",
        "Наличные Челябинск RUB": "Наличные(RUB)",
        "Наличные-Ярославль RUB": "Наличные(RUB)",
        "Открытие RUB": "Открытие(RUB)",
        "ОщадБанк UAH": "ОщадБанк(UAH)",
        "Приват24 UAH": "Приват24(UAH)",
        "Промсвязьбанк RUB": "Промсвязьбанк(RUB)",
        "Райфайзен RUB": "Райффайзен(RUB)",
        "Райффайзен UAH": "Райффайзен(UAH)",
        "Райффайзен банк RUB": "Райффайзен(RUB)",
        "РНКБ RUB": "РНКБ(RUB)",
        "Россельхоз банк RUB": "Россельхозбанк(RUB)",
        "Россельхозбанк RUB": "Россельхозбанк(RUB)",
        "Ростов-на-Дону RUB": "Наличные(RUB)",
        "РС (cash-in) RUB": "Русский Стандарт(RUB) ",
        "Русский Стандарт RUB": "Русский Стандарт(RUB)",
        "Сальдо BTC": "Bitcoin(BTC)",
        "Сальдо USDT": "Tether ERC20(USDT)",
        "Сбербанк KZT": "Сбербанк(KZT)",
        "СберБанк RUB": "Сбербанк(RUB)",
        "Ситибанк RUB": "Ситибанк(RUB)",
        "Совкомбанк RUB": "Совкомбанк(RUB)",
        "Тинькофф cash-in RUB": "Тинькофф cash-in(RUB)",
        "Тинькофф Mir Pay RUB": "Карта Мир(RUB)",
        "Тинькофф QR RUB": "Тинькофф QR(RUB)",
        "Тинькофф Банк RUB": "Тинькофф(RUB)",
        "ТКС (cash-in) RUB": "Тинькофф cash-in(RUB)",
        "ТКС cash-in RUB": "Тинькофф cash-in(RUB)",
        "Турецкая Лира TRY": "Visa/MasterCard(TRY)",
        "Укрсиббанк UAH": "Укрсиббанк(UAH)",
        "Уралсиб RUB": "Уралсиб(RUB)",
        "Хоум Кредит RUB": "Хоум Кредит(RUB)",
        "Хоум Кредит Банк RUB": "Хоум Кредит(RUB)",
        "Пумб UAH": "Пумб(UAH)",
        "Наличные Челябинск USD": "Наличные(USD)",
        "Наличные СПБ USD": "Наличные(USD)",
        "Наличные Sankt-Peterburg USD": "Наличные(USD)",
        "Tether TRC20 Sankt-Peterburg USDTTRC": "Наличные(USD)",
        "Tether TRC20 Stambul USDTTRC": "Наличные(USD)",
        "Tether OMNI USDT": "Tether OMNI(USDT)",
        "Банковский счёт EUR": "Банковский счёт(EUR)",
        "Банковский счёт USD": "Банковский счёт(USD)",
        "Наличные EUR": "Наличные(EUR)",
        "Bat BAT": "BAT(BAT)",
        "Bitcoin (BEP-20) BTC": "Bitcoin BEP20(BTCB)",
        "Bitcoin CashSV BSV": "Bitcoin SV(BSV)",
        "Dai (BEP-20) DAI": "DAI(DAI)",
        "Dai DAI USD": "DAI(DAI)",
        "Dai (ERC-20) DAI": "DAI(DAI)",
        "Dashcoin DASH": "Dashcoin(DASH)",
        "Ethereum (BEP-20) ETH": "Ethereum BEP20(ETH)",
        "IOTA MIOTA": "IOTA(MIOTA)",
        "MONERO XMR": "Monero(XMR)",
        "Tether Omni USDT": "Tether OMNI(USDT)",
        "VISA/MasterCard/Мир RUB": "Visa/MasterCard(RUB)",
        "Visa/MasterCard РФ RUB": "Visa/MasterCard(RUB)",
        "ZCash ZEC": "Zcash(ZEC)",
        "Альфабанк RUB": "Альфа-банк(RUB)",
        "ВТБ Банк RUB": "ВТБ(RUB)",
        "Карта МИР RUB": "Карта Мир(RUB)",
        "МоноБанк UAH": "Монобанк(UAH)",
        "Наличные TRY": "Наличные(TRY)",
        "Счет ИП или ООО RUB": "Наличные(RUB)",
        "Тинькофф банк RUB": "Тинькофф(RUB)",
        "ТКС QR-код RUB": "Тинькофф QR(RUB)",
        "USD Coin USDC": "USDCoin ERC20(USDC)",
        "TrueUSD TUSD": "TrueUSD ERC20(TUSD)",
        "Terra LUNA": "Terra(LUNA)",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",
        "": "",









        # Добавьте другие соответствия по мере необходимости
    }

    # Унификация данных для give_pair_name
    row_data["give_pair_name"] = give_pair_name_mapping_dict.get(row_data["give_pair_name"], row_data["give_pair_name"])

    # Унификация данных для receive_pair_name
    row_data["receive_pair_name"] = receive_pair_name_mapping_dict.get(row_data["receive_pair_name"], row_data["receive_pair_name"])

    return row_data


def extract_coolcoin_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_bitcoin24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        row_data["trading_pair"] = match.group(1).replace("-to-", "-")

        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_apexchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        row_data["trading_pair"] = match.group(1).replace("-to-", "-")

        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_cashadmin_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        row_data["trading_pair"] = match.group(1).replace("-to-", "-")

        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_grambit_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_finex24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        link = tarif_line['href'].rstrip('/')
        match = re.search(r'exchange-(.*?)$', link)

        if match:
            base_currency, quote_currency = match.group(1).split('-to-')
            trading_pair = f"{base_currency.upper()}-{quote_currency.upper()}"

            row_data = {
                "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
                "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
                "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
                "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
                "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
                "link": link,
                "exchange_id": 0,
                "trading_pair": trading_pair
            }

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_obama_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_pandpay_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_cryptomax_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_obmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_excoin_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_allmoney_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_robmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_cointok_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_realexchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_na_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_favoriteexchanger_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_realbit_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_na_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_altinbit_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_epichange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_exchangeyourmoney_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_sberbit_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_niceobmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_wmsell_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list

def extract_getexch_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_crystaltrade_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_100bitcoins_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_cryptobar_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_goldobmen_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_adb_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_natebit_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext1').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext1') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_globalbits_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_coinguru_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_atpayz_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_obmenlite24_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_expochange_data(soup):
    rows = soup.find_all('tr', class_='javahref')
    data_list = []

    for row in rows:
        row_data = {
            "give_count": "",
            "give_pair_name": "",
            "receive_count": "",
            "receive_pair_name": "",
            "reserve": "",
            "link": "",
            "trading_pair": "",
            "exchange_id": 0
        }
        if row.find_all('td'):
            row_data["give_count"] = row.find_all('td')[0].div.text.strip() if row.find_all('td')[0].div.text.strip() else row.find_all('td')[0].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[0].find_next('td', class_='tacursotd') else ""
            row_data["give_pair_name"] = row.find_all('td')[1].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[1].find('div', class_='obmenlinetext') else ""
            row_data["receive_count"] = row.find_all('td')[3].div.text.strip() if row.find_all('td')[3].div.text.strip() else row.find_all('td')[3].find_next('td', class_='tacursotd').div.text.strip() if row.find_all('td')[3].find_next('td', class_='tacursotd') else ""
            row_data["receive_pair_name"] = row.find_all('td')[4].find('div', class_='obmenlinetext').text.strip() if row.find_all('td')[4].find('div', class_='obmenlinetext') else ""
            row_data["reserve"] = row.find_all('td')[5].div.text.strip() if row.find_all('td')[5].div.text.strip() else ""
            link_element = row.get('name')
            if link_element:
                row_data["link"] = link_element
                match = re.search(r'xchange_(.*?)_to_(.*?)/', link_element)
                if match:
                    base_currency = match.group(1)
                    quote_currency = match.group(2)
                    trading_pair = f"{base_currency}-{quote_currency}"
                    row_data["trading_pair"] = trading_pair

            data_list.append(unify_data(row_data))  # Применяем унификацию данных
    return data_list


def extract_ejpmarket_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_to_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_24expay_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_moneymix_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_1654_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_swiftchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных



    return data_list



def extract_intercontinental_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_btchange_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list


def extract_bitobmenka_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange_(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("_na_", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list



def extract_bitbong_data(soup):
    tarif_lines = soup.find_all('a', class_='tarif_line')
    data_list = []

    for tarif_line in tarif_lines:
        row_data = {
            "give_count": tarif_line.find('div', class_='tarif_curs_ins').span.get_text(),
            "give_pair_name": tarif_line.find('div', class_='tarif_curs_title_ins').span.get_text(),
            "receive_pair_name": tarif_line.find_all('div', class_='tarif_curs_title_ins')[1].span.get_text(),
            "receive_count": tarif_line.find_all('div', class_='tarif_curs_ins')[1].span.get_text(),
            "reserve": tarif_line.find('div', class_='tarif_curs_reserv_ins').get_text().replace("Резерв: ", ""),
            "link": tarif_line['href'].rstrip('/'),
            "exchange_id": 0
        }

        match = re.search(r'exchange-(.*?)$', row_data["link"])
        trading_pair = match.group(1).replace("-to-", "-")
        row_data["trading_pair"] = trading_pair.upper()
        data_list.append(unify_data(row_data))  # Применяем унификацию данных

    return data_list

def split_count_and_coin_name(value):
    match = re.match(r'(\d+(\.\d+)?)\s*([^\d]*)', value)
    if match:
        count = match.group(1)
        coin_name = match.group(3)
        return count, coin_name
    else:
        return value, None

def scrape_and_save_data(url, exchange_name, data_extraction_callback):
    response = requests.get(url)
    if response.status_code == 200:
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        data_list = data_extraction_callback(soup)

        if data_list:
            with SessionLocal() as db:
                exchange = db.query(Exchanges).filter_by(exchange_name=exchange_name).first()
                exchange_id = exchange.id

                for row_data in data_list:
                    # Обработка "give_count" и "receive_count"
                    give_count, give_name_coin = split_count_and_coin_name(row_data["give_count"])
                    receive_count, receive_name_coin = split_count_and_coin_name(row_data["receive_count"])

                    # Применение значений после обработки
                    row_data["give_count"] = give_count
                    row_data["give_name_coin"] = give_name_coin
                    row_data["receive_count"] = receive_count
                    row_data["receive_name_coin"] = receive_name_coin

                    # Используем регулярное выражение для проверки "give_count" на наличие символов после 0
                    if row_data["give_count"] == '0':
                        continue  # Пропускаем запись, если "give_count" равно 0 и не имеет дополнительных символов

                    row_data["exchange_id"] = exchange_id
                    row_data["exchange_name"] = exchange_name
                    existing_record = db.query(CurrencyRate).filter_by(link=row_data["link"]).first()

                    if existing_record:
                        for key, value in row_data.items():
                            setattr(existing_record, key, value)
                    else:
                        new_record = CurrencyRate(**row_data)
                        db.add(new_record)

                db.commit()
                db.flush()

            print(f"Данные успешно сохранены в базе данных для {exchange_name}")
        else:
            print(f"Элементы не найдены на бирже {exchange_name}")
    else:
        print(f"Ошибка при запросе страницы {url}. Код статуса: {response.status_code}")



if __name__ == "__main__":
    # Определите URL и название бирж для каждой функции
    exchange_data_list = [
        ("https://coolcoin.best/tarifs/", "coolcoin", extract_coolcoin_data),
        ("https://bitcoin24.su/tarifs/", "bitcoin24", extract_bitcoin24_data),
        ("https://apexchange.cc/tarifs/", "apexchange", extract_apexchange_data),
        ("https://cashadmin.ru/tarifs/", "cashadmin", extract_cashadmin_data),
        ("https://grambit.biz/tarifyi/", "grambit", extract_grambit_data),
        ("https://finex24.io/tarifs/", "finex24", extract_finex24_data),
        ("https://obama.ru/tarifs/", "obama", extract_obama_data),
        ("https://pandpay.net/tarifs/", "pandpay", extract_pandpay_data),
        ("https://cryptomax.ru/tarifs/", "cryptomax", extract_cryptomax_data),
        ("https://ob-men.com/tarifs/", "ob-men", extract_obmen_data),
        ("https://excoin.in/tarifs/", "excoin", extract_excoin_data),
        ("https://allmoney.market/tarifs/", "allmoney", extract_allmoney_data),
        ("https://r-obmen.ru/tarifs/", "r-obmen", extract_robmen_data),
        ("https://cointok.net/tarifs/", "cointok", extract_cointok_data),
        ("https://real-exchange.ru/tarifs/", "real-exchange", extract_realexchange_data),
        ("https://favorite-exchanger.net/tarifs/", "favorite-exchanger", extract_favoriteexchanger_data),
        ("https://real-bit.net/tarifs/", "real-bit", extract_realbit_data),
        ("https://altinbit.com/tarifs/", "altinbit", extract_altinbit_data),
        ("https://epichange.online/tarifs/", "epichange", extract_epichange_data),
        ("https://exchangeyourmoney.com/tarifs/", "exchangeyourmoney", extract_exchangeyourmoney_data),
        ("https://sberbit.vip/tarifs/", "sberbit", extract_sberbit_data),
        ("https://niceobmen.com/tarifs/", "niceobmen", extract_niceobmen_data),
        ("https://wmsell.biz/tarifs/", "wmsell", extract_wmsell_data),
        ("https://getexch.com/tarifs/", "getexch", extract_getexch_data),
        ("https://crystal-trade.org/tarifs/", "crystal-trade", extract_crystaltrade_data),
        ("https://100bitcoins.com/tarifs/", "100bitcoins", extract_100bitcoins_data),
        ##("https://sellver.com/tariffs", "sellver", extract_sellver_data), адаптировать поиск
        ("https://cryptobar.men/tarifs/", "cryptobar", extract_cryptobar_data),
        ("https://goldobmen.com/tarifs/", "goldobmen", extract_goldobmen_data),
        ("https://adb.bz/tarifs/", "adb", extract_adb_data),
        ("https://globalbits.org/tarifs/", "globalbits", extract_globalbits_data),
        ("https://natebit.pro/tarifs/", "natebit", extract_natebit_data),
        ("https://coinguru.pw/tarifs", "coinguru", extract_coinguru_data),
        ("https://atpayz.com/tarifs/", "atpayz", extract_atpayz_data),
        ("https://obmenlite24.ru/tarifs/", "obmenlite24", extract_obmenlite24_data),
        ("https://expochange.org/tarifs/", "expochange", extract_expochange_data),
        ("https://jpmarket.cc/tarifs/", "jpmarket", extract_ejpmarket_data),
        ("https://24expay.com/tarifs/", "24expay", extract_24expay_data),
        ("https://intercontinental.trade/tarifs/", "intercontinental", extract_intercontinental_data),
        ("https://moneymix.org/tarifs/", "moneymix", extract_moneymix_data),
        ("https://1654.exchange/tarifs/", "1654", extract_1654_data),
        ("https://swiftchange.net/tarifs/", "swiftchange", extract_swiftchange_data),
        ("https://btchange.ru/tarifs/", "btchange", extract_btchange_data),
        ("https://bit-obmenka.vip/tarifs/", "bit-obmenka", extract_bitobmenka_data),
        #https://obmenoff.cc/tariffs krutit nado
        ("https://bitbong.pro/tarifs/", "bitbong", extract_bitbong_data),

        # Добавьте остальные биржи и функции здесь
    ]

    processes = []

    for exchange_url, exchange_name, data_extraction_callback in exchange_data_list:
        process = Process(target=scrape_and_save_data, args=(exchange_url, exchange_name, data_extraction_callback))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

