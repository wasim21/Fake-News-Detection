{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "from collections import Counter\n",
    "import re\n",
    "import numpy as np\n",
    "from sklearn.utils import shuffle\n",
    "from sklearn.feature_extraction.text import TfidfVectorizer\n",
    "from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS\n",
    "from sklearn.metrics import f1_score, accuracy_score \n",
    "import matplotlib.pyplot as plt\n",
    "from sklearn.ensemble import RandomForestClassifier\n",
    "import nltk\n",
    "%matplotlib inline\n",
    "%config InlineBackend.figure_format = 'retina'"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df=pd.read_csv(\"C:/Users/Nandini/Desktop/sa/SourceCode/Combining and Modeling/final.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import nltk\n",
    "nltk.download('stopwords')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import pandas as pd\n",
    "import os\n",
    "import gensim\n",
    "import nltk \n",
    "from sklearn.linear_model import LogisticRegression\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df=pd.read_csv(\"C:/Users/Nandini/Desktop/sa/SourceCode/Combining and Modeling/final.csv\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "import nltk\n",
    "nltk.download('punkt')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "for sentences in df['body']:\n",
    "    print(sentences)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "#sentence=\"my text\"\n",
    "#tokens = nltk.word_tokenize(sentence)\n",
    "#tokens\n",
    "tokens = [nltk.word_tokenize(sentences) for sentences in df['body']]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {
    "scrolled": true
   },
   "outputs": [],
   "source": [
    "model = gensim.models.Word2Vec(tokens, size=300, min_count=1, workers=4)\n",
    "print(\"\\n Training the word2vec model...\\n\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    " model.save(\"word2vec.model\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "model = gensim.models.Word2Vec.load(\"word2vec.model\")\n",
    "model.train(df.body, total_examples=len(df.body), epochs=4)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    " model.save(\"word2vecbody.model\")\n",
    "import numpy as np\n",
    "np.load('word2vecbody.model.wv.vectors.npy')"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "df.columns"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "train = []\n",
    "#getting only the first 4 columns of the file \n",
    "for sentences in df[df.columns[0:4]].values:\n",
    "    train.extend(sentences)\n",
    "#print (train)\n",
    "\n",
    "#Create an array of tokens using nltk\n",
    "#for sentences in train:\n",
    "#    tokens = tokens.append(nltk.word_tokenize(str(sentences)))\n",
    "tokens = [nltk.word_tokenize(str(sentences)) for sentences in train]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "model = gensim.models.Word2Vec(tokens, size=300, min_count=1, workers=4)\n",
    "print(\"\\n Training the word2vec model...\\n\")\n",
    "#model = gensim.models.Word2Vec.load(\"word.model\")\n",
    "model.train(tokens, total_examples=len(tokens), epochs=4)\n",
    "model.save(\"word.model\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "# The two datasets must be the same size\n",
    "model = gensim.models.Word2Vec.load(\"word.model\")\n",
    "max_dataset_size = len(model.trainables.syn1neg)\n",
    "\n",
    "\n",
    "clf = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial').fit(model.trainables.syn1neg, df.fakeness[:max_dataset_size])\n",
    "\n",
    "# Prediction of the first 15 samples of all features\n",
    "predict = clf.predict(model.trainables.syn1neg[:15, :])\n",
    "# Calculating the score of the predictions\n",
    "score = clf.score(model.trainables.syn1neg, Y_dataset[:max_dataset_size])\n",
    "print(\"\\nPrediction word2vec : \\n\", predict)\n",
    "print(\"Score word2vec : \\n\", score)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": [
    "from sklearn.cross_validation import train_test_split\n",
    "#X_headline_train, X_headline_test, y_headline_train, y_headline_test = train_test_split(X_headline,Y, test_size = 0.25, random_state=420)\n",
    "X_train, X_test, y_train, y_test = train_test_split(model.trainables.syn1neg,df['fakeness'], test_size = 0.25, random_state=420)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\gensim\\utils.py:1212: UserWarning: detected Windows; aliasing chunkize to chunkize_serial\n",
      "  warnings.warn(\"detected Windows; aliasing chunkize to chunkize_serial\")\n"
     ]
    }
   ],
   "source": [
    "import pandas as pd\n",
    "import numpy as np\n",
    "from tqdm import tqdm\n",
    "tqdm.pandas(desc=\"progress-bar\")\n",
    "from gensim.models import Doc2Vec\n",
    "from sklearn import utils\n",
    "from sklearn.model_selection import train_test_split\n",
    "import gensim\n",
    "from sklearn.linear_model import LogisticRegression\n",
    "from gensim.models.doc2vec import TaggedDocument\n",
    "import re\n",
    "import seaborn as sns\n",
    "import matplotlib.pyplot as plt\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/html": [
       "<div>\n",
       "<style scoped>\n",
       "    .dataframe tbody tr th:only-of-type {\n",
       "        vertical-align: middle;\n",
       "    }\n",
       "\n",
       "    .dataframe tbody tr th {\n",
       "        vertical-align: top;\n",
       "    }\n",
       "\n",
       "    .dataframe thead th {\n",
       "        text-align: right;\n",
       "    }\n",
       "</style>\n",
       "<table border=\"1\" class=\"dataframe\">\n",
       "  <thead>\n",
       "    <tr style=\"text-align: right;\">\n",
       "      <th></th>\n",
       "      <th>Unnamed: 0</th>\n",
       "      <th>Unnamed: 0.1</th>\n",
       "      <th>body</th>\n",
       "      <th>fakeness</th>\n",
       "      <th>headline</th>\n",
       "      <th>id</th>\n",
       "      <th>published</th>\n",
       "    </tr>\n",
       "  </thead>\n",
       "  <tbody>\n",
       "    <tr>\n",
       "      <th>0</th>\n",
       "      <td>0</td>\n",
       "      <td>0</td>\n",
       "      <td>Print They should pay all the back all the mon...</td>\n",
       "      <td>1</td>\n",
       "      <td>Muslims BUSTED: They Stole Millions In Gov????????t...</td>\n",
       "      <td>6a175f46bcd24d39b3e962ad0f29936721db70db</td>\n",
       "      <td>2016-10-26T21:41:00.000+03:00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>1</th>\n",
       "      <td>1</td>\n",
       "      <td>1</td>\n",
       "      <td>Why Did Attorney General Loretta Lynch Plead T...</td>\n",
       "      <td>1</td>\n",
       "      <td>Re: Why Did Attorney General Loretta Lynch Ple...</td>\n",
       "      <td>2bdc29d12605ef9cf3f09f9875040a7113be5d5b</td>\n",
       "      <td>2016-10-29T08:47:11.259+03:00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>2</th>\n",
       "      <td>2</td>\n",
       "      <td>2</td>\n",
       "      <td>Red State : \\r\\r\\nFox News Sunday reported thi...</td>\n",
       "      <td>1</td>\n",
       "      <td>BREAKING: Weiner Cooperating With FBI On Hilla...</td>\n",
       "      <td>c70e149fdd53de5e61c29281100b9de0ed268bc3</td>\n",
       "      <td>2016-10-31T01:41:49.479+02:00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>3</th>\n",
       "      <td>3</td>\n",
       "      <td>3</td>\n",
       "      <td>Email Kayla Mueller was a prisoner and torture...</td>\n",
       "      <td>1</td>\n",
       "      <td>PIN DROP SPEECH BY FATHER OF DAUGHTER Kidnappe...</td>\n",
       "      <td>7cf7c15731ac2a116dd7f629bd57ea468ed70284</td>\n",
       "      <td>2016-11-01T05:22:00.000+02:00</td>\n",
       "    </tr>\n",
       "    <tr>\n",
       "      <th>4</th>\n",
       "      <td>4</td>\n",
       "      <td>4</td>\n",
       "      <td>Email HEALTHCARE REFORM TO MAKE AMERICA GREAT ...</td>\n",
       "      <td>1</td>\n",
       "      <td>FANTASTIC! TRUMP'S 7 POINT PLAN To Reform Heal...</td>\n",
       "      <td>0206b54719c7e241ffe0ad4315b808290dbe6c0f</td>\n",
       "      <td>2016-11-01T21:56:00.000+02:00</td>\n",
       "    </tr>\n",
       "  </tbody>\n",
       "</table>\n",
       "</div>"
      ],
      "text/plain": [
       "   Unnamed: 0  Unnamed: 0.1  \\\n",
       "0           0             0   \n",
       "1           1             1   \n",
       "2           2             2   \n",
       "3           3             3   \n",
       "4           4             4   \n",
       "\n",
       "                                                body  fakeness  \\\n",
       "0  Print They should pay all the back all the mon...         1   \n",
       "1  Why Did Attorney General Loretta Lynch Plead T...         1   \n",
       "2  Red State : \\r\\r\\nFox News Sunday reported thi...         1   \n",
       "3  Email Kayla Mueller was a prisoner and torture...         1   \n",
       "4  Email HEALTHCARE REFORM TO MAKE AMERICA GREAT ...         1   \n",
       "\n",
       "                                            headline  \\\n",
       "0  Muslims BUSTED: They Stole Millions In Gov????????t...   \n",
       "1  Re: Why Did Attorney General Loretta Lynch Ple...   \n",
       "2  BREAKING: Weiner Cooperating With FBI On Hilla...   \n",
       "3  PIN DROP SPEECH BY FATHER OF DAUGHTER Kidnappe...   \n",
       "4  FANTASTIC! TRUMP'S 7 POINT PLAN To Reform Heal...   \n",
       "\n",
       "                                         id                      published  \n",
       "0  6a175f46bcd24d39b3e962ad0f29936721db70db  2016-10-26T21:41:00.000+03:00  \n",
       "1  2bdc29d12605ef9cf3f09f9875040a7113be5d5b  2016-10-29T08:47:11.259+03:00  \n",
       "2  c70e149fdd53de5e61c29281100b9de0ed268bc3  2016-10-31T01:41:49.479+02:00  \n",
       "3  7cf7c15731ac2a116dd7f629bd57ea468ed70284  2016-11-01T05:22:00.000+02:00  \n",
       "4  0206b54719c7e241ffe0ad4315b808290dbe6c0f  2016-11-01T21:56:00.000+02:00  "
      ]
     },
     "execution_count": 2,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "df=pd.read_csv(\"C:/Users/Nandini/Desktop/sa/SourceCode/Combining and Modeling/final.csv\")\n",
    "df.head()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 864x288 with 1 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    }
   ],
   "source": [
    "cnt_pro = df['fakeness'].value_counts()\n",
    "plt.figure(figsize=(12,4))\n",
    "sns.barplot(cnt_pro.index, cnt_pro.values, alpha=0.8)\n",
    "plt.ylabel('Number of Occurrences', fontsize=12)\n",
    "plt.xlabel('fake', fontsize=12)\n",
    "plt.xticks(rotation=90)\n",
    "plt.show();"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [],
   "source": [
    "from bs4 import BeautifulSoup\n",
    "def cleanText(text):\n",
    "    text = BeautifulSoup(text, \"lxml\").text\n",
    "    text = re.sub(r'\\|\\|\\|', r' ', text) \n",
    "    text = re.sub(r'http\\S+', r'<URL>', text)\n",
    "    text = text.lower()\n",
    "    text = text.replace('x', '')\n",
    "    return text\n",
    "df['body'] = df['body'].apply(cleanText)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [],
   "source": [
    "train, test = train_test_split(df, test_size=0.3, random_state=42)\n",
    "import nltk\n",
    "from nltk.corpus import stopwords\n",
    "def tokenize_text(text):\n",
    "    tokens = []\n",
    "    for sent in nltk.sent_tokenize(text):\n",
    "        for word in nltk.word_tokenize(sent):\n",
    "            if len(word) < 2:\n",
    "                continue\n",
    "            tokens.append(word.lower())\n",
    "    return tokens\n",
    "train_tagged = train.apply(\n",
    "    lambda r: TaggedDocument(words=tokenize_text(r['body']), tags=[r.fakeness]), axis=1)\n",
    "test_tagged = test.apply(\n",
    "    lambda r: TaggedDocument(words=tokenize_text(r['body']), tags=[r.fakeness]), axis=1)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "TaggedDocument(words=['rescuers', 'on', 'the', 'indonesian', 'island', 'of', 'lombok', 'have', 'been', 'struggling', 'to', 'reach', 'possible', 'survivors', 'after', 'the', 'devastating', 'earthquake', 'due', 'to', 'lack', 'of', 'equipment', 'in', 'some', 'districts', 'in', 'northern', 'lombok', 'authorities', 'said', 'more', 'than', 'half', 'the', 'homes', 'had', 'been', 'destroyed', 'or', 'badly', 'damaged', 'by', 'the', 'quake', 'on', 'sunday', 'which', 'has', 'killed', 'at', 'least', '98', 'people', 'and', 'injured', '269.', 'there', 'was', 'massive', 'damage', 'said', 'sutopo', 'purwo', 'nugroho', 'of', 'the', 'disaster', 'management', 'agency', 'and', 'some', 'areas', 'were', 'unreachable', 'rescue', 'teams', 'were', 'trying', 'to', 'dig', 'up', 'bodies', 'from', 'underneath', 'mosque', 'in', 'the', 'village', 'of', 'lading-lading', 'the', 'building????????s', 'green', 'dome', 'was', 'perched', 'on', 'top', 'of', 'slabs', 'of', 'flattened', 'concrete', 'about', '40', 'people', 'were', 'believed', 'to', 'have', 'been', 'inside', 'the', 'mosque', 'when', 'the', '6.9-magnitude', 'earthquake', 'hit', 'lack', 'of', 'heavy', 'lifting', 'equipment', 'was', 'hampering', 'the', 'relief', 'effort', 'nugroho', 'said', 'with', 'some', 'rescuers', 'forced', 'to', 'dig', 'by', 'hand', 'other', 'obstacles', 'in', 'the', 'mountainous', 'north', 'and', 'east', 'of', 'lombok', 'included', 'collapsed', 'bridges', 'and', 'electricity', 'and', 'communication', 'blackouts', 'debris', 'blocked', 'damaged', 'roads', 'the', 'earthquake', 'was', 'the', 'second', 'in', 'week', 'to', 'hit', 'lombok', 'following', 'previous', 'one', 'on', '29', 'july', 'which', 'killed', '16', 'people', 'and', 'damaged', 'numerous', 'houses', 'the', 'death', 'toll', 'form', 'this', 'quake', 'is', 'epected', 'to', 'increase', 'about', '20,000', 'people', 'are', 'in', 'temporary', 'shelters', 'najmul', 'akhyar', 'the', 'north', 'lombok', 'district', 'chief', 'estimated', 'that', '80', 'of', 'the', 'region', 'had', 'been', 'damaged', 'by', 'the', 'quake', 'nugroho', 'said', '???????we', 'epect', 'the', 'number', 'of', 'fatalities', 'to', 'keep', 'rising', 'all', 'victims', 'who', 'died', 'are', 'indonesians.????????', 'search', 'teams', 'rescued', 'between', '2,000', 'and', '2,700', 'tourists', 'from', 'the', 'gili', 'islands', 'three', 'tiny', 'coral-fringed', 'tropical', 'islands', 'off', 'the', 'north-west', 'coast', 'of', 'lombok', 'footage', 'posted', 'online', 'by', 'rescue', 'officials', 'showed', 'hundreds', 'of', 'panicked', 'tourists', 'and', 'locals', 'crowding', 'on', 'to', 'powder-white', 'beaches', 'waiting', 'for', 'evacuation', 'james', 'kelsall', '28-year-old', 'british', 'tourist', 'was', 'visiting', 'one', 'of', 'the', 'gili', 'islands', 'with', 'his', 'partner', 'when', 'the', 'quake', 'struck', 'speaking', 'from', 'beach', 'as', 'he', 'awaited', 'evacuation', 'the', 'teacher', 'said', '???????there', 'were', 'lots', 'of', 'injuries', 'and', 'pain', 'on', 'the', 'island', 'from', 'buildings', 'that', 'had', 'collapsed', 'on', 'to', 'people', '???????the', 'most', 'terrifying', 'part', 'was', 'the', 'tsunami', 'warning', 'that', 'followed', 'all', 'the', 'locals', 'were', 'frantically', 'running', 'and', 'screaming', 'putting', 'on', 'lifejackets.????????', 'hospitals', 'were', 'reportedly', 'full', 'and', 'injured', 'people', 'were', 'being', 'treated', 'in', 'car', 'parks', 'and', 'makeshift', 'medical', 'tents', 'aid', 'agencies', 'said', 'they', 'were', 'distributing', 'food', 'water', 'tents', 'blankets', 'and', 'hygiene', 'kits', 'zul', 'ashfi', 'the', 'humanitarian', 'programme', 'coordinator', 'for', 'islamic', 'relief', 'in', 'indonesia', 'described', 'the', 'situation', 'as', '???????catastrophic????????', '???????i', 'saw', 'people', 'fleeing', 'for', 'their', 'lives', 'screaming', 'for', 'help', 'into', 'their', 'mobile', 'phones', 'as', 'they', 'ran', '????????', 'he', 'said', '???????it', 'was', 'very', 'traumatic', 'they', 'are', 'now', 'sleeping', 'in', 'the', 'open', 'air', 'and', 'have', 'nothing', 'we', 'are', 'now', 'working', 'against', 'the', 'clock', 'to', 'reach', 'as', 'many', 'people', 'in', 'need', 'as', 'we', 'can.????????', 'the', 'earthquake', 'caused', 'widespread', 'panic', 'across', 'lombok', 'with', 'residents', 'fleeing', 'their', 'homes', 'and', 'heading', 'to', 'higher', 'ground', 'after', 'the', 'tremor', 'initially', 'triggered', 'tsunami', 'warning', 'rescue', 'officials', 'said', 'much', 'of', 'the', 'damage', 'was', 'in', 'lombok????????s', 'main', 'city', 'of', 'mataram', 'with', 'several', 'areas', 'losing', 'power', 'and', 'patients', 'evacuated', 'from', 'the', 'main', 'hospital', 'iman', 'who', 'like', 'many', 'indonesians', 'has', 'one', 'name', 'told', 'agence', 'france-presse', '???????everyone', 'immediately', 'ran', 'out', 'of', 'their', 'homes', 'everyone', 'is', 'panicking.????????', 'the', 'united', 'states', 'geological', 'survey', 'said', 'the', 'epicentre', 'of', 'the', 'quake', 'was', 'on', 'land', 'on', 'lombok', 'but', 'initial', 'reports', 'put', 'it', 'just', 'off', 'the', 'coast', 'it', 'struck', 'at', 'depth', 'of', '31km', '19', 'miles', 'two', 'helicopters', 'have', 'been', 'deployed', 'to', 'assist', 'in', 'emergency', 'operations', 'and', 'the', 'military', 'has', 'sent', 'troops', 'and', 'medical', 'personnel', 'as', 'well', 'as', 'medical', 'supplies', 'and', 'communications', 'equipment', 'government', 'ministers', 'and', 'officials', 'from', 'countries', 'across', 'the', 'region', 'who', 'were', 'attending', 'summit', 'on', 'security', 'and', 'counter-terrorism', 'in', 'mataram', 'were', 'among', 'those', 'evacuated', 'from', 'their', 'hotels', 'singapore????????s', 'law', 'and', 'home', 'affairs', 'minister', 'shanmugam', 'said', 'his', '10th-floor', 'hotel', 'room', 'shook', 'violently', 'and', 'the', 'walls', 'cracked', '???????it', 'was', 'quite', 'impossible', 'to', 'stand', 'up', 'heard', 'screams', '????????', 'he', 'wrote', 'on', 'facebook', '???????came', 'out', 'and', 'made', 'my', 'way', 'down', 'staircase', 'while', 'building', 'was', 'still', 'shaking', 'power', 'went', 'out', 'for', 'while', 'lots', 'of', 'cracks', 'fallen', 'doors.????????', 'the', 'australian', 'home', 'affairs', 'minister', 'peter', 'dutton', 'said', 'all', 'the', 'members', 'of', 'his', 'country????????s', 'delegation', 'were', 'safe', 'the', 'quake', 'was', 'also', 'strongly', 'felt', 'in', 'bali', 'where', 'people', 'ran', 'out', 'of', 'houses', 'hotels', 'and', 'restaurants', 'pictures', 'showed', 'damage', 'to', 'two', 'shopping', 'centres', 'and', 'temple', 'in', 'ubud', 'despite', 'superficial', 'damage', 'flights', 'from', 'lombok', 'airport', 'and', 'bali????????s', 'ngurah', 'rai', 'airport', 'continued', 'to', 'operate', 'on', 'sunday', 'evening', 'michelle', 'lindsay', 'an', 'australian', 'tourist', 'in', 'bali', 'said', '???????all', 'the', 'hotel', 'guests', 'were', 'running', 'so', 'did', 'too', 'people', 'filled', 'the', 'streets', 'lot', 'of', 'officials', 'were', 'urging', 'people', 'not', 'to', 'panic.????????', 'the', 'american', 'model', 'chrissy', 'teigen', 'was', 'on', 'holiday', 'in', 'bali', 'with', 'her', 'family', 'when', 'the', 'quake', 'struck', 'and', 'tweeted', 'throughout', 'the', 'tremors', 'an', 'indonesian', 'imam', 'became', 'hero', 'after', 'stoically', 'reciting', 'evening', 'prayers', 'during', 'the', 'quake', 'mobile', 'phone', 'footage', 'showed', 'him', 'continuing', 'to', 'preach', 'at', 'mosque', 'in', 'denpasar', 'bali', 'as', 'people', 'made', 'for', 'the', 'eits', 'indonesia', 'is', 'one', 'of', 'the', 'most', 'disaster-prone', 'nations', 'on', 'earth', 'it', 'straddles', 'the', 'pacific', 'ring', 'of', 'fire', 'where', 'tectonic', 'plates', 'collide', 'and', 'many', 'of', 'the', 'world????????s', 'volcanic', 'eruptions', 'and', 'earthquakes', 'occur'], tags=[0])"
      ]
     },
     "execution_count": 6,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "train_tagged.values[3]"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 7,
   "metadata": {},
   "outputs": [],
   "source": [
    "import multiprocessing\n",
    "cores = multiprocessing.cpu_count()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1388236.83it/s]\n"
     ]
    }
   ],
   "source": [
    "model_dbow = Doc2Vec(dm=0, vector_size=300, negative=5, hs=0, min_count=2, sample = 0, workers=cores)\n",
    "model_dbow.build_vocab([x for x in tqdm(train_tagged.values)])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 9,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384419.74it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1211201.79it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1076695.31it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1293350.25it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 922736.38it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 964499.78it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1122993.88it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1052811.32it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384230.62it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2154334.89it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490627.66it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384254.25it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1292010.35it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384088.81it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2153304.82it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384254.25it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384112.44it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2153476.43it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422258.81it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490737.31it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422475.97it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422837.99it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1615096.60it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1937783.89it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490764.72it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422620.76it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2153190.43it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761786.35it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2421679.91it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2153476.43it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761824.64it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422693.17it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2153190.43it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422475.97it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422548.37it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1615000.07it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2425738.03it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422837.99it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422837.99it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384206.98it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490682.48it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422620.76it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761939.52it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2422620.76it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1940334.95it/s]\n"
     ]
    }
   ],
   "source": [
    "#time\n",
    "for epoch in range(45):\n",
    "    model_dbow.train(utils.shuffle([x for x in tqdm(train_tagged.values)]), total_examples=len(train_tagged.values), epochs=1)\n",
    "    model_dbow.alpha -= 0.002\n",
    "    model_dbow.min_alpha = model_dbow.alpha"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 10,
   "metadata": {},
   "outputs": [],
   "source": [
    "def vec_for_learning(model, tagged_docs):\n",
    "    sents = tagged_docs.values\n",
    "    targets, regressors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in sents])\n",
    "    return targets, regressors\n",
    "def vec_for_learning(model, tagged_docs):\n",
    "    sents = tagged_docs.values\n",
    "    targets, regressors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in sents])\n",
    "    return targets, regressors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 11,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Testing accuracy 0.612942170711095\n",
      "Testing F1 score: 0.5926642075536247\n"
     ]
    }
   ],
   "source": [
    "y_train_dbow, X_train_dbow = vec_for_learning(model_dbow, train_tagged)\n",
    "y_test_dbow, X_test_dbow = vec_for_learning(model_dbow, test_tagged)\n",
    "logreg = LogisticRegression(n_jobs=1, C=1e5)\n",
    "logreg.fit(X_train_dbow, y_train_dbow)\n",
    "y_pred_dbow = logreg.predict(X_test_dbow)\n",
    "from sklearn.metrics import accuracy_score, f1_score\n",
    "print('Testing accuracy %s' % accuracy_score(y_test_dbow, y_pred_dbow))\n",
    "print('Testing F1 score: {}'.format(f1_score(y_test_dbow, y_pred_dbow, average='weighted')))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 12,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761709.77it/s]\n"
     ]
    }
   ],
   "source": [
    "model_dmm = Doc2Vec(dm=1, dm_mean=1, vector_size=300, window=10, negative=5, min_count=1, workers=5, alpha=0.065, min_alpha=0.065)\n",
    "model_dmm.build_vocab([x for x in tqdm(train_tagged.values)])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 13,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1614839.21it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761862.93it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490682.48it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384230.62it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1614935.72it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384112.44it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384112.44it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490709.90it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490682.48it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1385745.04it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490682.48it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490709.90it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490655.07it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384301.53it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1491258.36it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490627.66it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384206.98it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490572.84it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384136.08it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490545.43it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490490.62it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384112.44it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384112.44it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490709.90it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490737.31it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1615064.42it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1614807.04it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384254.25it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490792.14it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490764.72it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384443.38it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1491066.35it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490709.90it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490600.25it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384183.34it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 2153419.23it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490518.03it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490737.31it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761709.77it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490737.31it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490655.07it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1384183.34it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1761862.93it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490572.84it/s]\n",
      "100%|??????????????????????????????| 19327/19327 [00:00<00:00, 1490819.56it/s]\n"
     ]
    }
   ],
   "source": [
    "for epoch in range(45):\n",
    "    model_dmm.train(utils.shuffle([x for x in tqdm(train_tagged.values)]), total_examples=len(train_tagged.values), epochs=1)\n",
    "    model_dmm.alpha -= 0.002\n",
    "    model_dmm.min_alpha = model_dmm.alpha"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 14,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Testing accuracy 0.9498973801762647\n",
      "Testing F1 score: 0.9498814470291072\n"
     ]
    }
   ],
   "source": [
    "y_train_dm, X_train_dm = vec_for_learning(model_dmm, train_tagged)\n",
    "y_test_dm, X_test_dm = vec_for_learning(model_dmm, test_tagged)\n",
    "logreg.fit(X_train_dm, y_train_dm)\n",
    "y_pred_dm = logreg.predict(X_test_dm)\n",
    "print('Testing accuracy %s' % accuracy_score(y_test_dm, y_pred_dm))\n",
    "print('Testing F1 score: {}'.format(f1_score(y_test_dm, y_pred_dm, average='weighted')))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 15,
   "metadata": {},
   "outputs": [],
   "source": [
    "model_dbow.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)\n",
    "model_dmm.delete_temporary_training_data(keep_doctags_vectors=True, keep_inference=True)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 16,
   "metadata": {},
   "outputs": [],
   "source": [
    "from gensim.test.test_doc2vec import ConcatenatedDoc2Vec\n",
    "new_model = ConcatenatedDoc2Vec([model_dbow, model_dmm])"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 17,
   "metadata": {},
   "outputs": [],
   "source": [
    "def get_vectors(model, tagged_docs):\n",
    "    sents = tagged_docs.values\n",
    "    targets, regressors = zip(*[(doc.tags[0], model.infer_vector(doc.words, steps=20)) for doc in sents])\n",
    "    return targets, regressors"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 18,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Testing accuracy 0.9414463358686467\n",
      "Testing F1 score: 0.9414706890767734\n"
     ]
    }
   ],
   "source": [
    "y_train, X_train = get_vectors(new_model, train_tagged)\n",
    "y_test, X_test = get_vectors(new_model, test_tagged)\n",
    "logreg.fit(X_train, y_train)\n",
    "y_pred = logreg.predict(X_test)\n",
    "print('Testing accuracy %s' % accuracy_score(y_test, y_pred))\n",
    "print('Testing F1 score: {}'.format(f1_score(y_test, y_pred, average='weighted')))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 23,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\sklearn\\utils\\deprecation.py:77: DeprecationWarning: Function plot_confusion_matrix is deprecated; This will be removed in v0.4.0. Please use scikitplot.metrics.plot_confusion_matrix instead.\n",
      "  warnings.warn(msg, category=DeprecationWarning)\n",
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\matplotlib\\cbook\\deprecation.py:107: MatplotlibDeprecationWarning: Passing one of 'on', 'true', 'off', 'false' as a boolean is deprecated; use an actual boolean (True/False) instead.\n",
      "  warnings.warn(message, mplDeprecation, stacklevel=1)\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "confusion matrix of logistic regression of Doc2vec using distributed memory\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\sklearn\\utils\\deprecation.py:77: DeprecationWarning: Function plot_confusion_matrix is deprecated; This will be removed in v0.4.0. Please use scikitplot.metrics.plot_confusion_matrix instead.\n",
      "  warnings.warn(msg, category=DeprecationWarning)\n",
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\matplotlib\\cbook\\deprecation.py:107: MatplotlibDeprecationWarning: Passing one of 'on', 'true', 'off', 'false' as a boolean is deprecated; use an actual boolean (True/False) instead.\n",
      "  warnings.warn(message, mplDeprecation, stacklevel=1)\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "confusion matrix of logistic regression of Doc2vec using distributed bag of words\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\sklearn\\utils\\deprecation.py:77: DeprecationWarning: Function plot_confusion_matrix is deprecated; This will be removed in v0.4.0. Please use scikitplot.metrics.plot_confusion_matrix instead.\n",
      "  warnings.warn(msg, category=DeprecationWarning)\n",
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\matplotlib\\cbook\\deprecation.py:107: MatplotlibDeprecationWarning: Passing one of 'on', 'true', 'off', 'false' as a boolean is deprecated; use an actual boolean (True/False) instead.\n",
      "  warnings.warn(message, mplDeprecation, stacklevel=1)\n"
     ]
    },
    {
     "data": {
      "image/png": "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\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "confusion matrix of logistic regression of Doc2vec combining both models\n"
     ]
    }
   ],
   "source": [
    "import scikitplot.plotters as skplt\n",
    "def plot_cmat(y_test, y_pred):\n",
    "    skplt.plot_confusion_matrix(y_test,y_pred)\n",
    "    plt.show()\n",
    "    \n",
    "plot_cmat(y_test_dm, y_pred_dm)\n",
    "print(\"confusion matrix of logistic regression of Doc2vec using distributed memory\")\n",
    "plot_cmat(y_test_dbow, y_pred_dbow)\n",
    "print(\"confusion matrix of logistic regression of Doc2vec using distributed bag of words\")\n",
    "plot_cmat(y_test, y_pred)\n",
    "print(\"confusion matrix of logistic regression of Doc2vec combining both models\")\n"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 25,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Testing accuracy 0.9489315465411083\n",
      "Testing F1 score: 0.9489114179945066\n"
     ]
    }
   ],
   "source": [
    "C = 1.0  \n",
    "from sklearn import svm\n",
    "svc = svm.SVC(kernel='linear', C=C).fit(X_train_dm, y_train_dm)\n",
    "y_pred= svc.predict(X_test_dm)\n",
    "print('Testing accuracy %s' % accuracy_score(y_test_dm, y_pred))\n",
    "print('Testing F1 score: {}'.format(f1_score(y_test_dm, y_pred, average='weighted')))"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 27,
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\sklearn\\utils\\deprecation.py:77: DeprecationWarning: Function plot_confusion_matrix is deprecated; This will be removed in v0.4.0. Please use scikitplot.metrics.plot_confusion_matrix instead.\n",
      "  warnings.warn(msg, category=DeprecationWarning)\n",
      "C:\\Users\\Nandini\\Anaconda3\\lib\\site-packages\\matplotlib\\cbook\\deprecation.py:107: MatplotlibDeprecationWarning: Passing one of 'on', 'true', 'off', 'false' as a boolean is deprecated; use an actual boolean (True/False) instead.\n",
      "  warnings.warn(message, mplDeprecation, stacklevel=1)\n"
     ]
    },
    {
     "data": {
      "image/png": "iVBORw0KGgoAAAANSUhEUgAAAT8AAAEWCAYAAAAQBZBVAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAADl0RVh0U29mdHdhcmUAbWF0cGxvdGxpYiB2ZXJzaW9uIDIuMi4yLCBodHRwOi8vbWF0cGxvdGxpYi5vcmcvhp/UCwAAIABJREFUeJzt3Xm81VW9//HX+5zD4IACIkqmSYqKWiKimMMvNEU0y9mcksz0Vtqta8PVtOuQOJdmWl1LFLREs1RSDMmy0hwQRRRHHLgOCCJKTiDg5/fHdx3c4Dn77O9h77PP2fv97PF9sPf6rr2+66v2Ya3vsD6KCMzM6k1DtTtgZlYNDn5mVpcc/MysLjn4mVldcvAzs7rk4GdmdcnBr8ZIWk3SnyQtlPT7VWjnSEl3lLNv1SDpdkmjq90P63wc/KpE0hGSHpT0tqQ56f+ku5Sh6YOB9YB1IuKQ9jYSEb+NiJFl6M8KJI2QFJL+uFL5Nqn8rhLbOUPStW3Vi4i9I2JcO7trNczBrwoknQRcApxDFqg2An4B7FeG5j8BPB0RS8vQVqW8BuwkaZ2CstHA0+U6gDL+79taFxHeOnAD1gbeBg4pUqcHWXB8JW2XAD3SvhHAS8B3gXnAHOCYtO9M4H1gSTrGscAZwLUFbW8MBNCUvn8FeA54C3geOLKg/O6C3+0ETAUWpj93Kth3F/Bj4J7Uzh1Av1bOrbn/vwJOSGWNqex/gLsK6v4MeBH4NzAN2DWVj1rpPB8p6MeY1I/3gE1T2dfS/l8CNxa0fz5wJ6Bq/3fhreM3/83Y8T4D9ARuKlLnVGBHYAiwDbADcFrB/vXJgugGZAHuckl9IuJ0stHk9RGxZkRcWawjktYALgX2joheZAFuegv1+gK3pbrrAD8Fbltp5HYEcAzQH+gOfK/YsYHxwNHp817ATLJAX2gq2T+DvsDvgN9L6hkRf17pPLcp+M2XgeOBXsDsldr7LvBpSV+RtCvZP7vREeF3POuQg1/HWweYH8WnpUcCZ0XEvIh4jWxE9+WC/UvS/iURMYls9LN5O/vzAbC1pNUiYk5EzGyhzueBZyLimohYGhHXAU8CXyioc1VEPB0R7wE3kAWtVkXEv4C+kjYnC4LjW6hzbUS8no75E7IRcVvneXVEzEy/WbJSe+8CR5EF72uBb0XES220ZzXKwa/jvQ70k9RUpM7HWHHUMjuVLW9jpeD5LrBm3o5ExDvAl4CvA3Mk3SZpixL609ynDQq+v9qO/lwDnAjsRgsjYUnflfREunP9Jtlot18bbb5YbGdEPEA2zRdZkLY65eDX8e4FFgH7F6nzCtmNi2Yb8dEpYaneAVYv+L5+4c6ImBwRewIDyEZzvy6hP819ermdfWp2DfBNYFIalS2XpqX/DRwK9ImI3mTXG9Xc9VbaLDqFlXQC2QjyFeAH7e+6dXUOfh0sIhaSXdi/XNL+klaX1E3S3pIuSNWuA06TtK6kfql+m491tGI68P8kbSRpbeCU5h2S1pP0xXTtbzHZ9HlZC21MAjZLj+c0SfoSsCVwazv7BEBEPA98luwa58p6AUvJ7gw3SfofYK2C/XOBjfPc0ZW0GXA22dT3y8APJBWdnlvtcvCrgoj4KXAS2U2M18imaicCN6cqZwMPAjOAR4GHUll7jjUFuD61NY0VA1YD2U2AV4AFZIHomy208Tqwb6r7OtmIad+ImN+ePq3U9t0R0dKodjJwO9njL7PJRsuFU9rmB7hfl/RQW8dJlxmuBc6PiEci4hngh8A1knqsyjlY1yTf6DKzeuSRn5nVJQc/M6tLDn5mVpcc/MysLhV70LbDqWm1UPde1e6G5bDt4I2q3QXLYfbsF5g/f77artm6xrU+EbH0vZLqxnuvTY6IUcXqSGoke7rh5YjYV9LVZE8eLExVvhIR0yWJ7H3vfcgepP9KRDyU2hjNh6+Anh0lrOTTuYJf91702PzQanfDcrjn/suq3QXLYefhw1a5jVj6Xsn/P100/fK23sgB+DbwBCs+x/n9iLhxpXp7A4PSNpxsoYrh6d3z04FhZA+5T5M0MSLeKHZQT3vNLCeBGkrb2mpJ+jjZu+O/KeHA+wHjI3Mf0FvSALKFMaZExIIU8KaQrfxTlIOfmeUjoKGxtC17j/3Bgu34lVq7hOyh+Q9WKh8jaYakiwseQt+AFR90fymVtVZeVKea9ppZF6GSLxvOj4gW59qS9gXmRcQ0SSMKdp1CtlBGd+AKsne8z+LD97oLRZHyojzyM7Ocyjbt3Rn4oqQXgAnA7pKuTUurRUQsBq4iW88SshHdhgW//zjZq5mtlRfl4Gdm+UmlbUVExCkR8fGI2Bg4DPhrRByVruOR7u7uDzyWfjIRODqlKNgRWBgRc8jeAx8pqY+kPsDIVFaUp71mlo8o6WbGKvitpHXTkaaTrTcJ2epC+wCzyB51OQYgIhZI+jHZyt+QLfS7oK2DOPiZWU5tj+ryioi7yPKtEBG7t1IngBNa2TcWGJvnmA5+ZpZfdie3S3PwM7OcVOlpb4dw8DOzfETZp73V4OBnZvl55Gdm9cfTXjOrRwIafcPDzOqRr/mZWf3xtNfM6pVHfmZWlzzyM7O6U8KiBV2Bg5+Z5efX28ys/viGh5nVK097zazuVH49vw7h4GdmOdXGtLfrn4GZdbzSs7e1SVKjpIcl3Zq+D5R0v6RnJF0vqXsq75G+z0r7Ny5o45RU/pSkvUo6hdwnbWZWhhweBZqTljc7H7g4IgYBbwDHpvJjgTciYlPg4lQPSVuS5QDZiixf7y8ktRl5HfzMLB9VLml5Slq0O3BjqjKOLIkRZEnLx6XPNwKfS/X3AyZExOKIeJ4sx0dzxrdWOfiZWX6lj/zyJi1fB3gzIpam74UJyJcnJ0/7F6b6TlpuZh1DlUtaXiwBeVmTljv4mVku2Sr2ZXnOrzlp+T5AT2AtspFgb0lNaXRXmIC8OTn5S5KagLWBBThpuZl1CAk1lLYV00rS8iOBvwEHp2qjgVvS54npO2n/X1M6y4nAYelu8EBgEPBAW6fhkZ+Z5VamkV9r/huYIOls4GHgylR+JXCNpFlkI77DACJipqQbgMeBpcAJEbGsrYM4+JlZbuUOfislLX+OFu7WRsQi4JBWfj8GGJPnmA5+ZpZbhUd+HcLBz8zyES3fX+1iHPzMLBchj/zMrD41NHT9B0Uc/MwsN4/8zKz++JqfmdUrj/zMrO74hoeZ1a22Xl3rChz8zCwfedprZnXKwc/M6pKDn5nVHd/wMLP61fVjn4OfmeUkv95mZnWqFqa9XT98m1nHU4lbsSaknpIekPSIpJmSzkzlV0t6XtL0tA1J5ZJ0aUpOPkPS0IK2Rqck589IGt3aMQs5+K2ChgZx73X/zR9+9nUArjjzKJ649Qzum3Ay9004mU9vlmXP23W7Qbz6jwuXl59y/KjlbZxw+Age/P0PmXbjqZx4xIhqnEbdefHFF9lrj90Y8qnBDN1mKy679GcALFiwgM+P2pOtBw/i86P25I033gDgqSef5LO7fIa11+jBxT+9qJpd7zQklbS1YTGwe0RsAwwBRknaMe37fkQMSdv0VLY3WX6OQcDxwC9TX/oCpwPDyVaAPl1Sn7YOXtFpr6RRwM+ARuA3EXFeJY/X0U48Yjeeen4uvdboubzsh5fczE1/mf6Ruvc8/CwHfftXK5RtuckAjjlwJ3b98oW8v2QZEy//JrffPZNn/++1ive9njU1NXHeBT9h26FDeeutt9hp+HZ8bo89uWb81YzY/XN8/wcnc+EF53HRBecx5tzz6dO3Lz+5+FL+NPHmane9UygxsLUpJR96O33tlrZiKSf3A8an390nqbekAcAIYEpELEj9mwKMAq4rdvyKjfwkNQKXk0XrLYHDJW1ZqeN1tA3692bULltx1U3/ancbWwxcnwcefYH3Fi1h2bIP+Oe0Wey32zZl7KW1ZMCAAWw7NJsx9erViy22GMwrr7zMrX+6haO+nM2Yjvry6OXBrn///gzbfnu6detWtT53NjlGfkWTlktqlDQdmEcWwO5Pu8akqe3FknqkstaSk7craXklp707ALMi4rmIeB+YQBa5a8KF3z+IU392Mx98sOJfVGec8AUeuP4ULvjugXTv9uHAevinB3L/9Sdz82XfYPAn1wdg5rOvsMvQTem79hqs1rMbo3bZio+v3+Zo3cpo9gsvMH36w2y/w3DmzZ3LgAEDgCxAvjZvXpV713nlSF05PyKGFWxXFLYTEcsiYghZrt0dJG0NnAJsAWwP9CXL5gZlTlpeyeBXUjSWdHzz3wqx9L0Kdqd89t51a+YteIuHn3hxhfL/+flEtjngx+xy1IX0WXsNvnvMHgBMf/JFNt/nRwz/0nn8csLfueHi7C+/p56fy0+unsKtvzyRiZefwIynX2bp0jYz7lmZvP322xx+6EFc+JNLWGuttardnS6lTNf8louIN8myt42KiDmRWQxcxYeZ3FpLTt7pkpaXFI0j4ormvxXUtFoFu1M+nxnySfb97Kd48rYzGX/eMYzYfjPGnn00r87/NwDvL1nK+FvuY9hWGwPw1juLeOe99wGYfPfjdGtqZJ3eawAw7uZ72emI89nz2Et4Y+E7zPL1vg6xZMkSDj/0IL50+JHsf8CBAPRfbz3mzJkDwJw5c1i3f/9qdrHzUnmCn6R1JfVOn1cD9gCeTNfxUNbA/sBj6ScTgaPTXd8dgYURMQeYDIyU1Cfd6BiZyoqqZPBrVzTuCv7n5xPZdNSP2OLzp3P0yVdx19Sn+epp41m/34ejhy/u9mkefzY73fXW6bW8fNhWn6BB4vU33wFg3T5rArDh+n3Yb/dtuOHPD3bgmdSniODrxx3L5lsM5tv/ddLy8s/v+0WuvWYcANdeM459v1AzV2nKSoBU2taGAcDfJM0AppJd87sV+K2kR4FHgX7A2an+JOA5YBbwa+CbAOlGx49TG1OBs5pvfhRTybu9U4FBkgYCL5NlVz+igseruqvGjKZfn15IMOOpl/jWmAkAHLDHthx3yK4sXbaMRYuWcPQpVy3/zXUXfY2+vddgydJlfOe8G3jzra4x9e/K/nXPPfzut9ew9dafYvh2QwA48+xz+N4PTuaoww9l3FVXsuGGG/HbCb8H4NVXX2XnHYfx1r//TUNDA5ddegkPz3i8jqfKZbvbOwPYtoXy3VupH8AJrewbC4zNc3xl7VWGpH2AS8gedRmbsqq3qmH1/tFj80Mr1h8rvzemXlbtLlgOOw8fxrRpD65S5Oq5/mbxidE/L6nu0xeMmhYRw1bleJVS0ef8ImIS2VDVzGpFaVPaTs/v9ppZLiJ7u6mrc/Azs9w88jOzulQLq7o4+JlZPr7mZ2b1SMiLmZpZffLIz8zqkq/5mVn98TU/M6tH2bu9XT/6OfiZWW41EPsc/MwsP7/hYWb1R572mlkdal7Pr6tz8DOznMqznl+1df3HtM2sw5VjJeciScsHSro/JSC/XlL3VN4jfZ+V9m9c0NYpqfwpSXuVcg4OfmaWj7IbHqVsbWgtafn5wMURMQh4Azg21T8WeCMiNgUuTvVIKXEPA7Yiy9f7i5Q6tygHPzPLpfk5v1VNYJQytLWUtHx34MZUPo4siRFkqW/Hpc83Ap9LSY72AyZExOKIeJ4sx0dzxrdWOfiZWW6VSloOPAu8GRFLU5XClLfL0+Gm/QuBdWhn0nLf8DCz3HLc75hfLIdHRCwDhqQUljcBg1uq1nzYVvZ1uqTlZlajKpi0fEegt6TmgVlhytvl6XDT/rWBBXTCpOVmVotKvNNbwt3elpKWPwH8DTg4VRsN3JI+T0zfSfv/mtJZTgQOS3eDBwKDgAfaOg1Pe80sl2wx07I85zcAGJfuzDYAN0TErZIeByZIOht4GLgy1b8SuEbSLLIR32EAETFT0g3A48BS4IQ0nS7Kwc/McmuobNLy52jhbm1ELAIOaaWtMUDRvOArc/Azs9xq4AUPBz8zy0e1vrCBpLWK/TAi/l3+7phZV1ADK1oVHfnN5KPP0DR/D2CjCvbLzDqxml7PLyI2bG2fmdUvkd3x7epKes5P0mGSfpg+f1zSdpXtlpl1Zg0qbevM2gx+ki4DdgO+nIreBX5VyU6ZWSdW4tsdnf2mSCl3e3eKiKGSHgaIiAXN62uZWX3q5HGtJKUEvyWSGkgvCktaB/igor0ys05LlOch52orJfhdDvwBWDettHoocGZFe2VmnVpN3+1tFhHjJU0je+kY4JCIeKyy3TKzzqqURQu6glLf8GgElpBNfb0SjFmdq4Vpbyl3e08FrgM+RrZO1u8knVLpjplZ56USt86slJHfUcB2EfEugKQxwDTg3Ep2zMw6r87+GEspSgl+s1eq1wQ8V5numFlnl93trXYvVl2xhQ0uJrvG9y4wU9Lk9H0kcHfHdM/MOh2VbTHTqip2ze8xssUNbgPOAO4F7gPOAv5a8Z6ZWadVjjc8JG0o6W+SnkhJy7+dys+Q9LKk6Wnbp+A3LSYnlzQqlc2SdHIp51BsYYMrW9tnZvWrjNPepcB3I+IhSb2AaZKmpH0XR8RFKxx3xeTkHwP+ImmztPtyYE+yZEZTJU2MiMeLHbzNa36SNiFbHnpLoGdzeURs1uqPzKymleOGR0TMAeakz29JeoLi+XaXJycHnk+5PJqXu5+Vlr9H0oRUt2jwK+WZvauBq8gC/t7ADcCEEn5nZjUqx6MuRZOWL29P2pgsn8f9qehESTMkjZXUJ5W1lpy8XUnLSwl+q0fEZICIeDYiTiNb5cXM6pAEjQ0qaSMlLS/Yrvhoe1qT7BXa76QV4n8JbAIMIRsZ/qS5agvdaXfS8lIedVmsbIz7rKSvAy8D/Uv4nZnVqHI95yepG1ng+21E/BEgIuYW7P81cGv6Wiw5eUWSlv8XsCbwn8DOwHHAV0v4nZnVqDIlLRdZLt4nIuKnBeUDCqodQPbkCbSenHwqMEjSwLTc3mGpblGlLGzQPAd/iw8XNDWzOiVUrnd7dyaLKY9Kmp7KfggcLmkI2dT1BeA/oHhyckknApPJ1iEYGxEz2zp4sYecb6LIvDkiDmzz1Mys9pRpVZeIuJuWr9dNKvKbFpOTR8SkYr9rSbGR32V5GiqHIYM34p77ft7Rh7VVsN3pd1S7C5bDc6+UJ+NsTb/bGxF3dmRHzKxrENBYy8HPzKw1NfBqr4OfmeVXV8FPUo/0WomZ1bHsMZauH/1KWcl5B0mPAs+k79tI8l0JszpWF0nLgUuBfYHXASLiEfx6m1ldK8dDztVWyrS3ISJmrzTMXVah/phZJyegqbNHthKUEvxelLQDEJIagW8BT1e2W2bWmdVA7Csp+H2DbOq7ETAX+EsqM7M6JJXt9baqKuXd3nlkLwqbmQF1MvJLS8p85B3fiGhxUUIzq32d/U5uKUqZ9v6l4HNPsiVmXmylrpnVOEHzQqVdWinT3usLv0u6BpjSSnUzq3Vd4Bm+UrTn9baBwCfK3REz6zrU4kpUXUsp1/ze4MNrfg3AAqCkvJhmVnvKmLqyqoq+4ZGWmd4GWDdtfSLikxFxQ0d0zsw6p3K83lYkaXlfSVMkPZP+7JPKJenSlJh8hqShBW2NTvWfkTS6pHMotjMiArgpIpalrc2MSGZW+ySVtLWhOWn5YGBH4ISUmPxk4M6IGATcyYczzb3J8nYMAo4ny/KGpL7A6cBwsjy+pxeku2xVKe/2PlAYYc2svmWpK0vbiomIORHxUPr8FtCctHw/YFyqNg7YP33eDxgfmfuA3inZ0V7AlIhYEBFvkN2QHdXWeRTL4dEUEUuBXYDjJD0LvEM25Y+IcEA0q1M53vDoJ+nBgu9XtJK7d2M+TFq+XkTMgSxASmpOlVvWpOXFbng8AAzlw6hrZpb3hsf8iBhWtL2VkpYXmS53WNJyAUTEs201Ymb1pVyvt7WUtByYK2lAGvUNAOal8taSlr8EjFip/K62jl0s+K0r6aTWdhYmGTazeiIayvCcX2tJy8kSjo8Gzkt/3lJQfqKkCWQ3NxamADkZOKfgJsdI4JS2jl8s+DUCa9LykNLM6pQo28ivtaTl5wE3SDoW+D/gkLRvErAPMAt4FzgGICIWSPoxMDXVOysiFrR18GLBb05EnJXzZMys1gmayvCUc5Gk5QCfa6F+ACe00tZYYGye47d5zc/MrFAZR35VVSz4fSTymplBrkddOq1Wg18pc2Yzq081EPuctNzM8hGlvRrW2Tn4mVk+qvFpr5lZS7I3PBz8zKwOdf3Q5+BnZu1QAwM/Bz8zy6uktfo6PQc/M8vFd3vNrG75hoeZ1R/haa+Z1R9Pe82sbnnkZ2Z1qeuHPgc/M8tJQGMNjPxqYepuZh1MKm1rux2NlTRP0mMFZWdIelnS9LTtU7DvlJS0/ClJexWUj0plsySdvPJxWuLgZ2Y5qeT/leBqWs6xe3FEDEnbJICU0PwwYKv0m19IapTUCFxOltR8S+DwVLcoT3vNLLdyzXoj4h8pZ28p9gMmRMRi4HlJs4Ad0r5ZEfFc1jdNSHUfL9aYR35mlkv2qItK2khJywu240s8zImSZqRpcXNWtrImLXfwM7N8Srzel0aH8yNiWMF2RQlH+CWwCTAEmAP85MMjf0RFkpabmbWokq+3RcTc5s+Sfg3cmr62lrScIuWt8sjPzHLJFjMtbWtX+9KAgq8HAM13gicCh0nqIWkgMAh4gCxf7yBJAyV1J7spMrGt43jkZ2a5lXgnt+12pOuAEWTXBl8CTgdGSBpCNnV9AfgPgIiYKekGshsZS4ETImJZaudEYDLQCIyNiJltHdvBz8xyK+Pd3sNbKL6ySP0xwJgWyicBk/Ic28FvFb304ot87aujmfvqqzQ0NPDVrx3HCd/6Nj88+ftMuvVWunfvzsBPbsL//mYsvXv35s6/TOFHp57Ckvffp1v37pxz3gWM2G33ap9Gzeve1MD447ane2MDjQ3ijplzufzOZznrgC3ZeoO1QTB7/ruc+ofHePf9ZXRrFOce/Cm22mAt3nx3Cd+d8AivvLmItVfrxiVHbMPWG6zFzQ+/wpg/PVntU6uKco38qqli1/xaenK7FjU2NXHuBRfx8KOPc9fd9/K/v/wFTzz+OLt/bk8enP4oDzz0CIMGDeKi888FYJ11+nHjTROZ+vAMfn3l1Rx7zNFVPoP68P7SD/jqlQ9y4GX3ctBl97LLoH58esO1OX/SUxx42b0c+PN7mfPmexyxY3bd/KBhH+ffi5aw90/vZvw9szlpr82Wt/Pzv8ziwj8/Xc3TqapKX/PrKJW84XE1LT+5XVMGDBjAttsOBaBXr15svsVgXnnlZfbYcyRNTdnAevvhO/Lyyy8DMGTbbfnYxz4GwJZbbcXiRYtYvHhxdTpfZ959fxkATY2iqVFEwDuLly3f36NbI5EekNh98Lrc8lB2w/COmXPZcZO+ALy3ZBkPzX6T95d80LGd70wkGkrcOrOKTXtzPrldE2a/8AKPPPIw2+8wfIXy8VdfxcGHHPqR+jf/8Q9sM2RbevTo0VFdrGsNgt+fsCMb9V2d6+5/kUdfWgjA2Qduxa6b9+O5ee9w4e1PAdB/rZ68unARAMs+CN5atJTeq3fjzXeXVK3/nUnnDmulqfo1v/TE9/EAG260UZV7035vv/02h3/pYC646GLWWmut5eXnnzuGpqYmDjviyBXqPz5zJqedejJ/um1yR3e1bn0QcNBl99GrZxOXHjmETfuvyax5b3PaH2fSIDj1C4MZ9an1ufmhV1p+arbNx2brQ63k7a36c34RcUXz09/9+q1b7e60y5IlSzjiSwdz2OFHsP8BBy4vv3b8OG6fdBtXjb92hcUfX3rpJQ475EB+M3Ycn9xkk2p0ua69tWgpDzy/gF02W2d52QcBt894lT23Wg+Auf9exPpr9wSgsUH06tnEwvc86mumErfOrOrBr6uLCL5x/NfYfIst+M/vnLS8/I7Jf+anF13A7/94C6uvvvry8jfffJOD9tuXs84+h8/stHM1ulyX+qzejV49s4lOj6YGPrPJOrww/1026rva8jojtliX5197B4C/PfEa+w3Nrs2O3Go97n9uQcd3ujOrgehX9WlvV3fvv+7hd7+9hq23/hTDh20LwJk/HsP3Tvo2ixcvZt+9RwKww/Dh/PzyX/GrX1zGs8/O4txzzubcc84G4E+TJtO/f/+qnUM9WLdXD845eGsaGrIL8ZMffZW/P/Ua1xy3PWv0aEIST815i7MmZguB/GHay5x38NbcftIuLHxvCd+bMGN5W3d8b1fW7NFEt0ax++D+HH/VNJ5NQbNe1MK0V1GhCxmFT24Dc4HTI6LVhxcBhm43LO65b2pF+mOVMeyMKdXuguXw3NgTeW/O06sUuQZ/atsYf8tdJdXdYZPe0yJi2Kocr1Iqebe3pSe3zawWdP2Bn6e9ZpZPdjmv60c/Bz8zy6fE/BydnYOfmeVWA7HPwc/M8pKTlptZfaqB2OfgZ2b5dIHnl0viNzzMLL8yveHRStLyvpKmSHom/dknlUvSpSkx+QxJQwt+MzrVf0bS6FJOwcHPzHKrcNLyk4E7I2IQcGf6DllS8kFpO54syxuS+pItfz+cLI/v6QXpLlvl4GdmueVIXVlURPwDWPnF6f2AcenzOGD/gvLxkbkP6J2SHe0FTImIBRHxBjCFEtYS9TU/M8sn33N+/SQ9WPD9ihJy964XEXMAImKOpOYX38uatNzBz8xyy/GGx/wyvttb1qTlnvaaWS6ifNPeVsxtzt2b/pyXyltLWl4smXmrHPzMLLcKL+c3EWi+YzsauKWg/Oh013dHYGGaHk8GRkrqk250jExlRXnaa2b5lelBv1aSlp8H3CDpWOD/gENS9UnAPsAs4F3gGICIWCDpx0DzenhnRUSbq886+JlZbuVazLTI0nefa6FuACe00s5YYGyeYzv4mVlutfCGh4OfmeVXA9HPwc/McvFipmZWn7yYqZnVqxqIfQ5+ZpaXFzM1szpVA7HPwc/M8qmVxUwd/MwsvxqIfg5+ZpabH3Uxs7rka35mVn8EDQ5+Zlafun70c/Azs1yaFzPt6hz8zCy3Goh9Dn5mll8tjPy8jL2Z5SappK2Edl6Q9Kik6c1Z3tqTtLw9HPzMLLdiodlNAAAFRElEQVQy5/DYLSKGFGR5y5W0vL0c/Mwsl1Izt63C1Dhv0vJ2cfAzs9xU4v9IScsLtuNXaiqAOyRNK9i3QtJyoK2k5e3iGx5mll/po7q2kpbvHBGvSOoPTJH0ZM6jtpmcvDUe+ZlZbuW65hcRr6Q/5wE3ATuQP2l5uzj4mVlOokGlbUVbkdaQ1Kv5M1my8cfIn7S8XTztNbNcyviGx3rATemRmCbgdxHxZ0lTyZG0vL0c/MysKiLiOWCbFspfJ2fS8vZw8DOz3GrhDQ8HPzPLzYuZmln9cd5eM6tHXtLKzOqWp71mVpc88jOzulQDsc/Bz8zaoQain4OfmeUiaPPVta5A2UPTnYOk14DZ1e5HBfQD5le7E5ZLrf47+0RErLsqDUj6M9k/n1LMj4hRq3K8SulUwa9WSXqwjWV9rJPxv7Pa51VdzKwuOfiZWV1y8OsYV1S7A5ab/53VOF/zM7O65JGfmdUlBz8zq0sOfhUkaZSkp1KG+ZPb/oVVm6SxkuZJeqzafbHKcvCrEEmNwOVkWea3BA6XtGV1e2UluBrolA/lWnk5+FXODsCsiHguIt4HJpBlnLdOLCL+ASyodj+s8hz8Kqes2eXNrLwc/CqnrNnlzay8HPwqp6zZ5c2svBz8KmcqMEjSQEndgcPIMs6bWSfg4FchEbEUOBGYDDwB3BARM6vbK2uLpOuAe4HNJb0k6dhq98kqw6+3mVld8sjPzOqSg5+Z1SUHPzOrSw5+ZlaXHPzMrC45+HUhkpZJmi7pMUm/l7T6KrQ1QtKt6fMXi606I6m3pG+24xhnSPpeqeUr1bla0sE5jrWxV2KxPBz8upb3ImJIRGwNvA98vXCnMrn/nUbExIg4r0iV3kDu4GfWmTn4dV3/BDZNI54nJP0CeAjYUNJISfdKeiiNENeE5esLPinpbuDA5oYkfUXSZenzepJukvRI2nYCzgM2SaPOC1O970uaKmmGpDML2jo1rWH4F2Dztk5C0nGpnUck/WGl0ewekv4p6WlJ+6b6jZIuLDj2f6zqP0irTw5+XZCkJrJ1Ah9NRZsD4yNiW+Ad4DRgj4gYCjwInCSpJ/Br4AvArsD6rTR/KfD3iNgGGArMBE4Gnk2jzu9LGgkMIlu2awiwnaT/J2k7stf4tiULrtuXcDp/jIjt0/GeAArfqNgY+CzweeBX6RyOBRZGxPap/eMkDSzhOGYraKp2ByyX1SRNT5//CVwJfAyYHRH3pfIdyRZPvUcSQHey17W2AJ6PiGcAJF0LHN/CMXYHjgaIiGXAQkl9VqozMm0Pp+9rkgXDXsBNEfFuOkYp7zJvLelssqn1mmSvAza7ISI+AJ6R9Fw6h5HApwuuB66djv10CccyW87Br2t5LyKGFBakAPdOYREwJSIOX6neEMq3pJaAcyPif1c6xnfacYyrgf0j4hFJXwFGFOxbua1Ix/5WRBQGSSRtnPO4Vuc87a099wE7S9oUQNLqkjYDngQGStok1Tu8ld/fCXwj/bZR0lrAW2SjumaTga8WXEvcQFJ/4B/AAZJWk9SLbIrdll7AHEndgCNX2neIpIbU508CT6VjfyPVR9JmktYo4ThmK/DIr8ZExGtpBHWdpB6p+LSIeFrS8cBtkuYDdwNbt9DEt4Er0momy4BvRMS9ku5Jj5Lcnq77DQbuTSPPt4GjIuIhSdcD04HZZFPztvwIuD/Vf5QVg+xTwN+B9YCvR8QiSb8huxb4kLKDvwbsX9o/HbMPeVUXM6tLnvaaWV1y8DOzuuTgZ2Z1ycHPzOqSg5+Z1SUHPzOrSw5+ZlaX/j83REnLJqrdhQAAAABJRU5ErkJggg==\n",
      "text/plain": [
       "<Figure size 432x288 with 2 Axes>"
      ]
     },
     "metadata": {},
     "output_type": "display_data"
    },
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "confusion matrix of SVM of Doc2vec using distributed memory\n"
     ]
    }
   ],
   "source": [
    "plot_cmat(y_test_dm, y_pred)\n",
    "print(\"confusion matrix of SVM of Doc2vec using distributed memory\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": None,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
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
   "version": "3.7.0"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 2
}
