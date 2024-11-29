def main(file:str) -> int:
    """
    1. Data is from https://itprice.com/cisco-gpl/meraki%20switch.
    2. I highlighted all the products from their "#No" to "Our Price" columns, and put the copied text into to a `.txt` file.
    3. The output is the average of the sum of all rows under "List Price" ($8250).
    """
    listings = get_item_listings(file=file)
    prices= get_prices_from_listings(listings=listings)
    prices = clean_the_data(prices)
    return sum(prices)//len(prices)

def get_item_listings(file:str)->list[str]:
    """
    1. With how the data is copied onto the text file, the first 2 columns are in a line of their own. This function removes those entries.
    2. Sample: 
        1 		
        MS220-8-HW
	        Meraki MS220-8 Cloud Managed 8 Port GigE Switch. 	$985.00 	$519.00 (47% OFF) 	
        2 	
        MS220-8P-HW
	        Meraki MS220-8P L2 Cloud Managed 8 Port GigE 124W PoE Switch. 	$1,255.00 	$674.00 (46% OFF) 	
        3 	
    3. The output becomes:
	        [[Meraki, MS220-8, Cloud, Managed, 8, Port, GigE, Switch., $985.00, $519.00 (47% OFF)],[Meraki, MS220-8P, L2, Cloud, Managed, 8, Port, GigE, 124W, PoE, Switch., $1,255.00, $674.00 (46% OFF)]]

            1. This is akin to splitting a data that already looks like this:                   
                Meraki MS220-8 Cloud Managed 8 Port GigE Switch. 	$985.00 	$519.00 (47% OFF) 	
                Meraki MS220-8P L2 Cloud Managed 8 Port GigE 124W PoE Switch. 	$1,255.00 	$674.00 (46% OFF) 
        """
    listings = []
    with open(file,"r") as my_file:
        listings+= [line.split() for line in my_file if len(line.split())>1]
    return listings

def get_prices_from_listings(listings:list)->list[str]:
    """
    1. The prices are stored either as the second-to-the-last element or the last element. 
    2. The only way to differentiate the listing price from the website's price is the fact that the listing price is the first element with a `$` within the list.  
        1. Subsequent prices after the listing price are the website's price, which we don't need.
    """
    prices= []
    for product in listings[:]:
        price_obtained = False
        for spec in product:
            if "$" in spec and not price_obtained:
                prices.append(spec)
                price_obtained=True
    return prices

def clean_the_data(prices:list[str])->list[float]:
    """
    1. The format of the price data looks like "$1,000.00". We remove the $ and the comma from the string to make the data type a float number.
        1. The data type is float because of the decimal point and converting "100.00" to float is cleaner to read than converting it from str to float to int.
    """
    return [float(price.strip("$").replace(",","")) for price in prices]

if __name__=="__main__":
    FILE=r'{}'.format(input("Enter the directory of the file including the file itself:\n"))# input("Enter the directory of the file including the file itself:\n")
    out=main(file=FILE)
    print(out)