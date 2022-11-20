from pandas import pandas as pd
from dtale import show
from election_25 import exp_creation,convert_election_df_to_perentage_df
from election_25 import kalpi_places,add_addresses_to_df, bibi_no_bibi
pd.options.display.float_format = '{:.2f}'.format
expb_url = 'expb.csv'
expc_url = 'expc.csv'
kalpi_places_url = 'kalpiplaces.csv'


if __name__ == '__main__':
    kalpi_places_df = kalpi_places(kalpi_places_url)

    tmp = pd.read_csv(expc_url,
                        dtype = {'קלפי': str},
    )
    tmp = tmp[tmp["שם ישוב"].str.contains('מעטפות חיצוניות') == False]
    tmp.drop(
        ['סמל ועדה','סמל ישוב',],
        inplace=True,axis=1,
    )
    expc_df = exp_creation(tmp)
    expc_percentage_df = convert_election_df_to_perentage_df(expc_df)

    tmp = pd.read_csv(expb_url,
                      dtype={'קלפי': str},
                      )
    tmp = tmp[tmp["שם ישוב"].str.contains('מעטפות חיצוניות') == False]
    tmp.drop(
         ['סמל ועדה', 'ברזל', 'ריכוז', 'שופט'],
        inplace=True, axis=1,
    )
    expb_df = exp_creation(tmp)




    tmp = add_addresses_to_df(expb_df,kalpi_places_df)
    expb_df = tmp
    expb_percentage_df = convert_election_df_to_perentage_df(expb_df)


    expc_bibi_no_bibi_df = bibi_no_bibi(expc_df)
    expb_bibi_no_bibi_df = bibi_no_bibi(expb_df)

    expb_pivot_df = pd.pivot_table(expb_df, index = ['city','address'],
                                   values =['voters','good_voters'],
                                   aggfunc = ['sum'],
                                    margins =True,
                                    margins_name = 'Total'
                                   )
    expb_pivot_df.reset_index(level=['city','address'], inplace=True)
    expb_pivot_df



