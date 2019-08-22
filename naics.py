import pickle
from pyspark import SparkContext
from pyspark.ml import Pipeline
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.feature import CountVectorizer, HashingTF, IDF, RegexTokenizer, StopWordsRemover, StringIndexer
from pyspark.ml.tuning import ParamGridBuilder, CrossValidator
from pyspark.sql import SQLContext

from config import BUILDDIR, DATADIR


spark = SQLContext(SparkContext.getOrCreate())


def main():

    # read data
    yahoo = spark.read.csv(f'{BUILDDIR}/yahoo.csv', header=True)
    data = yahoo.select(['sector', 'description']).dropna()

    # tokenize texts based on regular expression
    tokenize = RegexTokenizer(inputCol='description', outputCol='words_all', pattern='\\W')

    # remove stop words
    stopwords = '\n'.join((DATADIR/'stopwords'/f).read_text().strip() for f in ('mysql.txt', 'nltk.txt')).splitlines()
    remove_stopwords = StopWordsRemover(inputCol='words_all', outputCol='words_clean').setStopWords(stopwords)

    # get words frequency using simple count (bag of words)
    add_wordcount = CountVectorizer(inputCol='words_clean', outputCol='words_count', vocabSize=10000, minDF=5)

    # get tf-idf words frequencies

    add_wordtf = HashingTF(inputCol='words_clean', outputCol='words_tf', numFeatures=10000)
    add_wordidf = IDF(inputCol='words_tf', outputCol='words_tfidf', minDocFreq=5)

    # prepare output values
    index_target = StringIndexer(inputCol='sector', outputCol='label')

    # data preparation pipeline
    pipeline_wordcount = Pipeline(stages=[
        tokenize,
        remove_stopwords,
        add_wordcount,
        add_wordtf,
        add_wordidf,
        index_target,
        ])
    # apply data preparation pipeline
    model_wordcount = pipeline_wordcount.fit(data)
    prepared = model_wordcount.transform(data)

    # split to training and testing
    training, testing = prepared.randomSplit([0.7, 0.3], seed=100500)

    # fit logistic regression models

    logistic_wordcount = LogisticRegression(regParam=0.3, elasticNetParam=0,
        featuresCol='words_count', labelCol='label', predictionCol='prediction', probabilityCol='probability')

    logistic_tfidf = LogisticRegression(regParam=0.3, elasticNetParam=0,
        featuresCol='words_tfidf', labelCol='label', predictionCol='prediction', probabilityCol='probability')

    for model, name in (
            (logistic_wordcount, 'Word count + Logistic regression'),
            (logistic_tfidf, 'TF-IDF + Logistic regression')):
        predicted = model.fit(training).transform(testing)
        evaluator = MulticlassClassificationEvaluator(predictionCol='prediction', metricName='accuracy')
        print(f'{name} model accuracy = {evaluator.evaluate(predicted)}')

    # fit hyperparameters
    grid = (ParamGridBuilder()
        .addGrid(logistic_wordcount.regParam, [0.1, 0.2, 0.3, 0.4])
        .addGrid(logistic_wordcount.elasticNetParam, [0.0, 0.1, 0.2, 0.3])
        .build()
        )
    cv = CrossValidator(
        estimator=logistic_wordcount,
        )



if __name__ == '__main__':
    main()
