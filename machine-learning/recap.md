# Machine learning — recap & real-world examples

*Part of [Machine learning for the product and technology leader](./README.md)*

## Real-world examples & war stories

**Google Flu Trends overshoots (2013).** Google built a model that estimated flu activity from
search terms, and it was trained to match the reports of the US Centers for Disease Control and
Prevention (CDC). In February 2013, Nature reported that it was predicting more than double the
share of doctor visits for influenza-like illness that the CDC reported. Lazer and colleagues
later argued in *Science* (2014) that the design invited the error. The team had searched about
50 million candidate search terms to fit about 1,152 data points. With so many candidates,
some would track the flu season by chance. 🎯 *Takeaway:* a model with far more candidate
signals than cases will find patterns that are not there, and will look fine until the world
moves. This is [overfitting](./generalization-overfitting-and-bias-variance.md), and the drift
that exposed it is covered in [ML in production](./ml-in-production.md).

**A sepsis alert that did not travel (2021).** Epic's original sepsis model (version 1) was
used in many US hospitals. Researchers at the University of Michigan tested it on 38,455
hospitalizations and published the result in *JAMA Internal Medicine* in 2021. They reported
an AUC of 0.63. At an alert score of 6, which is within the range Epic recommends, the model
caught 33% of sepsis cases, missed 67%, and raised alerts on 18% of all hospitalized
patients. Epic disputed how the study defined sepsis and its onset. Epic has since released a
revised version. As of 2026-10, a multi-hospital study of that version in *JAMA Network Open*
reported AUROC between 0.82 and 0.92, with low positive predictive value and a heavy alert
load. 🎯 *Takeaway:* a score a vendor reports for one setting is a claim, not a fact about
your hospital, and it belongs to one version of the model. Test the version you run on your
own data, and look at the [confusion matrix and threshold](./measuring-a-model.md), not only
one headline number.

**An experimental hiring tool shut down (reported 2018).** Reuters reported in October 2018
that Amazon had built an experimental tool to score job applicants' resumes, trained on
patterns in the resumes the company had received. Reuters said engineers found by 2015 that
it did not rate technical candidates in a gender-neutral way, and that the team was disbanded
by the start of 2017. Citing people familiar with the effort, it reported that recruiters
looked at the tool's recommendations but never relied solely on them. Amazon declined to
comment on the tool's problems. It said the tool "was never used by Amazon recruiters to
evaluate candidates." 🎯 *Takeaway:* a model learns the patterns in its history, including the ones you did not want.
This is the [label and selection problem](./data-features-labels-and-leakage.md): the past you
learn from is not neutral.

**Zillow winds down its home-buying business (2021).** On 2 November 2021, Zillow announced it
would wind down Zillow Offers. It recorded an inventory write-down of about $304 million in the
third quarter and said it would cut about 25% of its workforce. Its shareholder letter said
the unpredictability of forecasting home prices was far greater than the company had
anticipated. The company had bought 9,680 homes in that quarter. 🎯 *Takeaway:* a forecast
that is wrong a little is a rounding error. A forecast that drives large purchases at scale
turns small error into large loss. Measure the cost of [each kind of error](./measuring-a-model.md)
before you let the model act at volume. The post-mortem is Zillow's own account, not an
independent one, and we do not claim a single cause.

**The unit that changed (an illustration).** A team ships a churn model. Offline, it scores an
AUC of 0.73. At launch, the serving system passes tenure in days where training used months.
No error appears. Live performance drops by about 11 points, and the first alert is a
quarter-end review. The story is invented, and the [numbers come from the lesson-7 code](./ml-in-production.md).
🎯 *Takeaway:* skew produces no crash, only wrong answers. A check on input spread catches it
on day one.

## Module recap

| Lesson | The one idea | The question it makes you ask |
| --- | --- | --- |
| [What machine learning is, and when to use it](./what-machine-learning-is.md) | A learned system has data, a model and an objective. Rules, a trained model and an LLM suit different problems. | What is the best simple rule, and how much better is the model? |
| [Data: features, labels, splits and leakage](./data-features-labels-and-leakage.md) | The data is part of the logic. A score that looks too good often has a leak. | For every input, do we know it at prediction time, and was the test split honest? |
| [Training: loss and gradient descent](./training-loss-and-gradient-descent.md) | Training is a loop: predict, measure the loss, step downhill, repeat. The learning rate is the setting that matters. | Did the training and validation curves flatten together? |
| [Generalization: overfitting and bias–variance](./generalization-overfitting-and-bias-variance.md) | A model must work on cases it has not seen. Two charts show whether to buy data, simplicity or better features. | What is the gap between training and validation, and would more data close it? |
| [Measuring a model](./measuring-a-model.md) | One number hides the decision. Use a baseline, a confusion matrix, a cost-based cutoff, and a calibration check. | What does each error cost, and where did we set the threshold? |
| [Model families](./model-families.md) | A model can only find patterns its shape allows. Tables suit linear models and trees. Perception suits neural networks. | How much better is this family than a linear model on the same data? |
| [ML in production](./ml-in-production.md) | Launch is the middle. Skew, drift, feedback loops and silent upstream changes decay a model. | If it got worse next Tuesday, which alarm fires and who owns it? |
| [Learning and doing ML with Claude Code](./learning-and-doing-ml-with-claude-code.md) | An agent speeds up the loop and does not change what makes a score honest. You hold the contract, and the checks fail loudly. | How many times did the agent score the test rows, and where is the log? |

**The through-line:** a learned model is a bet that the past resembles the future. Every
lesson tests that bet from a different side. Does the data describe the future (lesson 2)?
Did the model learn the pattern or the noise (lesson 4)? Does the score mean what we think it
means (lesson 5)? Will the world stay still (lesson 7)? The model itself, the part that gets
the attention, is the smallest question. The costly failures sit in the data, the test and
the lifecycle.

> **Walk-away question:** *"For our most important model: what is the baseline, was the test
> split honest, what does each kind of error cost and where is the threshold, and which alarm
> fires if it decays?"*

If you can answer all four, you can steer the project. If not, you know which lesson to reread.

## Test yourself

1. **A team proposes a model for a decision that fits on one page of rules. What do you ask?**
   <details><summary>Answer</summary>Ask for the best simple rule and its score, and how much better the model is. A model must beat the baseline by enough to pay for its data, upkeep and risk. (<a href="./what-machine-learning-is.md">Lesson 1</a>)</details>
2. **Name the three parts of every learned system.**
   <details><summary>Answer</summary>Data (cases, with features and often a label), a model (a function with adjustable parameters), and an objective (a score of how wrong the model is). (<a href="./what-machine-learning-is.md">Lesson 1</a>)</details>
3. **A model scores 97% in testing and 50% in production. What is the first suspect?**
   <details><summary>Answer</summary>Leakage. A feature that is known only after the outcome, or a split that puts the same customer on both sides, makes the test easier than real life. (<a href="./data-features-labels-and-leakage.md">Lesson 2</a>)</details>
4. **Why must the test set be looked at once?**
   <details><summary>Answer</summary>Each choice made by looking at the test score moves information from the test set into the model. Choose on validation rows, and report on the test rows at the end. (<a href="./data-features-labels-and-leakage.md">Lesson 2</a>)</details>
5. **What are the four steps of the training loop, and what happens if the learning rate is far too large?**
   <details><summary>Answer</summary>Predict, compute the loss, work out the gradient, update the parameters, and repeat. With a rate far too large the steps overshoot, and the loss jumps around or grows. (<a href="./training-loss-and-gradient-descent.md">Lesson 3</a>)</details>
6. **Training loss keeps falling while validation loss rises. What is happening, and what do you try?**
   <details><summary>Answer</summary>Overfitting: the model memorizes the training rows. Try more data, a simpler model, regularization, fewer features, or early stopping. (<a href="./generalization-overfitting-and-bias-variance.md">Lesson 4</a>)</details>
7. **In the worked example, why did the depth-4 tree on 600 rows beat the depth-8 tree on 3,000 rows?**
   <details><summary>Answer</summary>The deeper tree overfits, and five times the data only narrowed the gap. A simpler model on less data did better. (<a href="./generalization-overfitting-and-bias-variance.md">Lesson 4</a>)</details>
8. **About 18% of customers cancel. A model predicting "nobody cancels" is 82% accurate. What do you ask for instead?**
   <details><summary>Answer</summary>A baseline, a confusion matrix, and precision and recall, or a cost. Accuracy rewards the model that does nothing on a rare outcome. (<a href="./measuring-a-model.md">Lesson 5</a>)</details>
9. **A missed churner costs $60 and a wasted offer costs $15. Where does a good cutoff sit, if the scores are calibrated?**
   <details><summary>Answer</summary>At 15 ÷ (15 + 60) = 0.20. Flag customers whose risk is 20% or more. The cutoff follows the costs, and it moves when they move. (<a href="./measuring-a-model.md">Lesson 5</a>)</details>
10. **Two models have the same AUC. Why might you still prefer one?**
    <details><summary>Answer</summary>AUC measures ranking only. One model can report probabilities that are far off. If anyone reads the score as a probability, or the cutoff is computed from it, calibration matters too. (<a href="./measuring-a-model.md">Lesson 5</a>)</details>
11. **Why does a linear model fail on a pattern where two scores matter only together?**
    <details><summary>Answer</summary>A linear model adds up separate effects. It cannot express "same sign". A tree or a small neural network can. In the example, the linear model scored 47% and the tree 91%. (<a href="./model-families.md">Lesson 6</a>)</details>
12. **For a customer table with 50,000 rows, which two families do you try first?**
    <details><summary>Answer</summary>A linear (logistic) model and a boosted tree ensemble. Deep networks are the first choice for text, images and audio, usually pre-trained. (<a href="./model-families.md">Lesson 6</a>)</details>
13. **What is training-serving skew, and why does it not crash anything?**
    <details><summary>Answer</summary>The model sees different inputs live than in training, such as a different unit or a stale lookup. The values are valid numbers, so nothing fails. The answers are just wrong. Share one feature code path and monitor input spread. (<a href="./ml-in-production.md">Lesson 7</a>)</details>
14. **Why do teams watch inputs, scores and outcomes, not just accuracy?**
    <details><summary>Answer</summary>Outcomes arrive late, by the label delay. Input and score checks are immediate but cannot prove the model is wrong. You need both. (<a href="./ml-in-production.md">Lesson 7</a>)</details>

15. **An agent tried 36 settings and reports its best test score. Why is the number too good, and what do you ask for?**
    <details><summary>Answer</summary>Choosing the winner by its test score picks partly on luck, so the score overstates what fresh rows will show. In the lesson-8 example the average overstatement was 2.5 points. Ask for the log of every evaluation, how many times the test rows were scored, and a score on rows that were never used to choose. (<a href="./learning-and-doing-ml-with-claude-code.md">Lesson 8</a>)</details>
16. **Why is a deny rule on the test file not enough to protect the test rows from an agent?**
    <details><summary>Answer</summary>A rule limits the agent's own file tools. A script the agent writes and runs can open any file the operating system allows. Keep the final labels out of the agent's reach, and score them through a step you run. (<a href="./learning-and-doing-ml-with-claude-code.md">Lesson 8</a>)</details>

## Sources

- Lazer, Kennedy, King and Vespignani, *The Parable of Google Flu: Traps in Big Data Analysis*,
  Science 343, 1203–1205, 14 Mar 2014.
  [doi.org/10.1126/science.1248506](https://doi.org/10.1126/science.1248506). The February 2013
  report that Google Flu Trends predicted more than double the CDC's share of doctor visits
  for influenza-like illness, and the point about about 50 million terms and 1,152 data
  points. Checked through search-result excerpts, 2026-10.
- Butler, D. *When Google got flu wrong*, Nature 494, 155–156, 14 Feb 2013. The news report
  that Lazer et al. cite for the overshoot. Not opened directly; checked through search
  results, 2026-10.
- Wong et al., *External Validation of a Widely Implemented Proprietary Sepsis Prediction Model
  in Hospitalized Patients*, JAMA Internal Medicine 181(8), June 2021
  ([doi.org/10.1001/jamainternmed.2021.2626](https://doi.org/10.1001/jamainternmed.2021.2626)):
  38,455 hospitalizations, AUC 0.63, 33% sensitivity, 67% of sepsis cases not identified,
  alerts on 18% of patients, at an alert score of 6. These figures are for the original
  model, version 1. Epic's response disputed the definition of sepsis onset. Checked through
  search-result summaries, 2026-10.
- A multicenter external validation of Epic Sepsis Model version 2, *JAMA Network Open*
  ([jamanetwork.com/journals/jamanetworkopen/article-abstract/2845595](https://jamanetwork.com/journals/jamanetworkopen/article-abstract/2845595)):
  227,091 inpatient encounters at four US health systems, AUROC between 0.82 and 0.92, high
  variation between sites, low positive predictive value and a high alert burden. Checked
  through search-result excerpts, 2026-10. The article was not opened, so read it before you
  quote it.
- Dastin, J. *Amazon scraps secret AI recruiting tool that showed bias against women*, Reuters,
  10 Oct 2018. The project start in 2014, the finding of gender skew by 2015, recruiters not
  relying on it alone (from people familiar with the effort), the team disbanded by the start
  of 2017, and Amazon's statement that the tool "was never used by Amazon recruiters to
  evaluate candidates". The statement is checked through coverage of the Reuters report.
  Checked through reprints and summaries, 2026-10.
- Zillow Group, third-quarter 2021 results and shareholder letter, 2 Nov 2021, filed as
  exhibit 99.1 to a Form 8-K ([sec.gov](https://www.sec.gov/Archives/edgar/data/1617640/000161764021000085/q32021991.htm)):
  the decision to wind down Zillow Offers, the inventory write-down of about $304 million
  in the third quarter, the cut of about 25% of the workforce, the statement about
  forecasting home prices, and the 9,680 homes bought in the quarter. Checked through
  search-result excerpts, 2026-10.
- The unit-mismatch story is an invented illustration. All figures from the example data come
  from `machine-learning/code/`.

---

← Back to [module overview](./README.md)
