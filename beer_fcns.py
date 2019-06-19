def make_beer_df():
    import pandas as pd
    cols = ['brewery_name', 'beer_name','beer_style','beer_beerid', 'beer_abv','review_overall',
            'review_taste','review_aroma', 'review_appearance', 'review_palate', ]
    #change path below
    df = pd.read_csv('beer_reviews.tar.gz',usecols=cols)
    df = df[['brewery_name', 'beer_name','beer_style','beer_beerid', 'beer_abv','review_overall',
             'review_taste','review_aroma', 'review_appearance', 'review_palate']]
    df.columns = ['brewery', 'beer','style','beer_id', 'abv','overall',
             'taste','aroma', 'appearance', 'palate']
    return df

def get_rid(df,cutoff=10):
    '''Get rid of beers with fewer than cutoff amount of reviews'''
    vc = df['beer_id'].value_counts().to_frame(name='count')
    beers_to_keep = list(vc[vc['count']>=cutoff].index)
    new = df[df.beer_id.isin(beers_to_keep)]
    return new

def rank(df,rank_var='overall'):
    ''' Rank the remaining beers by their mean overall rating '''
    rank = df.groupby(['brewery','beer','style','abv']).agg({'beer_id':'count',
                       'overall':'mean','taste':'mean','aroma':'mean',
                       'palate':'mean', 'appearance':'mean'}).sort_values(rank_var,ascending=False)
    rank = rank.rename(columns={'beer_id':'count'})
    return rank

def findrank(df,**kwargs):
    for item in kwargs.keys():
        df = df[df[item].str.contains(kwargs[item])].sort_values('overall',ascending=False)
    return df

def main():
    df = make_beer_df()
    new = get_rid(df,cutoff=35)
    rk = rank(df = new, rank_var='overall').reset_index()
    return rk