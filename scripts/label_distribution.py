import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib
import jsonlines
from sklearn.preprocessing import MultiLabelBinarizer


matplotlib.style.use('ggplot')


with jsonlines.open("../data/train-test-val/train.jsonl") as reader:
    json_list = []
    for obj in reader:
        json_list.append(obj)

df= pd.DataFrame(json_list)
labels= list(df["accept"])

mlb = MultiLabelBinarizer()
all_transformed_labels = mlb.fit_transform(labels)

all_transformed_df= pd.DataFrame(all_transformed_labels)

def get_class_totals(dummy_all):
    labels = list(dummy_all.columns.values)
    counts = []
    for i in labels:
        counts.append((i, dummy_all[i].sum()))
    df_totals = pd.DataFrame(counts, columns=['label', 'number_of_tables'])
    return df_totals

label_totals= get_class_totals(all_transformed_df)

def plot_class_totals(df_totals):
    df_totals.plot(x='label', y='number_of_tables', kind='bar', legend=False, figsize=(8, 5))
    plt.title("Number of tables per class")
    plt.ylabel('# of Occurrences', fontsize=12)
    plt.xlabel('Class', fontsize=12)
    plt.xticks([0,1,2,3,4,5,6,7,8,9], ['NC Params', 'Comp Params', 'Param-Cov Relations',
                      'Params Other', 'Not Relevant', 'Doses', 'Number of Subs',
                      'Sample timings', 'Demographics', 'Covariates Other'])
    plt.tight_layout()
    plt.show()

plot_class_totals(label_totals)



def plot_mutlilabel_tables(df):
    rowsums = df.sum(axis=1)
    x = rowsums.value_counts()
    # plot
    ax = sns.barplot(x.index, x.values)
    plt.title("Multiple Labels per Table")
    plt.ylabel('# of Occurrences', fontsize=12)
    plt.xlabel('# of categories', fontsize=12)
    plt.tight_layout()
    plt.show()

plot_mutlilabel_tables(all_transformed_df)


def plot_html_len(df):
    lens = df["html"].str.len()
    lens.hist(bins=np.arange(0, 5000, 50))
    plt.title("Len of html string")
    plt.ylabel('Words', fontsize=12)
    plt.xlabel('Count', fontsize=12)
    plt.tight_layout()
    plt.show()
