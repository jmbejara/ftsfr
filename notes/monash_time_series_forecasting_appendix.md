### Page 1
# Appendix <br> Monash Time Series Forecasting Archive 

Rakshitha Godahewa<br>Monash University<br>Melbourne, Australia<br>rakshitha.godahewa@monash.edu<br>Christoph Bergmeir<br>Monash University<br>Melbourne, Australia<br>christoph.bergmeir@monash.edu

Geoffrey L Webb<br>Monash University<br>Melbourne, Australia<br>geoff.webb@monash.edu<br>Rob J. Hyndman<br>Monash University<br>Melbourne, Australia<br>rob.hyndman@monash.edu<br>Pablo Montero-Manso<br>University of Sydney<br>Australia<br>pmontm@gmail.com

## A Data records

Our archive contains 30 time series datasets. Out of these, 25 datasets contain multiple related time series to facilitate the evaluation of global time series forecasting models (Section A.6). The remaining 5 datasets contain single very long time series (Section A.7).

## A. 1 Data collection procedure

Out of the 30 datasets, 23 were already publicly available in different platforms with different data formats. The original sources of all datasets are mentioned in the datasets descriptions (Sections A. 6 and A.7). Out of these 23 datasets, 8 originate from competition platforms, 3 from research conducted by Lai et al. [1], 5 are taken from R packages, 1 is from the Kaggle platform [2], and 1 is taken from a Johns Hopkins repository [3] whereas the other datasets have been extracted from corresponding domain specific platforms. The remaining 7 datasets were manually curated by us as explained in Sections A.6.11, A.6.12, A.6.16, A.6.19, A.6.25, A.7.4 and A.7.5.

After extracting and curating these datasets, we analysed them individually to identify the datasets containing series with different frequencies and missing observations. Nine datasets contain time series belonging to different frequencies and the archive contains a separate dataset per each frequency. Eleven of the datasets have series with missing values. The archive contains 2 versions of each of these, one with and one without missing values. In the latter case, the missing values have been replaced by using an appropriate imputation technique as explained in Sections A. 6 and A.7. Finally, we obtain 58 datasets with the above explained different versions.

The 58 datasets are then converted to .tsf format which is a new format we introduce to store time series datasets as explained in Section 2.1 of the main paper. An example of series in this format is shown in Figure 1. The .tsf files are zipped and uploaded into our datasets archive available at https: //zenodo.org/communities/forecasting where other researchers can directly download them for further research use. Code to load the datasets in .tsf format into R and Python is available in our github repository at https://github.com/rakshitha123/TSForecasting.

## A. 2 Intended use of datasets

All datasets in our repository are intended for research purposes and to evaluate the performance of new forecasting algorithms.

### Page 2
```
# Dataset Information
# This dataset was used in the NN5 forecasting competition.
# It contains 111 daily time series from the banking domain.
# The goal is predicting the daily cash withdrawals from ATMs in UK.
#
# For more details, please refer to
# Ben Taieb, S., Bontempi, G., Atiya, A.F., Sorjamas, A., 2012.
# A review and comparison of strategies for multi-step ahead time series forecasting based on
# the nn5 forecasting competition. Expert Systems with Applications 39(0), 7067 - 7083
#
# Neural Forecasting Competitions, 2008.
# NN5 forecasting competition for artificial neural networks and computational intelligence.
# Accessed: 2020-05-10. UNL http://www.neural-forecasting-competition.com/NN5/
#
@relation NN5
@attribute series_name string
@attribute start_timestamp date
@frequency daily
@horizon 54
@missing true
@equallength true
@data
TI:1996=03=18 00=00=00:13.4070294784581,14.7250566893424,20.5640589569161,34.7080498866213,26.
T2:1996=03=18 00=00=00:11.5504535147392,15.5912698412498,15.0368480725624,21.5702947845805,19.
T3:1996=03=18 00=00=00:5.640589569161,14.3990929705215,24.4189342403628,28.7840136054422,20.61
T4:1996=03=18 00=00=00:13.1802721088435,8.44671201814059,19.515306122449,28.8832199546485,19.4
T5:1996=03=18 00=00=00:9.7789156462585,10.8134920634921,21.6128117913832,38.5204081632653,24.
T6:1996=03=18 00=00=00:9.24036281179138,11.6354875283447,12.1031746031746,21.4143990929705,24.
T7:1996=03=18 00=00=00:14.937641723356,16.2840136054422,16.6666666666667,23.5685941043084,26.1
T8:1996=03=18 00=00=00:2.89115646258503,12.3582766439909,16.3832199546485,30.1587301587302,31.
T9:1996=03=18 00=00=00:7.34126984126988,9.15532879818594,10.5867346938776,12.5,7.1570294784581
T10:1996=03=18 00=00=00:10.2891156462585,12.7125850340136,14.4416099773243,19.4019274376417,21
```

Figure 1: An example of the file format for the NN5 daily dataset.

# A. 3 Hosting, licensing, maintenance and preservation 

All datasets are permanently available, and they are hosted and maintained at https://zenodo.org/ communities/forecasting where researchers can directly download the datasets. All datasets are under Creative Commons Attribution 4.0 International license where the users can modify, distribute and use the datasets as long as they credit the original authors for the downloaded datasets from the repository.

Furthermore, a summary of datasets, links to download all datasets, the extracted features of each time series of all datasets, benchmark results of the datasets across 10 error metrics and links to all implementations related to the archive are hosted and maintained on our website at https: //forecastingdata.org/.

We also encourage other researchers to contribute time series datasets to our repository either by directly uploading them into the archive and/or by contacting the authors via email.

## A. 4 Code availability and reproducibility of results

All implementations related to the forecasting archive, namely code to reproduce all benchmark experiments, the feature extraction, and code for loading the datasets in our .tsf format into the R and Python environments, is available at https://github.com/rakshitha123/TSForecasting.

We ensure that both feature analysis and benchmark results are reproducible. The instructions on executing the related experiments are available in our github repository. The code uses the best implementations available across the R and Python programming languages and they do not require any paid dependencies.

As new forecasting models emerge rapidly, we also provide a simple interface for users to implement other statistical, machine learning and deep learning baselines. Our github repository contains detailed instructions and example code snippets explaining how to integrate new forecasting models to our framework. The results of the newly integrated forecasting models are also evaluated in the same way as our baselines using the same evaluation metrics and thus, the results of new forecasting models and our baselines are directly comparable. After integrating the new forecasting models, users can send

### Page 3
us a pull-request on github to officially integrate their implementations to our framework. The users are also invited to send us the results of their new forecasting models. If computationally feasible, we expect to re-execute the models and confirm the results. In the future, we expect to maintain two results tables in our website with the confirmed and unconfirmed results of the forecasting models.

# A. 5 Author statement 

We, all authors bear all responsibility in case of violation of dataset rights. We have checked the licensing of all datasets and have only uploaded the publicly shareable datasets to our repository. We have also mentioned the original sources of all datasets in our website, https://forecastingdata. org/.

If there are any copyright issues of the datasets, please contact the authors via email.

The next sections explain the datasets in our repository in detail.

## A. 6 Time series datasets

This section describes the benchmark datasets that have a sufficient number of series from a particular frequency. The datasets may contain different categories in terms of domain and frequency.

## A.6.1 M1 dataset

The M1 competition dataset [4] contains 1001 time series with 3 different frequencies: yearly, quarterly, and monthly as shown in Table 1. The series belong to 7 different domains: macro 1, macro 2 , micro 1 , micro 2 , micro 3 , industry, and demographic.

Table 1: Summary of M1 dataset

| Frequency | No: of Series | Min. Length | Max. Length | Forecast Horizon |
| :-- | :--: | :--: | :--: | :--: |
| Yearly | 181 | 15 | 58 | 6 |
| Quarterly | 203 | 18 | 114 | 8 |
| Monthly | 617 | 48 | 150 | 18 |
| Total | 1001 |  |  |  |

Research work which uses this dataset includes:

- Forecasting with artificial neural networks: the state of the art [5]
- Time series forecasting using a hybrid ARIMA and neural network model [6]
- Automatic time series forecasting: the forecast package for R [7]
- Exponential Smoothing: the state of the art [8]
- Neural network forecasting for seasonal and trend time series [9]

The DOI links to access and download the datasets are as follows:

- Yearly dataset: http://doi.org/10.5281/zenodo. 4656193
- Quarterly dataset: http://doi.org/10.5281/zenodo. 4656154
- Monthly dataset: http://doi.org/10.5281/zenodo. 4656159


## A.6.2 M3 dataset

The M3 competition dataset [10] contains 3003 time series of various frequencies including yearly, quarterly, and monthly, as shown in Table 2. The series belong to 6 different domains: demographic, micro, macro, industry, finance, and other.
Research work which uses this dataset includes:

- The theta model: a decomposition approach to forecasting [11]

### Page 4
Table 2: Summary of M3 dataset

| Frequency | No: of Series | Min. Length | Max. Length | Forecast Horizon |
| :-- | :--: | :--: | :--: | :--: |
| Yearly | 645 | 20 | 47 | 6 |
| Quarterly | 756 | 24 | 72 | 8 |
| Monthly | 1428 | 66 | 144 | 18 |
| Other | 174 | 71 | 104 | 8 |
| Total | 3003 |  |  |  |

- Recurrent neural networks for time series forecasting: current status and future directions [12]
- Ensembles of localised models for time series forecasting [13]
- Out-of-sample tests of forecasting accuracy: an analysis and review [14]
- Metrics for evaluating performance of prognostic techniques [15]
- Temporal link prediction using matrix and tensor factorizations [16]
- Forecasting time series with complex seasonal patterns using exponential smoothing [17]
- Evaluating forecasting methods [18]
- Exponential smoothing with a damped multiplicative trend [19]

The DOI links to access and download the datasets are as follows:

- Yearly dataset: http://doi.org/10.5281/zenodo. 4656222
- Quarterly dataset: http://doi.org/10.5281/zenodo. 4656262
- Monthly dataset: http://doi.org/10.5281/zenodo. 4656298
- Other dataset: http://doi.org/10.5281/zenodo. 4656335


# A.6.3 M4 dataset 

The M4 competition dataset [20, 21] contains 100,000 time series with 6 different frequencies: yearly, quarterly, monthly, weekly, daily, and hourly, as shown in Table 3. The series belong to 6 different domains: demographic, micro, macro, industry, finance, and other, similar to the M3 forecasting competition. This dataset contains a subset of series available at ForeDeCk [22].

Table 3: Summary of M4 dataset

| Frequency | No: of Series | Min. Length | Max. Length | Forecast Horizon |
| :-- | :--: | :--: | :--: | :--: |
| Yearly | 23000 | 19 | 841 | 6 |
| Quarterly | 24000 | 24 | 874 | 8 |
| Monthly | 48000 | 60 | 2812 | 18 |
| Weekly | 359 | 93 | 2610 | 13 |
| Daily | 4227 | 107 | 9933 | 14 |
| Hourly | 414 | 748 | 1008 | 48 |
| Total | 100000 |  |  |  |

Research work which uses this dataset includes:

- A hybrid method of exponential smoothing and recurrent neural networks for time series forecasting [23]
- FFORMA: Feature-based Forecast Model Averaging [24]
- Ensembles of localised models for time series forecasting [13]
- Recurrent neural networks for time series forecasting: current status and future directions [12]
- LSTM-MSNet: leveraging forecasts on sets of related time series with multiple seasonal patterns $[25]$

### Page 5
- Are forecasting competitions data representative of the reality? [26]
- Averaging probability forecasts: back to the future [27]
- A strong baseline for weekly time series forecasting [28]

The DOI links to access and download the datasets are as follows:

- Yearly dataset: http://doi.org/10.5281/zenodo.4656379
- Quarterly dataset: http://doi.org/10.5281/zenodo.4656410
- Monthly dataset: http://doi.org/10.5281/zenodo.4656480
- Weekly dataset: http://doi.org/10.5281/zenodo.4656522
- Daily dataset: http://doi.org/10.5281/zenodo.4656548
- Hourly dataset: http://doi.org/10.5281/zenodo.4656589


# A.6.4 Tourism dataset 

This dataset originates from a Kaggle competition [29, 30] and contains 1311 tourism related time series with 3 different frequencies: yearly, quarterly, and monthly as shown in Table 4.

Table 4: Summary of tourism dataset

| Frequency | No: of Series | Min. Length | Max. Length | Forecast Horizon |
| :-- | :--: | :--: | :--: | :--: |
| Yearly | 518 | 11 | 47 | 4 |
| Quarterly | 427 | 30 | 130 | 8 |
| Monthly | 366 | 91 | 333 | 24 |
| Total | 1311 |  |  |  |

Research work which uses this dataset includes:

- Recurrent neural networks for time series forecasting: current status and future directions [12]
- A meta-analysis of international tourism demand forecasting and implications for practice [31]
- Improving forecasting by estimating time series structural components across multiple frequencies [32]
- Forecasting tourist arrivals using time-varying parameter structural time series models [33]
- Forecasting monthly and quarterly time series using STL decomposition [34]
- A novel approach to model selection in tourism demand modeling [35]

The DOI links to access and download the datasets are as follows:

- Yearly dataset: http://doi.org/10.5281/zenodo.4656103
- Quarterly dataset: http://doi.org/10.5281/zenodo.4656093
- Monthly dataset: http://doi.org/10.5281/zenodo.4656096


## A.6.5 NN5 dataset

This dataset contains 111 time series of daily cash withdrawals from Automated Teller Machines (ATM) in the UK, and was used in the NN5 forecasting competition [36]. The forecast horizon considered in the competition was 56. The original dataset contains missing values. Our repository contains two versions of the dataset: the original version with missing values and a modified version where the missing values have been replaced using a median substitution where a missing value on a particular day is replaced by the median across all the same days of the week along the whole series as in Hewamalage et al. [12]. Furthermore, Godahewa et al. [28] use a weekly aggregated version of this dataset. The aggregated weekly version of this dataset is also available in our repository. Research work which uses this dataset includes:

### Page 6
- Recurrent neural networks for time series forecasting: current status and future directions [12]
- A strong baseline for weekly time series forecasting [28]
- Forecasting across time series databases using recurrent neural networks on groups of similar series: a clustering approach [37]
- Forecast combinations of computational intelligence and linear models for the NN5 time series forecasting competition [38]
- Forecasting the NN5 time series with hybrid models [39]
- Multiple-output modeling for multi-step-ahead time series forecasting [40]
- Recursive multi-step time Series forecasting by perturbing data [41]
- Benchmarking of classical and machine-learning algorithms (with special emphasis on bagging and boosting approaches) for time series forecasting [42]

The DOI links to access and download the datasets are as follows:

- Daily dataset with missing values: http://doi.org/10.5281/zenodo.4656110
- Daily dataset without missing values: http://doi.org/10.5281/zenodo.4656117
- Weekly dataset: http://doi.org/10.5281/zenodo.4656125


# A.6.6 CIF 2016 dataset 

The dataset from the Computational Intelligence in Forecasting (CIF) 2016 forecasting competition contains 72 monthly time series. Out of those, 24 series originate from the banking sector, and the remaining 48 series are artificially generated. There are 2 forecast horizons considered in the competition where 57 series have a forecasting horizon of 12 and the remaining 15 series consider the forecast horizon as 6 [43]. Research work which uses this dataset includes:

- Recurrent neural networks for time series forecasting: current status and future directions [12]
- Ensembles of localised models for time series forecasting [13]
- Forecasting across time series databases using recurrent neural networks on groups of similar series: a clustering approach [37]
- Improving time series forecasting: an approach combining bootstrap aggregation, clusters and exponential smoothing [44]
- Time series clustering using numerical and fuzzy representations [45]
- An automatic calibration framework applied on a metaheuristic fuzzy model for the CIF competition $[46]$

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656042.

## A.6.7 Kaggle web traffic dataset

This dataset contains 145063 daily time series representing the number of hits or web traffic for a set of Wikipedia pages from 01/07/2015 to 10/09/2017 used by the Kaggle web traffic forecasting competition [47]. The forecast horizon considered in the competition was 59. As the original dataset contains missing values, we include both the original dataset in our repository and an imputed version. This dataset is intermittent and hence, we impute missing values with zeros. Furthermore, Godahewa et al. [28] use the weekly aggregated version of this dataset containing the first 1000 series. Our repository also contains this aggregated weekly version of the dataset for all series. The missing values of the original dataset were imputed before the aggregation. Research work which uses this dataset includes:

- Recurrent neural networks for time series forecasting: current status and future directions [12]
- Ensembles of localised models for time series forecasting [13]

### Page 7
- A strong baseline for weekly time series forecasting [28]
- Web traffic prediction of Wikipedia pages [48]
- Improving time series forecasting using mathematical and deep learning models [49]
- Foundations of sequence-to-sequence modeling for time series [50]

The DOI links to access and download the datasets are as follows:

- Daily dataset with missing values: http://doi.org/10.5281/zenodo.4656080
- Daily dataset without missing values: http://doi.org/10.5281/zenodo. 4656075
- Weekly dataset: http://doi.org/10.5281/zenodo. 4656664


# A.6.8 Solar dataset 

This dataset contains 137 time series representing the solar power production recorded every 10 minutes in the state of Alabama in 2006. It was used by Lai et al. [1], and originally extracted from Solar [51]. Furthermore, Godahewa et al. [28] use an aggregated version of this dataset containing weekly solar power production records. The aggregated weekly version of this dataset is also available in our repository.
The DOI links to access and download the datasets are as follows:

- 10 minutes dataset: http://doi.org/10.5281/zenodo. 4656144
- Weekly dataset: http://doi.org/10.5281/zenodo. 4656151


## A.6.9 Electricity dataset

This dataset represents the hourly electricity consumption of 321 clients from 2012 to 2014 in kilowatt (kW). It was used by Lai et al. [1], and originally extracted from UCI [52]. Our repository also contains an aggregated version of this dataset representing the weekly electricity consumption values.
The DOI links to access and download the datasets are as follows:

- Hourly dataset: http://doi.org/10.5281/zenodo. 4656140
- Weekly dataset: http://doi.org/10.5281/zenodo. 4656141


## A.6.10 London smart meters dataset

This dataset contains 5560 half-hourly time series that represent the energy consumption readings of London households in kWh from November 2011 to February 2014 [53]. The series are categorized into 112 blocks in the original dataset. The series in our repository are in the same order (from block 0 to block 111) as they are in the original dataset. The original dataset contains missing values and we impute them using the last observation carried forward (LOCF) method. Our repository contains both versions: the original version with missing values and the modified version where the missing values have been replaced. Research work which uses this dataset includes:

- Predicting electricity consumption using deep recurrent neural networks [54]
- A single scalable LSTM model for short-term forecasting of disaggregated electricity loads [55]
- Deep learning based short-term load forecasting for urban areas [56]
- Smart grid energy management using RNN-LSTM: a deep learning-based approach [57]

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 4656072
- Dataset without missing values: http://doi.org/10.5281/zenodo. 4656091

### Page 8
# A.6.11 Australian electricity demand dataset 

This dataset contains 5 time series representing the half hourly electricity demand of 5 states in Australia: Victoria, New South Wales, Queensland, Tasmania and South Australia. This dataset was donated to our archive by the Australian Energy Market Operator (AEMO) [58].
The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4659727.

## A.6.12 Wind farms dataset

This dataset contains very long minutely time series representing the wind power production of 339 wind farms in Australia.
This dataset is curated by us and note that the entire dataset is not publicly available elsewhere. The data are gathered from the AEMO online platform [58]. As the website does not enable extraction of historical data over longer time frames, the data has been gathered by us periodically over a period of one year from 01/08/2019 to 31/07/2020. The collected periodical data are aggregated to make all the series span over one year.
The collected data contain missing values where some series contain missing data for more than seven consecutive days. Our repository contains both the original version of the collected dataset and a version where the missing values have been replaced by zeros.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 4654909
- Dataset without missing values: http://doi.org/10.5281/zenodo. 4654858


## A.6.13 Car parts dataset

This dataset contains 2674 intermittent monthly time series showing car parts sales from January 1998 to March 2002. It was extracted from the R package expsmooth [59]. The package contains this dataset as "carparts". As the original dataset contains missing values, we include the original version of the dataset in the repository as well as a version where the missing values have been replaced with zeros, as the series are intermittent. Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 4656022
- Dataset without missing values: http://doi.org/10.5281/zenodo. 4656021


## A.6.14 Dominick dataset

This dataset contains 115704 weekly time series representing the profit of individual stock keeping units (SKU) from a retailer.
It was extracted from the Kilts Center, University of Chicago Booth School of Business online platform [61]. This platform also contains daily store-level sales data on more than 3500 products collected from Dominick's Finer Foods, a large American retail chain in the Chicago area, for approximately 9 years. The data are provided in different categories such as customer counts, store-specific demographics and sales products. Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]
- The value of competitive information in forecasting FMCG retail product sales and the variable selection problem [62]
- Beer snobs do exist: estimation of beer demand by type [63]
- Downsizing and supersizing: how changes in product attributes influence consumer preferences [64]
- Reference prices, costs, and nominal rigidities [65]

### Page 9
- Sales and monetary policy [66]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4654802.

# A.6.15 FRED-MD dataset 

This dataset contains 107 monthly time series showing a set of macro-economic indicators from the Federal Reserve Bank [67] starting from 01/01/1959. It was extracted from the FRED-MD database. The series are differenced and log-transformed as suggested in the literature. Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4654833.

## A.6.16 Bitcoin dataset

This dataset contains 18 daily time series showing the potential influencers of the bitcoin price such as transaction values and hash rate. Out of the 18 series, 2 series show the public opinion of bitcoins in the form of tweets and google searches mentioning the keyword, bitcoin.
The dataset has been curated by us by extracting the data from interactive web graphs available at BitInfoCharts [68] by using a Python script.
The collected data contain missing values. Our repository contains both the original version of the collected dataset and a version where the missing values have been replaced using the LOCF method.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo.5121965
- Dataset without missing values: http://doi.org/10.5281/zenodo.5122101


## A.6.17 San Francisco traffic dataset

This dataset contains 862 hourly time series showing the road occupancy rates on San Francisco Bay area freeways from 2015 to 2016. It was used by Lai et al. [1], and originally extracted from Caltrans [69]. Godahewa et al. [28] use a weekly aggregated version of this dataset, which is also available in our repository.
The DOI links to access and download the datasets are as follows:

- Hourly dataset: http://doi.org/10.5281/zenodo.4656132
- Weekly dataset: http://doi.org/10.5281/zenodo.4656135


## A.6.18 Melbourne pedestrian counts dataset

This dataset contains hourly pedestrian counts captured from 66 sensors in Melbourne city starting from May 2009 [70]. The original data are updated on a monthly basis when the new observations become available. The dataset in our repository contains pedestrian counts up to 30/04/2020. Research work which uses this dataset includes:

- Enhancing pedestrian mobility in smart cities using big data [71]
- Visualising Melbourne pedestrian count [72]
- PedaViz: visualising hour-level pedestrian activity [73]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656626.

## A.6.19 Rideshare dataset

This dataset contains 2304 hourly time series showing the attributes related to Uber and Lyft rideshare services such as price and distance for different locations in New York from 26/11/2018 to 18/12/2018.

### Page 10
We have curated the dataset by extracting the data from RaviMunde [74], and then aggregating attributes such as price and distance for a given hour, location, and service provider.
The collected data contain missing values. Our repository contains both the original version of the collected dataset and a version where the missing values have been replaced by zeros.

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo.5122114
- Dataset without missing values: http://doi.org/10.5281/zenodo.5122232


# A.6.20 Vehicle trips dataset 

This dataset contains 329 daily time series representing the number of trips and vehicles belonging to a set of for-hire vehicle (FHV) companies, extracted from fivethirtyeight [75].
The original dataset contains missing values. Our repository contains both the original version of the dataset and a version where the missing values have been replaced using the LOCF method.

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo.5122535
- Dataset without missing values: http://doi.org/10.5281/zenodo.5122537


## A.6.21 Hospital dataset

This dataset contains 767 monthly time series showing the patient counts related to medical products from January 2000 to December 2006. It was extracted from the R package expsmooth [59]. The package contains this dataset as "hospital". Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656014.

## A.6.22 COVID deaths dataset

This dataset contains 266 daily time series that represent the total COVID-19 deaths in a set of countries and states from 22/01/2020 to 20/08/2020. It was extracted from the Johns Hopkins repository [3, 76]. The original data are updated on a daily basis when the new observations become available.
The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656009.

## A.6.23 KDD cup 2018 dataset

This competition dataset contains long hourly time series representing the air quality levels in 59 stations in 2 cities, Beijing ( 35 stations) and London ( 24 stations) from 01/01/2017 to 31/03/2018 [77]. The dataset represents the air quality in multiple measurements such as $P M 2.5, P M 10, N O_{2}$, $C O, O_{3}$ and $S O_{2}$ levels.

Our repository dataset contains 270 hourly time series which have been categorized using city, station name, and air quality measurement.

As the original dataset contains missing values, we include both the original dataset and an imputed version in our repository. We impute leading missing values with zeros and the remaining missing values using the LOCF method. Research work which uses this dataset includes:

- AccuAir: winning solution to air quality prediction for KDD cup 2018 [78]

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo.4656719
- Dataset without missing values: http://doi.org/10.5281/zenodo.4656756

### Page 11
# A.6.24 Weather dataset 

This dataset contains 3010 daily time series of four weather variables: rain, minimum temperature, maximum temperature, and solar radiation, measured at weather stations in Australia. The series were extracted from the R package bomrang [79]. Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4654822.

## A.6.25 Temperature rain dataset

This dataset contains 32072 daily time series showing the temperature/rainfall observations and forecasts, gathered by the Australian Bureau of Meteorology [80, 81] for 422 weather stations across Australia, between 02/05/2015 and 26/04/2017.
We curated the dataset as follows. The data are originally extracted for 2 parts where one part contains data from 2015 to 2016 [80] and the other part contains data from 2016 to 2017 [81]. The two parts are merged and the temperature/rainfall observations are aggregated over 24 hour periods to construct daily series.
As the dataset has missing values, our repository contains both the original version of the curated dataset and a version where the missing values have been replaced by zeros.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo.5129073
- Dataset without missing values: http://doi.org/10.5281/zenodo.5129091


## A. 7 Single long time series datasets

This section describes the benchmark datasets which have single time series with a large amount of data points.

## A.7.1 Sunspot dataset

The original data source contains a single very long daily time series of sunspot numbers from 01/01/1818 until the present [82]. Furthermore, it also contains monthly mean total sunspot numbers (starting from 1749), 13-month smoothed monthly total sunspot numbers (starting from 1749), yearly mean total sunspot numbers (starting from 1700), daily hemispheric sunspot numbers (starting from 1992), monthly mean hemispheric sunspot numbers (starting from 1992), 13-month smoothed monthly hemispheric sunspot numbers (starting from 1992), and yearly mean total sunspot numbers (starting from 1610). The original datasets are updated as new observations become available.
Our repository contains the single daily time series representing the sunspot numbers from 08/01/1818 to 31/05/2020. As the dataset contains missing values, we include an LOCF-imputed version besides it in the repository. Research work which uses this dataset includes:

- Re-evaluation of predictive models in light of new data: sunspot number version 2.0 [83]
- Correlation between sunspot number and ca II K emission index [84]
- Dynamics of sunspot series on time scales from days to years: correlation of sunspot births, variable lifetimes, and evolution of the high-frequency spectral component [85]
- Long term sunspot cycle phase coherence with periodic phase disruptions [86]

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo.4654773
- Dataset without missing values: http://doi.org/10.5281/zenodo.4654722

### Page 12
# A.7.2 Saugeen river flow dataset 

This dataset contains a single very long time series representing the daily mean flow of the Saugeen River at Walkerton in cubic meters per second from 01/01/1915 to 31/12/1979. The length of this time series is 23,741 . It was extracted from the R package, deseasonalize [87]. The package contains this dataset as "SaugeenDay".

Research work which uses this dataset includes:

- Telescope: an automatic feature extraction and transformation approach for time series forecasting on a level-playing field [88]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656058.

## A.7.3 US births dataset

This dataset contains a single very long daily time series representing the number of births in the US from 01/01/1969 to 31/12/1988. The length of this time series is 7,305 . It was extracted from the R package, mosaicData [89]. The package contains this dataset as "Births". Research work which uses this dataset includes:

- Telescope: an automatic feature extraction and transformation approach for time series forecasting on a level-playing field [88]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656049.

## A.7.4 Solar power dataset

This dataset contains a single very long time series representing the solar power production of an Australian wind farm recorded per each 4 seconds starting from 01/08/2019. The length of this time series is $7,397,222$.

This dataset is curated by us as follows. The data are gathered from the AEMO online platform [58]. As the website does not enable extraction of historical data over longer time frames, the data has been gathered by us periodically where the collected periodical data are then aggregated to make the single long time series available in our repository.

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656027.

## A.7.5 Wind power dataset

This dataset contains a single very long time series representing the wind power production of an Australian wind farm recorded per each 4 seconds starting from 01/08/2019. The length of this time series is $7,397,147$. This dataset is also curated by us following the procedure explained in Section A.7.4.

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo.4656032.

### Page 13
# B Feature plots 

Figure 2 shows the normalised density values of the low-dimensional feature space generated by PCA for the datasets in our archive across 4 tsfeatures: ACF1, trend, entropy and seasonal strength, and the Box-Cox transformation parameter, lambda. The dark and light hexbins denote the high and low density areas, respectively.
![img-0.jpeg](img-0.jpeg)

Figure 2: Hexbin plots showing the normalised density values of the low-dimensional feature space generated by PCA across ACF1, trend, entropy, seasonal strength, and Box-Cox lambda.

### Page 14
![img-1.jpeg](img-1.jpeg)

Figure 2 (cont.): Hexbin plots showing the normalised density values of the low-dimensional feature space generated by PCA across ACF1, trend, entropy, seasonal strength, and Box-Cox lambda.

### Page 15
Figure 3 shows the normalised density values of the low-dimensional feature space generated by PCA for the datasets in our archive across the catch22 features. The dark and light hexbins denote the high and low density areas, respectively.
![img-2.jpeg](img-2.jpeg)

Figure 3: Hexbin plots showing the normalised density values of the low-dimensional feature space generated by PCA across catch22 features.

### Page 16
![img-3.jpeg](img-3.jpeg)

Figure 3 (cont.): Hexbin plots showing the normalised density values of the low-dimensional feature space generated by PCA across catch22 features.

### Page 17
# C Baseline results 

Equations 1, 2, 3, 4, and 5, respectively, show the formulas of MASE, sMAPE, modified sMAPE (msMAPE), MAE, and RMSE, where $M$ is the number of data points in the training series, $S$ is the seasonality of the dataset, $h$ is the forecast horizon, $F_{k}$ are the generated forecasts and $Y_{k}$ are the actual values. We set the parameter $\epsilon$ in Equation 3 to its proposed default of 0.1 .

$$
\begin{gathered}
M A S E=\frac{\sum_{k=M+1}^{M+h}\left|F_{k}-Y_{k}\right|}{\frac{h}{M-S} \sum_{k=S+1}^{M}\left|Y_{k}-Y_{k-S}\right|} \\
s M A P E=\frac{100 \%}{h} \sum_{k=1}^{h} \frac{\left|F_{k}-Y_{k}\right|}{\left(\left|Y_{k}\right|+\left|F_{k}\right|\right) / 2} \\
m s M A P E=\frac{100 \%}{h} \sum_{k=1}^{h} \frac{\left|F_{k}-Y_{k}\right|}{m a x\left(\left|Y_{k}\right|+\left|F_{k}\right|+\epsilon, 0.5+\epsilon\right) / 2} \\
M A E=\frac{\sum_{k=1}^{h}\left|F_{k}-Y_{k}\right|}{h} \\
R M S E=\sqrt{\frac{\sum_{k=1}^{h}\left|F_{k}-Y_{k}\right|^{2}}{h}}
\end{gathered}
$$

Tables 5, 6, 7, 8, 9, 10, 11, 12, 13 and 14, respectively show the mean MASE, median MASE, mean sMAPE, median sMAPE, mean msMAPE, median msMAPE, mean MAE, median MAE, mean RMSE and median RMSE results of SES, Theta, TBATS, ETS, ARIMA/DHR-ARIMA, PR, CatBoost, FFNN, DeepAR, N-BEATS, WaveNet and Transformer models on all datasets. The best model across each dataset is highlighted in boldface in all results tables. We use 2 versions of ARIMA. The results of the general ARIMA method are reported for yearly, quarterly, monthly, and daily datasets whereas the results of DHR-ARIMA are reported for weekly datasets and multi-seasonal datasets such as 10 minutely, half hourly, and hourly.
We note that the MASE values of the baselines are generally high on multi-seasonal datasets. For multi-seasonal datasets, we consider longer forecasting horizons corresponding to one week unless they are competition datasets. For multi-seasonal datasets, the MASE measures the performance of a model compared to the in-sample snaïve forecasts corresponding with the daily seasonality which uses the observations of the previous day as the forecasts. One would expect the MASE to lie between 0 and 1 , if a method on average outperforms the snaïve forecasts. However, the MASE values we report are often considerably larger than 1 for multi-seasonal datasets across all baselines, because the MASE compares the forecasts of longer horizons with the in-sample snaïve forecasts obtained using one day.
While methods can be optimised towards different measures and therewith perform better on some measures than others, we opt here to not change the loss functions from their defaults, and nonetheless use different error measures, as changing loss functions may be easy for some methods and very difficult for others in practice, so that practitioners can assess from our results how likely a method will work with a certain error measure in its default configuration.

### Page 18
![img-4.jpeg](img-4.jpeg)

### Page 19
![img-5.jpeg](img-5.jpeg)

### Page 20
![img-6.jpeg](img-6.jpeg)

### Page 21
![img-7.jpeg](img-7.jpeg)

### Page 22
![img-8.jpeg](img-8.jpeg)

### Page 23
![img-9.jpeg](img-9.jpeg)

### Page 24
![img-10.jpeg](img-10.jpeg)

### Page 25
![img-11.jpeg](img-11.jpeg)

### Page 26
![img-12.jpeg](img-12.jpeg)

### Page 27
![img-13.jpeg](img-13.jpeg)

### Page 28
# D Execution times 

Table 15 shows the execution times corresponding with the SES, Theta, TBATS, ETS, ARIMA/DHRARIMA, PR, CatBoost, FFNN, DeepAR, N-BEATS, WaveNet and Transformer models across all datasets. The times are rounded to their closest hours, minutes and seconds, accordingly.
The experiments are run on an Intel(R) Core(TM) i7-8700 processor (3.2GHz) and 65GB of main memory.

Table 15: Execution times of baseline models. The times are formatted as hhh:mm:ss where h, m, and s refer to hours, minutes, and seconds. Leading zeros are omitted.

| Dataset | SES | Theta | TBATS | ETS | (DHR-) <br> ARIMA | PR | Cat FFNN <br> Boost | Deep | N- | Wave | Trans |  |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
|  |  |  |  |  |  |  |  | AR |  |  | Net | former |
| M1 Yearly | 6 | 7 | 45 | 7 | 18 | 2 | 2 | 17 | 2:00 | 7:00 | 8:00 | 1:00 |
| M1 Quarterly | 7 | 7 | 3:00 | 29 | 57 | 3 | 3 | 18 | 3:00 | 7:00 | 8:00 | 1:00 |
| M1 Monthly | 20 | 22 | 13:00 | 6:00 | 22:00 | 8 | 7 | 22 | 5:00 | 8:00 | 20:00 | 2:00 |
| M3 Yearly | 23 | 23 | 3:00 | 27 | 55 | 9 | 6 | 18 | 2:00 | 7:00 | 7:00 | 1:00 |
| M3 Quarterly | 25 | 28 | 10:00 | 2:00 | 4:00 | 10 | 7 | 19 | 2:00 | 8:00 | 7:00 | 1:00 |
| M3 Monthly | 49 | 53 | 30:00 | 14:00 | 1:00:00 | 26 | 19 | 21 | 5:00 | 20:00 | 27:00 | 2:00 |
| M3 Other | 1 | 1 | 44 | 2 | 10 | 2 | 2 | 19 | 2:00 | 8:00 | 8:00 | 1:00 |
| M4 Yearly | 17:00 | 17:00 | 2:00:00 | 20:00 | 36:00 | 9:00 | 6:00 | - | - | - | - | - |
| M4 Quarterly | 22:00 | 24:00 | 8:00:00 | 1:00:00 | 4:00:00 | 31:00 | 21:00 | 23 | 4:00 | 36:00 | 39:00 | 4:00 |
| M4 Monthly | 2:00:00 | 2:00:00 | 24:00:00 | 11:00:00 | 48:00:00 | 6:00:00 | 5:00:00 | 34 | 11:00 | 2:00:00 | 3:00:00 | 18:00 |
| M4 Weekly | 16 | 17 | 1:00:00 | 32 | 4:00 | 14 | 51 | 25 | 9:00 | 8:00 | 31:00 | 4:00 |
| M4 Daily | 14:00 | 12:00 | 7:00:00 | 3:00:00 | 4:00:00 | 32:00 | 32:00 | 25 | 4:00 | 13:00 | 22:00 | 3:00 |
| M4 Hourly | 13 | 13 | 1:00:00 | 36 | 11 | 21 | 1:00 | 27 | 29:00 | 9:00 | 3:00:00 | 21:00 |
| Tourism Yearly | 18 | 19 | 2:00 | 21 | 46 | 6 | 5 | 14 | 2:00 | 7:00 | 5:00 | 1:00 |
| Tourism Quarterly | 15 | 17 | 12:00 | 1:00 | 7:00 | 6 | 5 | 16 | 1:00 | 17:00 | 6:00 | 1:00 |
| Tourism Monthly | 14 | 15 | 17:00 | 5:00 | 47:00 | 8 | 8 | 19 | 5:00 | 8:00 | 24:00 | 2:00 |
| CIF 2016 | 1 | 1 | 2:00 | 43 | 2:00 | 1 | 2 | 32 | 7:00 | 33:00 | 22:00 | 3:00 |
| Aus. Elecdemand | 11 | 29 | 7:00:00 | 47 | 8 | 7:00 | 4:00 | 6:00 | 44:00 | 14:00 | 12:00:00 | 2:00:00 |
| Dominick | 5:00:00 | 4:00:00 | 48:00:00 | 4:00:00 | 10:00:00 | 9:00:00 | 13:00:00 | 54 | 11:00 | 3:00:00 | 5:00:00 | 17:00 |
| Bitcoin | 1 | 1 | 6:00 | 1:00 | 21:00 | 1 | 4 | 21 | 2:00 | 7:00 | 47:00 | 3:00 |
| Pedestrian Counts | 12:00:00 | 11:00:00 | 24:00:00 | 2:00:00 | 11:00:00 | 7:00 | 8:00 | 1:00 | 20:00 | 13:00 | 3:00:00 | 18:00 |
| Vehicle Trips | 8 | 9 | 10:00 | 2:00 | 9:00 | 3 | 5 | 17 | 3:00 | 6:00 | 56:00 | 3:00 |
| KDD Cup | 2:00:00 | 2:00:00 | 8:00:00 | 1:00:00 | 2:00:00 | 10:00 | 11:00 | 54 | 29:00 | 12:00 | 5:00:00 | 40:00 |
| Weather | 18:00 | 19:00 | 24:00:00 | 7:00:00 | 24:00:00 | 56:00 | 1:00:00 | 38 | 6:00 | 15:00 | 43:00 | 5:00 |
| NN5 Daily | 3 | 3 | 5:00 | 48 | 30:00 | 5 | 5 | 25 | 8:00 | 7:00 | 58:00 | 4:00 |
| NN5 Weekly | 3 | 3 | 7:00 | 4 | 20 | 1 | 4 | 21 | 9:00 | 8:00 | 34:00 | 4:00 |
| Kaggle Daily | 96:00:00 | 96:00:00 | 240:00:00 | 120:00:00 | 168:00:00 |  |  |  |  |  |  |  |
| Kaggle Weekly | 13:00:00 | 14:00:00 | 120:00:00 | 15:00:00 | 17:00:00 | 24:00:00 | 24:00:00 | 1:00 | 10:00 | 3:00:00 | 6:00:00 | 20:00 |
| Solar 10 Minutes | 44 | 48 | 17:00:00 | 3:00 | 24 | 3:00 | 9:00 | 3:00 | 1:00:00 | 13:00 | - | 6:00:00 |
| Solar Weekly | 3 | 3 | 1:00 | 4 | 13 | 2 | 4 | 19 | 2:00 | 8:00 | 38:00 | 1:00 |
| Electricity Hourly | 2:00 | 3:00 | 24:00:00 | 5:00 | 1:00 | 6:00 | 9:00 | 58 | 24:00 | 12:00 | 5:00:00 | 18:00 |
| Electricity Weekly | 8 | 9 | 19:00 | 10 | 1:00 | 4 | 11 | 21 | 9:00 | 8:00 | 28:00 | 4:00 |
| Carparts | 2:00 | 2:00 | 20:00 | 10:00 | 20:00 | 38 | 41 | 21 | 4:00 | 12:00 | 16:00 | 2:00 |
| FRED-MD | 5 | 6 | 9:00 | 3:00 | 7:00 | 2 | 5 | 19 | 4:00 | 8:00 | 12:00 | 2:00 |
| Traffic Hourly | 6:00 | 6:00 | 48:00:00 | 17:00 | 5:00 | 28:00 | 27:00 | 1:00 | 25:00 | 12:00 | 6:00:00 | 24:00 |
| Traffic Weekly | 20 | 21 | 13:00 | 26 | 3:00 | 16 | 17 | 20 | 9:00 | 9:00 | 26:00 | 3:00 |
| Rideshare | 1:00 | 2:00 | 5:00:00 | 2:00 | 2:00 | 9:00 | 6:00 | 43 | 22:00 | 13:00 | 6:00:00 | 2:00:00 |
| Hospital | 26 | 27 | 13:00 | 8:00 | 20:00 | 10 | 8 | 18 | 4:00 | 16:00 | 11:00 | 2:00 |
| COVID Deaths | 6 | 7 | 3:00 | 39 | 44 | 2 | 13 | 21 | 5:00 | 10:00 | 26:00 | 2:00 |
| Temp. Rain | 4:00:00 | 4:00:00 | 16:00:00 | 7:00:00 | 8:00:00 | 7:00:00 | 5:00:00 | 35 | 10:00 | 48:00 | 4:00:00 | 23:00 |
| Sunspot | 1 | 1 | 2:00 | 15 | 4:00 | 30 | 3 | 2:00 | 10:00 | 13:00 | 24:00 | 5:00 |
| Saugern River Flow | 1 | 1 | 1:00 | 22 | 35 | 9 | 2 | 35 | 7:00 | 10:00 | 27:00 | 3:00 |
| US Births | 1 | 1 | 40 | 4 | 13 | 3 | 2 | 30 | 6:00 | 10:00 | 28:00 | 3:00 |

## References

[1] G. Lai, W.-C. Chang, Y. Yang, and H. Liu. Modeling long- and short-term temporal patterns with deep neural networks. In The 41st International ACM SIGIR Conference on Research and Development in Information Retrieval, page 95-104, New York, NY, USA, 2018.
[2] Kaggle. https://www.kaggle.com/, 2019.
[3] Center for Systems Science and Engineering at Johns Hopkins University. COVID-19 data repository. https://github.com/CSSEGISandData/COVID-19, 2020.
[4] S. Makridakis, A. Andersen, R. F. Carbone, R. Fildes, M. Hibon, R. Lewandowski, J. Newton, E. Parzen, and R. L. Winkler. The accuracy of extrapolation (time series) methods: results of a forecasting competition. Journal of Forecasting, 1(2):111-153, 1982.

### Page 29
[5] G. Zhang, B. E. Patuwo, and M. Y. Hu. Forecasting with artificial neural networks:: the state of the art. International Journal of Forecasting, 14(1):35-62, 1998.
[6] G. P. Zhang. Time series forecasting using a hybrid arima and neural network model. Neurocomputing, 50:159 - 175, 2003. ISSN 0925-2312.
[7] R. J. Hyndman and Y. Khandakar. Automatic time series forecasting: the forecast package for R. Journal of Statistical Software, 27(3):1-22, 2008. URL http://www.jstatsoft.org/ $\mathrm{v} 27 / \mathrm{i} 03$.
[8] E. S. Gardner. Exponential smoothing: the state of the art. Journal of Forecasting, 4(1):1-28, 1985.
[9] G. P. Zhang and M. Qi. Neural network forecasting for seasonal and trend time series. European Journal of Operational Research, 160(2):501 - 514, 2005. ISSN 0377-2217.
[10] S. Makridakis and M. Hibon. The M3-competition: results, conclusions and implications. International Journal of Forecasting, 16(4):451-476, 2000.
[11] V. Assimakopoulos and K. Nikolopoulos. The theta model: a decomposition approach to forecasting. International Journal of Forecasting, 16(4):521-530, 2000.
[12] H. Hewamalage, C. Bergmeir, and K. Bandara. Recurrent neural networks for time series forecasting: current status and future directions. International Journal of Forecasting, 37(1): $388-427,2021$.
[13] R. Godahewa, K. Bandara, G. I. Webb, S. Smyl, and C. Bergmeir. Ensembles of localised models for time series forecasting. Knowledge-Based Systems, 233:107518, 2021.
[14] L. J. Tashman. Out-of-sample tests of forecasting accuracy: an analysis and review. International Journal of Forecasting, 16(4):437 - 450, 2000. ISSN 0169-2070.
[15] A. Saxena, J. Celaya, E. Balaban, K. Goebel, B. Saha, S. Saha, and M. Schwabacher. Metrics for evaluating performance of prognostic techniques. In 2008 International Conference on Prognostics and Health Management, pages 1-17, 2008.
[16] D. M. Dunlavy, T. G. Kolda, and E. Acar. Temporal link prediction using matrix and tensor factorizations. ACM Trans. Knowl. Discov. Data, 5(2), February 2011. ISSN 1556-4681.
[17] A. M. De Livera, R. J. Hyndman, and R. D. Snyder. Forecasting time series with complex seasonal patterns using exponential smoothing. Journal of the American Statistical Association, 106(496):1513-1527, 2011.
[18] J. S. Armstrong. Evaluating Forecasting Methods, pages 443-472. Springer US, Boston, MA, 2001. ISBN 978-0-306-47630-3.
[19] J. W. Taylor. Exponential smoothing with a damped multiplicative trend. International Journal of Forecasting, 19(4):715-725, 2003.
[20] S. Makridakis, E. Spiliotis, and V. Assimakopoulos. The M4 competition: results, findings, conclusion and way forward. International Journal of Forecasting, 34(4):802-808, 2018.
[21] S. Makridakis, E. Spiliotis, and V. Assimakopoulos. The M4 competition: 100,000 time series and 61 forecasting methods. International Journal of Forecasting, 36(1):54 - 74, 2020. ISSN 0169-2070.
[22] Forecasting \& Strategy Unit. Foredeck. http://fsudataset.com/, 2019.
[23] S. Smyl. A hybrid method of exponential smoothing and recurrent neural networks for time series forecasting. International Journal of Forecasting, 36(1):75-85, 2020.
[24] P. Montero-Manso, G. Athanasopoulos, R. J. Hyndman, and T. S. Talagala. FFORMA: featurebased forecast model averaging. International Journal of Forecasting, 36(1):86-92, 2020.

### Page 30
[25] K. Bandara, C. Bergmeir, and H. Hewamalage. LSTM-MSNet: leveraging forecasts on sets of related time series with multiple seasonal patterns. IEEE Transactions on Neural Networks and Learning Systems, 32(4):1586-1599, 2021.
[26] E. Spiliotis, A. Kouloumos, V. Assimakopoulos, and S. Makridakis. Are forecasting competitions data representative of the reality? International Journal of Forecasting, 36(1):37 - 53, 2020. ISSN 0169-2070.
[27] R. L. Winkler, Y. Grushka-Cockayne, K. C. Lichtendahl, and V. R. R. Jose. Averaging probability forecasts: back to the future. 2018.
[28] R. Godahewa, C. Bergmeir, G. I. Webb, and P. Montero-Manso. A strong baseline for weekly time series forecasting. https://arxiv.org/abs/2010.08158, 2020.
[29] G. Athanasopoulos, R. J. Hyndman, H. Song, and D. C. Wu. The tourism forecasting competition. International Journal of Forecasting, 27(3):822-844, 2011.
[30] P. Ellis. Tcomp: data from the 2010 tourism forecasting competition. https://cran. r-project.org/web/packages/Tcomp, 2018.
[31] B. Peng, H. Song, and G. I. Crouch. A meta-analysis of international tourism demand forecasting and implications for practice. Tourism Management, 45:181 - 193, 2014. ISSN 0261-5177.
[32] N. Kourentzes, F. Petropoulos, and J. R. Trapero. Improving forecasting by estimating time series structural components across multiple frequencies. International Journal of Forecasting, 30(2):291 - 302, 2014. ISSN 0169-2070.
[33] H. Song, G. Li, S. F. Witt, and G. Athanasopoulos. Forecasting tourist arrivals using timevarying parameter structural time series models. International Journal of Forecasting, 27(3): 855 - 869, 2011. ISSN 0169-2070.
[34] M. Theodosiou. Forecasting monthly and quarterly time series using STL decomposition. International Journal of Forecasting, 27(4):1178 - 1195, 2011. ISSN 0169-2070.
[35] M. Akin. A novel approach to model selection in tourism demand modeling. Tourism Management, 48:64 - 72, 2015. ISSN 0261-5177.
[36] S. Ben Taieb, G. Bontempi, A. F. Atiya, and A. Sorjamaa. A review and comparison of strategies for multi-step ahead time series forecasting based on the NN5 forecasting competition. Expert Systems with Applications, 39(8):7067 - 7083, 2012.
[37] K. Bandara, C. Bergmeir, and S. Smyl. Forecasting across time series databases using recurrent neural networks on groups of similar series: a clustering approach. Expert Syst. Appl., 140: 112896, 2020. ISSN 0957-4174.
[38] R. R. Andrawis, A. F. Atiya, and H. El-Shishiny. Forecast combinations of computational intelligence and linear models for the NN5 time series forecasting competition. International Journal of Forecasting, 27(3):672 - 688, 2011. ISSN 0169-2070.
[39] J. D. Wichard. Forecasting the NN5 time series with hybrid models. International Journal of Forecasting, 27(3):700 - 707, 2011. ISSN 0169-2070.
[40] S. Ben Taieb, A. Sorjamaa, and G. Bontempi. Multiple-output modeling for multi-step-ahead time series forecasting. Neurocomputing, 73(10):1950 - 1957, 2010. ISSN 0925-2312.
[41] S. Ben Taieb and G. Bontempi. Recursive multi-step time series forecasting by perturbing data. In 2011 IEEE 11th International Conference on Data Mining, pages 695-704, 2011.
[42] U. Pritzsche. Benchmarking of Classical and Machine-Learning Algorithms (with special emphasis on Bagging and Boosting Approaches) for Time Series Forecasting. PhD thesis, 2015.
[43] M. Štěpnička and M. Burda. On the results and observations of the time series forecasting competition CIF 2016. In 2017 IEEE International Conference on Fuzzy Systems (FUZZ-IEEE), pages 1-6, 2017.

### Page 31
[44] T. M. Dantas and F. L. C. Oliveira. Improving time series forecasting: an approach combining bootstrap aggregation, clusters and exponential smoothing. International Journal of Forecasting, 34(4):748 - 761, 2018. ISSN 0169-2070.
[45] T. Afanasieva, N. Yarushkina, and I. Sibirev. Time series clustering using numerical and fuzzy representations. In 2017 Joint 17th World Congress of International Fuzzy Systems Association and 9th International Conference on Soft Computing and Intelligent Systems (IFSA-SCIS), pages 1-7, 2017.
[46] V. N. Coelho, I. M. Coelho, I. R. Meneghini, M. J. F. Souza, and F. G. Guimarães. An automatic calibration framework applied on a metaheuristic fuzzy model for the cif competition. In 2016 International Joint Conference on Neural Networks (IJCNN), pages 1507-1514, 2016.
[47] Google. Web traffic time series forecasting, 2017. URL https://www.kaggle.com/c/ web-traffic-time-series-forecasting.
[48] N. Petluri and E. Al-Masri. Web traffic prediction of wikipedia pages. In 2018 IEEE International Conference on Big Data (Big Data), pages 5427-5429, 2018.
[49] M. Gupta, A. Asthana, N. Joshi, and P. Mehndiratta. Improving time series forecasting using mathematical and deep learning models. In A. Mondal, H. Gupta, J. Srivastava, P. K. Reddy, and D. V. L. N. Somayajulu, editors, Big Data Analytics, pages 115-125, Cham, 2018. Springer International Publishing. ISBN 978-3-030-04780-1.
[50] Z. Mariet and V. Kuznetsov. Foundations of sequence-to-sequence modeling for time series. In K. Chaudhuri and M. Sugiyama, editors, Proceedings of Machine Learning Research, volume 89 of Proceedings of Machine Learning Research, pages 408-417. PMLR, April 2019.
[51] Solar. Solar power data for integration studies, national renewable energy laboratory, 2020. URL https://www.nrel.gov/grid/solar-power-data.html.
[52] UCI. Electricityloaddiagrams20112014 data set, UCI machine learning repository, 2020. URL https://archive.ics.uci.edu/ml/datasets/ElectricityLoadDiagrams20112014.
[53] D. Jean-Michel. Smart meter data from London area, 2019. URL https://www.kaggle.com/ jeanmidev/smart-meters-in-london.
[54] A. Nugaliyadde, U. V. Somaratne, and K. W. Wong. Predicting electricity consumption using deep recurrent neural networks. ArXiv, abs/1909.08182, 2019.
[55] A. M. Alonso, F. J. Nogales, and C. Ruiz. A single scalable lstm model for short-term forecasting of disaggregated electricity loads. ArXiv, abs/1910.06640, 2019.
[56] M. Maksut, A. Karbozov, M. Myrzaliyeva, H. S. V. S. K. Nunna, P. K. Jamwal, and S. Doolla. Deep learning based short- term load forecasting for urban areas. In 2019 IEEE Industry Applications Society Annual Meeting, pages 1-6, 2019.
[57] D. Kaur, R. Kumar, N. Kumar, and M. Guizani. Smart grid energy management using RNNLSTM: a deep learning-based approach. In 2019 IEEE Global Communications Conference (GLOBECOM), pages 1-6, 2019.
[58] AEMO. Market data nemweb. http://www.nemweb.com.au/, 2020.
[59] R. J. Hyndman. expsmooth: data sets from forecasting with exponential smoothing. https: //cran.r-project.org/web/packages/expsmooth, 2015.
[60] P. Montero-Manso and R. J. Hyndman. Principles and algorithms for forecasting groups of time series: locality and globality. International Journal of Forecasting, 37(4):1632-1653, 2021.
[61] James M. Kilts Center. Dominick's dataset. https://www.chicagobooth.edu/research/ kilts/datasets/dominicks, 2020.
[62] T. Huang, R. Fildes, and D. Soopramanien. The value of competitive information in forecasting fmcg retail product sales and the variable selection problem. European Journal of Operational Research, 237(2):738 - 748, 2014. ISSN 0377-2217.

### Page 32
[63] D. Toro-González, J. J. McCluskey, and R. Mittelhammer. Beer snobs do exist: estimation of beer demand by type. Journal of Agricultural and Resource Economics, 39(2):174-187, 2014.
[64] A. Jami and H. Mishra. Downsizing and supersizing: how changes in product attributes influence consumer preferences. Journal of Behavioral Decision Making, 27(4):301-315, January 2014. ISSN 0894-3257.
[65] M. Eichenbaum, N. Jaimovich, and S. Rebelo. Reference prices, costs, and nominal rigidities. American Economic Review, 101(1):234-262, February 2011.
[66] B. Guimaraes and K. D. Sheedy. Sales and monetary policy. American Economic Review, 101 (2):844-76, April 2011.
[67] M. W. McCracken and S. Ng. FRED-MD: a monthly database for macroeconomic research. Journal of Business and Economic Statistics, 34(4):574-589, 2016.
[68] BitInfoCharts. Cryptocurrency statistics, 2021. URL https://bitinfocharts.com.
[69] Caltrans. Caltrans performance measurement system, California department of transportation, 2020. URL http://pems.dot.ca.gov.
[70] City of Melbourne. Pedestrian counting system - 2009 to present (counts per hour), 2017. URL https://data.melbourne.vic.gov.au/Transport/ Pedestrian-Counting-System-2009-to-Present-counts-/b2ak-trbp.
[71] E. Carter, P. Adam, D. Tsakis, S. Shaw, R. Watson, and P. Ryan. Enhancing pedestrian mobility in smart cities using big data. Journal of Management Analytics, 7(2):173-188, 2020.
[72] H. O. Obie, C. Chua, I. Avazpour, M. Abdelrazek, and J. Grundy. Visualising melbourne pedestrian count. In 2017 IEEE Symposium on Visual Languages and Human-Centric Computing (VL/HCC), pages 343-344, 2017.
[73] H. O. Obie, C. Chua, I. Avazpour, M. Abdelrazek, J. Grundy, and T. Bednarz. Pedaviz: visualising hour-level pedestrian activity. In Proceedings of the 11th International Symposium on Visual Information Communication and Interaction, VINCI '18, page 9-16, New York, NY, USA, 2018. Association for Computing Machinery. ISBN 9781450365017.
[74] RaviMunde. Uber \& lyft cab prices, 2019. URL https://www.kaggle.com/ravi72munde/ uber-lyft-cab-prices.
[75] fivethirtyeight. Uber TLC FOIL response, 2015. URL https://github.com/ fivethirtyeight/uber-tlc-foil-response.
[76] E. Dong, H. Du., and L. Gardner. An interactive web-based dashboard to track COVID-19 in real time. Lancet Inf Dis., 20(5):533-534, 2020.
[77] KDD2018. Kdd cup 2018, 2018. URL https://www.kdd.org/kdd2018/kdd-cup.
[78] Z. Luo, J. Huang, K. Hu, X. Li, and P. Zhang. AccuAir: winning solution to air quality prediction for kdd cup 2018. In Proceedings of the 25th ACM SIGKDD International Conference on Knowledge Discovery and Data Mining, KDD '19, page 1842-1850, New York, NY, USA, 2019. Association for Computing Machinery. ISBN 9781450362016.
[79] A. H. Sparks, J. Carroll, J. Goldie, D. Marchiori, P. Melloy, M. Padgham, H. Parsonage, and K. Pembleton. bomrang: Australian Government Bureau of Meteorology (BOM) Data Client, 2020. URL https://CRAN.R-project.org/package=bomrang.
[80] Australian Government. Historical rainfall and temperature forecast and observations hourly data - weather forecasting verification data (201505 to 2016-04), 2016. URL https://data.gov.au/data/dataset/ weather-forecasting-verification-data-2015-05-to-2016-04.
[81] Australian Government. Rainfall and temperature forecast and observations - verification 2016-05 to 2017-04, 2017.

### Page 33
[82] Sunspot. Sunspot number version 2.0: new data and conventions, 2015. URL http://www. sidc.be/silso/newdataset.
[83] A. Gkana and L. Zachilas. Re-evaluation of predictive models in light of new data: sunspot number version 2.0. Solar Physics, 291, August 2016.
[84] L. Bertello, A. Pevtsov, A. Tlatov, and J. Singh. Correlation between sunspot number and ca ii k emission index. Solar Physics, 291, June 2016.
[85] A. Shapoval, J. Le Mouel, M. Shnirman, and V. Courtillot. Dynamics of sunspot series on time scales from days to years: correlation of sunspot births, variable lifetimes, and evolution of the high-frequency spectral component. Journal of Geophysical Research: Space Physics, 122, December 2017.
[86] G. Pease and G. Glenn. Long term sunspot cycle phase coherence with periodic phase disruptions. October 2016.
[87] A. I. McLeod and H. Gweon. Optimal deseasonalization for monthly and daily geophysical time series. Journal of Environmental Statistics, 4(11), 2013. URL http://www.jenvstat. org/v04/i11.
[88] A. Bauer, M. Züfle, N. Herbst, S. Kounev, and V. Curtef. Telescope: an automatic feature extraction and transformation approach for time series forecasting on a level-playing field. In 2020 IEEE 36th International Conference on Data Engineering (ICDE), pages 1902-1905, 2020.
[89] R. Pruim, D. Kaplan, and N. Horton. mosaicData: project MOSAIC Data Sets, 2020. URL https://CRAN.R-project.org/package=mosaicData.