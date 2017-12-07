# Hackbright-Project
Hackbright Academy


Lglease is a web application that allows users to upload a legal document and autogenerate a response document. The uploaded document is processed via optical character recognition (Textract, using Tesseract), parsed with a natural language processing library (TextBlob), and indexed into an enterprise search engine (Elasticsearch).  Users may customize their responses by selecting among legal arguments to include. Users may also generate a legal document by inputting custom data into the API. All documents are generated as MS word documents (Python-docx). Case status is displayed in an enterprise-style dashboard (JQuery), and case notes are stored in the user's local web storage.
