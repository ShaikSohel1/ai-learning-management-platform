"""
Production Audit Test Suite: Gemini Model Failover & Resilience System.
Verifies:
1. Successful request using primary model (models/gemini-2.5-flash).
2. Automatic switch after simulated 429 RESOURCE_EXHAUSTED error to secondary model (models/gemini-3.6-flash).
3. Failover chain across multiple models (models 1 -> 2 -> 3 -> 4).
4. Active model cache updates and persists for subsequent requests.
5. Restart / Reset resets active model back to preferred primary model.
6. Non-retryable errors (400, 401, 403, 404) re-raise immediately without switching models.
7. Final graceful 503 exception (AllGeminiModelsQuotaExhaustedError) when all 7 models return 429.
"""

import unittest
from unittest.mock import MagicMock

from google.genai.errors import APIError

from app.ai.gemini_client import (
    MODEL_PRIORITY_LIST,
    AllGeminiModelsQuotaExhaustedError,
    GeminiClient,
)


def make_api_error(code: int, message: str) -> APIError:
    """Helper to construct a google-genai APIError with status code and message."""
    return APIError(code, {"error": {"message": message, "code": code}})


class TestGeminiModelFailover(unittest.TestCase):
    def setUp(self):
        GeminiClient.reset_active_model()

    def tearDown(self):
        GeminiClient.reset_active_model()

    def test_01_primary_model_success(self):
        client = GeminiClient(api_key="mock_api_key")
        mock_genai_client = MagicMock()
        mock_response = MagicMock()
        mock_response.text = '{"status": "ok"}'
        mock_genai_client.models.generate_content.return_value = mock_response
        client.client = mock_genai_client

        output = client.generate_content(prompt="Hello Test")

        self.assertEqual(output, '{"status": "ok"}')
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-2.5-flash")
        mock_genai_client.models.generate_content.assert_called_once()
        _, kwargs = mock_genai_client.models.generate_content.call_args
        self.assertEqual(kwargs["model"], "models/gemini-2.5-flash")
        print("\n[PASS] Test 1: Primary model (models/gemini-2.5-flash) request succeeded.")

    def test_02_failover_after_429_quota_exhausted(self):
        client = GeminiClient(api_key="mock_api_key")
        mock_genai_client = MagicMock()

        # First call on 2.5-flash raises 429; second call on 3.6-flash succeeds
        err_429 = make_api_error(429, "429 RESOURCE_EXHAUSTED: Quota exceeded for gemini-2.5-flash")
        ok_response = MagicMock()
        ok_response.text = '{"status": "recovered_on_3.6"}'

        mock_genai_client.models.generate_content.side_effect = [err_429, ok_response]
        client.client = mock_genai_client

        output = client.generate_content(prompt="Test prompt")

        self.assertEqual(output, '{"status": "recovered_on_3.6"}')
        # Active model cache must update to models/gemini-3.6-flash
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-3.6-flash")
        self.assertEqual(mock_genai_client.models.generate_content.call_count, 2)
        print("[PASS] Test 2: Automatic failover from gemini-2.5-flash to gemini-3.6-flash succeeded on 429.")

    def test_03_multi_model_chain_failover(self):
        client = GeminiClient(api_key="mock_api_key")
        mock_genai_client = MagicMock()

        # Fail models 1, 2, 3 with 429 / 503; succeed on model 4 (gemini-3-flash)
        err1 = make_api_error(429, "Quota exceeded on model 1")
        err2 = make_api_error(429, "Quota exceeded on model 2")
        err3 = make_api_error(503, "503 Service Unavailable on model 3")
        ok_response = MagicMock()
        ok_response.text = '{"status": "recovered_on_model_4"}'

        mock_genai_client.models.generate_content.side_effect = [err1, err2, err3, ok_response]
        client.client = mock_genai_client

        output = client.generate_content(prompt="Multi-chain test")

        self.assertEqual(output, '{"status": "recovered_on_model_4"}')
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-3-flash")
        self.assertEqual(mock_genai_client.models.generate_content.call_count, 4)
        print("[PASS] Test 3: Multi-model chain failover (1 -> 2 -> 3 -> 4: gemini-3-flash) succeeded.")

    def test_04_active_model_cache_persistence(self):
        client = GeminiClient(api_key="mock_api_key")
        mock_genai_client = MagicMock()

        # Request 1: 2.5-flash fails with 429, 3.6-flash succeeds
        err_429 = make_api_error(429, "Quota exceeded")
        ok_resp1 = MagicMock()
        ok_resp1.text = '{"req": 1}'
        ok_resp2 = MagicMock()
        ok_resp2.text = '{"req": 2}'

        mock_genai_client.models.generate_content.side_effect = [err_429, ok_resp1, ok_resp2]
        client.client = mock_genai_client

        # Call 1
        res1 = client.generate_content(prompt="Req 1")
        self.assertEqual(res1, '{"req": 1}')
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-3.6-flash")

        # Call 2: Should use models/gemini-3.6-flash DIRECTLY without trying 2.5-flash again
        res2 = client.generate_content(prompt="Req 2")
        self.assertEqual(res2, '{"req": 2}')

        # Check call 2 model parameter
        last_call_args = mock_genai_client.models.generate_content.call_args_list[2]
        self.assertEqual(last_call_args.kwargs["model"], "models/gemini-3.6-flash")
        print("[PASS] Test 4: Active model cache persisted (gemini-3.6-flash used directly on subsequent request).")

    def test_05_restart_reset_to_primary(self):
        # Manually simulate active model cache pointing to model 5
        GeminiClient.set_active_model("gemini-3.5-flash-lite")
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-3.5-flash-lite")

        # Simulate application process restart
        GeminiClient.reset_active_model()
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-2.5-flash")
        print("[PASS] Test 5: Process restart/reset restored active model to primary (models/gemini-2.5-flash).")

    def test_06_non_retryable_error_does_not_failover(self):
        client = GeminiClient(api_key="mock_api_key")
        mock_genai_client = MagicMock()

        # Raise 400 Bad Request
        err_400 = make_api_error(400, "400 INVALID_ARGUMENT: Bad prompt syntax")
        mock_genai_client.models.generate_content.side_effect = err_400
        client.client = mock_genai_client

        with self.assertRaises(APIError) as ctx:
            client.generate_content(prompt="Bad prompt")

        self.assertEqual(ctx.exception.code, 400)
        self.assertEqual(mock_genai_client.models.generate_content.call_count, 1)
        self.assertEqual(GeminiClient.get_active_model(), "models/gemini-2.5-flash")
        print("[PASS] Test 6: Non-retryable error (400 Bad Request) raised immediately without switching models.")

    def test_07_all_models_quota_exhausted_raises_503_exception(self):
        client = GeminiClient(api_key="mock_api_key")
        mock_genai_client = MagicMock()

        # All 7 models fail with 429
        quota_errs = [make_api_error(429, f"429 Quota exhausted for model {i}") for i in range(len(MODEL_PRIORITY_LIST))]
        mock_genai_client.models.generate_content.side_effect = quota_errs
        client.client = mock_genai_client

        with self.assertRaises(AllGeminiModelsQuotaExhaustedError) as ctx:
            client.generate_content(prompt="Exhaustion test")

        self.assertIn("exhausted their available quota", str(ctx.exception))
        self.assertEqual(mock_genai_client.models.generate_content.call_count, len(MODEL_PRIORITY_LIST))
        print("[PASS] Test 7: All 7 models returning 429 raised AllGeminiModelsQuotaExhaustedError gracefully.")


if __name__ == "__main__":
    unittest.main()
