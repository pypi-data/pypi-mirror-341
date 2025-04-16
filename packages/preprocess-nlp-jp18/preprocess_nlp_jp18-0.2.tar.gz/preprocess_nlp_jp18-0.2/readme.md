# Text Preprocessing Python Package

### Installation from PyPi
You can install this package using pip as follows:
```
pip install preprocess_nlp_jp18
```

### Installation from GitHub
You can install this package from GitHub as follows:
```
pip install git+https://github.com/jayesh1802/preprocess_nlp.git --upgrade --force-reinstall
```

### Uninstall the Package

To uninstall the package, use the following command:

```bash
pip uninstall preprocess_nlp
```

### Requirements
You need to install these python packages.
```
pip install spacy==3.7.6
python -m spacy download en_core_web_sm==3.7.1
pip install nltk==3.9.1
pip install beautifulsoup4==4.12.2
pip install textblob==0.18.0.post0
```



## How to Use the Package

### 1. Basic Text Preprocessing

#### Lowercasing Text

```python
import preprocess_nlp_jp18 as ps

text = "HELLO WORLD!"
processed_text = ps.to_lower_case(text)
print(processed_text)  # Output: hello world!
```

#### Expanding Contractions

```python
import preprocess_nlp_jp18 as ps

text = "I'm learning NLP."
processed_text = ps.contraction_to_expansion(text)
print(processed_text)  # Output: I am learning NLP.
```

#### Removing Emails

```python
import preprocess_nlp_jp18 as ps

text = "Contact me at example@example.com"
processed_text = ps.remove_emails(text)
print(processed_text)  # Output: Contact me at 
```
