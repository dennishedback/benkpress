# benkpress

Graphical user interface for creating and evaluating classifiers for PDF
file/page/sentence targets using sklearn compatible pipelines.

## benkpress?

"Benkpress" is Norwegian for "benchpress"[^1]. Its meaning is relevant in two different
ways. First, benkpress is a tool to simplify the tagging  of PDF-sourced *training*
data for text classifiers. Second, benkpress can also
continuously *benchmark* the classifier intended to be trained by the generated
training data. You know when to quit tagging because your classifier has good
enough predictive power on previously unseen samples.

[^1]: But really, it's actually a way to write the Swedish word bänkpress as a
valid Python package name.

## The use case

Imagine having to classify PDFs as either this or that. The key information needed to
make the classification may be contained on a specific page or in a specific sentence.
Imagine then wanting to train a machine learning model to automatically perform this
classification. How do you tag the training data? Do you want to convert all PDFs into
plain text and read it as such, with potential optical text recognition errors? I argue
that it's much easier to read and tag this:

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



## Examples

