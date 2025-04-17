import pytest
import os
from unittest.mock import patch, Mock

from llm import Fragment, Template


def test_jina_reader_loader():
    from llm_jina_reader import jina_reader_loader

    with patch("llm_jina_reader._get_jina_response") as mock_get_response:
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "This is the Jina content"
        mock_get_response.return_value = mock_response

        # Test loading a fragment
        fragments = jina_reader_loader("https://example.com/content")

        # Verify the fragment content
        assert len(fragments) == 1
        assert fragments[0] == "This is the Jina content"
        assert fragments[0].source == "https://r.jina.ai/https://example.com/content"


def test_jina_reader_loader_error():
    from llm_jina_reader import jina_reader_loader

    with patch("llm_jina_reader._get_jina_response") as mock_get_response:
        # Mock failed response
        mock_get_response.side_effect = ValueError("Could not load content")

        # Test loading a non-existent resource
        with pytest.raises(ValueError, match="Could not load content"):
            jina_reader_loader("https://example.com/not-found")


def test_file_template_loader():
    from llm_jina_reader import file_template_loader

    with patch("llm_jina_reader._get_jina_response") as mock_get_response:
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "This is the template content"
        mock_get_response.return_value = mock_response

        # Test loading a template
        with patch("builtins.print"):  # Suppress print output
            template = file_template_loader("https://example.com/template")

        # Verify the template has system content
        assert template.name == "https://example.com/template"
        assert template.system == "This is the template content"


def test_get_jina_response():
    from llm_jina_reader import _get_jina_response

    # Test with token but invalid URL
    with patch.dict(os.environ, {"JINA_READER_TOKEN": "test_token"}):
        with pytest.raises(ValueError, match="INVALID url"):
            _get_jina_response(url_path="invalid-url")

    # Test with token and valid URL
    with patch.dict(os.environ, {"JINA_READER_TOKEN": "test_token"}):
        with patch("httpx.get") as mock_get:
            mock_response = Mock()
            mock_response.status_code = 200
            mock_get.return_value = mock_response

            response = _get_jina_response(url_path="https://example.com/content")
            
            # Verify httpx.get was called with correct parameters
            mock_get.assert_called_once_with(
                "https://r.jina.ai/https://example.com/content",
                headers={"Authorization": "Bearer test_token"}
            )
            assert response == mock_response


def test_get_jina_response_http_error():
    from llm_jina_reader import _get_jina_response

    with patch.dict(os.environ, {"JINA_READER_TOKEN": "test_token"}):
        with patch("httpx.get") as mock_get:
            mock_get.side_effect = Exception("HTTP error")

            with pytest.raises(ValueError, match="Could not load content"):
                _get_jina_response(url_path="https://example.com/content")
