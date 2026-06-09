from vaderSentiment.vaderSentiment import (
    SentimentIntensityAnalyzer
)


class SentimentService:

    def __init__(self):

        self.analyzer = (
            SentimentIntensityAnalyzer()
        )

    def analyze(

        self,

        text
    ):

        scores = (
            self.analyzer
            .polarity_scores(text)
        )

        compound = scores["compound"]

        if compound >= 0.5:

            label = "POSITIVE"

        elif compound <= -0.5:

            label = "NEGATIVE"

        else:

            label = "NEUTRAL"

        return {

            "label":
                label,

            "score":
                compound
        }