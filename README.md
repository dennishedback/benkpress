# pdfsupervisors
PyQt/PDFJs GUI for creating and evaluating classifiers for PDF file/page/sentence targets using sklearn compatible pipelines

## Usage

1. Create your sklearn compatible pipeline using the Python console or any other preferred method.
2. Pickle it using joblib.
3. Load your joblib pickle into pdfsupervisors.
4. Use pdfsupervisors to train your pipeline (or evaluate an already fitted pipeline).
5. Pickle your fitted pipeline for use in other applications.
6. pdfsupervisors exports your training data so that your pipeline may be easily refitted using either newer versions of sklearn or on other platforms.
7. Have fun.
