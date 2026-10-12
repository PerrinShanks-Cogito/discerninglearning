---
date: 2025-02-02
title: "Statistics Glossary"
description: "An A-Z of statistics and Lean Six Sigma terms."
permalink: /statistics-glossary/
---

<nav class="glossary-nav" markdown="1">
[\#](#num) [A](#A) [B](#B) [C](#C) [D](#D) [E](#E) [F](#F) [G](#G) [H](#H) [I](#I) [J](#J) [K](#K) [L](#L) [M](#M) [N](#N) [O](#O) [P](#P) [Q](#Q) [R](#R) [S](#S) [T](#T) [U](#U) [V](#V) [W](#W) [X](#X) [Y](#Y) [Z](#Z)
</nav>

## # {#num}

**1-proportion test**<br>
Used to compare the proportion of a sample against a known reference value. e.g. the number of people in a sample who follow a high-salt diet.

**1-sample t-test**<br>
Used to compare the mean of a single sample against a numerical reference value. For example, is the mean BMI of a sample of patients different to 25?

Ho: Sample mean = 25 versus Ha: Sample mean ≠ 25

Compare the reference value with the 95% confidence interval for the mean. If the reference value lies outside the confidence interval then the sample mean is significantly different to it.

**1-tailed t-test**<br>
Used when we are only interested in whether one sample mean is either greater than or less than a second sample mean. This results in an alternate hypothesis which specifies a direction.

Ha: Sample Mean A > Sample Mean B or Ha: Sample Mean A < Sample Mean B

This test provides more power to detect an effect in one direction by not testing the effect in the other direction. If you have a scenario where only one direction is important/valuable then this test is appropriate; for example you want to know if your product is cheaper; but you don’t gain value in knowing if it is more expensive.

**2-proportions test**<br>
Used to compare the proportions from two groups/samples. Used for attribute type data where the results can be summarised as a 2×2 table.<br>
Events = number of data points with a specific attribute e.g. lung cancer.<br>
Trials = total number of data points

**2-sample t-test**<br>
Commonly used to show whether the means of two samples are different e.g. whether male patients are different to female. A variant is the paired t-test (see below). To perform the test, both sets of data should be normally distributed. If the p-value is greater than 0.05 then we accept the null hypothesis that there is no difference between the two sample means. If the p-value is less than 0.05 then we reject the null hypothesis (if p is low, the null must go) and conclude that the two sample means are different.

**2-tailed t-test**<br>
Used to test whether two sample means are significantly different.<br>
Ha: Sample Mean A ≠ Sample Mean B

## A {#A}

**Alpha Risk/Error**<br>
The risk of rejecting the null hypothesis when it is actually true: type I error or false positive. Analogous to convicting an innocent defendant in a legal case. Mainly determined by sample size: the smaller the sample, the larger the Alpha Risk. Conventionally set to 5%.

**Anderson-Darling Test**<br>
Determine whether a sample of data follows a specified distribution. Commonly applied to test for normality. See also Normal Probability Plot. If p<0.05 then we reject the null hypothesis and conclude that the data is not normally distributed (if p is low the null must go).

**ANOVA**<br>
Analysis of variance (ANOVA) is used to analyse the difference between means of two or more factors each with 2 or more levels. A one-way ANOVA analyses the differences between the levels of a single factor. A two-way ANOVA analyses the differences between the levels of two factors simultaneously. By assessing the associated p-values, you can determine whether a factor is statistically significant. Assumes homogeneity of variance within levels if not use Kruskal Wallis test instead. To check for homogeneity use Bartlett’s or Levene’s test.

**Attribute Agreement Analysis (AAA)**<br>
Methodology for checking the reliability of a measurement system for qualitative data. AAA measures whether or not several people making a judgment or assessment of the same item have a high level of agreement among themselves by evaluating the repeatability, reproducibility and overall accuracy of the appraisers.

## B {#B}

**Bartlett’s Test**<br>
Used to test whether K groups/samples have equal variances. Bartlett’s test is more sensitive to non-normal data than Levene’s test. If you are confident that your data is normally distributed then Bartlett’s test is preferred. The test provides a statistic and associated p-value. If p<0.05 then we reject the null hypothesis and conclude that at least two of the variances are different (if p is low the null must go).

**Beta Risk/Error**<br>
The risk of failing to reject the null hypothesis when it is actually false: type II error or false negative. Analogous to releasing a guilty defendant in a legal case. Affected by sample size and the minimum difference you’re trying to detect. Typically lies in the range 10-20%. Power is equal to 1-Beta.

**Binomial Distribution**

**Box Plots**<br>
Visual representation of the median, minimum, maximum and interquartile range of different groups. The width of the box equals the interquartile range. They allow you to compare the location, dispersion and shape of the distribution of each group whilst also highlighting any outliers.

## C {#C}

**Canonical**

**C Chart**<br>
A C chart is an attribute control chart used to monitor the number of defects. The limits of the control chart are based on the Poisson distribution. Used to monitor the number of defects over time. The chart assesses trends and patterns in counts of events often expressed per time period (e.g. the number of falls per month in a certain hospital). For the C chart, there is no such thing as non-defects e.g. number of patients who didn’t fall. The centre line represents the average number of defects.

**Censoring**<br>
Occurs in reliability analysis and life testing when an observation is not completely known. For example, in a 17 year study of the survival of pancreatic cancer patients, anyone still alive at the end of the study is defined as censored. We know they survived for 17 years but we won’t know exactly when they died as patient follow-up ceased at study end (right censoring there is also left censoring).

**Central Limit Theorem**<br>
The distribution of sample means will follow a normal distribution. This applies regardless of the distribution of the underlying data. The theorem is important because it implies that statistical methods that work for normal distributions can be applied to problems involving other types of distributions.

**Chi-Squared Test**<br>
Used to test whether two categorical variables (the rows and columns of a contingency table) are independent of each other. E.g. do Did Not Attend rates depend on patient age? The chi-squared test compares the observed results with those expected if there was no association between the two categorical variables (rows and columns). The test provides a statistic and associated p-value. If p<0.05 then we reject the null hypothesis and conclude that there is a dependency between the two categorical variables.

**Common Cause Variation**<br>
Common cause variation is expected, natural variation that’s part of a stable process. Common cause variation is predictable and ongoing. There are no simple cures for common cause variation. Need to drill down and identify specific causes of variation, leading to fundamental changes to the process. Treating common cause variation as special cause will lead to unnecessary and costly process tampering.

**Confidence Interval**<br>
A confidence interval provides a range of estimation for an unknown statistic e.g. the population mean. Factors affecting the width of the confidence interval include the sample size, the sample variability and the confidence level. A 95% confidence interval for the sample mean implies that the true population mean will lie within the lower and upper values about 95 times out of 100. A 95% confidence interval for the mean is approximately ± 2 standard errors either side. The standard error is the standard deviation divided by the square root of the sample size.

**Correlation Coefficient**<br>
Measures the strength of the linear relationship between two continuous variables. Usually represented as r or R. R-squared is the square of the correlation coefficient. Used in linear regression to determine the degree of association between two continuous variables. The correlation coefficient ranges from -1 to 1. A correlation coefficient of -1 describes a perfect negative, or inverse, correlation, with values of one variable rising as those in the other decline. A value of 1 indicates a perfect positive correlation. A value of 0 indicates that there is no linear relationship between the two variables. Correlation doesn’t indicate causation <https://www.tylervigen.com/spurious-correlations>

## D {#D}

**Dispersion**<br>
Dispersion (or spread) is a means of describing the extent of variation of a distribution around its central value (e.g. mean). The most important are: standard deviation, range and interquartile range. Lower dispersion indicates higher precision in the manufacturing process or data measurements.

## E {#E}

**Expected Value (Chi-Squared Test)**<br>
The value you would expect if there is no association between the rows and columns (categorical variables) of a contingency table. Expected values are compared with actual values to calculate the Chi-squared statistic and associated p-value. The expected value for any cell is the row total multiplied by the column total divided by the grand total.

**Exponential growth**

## F {#F}

## G {#G}

**Gauge (Gage) R&R** <br>
Gauge R&R (Reproducibility and Repeatability) is relevant for continuous data. It is a type of Measurement System Analysis (MSA) which assesses the amount of variability caused by the measurement system itself and compares it to the total variability observed and the specification range (tolerance) to determine the viability of the measurement system.

Used when you want to assess the variability of a measurement system itself before embarking on expensive and time-consuming process improvement work. A Gauge R&R typically involves 2-4 people/operators and 10-20 items/parts with each measurement repeated 2-3 times. You are interested in the variation rather than the actual values. Criteria for acceptability of % study variation and precision to tolerance are:

1) Under 10%: measurement system acceptable<br>
2) 10-30%: measurement system may be acceptable<br>
3) Over 30%: measurement system is unacceptable and should be improved or replaced.

## H {#H}

**Hazard Function**<br>
In reliability analysis and life testing, e.g. the survival times of cancer patients, the hazard function shows the instantaneous failure rate at time t, having survived to that point in time. Used to assess the failure rate over time. For a Weibull distribution:

Shape > 1: failure rate is increasing<br>
Shape < 1: failure rate is decreasing<br>
Shape = 1: failure rate is constant

**Histogram**<br>
A plot showing the frequency distribution of continuous data. Each data point is allocated to one of several (usually) equally-sized bins. Histograms are useful for assessing the distribution of continuous variables, looking at things like shape, symmetry, skewness, bimodality etc.

**Hypothesis Testing**<br>
A statistical hypothesis is an unproven statement which can be tested using data. A hypothesis test determines whether the statement is true based on probability. There are two mutually exclusive hypotheses:<br>
Null hypothesis (H0): there is no difference between the populations you are testing<br>
Alternate hypothesis (Ha): the populations being tested are different

Used to test whether a hypothesis is true based on data. A t-test is an example of a hypothesis test. A hypothesis test produces a p-value which is the probability that H0 is true based on the data. Conventionally, if p<0.05 H0 is rejected and we accept the alternate hypothesis (if p is low the null must go). There are 5 steps to a hypothesis test:

1. State the null and alternate hypotheses<br>
2. Collect data<br>
3. Perform a statistical test e.g. a t-test<br>
4. Decide whether to accept or reject the null hypothesis<br>
5. Present your findings

## I {#I}

**I-MR Chart (Individuals & Moving Range)**<br>
The I-MR chart is a type of control chart which is actually a combination of two charts:

1. Individuals (I) chart: plots the individual data points<br>
2. Moving Range (MR) chart: plots the absolute differences between each pair of successive data points

The I-MR chart displays both the trend and the variation in the process. The I chart monitors the mean of the process, helping to identify trends, shifts, special causes etc. The MR chart monitors the variation in the process, helping to identify shifts and special causes.

## J {#J}

**Jenson’s Inequality**

## K {#K}

**Kappa Value**<br>
The Kappa value measures the degree of agreement between appraisers/operators and determines how much better the appraisers’ ratings are than random guesswork. The Kappa value is used in Attribute Agreement Analysis to determine the degree of agreement between and within appraisers. Kappa ranges from −1 to +1 with 1 indicating perfect agreement. A Kappa value below 0 indicates little or no agreement. A Kappa value above about 0.75 should be good enough for improvement purposes

**Kendall’s Coefficient of Concordance**<br>
Used to measure agreement within and between appraisers in Attribute Agreement Analysis when the categories are ordered e.g. criticality of defect: no defect, minor, major, critical. Kendall’s coefficient of concordance replaces the Kappa value in ordinal Attribute Agreement Analyses to determine the degree of agreement between and within appraisers. The coefficient ranges from 0 to 1 with 1 indicating perfect agreement. A value of 0 suggests that the assessors’ responses are essentially random. A coefficient above about 0.75 should be good enough for improvement purposes whilst a value above 0.9 is considered very good.

**Kendall’s Correlation Coefficient**<br>
Used to measure agreement between appraisers and a standard in Attribute Agreement Analysis when the categories are ordered e.g. criticality of defect: no defect, minor, major, critical. Kendall’s correlation coefficient replaces the Kappa value in ordinal Attribute Agreement Analyses to determine the degree of agreement between appraisers and known standards. The coefficient ranges from -1 to 1 with 1 indicating perfect agreement. A value of 0 indicates no agreement whilst a value of -1 indicates perfect disagreement. A value above 0.9 is considered very good.

## L {#L}

**Levene’s Test**<br>
Used to test whether k groups/samples have equal variances. Levene’s test is less sensitive to non-normal data than Bartlett’s test. If you are uncertain that your data is normally distributed then Levene’s test is preferred. The test provides a statistic and associated p-value. If p<0.05 then we reject the null hypothesis and conclude that at least two of the variances are different (if p is low the null must go).

**Linear Regression Model**<br>
Linear regression is a statistical model which estimates the linear relationship between a response variable (Y) and one or more explanatory variables (X). The situation with one explanatory variable is called simple linear regression. Simple linear regression is used to fit a straight line between two continuous variables, typically an X-variable and a Y-variable. The goodness of fit is measured by the R-Squared and adjusted R-squared values. The equation of a straight line has two parameters (intercept and slope):<br>
Y = Intercept + Slope \* X

**Location**<br>
In descriptive statistics we use location measures in order to describe the central value or central position of a distribution (also known as centring). The most important are: mean, median and mode.

**Long Term Variation**<br>
In the long term, processes experience special causes and the process mean changes. Therefore, long term variation is defined as any variation with common causes and special causes. In the long term, process capability will be lower (worse). In Six Sigma methodology, it is assumed that a process will shift by ± 1.5σ over a long period of time. Pp and Ppk measures are used for long term process capability.

## M {#M}

**Multiple Regression Model**<br>
Multiple linear regression is a statistical model relating a Y-variable (output) to two or more X-variables (inputs). Used to fit a model between a Y-variable and two or more X-variables. The goodness of fit is measured by the R-Squared and adjusted R-Squared values. The multiple regression equation has the following form:<br>
Y = Intercept + Slope1 \* X1 + Slope2 \* X2 + Slope3 \* X3 etc

## N {#N}

**Normal Probability Plot**<br>
A graphical technique for visually assessing whether or not a dataset is normally distributed. The data are plotted against a theoretical normal distribution in such a way that the points should lie on a straight line if they come from a normal distribution. The plot is commonly used in conjunction with the Anderson-Darling test for normality and whether a transformation may be necessary.

**NP Chart**<br>
An NP chart is an attribute control chart used to monitor the number of defective units in a sample of constant size. The limits of the control chart are based on the Binomial distribution. Used to monitor the number of defective units over time. The chart assesses trends and patterns in counts of binary events (e.g. pass, fail). The centre line represents the average number of non-conforming units.

N = number in sample<br>
P = probability of non-conformance<br>
Number non-conforming = N x P

**Null Hypothesis**<br>
The statistical hypothesis that there is no difference between groups or no relationship between variables. It is used in conjunction with the alternate hypothesis in hypothesis testing e.g. a t-test. Used in hypothesis testing to determine whether there is a difference between groups. A hypothesis test produces a p-value which is the probability that H0 is true based on the data. Conventionally, if p<0.05 H0 is rejected (if p is low the null must go).

## O {#O}

**Operational Definition**<br>
An operational definition, when applied to data collection, is a clear, concise and detailed definition of a measure. The need for operational definitions is fundamental when collecting all types of data, particularly where humans are involved. It is particularly important when a decision is being made about whether something is correct or incorrect, or when a visual check is being made where there is potential for confusion.

## P {#P}

**Paired t-test**<br>
Similar to a 2-sample t-test but used when the two samples come from a single population, e.g. before and after a treatment. The analysis boils down to whether the difference between the two sets of results is significantly different to zero. For example, comparing the blood pressure of a group of patients before and after going on a healthy diet regime for 3 months. In this case, both Before and After apply to the same patient.

**Poisson Distribution**

**Power**<br>
Power is the probability of correctly rejecting the null hypothesis when it’s false. It is the probability that a hypothesis test will detect a difference when it exists. If you are going to spend a lot of money and resources to test for a difference, you want to maximise the probability of detecting that difference. For example, a clinical trial to assess a promising new treatment for cancer.<br>
Power = 1 – Beta Risk

**Prediction Interval**<br>
A prediction interval is a type of confidence interval applied to predictions in regression analysis. The regression equation allows you to predict the Y-variable given specific values of the X-variables. The prediction interval provides a range for that prediction e.g. a 95% confidence interval.

**Process Capability (Cp, Cpk)**<br>
Measures how well a process meets customer requirements (voice of the customer). Process capability is the ratio of the voice of the customer to the voice of the process. Cp and Cpk are used for short term process capability.

Cp and Cpk are used to measure process capability when a process is under statistical control (no special causes, trends etc). In practice, Cp is rarely applied because it takes no account of the process mean which makes it over-optimistic when a process is not centred. Process capability is intrinsically linked to the % of defects:<br>
Cpk = 0.67: 4.55% defects<br>
Cpk = 1.00: 0.27% defects<br>
Cpk = 1.33: 0.0063% defects

**Process Capability (Pp, Ppk)**<br>
Pp and Ppk are used for long term process capability. Pp and Ppk are used to measure process capability when a process is under statistical control (no special causes, trends etc). In practice, Pp is rarely applied because it takes no account of the process mean which makes it over-optimistic when a process is not centred. Process capability is intrinsically linked to the % of defects:<br>
Ppk = 0.67: 4.55% defects<br>
Ppk = 1.00: 0.27% defects<br>
Ppk = 1.33: 0.0063% defects

**P-value**<br>
The p-value measures statistical significance in hypothesis testing. It is the probability that the null hypothesis is true based on the observed data. The p-value is the probability that H0 is true based on the observed data. Conventionally, if p<0.05 then H0 is rejected and we accept the alternate hypothesis (if p is low the null must go).

## Q {#Q}

## R {#R}

**Range**<br>
The range of a sample is the maximum value minus the minimum value. The range is a simple measure of dispersion. The range is not recommended for larger samples because it only depends on two values and so most of the data is ignored. As a result, it is also very sensitive to outliers.

**Repeatability**<br>
Variation when one person repeatedly measures the same thing using the same equipment. Quantifies how much variability in the measurement system is caused by the measurement device. Used in Gauge R&R to assess the effectiveness of a measurement system prior to conducting process improvement activities. High repeatability suggests that the measurement device needs to be changed/enhanced.

**Reproducibility**<br>
Variation when two or more people measure the same thing using the same equipment. Quantifies how much variability in the measurement system is caused by differences between operators. Used in Gauge R&R to assess the effectiveness of a measurement system prior to conducting process improvement activities. High reproducibility suggests that the operators need additional training.

**Residuals**<br>
In regression analysis, a residual is the difference between the actual observation and the fitted value based on the prediction equation. In regression analysis, the line of best fit through the data minimises the sum of squared residuals. There are three assumptions regarding the residuals in linear regression:<br>
1. They have constant variance across all values of X<br>
2. They are normally distributed<br>
3. They are random and independent of each other

**R-Squared**<br>
R-squared indicates how much variation in the Y-variable is explained by the X-variable(s). It is the square of the correlation coefficient expressed as a percentage.or example, in linear regression, an R-squared value of 60% indicates that 60% of the variability in Y has been explained by X. The higher the R-squared value the better.

The adjusted R-squared value is preferred to R-squared because it takes into account the complexity of the regression model in terms of how many X-variables are included. Adding superfluous X-variables to a multiple regression model will increase R-squared but decrease adjusted R-squared.

## S {#S}

**Sample Size**<br>
The sample size is the number of observations in a sample. For a two-sample t-test, the sample size is the number of data points in each group. For example, in a comparison of 50 men and 50 women, the sample size is 50. Choosing a sufficiently large sample is critical if you want to meet your study goals. In hypothesis testing, an appropriate sample size can be calculated based on the following inputs:<br>
1. The difference to be detected<br>
2. Power<br>
3. Standard deviation

**Simpson’s Paradox**

**Special Causes**<br>
Special causes are unexpected glitches which significantly impact a process. They are unusual, unpredictable and often one-off. Also known as assignable causes. It is important to identify special causes promptly and take action to ensure they don’t recur. The presence of special causes will negatively impact process capability. Special causes are identifiable using control charts. Common indicators of special cause variation include:<br>
1. Alternating: 14 points in a row alternating up and down<br>
2. Outlier: 1 point more than 3σ from centre line<br>
3. Shift: 9 points in a row on same side of centre line<br>
4. Trend: 6 points in a row, all increasing or all decreasing

**Specification Limits**<br>
Specification limits are the values within which the process should operate according to the customer. They therefore represent the voice of the customer.<br>
Upper Specification Limit: The highest value customers will accept.<br>
Lower Specification Limit: The lowest value customers will accept.<br>
The specification limits determine the process capability and the sigma value.

**Standard Deviation**<br>
Expresses how much variation there is in relation to the mean. The standard deviation is the square root of the variance. The population standard deviation is represented by the Greek letter σ (sigma), the sample standard deviation is represented by the letter s. It tells you, on average, how far each value lies from the mean. A high standard deviation means that values are generally far from the mean while a low standard deviation indicates that values are tightly clustered around the mean.

**Standard Error**<br>
When calculating confidence intervals of the sample mean, the standard error is the standard deviation divided by the square root of the sample size. Used to calculate confidence intervals. For example, a 95% confidence interval for the mean is approximately ± 2 standard errors either side of it.

**Survival Function**<br>
In reliability analysis and life testing, the survival function shows the probability of survival beyond a certain time. Commonly used in healthcare to model statistically the survival times of patients following a particular diagnosis.

## T {#T}

**Transformation**<br>
Transformation is a way of making non-normal data normal using a mathematical function. Square root/logarithmic transformations are used to normalise skewed distributions. The transformations replace the original data with either the square root or logarithm. This has the effect of squashing the x-axis of the distribution making it more normal. The effectiveness of a transformation can be assessed using the Anderson-Darling test.

## U {#U}

## V {#V}

**Variance Inflation Factor**<br>
The Variance Inflation Factor (VIF) indicates the severity of multicollinearity in multiple regression analysis. Multicollinearity exists when two or more X-variables are highly correlated with each other. VIFs range from 1 upwards. The value of VIFs indicate how much the variance is inflated for each regression coefficient due to multicollinearity. For example, a VIF of 1.9 indicates that the variance of a particular coefficient is 90% larger than would be expected if no multicollinearity existed among the X-variables. Multiple regression analysis can become unstable when there is a high degree of multicollinearity among the X-variables. As a guideline, a VIF greater than 5 can be considered problematic.

**Voice of the Customer**<br>
The Voice of the Customer (VOC) is the structured process of gathering the specifically stated performance needs and expectations of the customer regarding the products or services you provide to them. VOC is used in gauge R&R studies to assess the effectiveness of existing measurement systems. It is also used to calculate process capability which is the ratio of VOC to VOP. In numerical terms, VOC is characterised by the upper and lower specification limits.

**Voice of the Process**<br>
The Voice of the Process (VOP) defines the capability of your process to meet the needs and expectations of your customer. The VOP often comes from the use of common statistical tools such as control charts which will tell you whether your process is stable. Control charts will also tell you whether you are in control and whether you are exhibiting common cause or special cause variation. Process capability is the ratio of VOC to VOP. In numerical terms, VOP is characterised by the mean and standard deviation of the process.

## W {#W}

**Weibull Distribution**<br>
The Weibull distribution is a flexible distribution using in reliability analysis and life testing e.g. the survival times of cancer patients.The Weibull distribution is a versatile probability distribution which can take a wide variety of shapes. Indeed, it is flexible enough to model both left and right skewed data. If the variable t is time to failure, the Weibull distribution provides a failure rate that is proportional to time:<br>
Shape < 1: failure rate decreases over time e.g. rate of infant mortality <br>
Shape = 1: failure rate is constant over time <br>
Shape > 1: failure rate increases over time e.g. failure of a device due to wear and tear

## X {#X}

**X-bar R Chart**<br>
X-Bar R controls charts are a pair of charts presented in tandem. They are used when the data falls in subgroups e.g. four results per day. The X-bar chart monitors the subgroup means over time highlighting the location of the process. The R chart monitors the subgroup ranges over time highlighting the variability of the process. The X-bar R control chart is typically used for continuous data when the subgroup size is 8 or fewer.

## Y {#Y}

## Z {#Z}

**Z-test**
