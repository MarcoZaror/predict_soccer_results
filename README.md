# predict_soccer_results

This work intends to predict premier league soccer results. So far, its results are comparable to the ones from BET365.

## Structure

### File: ETL_1.py
 - Objective: Mostly data preprocessing and variable generation

### File: ETL_2.py
 - Objective: Initial analysis of the database and final adaptations

### Modelling.py
 - Objective: Treat the problem as a 3-label classificaton problem (win, draw or loss).

### Modelling_2classes.py
 - Objective: Treat the problem as a binary classificaton problem (win or other).

## Conclusion
### 3-label classification
 - Results: 72% of accuracy on test set
 - 4.5% of return on investing (betting)

### Binary classificaton
 - Results: 69% of accuracy on test set
 - 4% of return on investing (betting)

* Inner functions are not published
* Data was webscrapped