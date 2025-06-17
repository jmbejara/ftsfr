"""
Downloads treasury auction data from TreasuryDirect.gov
See here: https://treasurydirect.gov/TA_WS/securities/jqsearch

Key Auction Terminology:
- Tendered: The amount bid or submitted in an auction. This is what bidders want to buy.
- Accepted: The amount actually awarded or allocated to bidders. This is what they actually get.
- The difference occurs because auctions can be oversubscribed (more bids than securities available).

What is SOMA?
SOMA (System Open Market Account) is the Federal Reserve's portfolio of securities used to 
implement monetary policy. When the Fed participates in Treasury auctions:
- It typically bids non-competitively (accepts whatever rate/yield is determined)
- Purchases inject money into the banking system (expansionary policy)
- Sales or non-replacement of maturing securities drain money (contractionary policy)
- SOMA data helps researchers track Fed monetary policy implementation and its market impact

Data Dictionary:

Core Identifiers:
- cusip: Unique 9-character identifier for each security (Committee on Uniform Securities Identification Procedures)
- announcedCusip: CUSIP announced at time of auction announcement (may differ from final CUSIP)
- originalCusip: CUSIP from original issue (for reopened securities)
- corpusCusip: CUSIP for the principal portion of a stripped security

Security Information:
- securityType: Type of marketable security (Bill, Note, Bond, TIPS, FRN)
- securityTerm: Term of the security (e.g., "4-Week", "2-Year", "30-Year")
- securityTermDayMonth: Security term expressed in days/months format
- securityTermWeekYear: Security term expressed in weeks/years format
- series: Series designation for notes (letter + year of maturity)
- type: Additional security type classification
- term: Alternative term designation
- originalSecurityTerm: Original term for reopened securities

Key Dates:
- issueDate: Date security is delivered to buyer's account
- maturityDate: Date security stops earning interest and principal is repaid
- announcementDate: Date auction is announced to public
- auctionDate: Date auction is conducted
- auctionDateYear: Year of the auction
- datedDate: Date interest begins accruing (usually same as issue date)
- maturingDate: Date of maturing securities being replaced
- firstInterestPaymentDate: Date of first interest payment (for notes/bonds)
- originalIssueDate: First issue date for reopened securities
- originalDatedDate: Original dated date for reopened securities
- callDate: Date bond can be called (pre-1985 bonds)
- calledDate: Date bond was actually called
- backDatedDate: Date for backdated securities

Interest/Rate Information:
- interestRate: Annual interest rate (percentage) for notes/bonds/TIPS
- refCpiOnIssueDate: Reference CPI on issue date (TIPS only)
- refCpiOnDatedDate: Reference CPI on dated date (TIPS only)
- indexRatioOnIssueDate: Index ratio on issue date (TIPS only)
- interestPaymentFrequency: Frequency of interest payments
- firstInterestPeriod: Length of first interest period
- standardInterestPaymentPer1000: Standard interest payment per $1,000 face value
- spread: Fixed spread over index rate (FRNs only)
- frnIndexDeterminationDate: Date index rate determined (FRNs)
- frnIndexDeterminationRate: Index rate used (FRNs)

Accrued Interest:
- accruedInterestPer1000: Accrued interest per $1,000 (unadjusted)
- accruedInterestPer100: Accrued interest per $100 (unadjusted)
- adjustedAccruedInterestPer1000: Inflation-adjusted accrued interest (TIPS)
- unadjustedAccruedInterestPer1000: Unadjusted accrued interest (TIPS)

Auction Results - Rates/Yields:
- averageMedianDiscountRate: Median discount rate (bills) or average in multiple-price auction
- averageMedianInvestmentRate: Median investment rate (bills)
- averageMedianPrice: Median price accepted
- averageMedianDiscountMargin: Median discount margin (FRNs)
- averageMedianYield: Median yield (notes/bonds/TIPS)
- highDiscountRate: Highest discount rate accepted (bills)
- highInvestmentRate: Highest investment rate accepted (bills)
- highPrice: Highest price accepted
- highDiscountMargin: Highest discount margin accepted (FRNs)
- highYield: Highest yield accepted (notes/bonds/TIPS)
- lowDiscountRate: Lowest discount rate accepted (bills)
- lowInvestmentRate: Lowest investment rate accepted (bills)
- lowPrice: Lowest price accepted
- lowDiscountMargin: Lowest discount margin accepted (FRNs)
- lowYield: Lowest yield accepted (notes/bonds/TIPS)

Pricing:
- adjustedPrice: Inflation-adjusted price (TIPS)
- unadjustedPrice: Price before inflation adjustment (TIPS)
- pricePer100: Price per $100 face value

Auction Statistics:
- totalAccepted: Total dollar amount actually sold in the auction
- totalTendered: Total dollar amount of all bids received (demand)
- bidToCoverRatio: Ratio showing auction demand (totalTendered/totalAccepted)
- allocationPercentage: Percentage allocated at high rate/yield when oversubscribed
- allocationPercentageDecimals: Number of decimal places in allocation percentage

Bidder Categories:
- competitiveAccepted: Dollar amount awarded to competitive bidders (who specify rate/yield)
- competitiveTendered: Dollar amount competitive bidders tried to buy
- competitiveTendersAccepted: Number of competitive bids that were successful
- competitiveBidDecimals: Decimal places allowed in competitive bids
- noncompetitiveAccepted: Dollar amount awarded to noncompetitive bidders (who accept any rate)
- noncompetitiveTendersAccepted: Number of noncompetitive bids that were successful
- primaryDealerAccepted: Amount awarded to primary dealers (large banks/brokers)
- primaryDealerTendered: Amount primary dealers bid for
- directBidderAccepted: Amount awarded to direct bidders (bid directly with Treasury)
- directBidderTendered: Amount direct bidders bid for
- indirectBidderAccepted: Amount awarded to indirect bidders (bid through intermediaries)
- indirectBidderTendered: Amount indirect bidders bid for
- treasuryRetailAccepted: Amount awarded to individual investors via TreasuryDirect
- treasuryRetailTendersAccepted: Number of successful TreasuryDirect bids

Federal Reserve & Foreign:
- somaAccepted: Dollar amount the Fed was awarded in this auction
- somaTendered: Dollar amount the Fed bid for in this auction
- somaIncluded: Boolean indicating if the Fed participated in this auction
- somaHoldings: Fed's current holdings of this specific security
- fimaIncluded: Whether foreign/international accounts included
- fimaNoncompetitiveAccepted: Foreign/international noncompetitive accepted
- fimaNoncompetitiveTendered: Foreign/international noncompetitive tendered

Auction Parameters:
- offeringAmount: Total amount offered in auction
- minimumBidAmount: Minimum bid amount allowed
- maximumCompetitiveAward: Maximum competitive award to single bidder
- maximumNoncompetitiveAward: Maximum noncompetitive award
- maximumSingleBid: Maximum single bid amount
- multiplesToBid: Required bid increment
- multiplesToIssue: Required issue increment
- minimumToIssue: Minimum amount that will be issued
- minimumStripAmount: Minimum amount for stripping
- currentlyOutstanding: Amount currently outstanding
- estimatedAmountOfPubliclyHeldMaturingSecuritiesByType: Estimate of maturing securities

Auction Timing:
- closingTimeCompetitive: Closing time for competitive bids
- closingTimeNoncompetitive: Closing time for noncompetitive bids
- auctionFormat: Format of auction (single-price, multiple-price)

Special Features:
- reopening: Boolean indicating if this is a reopening
- cashManagementBillCMB: Boolean for cash management bills
- floatingRate: Boolean for floating rate notes
- tips: Boolean for Treasury Inflation-Protected Securities
- callable: Boolean if bond is callable
- backDated: Boolean if security is backdated
- strippable: Boolean if security can be stripped

TIPS-Specific:
- cpiBaseReferencePeriod: Base reference period for CPI
- tiinConversionFactorPer1000: TIIN conversion factor per $1,000

Position Reporting:
- nlpExclusionAmount: Net long position exclusion amount
- nlpReportingThreshold: Net long position reporting threshold

Documentation:
- pdfFilenameAnnouncement: PDF file for auction announcement
- pdfFilenameCompetitiveResults: PDF file for competitive results
- pdfFilenameNoncompetitiveResults: PDF file for noncompetitive results
- pdfFilenameSpecialAnnouncement: PDF file for special announcements
- xmlFilenameAnnouncement: XML file for auction announcement
- xmlFilenameCompetitiveResults: XML file for competitive results
- xmlFilenameSpecialAnnouncement: XML file for special announcements

STRIPS Components:
- tintCusip1: CUSIP for first interest component
- tintCusip2: CUSIP for second interest component
- tintCusip1DueDate: Due date for first interest component
- tintCusip2DueDate: Due date for second interest component

Metadata:
- updatedTimestamp: Timestamp of last update
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

import json
import urllib.request
from pathlib import Path

import pandas as pd

from settings import config

DATA_DIR = Path(config("DATA_DIR"))


def pull_treasury_auction_data():
    url = "https://treasurydirect.gov/TA_WS/securities/jqsearch?format=jsonp"

    with urllib.request.urlopen(url) as wpg:
        x = wpg.read()
        data = json.loads(x.replace(b");", b"").replace(b"callback (", b""))

    df = pd.DataFrame(data["securityList"])

    # Date columns
    date_cols = [
        "issueDate",
        "maturityDate",
        "announcementDate",
        "auctionDate",
        "datedDate",
        "backDatedDate",
        "callDate",
        "calledDate",
        "firstInterestPaymentDate",
        "maturingDate",
        "originalDatedDate",
        "originalIssueDate",
        "tintCusip1DueDate",
        "tintCusip2DueDate",
    ]
    df[date_cols] = df[date_cols].apply(pd.to_datetime, errors="coerce")

    # Numeric columns (percentages and amounts)
    numeric_cols = [
        "interestRate",
        "accruedInterestPer1000",
        "accruedInterestPer100",
        "adjustedAccruedInterestPer1000",
        "adjustedPrice",
        "allocationPercentage",
        "averageMedianDiscountRate",
        "averageMedianInvestmentRate",
        "averageMedianPrice",
        "bidToCoverRatio",
        "totalAccepted",
        "totalTendered",
    ]
    df[numeric_cols] = df[numeric_cols].apply(pd.to_numeric, errors="coerce")

    # Boolean columns
    bool_cols = [
        "backDated",
        "callable",
        "cashManagementBillCMB",
        "fimaIncluded",
        "floatingRate",
        "reopening",
        "somaIncluded",
        "strippable",
        "tips",
    ]
    for col in bool_cols:
        df[col] = df[col].map({"true": True, "false": False})

    return df


def load_treasury_auction_data(data_dir: Path = DATA_DIR):
    """
    Load treasury auction data from parquet file.

    >>> df = load_treasury_auction_data()
    >>> df.info(verbose=True)
    <class 'pandas.core.frame.DataFrame'>
    RangeIndex: 10569 entries, 0 to 10568
    Data columns (total 120 columns):
    #    Column                                                 Dtype         
    ---   ------                                                 -----         
    0    cusip                                                  object        
    1    issueDate                                              datetime64[ns]
    2    securityType                                           object        
    3    securityTerm                                           object        
    4    maturityDate                                           datetime64[ns]
    5    interestRate                                           float64       
    6    refCpiOnIssueDate                                      object        
    7    refCpiOnDatedDate                                      object        
    8    announcementDate                                       datetime64[ns]
    9    auctionDate                                            datetime64[ns]
    10   auctionDateYear                                        object        
    11   datedDate                                              datetime64[ns]
    12   accruedInterestPer1000                                 float64       
    13   accruedInterestPer100                                  float64       
    14   adjustedAccruedInterestPer1000                         float64       
    15   adjustedPrice                                          float64       
    16   allocationPercentage                                   float64       
    17   allocationPercentageDecimals                           object        
    18   announcedCusip                                         object        
    19   auctionFormat                                          object        
    20   averageMedianDiscountRate                              float64       
    21   averageMedianInvestmentRate                            float64       
    22   averageMedianPrice                                     float64       
    23   averageMedianDiscountMargin                            object        
    24   averageMedianYield                                     object        
    25   backDated                                              object        
    26   backDatedDate                                          datetime64[ns]
    27   bidToCoverRatio                                        float64       
    28   callDate                                               datetime64[ns]
    29   callable                                               object        
    30   calledDate                                             datetime64[ns]
    31   cashManagementBillCMB                                  object        
    32   closingTimeCompetitive                                 object        
    33   closingTimeNoncompetitive                              object        
    34   competitiveAccepted                                    object        
    35   competitiveBidDecimals                                 object        
    36   competitiveTendered                                    object        
    37   competitiveTendersAccepted                             object        
    38   corpusCusip                                            object        
    39   cpiBaseReferencePeriod                                 object        
    40   currentlyOutstanding                                   object        
    41   directBidderAccepted                                   object        
    42   directBidderTendered                                   object        
    43   estimatedAmountOfPubliclyHeldMaturingSecuritiesByType  object        
    44   fimaIncluded                                           object        
    45   fimaNoncompetitiveAccepted                             object        
    46   fimaNoncompetitiveTendered                             object        
    47   firstInterestPeriod                                    object        
    48   firstInterestPaymentDate                               datetime64[ns]
    49   floatingRate                                           object        
    50   frnIndexDeterminationDate                              object        
    51   frnIndexDeterminationRate                              object        
    52   highDiscountRate                                       object        
    53   highInvestmentRate                                     object        
    54   highPrice                                              object        
    55   highDiscountMargin                                     object        
    56   highYield                                              object        
    57   indexRatioOnIssueDate                                  object        
    58   indirectBidderAccepted                                 object        
    59   indirectBidderTendered                                 object        
    60   interestPaymentFrequency                               object        
    61   lowDiscountRate                                        object        
    62   lowInvestmentRate                                      object        
    63   lowPrice                                               object        
    64   lowDiscountMargin                                      object        
    65   lowYield                                               object        
    66   maturingDate                                           datetime64[ns]
    67   maximumCompetitiveAward                                object        
    68   maximumNoncompetitiveAward                             object        
    69   maximumSingleBid                                       object        
    70   minimumBidAmount                                       object        
    71   minimumStripAmount                                     object        
    72   minimumToIssue                                         object        
    73   multiplesToBid                                         object        
    74   multiplesToIssue                                       object        
    75   nlpExclusionAmount                                     object        
    76   nlpReportingThreshold                                  object        
    77   noncompetitiveAccepted                                 object        
    78   noncompetitiveTendersAccepted                          object        
    79   offeringAmount                                         object        
    80   originalCusip                                          object        
    81   originalDatedDate                                      datetime64[ns]
    82   originalIssueDate                                      datetime64[ns]
    83   originalSecurityTerm                                   object        
    84   pdfFilenameAnnouncement                                object        
    85   pdfFilenameCompetitiveResults                          object        
    86   pdfFilenameNoncompetitiveResults                       object        
    87   pdfFilenameSpecialAnnouncement                         object        
    88   pricePer100                                            object        
    89   primaryDealerAccepted                                  object        
    90   primaryDealerTendered                                  object        
    91   reopening                                              object        
    92   securityTermDayMonth                                   object        
    93   securityTermWeekYear                                   object        
    94   series                                                 object        
    95   somaAccepted                                           object        
    96   somaHoldings                                           object        
    97   somaIncluded                                           object        
    98   somaTendered                                           object        
    99   spread                                                 object        
    100  standardInterestPaymentPer1000                         object        
    101  strippable                                             object        
    102  term                                                   object        
    103  tiinConversionFactorPer1000                            object        
    104  tips                                                   object        
    105  totalAccepted                                          float64       
    106  totalTendered                                          float64       
    107  treasuryRetailAccepted                                 object        
    108  treasuryRetailTendersAccepted                          object        
    109  type                                                   object        
    110  unadjustedAccruedInterestPer1000                       object        
    111  unadjustedPrice                                        object        
    112  updatedTimestamp                                       object        
    113  xmlFilenameAnnouncement                                object        
    114  xmlFilenameCompetitiveResults                          object        
    115  xmlFilenameSpecialAnnouncement                         object        
    116  tintCusip1                                             object        
    117  tintCusip2                                             object        
    118  tintCusip1DueDate                                      datetime64[ns]
    119  tintCusip2DueDate                                      datetime64[ns]
    dtypes: datetime64[ns](14), float64(12), object(94)
    memory usage: 9.7+ MB
    """
    df = pd.read_parquet(data_dir / "treasury_auction_stats.parquet")
    return df


def _demo():
    # Set display options to show all columns
    pd.set_option("display.max_columns", None)  # Show all columns
    pd.set_option("display.width", None)  # Don't wrap to multiple lines
    pd.set_option("display.max_rows", None)  # Show all rows

    df.dtypes
    df.info()


if __name__ == "__main__":
    dir_path = DATA_DIR
    dir_path.mkdir(parents=True, exist_ok=True)

    df = pull_treasury_auction_data()
    df.to_parquet(dir_path / "treasury_auction_stats.parquet", index=False)

# with open(data_dir / 'treasury_auction_stats.json', 'w') as json_file:
#     json.dump(data, json_file)
