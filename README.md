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

## Usage at a glance

1. Interface with benkpress-plugin-api to create your custom sklearn compatible pipeline
   as well as any preprocessing routines you need.
2. Install your pipeline and preprocessor as plugins using the setuptools entrypoints
   specified by benkpress-plugin-api.
3. Load your preprocessor and pipeline in benkpress and use the GUI to tag training data.
4. Save your dataset for later use.

## The benkpress plugin API

Not yet described.

## Examples

Not yet described.

## benkpress?

"Benkpress" is Norwegian for "benchpress"[^1]. Its meaning is relevant in two different
ways. First, benkpress is a tool to simplify the tagging  of PDF-sourced *training*
data for text classifiers. Second, benkpress can also
continuously *benchmark* the classifier intended to be trained by the generated
training data. You know when to quit tagging because your classifier has good
enough predictive power on previously unseen samples.

[^1]: But really, it's actually a way to write the Swedish word bänkpress as a
valid Python package name.

