# Data Dictionary: Credit Card Fraud Dataset

This document describes the columns present in the `data/creditcard.csv` dataset.

| Column Name | Description | Data Type |
|-------------|-------------|-----------|
| **Time**    | Number of seconds elapsed between this transaction and the first transaction in the dataset. | Numeric (Continuous) |
| **V1 - V28**| Principal components obtained using PCA. Due to confidentiality issues, the original features and more background information about the data are not provided. | Numeric (Continuous) |
| **Amount**  | The transaction amount. This feature can be used for example-dependent cost-sensitive learning. | Numeric (Continuous) |
| **Class**   | The response variable (target). It takes the value `1` in case of a fraudulent transaction and `0` otherwise. | Numeric (Categorical/Binary) |

## Additional Notes
- The features `V1` through `V28` are the result of a PCA transformation. 
- `Time` and `Amount` are the only features which have not been transformed with PCA.
