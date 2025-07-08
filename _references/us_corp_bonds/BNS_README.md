### Page 1
# Duration-Matched Treasury Returns for WRDS Bond Returns Data 

Yoshio Nozawa

This Version: June 6, 2024

## Summary

This dataset contains a monthly return on Treasury bonds whose duration is matched to a corporate bond in the WRDS Bond Returns data. The procedure for computing the return follows Binsbergen, Nozawa, and Schwert (2024) with some modifications to match the return variable in WRDS.

The return (tr_return) is computed for all bonds where possible, including those that are not used in the paper (such as bonds that do not have semi-annual coupons or bonds that are issued by financial or utility companies). The return is missing if no yield is available for the previous month or if the bond has a maturity of more than 30 years. The unit is percentage per month (e.g. 0.2 means $0.20 \%$ per month). In addition, the dataset provides the yield to maturity of the Treasury bond (tr_ytm_match), expressed in percent per year, and the remaining time to maturity (tau) in years.

You can calculate duration-adjusted corporate bond returns by taking the difference between corporate bond returns in WRDS and the duration-matched Treasury returns in this dataset. This return removes the mechanical changes in corporate bond prices resulting from movements in the Treasury yield curve and better captures the component of corporate bond returns that corresponds to credit and liquidity risk.

When using these data, please cite Binsbergen, Nozawa and Schwert (2024).

## Details

To match the return in the WRDS data, I use the Gürkaynak, Sack, and Wright (2007)'s yield curve data ${ }^{1}$ as of the transaction date of corporate bonds, not as of the end of the month. For example, if a May 2024 return on a corporate bond is computed using transaction prices on April $10^{\text {th }}$ and May $20^{\text {th }}$, then I use the yield curve information on those dates and calculate the changes in Treasury zero-coupon bond prices implicit in the yield curve. The cash flows

[^0]
[^0]:    ${ }^{1}$ https://www.federalreserve.gov/data/nominal-yield-curve.htm

### Page 2
of the corporate bond are projected as of April $10^{\text {th }}$, which determines the weight for each payment date in the future.

For each payment among the projected cash flows, I compute Treasury zero-coupon bond prices using the yield curve parameters provided in the GSW dataset on the corporate bond's transaction dates. If a zero-coupon bond matures (i.e. a coupon of the corporate bond is paid) during the holding period, it has a price of one. The growth rate of the Treasury zerocoupon bond prices is the return. Then, the returns of each payment are averaged using the present value of the corporate bond's cash flows as the weight, and the resulting average is the duration-matched Treasury return.

There are three corporate bond return variables in the WRDS data: ret_eom, ret_l5m, and ret_ldm. Regardless of the choice among the three variables, the matched Treasury bond returns are the same because the transaction dates are common across the three types of returns.

The resulting market returns as of December 2020 are plotted below.
![img-0.jpeg](img-0.jpeg)

### Page 3
|  The number of observations of variable tr_return. | |   |   |
| --- | --- | --- | --- |
|   | Deleted Obs. | Remaining Obs.  |
|  # Observations of RET_EOM |  | 1,984,308  |
|  Maturity more than 30 years | 21,692 | 1,962,616  |
|  Yield in the previous month cannot be computed | 658 | 1,961,958  |
|  Yield is -100% and the annual coupon payment | 5 | 1,961,953  |
|  Trade is on Jan 18, 2021 (holiday) | 1 | 1,961,952  |
|  # Observations of TR_RET |  | 1,961,952  |

### Page 4
# Reference 

Binsbergen, Van Jules, Yoshio Nozawa and Michael Schwert, "Duration-Based Valuation of Corporate Bonds", Review of Financial Studies, forthcoming.

Gürkaynak, Refet S., Brian Sack, and Jonathan H. Wright (2007), "The U.S. Treasury Yield Curve: 1961 to the Present," Journal of Monetary Economics, vol 54, pp2291-2304. Return to text