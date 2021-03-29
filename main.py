import json
import requests
from time import sleep
from typing import Tuple, List

apiUrl = 'https://bitbay.net/API/Public/'


def loadDataFromApi(url: str):
    try:
        response = requests.get(url)
        return json.loads(response.text)
    except requests.exceptions.ConnectionError:
        print("Error occured while connecting to the API.")
        return None


def displayOffer(marketSymbol: Tuple[str, str], offer):
    print(f'Price (' + '{:.3f}'.format(offer[1]) + f' {marketSymbol[0]}):', '{:.3f}'.format(offer[1] * offer[0]) + f' {marketSymbol[1]}')
    print(f'Price (1 {marketSymbol[0]}):', f'{offer[0]} {marketSymbol[1]} \n')


def displayOffers(marketSymbol: Tuple[str, str], offers):
    for offer in offers:
        displayOffer(marketSymbol, offer)


def getOffer(marketSymbol: Tuple[str, str], numberOfOffers: int):
    if numberOfOffers <= 0:
        raise Exception("Number of offers should be positive")

    tradeOffers = loadDataFromApi(f'{apiUrl}/{marketSymbol[0]}{marketSymbol[1]}/orderbook.json')

    if tradeOffers:
        bids = tradeOffers["bids"][:numberOfOffers]
        asks = tradeOffers["asks"][:numberOfOffers]
        return [bids, asks]
    else:
        raise Exception(f'Unable to load a market for {marketSymbol[0]}-{marketSymbol[1]}.')


def presentOffers(marketSymbol: Tuple[str, str], numberOfOffers: int):
    offers = getOffer(marketSymbol, numberOfOffers)
    if len(offers) <= 0: raise Exception("No offers to display.")

    buyOffers = offers[1]  # ask
    sellOffers = offers[0] # bid

    print(f'BUY/SELL offers for {marketSymbol[0]}-{marketSymbol[1]}')

    print('\nBUY Offers')
    displayOffers(marketSymbol, buyOffers)

    print('\nSELL Offers')
    displayOffers(marketSymbol, sellOffers)

    return buyOffers, sellOffers


def calculateDifference(marketSymbols: List[Tuple[str, str]], numberOfOffers: int, refreshDelay: int = 20):
    while True:
        print()

        for marketSymbol in marketSymbols:
            offers = getOffer(marketSymbol, numberOfOffers)
            if offers:
                buyOffers, sellOffers = presentOffers(marketSymbol, numberOfOffers)

                buyOffersLength = len(buyOffers)
                sellOffersLength = len(sellOffers)

                numberOfComparisions = sellOffersLength if buyOffersLength >= sellOffersLength else buyOffersLength

                for index in range(numberOfComparisions):
                    buyOfferPrice = buyOffers[index][0]
                    sellOfferPrice = sellOffers[index][0]

                    differenceRatio = (1 - (sellOfferPrice - buyOfferPrice) / buyOfferPrice)
                    print(f'Profit ratio for {marketSymbol}: ' + '{:.3f}'.format(differenceRatio), sep="")
        sleep(refreshDelay)


def showOffers(marketSymbols: List[Tuple[str, str]], numberOfOffers: int):
    for item in marketSymbols:
        presentOffers(item, numberOfOffers)


def main():
    marketSymbols: List[Tuple[str, str]] = [
        ('BTC', 'USD'),
        ('LTC', 'USD'),
        ('DASH', 'USD')
    ]

    # showOffers(marketSymbols, 20)
    calculateDifference(marketSymbols, 15, 20)


if __name__ == "__main__":
    main()

