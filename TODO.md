# Forecasting Methodology Improvements

A list of methodological improvements to consider for the neural / Auto-tuned
forecasting pipeline. Motivated by the observation that hybrid and deep-learning
families have strong median R² but sharply negative mean R² — driven by a
handful of catastrophic blowups on heavy-tailed disaggregated panels (CRSP
stocks, individual corporate bonds, BHC leverage).

See [src/forecasting/forecast_neural_auto.py](src/forecasting/forecast_neural_auto.py)
for the current Auto wrapper configuration.

## Status

- **2026-06-05** — **Data fixes on FX_returns and hkm_factors_monthly /
  hkm_all; ~6h targeted re-run.** While auditing the high pooled R² values
  from Phase C v2, found two genuine data bugs:

  1. **`src/foreign_exchange/calc_fx.py`** was computing
     `ret = spot_ratio * annualized_interest_pct` — i.e.\ multiplying the
     daily spot ratio (≈ 1) by the foreign interest rate **in annualised
     percent space** (e.g.\ 1.7 for 1.7\%). The result was essentially a
     "trajectory of foreign interest rates" with massive persistence, so any
     forecaster trivially achieved R² ≈ 0.99. The script's own docstring
     flagged the issue. Fix: convert annualised % to per-day decimal
     (ACT/360) and apply the carry-trade formula
     `ret = (S_{t-1}/S_t)(1 + r_f,daily) - 1`. After the fix, FX daily
     returns have std ≈ 0.5-0.8\% (correct), with the 2015 SNB peg break
     showing up as a +21\% outlier on CHF.

  2. **`src/he_kelly_manela/create_ftsfr_datasets.py`** was mixing two
     return series (intermediary capital risk factor and value-weighted
     investment return) with two state variables
     (`intermediary_capital_ratio`, `intermediary_leverage_ratio_squared`)
     in the same panel. The leverage-ratio-squared series had variance
     ~10^7× the returns, so the pooled R² was dominated by it. Fix: keep
     only the two return series.

  Affected: `ftsfr_FX_returns`, `ftsfr_he_kelly_manela_factors_monthly`,
  `ftsfr_he_kelly_manela_all` (and unused
  `ftsfr_he_kelly_manela_factors_daily`). 60-job re-run (8 auto neural × 2
  losses + 4 classical = 20 per dataset) at 4-way parallel: 5.8h wall. Plus
  one wasted prior 4h run because I updated `_data/<module>/` but not
  `_data/formatted/<module>/` — the forecasting pipeline reads from
  `_data/formatted/`. Lesson: always overwrite the formatted copy too.

  Backup of pre-fix CSVs at
  `_output/forecasting/error_metrics_backup_phase_c_v2_pre_data_fixes/`.

  Post-fix R²oos picture (pooled, 420 cells):

  - Mean: -0.092 (was +0.068 — FX/hkm artifacts had inflated it)
  - Median: 0.000
  - Min: -5.12, Max: 0.982 (legit: `treasury_swap_basis`, persistent basis
    spread)
  - #R²<-1: 24, #R²<-2: 15, #R²<-5: 1

  Per-model: ARIMA mean +0.11, TiDE +0.04, DLinear +0.02; NBEATS worst at
  -0.44 (still has 6 R²<-1 cells, mostly disaggregated panels). NHITS on
  `hkm_factors_monthly` achieves +0.44 (genuine — that dataset has only 2
  return series, so the panel is well-conditioned). `treasury_swap_basis`
  R²>0.97 across the board: basis spreads ARE highly forecastable in the
  literature.

  The paper narrative "asset returns have R²oos near zero, basis spreads
  are where ML helps" is *more* supported after these fixes, not less. FX
  return R² now ≈ 0 for the best models (consistent with Welch-Goyal-style
  results); basis spreads stay at R² ≈ 1.

  **cjs_options flagged but not changed**: 54 option-portfolio series have
  3160× variance heterogeneity, and pooled R² hits 0.998 for most models.
  Hard to disentangle whether this is (a) real predictability driven by a
  few high-variance OTM call contracts that dominate the panel sum or
  (b) a data construction artifact — separate investigation underway.
  Also: nearly every series has `min y > 0`, which is unusual since
  calls/puts held to expiration should sometimes return -100%. Worth
  digging into the source paper's exact return definition; left for the
  options-thread.

- **2026-06-05** — **Phase C v2 complete; R²oos formula changed to pooled
  panel-wide.** While investigating why KAN went from legacy R²=−0.085 to
  Phase C v1 R²=−40.59 on `ftsfr_CDS_contract_returns`, the diagnostic ran
  in `/tmp/diagnose_kan.py` showed KAN's predictions were unchanged. The
  collapse was an **aggregation artifact**: the legacy formula computed
  per-series `1 − MSE_model/MSE_HistAvg` and then averaged across series,
  so a handful of CDS contracts with extremely low return variance
  (`MSE_HistAvg` ≈ 1e-7) blew up the mean. We switched to the canonical
  pooled definition

      R²oos = 1 − Σ_{s,t} (y - ŷ)² / Σ_{s,t} (y - ȳ_train,s)²

  (Gu-Kelly-Xiu 2020, Campbell-Thompson 2008). `calculate_oos_r2` now
  returns both; the CSV `R2oos` column is the headline pooled value,
  `R2oos_per_series_mean` is kept as a hidden diagnostic. Paper §
  *Error Metrics* in [reports/draft_ftsfr.tex](reports/draft_ftsfr.tex)
  reflects the change; the legacy formula is not mentioned in the draft.

  Re-ran all 560 dual-fit jobs (45h wall, 4-way parallel, 0 failures).
  Predictions identical to v1, only the reported R² changes. Backup of
  v1 CSVs (with the legacy R² as headline) is at
  `_output/forecasting/error_metrics_backup_phase_c_v1_persmean_r2/`.

  Per-model picture from pooled R² (Phase C v2):

  | model       | mean R² | median R² | min R² | #R²<-1 | #R²<-2 |
  | ----------- | ------: | --------: | -----: | -----: | -----: |
  | arima       |  +0.21  |   +0.17   | -0.42  | 0 | 0 |
  | deepar      |  +0.11  |   +0.03   | -1.05  | 1 | 0 |
  | dlinear     |  +0.21  |   +0.10   | -2.08  | 1 | 1 |
  | kan         |  +0.06  |   +0.07   | -3.82  | 1 | 1 |
  | nbeats      |  -0.19  |   +0.03   | -5.12  | 4 | 3 |
  | nhits       |  +0.04  |   +0.02   | -1.71  | 3 | 0 |
  | nlinear     |  +0.06  |   +0.02   | -4.59  | 2 | 1 |
  | ses         |  +0.01  |   +0.18   | -3.04  | 2 | 2 |
  | theta       |  +0.02  |   +0.20   | -4.32  | 2 | 2 |
  | tide        |  +0.19  |   +0.04   | -0.80  | 0 | 0 |
  | transformer |  +0.11  |   +0.03   | -1.50  | 1 | 0 |

  **Headline narrative change**: across all 420 (dataset, model) cells,
  mean pooled R² = **+0.068**, median = +0.028, only **10 cells with
  R² < −2** (was 33 under v1's per-series mean). The v1 framing of
  "deep learning has positive median but catastrophic mean R²" was
  largely an aggregation artifact. Under pooled aggregation, every
  neural model has a positive mean R² except NBEATS (which still has
  3 R² < −2 cells; worth a follow-up). The "DeepAR catastrophic
  blowups on CRSP/corp_bond" narrative that motivated item (2) of this
  TODO was also partly an artifact — DeepAR's pooled R² on those
  datasets was small-negative even pre-StudentT.

- **2026-05-31 — canary verdict on `--scale-entity` (DROPPED)**: 4
  datasets × 8 models × `--loss mse` × {scale, no-scale} = 64 jobs, 22.6h
  wall. 13 wins / 12 losses / 7 ties; mean Δ per-series-mean R² ≈ 0 with
  worst loss −8.59 (NHITS on CRSP_ret under legacy R²). Implementation
  is in `forecast_neural_auto.py` behind `--scale-entity` and stays
  available for sensitivity work; default off. Note: the canary measured
  ΔR² under the v1 per-series-mean formula; the verdict may shift under
  the new pooled formula but a re-canary is unlikely to be worth ~30h.

- **2026-05-29/30**: Items (2) and (3) applied **to AutoDeepAR only**. DeepAR
  now uses `DistributionLoss(distribution="StudentT")` and `valid_loss=MSE()`.
  Full 32-dataset DeepAR sweep on Apple-Silicon MPS took **~7.4h wall** (down
  from ~15.3h pre-StudentT; the speedup is from faster convergence in the new
  Optuna search, not from compute). Requires `PYTORCH_ENABLE_MPS_FALLBACK=1`
  because StudentT sampling needs `aten::_standard_gamma` which is not yet on
  MPS — only the predict-time sampling op falls back to CPU.

  Effect on the catastrophic-blowup datasets that motivated this TODO:

  | dataset                                          | old R² | new R² |
  | ------------------------------------------------ | -----: | -----: |
  | ftsfr_CRSP_monthly_stock_ret                     | −27.92 |  −0.77 |
  | ftsfr_CRSP_monthly_stock_retx                    | −35.59 |  −0.58 |
  | ftsfr_corp_bond_returns                          | −29.04 |  −0.10 |
  | ftsfr_corp_bond_str_deciles_naive                |  −4.01 |  +0.06 |
  | ftsfr_nyu_call_report_holding_company_leverage   | −15.78 |  −0.04 |
  | ftsfr_nyu_call_report_holding_company_cash_liq.  |  −2.75 |  +0.35 |
  | ftsfr_nyu_call_report_leverage                   |  −2.94 |  −0.01 |
  | ftsfr_FX_returns                                 |  −0.79 |  +0.94 |

  Across all 32 datasets, mean DeepAR R² went **−3.64 → +0.06**, median
  **−0.09 → +0.10**, and the count of datasets with R² < −1 fell **7 → 1**
  (only `ftsfr_treasury_sf_basis` remains, at −1.27).

  A handful of well-behaved datasets regressed mildly (e.g., tips_treasury_basis
  0.87 → 0.61, treasury_swap_basis 0.96 → 0.94, treas_portfolios_strict
  0.22 → 0.11). Net effect on aggregate metrics is strongly positive.

- **Compute extrapolation for the big fix (item 1 + dual-fit across all
  neural models)**: 7.4h for DeepAR alone over 32 datasets. The seven other
  Auto wrappers (NBEATS, NHITS, DLinear, NLinear, VanillaTransformer, TiDE,
  KAN) currently use `MAE()` only. A dual-fit pipeline doubles that, and
  applies to all eight neural models, so a rough budget is
  `7.4h × 2 (loss variants) × 8 (models) / 1 (DeepAR baseline) ≈ 120h` of
  serial MPS compute — call it ~5 days serial, or a weekend on a multi-GPU
  box. Items (3) and (4) are essentially free once we are already paying for
  (1). This is the number to make the go/no-go call from.

## 1. Metric-aligned dual fitting (HIGH IMPACT)

Currently the Auto wrappers train all models with `MAE()` and select
hyperparameters by the same MAE objective during Optuna search. But the paper
reports both MASE (absolute-error-based) and R² (squared-error-based). A model
tuned for MAE can have a perfectly reasonable MASE while producing a
catastrophic R² on heavy-tailed data — a single tail point dominates MSE.

**Proposal**: fit each neural model twice per dataset.

- **MAE fit**: train and tune with `loss=MAE()`. Use these forecasts when
  computing MASE and Relative MASE.
- **MSE fit**: train and tune with `loss=MSE()`. Use these forecasts when
  computing R²oos.

This is more compute (roughly 2× neural training cost) but makes the reported
numbers internally consistent: every metric is reported from a model that was
actually optimized for that metric. Removes the implicit metric mismatch in
the current setup and gives ML/hybrid methods a fair shot at R²oos.

Implementation notes:
- Easiest path: parameterize `forecast_neural_auto.py` by a `--loss {mae,mse}`
  CLI flag, write outputs into separate result files
  (`results_all_mae.csv`, `results_all_mse.csv`), and stitch them together in
  `create_results_tables.py` when building each metric's pivot.
- `dodo_02_forecasting.py` would need parallel task definitions for the two
  loss variants.
- Classical models (ARIMA, Theta, SES) are unaffected — they don't expose a
  loss choice; report the same forecasts under both metrics.

## 2. DeepAR: switch Normal → Student-t (HIGH IMPACT, LOW EFFORT)

DeepAR is the worst single offender, with 6 catastrophic blowups out of 27
datasets (next-worst is N-HiTS at 4). It is also the only model using a
distributional loss: `DistributionLoss(distribution="Normal")` in
[forecast_neural_auto.py:878](src/forecasting/forecast_neural_auto.py#L878).

A Gaussian likelihood is empirically wrong for financial returns — fat tails
pull the location estimate far from the median to absorb tail residuals the
Normal cannot represent. The fix is one line:

```python
loss=DistributionLoss(distribution="StudentT"),
```

This should dramatically reduce DeepAR's blowup count on stock and bond
panels. Worth doing even outside the dual-fit proposal above.

## 3. Align Auto validation metric with reporting metric (MEDIUM IMPACT)

Independent of (1), Nixtla's Auto wrappers accept a separate `valid_loss`
argument that controls the Optuna search objective. By default it equals
the training `loss`. If we keep a single fit per model (i.e., decline to do
dual fitting), at minimum we should pass `valid_loss=MSE()` so the
hyperparameter search optimizes for R² when we'll report R².

This is a strict improvement over the current setup, but is superseded by
proposal (1) which does the better thing of training on the right metric too.

## 4. Add gradient clipping and explicit early stopping (LOW IMPACT)

PyTorch Lightning supports `gradient_clip_val` and `EarlyStopping` callbacks
that the current config doesn't use. Adding them would prevent occasional
training instabilities at high learning rates and avoid wasting compute when
a model has already converged before `max_steps`.

Suggested values:
- `gradient_clip_val=1.0` in all `config()` builders.
- `EarlyStopping(monitor="ptl/val_loss", patience=20)` as a callback.

Probably won't move the blowup count much because the blowups appear to be
about model class fit, not training instability — but cheap to add and standard
practice.

## 5. Increase Optuna budget for high-cardinality panels (LOW IMPACT, HIGH COMPUTE)

`NUM_SAMPLES = 20` (5 for daily frequency) is small for the 16K-entity
corporate bond panel and the multi-thousand-entity CRSP / BHC panels.
Doubling to 40 for monthly and 10 for daily might give Auto a better shot at
finding configurations that don't blow up on heavy-tailed panels.

Trade-off: roughly linear increase in compute. Probably not worth doing
unless (1) and (2) are already in place and we still see structural blowups.

## 6. Reconsider per-entity scaling (RESEARCH QUESTION)

Current scaling is `scaler_type="robust"` applied per training window. For
panels with extreme cross-sectional heterogeneity (CRSP stocks have
returns ranging from -90% to +500% over the sample), per-window scaling
within a single global model may be insufficient — the model sees normalized
inputs but the realized return distribution that R²oos is computed against
is still raw.

Worth investigating whether a per-entity standardization layer (z-score
each entity's history during training, invert at predict time) would help on
the stock and bond panels. Risk: introduces a layer of complexity that
breaks the "off-the-shelf Auto" framing.

## 7b. Revisit ML-vs-classical framing on bank and intermediary indicators after (1)/(2)

Current finding: classical statistical methods (ARIMA, Theta) edge out hybrid
and deep-learning baselines on bank and intermediary indicators by mean R²oos
(0.470 vs 0.372 hybrid vs -0.158 deep learning). The negative deep-learning
mean is driven by tail blowups on BHC Leverage (and similar disaggregated
panels) that the dual-fit + StudentT improvements in items (1)-(2) above are
expected to mitigate.

After applying (1) and (2), re-run the bank-and-intermediary panel and check
whether the classical edge survives. If it shrinks materially, soften the
abstract / intro / conclusion phrasing from "edge out" to "are competitive
with." The current paper text uses the firmer phrasing because that is what
the table actually shows today; revisit once the methodology fixes land.

## 7. Honest caveat to flag in paper regardless

Some chunk of the mean R²oos of ~-0.79 for hybrid / -0.71 for deep learning
is an honest feature of the data: pooling tens of thousands of individual
securities into a global model means *some* idiosyncratic shocks are
unforecastable, and squared-error scoring punishes the worst miss heavily.
Even after applying every fix above we should expect a non-trivial residual
gap between median and mean R²oos on the disaggregated panels.

If we don't apply (1) and (2), Section 5 should explicitly note that:
(a) DeepAR uses a Gaussian distribution loss inconsistent with heavy-tailed
return data, and (b) hyperparameters are selected by MAE on validation
folds while R²oos is computed from squared errors at test time — so the
search is not optimizing what we report.

## Priority order if pursuing

1. **DeepAR Normal → Student-t** (item 2): one-line fix, large expected impact, defensible as a bug fix.
2. **Dual-fit MAE+MSE pipeline** (item 1): the rigorous solution; more compute and code, but eliminates the metric mismatch entirely.
3. **Gradient clipping + early stopping** (item 4): cheap hygiene, do alongside (2).
4. **Optuna budget bump** (item 5): only if (1)-(3) haven't closed the gap.
5. **Per-entity scaling** (item 6): exploratory; revisit if the mean-vs-median R² gap persists.
