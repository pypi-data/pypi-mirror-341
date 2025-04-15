"""
Example usage of the Enemera API client to get price data.
"""

from enemera import EnemeraClient
from datetime import datetime, timedelta
import argparse
import sys


def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Fetch energy prices from Enemera API")
    parser.add_argument("--api-key", required=True, help="Your Enemera API key")
    parser.add_argument("--market", default="MGP", help="Market identifier (e.g., MGP, MI1)")
    parser.add_argument("--days", type=int, default=7, help="Number of days to fetch (default: 7)")
    parser.add_argument("--area", default="NORD,SUD", help="Comma-separated list of areas")
    args = parser.parse_args()

    # Initialize the client
    client = EnemeraClient(api_key=args.api_key)

    # Calculate date range
    to_date = datetime.now()
    from_date = to_date - timedelta(days=args.days)

    # Format dates for the API request
    date_to = to_date.strftime("%Y-%m-%d")
    date_from = from_date.strftime("%Y-%m-%d")

    print(f"Fetching {args.market} prices from {date_from} to {date_to} for areas: {args.area}")

    try:
        # Get prices
        prices = client.prices.get(
            market=args.market,
            date_from=date_from,
            date_to=date_to,
            area=args.area
        )

        print(f"Retrieved {len(prices)} price records")

        # Print the first 5 prices
        print("\nSample of price data:")
        for price in prices[:5]:
            print(f"Time: {price.utc}, Market: {price.market}, Zone: {price.zone}, Price: {price.price} EUR/MWh")

        # Calculate average price per zone
        zones = set(price.zone for price in prices)
        print("\nAverage prices by zone:")
        for zone in zones:
            zone_prices = [price.price for price in prices if price.zone == zone]
            avg_price = sum(zone_prices) / len(zone_prices) if zone_prices else 0
            print(f"Average price in {zone}: {avg_price:.2f} EUR/MWh")

    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()