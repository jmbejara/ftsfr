### Page 1
# Appendix <br> Monash Time Series Forecasting Archive 

Rakshitha Godahewa<br>Monash University<br>Melbourne, Australia<br>rakshitha.godahewa@monash.edu

## Christoph Bergmeir

Monash University
Melbourne, Australia
christoph.bergmeir@monash.edu

Geoffrey I. Webb
Monash University
Melbourne, Australia
geoff.webb@monash.edu

Rob J. Hyndman
Monash University
Melbourne, Australia
rob.hyndman@monash.edu

Pablo Montero-Manso
University of Sydney
Australia
pmontm@gmail.com

## A Data records

Our archive contains 30 time series datasets. Out of these, 25 datasets contain multiple related time series to facilitate the evaluation of global time series forecasting models (Section A.6). The remaining 5 datasets contain single very long time series (Section A.7).

## A. 1 Data collection procedure

Out of the 30 datasets, 23 were already publicly available in different platforms with different data formats. The original sources of all datasets are mentioned in the datasets descriptions (Sections A. 6 and A.7). Out of these 23 datasets, 8 originate from competition platforms, 3 from research conducted by Lai et al. [1], 5 are taken from R packages, 1 is from the Kaggle platform [2], and 1 is taken from a Johns Hopkins repository [3] whereas the other datasets have been extracted from corresponding domain specific platforms. The remaining 7 datasets were manually curated by us as explained in Sections A.6.11, A.6.12, A.6.16, A.6.19, A.6.25, A.7.4 and A.7.5.

After extracting and curating these datasets, we analysed them individually to identify the datasets containing series with different frequencies and missing observations. Nine datasets contain time series belonging to different frequencies and the archive contains a separate dataset per each frequency. Eleven of the datasets have series with missing values. The archive contains 2 versions of each of these, one with and one without missing values. In the latter case, the missing values have been replaced by using an appropriate imputation technique as explained in Sections A. 6 and A.7. Finally, we obtain 58 datasets with the above explained different versions.

The 58 datasets are then converted to .tsf format which is a new format we introduce to store time series datasets as explained in Section 2.1 of the main paper. An example of series in this format is shown in Figure 1. The .tsf files are zipped and uploaded into our datasets archive available at https : //zenodo.org/communities/forecasting where other researchers can directly download them for further research use. Code to load the datasets in .tsf format into R and Python is available in our github repository at https://github.com/rakshitha123/TSForecasting.

## A. 2 Intended use of datasets

All datasets in our repository are intended for research purposes and to evaluate the performance of new forecasting algorithms.

### Page 2
\# Dataset Information
\# This dataset was used in the NN5 forecasting competition.
\# It contains 111 daily time series from the banking domain.
\# The goal is predicting the daily cash withdrawals from ATMs in UK.
\#
\# For more details, please refer to
\# Ben Taieb, S., Bontempi, G., Atiya, A.F., Sorjamaa, A., 2012.
\# A review and comparison of strategies for multi-step ahead time series forecasting based on
\# the nn5 forecasting competition. Expert Systems with Applications 39(8), 7067 - 7083
\#
\# Neural Forecasting Competitions, 2008.
\# NN5 forecasting competition for artificial neural networks and computational intelligence.
\# Accessed: 2020-05-10. URL http://www.neural-forecasting-competition.com/NN5/
\#
@relation NN5
@attribute series_name string
@attribute start_timestamp date
@frequency daily
@horizon 06
@missing true
@equallength true
@data
T1:1996-03-18 00-00-00:13.4070294784581,14.7250566893424,20.5640589569161,34.7080498866213,26. T2:1996-03-18 00-00-00:11.5504535147392,13.5912698412698,15.0368480725624,21.5702947845805,19. T3:1996-03-18 00-00-00:15.640589569161,14.3990929705215,24.4189342403628,28.7840136054422,20.62 T4:1996-03-18 00-00-00:13.1802721088435,8.44671201814059,19.515306122449,28.8832199546485,19.6 T5:1996-03-18 00-00-00:19.77891156462585,10.8134920634921,21.6128117913832,38.5204081632653,24. T6:1996-03-18 00-00-00:19.24036281179130,11.6354875283447,12.1031746031746,21.4143990929705,24. T7:1996-03-18 00-00-00:14.937641723356,16.2840136054422,16.6666666666667,23.5685941043084,26.7 T8:1996-03-18 00-00-00:12.89115646258503,12.3582766439909,16.3832199546485,30.1587301587302,31. T9:1996-03-18 00-00-00:17.34126984126984,9.15532879818594,10.5867346938776,12.5,7.1570294784585 T10:1996-03-18 00-00-00:10.2891156462585,12.7125850340136,14.4416099773243,19.4019274376417,23
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

The M1 competition dataset [4] contains 1001 time series with 3 different frequencies: yearly, quarterly, and monthly as shown in Table 1. The series belong to 7 different domains: macro 1, macro 2, micro 1, micro 2, micro 3, industry, and demographic.

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
- LSTM-MSNet: leveraging forecasts on sets of related time series with multiple seasonal patterns [25]

### Page 5
- Are forecasting competitions data representative of the reality? [26]
- Averaging probability forecasts: back to the future [27]
- A strong baseline for weekly time series forecasting [28]

The DOI links to access and download the datasets are as follows:

- Yearly dataset: http://doi.org/10.5281/zenodo. 4656379
- Quarterly dataset: http://doi.org/10.5281/zenodo. 4656410
- Monthly dataset: http://doi.org/10.5281/zenodo. 4656480
- Weekly dataset: http://doi.org/10.5281/zenodo. 4656522
- Daily dataset: http://doi.org/10.5281/zenodo. 4656548
- Hourly dataset: http://doi.org/10.5281/zenodo. 4656589


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

- Yearly dataset: http://doi.org/10.5281/zenodo. 4656103
- Quarterly dataset: http://doi.org/10.5281/zenodo. 4656093
- Monthly dataset: http://doi.org/10.5281/zenodo. 4656096


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

- Daily dataset with missing values: http://doi.org/10.5281/zenodo. 4656110
- Daily dataset without missing values: http://doi.org/10.5281/zenodo. 4656117
- Weekly dataset: http://doi.org/10.5281/zenodo. 4656125


# A.6.6 CIF 2016 dataset 

The dataset from the Computational Intelligence in Forecasting (CIF) 2016 forecasting competition contains 72 monthly time series. Out of those, 24 series originate from the banking sector, and the remaining 48 series are artificially generated. There are 2 forecast horizons considered in the competition where 57 series have a forecasting horizon of 12 and the remaining 15 series consider the forecast horizon as 6 [43]. Research work which uses this dataset includes:

- Recurrent neural networks for time series forecasting: current status and future directions [12]
- Ensembles of localised models for time series forecasting [13]
- Forecasting across time series databases using recurrent neural networks on groups of similar series: a clustering approach [37]
- Improving time series forecasting: an approach combining bootstrap aggregation, clusters and exponential smoothing [44]
- Time series clustering using numerical and fuzzy representations [45]
- An automatic calibration framework applied on a metaheuristic fuzzy model for the CIF competition [46]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656042.

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

- Daily dataset with missing values: http://doi.org/10.5281/zenodo. 4656080
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
The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4659727.

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

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4654802.

# A.6.15 FRED-MD dataset 

This dataset contains 107 monthly time series showing a set of macro-economic indicators from the Federal Reserve Bank [67] starting from 01/01/1959. It was extracted from the FRED-MD database. The series are differenced and log-transformed as suggested in the literature. Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4654833.

## A.6.16 Bitcoin dataset

This dataset contains 18 daily time series showing the potential influencers of the bitcoin price such as transaction values and hash rate. Out of the 18 series, 2 series show the public opinion of bitcoins in the form of tweets and google searches mentioning the keyword, bitcoin.
The dataset has been curated by us by extracting the data from interactive web graphs available at BitInfoCharts [68] by using a Python script.
The collected data contain missing values. Our repository contains both the original version of the collected dataset and a version where the missing values have been replaced using the LOCF method.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 5121965
- Dataset without missing values: http://doi.org/10.5281/zenodo. 5122101


## A.6.17 San Francisco traffic dataset

This dataset contains 862 hourly time series showing the road occupancy rates on San Francisco Bay area freeways from 2015 to 2016. It was used by Lai et al. [1], and originally extracted from Caltrans [69]. Godahewa et al. [28] use a weekly aggregated version of this dataset, which is also available in our repository.
The DOI links to access and download the datasets are as follows:

- Hourly dataset: http://doi.org/10.5281/zenodo. 4656132
- Weekly dataset: http://doi.org/10.5281/zenodo. 4656135


## A.6.18 Melbourne pedestrian counts dataset

This dataset contains hourly pedestrian counts captured from 66 sensors in Melbourne city starting from May 2009 [70]. The original data are updated on a monthly basis when the new observations become available. The dataset in our repository contains pedestrian counts up to 30/04/2020. Research work which uses this dataset includes:

- Enhancing pedestrian mobility in smart cities using big data [71]
- Visualising Melbourne pedestrian count [72]
- PedaViz: visualising hour-level pedestrian activity [73]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656626.

## A.6.19 Rideshare dataset

This dataset contains 2304 hourly time series showing the attributes related to Uber and Lyft rideshare services such as price and distance for different locations in New York from 26/11/2018 to 18/12/2018.

### Page 10
We have curated the dataset by extracting the data from RaviMunde [74], and then aggregating attributes such as price and distance for a given hour, location, and service provider.
The collected data contain missing values. Our repository contains both the original version of the collected dataset and a version where the missing values have been replaced by zeros.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 5122114
- Dataset without missing values: http://doi.org/10.5281/zenodo. 5122232


# A.6.20 Vehicle trips dataset 

This dataset contains 329 daily time series representing the number of trips and vehicles belonging to a set of for-hire vehicle (FHV) companies, extracted from fivethirtyeight [75].
The original dataset contains missing values. Our repository contains both the original version of the dataset and a version where the missing values have been replaced using the LOCF method.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 5122535
- Dataset without missing values: http://doi.org/10.5281/zenodo. 5122537


## A.6.21 Hospital dataset

This dataset contains 767 monthly time series showing the patient counts related to medical products from January 2000 to December 2006. It was extracted from the R package expsmooth [59]. The package contains this dataset as "hospital". Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656014.

## A.6.22 COVID deaths dataset

This dataset contains 266 daily time series that represent the total COVID-19 deaths in a set of countries and states from 22/01/2020 to 20/08/2020. It was extracted from the Johns Hopkins repository $[3,76]$. The original data are updated on a daily basis when the new observations become available.
The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656009.

## A.6.23 KDD cup 2018 dataset

This competition dataset contains long hourly time series representing the air quality levels in 59 stations in 2 cities, Beijing ( 35 stations) and London ( 24 stations) from 01/01/2017 to 31/03/2018 [77]. The dataset represents the air quality in multiple measurements such as $P M 2.5, P M 10, N O_{2}$, $C O, O_{3}$ and $S O_{2}$ levels.
Our repository dataset contains 270 hourly time series which have been categorized using city, station name, and air quality measurement.
As the original dataset contains missing values, we include both the original dataset and an imputed version in our repository. We impute leading missing values with zeros and the remaining missing values using the LOCF method. Research work which uses this dataset includes:

- AccuAir: winning solution to air quality prediction for KDD cup 2018 [78]

The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 4656719
- Dataset without missing values: http://doi.org/10.5281/zenodo. 4656756

### Page 11
# A.6.24 Weather dataset 

This dataset contains 3010 daily time series of four weather variables: rain, minimum temperature, maximum temperature, and solar radiation, measured at weather stations in Australia. The series were extracted from the R package bomrang [79]. Research work which uses this dataset includes:

- Principles and algorithms for forecasting groups of time series: locality and globality [60]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4654822.

## A.6.25 Temperature rain dataset

This dataset contains 32072 daily time series showing the temperature/rainfall observations and forecasts, gathered by the Australian Bureau of Meteorology [80, 81] for 422 weather stations across Australia, between 02/05/2015 and 26/04/2017.
We curated the dataset as follows. The data are originally extracted for 2 parts where one part contains data from 2015 to 2016 [80] and the other part contains data from 2016 to 2017 [81]. The two parts are merged and the temperature/rainfall observations are aggregated over 24 hour periods to construct daily series.
As the dataset has missing values, our repository contains both the original version of the curated dataset and a version where the missing values have been replaced by zeros.
The DOI links to access and download the datasets are as follows:

- Dataset with missing values: http://doi.org/10.5281/zenodo. 5129073
- Dataset without missing values: http://doi.org/10.5281/zenodo. 5129091


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

- Dataset with missing values: http://doi.org/10.5281/zenodo. 4654773
- Dataset without missing values: http://doi.org/10.5281/zenodo. 4654722

### Page 12
# A.7.2 Saugeen river flow dataset 

This dataset contains a single very long time series representing the daily mean flow of the Saugeen River at Walkerton in cubic meters per second from 01/01/1915 to 31/12/1979. The length of this time series is 23,741 . It was extracted from the R package, deseasonalize [87]. The package contains this dataset as "SaugeenDay".

Research work which uses this dataset includes:

- Telescope: an automatic feature extraction and transformation approach for time series forecasting on a level-playing field [88]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656058.

## A.7.3 US births dataset

This dataset contains a single very long daily time series representing the number of births in the US from 01/01/1969 to 31/12/1988. The length of this time series is 7,305 . It was extracted from the R package, mosaicData [89]. The package contains this dataset as "Births". Research work which uses this dataset includes:

- Telescope: an automatic feature extraction and transformation approach for time series forecasting on a level-playing field [88]

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656049.

## A.7.4 Solar power dataset

This dataset contains a single very long time series representing the solar power production of an Australian wind farm recorded per each 4 seconds starting from 01/08/2019. The length of this time series is $7,397,222$.

This dataset is curated by us as follows. The data are gathered from the AEMO online platform [58]. As the website does not enable extraction of historical data over longer time frames, the data has been gathered by us periodically where the collected periodical data are then aggregated to make the single long time series available in our repository.
The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656027.

## A.7.5 Wind power dataset

This dataset contains a single very long time series representing the wind power production of an Australian wind farm recorded per each 4 seconds starting from 01/08/2019. The length of this time series is $7,397,147$. This dataset is also curated by us following the procedure explained in Section A.7.4.

The DOI link to access and download the dataset is http://doi.org/10.5281/zenodo. 4656032.

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
m s M A P E=\frac{100 \%}{h} \sum_{k=1}^{h} \frac{\left|F_{k}-Y_{k}\right|}{\max \left(\left|Y_{k}\right|+\left|F_{k}\right|+\epsilon, 0.5+\epsilon\right) / 2} \\
M A E=\frac{\sum_{k=1}^{h}\left|F_{k}-Y_{k}\right|}{h} \\
R M S E=\sqrt{\frac{\sum_{k=1}^{h}\left|F_{k}-Y_{k}\right|^{2}}{h}}
\end{gathered}
$$

Tables 5, 6, 7, 8, 9, 10, 11, 12, 13 and 14, respectively show the mean MASE, median MASE, mean sMAPE, median sMAPE, mean msMAPE, median msMAPE, mean MAE, median MAE, mean RMSE and median RMSE results of SES, Theta, TBATS, ETS, ARIMA/DHR-ARIMA, PR, CatBoost, FFNN, DeepAR, N-BEATS, WaveNet and Transformer models on all datasets. The best model across each dataset is highlighted in boldface in all results tables. We use 2 versions of ARIMA. The results of the general ARIMA method are reported for yearly, quarterly, monthly, and daily datasets whereas the results of DHR-ARIMA are reported for weekly datasets and multi-seasonal datasets such as 10 minutely, half hourly, and hourly.
We note that the MASE values of the baselines are generally high on multi-seasonal datasets. For multi-seasonal datasets, we consider longer forecasting horizons corresponding to one week unless they are competition datasets. For multi-seasonal datasets, the MASE measures the performance of a model compared to the in-sample snaïve forecasts corresponding with the daily seasonality which uses the observations of the previous day as the forecasts. One would expect the MASE to lie between 0 and 1, if a method on average outperforms the snave forecasts. However, the MASE values we report are often considerably larger than 1 for multi-seasonal datasets across all baselines, because the MASE compares the forecasts of longer horizons with the in-sample snalve forecasts obtained using one day.
While methods can be optimised towards different measures and therewith perform better on some measures than others, we opt here to not change the loss functions from their defaults, and nonetheless use different error measures, as changing loss functions may be easy for some methods and very difficult for others in practice, so that practitioners can assess from our results how likely a method will work with a certain error measure in its default configuration.

### Page 18
Table 5: Mean MASE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 4.938 | 4.191 | 3.499 | 3.771 | 4.479 | 4.588 | 4.427 | 4.355 | 4.603 | 4.384 | 4.666 | 5.519  |
|  M1 Quarterly | 1.929 | 1.702 | 1.694 | 1.658 | 1.787 | 1.892 | 2.031 | 1.862 | 1.833 | 1.788 | 1.700 | 2.772  |
|  M1 Monthly | 1.379 | 1.091 | 1.118 | 1.074 | 1.164 | 1.123 | 1.209 | 1.205 | 1.192 | 1.168 | 1.200 | 2.191  |
|  M3 Yearly | 3.167 | 2.774 | 3.127 | 2.860 | 3.417 | 3.223 | 3.788 | 3.399 | 3.508 | 2.961 | 3.014 | 3.003  |
|  M3 Quarterly | 1.417 | 1.117 | 1.256 | 1.170 | 1.240 | 1.248 | 1.441 | 1.329 | 1.310 | 1.182 | 1.290 | 2.452  |
|  M3 Monthly | 1.091 | 0.864 | 0.861 | 0.865 | 0.873 | 1.010 | 1.065 | 1.011 | 1.167 | 0.934 | 1.008 | 1.454  |
|  M3 Other | 3.089 | 2.271 | 1.848 | 1.814 | 1.831 | 2.655 | 3.178 | 2.615 | 2.975 | 2.390 | 2.127 | 2.781  |
|  M4 Yearly | 3.981 | 3.375 | 3.437 | 3.444 | 3.876 | 3.625 | 3.649 | - | - | - | - | -  |
|  M4 Quarterly | 1.417 | 1.231 | 1.186 | 1.161 | 1.228 | 1.316 | 1.338 | 1.420 | 1.274 | 1.239 | 1.242 | 1.520  |
|  M4 Monthly | 1.150 | 0.970 | 1.053 | 0.948 | 0.962 | 1.080 | 1.093 | 1.151 | 1.163 | 1.026 | 1.160 | 2.125  |
|  M4 Weekly | 0.587 | 0.546 | 0.504 | 0.575 | 0.550 | 0.481 | 0.615 | 0.545 | 0.586 | 0.453 | 0.587 | 0.695  |
|  M4 Daily | 1.154 | 1.153 | 1.157 | 1.239 | 1.179 | 1.162 | 1.593 | 1.141 | 2.212 | 1.218 | 1.157 | 1.377  |
|  M4 Hourly | 11.607 | 11.524 | 2.663 | 26.690 | 13.557 | 1.662 | 1.771 | 2.862 | 2.145 | 2.247 | 1.680 | 8.840  |
|  Tourism Yearly | 3.253 | 3.015 | 3.085 | 3.395 | 3.775 | 3.516 | 3.553 | 3.401 | 3.205 | 2.977 | 3.624 | 3.552  |
|  Tourism Quarterly | 3.210 | 1.661 | 1.835 | 1.592 | 1.782 | 1.643 | 1.793 | 1.678 | 1.597 | 1.475 | 1.714 | 1.859  |
|  Tourism Monthly | 3.306 | 1.649 | 1.751 | 1.526 | 1.589 | 1.678 | 1.699 | 1.382 | 1.409 | 1.574 | 1.482 | 1.571  |
|  CIF 2016 | 1.291 | 0.997 | 0.861 | 0.841 | 0.929 | 1.019 | 1.175 | 1.053 | 1.159 | 0.971 | 1.800 | 1.173  |
|  Aus. Elecdemand | 1.857 | 1.867 | 1.174 | 5.663 | 2.574 | 0.780 | 0.705 | 1.222 | 1.591 | 1.014 | 1.102 | 1.113  |
|  Dominick | 0.582 | 0.610 | 0.722 | 0.595 | 0.796 | 0.980 | 1.038 | 0.614 | 0.540 | 0.952 | 0.531 | 0.531  |
|  Bitcoin | 4.327 | 4.344 | 4.611 | 2.718 | 4.030 | 2.664 | 2.888 | 6.006 | 6.394 | 7.254 | 5.315 | 8.462  |
|  Pedestrians | 0.957 | 0.958 | 1.297 | 1.190 | 3.947 | 0.256 | 0.262 | 0.267 | 0.272 | 0.380 | 0.247 | 0.274  |
|  Vehicle Trips | 1.224 | 1.244 | 1.860 | 1.305 | 1.282 | 1.212 | 1.176 | 1.843 | 1.929 | 2.143 | 1.851 | 2.532  |
|  KDD | 1.645 | 1.646 | 1.394 | 1.787 | 1.982 | 1.265 | 1.233 | 1.228 | 1.699 | 1.600 | 1.185 | 1.696  |
|  Weather | 0.677 | 0.749 | 0.689 | 0.702 | 0.746 | 3.046 | 0.762 | 0.638 | 0.631 | 0.717 | 0.721 | 0.650  |
|  NN5 Daily | 1.521 | 0.885 | 0.858 | 0.865 | 1.013 | 1.263 | 0.973 | 0.941 | 0.919 | 1.134 | 0.916 | 0.958  |
|  NN5 Weekly | 0.903 | 0.885 | 0.872 | 0.911 | 0.887 | 0.854 | 0.853 | 0.850 | 0.863 | 0.808 | 1.123 | 1.141  |
|  Kaggle Daily | 0.924 | 0.928 | 0.947 | 1.231 | 0.890 | - | - | - | - | - | - | -  |
|  Kaggle Weekly | 0.698 | 0.694 | 0.622 | 0.770 | 0.815 | 1.021 | 1.928 | 0.689 | 0.758 | 0.667 | 0.628 | 0.888  |
|  Solar 10 Mins | 1.451 | 1.452 | 3.936 | 1.451 | 1.034 | 1.451 | 2.504 | 1.450 | 1.450 | 1.573 | - | 1.451  |
|  Solar Weekly | 1.215 | 1.224 | 0.916 | 1.134 | 0.848 | 1.053 | 1.530 | 1.045 | 0.725 | 1.184 | 1.961 | 0.574  |
|  Electricity Hourly | 4.544 | 4.545 | 3.690 | 6.501 | 4.602 | 2.912 | 2.262 | 3.200 | 2.516 | 1.968 | 1.606 | 2.522  |
|  Electricity Weekly | 1.536 | 1.476 | 0.792 | 1.526 | 0.878 | 0.916 | 0.815 | 0.769 | 1.005 | 0.800 | 1.250 | 1.770  |
|  Carparts | 0.897 | 0.914 | 0.998 | 0.925 | 0.926 | 0.755 | 0.853 | 0.747 | 0.747 | 2.836 | 0.754 | 0.746  |
|  FRED-MD | 0.617 | 0.698 | 0.502 | 0.468 | 0.533 | 8.827 | 0.947 | 0.601 | 0.640 | 0.604 | 0.806 | 1.823  |
|  Traffic Hourly | 1.922 | 1.922 | 2.482 | 2.294 | 2.535 | 1.281 | 1.571 | 0.892 | 0.825 | 1.100 | 1.066 | 0.821  |
|  Traffic Weekly | 1.116 | 1.121 | 1.148 | 1.125 | 1.191 | 1.122 | 1.116 | 1.150 | 1.182 | 1.094 | 1.233 | 1.555  |
|  Ride4tare | 3.014 | 3.641 | 3.067 | 4.660 | 1.530 | 3.019 | 2.908 | 4.198 | 4.029 | 3.877 | 3.009 | 4.040  |
|  Hospital | 0.813 | 0.761 | 0.768 | 0.765 | 0.787 | 0.782 | 0.798 | 0.840 | 0.769 | 0.791 | 0.779 | 1.031  |
|  COVID | 7.776 | 7.793 | 5.719 | 5.326 | 6.117 | 8.731 | 8.241 | 5.459 | 6.895 | 5.858 | 7.835 | 8.941  |
|  Temp. Rain | 1.347 | 1.368 | 1.227 | 1.401 | 1.174 | 0.876 | 1.028 | 0.847 | 0.785 | 1.300 | 0.786 | 0.687  |
|  Sunspot | 0.128 | 0.128 | 0.067 | 0.128 | 0.067 | 0.099 | 0.059 | 0.207 | 0.020 | 0.375 | 0.004 | 0.003  |
|  Saagren | 1.426 | 1.425 | 1.477 | 2.036 | 1.485 | 1.674 | 1.411 | 1.524 | 1.560 | 1.852 | 1.471 | 1.861  |
|  Buths | 4.343 | 2.138 | 1.453 | 1.529 | 1.917 | 2.094 | 1.609 | 2.032 | 1.548 | 1.537 | 1.837 | 1.650  |

### Page 19
Table 6: Median MASE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 3.772 | 3.155 | 2.215 | 2.324 | 2.127 | 2.847 | 3.005 | 2.704 | 3.190 | 3.078 | 3.330 | 2.935  |
|  M1 Quarterly | 1.417 | 1.264 | 1.200 | 1.196 | 1.171 | 1.376 | 1.488 | 1.397 | 1.305 | 1.248 | 1.136 | 1.919  |
|  M1 Monthly | 1.167 | 0.885 | 0.902 | 0.851 | 0.894 | 0.947 | 1.009 | 0.984 | 0.984 | 0.946 | 0.994 | 1.724  |
|  M3 Yearly | 2.261 | 1.985 | 1.900 | 1.907 | 2.003 | 2.267 | 2.756 | 2.487 | 2.428 | 2.041 | 1.992 | 2.111  |
|  M3 Quarterly | 1.073 | 0.831 | 0.914 | 0.855 | 0.917 | 0.902 | 1.162 | 0.970 | 0.984 | 0.879 | 0.949 | 1.702  |
|  M3 Monthly | 0.861 | 0.721 | 0.699 | 0.712 | 0.704 | 0.825 | 0.885 | 0.836 | 0.932 | 0.766 | 0.825 | 1.071  |
|  M3 Other | 2.771 | 1.896 | 1.465 | 1.489 | 1.418 | 2.067 | 2.765 | 2.087 | 2.026 | 1.930 | 1.790 | 2.517  |
|  M4 Yearly | 2.940 | 2.312 | 2.402 | 2.329 | 2.753 | 2.568 | 2.576 | - | - | - | - | -  |
|  M4 Quarterly | 1.142 | 0.973 | 0.915 | 0.886 | 0.925 | 1.038 | 1.053 | 1.122 | 1.003 | 0.972 | 0.973 | 1.203  |
|  M4 Monthly | 0.867 | 0.763 | 0.733 | 0.736 | 0.727 | 0.844 | 0.845 | 0.937 | 0.901 | 0.792 | 0.913 | 1.520  |
|  M4 Weekly | 0.441 | 0.416 | 0.365 | 0.397 | 0.382 | 0.392 | 0.394 | 0.398 | 0.447 | 0.345 | 0.440 | 0.625  |
|  M4 Daily | 0.862 | 0.861 | 0.870 | 0.859 | 0.867 | 0.868 | 0.879 | 0.835 | 1.964 | 0.906 | 0.788 | 1.029  |
|  M4 Hourly | 3.685 | 3.688 | 1.873 | 5.792 | 3.507 | 1.010 | 1.045 | 1.384 | 1.490 | 1.658 | 1.161 | 1.225  |
|  Tourism Yearly | 2.442 | 2.360 | 2.518 | 2.373 | 2.719 | 2.356 | 2.950 | 2.745 | 2.246 | 2.267 | 2.751 | 2.715  |
|  Tourism Quarterly | 2.309 | 1.348 | 1.478 | 1.275 | 1.388 | 1.361 | 1.387 | 1.438 | 1.347 | 1.168 | 1.449 | 1.615  |
|  Tourism Monthly | 2.336 | 1.382 | 1.491 | 1.276 | 1.337 | 1.484 | 1.435 | 1.435 | 1.222 | 1.375 | 1.360 | 1.395  |
|  CIF 2016 | 0.862 | 0.662 | 0.537 | 0.532 | 0.559 | 0.746 | 0.802 | 0.772 | 0.644 | 0.663 | 0.810 | 0.671  |
|  Aus. Electricity Demand | 1.829 | 1.829 | 0.807 | 5.769 | 2.645 | 0.666 | 0.383 | 1.122 | 1.007 | 0.896 | 1.079 | 0.734  |
|  Dominick | 0.194 | 0.208 | 0.453 | 0.242 | 0.453 | 0.000 | 0.681 | 0.009 | 0.003 | 0.416 | 0.008 | 0.007  |
|  Bitcoin | 1.831 | 1.839 | 3.207 | 1.676 | 2.063 | 2.160 | 1.657 | 3.131 | 2.695 | 4.236 | 3.505 | 3.018  |
|  Pedestrian Counts | 0.604 | 0.605 | 1.004 | 0.645 | 4.125 | 0.128 | 0.175 | 0.135 | 0.162 | 0.199 | 0.122 | 0.149  |
|  Vehicle Trips | 0.668 | 0.665 | 0.963 | 0.689 | 0.665 | 0.646 | 0.587 | 1.078 | 1.091 | 1.315 | 0.970 | 1.278  |
|  KDD Cup | 1.357 | 1.357 | 1.246 | 1.402 | 1.744 | 1.035 | 0.969 | 0.984 | 1.480 | 1.349 | 0.895 | 1.298  |
|  Weather | 0.618 | 0.624 | 0.611 | 0.643 | 0.687 | 1.755 | 0.686 | 0.587 | 0.572 | 0.619 | 0.638 | 0.602  |
|  NN5 Daily | 1.482 | 0.838 | 0.834 | 0.809 | 0.926 | 1.224 | 0.896 | 0.895 | 0.911 | 1.056 | 0.909 | 0.898  |
|  NN5 Weekly | 0.781 | 0.805 | 0.827 | 0.775 | 0.769 | 0.781 | 0.804 | 0.756 | 0.729 | 0.746 | 1.007 | 1.048  |
|  Kaggle Daily | 0.539 | 0.548 | 0.551 | 0.667 | 0.528 | - | - | - | - | - | - | -  |
|  Kaggle Weekly | 0.432 | 0.418 | 0.330 | 0.383 | 0.529 | 0.573 | 1.120 | 0.302 | 0.353 | 0.314 | 0.318 | 0.318  |
|  Solar 10 Minutes | 1.403 | 1.404 | 2.431 | 1.403 | 1.029 | 1.403 | 2.482 | 1.403 | 1.402 | 1.529 | - | 1.403  |
|  Solar Weekly | 1.231 | 1.241 | 0.894 | 1.209 | 0.861 | 1.063 | 1.557 | 1.047 | 0.754 | 1.224 | 1.741 | 0.595  |
|  Electricity Hourly | 4.766 | 4.766 | 2.300 | 5.846 | 4.630 | 2.878 | 2.183 | 1.950 | 1.724 | 1.842 | 1.567 | 2.041  |
|  Electricity Weekly | 1.341 | 1.303 | 0.705 | 1.337 | 0.798 | 0.842 | 0.741 | 0.692 | 0.928 | 0.730 | 1.161 | 1.645  |
|  Carpats | 0.562 | 0.482 | 0.596 | 0.562 | 0.600 | 0.375 | 0.562 | 0.350 | 0.351 | 1.768 | 0.375 | 0.351  |
|  FRED-MD | 0.430 | 0.407 | 0.370 | 0.385 | 0.355 | 8.458 | 0.525 | 0.439 | 0.416 | 0.405 | 0.608 | 1.604  |
|  Traffic Hourly | 1.817 | 1.817 | 1.380 | 1.875 | 2.365 | 1.228 | 1.398 | 0.832 | 0.754 | 1.041 | 0.847 | 0.730  |
|  Traffic Weekly | 0.973 | 0.983 | 0.996 | 0.977 | 1.035 | 0.980 | 0.939 | 1.020 | 1.023 | 0.943 | 1.088 | 1.320  |
|  Rideshare | 2.998 | 3.611 | 2.865 | 4.054 | 1.427 | 3.003 | 2.928 | 4.223 | 4.043 | 3.790 | 2.073 | 4.054  |
|  Hospital | 0.745 | 0.723 | 0.734 | 0.731 | 0.733 | 0.740 | 0.760 | 0.780 | 0.726 | 0.750 | 0.741 | 0.879  |
|  COVID Deaths | 1.554 | 2.192 | 0.605 | 0.614 | 0.982 | 5.313 | 2.224 | 0.714 | 0.849 | 0.815 | 1.533 | 4.394  |
|  Temperature Rain | 0.828 | 0.852 | 0.887 | 0.829 | 0.856 | 0.608 | 0.889 | 0.624 | 0.566 | 0.766 | 0.621 | 0.575  |
|  Sunspot | 0.128 | 0.128 | 0.067 | 0.128 | 0.067 | 0.099 | 0.059 | 0.207 | 0.020 | 0.375 | 0.004 | 0.003  |
|  Saugern River Flow | 1.426 | 1.425 | 1.477 | 2.036 | 1.485 | 1.674 | 1.411 | 1.524 | 1.560 | 1.852 | 1.471 | 1.861  |
|  US Births | 4.343 | 2.138 | 1.453 | 1.529 | 1.917 | 2.094 | 1.609 | 2.032 | 1.548 | 1.537 | 1.837 | 1.650  |

### Page 20
Table 7: Mean sMAPE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 23.10 | 20.17 | 17.42 | 18.61 | 19.47 | 18.79 | 20.25 | 18.20 | 18.72 | 20.52 | 21.25 | 18.96  |
|  M1 Quarterly | 18.10 | 16.35 | 16.65 | 17.47 | 16.62 | 16.67 | 17.60 | 16.45 | 16.17 | 16.76 | 15.76 | 19.37  |
|  M1 Monthly | 17.43 | 16.53 | 15.15 | 15.05 | 15.65 | 15.20 | 16.51 | 15.71 | 17.16 | 16.77 | 16.59 | 22.17  |
|  M3 Yearly | 17.76 | 16.76 | 17.37 | 17.00 | 18.84 | 17.13 | 20.07 | 17.59 | 17.24 | 17.03 | 16.98 | 15.82  |
|  M3 Quarterly | 10.90 | 9.20 | 10.22 | 9.68 | 10.24 | 9.77 | 11.18 | 9.90 | 9.93 | 9.47 | 9.72 | 13.17  |
|  M3 Monthly | 16.22 | 13.86 | 13.85 | 14.14 | 14.24 | 15.17 | 16.41 | 15.33 | 15.74 | 14.76 | 15.43 | 17.13  |
|  M3 Other | 6.28 | 4.92 | 4.35 | 4.37 | 4.35 | 5.32 | 6.74 | 5.41 | 5.57 | 4.97 | 5.09 | 5.78  |
|  M4 Yearly | 16.40 | 14.56 | 14.92 | 15.36 | 16.03 | 14.53 | 15.28 | - | - | - | - | -  |
|  M4 Quarterly | 11.08 | 10.31 | 10.19 | 10.29 | 10.52 | 10.84 | 10.81 | 11.09 | 10.64 | 10.46 | 10.75 | 11.60  |
|  M4 Monthly | 14.38 | 13.01 | 12.95 | 13.53 | 13.08 | 13.74 | 14.05 | 14.03 | 14.29 | 13.40 | 15.42 | 18.37  |
|  M4 Weekly | 9.01 | 7.83 | 7.70 | 8.73 | 7.94 | 7.43 | 7.44 | 8.54 | 7.93 | 6.81 | 8.80 | 9.21  |
|  M4 Daily | 3.05 | 3.07 | 3.00 | 3.13 | 3.01 | 3.06 | 3.47 | 3.06 | 5.04 | 3.20 | 3.19 | 3.55  |
|  M4 Hourly | 42.95 | 42.98 | 28.12 | 69.60 | 35.99 | 11.68 | 9.55 | 16.26 | 15.07 | 15.75 | 12.05 | 15.74  |
|  Tourism Yearly | 34.14 | 31.96 | 33.97 | 36.56 | 33.44 | 46.94 | 31.58 | 33.76 | 34.09 | 30.27 | 28.82 | 34.69  |
|  Tourism Quarterly | 27.41 | 15.37 | 17.16 | 15.07 | 16.58 | 15.86 | 16.53 | 16.20 | 15.29 | 14.45 | 15.56 | 16.97  |
|  Tourism Monthly | 36.39 | 19.90 | 21.20 | 19.02 | 19.73 | 21.11 | 21.11 | 20.11 | 18.35 | 20.42 | 18.92 | 19.75  |
|  CIF 2016 | 14.95 | 13.05 | 12.20 | 12.18 | 11.70 | 12.33 | 14.87 | 12.32 | 13.58 | 11.72 | 18.86 | 12.56  |
|  Aus. Electricity Demand | 22.07 | 22.18 | 13.70 | 44.23 | 28.75 | 8.77 | 8.35 | 9.22 | 12.77 | 7.74 | 8.07 | 8.68  |
|  Dominick | - | - | - | - | - | - | 156.87 | 161.83 | 161.47 | 151.54 | 161.02 | 161.33  |
|  Bitcoin | 30.69 | 40.54 | 20.48 | 20.99 | 31.50 | 22.00 | 30.00 | 21.31 | 21.50 | 34.26 | 22.49 | 23.59  |
|  Pedestrian Counts | 123.96 | 124.19 | 119.96 | 150.11 | 138.67 | 41.10 | 45.92 | 39.96 | 37.23 | 55.20 | 35.50 | 37.01  |
|  Vehicle Trips | 36.41 | 37.60 | 29.36 | 39.22 | 37.11 | 35.19 | 30.92 | 30.33 | 30.41 | 36.84 | 29.08 | 32.29  |
|  KDD Cup | 62.20 | 62.31 | 56.37 | 66.40 | 86.13 | 50.73 | 48.53 | 50.48 | 87.42 | 80.00 | 49.00 | 69.76  |
|  Weather | 62.16 | 68.24 | 61.57 | 62.85 | - | - | 61.45 | 64.82 | 66.16 | 68.51 | 64.55 | 69.75  |
|  NN5 Daily | 35.50 | 22.01 | 21.19 | 21.57 | 26.01 | 30.30 | 24.13 | 23.39 | 23.85 | 28.58 | 22.73 | 23.26  |
|  NN5 Weekly | 12.24 | 11.96 | 11.63 | 12.30 | 11.84 | 11.45 | 11.67 | 11.50 | 11.52 | 10.93 | 14.96 | 14.84  |
|  Kaggle Daily | - | - | - | - | - | - | - | - | - | - | - | -  |
|  Kaggle Weekly | - | - | - | - | - | - | - | - | - | - | - | -  |
|  Solar 10 Minutes | 200.00 | 200.00 | 165.81 | 200.00 | 85.81 | 199.99 | 174.99 | 197.65 | 199.29 | 179.51 | - | 199.66  |
|  Solar Weekly | 24.59 | 24.76 | 19.05 | 22.93 | 17.87 | 21.65 | 29.35 | 21.52 | 15.00 | 24.05 | 32.50 | 12.26  |
|  Electricity Hourly | - | - | 40.47 | - | - | - | - | 23.06 | 20.96 | 23.39 | - | 24.18  |
|  Electricity Weekly | - | 14.58 | - | - | 10.86 | - | 9.68 | 9.24 | 10.88 | 10.24 | 12.65 | 16.19  |
|  Carpats | - | - | - | - | - | - | - | - | - | 166.05 | - | -  |
|  FRED-MD | 10.65 | 13.41 | 9.99 | 10.33 | 11.36 | 33.21 | 11.24 | 10.86 | 10.86 | 12.15 | 11.18 | 13.90  |
|  Traffic Hourly | - | 82.44 | 70.59 | - | 92.58 | - | 56.19 | 44.23 | 38.52 | 53.85 | 36.37 | 37.29  |
|  Traffic Weekly | 12.49 | 12.56 | 12.88 | 12.71 | 13.54 | 12.55 | 12.99 | 12.73 | 13.22 | 12.40 | 13.30 | 15.28  |
|  Rideshare | 199.96 | 200.00 | 183.94 | 199.96 | 73.66 | 198.13 | 188.92 | 192.99 | 198.14 | 147.23 | 145.48 | 199.93  |
|  Hospital | 17.98 | 17.31 | 17.60 | 17.50 | 17.83 | 17.60 | 18.09 | 18.33 | 17.45 | 17.77 | 17.55 | 20.08  |
|  COVID Deaths | - | - | - | - | - | - | - | - | 37.06 | 34.78 | - | 41.51  |
|  Temperature Rain | - | - | - | - | - | - | 146.92 | 156.48 | 167.76 | 183.31 | 159.76 | 172.75  |
|  Sunspot | 196.19 | 196.19 | 195.06 | 196.19 | 194.29 | 195.56 | 193.33 | 197.95 | 200.00 | 198.33 | 200.00 | 200.00  |
|  Saugren River Flow | 36.03 | 36.01 | 37.38 | 67.60 | 37.58 | 45.37 | 35.59 | 39.36 | 40.26 | 56.10 | 37.06 | 56.70  |
|  US Births | 11.77 | 5.82 | 3.81 | 4.05 | 5.17 | 5.75 | 4.23 | 5.55 | 4.13 | 4.17 | 4.88 | 4.36  |

### Page 21
Table 8: Median sMAPE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 17.33 | 14.74 | 12.68 | 13.01 | 11.99 | 13.49 | 14.22 | 12.77 | 14.42 | 14.61 | 15.95 | 14.99  |
|  M1 Quarterly | 11.24 | 8.63 | 8.60 | 8.40 | 9.66 | 10.13 | 12.07 | 9.53 | 8.96 | 9.57 | 8.73 | 13.83  |
|  M1 Monthly | 14.35 | 11.18 | 11.28 | 10.82 | 11.51 | 11.88 | 12.29 | 12.05 | 11.94 | 11.97 | 12.02 | 19.11  |
|  M3 Yearly | 12.44 | 11.54 | 11.52 | 11.52 | 12.37 | 12.92 | 15.23 | 13.14 | 12.27 | 12.16 | 11.64 | 11.39  |
|  M3 Quarterly | 6.74 | 5.23 | 6.17 | 5.53 | 6.36 | 5.73 | 7.59 | 5.95 | 5.73 | 5.44 | 5.66 | 10.54  |
|  M3 Monthly | 10.71 | 9.25 | 9.04 | 9.13 | 9.01 | 10.40 | 11.12 | 10.55 | 10.91 | 9.95 | 10.55 | 12.66  |
|  M3 Other | 4.62 | 2.88 | 2.07 | 2.23 | 2.19 | 3.42 | 4.26 | 3.38 | 3.80 | 2.97 | 2.59 | 3.66  |
|  M4 Yearly | 11.41 | 9.23 | 8.84 | 8.97 | 10.20 | 9.49 | 9.51 | - | - | - | - | -  |
|  M4 Quarterly | 6.94 | 6.06 | 5.76 | 5.61 | 5.80 | 6.34 | 6.43 | 6.35 | 6.03 | 5.87 | 5.79 | 6.90  |
|  M4 Monthly | 8.38 | 7.24 | 7.06 | 7.00 | 7.13 | 8.20 | 8.12 | 8.18 | 8.41 | 7.94 | 8.43 | 12.17  |
|  M4 Weekly | 5.17 | 5.19 | 4.81 | 5.06 | 5.10 | 4.99 | 5.74 | 4.72 | 5.37 | 4.30 | 5.08 | 6.52  |
|  M4 Daily | 1.99 | 2.01 | 2.01 | 1.99 | 2.01 | 2.00 | 2.08 | 1.96 | 4.07 | 2.10 | 1.83 | 2.40  |
|  M4 Hourly | 19.88 | 19.79 | 6.55 | 51.14 | 32.18 | 5.80 | 5.12 | 6.01 | 10.18 | 7.33 | 5.41 | 12.17  |
|  Tourism Yearly | 18.81 | 16.83 | 20.62 | 19.20 | 22.66 | 16.88 | 23.66 | 19.21 | 17.76 | 16.64 | 19.06 | 20.30  |
|  Tourism Quarterly | 22.48 | 13.17 | 14.77 | 12.89 | 13.13 | 13.33 | 13.46 | 13.23 | 12.86 | 11.80 | 13.03 | 14.14  |
|  Tourism Monthly | 30.24 | 17.40 | 19.03 | 17.16 | 18.01 | 18.47 | 18.67 | 17.24 | 15.78 | 18.01 | 16.66 | 17.37  |
|  CIF 2016 | 11.40 | 7.95 | 7.00 | 6.58 | 7.69 | 8.43 | 10.44 | 8.08 | 8.97 | 7.71 | 9.92 | 7.77  |
|  Aus. Electricity Demand | 22.99 | 22.99 | 9.55 | 47.33 | 29.01 | 6.47 | 4.72 | 6.75 | 7.16 | 4.62 | 6.32 | 4.66  |
|  Dominick | - | - | - | - | - | - | 200.00 | 200.00 | 200.00 | 200.00 | 200.00 | 200.00  |
|  Bitcoin | 18.23 | 18.37 | 17.52 | 19.31 | 19.95 | 17.23 | 18.58 | 18.51 | 17.86 | 25.50 | 18.36 | 17.91  |
|  Pedestrian Counts | 123.48 | 124.69 | 118.71 | 146.91 | 142.81 | 36.80 | 42.76 | 35.28 | 32.36 | 51.47 | 28.71 | 32.74  |
|  Vehicle Trips | 34.19 | 34.22 | 22.84 | 34.75 | 34.19 | 32.71 | 25.52 | 25.20 | 24.58 | 32.30 | 23.11 | 26.23  |
|  KDD Cup | 60.40 | 60.57 | 53.99 | 61.29 | 85.87 | 52.82 | 48.04 | 53.53 | 95.08 | 81.68 | 48.66 | 72.17  |
|  Weather | 23.71 | 23.83 | 23.63 | 25.36 | - | - | 22.60 | 23.72 | 21.38 | 27.87 | 23.47 | 22.18  |
|  NN5 Daily | 34.68 | 20.56 | 19.61 | 20.35 | 22.80 | 28.81 | 22.59 | 22.05 | 22.40 | 26.21 | 21.45 | 21.94  |
|  NN5 Weekly | 10.95 | 10.96 | 10.97 | 10.79 | 11.08 | 10.50 | 10.54 | 11.01 | 10.06 | 10.24 | 13.88 | 13.83  |
|  Kaggle Daily | - | - | - | - | - | - | - | - | - | - | - | -  |
|  Kaggle Weekly | - | - | - | - | - | - | - | - | - | - | - | -  |
|  Solar 10 Minutes | 200.00 | 200.00 | 161.88 | 200.00 | 85.73 | 200.00 | 175.35 | 198.80 | 199.53 | 176.49 | - | 199.69  |
|  Solar Weekly | 24.76 | 24.90 | 18.36 | 24.44 | 17.64 | 21.77 | 29.91 | 20.92 | 15.12 | 24.03 | 31.39 | 12.54  |
|  Electricity Hourly | - | - | 23.23 | - | - | - | - | 17.01 | 15.44 | 16.58 | - | 19.21  |
|  Electricity Weekly | - | 11.72 | - | - | 6.97 | - | 6.23 | 6.25 | 8.02 | 6.30 | 10.22 | 15.65  |
|  Carpats | - | - | - | - | - | - | - | - | - | 172.22 | - | -  |
|  FRED-MD | 1.61 | 1.53 | 1.31 | 1.54 | 1.57 | 29.14 | 2.91 | 1.85 | 1.63 | 1.49 | 2.45 | 5.16  |
|  Traffic Hourly | - | 74.21 | 55.69 | - | 86.56 | - | 45.52 | 29.16 | 23.20 | 39.89 | 23.49 | 23.74  |
|  Traffic Weekly | 9.70 | 9.75 | 10.05 | 9.81 | 10.54 | 9.75 | 10.15 | 9.92 | 10.52 | 9.47 | 10.66 | 12.78  |
|  Rideshare | 200.00 | 200.00 | 197.43 | 200.00 | 59.75 | 198.10 | 188.02 | 193.70 | 198.10 | 144.95 | 184.65 | 199.93  |
|  Hospital | 16.58 | 15.91 | 16.35 | 16.13 | 16.77 | 16.14 | 16.91 | 17.15 | 16.41 | 16.14 | 16.53 | 18.16  |
|  COVID Deaths | - | - | - | - | - | - | - | - | 4.08 | 3.94 | - | 15.57  |
|  Temperature Rain | - | - | - | - | - | - | 159.43 | 169.49 | 189.27 | 186.21 | 189.86 | 198.51  |
|  Sunspot | 196.19 | 196.19 | 195.06 | 196.19 | 194.29 | 195.56 | 193.33 | 197.95 | 200.00 | 198.33 | 200.00 | 200.00  |
|  Saugren River Flow | 36.03 | 36.01 | 37.38 | 67.60 | 37.58 | 45.37 | 35.59 | 39.36 | 40.26 | 56.10 | 37.06 | 56.70  |
|  US Births | 11.77 | 5.82 | 3.81 | 4.05 | 5.17 | 5.75 | 4.23 | 5.55 | 4.13 | 4.17 | 4.88 | 4.36  |

### Page 22
|  Table 9: Mean msMAPE results | |
| --- | --- |
|  |

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 23.08 | 20.16 | 17.41 | 18.60 | 19.46 | 18.77 | 20.24 | 18.19 | 18.70 | 20.50 | 21.23  |
|  M2 Quarterly | 18.07 | 16.33 | 16.62 | 17.41 | 16.59 | 16.64 | 17.57 | 16.42 | 16.14 | 16.73 | 15.73  |
|  M3 Monthly | 17.12 | 15.53 | 14.82 | 14.64 | 15.26 | 14.85 | 16.05 | 15.40 | 16.08 | 16.20 | 16.27  |
|  M3 Yearly | 17.76 | 16.76 | 17.37 | 17.00 | 18.84 | 17.13 | 20.07 | 17.59 | 17.24 | 17.03 | 16.98  |
|  M3 Quarterly | 10.90 | 9.20 | 10.22 | 9.68 | 10.24 | 9.77 | 11.18 | 9.90 | 9.93 | 9.47 | 9.72  |
|  M3 Monthly | 16.22 | 13.86 | 13.85 | 14.14 | 14.24 | 15.17 | 16.41 | 15.33 | 15.74 | 14.76 | 15.43  |
|  M3 Other | 6.28 | 4.92 | 4.35 | 4.37 | 4.35 | 5.32 | 6.74 | 5.41 | 5.57 | 4.97 | 5.09  |
|  M4 Yearly | 16.40 | 14.56 | 14.92 | 15.36 | 16.03 | 14.53 | 15.28 | - | - | - | -  |
|  M4 Quarterly | 11.08 | 10.31 | 10.19 | 10.29 | 10.52 | 10.83 | 10.81 | 11.09 | 10.64 | 10.46 | 10.75  |
|  M4 Monthly | 14.38 | 13.01 | 12.95 | 13.52 | 13.08 | 13.73 | 14.05 | 14.03 | 14.29 | 13.40 | 15.42  |
|  M4 Weekly | 9.01 | 7.83 | 7.70 | 8.73 | 7.94 | 7.43 | 7.44 | 8.54 | 7.93 | 6.81 | 8.80  |
|  M4 Daily | 3.04 | 3.07 | 3.00 | 3.13 | 3.01 | 3.06 | 3.47 | 3.06 | 5.04 | 3.20 | 3.19  |
|  M4 Hourly | 42.92 | 42.94 | 28.10 | 69.51 | 35.94 | 11.67 | 9.54 | 16.24 | 15.06 | 15.73 | 12.04  |
|  Tourism Yearly | 34.10 | 31.93 | 33.94 | 36.52 | 33.39 | 46.92 | 31.54 | 33.73 | 34.06 | 30.24 | 28.80  |
|  Tourism Quarterly | 27.41 | 15.37 | 17.16 | 15.07 | 16.58 | 15.86 | 16.53 | 16.20 | 15.29 | 14.45 | 15.56  |
|  Tourism Monthly | 36.39 | 19.89 | 21.20 | 19.02 | 19.73 | 21.11 | 21.10 | 20.11 | 18.35 | 20.42 | 18.92  |
|  CIF 2016 | 14.94 | 13.04 | 12.19 | 12.18 | 11.69 | 12.32 | 14.86 | 12.31 | 13.54 | 11.71 | 18.82  |
|  Aus. Electricity Demand | 22.07 | 22.18 | 13.70 | 44.22 | 28.75 | 8.76 | 8.35 | 9.22 | 12.77 | 7.74 | 8.07  |
|  Dominick | 72.94 | 114.89 | 103.08 | 79.37 | 136.72 | 68.44 | 143.08 | 52.26 | 39.59 | 127.80 | 42.56  |
|  Bitcoin | 30.31 | 40.36 | 20.12 | 20.65 | 31.11 | 21.48 | 29.78 | 21.00 | 21.16 | 31.95 | 22.16  |
|  Pedestrian Counts | 121.39 | 122.08 | 119.76 | 148.48 | 138.58 | 40.29 | 45.54 | 39.30 | 36.10 | 54.15 | 34.22  |
|  Vehicle Trips | 36.20 | 37.37 | 29.16 | 38.96 | 36.90 | 34.97 | 30.72 | 30.13 | 30.20 | 36.60 | 28.88  |
|  KDD Cup | 61.68 | 61.80 | 55.91 | 65.89 | 85.32 | 50.33 | 48.16 | 50.08 | 86.36 | 79.25 | 48.59  |
|  Weather | 50.85 | 56.19 | 58.06 | 51.47 | 57.98 | 106.01 | 59.12 | 38.17 | 36.46 | 50.87 | 40.13  |
|  NN5 Daily | 35.38 | 21.93 | 21.11 | 21.49 | 25.91 | 30.20 | 24.04 | 23.30 | 23.75 | 28.47 | 22.65  |
|  NN5 Weekly | 12.24 | 11.96 | 11.62 | 12.29 | 11.83 | 11.45 | 11.67 | 11.49 | 11.52 | 10.93 | 14.95  |
|  Kaggle Daily | 45.87 | 47.98 | 46.93 | 57.94 | 44.39 | - | - | - | - | - | -  |
|  Kaggle Weekly | 45.10 | 47.72 | 40.88 | 49.40 | 65.55 | 72.93 | 75.96 | 36.02 | 38.34 | 40.02 | 36.63  |
|  Solar 10 Minutes | 65.07 | 65.75 | 154.38 | 65.26 | 30.20 | 65.09 | 116.30 | 65.21 | 64.84 | 112.99 | 64.96  |
|  Solar Weekly | 24.59 | 24.76 | 19.05 | 22.93 | 17.87 | 21.65 | 29.35 | 21.52 | 15.00 | 24.05 | 32.50  |
|  Electricity Hourly | 44.39 | 44.94 | 40.15 | 73.31 | 43.78 | 30.00 | 25.45 | 23.04 | 20.94 | 23.24 | 18.71  |
|  Electricity Weekly | 14.17 | 14.58 | 8.58 | 14.10 | 10.86 | 9.98 | 9.68 | 9.24 | 10.88 | 10.13 | 12.65  |
|  Carparts | 64.88 | 59.27 | 65.89 | 65.76 | 65.61 | 43.23 | 65.51 | 38.87 | 38.92 | 151.48 | 41.31  |
|  FRED-MD | 8.72 | 9.72 | 7.97 | 8.40 | 7.98 | 30.77 | 9.16 | 8.99 | 8.53 | 8.32 | 9.08  |
|  Traffic Hourly | 8.73 | 8.73 | 12.58 | 9.84 | 11.72 | 5.97 | 7.94 | 4.30 | 4.16 | 5.16 | 5.22  |
|  Traffic Weekly | 12.40 | 12.48 | 12.80 | 12.63 | 13.45 | 12.46 | 12.90 | 12.64 | 13.13 | 12.31 | 13.21  |
|  Ride-bars | 141.34 | 154.03 | 134.50 | 141.14 | 57.26 | 142.89 | 131.71 | 157.44 | 143.66 | 119.55 | 92.54  |
|  Hospital | 17.94 | 17.27 | 17.55 | 17.46 | 17.79 | 17.56 | 18.04 | 18.29 | 17.41 | 17.72 | 17.51  |
|  COVID Deaths | 15.35 | 15.57 | 8.71 | 8.64 | 9.26 | 18.34 | 15.40 | 18.58 | 34.18 | 32.36 | 14.50  |
|  Temperature Rain | 120.81 | 121.98 | 125.07 | 120.90 | 124.66 | 95.96 | 125.04 | 91.57 | 77.95 | 124.40 | 74.02  |
|  Sunspot | 192.36 | 192.36 | 167.62 | 192.36 | 172.80 | 190.14 | 185.05 | 195.03 | 104.39 | 196.97 | 12.80  |
|  Saugren River Flow | 35.99 | 35.97 | 37.34 | 67.50 | 37.55 | 45.32 | 35.55 | 39.32 | 40.22 | 56.03 | 37.02  |
|  US Births | 11.77 | 5.82 | 3.81 | 4.05 | 5.17 | 5.75 | 4.23 | 5.55 | 4.13 | 4.17 | 4.88  |

### Page 23
Table 10: Median msMAPE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 17.14 | 14.74 | 12.68 | 12.99 | 11.99 | 13.49 | 14.13 | 12.77 | 14.36 | 14.61 | 15.95 | 14.99  |
|  M1 Quarterly | 11.23 | 8.63 | 8.60 | 8.40 | 9.66 | 10.13 | 12.07 | 9.53 | 8.96 | 9.57 | 8.73 | 13.66  |
|  M1 Monthly | 14.24 | 11.18 | 11.18 | 10.80 | 11.48 | 11.79 | 12.27 | 12.05 | 11.83 | 11.88 | 11.96 | 19.00  |
|  M3 Yearly | 12.44 | 11.54 | 11.52 | 11.52 | 12.37 | 12.92 | 15.23 | 13.14 | 12.27 | 12.16 | 11.64 | 11.39  |
|  M3 Quarterly | 6.74 | 5.23 | 6.17 | 5.53 | 6.36 | 5.73 | 7.59 | 5.95 | 5.73 | 5.44 | 5.66 | 10.54  |
|  M3 Monthly | 10.71 | 9.25 | 9.04 | 9.13 | 9.01 | 10.39 | 11.12 | 10.55 | 10.91 | 9.95 | 10.55 | 12.66  |
|  M3 Other | 4.62 | 2.88 | 2.07 | 2.23 | 2.19 | 3.42 | 4.26 | 3.38 | 3.80 | 2.97 | 2.59 | 3.66  |
|  M4 Yearly | 11.41 | 9.23 | 8.84 | 8.97 | 10.20 | 9.49 | 9.51 | - | - | - | - | -  |
|  M4 Quarterly | 6.94 | 6.06 | 5.76 | 5.61 | 5.80 | 6.34 | 6.43 | 6.35 | 6.03 | 5.87 | 5.79 | 6.90  |
|  M4 Monthly | 8.38 | 7.24 | 7.06 | 7.00 | 7.13 | 8.20 | 8.12 | 8.18 | 8.41 | 7.94 | 8.43 | 12.17  |
|  M4 Weekly | 5.17 | 5.19 | 4.81 | 5.06 | 5.10 | 4.99 | 5.74 | 4.72 | 5.37 | 4.30 | 5.08 | 6.52  |
|  M4 Daily | 1.99 | 2.01 | 2.01 | 1.99 | 2.01 | 2.00 | 2.08 | 1.96 | 4.07 | 2.10 | 1.83 | 2.40  |
|  M4 Hourly | 19.86 | 19.75 | 6.55 | 51.07 | 32.08 | 5.80 | 5.11 | 6.00 | 10.18 | 7.33 | 5.41 | 12.15  |
|  Tourism Yearly | 18.77 | 16.83 | 20.62 | 19.04 | 22.57 | 16.88 | 23.66 | 19.20 | 17.76 | 16.64 | 18.99 | 20.20  |
|  Tourism Quarterly | 22.48 | 13.17 | 14.77 | 12.89 | 13.13 | 13.33 | 13.46 | 13.23 | 12.86 | 11.80 | 13.03 | 14.14  |
|  Tourism Monthly | 30.24 | 17.40 | 19.03 | 17.16 | 18.00 | 18.47 | 18.67 | 17.24 | 15.78 | 18.01 | 16.66 | 17.37  |
|  CIF 2016 | 11.40 | 7.95 | 7.00 | 6.58 | 7.69 | 8.43 | 10.44 | 8.08 | 8.96 | 7.71 | 9.92 | 7.77  |
|  Aus. Electricity Demand | 22.99 | 22.99 | 9.55 | 47.33 | 29.01 | 6.47 | 4.72 | 6.75 | 7.16 | 4.62 | 6.32 | 4.66  |
|  Dominick | 41.90 | 130.16 | 112.37 | 55.78 | 164.14 | 0.00 | 175.94 | 10.98 | 7.42 | 156.30 | 24.30 | 8.50  |
|  Bitcoin | 18.23 | 18.36 | 17.52 | 18.85 | 19.62 | 17.23 | 18.58 | 18.47 | 17.62 | 25.45 | 16.63 | 17.91  |
|  Pedestrian Counts | 121.41 | 124.44 | 118.52 | 146.18 | 142.71 | 36.46 | 42.15 | 35.02 | 31.67 | 50.76 | 28.02 | 32.31  |
|  Vehicle Trips | 33.71 | 34.13 | 22.72 | 34.73 | 33.90 | 32.53 | 25.39 | 25.08 | 24.52 | 32.12 | 22.86 | 26.20  |
|  KDD Cup | 60.18 | 60.23 | 53.98 | 61.15 | 84.90 | 52.77 | 47.77 | 53.26 | 92.97 | 81.60 | 48.49 | 72.05  |
|  Weather | 22.26 | 22.31 | 23.49 | 23.59 | 23.00 | 119.15 | 22.48 | 21.25 | 19.12 | 27.72 | 19.93 | 18.83  |
|  NN5 Daily | 34.57 | 20.51 | 19.56 | 20.31 | 22.72 | 28.70 | 22.52 | 22.01 | 22.34 | 26.13 | 21.38 | 21.85  |
|  NN5 Weekly | 10.94 | 10.96 | 10.97 | 10.79 | 11.08 | 10.50 | 10.54 | 11.00 | 10.06 | 10.24 | 13.88 | 13.83  |
|  Kaggle Daily | 37.02 | 37.69 | 35.82 | 46.19 | 35.16 | - | - | - | - | - | - | -  |
|  Kaggle Weekly | 32.52 | 33.01 | 29.31 | 33.99 | 46.41 | 73.32 | 58.19 | 27.76 | 30.83 | 29.05 | 28.81 | 30.93  |
|  Solar 10 Minutes | 64.68 | 65.26 | 152.54 | 64.83 | 30.26 | 64.68 | 115.93 | 64.88 | 64.47 | 112.62 | - | 64.57  |
|  Solar Weekly | 24.76 | 24.90 | 18.36 | 24.44 | 17.64 | 21.77 | 29.91 | 20.92 | 15.12 | 24.03 | 31.39 | 12.54  |
|  Electricity Hourly | 42.08 | 42.20 | 23.22 | 59.79 | 38.30 | 24.78 | 18.85 | 17.01 | 15.44 | 16.58 | 14.03 | 19.21  |
|  Electricity Weekly | 12.22 | 11.72 | 6.17 | 12.17 | 6.97 | 7.41 | 6.23 | 6.25 | 8.02 | 6.30 | 10.22 | 15.65  |
|  Carparts | 45.45 | 45.45 | 46.18 | 46.18 | 46.18 | 30.30 | 47.69 | 30.30 | 30.30 | 157.85 | 30.30 | 30.30  |
|  FRED-MD | 1.58 | 1.53 | 1.31 | 1.54 | 1.57 | 29.09 | 2.90 | 1.83 | 1.63 | 1.49 | 2.45 | 3.16  |
|  Traffic Hourly | 8.26 | 8.26 | 7.58 | 8.92 | 10.66 | 5.43 | 6.69 | 3.63 | 3.59 | 4.47 | 4.04 | 3.42  |
|  Traffic Weekly | 9.66 | 9.71 | 10.01 | 9.77 | 10.48 | 9.69 | 10.10 | 9.86 | 10.48 | 9.42 | 10.62 | 12.72  |
|  Rideshare | 154.26 | 159.47 | 147.21 | 154.26 | 53.33 | 153.00 | 141.70 | 172.70 | 153.79 | 128.13 | 117.92 | 154.22  |
|  Hospital | 16.57 | 15.90 | 16.33 | 16.11 | 16.75 | 16.12 | 16.87 | 17.11 | 16.39 | 16.10 | 16.48 | 18.15  |
|  COVID Deaths | 2.68 | 6.10 | 1.48 | 1.38 | 1.94 | 16.99 | 5.27 | 3.01 | 4.08 | 3.94 | 3.30 | 15.50  |
|  Temperature Rain | 134.33 | 135.22 | 137.18 | 134.31 | 137.53 | 109.91 | 138.35 | 96.55 | 81.49 | 144.63 | 72.73 | 64.20  |
|  Sunspot | 192.36 | 192.36 | 167.62 | 192.36 | 172.80 | 190.14 | 185.05 | 195.03 | 104.39 | 196.97 | 12.80 | 12.70  |
|  Saugren River Flow | 35.99 | 35.97 | 37.34 | 67.50 | 37.55 | 45.32 | 35.55 | 39.32 | 40.22 | 56.03 | 37.02 | 56.62  |
|  US Births | 11.77 | 5.82 | 3.81 | 4.05 | 5.17 | 5.75 | 4.23 | 5.55 | 4.13 | 4.17 | 4.88 | 4.36  |

### Page 24
Table 11: Mean MAE results

|  Dataset | SES | Thria | TBATS | ETS | iDHR+ARIMA | PR | Calffood | FENN | DeepAR | N-BEATS | WarsNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 171353.41 | 152798.26 | 183006.90 | 146310.11 | 145608.87 | 134246.38 | 215904.20 | 136258.80 | 152084.40 | 173300.20 | 284953.90 | 164637.90  |
|  M1 Quarterly | 2206.27 | 1981.96 | 2326.46 | 2088.15 | 2191.10 | 1630.38 | 1802.18 | 1617.39 | 1951.14 | 1820.25 | 1855.49 | 1864.06  |
|  M1 Monthly | 2259.04 | 2166.18 | 2237.50 | 1905.28 | 2080.13 | 2088.25 | 2052.32 | 2162.58 | 1860.81 | 1820.37 | 2184.42 | 2723.88  |
|  M3 Yearly | 1022.27 | 957.40 | 1192.85 | 1031.40 | 1416.31 | 1018.48 | 1163.36 | 1082.10 | 994.72 | 962.33 | 987.28 | 924.47  |
|  M3 Quarterly | 571.96 | 486.31 | 561.77 | 513.06 | 559.40 | 519.30 | 593.29 | 528.47 | 519.35 | 494.85 | 523.04 | 519.62  |
|  M3 Monthly | 743.41 | 622.71 | 630.59 | 626.46 | 654.80 | 692.97 | 732.00 | 692.48 | 728.81 | 648.60 | 699.30 | 798.38  |
|  M3 Other | 277.83 | 233.35 | 189.42 | 194.98 | 193.02 | 234.43 | 318.13 | 240.17 | 247.56 | 221.85 | 245.29 | 239.24  |
|  M4 Yearly | 1009.06 | 890.51 | 960.45 | 920.66 | 1067.36 | 875.76 | 929.06 | - | - | - | - | -  |
|  M4 Quarterly | 622.57 | 574.34 | 578.26 | 573.19 | 604.51 | 610.51 | 689.55 | 631.01 | 597.16 | 580.44 | 596.78 | 637.60  |
|  M4 Monthly | 625.24 | 563.58 | 589.52 | 582.60 | 575.36 | 596.19 | 611.69 | 612.52 | 615.22 | 578.48 | 655.51 | 780.47  |
|  M4 Weekly | 336.82 | 333.32 | 296.15 | 335.66 | 321.61 | 293.21 | 364.65 | 338.37 | 351.78 | 277.73 | 359.46 | 378.89  |
|  M4 Daily | 178.27 | 178.86 | 176.60 | 193.26 | 179.67 | 181.92 | 231.36 | 177.91 | 299.79 | 190.44 | 189.47 | 201.08  |
|  M4 Hourly | 1218.06 | 1220.97 | 386.27 | 3758.10 | 1310.65 | 257.39 | 285.35 | 385.49 | 886.02 | 425.75 | 393.63 | 320.54  |
|  Tourism Yearly | 95579.23 | 90653.60 | 94121.08 | 94818.89 | 95033.24 | 82682.97 | 79567.22 | 79593.22 | 71471.29 | 70951.80 | 69905.47 | 74316.52  |
|  Tourism Quarterly | 15014.19 | 7656.49 | 9972.42 | 8925.52 | 10475.47 | 9092.58 | 10267.97 | 9981.04 | 9511.37 | 8640.56 | 9137.12 | 9521.67  |
|  Tourism Monthly | 5302.10 | 2069.96 | 2940.08 | 2004.51 | 2536.77 | 2187.28 | 2537.04 | 2022.21 | 1871.69 | 2003.02 | 2095.13 | 2146.98  |
|  CIF 2016 | 581875.97 | 714818.58 | 855578.40 | 642421.42 | 469059.49 | 563205.57 | 603551.38 | 1495923.44 | 3200418.00 | 679034.80 | 5998224.62 | 4057973.04  |
|  Acc. Electricity Demand | 659.60 | 665.04 | 370.74 | 1282.99 | 1045.92 | 247.18 | 241.77 | 258.76 | 302.41 | 213.83 | 227.50 | 331.45  |
|  Demnack | 5.70 | 5.66 | 7.00 | 5.81 | 7.10 | 8.19 | 8.09 | 5.85 | 5.23 | 8.28 | 5.10 | 5.18  |
|  Bitcoin | $5.33 \times 10^{18}$ | $5.33 \times 10^{18}$ | $9.9 \times 10^{17}$ | $1.10 \times 10^{18}$ | $3.02 \times 10^{18}$ | $6.66 \times 10^{17}$ | $1.93 \times 10^{16}$ | $1.45 \times 10^{16}$ | $1.95 \times 10^{16}$ | $1.06 \times 10^{16}$ | $2.46 \times 10^{16}$ | $2.61 \times 10^{16}$  |
|  Pedestrian Counts | 170.87 | 170.94 | 222.38 | 216.50 | 635.16 | 44.18 | 43.41 | 46.41 | 44.78 | 68.84 | 46.46 | 47.29  |
|  Vehicle Trips | 29.98 | 30.76 | 21.21 | 30.95 | 30.07 | 27.24 | 22.61 | 22.93 | 22.00 | 28.16 | 24.15 | 28.01  |
|  KDD Cup | 42.04 | 42.06 | 39.20 | 44.88 | 52.20 | 36.85 | 34.82 | 37.16 | 48.98 | 49.10 | 37.08 | 44.46  |
|  Weather | 2.34 | 2.51 | 2.30 | 2.55 | 2.45 | 8.17 | 2.51 | 2.09 | 2.02 | 2.34 | 2.29 | 2.03  |
|  NNT Daily | 6.63 | 3.80 | 3.70 | 3.72 | 4.41 | 5.47 | 4.22 | 4.06 | 3.94 | 4.82 | 3.97 | 4.16  |
|  NNT Weekly | 15.66 | 15.30 | 14.98 | 15.70 | 15.58 | 14.94 | 15.29 | 15.02 | 14.69 | 14.19 | 19.34 | 20.34  |
|  Kaggle Daily | 363.43 | 358.73 | 415.40 | 403.23 | 340.36 | - | - | - | - | - | - | -  |
|  Kaggle Weekly | 2337.11 | 2373.98 | 2241.84 | 2668.28 | 3115.03 | 4051.75 | 10715.36 | 2025.23 | 2272.58 | 2051.30 | 2023.50 | 3160.32  |
|  Solar 10 Minutes | 3.28 | 3.29 | 8.77 | 3.28 | 2.37 | 3.28 | 5.69 | 3.28 | 3.28 | 3.32 | 3.28 | 3.28  |
|  Solar Weekly | 1202.39 | 1210.83 | 908.65 | 1133.01 | 839.88 | 1044.88 | 1513.49 | 1050.64 | 721.59 | 1172.64 | 1996.89 | 576.35  |
|  Electricity Hourly | 845.97 | 846.03 | 574.30 | 1344.61 | 868.20 | 537.78 | 407.14 | 354.39 | 329.75 | 350.37 | 286.56 | 398.80  |
|  Conners | 74149.18 | 74111.14 | 24347.24 | 67737.82 | 28457.18 | 44882.52 | 34518.43 | 27451.83 | 50312.05 | 32991.72 | 61429.32 | 76382.47  |
|  Conners | 0.55 | 0.53 | 0.58 | 0.56 | 0.56 | 0.41 | 0.53 | 0.39 | 0.39 | 0.38 | 0.40 | 0.39  |
|  FRED-MD | 2798.22 | 3492.84 | 1989.97 | 2041.42 | 2957.11 | 8921.94 | 2475.68 | 2139.57 | 4264.36 | 2557.80 | 2508.40 | 4666.04  |
|  Traffic Hourly | 0.03 | 0.03 | 0.04 | 0.03 | 0.04 | 0.02 | 0.02 | 0.01 | 0.01 | 0.02 | 0.02 | 0.01  |
|  Traffic Weekly | 1.12 | 1.13 | 1.17 | 1.14 | 1.22 | 1.13 | 1.17 | 1.13 | 1.18 | 1.11 | 1.20 | 1.42  |
|  Rehmann | 6.29 | 7.62 | 6.45 | 6.29 | 3.37 | 6.50 | 6.07 | 6.59 | 6.28 | 5.25 | 2.75 | 6.28  |
|  Hospital | 21.76 | 18.54 | 17.43 | 17.97 | 19.60 | 19.24 | 19.17 | 22.86 | 18.25 | 20.18 | 19.35 | 36.19  |
|  COVID Deaths | 355.71 | 321.32 | 96.29 | 85.59 | 85.77 | 347.98 | 455.15 | 144.14 | 201.98 | 191.81 | 1649.48 | 408.69  |
|  Temperature Rain | 8.18 | 8.22 | 7.14 | 8.21 | 7.19 | 6.13 | 6.76 | 5.56 | 5.37 | 7.28 | 5.81 | 5.24  |
|  Sunspot | 4.93 | 4.93 | 2.57 | 4.93 | 2.57 | 3.83 | 2.27 | 3.93 | 3.77 | 14.47 | 0.17 | 0.13  |
|  Sunspots River Flow | 21.50 | 21.49 | 22.26 | 30.69 | 22.38 | 25.24 | 21.28 | 22.98 | 23.51 | 27.92 | 22.17 | 28.06  |
|  US Births | 1192.20 | 586.93 | 399.00 | 419.73 | 526.33 | 574.93 | 441.70 | 557.87 | 424.93 | 422.00 | 504.40 | 452.87  |

### Page 25
Table 12: Median MAE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 379.28 | 255.75 | 173.36 | 191.24 | 179.98 | 245.67 | 269.91 | 218.52 | 251.76 | 291.45 | 230.10 | 230.80  |
|  M1 Quarterly | 22.30 | 19.55 | 18.87 | 19.59 | 16.23 | 19.19 | 18.72 | 19.86 | 19.37 | 17.31 | 18.30 | 32.23  |
|  M1 Monthly | 45.33 | 38.23 | 35.78 | 38.51 | 40.54 | 37.37 | 38.24 | 38.35 | 36.97 | 35.35 | 44.29 | 65.23  |
|  M3 Yearly | 703.33 | 660.49 | 637.81 | 641.07 | 701.32 | 711.86 | 846.58 | 757.24 | 739.10 | 629.20 | 690.05 | 621.92  |
|  M3 Quarterly | 371.95 | 294.16 | 335.69 | 304.53 | 333.74 | 325.44 | 395.44 | 324.16 | 316.03 | 312.89 | 322.32 | 605.19  |
|  M3 Monthly | 517.09 | 420.80 | 406.83 | 408.92 | 412.47 | 479.18 | 527.74 | 482.42 | 528.96 | 449.60 | 489.82 | 614.65  |
|  M3 Other | 164.13 | 104.93 | 91.41 | 83.64 | 77.02 | 127.12 | 149.28 | 132.07 | 132.51 | 120.91 | 94.24 | 141.19  |
|  M4 Yearly | 529.96 | 428.94 | 429.69 | 427.24 | 493.19 | 456.65 | 472.12 | - | - | - | - | -  |
|  M4 Quarterly | 318.93 | 274.24 | 255.69 | 250.82 | 262.40 | 295.64 | 299.12 | 322.60 | 279.14 | 273.95 | 278.62 | 323.72  |
|  M4 Monthly | 291.89 | 249.73 | 242.18 | 244.21 | 243.12 | 280.83 | 285.76 | 289.33 | 295.71 | 268.57 | 310.75 | 477.20  |
|  M4 Weekly | 219.63 | 210.47 | 163.68 | 189.68 | 188.39 | 176.01 | 187.18 | 179.88 | 206.20 | 140.29 | 181.45 | 256.22  |
|  M4 Daily | 92.14 | 91.85 | 92.31 | 92.16 | 92.18 | 92.28 | 94.77 | 92.01 | 191.81 | 100.34 | 88.75 | 108.99  |
|  M4 Hourly | 49.20 | 49.21 | 33.77 | 63.13 | 30.75 | 14.21 | 11.94 | 19.80 | 20.69 | 19.91 | 16.60 | 16.65  |
|  Tourism Yearly | 4312.77 | 4085.98 | 4789.95 | 4271.06 | 4623.59 | 4340.90 | 4772.43 | 4811.91 | 4100.33 | 3911.97 | 4292.61 | 5100.47  |
|  Tourism Quarterly | 1921.00 | 1114.30 | 1176.19 | 1003.24 | 1047.01 | 992.12 | 1012.02 | 1077.92 | 984.98 | 868.63 | 1069.86 | 1178.66  |
|  Tourism Monthly | 967.57 | 478.45 | 492.46 | 457.04 | 462.53 | 474.72 | 464.27 | 464.51 | 414.92 | 458.19 | 452.88 | 466.42  |
|  CIF 2016 | 107.09 | 103.39 | 67.12 | 70.43 | 80.66 | 95.13 | 111.01 | 95.74 | 92.71 | 95.18 | 93.96 | 82.18  |
|  Aus. Electricity Demand | 626.71 | 653.88 | 440.53 | 971.67 | 1275.81 | 324.43 | 262.65 | 289.18 | 347.00 | 216.99 | 272.29 | 287.57  |
|  Dominick | 0.89 | 1.25 | 3.94 | 1.23 | 3.66 | 0.00 | 5.58 | 0.03 | 0.03 | 1.19 | 0.13 | 0.03  |
|  Bitcoin | 23205.45 | 23245.98 | 27294.27 | 23750.31 | 30614.26 | 25108.36 | 20939.08 | 23047.13 | 20700.93 | 35085.78 | 27945.00 | 21898.60  |
|  Pedestrian Counts | 67.40 | 67.52 | 131.83 | 78.79 | 448.38 | 17.02 | 21.73 | 18.27 | 18.52 | 28.04 | 15.00 | 19.75  |
|  Vehicle Trips | 6.03 | 6.50 | 4.43 | 6.60 | 6.07 | 6.97 | 5.47 | 5.50 | 4.80 | 6.40 | 4.63 | 6.43  |
|  KDD Cup | 27.75 | 27.74 | 22.25 | 28.17 | 31.06 | 18.00 | 17.54 | 17.80 | 26.41 | 24.72 | 15.89 | 23.47  |
|  Weather | 2.17 | 2.18 | 2.26 | 2.27 | 2.23 | 7.89 | 2.26 | 2.09 | 2.00 | 2.29 | 2.29 | 1.99  |
|  NNS Daily | 5.94 | 3.55 | 3.46 | 3.48 | 3.85 | 5.06 | 3.73 | 3.74 | 3.81 | 4.63 | 3.69 | 3.89  |
|  NNS Weekly | 14.18 | 13.90 | 13.73 | 14.27 | 14.82 | 12.84 | 13.77 | 13.85 | 13.25 | 12.88 | 17.40 | 18.09  |
|  Kaggle Daily | 51.05 | 51.64 | 49.61 | 69.27 | 46.27 | - | - | - | - | - | - | -  |
|  Kaggle Weekly | 357.12 | 355.50 | 278.00 | 312.88 | 609.62 | 494.38 | 1532.50 | 248.62 | 317.12 | 258.12 | 245.12 | 258.75  |
|  Solar 10 Minutes | 2.92 | 2.92 | 5.64 | 2.92 | 2.13 | 2.92 | 5.08 | 2.91 | 2.92 | 3.17 | - | 2.92  |
|  Solar Weekly | 1091.23 | 1103.20 | 780.04 | 1073.11 | 760.63 | 942.23 | 1362.51 | 916.82 | 660.87 | 1081.84 | 1519.05 | 510.46  |
|  Electricity Hourly | 210.20 | 210.20 | 127.05 | 272.73 | 215.60 | 137.88 | 188.12 | 96.86 | 83.70 | 92.78 | 78.30 | 96.55  |
|  Electricity Weekly | 10983.75 | 10447.12 | 6149.88 | 10992.50 | 6789.75 | 7090.88 | 6293.88 | 5798.12 | 8137.25 | 6310.00 | 8928.38 | 13803.38  |
|  Carpats | 0.33 | 0.25 | 0.42 | 0.33 | 0.33 | 0.25 | 0.42 | 0.17 | 0.17 | 0.92 | 0.25 | 0.17  |
|  FRED-MD | 1.89 | 1.94 | 1.99 | 2.35 | 2.73 | 41.36 | 4.37 | 3.26 | 2.61 | 2.31 | 4.21 | 11.50  |
|  Traffic Hourly | 0.02 | 0.02 | 0.02 | 0.03 | 0.03 | 0.02 | 0.02 | 0.01 | 0.01 | 0.01 | 0.01 | 0.01  |
|  Traffic Weekly | 0.92 | 0.92 | 0.94 | 0.92 | 0.98 | 0.93 | 0.94 | 0.93 | 0.99 | 0.88 | 1.00 | 1.25  |
|  Rideshare | 1.65 | 1.98 | 1.64 | 1.65 | 0.66 | 1.66 | 1.60 | 1.72 | 1.65 | 1.48 | 1.11 | 1.65  |
|  Hospital | 6.67 | 6.67 | 6.83 | 6.67 | 6.83 | 6.67 | 6.92 | 6.92 | 6.83 | 6.75 | 6.58 | 7.33  |
|  COVID Deaths | 2.23 | 4.42 | 1.80 | 1.65 | 1.78 | 6.77 | 3.60 | 2.00 | 3.73 | 1.72 | 2.28 | 10.48  |
|  Temperature Rain | 3.78 | 3.83 | 3.99 | 3.80 | 4.02 | 2.49 | 4.00 | 2.60 | 2.28 | 2.99 | 2.54 | 2.21  |
|  Sunspot | 4.93 | 4.93 | 2.57 | 4.93 | 2.57 | 3.83 | 2.27 | 7.97 | 0.77 | 14.47 | 0.17 | 0.13  |
|  Saugum River Flow | 21.50 | 21.49 | 22.26 | 30.69 | 22.38 | 25.24 | 21.28 | 22.98 | 23.51 | 27.92 | 22.17 | 28.06  |
|  US Births | 1192.20 | 586.93 | 399.00 | 419.73 | 526.33 | 574.93 | 441.70 | 557.87 | 424.93 | 422.00 | 504.40 | 452.87  |

### Page 26
Table 13: Mean RMSE results

|  Dataset | SEN | Theta | TRATS | ETS | cIMIR+ARIMA | PR | CalBoost | FENN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 193829.49 | 171458.07 | 116850.90 | 167739.02 | 175343.75 | 152038.68 | 217644.50 | 154309.80 | 173075.10 | 192489.80 | 312821.80 | 182850.60  |
|  M1 Quarterly | 2545.73 | 2282.85 | 2673.91 | 2408.47 | 2538.45 | 1909.31 | 2161.01 | 1871.85 | 2313.32 | 2267.27 | 2271.68 | 2231.50  |
|  M1 Monthly | 2725.83 | 2564.88 | 2594.48 | 2263.96 | 2450.61 | 2478.88 | 2461.68 | 2527.03 | 2202.19 | 2183.37 | 2578.93 | 3129.84  |
|  M1 Yearly | 1172.85 | 1106.03 | 1386.33 | 1189.21 | 1662.17 | 1181.81 | 1341.70 | 1256.21 | 1157.88 | 1117.37 | 1147.62 | 1084.75  |
|  M3 Quarterly | 670.56 | 567.70 | 653.61 | 598.73 | 650.76 | 605.50 | 697.96 | 621.73 | 606.56 | 582.83 | 606.75 | 619.18  |
|  M3 Monthly | 893.88 | 753.99 | 765.20 | 755.26 | 790.76 | 830.04 | 874.20 | 833.15 | 873.71 | 796.01 | 845.30 | 948.40  |
|  M3 Other | 309.68 | 242.11 | 216.95 | 224.08 | 220.77 | 262.31 | 349.90 | 266.69 | 277.74 | 248.53 | 276.07 | 271.02  |
|  M4 Yearly | 1154.49 | 1020.48 | 1099.85 | 1052.12 | 1230.35 | 1000.18 | 1065.02 | .. | .. | .. | .. | ..  |
|  M4 Quarterly | 732.82 | 673.15 | 672.74 | 674.27 | 709.99 | 711.93 | 714.21 | 735.84 | 700.32 | 684.65 | 696.96 | 739.06  |
|  M4 Monthly | 755.45 | 683.72 | 743.41 | 705.70 | 702.06 | 720.46 | 734.79 | 743.47 | 740.26 | 705.21 | 787.94 | 902.38  |
|  M4 Weekly | 412.60 | 405.17 | 356.74 | 408.50 | 386.30 | 350.29 | 420.84 | 399.10 | 422.18 | 330.78 | 437.26 | 456.90  |
|  M4 Daily | 209.75 | 210.37 | 208.36 | 229.97 | 212.64 | 213.01 | 263.13 | 209.44 | 243.48 | 221.69 | 220.45 | 233.63  |
|  M4 Hourly | 1476.81 | 1483.70 | 469.87 | 3830.44 | 1563.05 | 312.98 | 344.62 | 467.89 | 1095.10 | 501.19 | 468.09 | 391.22  |
|  Tourism Yearly | 106665.20 | 99914.21 | 105799.40 | 104700.51 | 108082.60 | 89645.61 | 87489.00 | 87931.79 | 78470.68 | 78241.67 | 77581.31 | 80089.25  |
|  Tourism Quarterly | 17270.57 | 9254.63 | 12001.48 | 10812.34 | 12564.77 | 11746.85 | 12787.97 | 12182.57 | 11761.96 | 11305.95 | 11546.58 | 11724.14  |
|  Tourism Monthly | 7039.35 | 2701.96 | 3661.51 | 2542.96 | 3132.40 | 2739.43 | 3102.76 | 2584.10 | 2359.87 | 2596.21 | 2694.22 | 2660.06  |
|  CIF 2016 | 657112.42 | 804654.19 | 940099.90 | 722397.37 | 526395.02 | 648890.31 | 705273.30 | 1629741.53 | 3532475.00 | 772924.30 | 6085242.41 | 4625974.00  |
|  Acc. Electricity Demand | 566.27 | 771.51 | 446.59 | 1404.02 | 1234.76 | 319.98 | 300.55 | 330.91 | 357.00 | 268.37 | 286.48 | 295.22  |
|  Denmark | 6.48 | 6.74 | 8.03 | 6.59 | 7.96 | 9.44 | 9.15 | 6.79 | 6.67 | 9.78 | 6.81 | 6.63  |
|  Bitcoin | $5.33 \times 10^{18}$ | $5.33 \times 10^{18}$ | $1.16 \times 10^{15}$ | $1.22 \times 10^{18}$ | $3.96 \times 10^{18}$ | $8.29 \times 10^{17}$ | $2.02 \times 10^{18}$ | $1.57 \times 10^{15}$ | $2.02 \times 10^{18}$ | $1.26 \times 10^{18}$ | $2.55 \times 10^{15}$ | $2.67 \times 10^{18}$  |
|  Pedestrian Counts | 228.14 | 228.20 | 261.25 | 278.26 | 820.28 | 61.84 | 60.78 | 67.17 | 65.77 | 99.33 | 67.99 | 70.17  |
|  Vehicle Trips | 36.53 | 37.44 | 25.69 | 37.61 | 34.95 | 31.69 | 27.28 | 27.88 | 26.46 | 33.56 | 28.99 | 32.98  |
|  KDD Cup | 73.81 | 73.83 | 71.21 | 76.71 | 82.66 | 68.20 | 65.71 | 68.43 | 80.39 | 80.39 | 68.87 | 76.21  |
|  Weather | 2.85 | 3.27 | 2.89 | 2.96 | 3.07 | 9.08 | 3.09 | 2.81 | 2.74 | 3.09 | 2.98 | 2.81  |
|  NNT Daily | 8.23 | 5.28 | 5.20 | 5.22 | 6.05 | 7.26 | 5.73 | 5.79 | 5.50 | 6.47 | 5.75 | 5.92  |
|  NNT Weekly | 18.82 | 18.85 | 18.53 | 18.82 | 18.55 | 18.62 | 18.67 | 18.29 | 18.53 | 17.35 | 24.16 | 24.02  |
|  Kaggle Daily | 590.11 | 583.32 | 740.74 | 650.43 | 595.43 |  |  |  |  |  |  |   |
|  Kaggle Weekly | 2970.78 | 3012.78 | 2951.87 | 3369.64 | 3777.28 | 4756.26 | 14040.64 | 2719.65 | 2961.91 | 2820.62 | 2719.37 | 3815.38  |
|  Solar 10 Minutes | 7.23 | 7.23 | 10.71 | 7.23 | 5.55 | 7.23 | 8.73 | 7.21 | 7.22 | 6.62 |  | 7.23  |
|  Solar Weekly | 1331.26 | 1341.55 | 1049.01 | 1264.43 | 967.87 | 1168.18 | 1754.22 | 1231.54 | 873.62 | 1307.78 | 2569.26 | 693.84  |
|  Electricity Hourly | 1026.29 | 1026.36 | 743.35 | 1524.87 | 1082.44 | 689.85 | 582.66 | 519.06 | 477.99 | 510.91 | 489.91 | 514.68  |
|  Electricity Weekly | 77067.87 | 76935.58 | 28039.73 | 70368.97 | 32594.81 | 47802.08 | 37289.74 | 30594.15 | 53188.26 | 35576.83 | 63916.89 | 78894.67  |
|  Cargents | 0.78 | 0.78 | 0.80 | 0.80 | 0.81 | 0.75 | 0.79 | 0.74 | 0.74 | 1.11 | 0.74 | 0.74  |
|  FREDARE | 3103.00 | 3898.72 | 2295.74 | 2341.72 | 3312.46 | 9736.93 | 2679.38 | 2631.04 | 4638.71 | 2812.97 | 2779.48 | 5098.91  |
|  Traffic Hourly | 0.04 | 0.04 | 0.05 | 0.04 | 0.04 | 0.03 | 0.03 | 0.02 | 0.02 | 0.02 | 0.03 | 0.02  |
|  Traffic Weekly | 1.51 | 1.53 | 1.53 | 1.53 | 1.54 | 1.50 | 1.50 | 1.55 | 1.51 | 1.44 | 1.61 | 1.54  |
|  Hotspot | 7.17 | 8.60 | 7.35 | 7.35 | 7.35 | 6.95 | 7.14 | 7.15 | 6.23 | 3.51 |  | 3.31  |
|  Hospital | 26.55 | 22.59 | 21.28 | 22.02 | 23.68 | 23.48 | 23.45 | 27.77 | 22.01 | 24.18 | 23.38 | 40.48  |
|  COSTS Deaths | 403.41 | 370.14 | 113.00 | 102.08 | 100.46 | 394.07 | 607.92 | 173.14 | 230.47 | 186.54 | 1135.41 | 479.96  |
|  Temperature Rain | 10.34 | 10.36 | 9.20 | 10.38 | 9.22 | 9.83 | 8.71 | 8.89 | 9.11 | 11.03 | 9.07 | 9.01  |
|  Sunspots | 4.95 | 4.95 | 2.97 | 4.95 | 2.96 | 3.95 | 2.38 | 8.43 | 3.14 | 14.52 | 0.66 | 0.52  |
|  Saugem River Flow | 39.79 | 39.79 | 42.58 | 50.39 | 43.23 | 47.70 | 39.32 | 40.64 | 45.28 | 48.91 | 42.99 | 49.12  |
|  US Births | 1369.50 | 735.51 | 686.54 | 607.20 | 705.51 | 732.09 | 618.38 | 726.72 | 683.99 | 627.74 | 768.81 | 686.51  |

### Page 27
Table 14: Median RMSE results

|  Dataset | SES | Theta | TBATS | ETS | (DHR-)ARIMA | PR | CatBoost | FFNN | DeepAR | N-BEATS | WaveNet | Transformer  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  M1 Yearly | 416.37 | 323.31 | 204.19 | 230.39 | 207.82 | 304.77 | 307.53 | 270.54 | 318.09 | 343.93 | 279.93 | 261.07  |
|  M1 Quarterly | 24.46 | 22.81 | 22.32 | 21.86 | 20.23 | 22.53 | 21.64 | 22.76 | 22.68 | 19.72 | 21.05 | 38.22  |
|  M1 Monthly | 54.67 | 46.40 | 44.04 | 44.39 | 47.11 | 45.35 | 45.58 | 45.32 | 43.82 | 42.49 | 51.44 | 80.42  |
|  M3 Yearly | 803.71 | 740.10 | 752.69 | 758.62 | 814.68 | 824.55 | 983.36 | 878.49 | 844.17 | 735.77 | 789.33 | 735.15  |
|  M3 Quarterly | 436.25 | 355.79 | 400.01 | 368.91 | 405.87 | 378.31 | 477.45 | 388.98 | 371.19 | 371.98 | 386.83 | 685.63  |
|  M3 Monthly | 633.56 | 516.79 | 493.19 | 495.97 | 497.97 | 582.04 | 628.56 | 582.51 | 632.19 | 547.24 | 599.23 | 723.72  |
|  M3 Other | 182.17 | 120.84 | 107.69 | 99.97 | 92.60 | 144.46 | 172.33 | 152.99 | 150.90 | 145.58 | 108.67 | 165.94  |
|  M4 Yearly | 610.38 | 497.80 | 495.02 | 494.90 | 567.70 | 525.42 | 547.34 | - | - | - | - | -  |
|  M4 Quarterly | 378.29 | 322.60 | 302.41 | 297.17 | 310.08 | 346.99 | 355.10 | 379.82 | 333.25 | 325.51 | 327.02 | 374.32  |
|  M4 Monthly | 348.59 | 299.02 | 290.01 | 293.25 | 292.51 | 333.30 | 340.25 | 352.49 | 351.00 | 319.98 | 368.61 | 534.24  |
|  M4 Weekly | 262.04 | 242.14 | 197.26 | 228.04 | 224.55 | 223.12 | 225.54 | 216.39 | 247.33 | 176.08 | 224.76 | 314.41  |
|  M4 Daily | 108.04 | 108.55 | 108.64 | 108.77 | 108.40 | 108.48 | 111.59 | 109.28 | 226.23 | 118.05 | 106.20 | 128.68  |
|  M4 Hourly | 61.40 | 61.58 | 42.90 | 78.21 | 42.93 | 19.89 | 16.92 | 26.45 | 27.42 | 30.67 | 24.17 | 22.66  |
|  Tourism Yearly | 4718.37 | 4615.95 | 5156.83 | 4626.74 | 5174.76 | 4717.10 | 5152.45 | 5418.40 | 4628.83 | 4241.97 | 4604.76 | 5338.69  |
|  Tourism Quarterly | 2295.67 | 1392.89 | 1470.61 | 1207.24 | 1196.05 | 1184.48 | 1219.62 | 1257.15 | 1140.29 | 1086.34 | 1224.35 | 1343.06  |
|  Tourism Monthly | 1250.26 | 675.10 | 670.85 | 598.88 | 603.66 | 596.26 | 603.96 | 604.81 | 511.55 | 582.93 | 598.19 | 601.31  |
|  CIF 2016 | 129.06 | 118.29 | 79.03 | 85.77 | 103.14 | 109.09 | 133.17 | 113.84 | 109.79 | 111.84 | 112.46 | 100.75  |
|  Aus. Electricity Demand | 771.69 | 797.84 | 544.49 | 1002.91 | 1513.03 | 404.47 | 338.18 | 376.77 | 433.76 | 271.70 | 354.74 | 369.17  |
|  Dominick | 0.93 | 1.32 | 4.51 | 1.29 | 4.00 | 0.00 | 6.17 | 0.04 | 0.03 | 1.46 | 0.13 | 0.03  |
|  Bitcoin | 30307.40 | 30549.40 | 33027.85 | 30863.47 | 38608.99 | 31356.35 | 28300.58 | 30298.77 | 26288.62 | 42326.66 | 33268.12 | 27629.30  |
|  Pedestrian Counts | 88.65 | 88.76 | 155.94 | 103.60 | 627.43 | 22.09 | 29.18 | 26.13 | 25.16 | 39.69 | 21.02 | 26.30  |
|  Vehicle Trips | 8.10 | 8.35 | 5.58 | 8.51 | 7.86 | 8.73 | 6.93 | 6.98 | 5.90 | 7.94 | 6.38 | 7.96  |
|  KDD Cup | 30.66 | 30.64 | 25.60 | 31.55 | 40.08 | 22.37 | 21.44 | 21.94 | 33.47 | 33.30 | 20.73 | 28.05  |
|  Weather | 2.67 | 2.68 | 2.72 | 2.76 | 2.76 | 8.74 | 2.74 | 2.64 | 2.53 | 2.86 | 2.85 | 2.61  |
|  NN5 Daily | 7.46 | 4.95 | 4.75 | 4.86 | 5.42 | 6.80 | 5.22 | 5.25 | 5.20 | 5.94 | 5.32 | 5.59  |
|  NN5 Weekly | 17.52 | 16.82 | 16.99 | 17.52 | 17.49 | 16.26 | 16.66 | 16.79 | 16.55 | 16.15 | 21.14 | 21.85  |
|  Kaggle Daily | 74.58 | 75.16 | 72.33 | 98.97 | 68.13 | - | - | - | - | - | - | -  |
|  Kaggle Weekly | 424.02 | 429.71 | 346.60 | 383.71 | 707.60 | 576.40 | 1823.75 | 313.51 | 382.89 | 331.06 | 310.14 | 324.99  |
|  Solar 10 Minutes | 6.59 | 6.60 | 7.47 | 6.59 | 5.05 | 6.59 | 7.84 | 6.57 | 6.59 | 5.79 | - | 6.59  |
|  Solar Weekly | 1193.90 | 1214.27 | 885.59 | 1163.10 | 878.01 | 1016.25 | 1509.43 | 1029.77 | 798.62 | 1174.02 | 1681.08 | 581.58  |
|  Electricity Hourly | 256.22 | 256.22 | 181.79 | 335.10 | 275.52 | 171.57 | 154.67 | 140.63 | 121.42 | 128.54 | 128.07 | 131.61  |
|  Electricity Weekly | 12460.16 | 11805.76 | 7278.04 | 12460.16 | 8268.55 | 8237.57 | 7480.76 | 7142.54 | 9296.76 | 7731.79 | 9866.38 | 14698.65  |
|  Carpats | 0.71 | 0.65 | 0.71 | 0.71 | 0.71 | 0.58 | 0.71 | 0.50 | 0.50 | 1.00 | 0.58 | 0.50  |
|  FRED-MD | 2.31 | 2.36 | 2.52 | 2.70 | 3.49 | 45.18 | 5.01 | 3.75 | 2.91 | 2.66 | 4.55 | 12.50  |
|  Traffic Hourly | 0.03 | 0.03 | 0.03 | 0.03 | 0.04 | 0.02 | 0.03 | 0.02 | 0.02 | 0.02 | 0.02 | 0.02  |
|  Traffic Weekly | 1.20 | 1.22 | 1.21 | 1.21 | 1.21 | 1.19 | 1.17 | 1.23 | 1.21 | 1.14 | 1.32 | 1.67  |
|  Rideshare | 1.84 | 2.19 | 1.85 | 1.84 | 1.03 | 1.84 | 1.80 | 1.83 | 1.83 | 1.56 | 1.42 | 1.84  |
|  Hospital | 8.26 | 8.20 | 8.36 | 8.25 | 8.45 | 8.25 | 8.50 | 8.47 | 8.27 | 8.31 | 8.26 | 8.93  |
|  COVID Deaths | 3.09 | 5.29 | 2.13 | 2.21 | 2.16 | 8.28 | 4.25 | 2.38 | 4.30 | 2.13 | 3.09 | 12.39  |
|  Temperature Rain | 5.74 | 5.76 | 5.77 | 5.78 | 5.75 | 5.48 | 5.45 | 5.35 | 5.44 | 6.03 | 5.47 | 4.99  |
|  Sunspot | 4.95 | 4.95 | 2.97 | 4.95 | 2.96 | 3.95 | 2.38 | 8.43 | 1.14 | 14.52 | 0.66 | 0.52  |
|  Saugum River Flow | 39.79 | 39.79 | 42.58 | 50.39 | 43.23 | 47.70 | 39.32 | 40.64 | 45.28 | 48.91 | 42.99 | 49.12  |
|  US Births | 1369.50 | 735.51 | 606.54 | 607.20 | 705.51 | 732.09 | 618.38 | 726.72 | 683.99 | 627.74 | 768.81 | 686.51  |

### Page 28
# D Execution times 

Table 15 shows the execution times corresponding with the SES, Theta, TBATS, ETS, ARIMA/DHRARIMA, PR, CatBoost, FFNN, DeepAR, N-BEATS, WaveNet and Transformer models across all datasets. The times are rounded to their closest hours, minutes and seconds, accordingly.
The experiments are run on an Intel(R) Core(TM) i7-8700 processor (3.2GHz) and 65GB of main memory.

Table 15: Execution times of baseline models. The times are formatted as hhh:mm:ss where h, m, and s refer to hours, minutes, and seconds. Leading zeros are omitted.

| Dataset | SES | Theta | TBATS | ETS | (DHR-) <br> ARIMA | PR | Cat FFNN <br> Boost | Deep <br> AR BEATS | N- <br> Net | Wave <br> for | Trans <br> former |
| :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: | :--: |
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
| Kaggle Daily | 96:00:00 | 96:00:00 | 240:00:00 | 120:00:00 | 168:00:00 | - | - | - | - | - | - | - |
| Kaggle Weekly | 13:00:00 | 14:00:00 | 120:00:00 | 15:00:00 | 17:00:00 | 24:00:00 | 24:00:00 | 1:00 | 10:00 | 3:00:00 | 6:00:00 | 20:00 |
| Solar 10 Minutes | 44 | 48 | 17:00:00 | 3:00 | 24 | 3:00 | 9:00 | 3:00 | 1:00:00 | 13:00 | - | $-6: 00: 00$ |
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
| Sunspot | 1 | 1 | 2:00 | 12 | 4:00 | 30 | 3 | 2:00 | 10:00 | 13:00 | 24:00 | 5:00 |
| Saugeen River Flow | 1 | 1 | 1:00 | 22 | 35 | 9 | 2 | 35 | 7:00 | 10:00 | 27:00 | 3:00 |
| US Births | 1 | 1 | 40 | 4 | 13 | 3 | 2 | 30 | 6:00 | 10:00 | 28:00 | 3:00 |

## References

[1] G. Lai, W.-C. Chang, Y. Yang, and H. Liu. Modeling long- and short-term temporal patterns with deep neural networks. In The 41st International ACM SIGIR Conference on Research and Development in Information Retrieval, page 95-104, New York, NY, USA, 2018.
[2] Kaggle. https://www.kaggle.com/, 2019.
[3] Center for Systems Science and Engineering at Johns Hopkins University. COVID-19 data repository. https://github.com/CSSEGISandData/COVID-19, 2020.
[4] S. Makridakis, A. Andersen, R. F. Carbone, R. Fildes, M. Hibon, R. Lewandowski, J. Newton, E. Parzen, and R. L. Winkler. The accuracy of extrapolation (time series) methods: results of a forecasting competition. Journal of Forecasting, 1(2):111-153, 1982.

### Page 29
[5] G. Zhang, B. E. Patuwo, and M. Y. Hu. Forecasting with artificial neural networks:: the state of the art. International Journal of Forecasting, 14(1):35-62, 1998.
[6] G. P. Zhang. Time series forecasting using a hybrid arima and neural network model. Neurocomputing, 50:159 - 175, 2003. ISSN 0925-2312.
[7] R. J. Hyndman and Y. Khandakar. Automatic time series forecasting: the forecast package for R. Journal of Statistical Software, 27(3):1-22, 2008. URL http://www.jstatsoft.org/ v27/i03.
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
[45] T. Afanasieva, N. Yarushkina, and I. Sibirev. Time series clustering using numerical and fuzzy representations. In 2017 Joint 17th World Congress of International Fuzzy Systems Association and 9th International Conference on Soft Computing and Intelligent Systems (IFSA-SCIS), pages $1-7,2017$.
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
[59] R. J. Hyndman. expsmooth: data sets from forecasting with exponential smoothing. https : //cran.r-project.org/web/packages/expsmooth, 2015.
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
[87] A. I. McLeod and H. Gweon. Optimal deseasonalization for monthly and daily geophysical time series. Journal of Environmental Statistics, 4(11), 2013. URL http://www.jenvstat. org/v04/il1.
[88] A. Bauer, M. Züfle, N. Herbst, S. Kounev, and V. Curtef. Telescope: an automatic feature extraction and transformation approach for time series forecasting on a level-playing field. In 2020 IEEE 36th International Conference on Data Engineering (ICDE), pages 1902-1905, 2020.
[89] R. Pruim, D. Kaplan, and N. Horton. mosaicData: project MOSAIC Data Sets, 2020. URL https://CRAN.R-project.org/package=mosaicData.