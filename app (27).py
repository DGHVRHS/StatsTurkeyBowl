import streamlit as st
import random
import time

st.set_page_config(page_title="Stats Turkey Bowl", layout="wide")

# Question Bank organized by Play Tier (covering Stats HW #1 through HW #9)
QUESTION_BANK = {
    "Easy": [
        {
            "source": "HW #1 (Simulation & P-Value)",
            "q": "A player rolls a custom 6-sided die 30 times and gets 11 sixes. In 500 simulated trials of a fair die, 15 trials produced 11 or more sixes. What is the estimated p-value, and does it give convincing evidence the die is weighted?",
            "options": [
                "p-value = 0.03; Yes, because 0.03 < 0.05, so 11 sixes is unlikely to occur by chance alone.",
                "p-value = 0.30; No, because 0.30 > 0.05, so it easily happens by chance.",
                "p-value = 0.15; Yes, because 15 trials is more than 10.",
                "p-value = 0.03; No, because p-values must be greater than 0.50 to prove bias."
            ],
            "answer": "p-value = 0.03; Yes, because 0.03 < 0.05, so 11 sixes is unlikely to occur by chance alone.",
            "explanation": "15 / 500 = 0.03 (3%). Since 0.03 is below the standard 0.05 significance threshold, it is convincing evidence the die is unfair."
        },
        {
            "source": "HW #1 (Sampling Bias)",
            "q": "A wildlife biologist casts a net from a shallow dock near a public fish-feeding station and weighs the first 15 trout caught. How does this sampling method affect the estimated mean weight of trout in the entire lake?",
            "options": [
                "Convenience sample; it likely overestimates the true mean weight because larger fish gather near feeding stations.",
                "Simple Random Sample; it provides an unbiased estimate of all trout in the lake.",
                "Voluntary response sample; it underestimates the true mean weight.",
                "Stratified sample; it eliminates all sampling variability."
            ],
            "answer": "Convenience sample; it likely overestimates the true mean weight because larger fish gather near feeding stations.",
            "explanation": "Sampling easily accessible fish near a feeding station is a convenience sample that systematically favors well-fed, larger trout."
        },
        {
            "source": "HW #2 (Observational vs. Experiment)",
            "q": "Researchers tracked 2,200 middle schoolers' weekly strategy video game hours and gave them a cognitive speed test, finding gamers scored 15% higher. Can they conclude strategy games cause higher cognitive speed?",
            "options": [
                "No — this is an observational study with no random assignment, so confounding variables may explain the difference.",
                "Yes — the sample size of 2,200 students is large enough to prove cause-and-effect.",
                "Yes — because a standardized cognitive assessment was used to measure the response.",
                "No — because the researchers did not use a voluntary response sample."
            ],
            "answer": "No — this is an observational study with no random assignment, so confounding variables may explain the difference.",
            "explanation": "Without random assignment to treatments, this is an observational study and cannot establish cause-and-effect."
        },
        {
            "source": "HW #2 (Survey Bias)",
            "q": "A city mailed 8,000 paper surveys about a library tax increase, and 620 residents mailed them back (74% in favor). What major bias is present, and in what direction?",
            "options": [
                "Nonresponse bias; 74% likely overestimates true support because residents passionate about the library are more likely to return surveys.",
                "Undercoverage bias; 74% underestimates true support because property owners never vote.",
                "Response bias; 74% is exact because 620 is a large sample.",
                "Voluntary response bias; 74% underestimates support because of mailing costs."
            ],
            "answer": "Nonresponse bias; 74% likely overestimates true support because residents passionate about the library are more likely to return surveys.",
            "explanation": "Over 92% of selected households did not respond (nonresponse bias), skewing results toward strongly motivated supporters."
        },
        {
            "source": "HW #2 (Response Bias)",
            "q": "The Vice President of HR emails 400 employees asking: 'Have you ever inflated your reported hours on remote work timesheets?' Only 2% answer 'Yes.' What bias explains this?",
            "options": [
                "Response bias — employees fear punishment from HR and underreport sensitive behavior, making 2% an underestimate.",
                "Undercoverage bias — remote workers do not check company email.",
                "Voluntary response bias — 2% is an overestimate of true timesheet inflation.",
                "Random sampling error — 400 employees is too small to detect any pattern."
            ],
            "answer": "Response bias — employees fear punishment from HR and underreport sensitive behavior, making 2% an underestimate.",
            "explanation": "Asking employees directly from an HR executive's email creates strong social desirability/fear response bias."
        },
        {
            "source": "HW #3 (Scope of Inference)",
            "q": "A random sample of high school students is selected, and students are randomly assigned to either a new math study method or their usual method. What conclusion can be drawn?",
            "options": [
                "Causal inference for the entire population (both random selection and random assignment were used).",
                "Causal inference for the sample only (no generalization to the population).",
                "Generalization to the population only (no cause-and-effect conclusion).",
                "Neither generalization nor cause-and-effect."
            ],
            "answer": "Causal inference for the entire population (both random selection and random assignment were used).",
            "explanation": "Random selection allows generalization to the population; random assignment allows cause-and-effect conclusions."
        },
        {
            "source": "HW #4 (Variable Classification)",
            "q": "Which of the following variables recorded in a high school student survey is CATEGORICAL rather than quantitative?",
            "options": [
                "Zip code of a student's home address",
                "Distance a student travels to school (in miles)",
                "Time spent doing homework on Sunday evening (in minutes)",
                "Daily water intake (in fluid ounces)"
            ],
            "answer": "Zip code of a student's home address",
            "explanation": "Zip codes are numeric labels for geographic regions; averaging zip codes has no numerical meaning."
        },
        {
            "source": "HW #4 (Misleading Graphs)",
            "q": "A news bar chart starts its vertical axis at $55 instead of $0, making Provider B ($70/mo, 12-inch bar) look 3 times taller than Provider A ($60/mo, 4-inch bar). What is the ACTUAL percentage increase in cost?",
            "options": [
                "16.7% increase ($10 / $60)",
                "300% increase (12 in / 4 in)",
                "10% increase ($70 - $60)",
                "14.3% increase ($10 / $70)"
            ],
            "answer": "16.7% increase ($10 / $60)",
            "explanation": "The actual increase is ($70 - $60) / $60 = 10/60 ≈ 16.7%, even though truncating the axis makes the bar 3 times taller."
        }
    ],
    "Medium": [
        {
            "source": "HW #3 (Statistical Significance)",
            "q": "An experiment finds students chewing gum scored 7.5 points higher on average than non-gum chewers. In 100 random-assignment simulations assuming no effect, only 4 produced a difference ≥ 7.5. What should we conclude?",
            "options": [
                "Statistically significant evidence that chewing gum improves test scores (p = 0.04 < 0.05).",
                "Not statistically significant because 4 simulations still reached 7.5 points.",
                "Chewing gum had no effect; random chance easily explains a 7.5-point gap.",
                "The experiment failed because 24 volunteers is not a random sample."
            ],
            "answer": "Statistically significant evidence that chewing gum improves test scores (p = 0.04 < 0.05).",
            "explanation": "Since 4% (0.04) is less than 5%, the observed difference is unlikely to happen by random assignment alone."
        },
        {
            "source": "HW #4 (Histograms & Medians)",
            "q": "In a science exam distribution of 80 students, score intervals have counts: [50–59]: 4, [60–69]: 12, [70–79]: 28, [80–89]: 24, [90–99]: 12. What percentage of students scored below 80?",
            "options": [
                "55% (44 out of 80 students)",
                "35% (28 out of 80 students)",
                "45% (36 out of 80 students)",
                "20% (16 out of 80 students)"
            ],
            "answer": "55% (44 out of 80 students)",
            "explanation": "4 + 12 + 28 = 44 students scored below 80, and 44 / 80 = 0.55 = 55%."
        },
        {
            "source": "HW #5 (Resistant Statistics)",
            "q": "Home prices in a city are heavily skewed to the right due to a few luxury mansions over $5,000,000. Which pair of statistics is most appropriate to summarize center and spread?",
            "options": [
                "Median and Interquartile Range (IQR), because both are resistant to extreme skewness and outliers.",
                "Mean and Standard Deviation (SD), because they use every home price in the calculation.",
                "Mean and IQR, because the mean is unaffected by high outliers.",
                "Median and Range, because the range ignores luxury mansions."
            ],
            "answer": "Median and Interquartile Range (IQR), because both are resistant to extreme skewness and outliers.",
            "explanation": "Skewness and outliers pull the non-resistant mean and standard deviation upward, whereas the median and IQR remain resistant."
        },
        {
            "source": "HW #5 (5-Number Summary & IQR)",
            "q": "Nine students reported weekend video game hours: 2, 4, 5, 7, 8, 10, 11, 14, 18. What is the Interquartile Range (IQR) of this dataset?",
            "options": [
                "IQR = 8 hours (Q3 = 12.5, Q1 = 4.5)",
                "IQR = 16 hours (Max = 18, Min = 2)",
                "IQR = 6 hours (Q3 = 11, Q1 = 5)",
                "IQR = 8 hours (Median = 8)"
            ],
            "answer": "IQR = 8 hours (Q3 = 12.5, Q1 = 4.5)",
            "explanation": "The median is 8. The lower half {2, 4, 5, 7} has Q1 = 4.5; the upper half {10, 11, 14, 18} has Q3 = 12.5. IQR = 12.5 - 4.5 = 8."
        },
        {
            "source": "HW #5 (Sample Standard Deviation)",
            "q": "A hotline received 4, 6, 8, 11, and 11 calls per hour over 5 hours (mean = 8). Given that the squared deviations sum to 38, what is the sample standard deviation (s)?",
            "options": [
                "s ≈ 3.08 calls (√(38 / 4))",
                "s ≈ 2.76 calls (√(38 / 5))",
                "s = 9.50 calls (38 / 4)",
                "s = 7.60 calls (38 / 5)"
            ],
            "answer": "s ≈ 3.08 calls (√(38 / 4))",
            "explanation": "Sample variance is s² = 38 / (5 - 1) = 9.5, so sample standard deviation is s = √9.5 ≈ 3.08 calls."
        },
        {
            "source": "HW #6 (Z-Scores & Relative Standing)",
            "q": "Sam scored 680 on SAT Math (μ = 520, σ = 115) and 29 on ACT Math (μ = 20.8, σ = 5.2). On which test did Sam perform better relative to test-takers nationwide?",
            "options": [
                "ACT Math (z = +1.58 vs. SAT Math z = +1.39)",
                "SAT Math (z = +1.39 vs. ACT Math z = +1.58)",
                "Both performances were identical because both are above the mean.",
                "SAT Math, because 680 is a larger raw number than 29."
            ],
            "answer": "ACT Math (z = +1.58 vs. SAT Math z = +1.39)",
            "explanation": "z_SAT = (680 - 520)/115 ≈ +1.39, while z_ACT = (29 - 20.8)/5.2 ≈ +1.58. Higher positive z-score indicates better relative standing."
        },
        {
            "source": "HW #6 (Linear Transformations)",
            "q": "A teacher adds 12 bonus points (Y = X + 12) to an exam with mean 64, median 62, SD 10.5, and IQR 14. What are the new mean and new standard deviation?",
            "options": [
                "New Mean = 76 points; New SD = 10.5 points (adding a constant shifts center but does not change spread).",
                "New Mean = 76 points; New SD = 22.5 points (both center and spread increase by 12).",
                "New Mean = 64 points; New SD = 22.5 points.",
                "New Mean = 74 points; New SD = 12.0 points."
            ],
            "answer": "New Mean = 76 points; New SD = 10.5 points (adding a constant shifts center but does not change spread).",
            "explanation": "Adding 12 shifts every score up by 12 (mean becomes 64 + 12 = 76), while distances between scores stay unchanged (SD stays 10.5)."
        },
        {
            "source": "HW #6 (Rescaling & Shifting)",
            "q": "Taxi trip distances (mean = 4.8 mi, SD = 1.8 mi) are converted to total fare in dollars using Y = 3.50 + 2.20X. What are the mean and standard deviation of taxi fares?",
            "options": [
                "Mean = $14.06; SD = $3.96",
                "Mean = $14.06; SD = $7.46",
                "Mean = $10.56; SD = $3.96",
                "Mean = $14.06; SD = $1.80"
            ],
            "answer": "Mean = $14.06; SD = $3.96",
            "explanation": "Mean is affected by both multiplying and adding: 3.50 + 2.20(4.8) = $14.06. SD is affected only by multiplying: 2.20(1.8) = $3.96."
        }
    ],
    "Hard": [
        {
            "source": "HW #6 (Standardizing Distributions)",
            "q": "Employee commute times (right-skewed, μ = 32.6 min, σ = 8.4 min) are all converted to z-scores using Z = (X - 32.6) / 8.4. What are the mean, SD, and shape of Z?",
            "options": [
                "Mean = 0, SD = 1, and the shape remains right-skewed.",
                "Mean = 0, SD = 1, and the shape becomes approximately Normal (bell-shaped).",
                "Mean = 32.6, SD = 1, and the shape becomes symmetric.",
                "Mean = 0, SD = 8.4, and the shape remains right-skewed."
            ],
            "answer": "Mean = 0, SD = 1, and the shape remains right-skewed.",
            "explanation": "Standardizing centers a distribution at 0 with SD 1, but linear transformations never change the shape of a distribution."
        },
        {
            "source": "HW #7 (Empirical Rule)",
            "q": "Smartwatch battery life is approximately Normal with μ = 40 hours and σ = 4 hours. Using the 68–95–99.7 Empirical Rule, what percentage of watches last between 32 and 44 hours?",
            "options": [
                "81.5% (47.5% below the mean to -2σ, plus 34% above the mean to +1σ)",
                "68.0% (within 1 standard deviation of the mean)",
                "95.0% (within 2 standard deviations of the mean)",
                "83.85% (half of 99.7% plus 34%)"
            ],
            "answer": "81.5% (47.5% below the mean to -2σ, plus 34% above the mean to +1σ)",
            "explanation": "32 hours is z = -2 (half of 95% = 47.5% between 32 and 40) and 44 hours is z = +1 (half of 68% = 34% between 40 and 44). 47.5% + 34% = 81.5%."
        },
        {
            "source": "HW #7 (Bootstrap Margin of Error)",
            "q": "A sample of 50 students has a mean daily study time of 150 minutes. A bootstrap sampling distribution is Normal with mean 150 min and SD 6 min. What is the approximate 95% interval for the true population mean?",
            "options": [
                "138 to 162 minutes (150 ± 12 minutes)",
                "144 to 156 minutes (150 ± 6 minutes)",
                "132 to 168 minutes (150 ± 18 minutes)",
                "147 to 153 minutes (150 ± 3 minutes)"
            ],
            "answer": "138 to 162 minutes (150 ± 12 minutes)",
            "explanation": "By the Empirical Rule, 95% falls within 2 standard deviations: Margin of Error = 2(6) = 12 minutes, giving [138, 162]."
        },
        {
            "source": "HW #7 (Normal Percentiles)",
            "q": "Coffee bag weights are Normal with μ = 16.2 oz and σ = 0.4 oz. Roughly what percentage of bags weigh less than 15.5 oz (z = -1.75)?",
            "options": [
                "About 4.0% (P(Z < -1.75) = 0.0401)",
                "About 96.0% (P(Z > -1.75) = 0.9599)",
                "About 2.5% (using z = -2.0)",
                "About 8.0% (doubling the tail area)"
            ],
            "answer": "About 4.0% (P(Z < -1.75) = 0.0401)",
            "explanation": "z = (15.5 - 16.2) / 0.4 = -1.75. Looking up z = -1.75 in the standard normal table gives an area to the left of 0.0401 (4.01%)."
        },
        {
            "source": "HW #7 (Inverse Normal Calculation)",
            "q": "Bread loaf weights are Normal with σ = 15 g. Policy requires no more than 4% of loaves weigh under 450 g (4th percentile z ≈ -1.75). What minimum mean weight (μ) must the bakery target?",
            "options": [
                "μ = 476.25 grams (450 + 1.75 × 15)",
                "μ = 423.75 grams (450 - 1.75 × 15)",
                "μ = 465.00 grams (450 + 15)",
                "μ = 480.00 grams (450 + 2 × 15)"
            ],
            "answer": "μ = 476.25 grams (450 + 1.75 × 15)",
            "explanation": "Using -1.75 = (450 - μ) / 15 gives 450 - μ = -26.25, so μ = 476.25 grams."
        },
        {
            "source": "HW #8 (Conditional vs. Marginal)",
            "q": "In a two-way table of 20 students' transportation mode and breakfast habit, which question asks for a CONDITIONAL percentage?",
            "options": [
                "'Of those who walk or bike to school, what percent eat breakfast regularly?'",
                "'What percent of all 20 surveyed students walk or bike to school?'",
                "'What percent of all 20 surveyed students both walk/bike and eat breakfast?'",
                "'What is the grand total of students surveyed?'"
            ],
            "answer": "'Of those who walk or bike to school, what percent eat breakfast regularly?'",
            "explanation": "Restricting the denominator to a single subgroup ('Of those who walk or bike...') defines a conditional percentage."
        },
        {
            "source": "HW #8 (Association in Segmented Bars)",
            "q": "When comparing weekday breakfast habits across Bus, Car, and Walk/Bike commuters in a segmented bar graph, how do we tell if there is an association between the two variables?",
            "options": [
                "The conditional percentages (segment heights) for eating breakfast differ substantially across the transportation groups.",
                "All three bars reach a total height of 100.0%.",
                "The total number of students in each transportation mode is identical.",
                "The correlation coefficient r is close to +1.0."
            ],
            "answer": "The conditional percentages (segment heights) for eating breakfast differ substantially across the transportation groups.",
            "explanation": "If knowing a person's transportation mode changes the conditional probability of eating breakfast, the variables are associated."
        },
        {
            "source": "HW #8 (Scatterplot Outliers)",
            "q": "In a scatterplot of daily screen time (x, hours) vs. nightly sleep (y, hours) showing a strong negative linear trend from (1, 8.8) to (7.5, 5.6), one student is at (1.5, 4.5). How does this point deviate?",
            "options": [
                "It is an outlier with much less sleep (4.5 hrs) than expected for someone with low screen time (1.5 hrs).",
                "It is a high-leverage point that strengthens the negative linear slope.",
                "It follows the exact linear pattern predicted for 1.5 hours of screen time.",
                "It proves that low screen time causes insomnia."
            ],
            "answer": "It is an outlier with much less sleep (4.5 hrs) than expected for someone with low screen time (1.5 hrs).",
            "explanation": "Students with ~1.5 hours of screen time typically sleep ~8.4 hours, making (1.5, 4.5) a clear negative vertical outlier."
        }
    ],
    "All-Pro": [
        {
            "source": "HW #9 (Unit Conversions & r)",
            "q": "The correlation between tree canopy cover (%) and summer temperature (°F) across 30 neighborhoods is r = -0.79. If temperatures are converted to Celsius via C = (5/9)(F - 32), what is the new correlation r?",
            "options": [
                "r = -0.79 (unchanged, because correlation is unitless and unaffected by linear unit conversions).",
                "r = -0.44 (multiplied by 5/9).",
                "r = +0.79 (the sign flips after subtracting 32).",
                "r = -0.79 °C/% (takes on the new temperature units)."
            ],
            "answer": "r = -0.79 (unchanged, because correlation is unitless and unaffected by linear unit conversions).",
            "explanation": "Because r is computed from standardized z-scores, converting units never alters the value or sign of r."
        },
        {
            "source": "HW #9 (Curved Relationships & r)",
            "q": "Low fertilizer gives low corn yield, moderate fertilizer (100 kg/acre) gives peak yield, and excessive fertilizer (200 kg/acre) burns crops for low yield. A scientist finds r = -0.02 and claims there is no relationship. Valid?",
            "options": [
                "Invalid — correlation only measures LINEAR strength; a strong curved (parabolic) relationship can have r near 0.",
                "Valid — whenever r is close to 0, the two variables are completely unrelated.",
                "Invalid — r can never be negative when crop yields are positive.",
                "Valid — fertilizer burn cancels out the positive effect so no pattern exists."
            ],
            "answer": "Invalid — correlation only measures LINEAR strength; a strong curved (parabolic) relationship can have r near 0.",
            "explanation": "An upside-down U-shaped (quadratic) relationship has symmetric positive and negative slopes that yield r ≈ 0 despite a strong association."
        },
        {
            "source": "HW #9 (Outliers & Correlation)",
            "q": "In a scatterplot of Hours Studied (x) vs. Exam Score (y) with a tight positive linear trend, one student studied 8.5 hours but scored 48% (far below the ~95% trend). How would REMOVING this outlier affect r?",
            "options": [
                "r would increase (move closer to +1.0) because the remaining points follow a much tighter linear pattern.",
                "r would decrease (move closer to 0) because fewer data points always weaken correlation.",
                "r would stay the exact same because outliers only change the slope.",
                "r would become negative."
            ],
            "answer": "r would increase (move closer to +1.0) because the remaining points follow a much tighter linear pattern.",
            "explanation": "An outlier that falls far off the linear pattern weakens r toward 0; removing it strengthens r toward +1."
        },
        {
            "source": "HW #9 (Confounding Variables)",
            "q": "A study of 50 cities finds r = 0.82 between ice cream parlors per capita and July ER visits for sunburns. Should the city restrict ice cream permits to reduce sunburns?",
            "options": [
                "No — association is not causation; sunny/hot summer weather is a confounding variable driving both ice cream sales and sunburns.",
                "Yes — a correlation of r = 0.82 proves ice cream consumption increases UV skin sensitivity.",
                "Yes — observational studies of 50 cities establish direct cause-and-effect.",
                "No — because r = 0.82 indicates a weak negative relationship."
            ],
            "answer": "No — association is not causation; sunny/hot summer weather is a confounding variable driving both ice cream sales and sunburns.",
            "explanation": "Hot, sunny weather causes more people to buy ice cream AND more people to get sunburned."
        },
        {
            "source": "HW #9 (Interpreting Slope & y-Intercept)",
            "q": "Delivery shipping cost (ŷ, in $) for packages weighing 1 to 30 lb is modeled by ŷ = 6.50 + 1.40x. Which interpretation of the slope (1.40) is correct?",
            "options": [
                "For each additional 1 pound in package weight, the predicted shipping cost increases by $1.40.",
                "For each additional $1.40 in shipping cost, the package weight increases by 1 pound.",
                "A package weighing 0 pounds costs $1.40 to ship.",
                "Every package's shipping cost is exactly $1.40 times its weight."
            ],
            "answer": "For each additional 1 pound in package weight, the predicted shipping cost increases by $1.40.",
            "explanation": "Slope is the predicted change in the response variable (cost) per 1-unit increase in the explanatory variable (weight)."
        },
        {
            "source": "HW #9 (Calculating Residuals)",
            "q": "A café models iced lattes sold (ŷ) from daily high temperature (x, °F) using ŷ = -35 + 2.1x. On a 75°F day, the café sold 118 lattes. What is the residual (y - ŷ)?",
            "options": [
                "-4.5 lattes (sold 4.5 fewer lattes than the predicted 122.5)",
                "+4.5 lattes (sold 4.5 more lattes than the predicted 122.5)",
                "-122.5 lattes (predicted value at 75°F)",
                "+118.0 lattes (actual observed value)"
            ],
            "answer": "-4.5 lattes (sold 4.5 fewer lattes than the predicted 122.5)",
            "explanation": "Predicted ŷ = -35 + 2.1(75) = 122.5. Residual = Actual - Predicted = 118 - 122.5 = -4.5 lattes."
        },
        {
            "source": "HW #9 (Extrapolation)",
            "q": "Laptop battery charge (ŷ, %) for 0 ≤ x ≤ 10 hours of streaming is modeled by ŷ = 98.5 - 8.4x. Using this equation at x = 14 hours predicts -19.1%. Why is this unreliable, and what is it called?",
            "options": [
                "Extrapolation — predicting far outside the observed 0–10 hour range produces an impossible negative battery percentage.",
                "Confounding — streaming video for 14 hours changes the slope of the regression line.",
                "Interpolation — predicting within the data range always produces negative residuals.",
                "Voluntary response — the laptop battery was not randomly sampled."
            ],
            "answer": "Extrapolation — predicting far outside the observed 0–10 hour range produces an impossible negative battery percentage.",
            "explanation": "Using a regression line far beyond the observed x-interval is extrapolation and often yields nonsensical predictions."
        },
        {
            "source": "HW #9 (Residuals in Context)",
            "q": "A sprinter's 100m dash time (ŷ, sec) from weekly strength-training hours (x) is ŷ = 13.8 - 0.25x. An athlete training 4 hours/week runs 12.3 seconds. Calculate the residual and interpret whether they ran faster or slower than predicted.",
            "options": [
                "Residual = -0.5 seconds; the athlete ran 0.5 seconds FASTER than predicted (12.8 s).",
                "Residual = +0.5 seconds; the athlete ran 0.5 seconds SLOWER than predicted (12.8 s).",
                "Residual = -0.5 seconds; the athlete ran 0.5 seconds SLOWER than predicted (12.8 s).",
                "Residual = +1.5 seconds; the athlete ran 1.5 seconds FASTER than predicted."
            ],
            "answer": "Residual = -0.5 seconds; the athlete ran 0.5 seconds FASTER than predicted (12.8 s).",
            "explanation": "Predicted ŷ = 13.8 - 0.25(4) = 12.8 s. Residual = 12.3 - 12.8 = -0.5 s. In a race, a lower time means faster!"
        }
    ]
}

OFFENSIVE_PLAYS = [
    {"name": "🏃 Inside Zone Run (+8 yds | Easy)", "yards": 8, "tier": "Easy", "idx": 0},
    {"name": "🎯 Quick Slant Pass (+14 yds | Medium)", "yards": 14, "tier": "Medium", "idx": 1},
    {"name": "🚀 Play-Action Deep Post (+24 yds | Hard)", "yards": 24, "tier": "Hard", "idx": 2},
    {"name": "🔥 Hail Mary Flea-Flicker (+40 yds | All-Pro)", "yards": 40, "tier": "All-Pro", "idx": 3},
]

DEFENSIVE_PLAYS = [
    {"name": "🛡️ Goal-Line Run Stuff (Counters Run | Easy)", "tier": "Easy", "idx": 0},
    {"name": "🔒 Man-to-Man Press (Counters Slant | Medium)", "tier": "Medium", "idx": 1},
    {"name": "🦅 Cover-3 Zone (Counters Deep Post | Hard)", "tier": "Hard", "idx": 2},
    {"name": "🚨 All-Out Blitz (Counters Hail Mary | All-Pro)", "tier": "All-Pro", "idx": 3},
]

# --- SESSION STATE INITIALIZATION ---
if "scores" not in st.session_state:
    st.session_state.scores = [0, 0]
if "team_names" not in st.session_state:
    st.session_state.team_names = ["Home Panthers", "Away Wildcats"]
if "possession" not in st.session_state:
    st.session_state.possession = 0  # 0 = Home, 1 = Away
if "ball_on" not in st.session_state:
    st.session_state.ball_on = 20  # 0 to 100 (100 = Touchdown)
if "down" not in st.session_state:
    st.session_state.down = 1
if "yards_to_go" not in st.session_state:
    st.session_state.yards_to_go = 10
if "phase" not in st.session_state:
    st.session_state.phase = "PLAY_CALL"  # PLAY_CALL, QUESTION_TIME, EXTRA_POINT
if "current_play" not in st.session_state:
    st.session_state.current_play = None
if "last_result" not in st.session_state:
    st.session_state.last_result = None
if "used_q" not in st.session_state:
    st.session_state.used_q = {t: set() for t in QUESTION_BANK}
if "meter_running" not in st.session_state:
    st.session_state.meter_running = False
if "meter_pos" not in st.session_state:
    st.session_state.meter_pos = 10
if "xp_done" not in st.session_state:
    st.session_state.xp_done = False
if "xp_msg" not in st.session_state:
    st.session_state.xp_msg = ""


def draw_question_for_tier(tier):
    pool = QUESTION_BANK[tier]
    avail = [i for i in range(len(pool)) if i not in st.session_state.used_q[tier]]
    if not avail:
        st.session_state.used_q[tier] = set()
        avail = list(range(len(pool)))
    chosen = random.choice(avail)
    st.session_state.used_q[tier].add(chosen)
    return pool[chosen]


def switch_possession(new_ball_on=20):
    st.session_state.possession = 1 - st.session_state.possession
    st.session_state.ball_on = new_ball_on
    st.session_state.down = 1
    st.session_state.yards_to_go = min(10, 100 - new_ball_on)
    st.session_state.phase = "PLAY_CALL"
    st.session_state.current_play = None
    st.session_state.meter_running = False
    st.session_state.xp_done = False
    st.session_state.xp_msg = ""


def render_field(ball_on, first_down_line, off_name, def_name):
    ball_pct = max(2, min(98, ball_on))
    fd_pct = max(2, min(98, first_down_line))
    html = f"""
    <div style="background: linear-gradient(90deg, #1e3a8a 0%, #1e3a8a 8%, #15803d 8%, #16a34a 50%, #15803d 92%, #991b1b 92%, #991b1b 100%);
                border: 3px solid #ffffff; border-radius: 10px; padding: 14px 10px; position: relative; height: 95px; margin-bottom: 10px;">
        <div style="display: flex; justify-content: space-between; color: rgba(255,255,255,0.85); font-weight: bold; font-size: 13px; padding: 0 8%;">
            <span>OWN 10</span><span>20</span><span>30</span><span>40</span><span>50</span><span>40</span><span>30</span><span>20</span><span>OPP 10</span>
        </div>
        <div style="position: absolute; left: {8 + fd_pct * 0.84}%; top: 10px; bottom: 10px; width: 3px; background-color: #facc15;" title="First Down Line"></div>
        <div style="position: absolute; left: calc({8 + ball_pct * 0.84}% - 14px); top: 38px; font-size: 28px;" title="Ball at {ball_on}-yard line">🏈</div>
        <div style="position: absolute; bottom: 6px; left: 10%; color: white; font-size: 12px; font-weight: bold;">
            Offense: {off_name} (Ball on {ball_on}-yd line)
        </div>
        <div style="position: absolute; bottom: 6px; right: 10%; color: #fef08a; font-size: 12px; font-weight: bold;">
            First Down Line: {min(100, first_down_line)}-yd line
        </div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)


# --- SIDEBAR CONTROLS ---
st.sidebar.header("🏟️ Stadium Controls")
st.session_state.team_names[0] = st.sidebar.text_input("🔵 Home Team Name", value=st.session_state.team_names[0])
st.session_state.team_names[1] = st.sidebar.text_input("🔴 Away Team Name", value=st.session_state.team_names[1])

st.sidebar.divider()
st.sidebar.subheader("Manual Score Override")
st.session_state.scores[0] = st.sidebar.number_input(f"🔵 {st.session_state.team_names[0]}", value=st.session_state.scores[0], step=1)
st.session_state.scores[1] = st.sidebar.number_input(f"🔴 {st.session_state.team_names[1]}", value=st.session_state.scores[1], step=1)

st.sidebar.divider()
if st.sidebar.button("🔄 Reset Entire Game", use_container_width=True):
    st.session_state.scores = [0, 0]
    st.session_state.possession = 0
    st.session_state.ball_on = 20
    st.session_state.down = 1
    st.session_state.yards_to_go = 10
    st.session_state.phase = "PLAY_CALL"
    st.session_state.current_play = None
    st.session_state.last_result = None
    st.session_state.used_q = {t: set() for t in QUESTION_BANK}
    st.session_state.meter_running = False
    st.session_state.xp_done = False
    st.rerun()

# --- SCOREBOARD & FIELD DISPLAY ---
st.title("🏈 Stats Turkey Bowl")

off_idx = st.session_state.possession
def_idx = 1 - off_idx
off_badge = "🔵" if off_idx == 0 else "🔴"
def_badge = "🔴" if off_idx == 0 else "🔵"
off_team = f"{off_badge} {st.session_state.team_names[off_idx]}"
def_team = f"{def_badge} {st.session_state.team_names[def_idx]}"

sb1, sb2, sb3, sb4 = st.columns(4)
sb1.metric(f"🔵 {st.session_state.team_names[0]}", f"{st.session_state.scores[0]} PTS")
sb2.metric(f"🔴 {st.session_state.team_names[1]}", f"{st.session_state.scores[1]} PTS")
down_suffix = {1: "1st", 2: "2nd", 3: "3rd", 4: "4th"}[st.session_state.down]
ytg_label = "Goal" if st.session_state.ball_on + st.session_state.yards_to_go >= 100 else str(st.session_state.yards_to_go)
sb3.metric("Down & Distance", f"{down_suffix} & {ytg_label}")
sb4.metric("Field Position", f"Own {st.session_state.ball_on}" if st.session_state.ball_on <= 50 else f"Opp {100 - st.session_state.ball_on}")

render_field(
    st.session_state.ball_on,
    st.session_state.ball_on + st.session_state.yards_to_go,
    off_team,
    def_team
)

if st.session_state.last_result:
    st.info(f"**Last Play Summary:** {st.session_state.last_result}")

# ==============================================================================
# PHASE 1: PLAY CALLING
# ==============================================================================
if st.session_state.phase == "PLAY_CALL":
    st.subheader(f"📋 Huddle Up! {off_team} (Offense) vs. {def_team} (Defense)")

    c_off, c_def = st.columns(2)
    with c_off:
        with st.container(border=True):
            st.markdown(f"### {off_team} — Offensive Playbook")
            off_choice_idx = st.selectbox(
                "Select Offensive Play (Higher yards = tougher Stats question):",
                options=list(range(len(OFFENSIVE_PLAYS))),
                format_func=lambda i: OFFENSIVE_PLAYS[i]["name"],
                key="off_select"
            )
    with c_def:
        with st.container(border=True):
            st.markdown(f"### {def_team} — Defensive Playbook")
            def_choice_idx = st.selectbox(
                "Select Defensive Scheme (Match Offense's play type for a Stop Bonus!):",
                options=list(range(len(DEFENSIVE_PLAYS))),
                format_func=lambda i: DEFENSIVE_PLAYS[i]["name"],
                key="def_select"
            )

    btn_hike, btn_punt = st.columns([2.5, 1])
    with btn_hike:
        if st.button("📣 HIKE BALL! (Generate Play Questions)", type="primary", use_container_width=True):
            off_play = OFFENSIVE_PLAYS[off_choice_idx]
            def_play = DEFENSIVE_PLAYS[def_choice_idx]
            q_off = draw_question_for_tier(off_play["tier"])
            q_def = draw_question_for_tier(def_play["tier"])
            # Ensure both teams get distinct questions even if they pick the same difficulty tier
            while q_def["q"] == q_off["q"] and len(QUESTION_BANK[def_play["tier"]]) > 1:
                q_def = draw_question_for_tier(def_play["tier"])

            st.session_state.current_play = {
                "off_play": off_play,
                "def_play": def_play,
                "q_off": q_off,
                "q_def": q_def,
                "countered": (off_play["idx"] == def_play["idx"])
            }
            st.session_state.phase = "QUESTION_TIME"
            st.rerun()

    with btn_punt:
        if st.session_state.down == 4:
            if st.button("🦶 Punt on 4th Down", use_container_width=True):
                punt_landing = min(80, st.session_state.ball_on + 40)
                new_opp_spot = max(20, 100 - punt_landing)
                st.session_state.last_result = f"🦶 {off_team} punted 40 yards! {def_team} takes over at their own {new_opp_spot}-yard line."
                switch_possession(new_opp_spot)
                st.rerun()

# ==============================================================================
# PHASE 2: DUAL PLAY QUESTIONS
# ==============================================================================
elif st.session_state.phase == "QUESTION_TIME":
    play = st.session_state.current_play
    off_play = play["off_play"]
    def_play = play["def_play"]
    q_off = play["q_off"]
    q_def = play["q_def"]

    if play["countered"]:
        st.warning(f"🚨 **DEFENSIVE READ!** {def_team} called **{def_play['name'].split(' (')[0]}** and guessed {off_team}'s exact play!")
    else:
        st.success(f"🏈 **PLAY IN MOTION:** {off_team} runs **{off_play['name'].split(' (')[0]}** against {def_team}'s **{def_play['name'].split(' (')[0]}**!")

    col_q1, col_q2 = st.columns(2)
    with col_q1:
        with st.container(border=True):
            st.markdown(f"### {off_team} Question ({off_play['tier']})")
            st.caption(f"Worksheet Source: {q_off['source']}")
            st.markdown(f"**{q_off['q']}**")
            ans_off = st.radio(
                f"{off_team} Answer:",
                q_off["options"],
                index=None,
                key="radio_off_ans"
            )

    with col_q2:
        with st.container(border=True):
            st.markdown(f"### {def_team} Question ({def_play['tier']})")
            st.caption(f"Worksheet Source: {q_def['source']}")
            st.markdown(f"**{q_def['q']}**")
            ans_def = st.radio(
                f"{def_team} Answer:",
                q_def["options"],
                index=None,
                key="radio_def_ans"
            )

    if st.button("⚡ RESOLVE PLAY!", type="primary", use_container_width=True):
        if ans_off is None or ans_def is None:
            st.error("⚠️ Both Offense and Defense must select an answer before resolving the play!")
        else:
            off_correct = (ans_off == q_off["answer"])
            def_correct = (ans_def == q_def["answer"])
            base_yds = off_play["yards"]

            # Determine yardage & turnover outcome
            turnover = False
            if off_correct and not def_correct:
                gained = base_yds if play["countered"] else base_yds + 5
                outcome_text = f"💥 {off_team} nailed their question while {def_team} missed! Gained **+{gained} yards**!"
            elif off_correct and def_correct:
                if play["countered"]:
                    gained = 0
                    outcome_text = f"🧱 Both teams answered right, and {def_team}'s counter stuffed the play for **0 yards**!"
                else:
                    gained = max(3, base_yds // 2)
                    outcome_text = f"⚔️ Both teams answered right! {off_team} fought through traffic for **+{gained} yards**."
            elif not off_correct and def_correct:
                if off_play["idx"] == 3:
                    gained = 0
                    turnover = True
                    outcome_text = f"🙌 **INTERCEPTION!** {off_team} missed their Hail Mary question and {def_team} picked it off!"
                else:
                    gained = -5
                    outcome_text = f"🛑 **SACK / TACKLE FOR LOSS!** {def_team} answered right while {off_team} missed (**-5 yards**)."
            else:
                gained = 0
                outcome_text = f"💨 Both teams missed their questions — incomplete play for **0 yards**."

            # Append answer key feedback
            feedback = (
                f"{outcome_text}\n\n"
                f"- **{off_team} ({'✅ Correct' if off_correct else '❌ Incorrect'}):** {q_off['explanation']}\n"
                f"- **{def_team} ({'✅ Correct' if def_correct else '❌ Incorrect'}):** {q_def['explanation']}"
            )
            st.session_state.last_result = feedback

            if turnover:
                new_spot = max(15, 100 - st.session_state.ball_on)
                switch_possession(new_spot)
                st.rerun()

            new_ball = max(1, st.session_state.ball_on + gained)
            st.session_state.ball_on = new_ball

            # Check for Touchdown!
            if new_ball >= 100:
                st.session_state.scores[off_idx] += 6
                st.session_state.phase = "EXTRA_POINT"
                st.session_state.meter_running = False
                st.session_state.meter_pos = 10
                st.session_state.xp_done = False
                st.session_state.xp_msg = ""
                st.rerun()

            # Check for First Down or Next Down
            if gained >= st.session_state.yards_to_go:
                st.session_state.down = 1
                st.session_state.yards_to_go = min(10, 100 - new_ball)
                st.session_state.last_result = f" chains move! **FIRST DOWN!** " + st.session_state.last_result
                st.session_state.phase = "PLAY_CALL"
                st.session_state.current_play = None
            else:
                st.session_state.down += 1
                st.session_state.yards_to_go = max(1, st.session_state.yards_to_go - gained)
                if st.session_state.down > 4:
                    st.session_state.last_result = f"🔄 **TURNOVER ON DOWNS!** " + st.session_state.last_result
                    new_spot = max(15, 100 - new_ball)
                    switch_possession(new_spot)
                else:
                    st.session_state.phase = "PLAY_CALL"
                    st.session_state.current_play = None
            st.rerun()

# ==============================================================================
# PHASE 3: TOUCHDOWN & EXTRA POINT POWER METER
# ==============================================================================
elif st.session_state.phase == "EXTRA_POINT":
    st.balloons()
    st.success(f"🎉 **TOUCHDOWN {off_team} (+6 Points)!** Line up for the **+1 Extra Point Kick**!")

    def render_power_meter(pos_val):
        meter_html = f"""
        <div style="background-color: #1f2937; border: 3px solid #f9fafb; border-radius: 12px; padding: 18px; margin: 12px 0;">
            <div style="color: white; font-weight: bold; text-align: center; margin-bottom: 8px; font-size: 16px;">
                🥅 EXTRA POINT POWER METER — Stop the football inside the GREEN GOALPOST ZONE (42% – 58%)!
            </div>
            <div style="position: relative; height: 38px; border-radius: 8px; overflow: hidden;
                        background: linear-gradient(90deg, #dc2626 0%, #facc15 32%, #16a34a 42%, #16a34a 58%, #facc15 68%, #dc2626 100%);">
                <div style="position: absolute; left: 42%; width: 16%; top: 0; bottom: 0; border-left: 3px dashed white; border-right: 3px dashed white;"></div>
                <div style="position: absolute; left: calc({pos_val}% - 14px); top: 3px; font-size: 24px;">🏈</div>
            </div>
            <div style="display: flex; justify-content: space-between; color: #d1d5db; font-size: 12px; margin-top: 6px;">
                <span>0% (Wide Left)</span>
                <span style="color: #4ade80; font-weight: bold;">🎯 GOALPOSTS (42% - 58%)</span>
                <span>100% (Wide Right)</span>
            </div>
        </div>
        """
        return meter_html

    if not st.session_state.xp_done:
        if not st.session_state.meter_running:
            st.markdown(render_power_meter(st.session_state.meter_pos), unsafe_allow_html=True)
            if st.button("▶️ Start Extra Point Power Meter", type="primary", use_container_width=True):
                st.session_state.meter_running = True
                st.rerun()
        else:
            # Clicking this button interrupts the animation loop and locks in st.session_state.meter_pos
            if st.button("🦵 KICK EXTRA POINT NOW! (Stop the Meter)", type="primary", use_container_width=True):
                st.session_state.meter_running = False
                st.session_state.xp_done = True
                final_pos = st.session_state.meter_pos
                if 42 <= final_pos <= 58:
                    st.session_state.scores[off_idx] += 1
                    st.session_state.xp_msg = f"✅ **IT'S GOOD! (+1 Extra Point!)** You stopped the meter right down the middle at **{final_pos}%**!"
                else:
                    direction = "Wide Left" if final_pos < 42 else "Wide Right"
                    st.session_state.xp_msg = f"❌ **NO GOOD ({direction} at {final_pos}%)!** Needed between 42% and 58%."
                st.rerun()

            meter_placeholder = st.empty()
            pos = st.session_state.meter_pos
            step = 5
            for _ in range(500):
                pos += step
                if pos >= 98:
                    pos = 98
                    step = -5
                elif pos <= 2:
                    pos = 2
                    step = 5
                st.session_state.meter_pos = pos
                meter_placeholder.markdown(render_power_meter(pos), unsafe_allow_html=True)
                time.sleep(0.065)
    else:
        st.markdown(render_power_meter(st.session_state.meter_pos), unsafe_allow_html=True)
        if "+1 Extra Point" in st.session_state.xp_msg:
            st.success(st.session_state.xp_msg)
        else:
            st.warning(st.session_state.xp_msg)

        if st.button("➡️ Kickoff to Opponent (Switch Possession)", type="primary", use_container_width=True):
            st.session_state.last_result = f"🏈 Kickoff after {off_team}'s touchdown! {def_team} starts at their own 20-yard line."
            switch_possession(20)
            st.rerun()
