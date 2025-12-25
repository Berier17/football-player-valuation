{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "id": "346163c9-6e74-4f69-a0a8-d8ecd872b14c",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Saving model to model.bin...\n",
      "Success! Model is ready for deployment.\n"
     ]
    }
   ],
   "source": [
    "# train.py\n",
    "import pandas as pd\n",
    "import pickle\n",
    "from sklearn.feature_extraction import DictVectorizer\n",
    "from xgboost import XGBRegressor\n",
    "\n",
    "# ---------------------------------------------------------\n",
    "# DATA SOURCE NOTE:\n",
    "# This dataset was scraped by the author. \n",
    "# Scraping logic is in 'scraping.ipynb'.\n",
    "# ---------------------------------------------------------\n",
    "\n",
    "# 1. PARAMETERS (Best params from your tuning)\n",
    "params = {\n",
    "    'n_estimators': 100,\n",
    "    'learning_rate': 0.1,\n",
    "    'max_depth': 3,\n",
    "    'random_state': 42,\n",
    "    'n_jobs': -1\n",
    "}\n",
    "\n",
    "output_file = 'model.bin'\n",
    "\n",
    "# 2. LOAD DATA\n",
    "df = pd.read_csv('final_dataset.csv')\n",
    "\n",
    "# 3. PREPARATION\n",
    "features = ['age', 'npxg+xag', 'starts', 'team', 'pos']\n",
    "target = 'value_euros'\n",
    "\n",
    "# Filter columns\n",
    "df = df[features + [target]].dropna().copy()\n",
    "\n",
    "# 4. ENCODING (Refactored for Production)\n",
    "# We switch from pd.factorize to DictVectorizer.\n",
    "# This ensures that \"Arsenal\" maps to the same number in Production as in Training.\n",
    "train_dicts = df[features].to_dict(orient='records')\n",
    "\n",
    "dv = DictVectorizer(sparse=False)\n",
    "X = dv.fit_transform(train_dicts)\n",
    "y = df[target].values\n",
    "\n",
    "# 5. TRAIN\n",
    "model = XGBRegressor(**params)\n",
    "model.fit(X, y)\n",
    "\n",
    "# 6. SAVE\n",
    "print(f\"Saving model to {output_file}...\")\n",
    "with open(output_file, 'wb') as f_out:\n",
    "    # Save both the Translator (dv) and the Brain (model)\n",
    "    pickle.dump((dv, model), f_out)\n",
    "\n",
    "print(\"Success! Model is ready for deployment.\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "0f76954c-d0f4-4988-87e4-829069d26e3b",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python [conda env:base] *",
   "language": "python",
   "name": "conda-base-py"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.12.3"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
