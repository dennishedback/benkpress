# benkpress

Graphical user interface for creating and evaluating classifiers for PDF
file/page/sentence targets using sklearn compatible pipelines.


## The pitch

Imagine having to classify PDFs as either this or that. The key information needed to
make the classification may be contained on a specific page or in a specific sentence.
Imagine then wanting to train a supervised machine learning model to automatically
perform this classification. How do you want to manually tag the training data? Do
you want to convert all PDFs into plain text and read it as such, with potential
optical text recognition errors?

I argue that it's much easier to read and tag this:

[Insert screenshot here]

Than it is to read and tag this:

[Insert screenshot here]

And this is exactly what benkpress is for.


## Usage at a glance

1. Create your sklearn compatible pipeline using the Python console or any other preferred method.
2. Pickle it using joblib.
3. Load your joblib pickle into benkpress.
4. Use benkpress to train your pipeline (or evaluate an already fitted pipeline).
5. Pickle your fitted pipeline for use in other applications. <- wrong
6. benkpress exports your training data so that your pipeline may be easily refitted using either newer versions of sklearn or on other platforms.
7. Have fun.

## The benkpress API

Lorem ipsum dolor sit amet.

## Examples

In this example, we'll tag training data for an [XGBoost](https://github.com/dmlc/xgboost) classifier to identify an arbitrary class of pages
in a sample of PDF documents. The pages are classified according to their vocabulary characteristics by first tokenizing
the page content using a [TfidfVectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).
Since we are classifying pages instead of, for example, sentences, we can use the `PassthroughPagePreprocessor` from benkpress_api.
The resulting `PDFClassifierContext` is saved to file using joblib:


```python

import joblib

from benkpress_api import PassthroughPagePreprocessor, PDFClassifierContext
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import Pipeline
from xgboost import XGBClassifier

RANDOM_STATE = 999

context = PDFClassifierContext(
    PassthroughPagePreprocessor(),
    Pipeline([
        ("Vectorizer", TfidfVectorizer(use_idf=True, max_features=None, stop_words=None)),
        ("Classifier", XGBClassifier(n_estimators=1000, random_state=RANDOM_STATE))
    ])
)

joblib.dump(context, "pagecontext.joblib")


```

The context is loaded in benkpress by selecting File -> Import context:

![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/import_context1.png)

After this, we choose a folder containing a sample of PDFs for tagging the training data:

![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/import_context3.png)

A PDF will appear in the reader and the preprocessed data points will appear to the right.
Note that since we are using `PassthroughPagePreprocessor`, each data point will be the text of
each respective page. We can now look through the PDF and tag which pages are of the relevant class
by changing the values in the rightmost column from 0 to 1. When we are done tagging, we click the
button ">>> Next document >>>" in the lower left corner and the next PDF in the sample will appear
in the reader:

![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/benkpress1.png)

After we have tagged some pages of the relevant class, the classifier provided in our
imported context can be evaluated, as well as help out with tagging. On the "Pipeline" tab,
click the "Refit pipeline" button. K-fold cross validation metrics will appear in the
view above the button:

![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/benkpress2.png)
![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/benkpress3.png)
![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/benkpress4.png)
![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/benkpress5.png)
![Load context](https://github.com/dennishedback/benkpress/raw/main/examples/benkpress6.png)

## benkpress?

"Benkpress" is Norwegian for "benchpress"[^1]. Its meaning is relevant in two different
ways. First, benkpress is a tool to simplify the tagging  of PDF-sourced *training*
data for text classifiers. Second, benkpress can also
continuously *benchmark* the classifier intended to be trained by the generated
training data. You know when to quit tagging because your classifier has good
enough predictive power on previously unseen samples.

[^1]: But really, it's actually a way to write the Swedish word bänkpress as a
valid Python package name.

## Known issues

- When trying to fit a classifier from a dataset which was loaded from file instead
  of generated in the application, an exception is thrown.
- If a sample is imported before the application has a valid context, the application
  will crash.


