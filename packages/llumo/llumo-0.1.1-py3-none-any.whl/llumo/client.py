import requests
from .exceptions import LlumoAPIError

class LlumoClient:
    """
    A client to interact with Llumo API for evaluating AI-generated responses
    
    """

    base_url = "https://app.llumo.ai/api"

    def __init__(self, api_key):
        """
        Initializes the LlumoClient with the given API key.

        Parameters:
        - api_key (str): The Llumo API key for authentication.
        """
        self.api_key = api_key


    def EvaluateGrounded(self, outputText, groundTruthText, embeddingModelName="Google", metricsName="Cosine"):
        """
        Evaluates the groundedness of a response using a similarity metric.

        Parameters:
        - outputText (str): The generated output text to evaluate.
        - groundTruthText (str): The reference ground truth text.
        - embeddingModelName (str): Name of the embedding model to use. Default is "Google".
        - metricsName (str): Similarity metric to apply (e.g., "Bleu"). Default is "Cosine".
        - test
        Returns:
        - dict: Contains statusCode, message, and evaluation data if successful.

        Raises:
        - LlumoAPIError for all specific error types.
        """
        url = f"{self.base_url}/external/grounded-external"

        requestBody = {
            "prompt": outputText,
            "groundTruth": groundTruthText,
            "embeddingModel": embeddingModelName,
            "similarityMetric": metricsName,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        try:
            res = requests.post(url=url, json=requestBody, headers=headers)

            if res.status_code == 401:
                raise LlumoAPIError.InvalidApiKey()

            res.raise_for_status()
            result = res.json()

            if 'data' not in result:
                raise LlumoAPIError.InvalidApiResponse()

            return {
                "statusCode": result['data'].get('statusCode'),
                "message": result['data'].get('message'),
                "analytics": result['data']
            }

        except requests.exceptions.HTTPError as e:
            raise LlumoAPIError.RequestFailed(str(e))
        except ValueError:
            raise LlumoAPIError.InvalidJsonResponse()
        except Exception as e:
            raise LlumoAPIError.UnexpectedError(str(e))


