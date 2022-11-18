from pandas import pandas as pd
from pandasgui import show

pd.options.display.float_format = "{:.2f}".format
expb_url = "expb.csv"
expc_url = "expc.csv"
kalpi_places_url = "kalpiplaces.csv"

all_parties = [
    "אמת",
    "אצ",
    "ב",
    "ג",
    "ד",
    "ום",
    "ז",
    "זך",
    "זנ",
    "זץ",
    "ט",
    "י",
    "יז",
    "ינ",
    "יץ",
    "יק",
    "כן",
    "ך",
    "ל",
    "מחל",
    "מרצ",
    "נז",
    "ני",
    "נף",
    "נץ",
    "נק",
    "נר",
    "עם",
    "פה",
    "ף",
    "צ",
    "ץ",
    "ק",
    "קי",
    "קך",
    "קנ",
    "קץ",
    "רז",
    "שס",
    "ת",
]

real_parties = [
    "מחל",
    "פה",
    "ט",
    "כן",
    "שס",
    "ג",
    "ל",
    "עם",
    "ום",
    "אמת",
    "מרצ",
    "ד",
    "ב",
    "אצ",
    "קץ",
    "יז",
    "ץ",
]

bibi = [
    "מחל",
    "ט",
    "שס",
    "ג",
    "ב",
]

no_bibi = [
    "פה",
    "כן",
    "ל",
    "עם",
    "אמת",
    "מרצ",
]


def convert_series_to_float(series: pd.Series) -> pd.Series:
    """
    Convert pandas series to float

    :param series:
    :return: new series
    """
    tmp = series
    new_series = pd.to_numeric(tmp)
    return new_series


def create_basic_election_df(df: pd.DataFrame) -> pd.DataFrame:
    new_df = pd.DataFrame()
    new_df["city"] = df["שם ישוב"].astype(pd.StringDtype()).values

    if "סמל ישוב" in df.columns:
        new_df["city_symb"] = df["סמל ישוב"].astype(pd.StringDtype()).values
        new_df["city_symb"] = new_df["city_symb"].apply(
            lambda x: "0" + x if len(x) == 3 else x
        )
        new_df["city_symb"] = new_df["city_symb"].apply(
            lambda x: "00" + x if len(x) == 2 else x
        )
        new_df["city_symb"] = new_df["city_symb"].apply(
            lambda x: "000" + x if len(x) == 1 else x
        )
    if "קלפי" in df.columns:
        new_df["kalpi_symb"] = df["קלפי"].astype(pd.StringDtype()).values
        new_df["kalpi_symb"] = new_df["kalpi_symb"].astype("float")
        new_df["kalpi_symb"] = new_df["kalpi_symb"].astype("string")

    new_df["total_voters"] = df["בזב"].values
    new_df["voters"] = df["מצביעים"].values
    new_df["good_voters"] = df["כשרים"].values
    return new_df.copy()


def convert_election_df_to_perentage_df(df: pd.DataFrame) -> pd.DataFrame:
    perce_df = df.copy()
    perce_df["good_voters"] = perce_df["good_voters"] / perce_df["voters"] * 100

    for symbol in real_parties:
        perce_df[symbol] = perce_df[symbol] / perce_df["voters"] * 100

    for symbol in all_parties:
        if symbol in real_parties:
            continue
        perce_df[symbol] = perce_df[symbol] / perce_df["voters"] * 100
    return perce_df.copy()


def exp_creation(df):
    exp_df = create_basic_election_df(df)
    for symbol in real_parties:
        exp_df[symbol] = df[symbol].values
    for symbol in all_parties:
        if symbol in real_parties:
            continue
        exp_df[symbol] = df[symbol].values
    return exp_df.copy()


def bibi_no_bibi(df):
    new_df = pd.DataFrame()
    new_df["city"] = df["city"].values
    new_df["good_voters"] = df["good_voters"].values
    if "סמל ישוב" in df.columns:
        new_df["city_symb"] = df["סמל ישוב"].astype(pd.StringDtype()).values
        new_df["city_symb"] = new_df["city_symb"].apply(
            lambda x: "0" + x if len(x) == 3 else x
        )
        new_df["city_symb"] = new_df["city_symb"].apply(
            lambda x: "00" + x if len(x) == 2 else x
        )
        new_df["city_symb"] = new_df["city_symb"].apply(
            lambda x: "000" + x if len(x) == 1 else x
        )
    if "קלפי" in df.columns:
        new_df["kalpi_symb"] = df["קלפי"].astype(pd.StringDtype()).values
        new_df["kalpi_symb"] = new_df["kalpi_symb"].astype("float")
        new_df["kalpi_symb"] = new_df["kalpi_symb"].astype("string")
    
    tmp = pd.DataFrame()
    for symbol in bibi:
        tmp[symbol] = df[symbol].copy()
    tmp["Total"] = tmp.sum(axis=1)
    new_df["bibi"] = tmp["Total"].copy()
    tmp = pd.DataFrame()
    for symbol in no_bibi:
        tmp[symbol] = df[symbol].copy()
    tmp["Total"] = tmp.sum(axis=1)
    new_df["no_bibi"] = tmp["Total"].copy()
    new_df["bibi_percent"] = new_df["bibi"] / new_df["good_voters"] * 100
    new_df["no_bibi_percent"] = new_df["no_bibi"] / new_df["good_voters"] * 100
    return new_df.copy()


def kalpi_places(url: str) -> pd.DataFrame:
    df = pd.read_csv(
        url,
        sep="|",
        dtype={
            "סמל ישוב בחירות": str,
            "סמל קלפי": str,
            "כתובת קלפי": str,
            "מקום קלפי": str,
        },
    )
    df.drop(
        [
            "סמל ועדה",
            "שם ועדה",
            "סמל רכוז",
        ],
        inplace=True,
        axis=1,
    )
    df = df.astype("string")
    new_df = pd.DataFrame()
    new_df["city"] = df["שם ישוב בחירות"].astype(pd.StringDtype()).values
    new_df["city_symb"] = df["סמל ישוב בחירות"].astype(pd.StringDtype()).values
    new_df["kalpi_symb"] = df["סמל קלפי"].values
    new_df["adress"] = df["כתובת קלפי"].values
    new_df["placement"] = df["מקום קלפי"].values
    return new_df


def add_addresses_to_df(elec_df: pd.DataFrame, kalpi_df: pd.DataFrame) -> pd.DataFrame:
    new_df = elec_df.copy()
    places = list()
    addresses = list()
    for index, row in new_df.iterrows():
        city = row["city"]
        city_symb = row["city_symb"]
        kalpi_symb = row["kalpi_symb"]
        kalpi_row = kalpi_df[
            (kalpi_df["kalpi_symb"] == kalpi_symb)
            & (kalpi_df["city_symb"] == city_symb)
        ]
        address = kalpi_row["adress"].values[0]
        place = kalpi_row["placement"].values[0]
        addresses.append(address)
        places.append(place)
    column_idx = new_df.columns.get_loc("total_voters") -1
    new_df.insert(3, 'address', addresses)
    new_df.insert(4, 'place', places)
    return new_df
