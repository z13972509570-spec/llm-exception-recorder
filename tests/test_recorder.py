import pytest
from src.llm_exception_recorder import ExceptionRecorder, ErrorType
from src.llm_exception_recorder.classifiers import ErrorClassifier


class TestErrorClassifier:
    def test_classify_rate_limit(self):
        clf = ErrorClassifier()
        err = Exception("Rate limit exceeded: 429")
        assert clf.classify(err, 429) == ErrorType.RATE_LIMIT

    def test_classify_auth(self):
        clf = ErrorClassifier()
        err = Exception("Invalid API key")
        assert clf.classify(err, 401) == ErrorType.AUTH

    def test_classify_timeout(self):
        clf = ErrorClassifier()
        err = Exception("Request timeout")
        assert clf.classify(err, 504) == ErrorType.TIMEOUT

    def test_get_retry_strategy(self):
        clf = ErrorClassifier()
        s = clf.get_retry_strategy(ErrorType.RATE_LIMIT)
        assert s.max_retries == 5
        assert s.backoff_factor == 2.0

    def test_extract_tags(self):
        clf = ErrorClassifier()
        err = Exception("Rate limit exceeded")
        tags = clf.extract_tags(err, "openai")
        assert "openai" in tags
        assert "ratelimiterror" in tags
