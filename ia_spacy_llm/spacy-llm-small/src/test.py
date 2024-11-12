import main
import pytest
import spacy


@pytest.fixture
def nlp():
    return main.load_model()


@pytest.fixture
def geosynchronization_text():
    # return """Trivia: The concept of geosynchronization was first postulated by Arthur C. Clarke.
    # Explanation: Geosynchronous orbits are orbits around Earth that have an orbital period matching Earth's rotation period.
    # This results in the satellite appearing stationary with respect to a point on Earth's surface. This concept is crucial in space physics and geodesy,
    # as it is used in various applications like communication satellites. Arthur C. Clarke, a British science fiction writer,
    # was the first to postulate this concept, which is why geosynchronous orbits are sometimes referred to as Clarke orbits."""

    return = """
        The share price of a small Chinese company in financial difficulties has skyrocketed in recent days. The company's only real asset is its name: Wisesoft, which in Chinese sounds like the phrase 'Trump wins big'. Chinese investors are prone to buying shares solely on the basis of a company name.
        Former US president Donald Trump’s influence looms large, and not just in the United States. In China, his name has prompted some people to make a quirky bet on the stock market.
        The share price of a small company that makes air traffic control software, Wisesoft, doubled over the past month on the Shenzhen Stock Exchange, a gain at odds with the company’s lacklustre financial results. It recorded a loss of Є3.5 million, (27.04 million yuan), for the first nine months of 2024.
        Wisesoft's attraction for local investors is in its name, phonetically close to the expression “Trump wins big”, notes Bloomberg News.
        """


def test_process_text_returns_expected_tuples(nlp, geosynchronization_text):
    result = main.process_text_returns_expected_tuples(nlp, geosynchronization_text)
    assert len(result) > 0, "Expected process_text to return at least one tuple, but it returned an empty list"
    assert all(isinstance(x, tuple) and len(x) == 3 for x in result), "Expected each element in the result to be a 3-tuple (text, pos, dep), but found a different structure"
    assert result[0][0] == "Trivia", "Expected the first token to be 'Trivia', but found a different token"


def test_extract_entities_returns_expected_entity_tuples(nlp, geosynchronization_text):
    result = main.extract_entities_returns_expected_entity_tuples(nlp, geosynchronization_text)
    assert len(result) > 0, "Expected extract_entities to return at least one tuple, but it returned an empty list"
    assert all(isinstance(x, tuple) and len(x) == 2 for x in result), "Expected each element in the result to be a 2-tuple (entity, entity type), but found a different structure"


def test_summarize_text_returns_expected_summary(nlp, geosynchronization_text):
    result = main.summarize_text_returns_expected_summary(nlp, geosynchronization_text)
    assert len(result) > 0, "Expected summarize_text to return at least one sentence, but it returned an empty list"
    assert all(isinstance(x, str) for x in result), "Expected each element in the result to be a string, but found a different structure"


if __name__ == '__main__':
    pytest.main()
