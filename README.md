# Twitter sentiment prediction

¿Can we predict the future median SIA score of a twitter hashtag?

Is there a Trend? Is it Seasonal?
[insert  fourrier lab image here]

It's often formulated as a `classification` task [says this article](https://www.ntu.edu.sg/home/axsun/paper/sun_jasist13a.pdf).

    ```
    Because   of   the   strong   relationshipbetween viewer reviews of a movie and the revenue of themovie,  Liu  et al.  (2007)  analyzed  sentiment  informationfrom  blogs  discussing  movies  and  leveraged  the  autore-gressive  model  to  predict  movie  revenues  in  the  nearfuture. Liu et al. (2011) proposed using various regressionalgorithms  to  predict  the  satisfaction  of  web  users  whosearch   with   the   community-based   question-answeringsystem, and they found that LR yields the best experimen-tal  outcomes.
    ```

## Objective 1

1. Using Chartmetric


1. Using Twitter API to query a popular #Hashtag or #Username 


2. Generate a timeseries of the tweets

4. Bin the tweets by week, day, or hour

3. Calculate the SIA scores for each tweet.

5. Use the SIA scores and the time intervals to create a vector (evolution of SIA on a timeframe)

6. Use a supervised learning approach to predict the SIA score in a future point in time.

7. Create a Flask API to 

8. Generate a docker image

9. Deploy to Heroku

10. Visualize the prediction on an API endpoint.

11. Enrich the timeseries data, with more APIs (ie: Chartmetric)


### Investigate:
- Twitter API:
    - `Tweepy`

- NLP Libraries: 
    - `Google Cloud Natural Language API` [1](https://cloud.google.com/natural-language) | [API](https://cloud.google.com/natural-language/docs/reference/rest/?apix=true) | [Languages supported](https://cloud.google.com/natural-language/docs/languages)
    - `nltk`
    - `spacy`
    - `TextBlob`
    - `polyglot`
    - `CoreNLP`
    - `Gensim`

-  NLP Concepts:
    - `Modal Words`[1](https://dzone.com/articles/nlp-analysis-python-using)
    - `Tokenize`[1](https://en.wikipedia.org/wiki/Lexical_analysis#Tokenization) [2]()
    - `Lemma`

- Database
    - `MongoAtlas` vs `MySQL` ?

##### Prediction:    
- Libraries
    - `H2O AutoML`
    - `sklearn`
    - `Keras`

- Supervised Learning
    - `NLP models`


    - Metrics `precision`, `accuracy`, `F-measure` and `recall`

    - `RMSE` https://arxiv.org/pdf/1211.6496.pdf

##### Visualization

![Prediction comparison graph](/INPUT/compare_prediction_gt.png)
!