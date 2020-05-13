# ===== Import Modules =====

import argparse
import requests
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# ===== /Import Modules/ =====

# ===== Define Functions =====


def doXticks( x ):
    myList = [ '' for i in range(len(x)) ]
    for i in np.arange(len(x)-1,0,-1):
        if i % 5 == 0:
            myList[i] = x[i]
    return myList

def makePlots( df, isoCode ):
    df = df[df.iso_code == isoCode]
    df = df[df.date > '2020-02-20']
    df['rollingNew']   = df.iloc[:,4].rolling(window=7).mean()
    df['rollingDeath'] = df.iloc[:,6].rolling(window=7).mean()

    xticks = doXticks(list(df.date))

    fig = plt.figure( constrained_layout=True, figsize=(20,10))

    ax = fig.add_subplot()
    ax.bar( df.date, df.new_cases, alpha=0.3, label="Daily cases bar" )
    ax.plot( df.date, df.rollingNew, c="C1", lw=4, label="Daily cases 7-day rolling average" )
    ax.tick_params(axis='y', labelcolor="C0")
    ax.set_ylabel('Daily Cases', color="C0")

    ax2 = ax.twinx()
    ax2.plot( df.date, df.total_cases, c="C2", lw=4, label="Cumulative cases log scale" )
    #ax2.set_ylim(0)
    ax2.tick_params(axis='y', labelcolor="C2")
    ax2.set_ylabel('Cumulative Cases', color="C2")
    ax2.set_yscale('log')

    plt.title("{} Daily New Cases".format(isoCode))
    plt.xticks(xticks)
    ax.legend(loc='upper left', bbox_to_anchor=(0,1),frameon=False)
    ax2.legend(loc='upper left', bbox_to_anchor=(0,0.955),frameon=False)
    plt.savefig("plots/daily_cases_{}.png".format(isoCode))
#    print("Figure saved as daily_cases_{}.png".format(isoCode))


    fig = plt.figure( constrained_layout=True, figsize=(20,10))
    
    ax = fig.add_subplot()
    ax.bar( df.date, df.new_deaths, alpha=0.3, label="Daily deaths bar" )
    ax.plot( df.date, df.rollingDeath, c="C1", lw=4, label="Daily deaths 7-day rolling average" )
    ax.tick_params(axis='y', labelcolor="C0")
    ax.set_ylabel('Daily Deaths', color="C0")

    ax2 = ax.twinx()
    ax2.plot( df.date, df.total_deaths, c="C2", lw=4, label="Cumulative deaths log scale" )
    #ax2.set_ylim(0)
    ax2.tick_params(axis='y', labelcolor="C2")
    ax2.set_ylabel('Cumulative Deaths', color="C2")
    ax2.set_yscale('log')

    plt.title("{} Daily New Deaths".format(isoCode))
    plt.xticks(xticks)
    ax.legend(loc='upper left', bbox_to_anchor=(0,1),frameon=False)
    ax2.legend(loc='upper left', bbox_to_anchor=(0,0.955),frameon=False)
    plt.savefig("plots/daily_deaths_{}.png".format(isoCode))
#    print("Figure saved as daily_deaths_{}.png".format(isoCode))

# ===== /Define Functions/ =====

# ===== Main Program =====

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument( "-c", "--country", required=True, help="Country")

    args = parser.parse_args()
    country = str(args.country)
    print(country)
    
    r = requests.get('https://covid.ourworldindata.org/data/owid-covid-data.csv', allow_redirects=True)
    open('data/owid_covid_data.csv', 'wb').write(r.content)
    df = pd.read_csv("data/owid_covid_data.csv")

    countryList = list(df.location.unique())
    isoList     = list(df.iso_code.unique())
    if country in countryList:

        isoCode = 0
        for i in range(len(countryList)):
            if country == countryList[i]:
                isoCode = i
        isoCode = isoList[isoCode]
        makePlots( df, isoCode )

    elif country in isoList:

        makePlots( df, country )

    else:
        print( "County (or ISO code) could not be found.")
        print( "These are the available countries:")
        countryList, isoList = zip(*sorted(zip(countryList, isoList)))
        for i in range(len(countryList)):
            print( "Name: '{}' | ISO Code: '{}'".format(countryList[i],isoList[i]) ) 


# ===== /Main Program/ =====
